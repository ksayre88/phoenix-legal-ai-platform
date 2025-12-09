# phoenix_contracts/semantic_matcher.py

import hashlib
import re
from typing import List, Tuple, Dict, Optional
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
    
    # Split by newline
    lines = raw_text.split('\n')
    
    # Clean and filter empty lines
    cleaned = [line.strip() for line in lines if line.strip()]
    
    return cleaned

def paragraph_hash(text: str) -> str:
    """
    Create a stable hash for a paragraph.
    """
    if not text:
        return ""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

# -----------------------------------------------------------
# 3. Embedding + Similarity Functions
# -----------------------------------------------------------

def embed_paragraphs(paragraphs: List[str]) -> np.ndarray:
    if not paragraphs:
        return np.zeros((0, 384))
    model = get_embedder()
    return model.encode(paragraphs, convert_to_tensor=True)

def pairwise_match(
    cp_paragraphs: List[str],
    tp_paragraphs: List[str],
    threshold: float = 0.50, # Slightly higher threshold
) -> List[Dict[str, Optional[str]]]:
    """
    Matches CP paragraphs to TP paragraphs.
    """
    if not cp_paragraphs:
        return []

    # Prepare results structure
    results = []
    
    # If no template, just return CP paragraphs as unmatched
    if not tp_paragraphs:
        for cp in cp_paragraphs:
            results.append({
                "cp_text": cp,
                "tp_text": None,
                "cp_hash": paragraph_hash(cp),
                "tp_hash": None,
                "similarity": None,
            })
        return results

    # Embed both sides
    cp_emb = embed_paragraphs(cp_paragraphs)
    tp_emb = embed_paragraphs(tp_paragraphs)

    # Calculate Cosine Similarity
    sim_matrix = util.pytorch_cos_sim(cp_emb, tp_emb).cpu().numpy()
    
    matched_tp_indices = set()

    for i, cp_text in enumerate(cp_paragraphs):
        row = sim_matrix[i]
        best_idx = int(np.argmax(row))
        best_score = float(row[best_idx])

        if best_score >= threshold:
            tp_text = tp_paragraphs[best_idx]
            matched_tp_indices.add(best_idx)
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
                "similarity": None
            })

    return results