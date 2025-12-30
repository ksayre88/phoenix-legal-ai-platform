import os
import re
from typing import Tuple, List, Dict, Any, Optional
from app.core.config import settings

# ---------------------------------------------------------
# 1. SMART PATH RESOLUTION
# ---------------------------------------------------------
POSSIBLE_PATHS = [
    settings.CORPUS_ROOT,                        
    os.path.expanduser("~/legal-rag"),           
    os.path.join(os.getcwd(), "legal-rag"),      
    os.path.join(os.path.dirname(__file__), "../../legal-rag") 
]

# Find the first path that actually exists
REAL_CORPUS_ROOT = next((p for p in POSSIBLE_PATHS if os.path.exists(p)), settings.CORPUS_ROOT)
print(f"[RAG] Resolved Corpus Root: {REAL_CORPUS_ROOT}")

# ---------------------------------------------------------
# 2. CONFIG & PERSONAS (Updated for Qwen)
# ---------------------------------------------------------
PERSONAS: Dict[str, Dict[str, str]] = {
    "mi": {
        "label": "Michigan Laws",
        "model": settings.DEFAULT_MODEL_NAME,
        "system": (
            "You are an expert legal research assistant for Michigan statutory law.\n"
            "INSTRUCTIONS:\n"
            "1. Answer the user's question STRICTLY based on the provided context.\n"
            "2. **EXTRACT AND QUOTE** the relevant statutory text. Do not just summarize; show the law.\n"
            "3. Cite specific statute numbers (e.g. MCL 750.540) for every quote.\n"
            "4. Format your answer by Statute Title/Number, followed by the text.\n"
            "5. If the context does not contain the answer, state 'Statute not found in database'.\n"
        ),
    },
    "ca": {
        "label": "California Laws",
        "model": settings.DEFAULT_MODEL_NAME,
        "system": (
            "You are an expert legal research assistant for California law.\n"
            "INSTRUCTIONS:\n"
            "1. Answer STRICTLY based on the provided context.\n"
            "2. **EXTRACT AND QUOTE** the relevant statutory text. Do not just summarize.\n"
            "3. Cite specific code sections (e.g. Penal Code 632).\n"
            "4. Format your answer by Code Section, followed by the text.\n"
        ),
    },
}

_STATUTE_CACHE: Dict[str, Dict[str, str]] = {}
rag_collection = None

if settings.USE_RAG_BACKEND:
    try:
        import chromadb
        from chromadb.utils import embedding_functions
        
        # Determine DB path
        possible_db = os.path.join(REAL_CORPUS_ROOT, "db")
        db_path = possible_db if os.path.exists(possible_db) else settings.RAG_DB_PATH
        
        client = chromadb.PersistentClient(path=db_path)
        embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        rag_collection = client.get_or_create_collection(
            name=settings.RAG_COLLECTION_NAME,
            embedding_function=embedding_fn,
        )
        print(f"[RAG] Loaded collection '{settings.RAG_COLLECTION_NAME}' from {db_path}")
    except Exception as e:
        print(f"[RAG] Failed to initialize Chroma: {e}")

# ---------------------------------------------------------
# 3. ROBUST METADATA EXTRACTION
# ---------------------------------------------------------

# FIX: Regex explicitly stops before trailing asterisks or parentheses
URL_RE = re.compile(r"(https?://[^\s)\*]+)")

def extract_url_from_doc(doc: str, meta: Dict[str, Any]) -> str:
    # 1. Try metadata first
    url = (meta.get("url") or "").strip()
    if url.startswith("http"): return url
    
    # 2. Try regex in the document text snippet
    m = URL_RE.search(doc)
    if m: 
        # FIX: Aggressively strip punctuation including the asterisk
        return m.group(1).strip().rstrip(").,'\"*")
    
    return ""

