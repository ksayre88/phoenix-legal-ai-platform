import hashlib
from typing import List, Tuple, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer, util

# -----------------------------------------------------------
# 1. Initialize Embedding Model (Singleton)
# -----------------------------------------------------------

_EMBED_MODEL = None

def get_embedder(model_name: str = "all-MiniLM-L6-v2"):
    global _EMBED_MODEL
    if _EMBED_MODEL is None:
        _EMBED_MODEL = SentenceTransformer(model_name)
    return _EMBED_MODEL

# -----------------------------------------------------------
# 2. Paragraph Processing
# -----------------------------------------------------------

def extract_paragraphs(raw_text: str) -> List[str]:
    """
    Splits text into non-empty paragraphs based on newlines.
    """
    if not raw_text:
        return []
    lines = raw_text.split('\n')
    cleaned = [line.strip() for line in lines if line.strip()]
    return cleaned

def paragraph_hash(text: str) -> str:
    if not text:
        return ""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

# -----------------------------------------------------------
# 3. Embedding + Similarity Functions
# -----------------------------------------------------------

def embed_paragraphs(paragraphs: List[str]):
    if not paragraphs:
        return None
    model = get_embedder()
    return model.encode(paragraphs, convert_to_tensor=True)

def find_best_match_in_library(query_text: str, library: Dict[str, str]) -> Tuple[str, float]:
    """
    REQUIRED FUNCTION: Compares a single query paragraph against the Standard Library.
    Returns: (Best_Key_Name, Score)
    """
    if not query_text or not library:
        return ("Unknown", 0.0)

    model = get_embedder()
    
    # Encode Query
    query_emb = model.encode(query_text, convert_to_tensor=True)

    # Encode Library
    keys = list(library.keys())
    values = list(library.values())
    lib_embs = model.encode(values, convert_to_tensor=True)

    # Compute Cosine Similarity
    cosine_scores = util.cos_sim(query_emb, lib_embs)[0]

    # Find Best Match
    best_idx = int(cosine_scores.argmax())
    best_score = float(cosine_scores[best_idx])
    
    return (keys[best_idx], best_score)

def pairwise_match(
    cp_paragraphs: List[str],
    tp_paragraphs: List[str],
    threshold: float = 0.50
) -> List[Dict[str, Any]]:
    """
    Matches CP paragraphs to Template paragraphs.
    """
    if not cp_paragraphs:
        return []

    # If no template, return empty match structure
    if not tp_paragraphs:
        return [{
            "cp_text": cp,
            "tp_text": None,
            "cp_hash": paragraph_hash(cp),
            "tp_hash": None,
            "similarity": 0.0
        } for cp in cp_paragraphs]

    cp_emb = embed_paragraphs(cp_paragraphs)
    tp_emb = embed_paragraphs(tp_paragraphs)
    sim_matrix = util.cos_sim(cp_emb, tp_emb).cpu().numpy()
    
    results = []

    for i, cp_text in enumerate(cp_paragraphs):
        row = sim_matrix[i]
        best_idx = int(np.argmax(row))
        best_score = float(row[best_idx])

        if best_score >= threshold:
            tp_text = tp_paragraphs[best_idx]
            results.append({
                "cp_text": cp_text,
                "tp_text": tp_text,
                "cp_hash": paragraph_hash(cp_text),
                "tp_hash": paragraph_hash(tp_text),
                "similarity": best_score
            })
        else:
            results.append({
                "cp_text": cp_text,
                "tp_text": None,
                "cp_hash": paragraph_hash(cp_text),
                "tp_hash": None,
                "similarity": 0.0
            })

    return results