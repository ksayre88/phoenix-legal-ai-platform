import json
import re
import asyncio
import difflib
from typing import List, Dict, Any, Optional

# --- Imports from Core/Utils ---
from app.core.config import settings
from app.core.north_star_config import GLOBAL_GUIDANCE
from app.utils.llm_client import call_ollama_generate
from app.utils.semantic_matcher import extract_paragraphs, find_best_match_in_library

# ---------------------------------------------------------
# 1. THE PLAYBOOK (Config & Standards)
# ---------------------------------------------------------

CONTRACT_PERSONAS: Dict[str, str] = {
    "General Counsel": (
        "**ROLE**: Prudent, risk-averse General Counsel.\n"
        "**STRATEGY**: Balance risk. Ensure no uncapped liability. Demand mutual indemnification. "
        "Align with the Standard Playbook. Reject unusual one-sided terms."
    ),
    "Buyer Advocate": (
        "**ROLE**: BUYER'S Counsel.\n"
        "**STRATEGY**: Aggressively push risk to Seller. Demand strict warranties and IP ownership."
    ),
    "Seller Advocate": (
        "**ROLE**: SELLER'S Counsel.\n"
        "**STRATEGY**: Limit liability to fees paid. Disclaim all warranties. Protect IP."
    )
}

STANDARD_CLAUSE_LIBRARY = {
    "Indemnification": "Each Party shall indemnify, defend, and hold harmless the other Party from and against any and all claims, damages, liabilities, costs, and expenses (including reasonable attorneys' fees) arising out of or related to: (a) its breach of any representation or warranty; or (b) its gross negligence or willful misconduct.",
    "Limitation of Liability": "EXCEPT FOR INDEMNIFICATION OBLIGATIONS OR BREACHES OF CONFIDENTIALITY, NEITHER PARTY SHALL BE LIABLE FOR ANY INDIRECT, SPECIAL, OR CONSEQUENTIAL DAMAGES. EACH PARTY'S TOTAL LIABILITY SHALL NOT EXCEED THE TOTAL FEES PAID OR PAYABLE UNDER THIS AGREEMENT IN THE 12 MONTHS PRECEDING THE CLAIM.",
    "Confidentiality": "Recipient shall protect Discloser’s Confidential Information with the same degree of care it uses to protect its own similar information, but not less than reasonable care. Recipient shall not disclose Confidential Information to any third party without Discloser’s prior written consent.",
    "Governing Law": "This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without regard to its conflict of laws principles. Venue shall be in Delaware.",
    "Intellectual Property": "Each Party retains all right, title, and interest in and to its Background IP. Any IP created solely by a Party in performance of this Agreement shall be owned by that Party.",
    "Termination": "Either Party may terminate this Agreement for cause upon 30 days written notice of a material breach, provided such breach remains uncured. Either Party may terminate for convenience with 90 days prior written notice.",
    "Warranties": "Provider represents and warrants that the Services will be performed in a professional and workmanlike manner in accordance with industry standards."
}

PLAYBOOK_KEYWORDS = {
    "Indemnification": ["indemnify", "indemnification", "hold harmless", "defense of claims"],
    "Limitation of Liability": ["limitation of liability", "total liability", "consequential damages", "cap on liability"],
    "Confidentiality": ["confidential information", "non-disclosure", "proprietary information"],
    "Governing Law": ["governing law", "jurisdiction", "venue", "laws of"],
    "Intellectual Property": ["intellectual property", "ownership", "patent", "copyright", "work made for hire"],
    "Termination": ["termination", "term and termination", "surrender"],
    "Warranties": ["warranties", "disclaimer", "representations"]
}

FEW_SHOT_EXAMPLES = """
Example (Indemnification):
Input Clause: "Supplier shall indemnify Customer for everything."
Standard Clause: "Mutual indemnification standard."
Output: {
  "risk_score": 9,
  "reasoning": "One-sided.",
  "replacements": [{"from": "Supplier shall indemnify Customer", "to": "Each Party shall indemnify the other"}],
  "comments": ["Reverted to standard mutual indemnification."]
}
"""

