# phoenix_contracts/persona_delta.py

import json
from typing import Dict, List, Optional, Any
from semantic_matcher import paragraph_hash

# --- Import North Star Configuration ---
try:
    from north_star_config import GLOBAL_GUIDANCE, SECTION_MAP
except ImportError:
    # Fallback if config file is missing
    GLOBAL_GUIDANCE = "Ensure terms are fair and balanced."
    SECTION_MAP = {}

# ---------------------------------------------------------------
# 1. Helper: Noise/Header Detector
# ---------------------------------------------------------------

def _is_noise_or_header(text: Optional[str]) -> bool:
    """
    Detects if a paragraph is likely just a header, page number, 
    or empty noise that should NOT be redlined.
    
    Heuristics:
    - Empty or None
    - Very short (under 6 words) AND no terminal punctuation (., ;, :)
    - e.g. "User Materials", "1. Definitions", "Page 1 of 5"
    """
    if not text or not text.strip():
        return True
    
    t = text.strip()
    words = t.split()
    
    # If it's short and lacks sentence structure, assume it's a header
    if len(words) < 8 and not t.endswith((".", ";", ":", "”", '"')):
        return True
        
    return False

# ---------------------------------------------------------------
# 2. Build Persona Prompt
# ---------------------------------------------------------------

def build_persona_prompt(
    cp_text: Optional[str],
    tp_text: Optional[str],
    persona_instructions: str,
    role: str = "Neutral",
    rag_clauses: Optional[List[str]] = None
) -> str:
    """
    Build the LLM prompt.
    UPDATES: 
    - Instructs AI to hide "North Star" references.
    - Instructs AI to ignore headers if they slip through.
    """

    rag_text = "\n\n".join(rag_clauses) if rag_clauses else "(none)"
    cp_block = cp_text if cp_text else "(no counterparty clause present)"
    tp_block = tp_text if tp_text else "(no template clause present)"

    # Format the Section Map for the Prompt
    sections_prompt = "\n".join([f"- **{k}**: {v.strip()}" for k, v in SECTION_MAP.items()])

    return f"""
You are a contract redlining engine acting as legal counsel for the **{role.upper()}**.

### 1. FIRM-WIDE GUIDANCE (INTERNAL RULES)
Apply these rules strictly, but **DO NOT** reference "North Star", "Policy", or "AI Instructions" in your output.
Write your comments as if you are a human lawyer explaining the legal reasoning (e.g., "Standardizing venue to New York").

**Global Rules:**
{GLOBAL_GUIDANCE}

**Section-Specific Rules:**
{sections_prompt}

### 2. ASSIGNED STRATEGY
{persona_instructions}

### 3. RELEVANT PRECEDENTS (RAG)
{rag_text}

---

### TASK
Compare the Counterparty Version against the Template Version.

**COUNTERPARTY VERSION:**
\"\"\"{cp_block}\"\"\"

**TEMPLATE VERSION:**
\"\"\"{tp_block}\"\"\"

**Instructions:**
1. **Ignore Headers**: If the text is just a title (e.g., "User Materials", "Article 1"), return empty diffs unless it is factually wrong.
2. **Analyze**: Check for risks to the {role} or violations of Firm-Wide Guidance.
3. **Redline**: Generate JSON diffs.
4. **Comment**: Explain *why* you made changes using legal reasoning.

Output STRICT JSON with this schema:
{{
  "insertions": ["text to add"],
  "deletions": ["text to remove"],
  "replacements": [
     {{"from": "old text", "to": "new text"}}
  ],
  "comments": ["Legal reasoning for the change"]
}}

Rules:
- Keep comments professional and direct.
- Return empty lists if the clause is acceptable.
- Output VALID JSON ONLY.
"""


# ---------------------------------------------------------------
# 3. Normalize Model Output (Hardened against Export Errors)
# ---------------------------------------------------------------