def get_statute_info(source: str, doc: str, meta: Dict[str, Any]) -> Tuple[str, str]:
    if source in _STATUTE_CACHE:
        return _STATUTE_CACHE[source]["title"], _STATUTE_CACHE[source]["url"]

    title, url = None, None
    
    try:
        # --- PATH RESOLUTION FIX ---
        # 1. Try exact path
        path = os.path.join(REAL_CORPUS_ROOT, source)
        
        # 2. If not found, try searching common jurisdiction subfolders (mi, ca)
        if not os.path.exists(path):
            for sub in ["mi", "ca", "michigan", "california"]:
                test_path = os.path.join(REAL_CORPUS_ROOT, sub, os.path.basename(source))
                if os.path.exists(test_path):
                    path = test_path
                    break
        
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                head = f.read(4000) 
            
            # Title Extraction
            m_title = re.search(r"^#\s+(.*)", head, flags=re.MULTILINE)
            if m_title: 
                title = m_title.group(1).strip()
            
            # URL Extraction - Restored stricter regex to avoid capturing junk
            m_url = re.search(r"\*Statute URL:\s*(https?://\S+)", head)
            if not m_url:
                # Fallback to loose regex only if strict fails
                m_url = re.search(r"Statute URL:\s*(https?://\S+)", head, re.IGNORECASE)
            
            if m_url: 
                # FIX: Ensure we strip any trailing asterisks captured here too
                url = m_url.group(1).strip().rstrip("*")
                
    except Exception as e:
        print(f"[RAG] Error reading source file {source}: {e}")

    # Fallbacks if file parsing failed
    if not title: 
        title = meta.get("title")
    if not title:
        base = os.path.basename(source).rsplit(".", 1)[0]
        title = base.replace("_", " ").replace("-", " ").title()
        
    if not url: 
        url = extract_url_from_doc(doc, meta)

    info = {"title": title, "url": url}
    _STATUTE_CACHE[source] = info
    return title, url

def infer_jurisdiction(meta: Dict[str, Any]) -> str:
    url = (meta.get("url") or "").lower()
    source = (meta.get("source") or "").lower()
    if "legislature.mi.gov" in url or "michigan" in source or "mcl" in source: return "MI"
    if "leginfo.legislature.ca.gov" in url or "california" in source: return "CA"
    return "UNK"

def get_rag_context_for_persona(question: str, persona_id: str, k: int = 5) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Retrieve context.
    FIX: Cap at 10 results max to prevent context overflow with Qwen 14B (8k limit).
    """
    if rag_collection is None: return "", []
    target_jur = "MI" if persona_id == "mi" else "CA" if persona_id == "ca" else None
    
    try:
        result = rag_collection.query(query_texts=[question], n_results=60)
        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
    except:
        return "", []

    context_pieces, sources = [], []
    seen_content = set()
    idx_counter = 1

    # --- SAFETY LIMIT ---
    # Max 10 chunks to stay under 8k tokens. 
    MAX_CHUNKS = 10 

    for doc, meta in zip(docs, metas):
        if doc in seen_content: continue
        seen_content.add(doc)
        
        jur = infer_jurisdiction(meta)
        if target_jur and jur != target_jur: continue
        
        source = meta.get("source", "unknown")
        
        # Pass source to helper to resolve URL/Title from disk
        title, url = get_statute_info(source, doc, meta)

        context_pieces.append(f"[{idx_counter}] [{jur}] {title}\nCitation: {title}\n{doc}\n")
        sources.append({
            "index": idx_counter, 
            "source": source, 
            "title": title, 
            "url": url, 
            "jurisdiction": jur, 
            "snippet": doc[:400]
        })
        idx_counter += 1
        
        # STOP if we hit the limit
        if len(context_pieces) >= MAX_CHUNKS: 
            break

    return "\n\n".join(context_pieces), sources

def build_prompt(persona_id: str, question: str, context: Optional[str]) -> str:
    """
    Builds a prompt optimized for Qwen/Llama 3.
    """
    persona = PERSONAS[persona_id]
    
    # Qwen instruction format works best with clear delimiters
    base = (
        f"{persona['system']}\n"
        "You have access to the following statutes:\n"
        "=========================================\n"
    )
    
    if context:
        base += context
    else:
        base += "No matching statutes found in database."
        
    base += (
        "\n=========================================\n"
        f"USER QUESTION: {question}\n\n"
        "ANALYSIS:"
    )
    return base