# ---------------------------------------------------------
# 2. Parsing & Grounding (The Fix)
# ---------------------------------------------------------

def _is_noise(text: str) -> bool:
    if not text or len(text.strip()) < 5: return True
    if text.strip().isdigit(): return True
    return False

def check_keyword_anchor(text: str) -> Optional[str]:
    text_lower = text.lower()
    for clause_type, keywords in PLAYBOOK_KEYWORDS.items():
        for k in keywords:
            if k in text_lower:
                return clause_type
    return None

def stitch_paragraphs(paragraphs: List[str]) -> List[str]:
    stitched = []
    skip_next = False
    for i in range(len(paragraphs)):
        if skip_next:
            skip_next = False
            continue
        current = paragraphs[i].strip()
        if i + 1 < len(paragraphs):
            next_para = paragraphs[i+1].strip()
            if len(current) < 60 and len(next_para) > 50:
                merged = f"{current}\n{next_para}"
                stitched.append(merged)
                skip_next = True
                continue
        stitched.append(current)
    return stitched

def ground_redlines(original_text: str, delta: Dict[str, Any]) -> Dict[str, Any]:
    """
    CRITICAL FIX: The LLM often quotes text imperfectly (e.g. missing spaces).
    This function finds the *exact* substring in the original text that matches
    the 'from' field, and updates it. This ensures the Frontend highlights it correctly.
    """
    replacements = delta.get("replacements", [])
    if not replacements: 
        return delta

    valid_replacements = []
    
    for rep in replacements:
        search_text = rep.get("from", "")
        if not search_text: 
            continue
            
        # Use difflib to find the best approximate match
        matcher = difflib.SequenceMatcher(None, original_text, search_text)
        match = matcher.find_longest_match(0, len(original_text), 0, len(search_text))
        
        # If we found a match, check if it's actually the right text (similarity > 70%)
        if match.size > 0:
            matched_substring = original_text[match.a : match.a + match.size]
            similarity = difflib.SequenceMatcher(None, matched_substring, search_text).ratio()
            
            if similarity > 0.70:
                # SUCCESS: We found the real text in the document!
                # Update the redline to use the EXACT text from the doc.
                rep["from"] = matched_substring
                valid_replacements.append(rep)
            else:
                # Match is too weak, AI likely hallucinated a quote.
                # We keep it but flag it or leave it as is (Frontend might fail to highlight)
                valid_replacements.append(rep)
        else:
            valid_replacements.append(rep)
            
    delta["replacements"] = valid_replacements
    return delta

# ---------------------------------------------------------
# 3. Prompting
# ---------------------------------------------------------

def build_prompt(cp_text: str, standard_text: str, clause_type: str, instructions: str) -> str:
    return f"""
You are an expert Legal AI Agent.
**TASK**: Review the "Counterparty Clause" against the "Standard Playbook Provision".
**STRATEGY**: {instructions}

**OBJECTIVE**:
1. Detect if the Counterparty Clause deviates from our Standard Playbook.
2. If risky, provide a Redline (Search & Replace) to align it with the Standard.
3. Ignore minor wording differences if the legal effect is the same.

**CONTEXT**:
Clause Type: {clause_type}
Standard Playbook Version: "{standard_text}"
Counterparty Version: "{cp_text}"

{GLOBAL_GUIDANCE}

**RESPONSE FORMAT**:
Return a valid JSON object only.
{FEW_SHOT_EXAMPLES}

Your Output:
"""

def parse_delta_json(raw_output: str) -> Dict[str, Any]:
    try:
        if "```json" in raw_output:
            raw_output = raw_output.split("```json")[1].split("```")[0]
        elif "```" in raw_output:
             raw_output = raw_output.split("```")[1].split("```")[0]
        return json.loads(raw_output)
    except:
        return {"risk_score": 0, "reasoning": "Parse Error", "replacements": [], "comments": []}