def parse_delta_json(raw_output: str) -> Dict[str, Any]:
    """
    Extracts and cleans JSON from LLM output.
    Ensures all required keys are present and types are safe for export.
    """
    try:
        parsed = json.loads(raw_output)
    except Exception:
        # Fallback regex extraction
        import re
        match = re.search(r"\{.*\}", raw_output, flags=re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group(0))
            except Exception:
                parsed = {}
        else:
            parsed = {}

    # Normalize output containers
    deltas = {
        "insertions": parsed.get("insertions", []) or [],
        "deletions": parsed.get("deletions", []) or [],
        "replacements": parsed.get("replacements", []) or [],
        "comments": parsed.get("comments", []) or [],
    }

    # --- TYPE SAFETY ENFORCEMENT ---
    
    # 1. Ensure lists are actually lists
    if not isinstance(deltas["insertions"], list): 
        deltas["insertions"] = [str(deltas["insertions"])]
    if not isinstance(deltas["deletions"], list): 
        deltas["deletions"] = [str(deltas["deletions"])]
    if not isinstance(deltas["comments"], list): 
        deltas["comments"] = [str(deltas["comments"])]
    if not isinstance(deltas["replacements"], list): 
        deltas["replacements"] = []

    # 2. Stringify simple lists to prevent non-string crashes
    deltas["insertions"] = [str(x) for x in deltas["insertions"] if x]
    deltas["deletions"] = [str(x) for x in deltas["deletions"] if x]
    deltas["comments"] = [str(x) for x in deltas["comments"] if x]

    # 3. CRITICAL FIX: Validate Replacements
    # The error "'str' object has no attribute 'get'" happens here if the LLM 
    # returns a string inside the replacements list instead of a dict object.
    valid_replacements = []
    for item in deltas["replacements"]:
        if isinstance(item, dict) and "from" in item and "to" in item:
            valid_replacements.append(item)
    
    deltas["replacements"] = valid_replacements

    return deltas


# ---------------------------------------------------------------
# 4. Generate Paragraph Delta
# ---------------------------------------------------------------

async def generate_paragraph_delta(
    llm_generate_fn,
    cp_text: Optional[str],
    tp_text: Optional[str],
    persona_instructions: str,
    role: str = "Neutral",
    rag_clauses: Optional[List[str]] = None,
):
    """
    Generates LLM deltas for a single CP/TP clause.
    """
    
    # --- NEW: Header/Noise Filter ---
    # If the text is just "User Materials" or similar noise, skip the LLM entirely.
    if _is_noise_or_header(cp_text):
        return {
            "cp_text": cp_text,
            "tp_text": tp_text,
            "cp_hash": paragraph_hash(cp_text) if cp_text else None,
            "tp_hash": paragraph_hash(tp_text) if tp_text else None,
            "delta": {"insertions":[], "deletions":[], "replacements":[], "comments":[]} # Empty delta
        }

    prompt = build_persona_prompt(cp_text, tp_text, persona_instructions, role, rag_clauses)

    # LLM call
    raw = await llm_generate_fn(prompt, json_mode=True) 
    delta = parse_delta_json(raw)

    return {
        "cp_text": cp_text,
        "tp_text": tp_text,
        "cp_hash": paragraph_hash(cp_text) if cp_text else None,
        "tp_hash": paragraph_hash(tp_text) if tp_text else None,
        "delta": delta,
    }


# ---------------------------------------------------------------
# 5. Full Document-Level Delta Generation
# ---------------------------------------------------------------

async def generate_document_deltas(
    llm_generate_fn,
    matched_paragraphs: List[Dict[str, Any]],
    persona_instructions: str,
    role: str = "Neutral",
    rag_fetch_fn=None,
):
    """
    Applies persona delta generation across all matched clauses.
    """
    all_deltas = []

    for entry in matched_paragraphs:
        cp = entry.get("cp_text")
        tp = entry.get("tp_text")

        rag_clauses = []
        if rag_fetch_fn:
            try:
                rag_clauses = rag_fetch_fn(cp, tp)
            except Exception:
                rag_clauses = []

        delta = await generate_paragraph_delta(
            llm_generate_fn,
            cp_text=cp,
            tp_text=tp,
            persona_instructions=persona_instructions,
            role=role,
            rag_clauses=rag_clauses,
        )

        # Preserve matching metadata
        delta["similarity"] = entry.get("similarity")
        delta["cp_hash"] = entry.get("cp_hash")
        delta["tp_hash"] = entry.get("tp_hash")

        all_deltas.append(delta)

    return all_deltas