# ---------------------------------------------------------
# 4. Exports
# ---------------------------------------------------------

def get_personas() -> List[Dict[str, str]]:
    return [{"name": k, "instructions": v} for k, v in CONTRACT_PERSONAS.items()]

def upsert_persona(name: str, instructions: str):
    CONTRACT_PERSONAS[name] = instructions

def delete_persona(name: str):
    if name in CONTRACT_PERSONAS:
        del CONTRACT_PERSONAS[name]

# ---------------------------------------------------------
# 5. MAIN LOGIC
# ---------------------------------------------------------

async def analyze_contract_logic(counterparty_text: str, template_text: Optional[str] = "", persona: str = "General Counsel") -> Dict[str, Any]:
    # 1. Parsing & Stitching
    raw_paragraphs = extract_paragraphs(counterparty_text)
    stitched_paragraphs = stitch_paragraphs(raw_paragraphs)
    
    # 2. Scanning & Grouping
    clause_candidates: Dict[str, List[Dict]] = {k: [] for k in STANDARD_CLAUSE_LIBRARY.keys()}
    
    for para in stitched_paragraphs:
        if _is_noise(para): continue
            
        anchor_type = check_keyword_anchor(para)
        best_match_key, score = find_best_match_in_library(para, STANDARD_CLAUSE_LIBRARY)
        
        if anchor_type:
            clause_candidates[anchor_type].append({"text": para, "score": 1.0, "method": "keyword"})
        elif score > 0.40:
            clause_candidates[best_match_key].append({"text": para, "score": score, "method": "semantic"})

    # 3. Deduplication
    final_queue = []
    for clause_type, candidates in clause_candidates.items():
        if not candidates: continue
        candidates.sort(key=lambda x: x["score"], reverse=True)
        winner = candidates[0]
        
        final_queue.append({
            "cp_text": winner["text"],
            "label": clause_type,
            "tp_text": STANDARD_CLAUSE_LIBRARY[clause_type],
            "score": winner["score"]
        })
        
        if len(candidates) > 1:
            runner_up = candidates[1]
            if runner_up["score"] > 0.85 and runner_up["text"] != winner["text"]:
                final_queue.append({
                    "cp_text": runner_up["text"],
                    "label": f"{clause_type} (Cont.)",
                    "tp_text": STANDARD_CLAUSE_LIBRARY[clause_type],
                    "score": runner_up["score"]
                })

    # 4. AI Analysis with Grounding
    persona_instr = CONTRACT_PERSONAS.get(persona, CONTRACT_PERSONAS["General Counsel"])
    sem = asyncio.Semaphore(10)

    async def analyze_item(item):
        async with sem:
            prompt = build_prompt(item["cp_text"], item["tp_text"], item["label"], persona_instr)
            try:
                raw = await call_ollama_generate(model=settings.DEFAULT_MODEL_NAME, prompt=prompt, json_mode=True)
                delta = parse_delta_json(raw)
            except Exception as e:
                print(f"LLM Error: {e}")
                return None
            
            # --- APPLY GROUNDING HERE ---
            # Fixes the 'from' text so the UI can highlight it
            delta = ground_redlines(item["cp_text"], delta)
            
            if delta.get("risk_score", 0) >= 2 or delta.get("replacements"):
                return {
                    "clause_type": item["label"],
                    "original_text": item["cp_text"],
                    "risk_score": delta.get("risk_score", 0),
                    "delta": delta,
                    # Frontend Aliases
                    "clause_name": item["label"],
                    "cp_text": item["cp_text"],
                    "section": item["label"]
                }
            return None

    tasks = [analyze_item(item) for item in final_queue]
    results = await asyncio.gather(*tasks)
    
    final_redlines = [r for r in results if r is not None]
    final_redlines.sort(key=lambda x: x["risk_score"], reverse=True)

    return {
        "status": "success",
        "diff": final_redlines,
        "match_count": len(final_redlines) 
    }