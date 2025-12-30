from fastapi import APIRouter
from typing import List, Any
from app.models.schemas import IntakeRequest, IntakeResponse, CsuiteHit
from app.services.intake import (
    build_intake_prompt, 
    _safe_parse_intake_json, 
    assign_team_owner, 
    send_intake_email
)
from app.utils.llm_client import call_ollama_generate
from app.core.config import settings

router = APIRouter()

def _build_intake_response(parsed: dict, raw: str, orig: str, watchlist: list) -> IntakeResponse:
    """
    Sanitizes LLM output into a strict Pydantic model.
    Handles type mismatches (list vs string) and validation logic.
    """
    # 1. Handle Categories (ensure list of strings)
    cats = parsed.get("categories", [])
    if isinstance(cats, str): cats = [cats]
    
    # 2. Handle Priority Score (ensure float)
    p_score = parsed.get("priority_score", 5.0)
    try:
        p_score = float(p_score)
    except:
        p_score = 5.0

    # 3. Handle Priority Label (Sanitize "High|Medium|Low" artifacts)
    raw_label = parsed.get("priority_label", "Medium")
    if "|" in raw_label or len(raw_label) > 20:
        # Fallback based on score if label is messy
        if p_score >= 9:
            p_lbl = "Critical"
        elif p_score >= 7:
            p_lbl = "High"
        elif p_score >= 4:
            p_lbl = "Medium"
        else:
            p_lbl = "Low"
    else:
        p_lbl = raw_label
    
    # 4. Handle Suggested Next Steps (Fix list->string crash)
    steps_raw = parsed.get("suggested_next_steps")
    if isinstance(steps_raw, list):
        # Convert list ["A", "B"] -> "- A\n- B"
        suggested_steps = "\n".join([f"- {s}" for s in steps_raw])
    else:
        # It's already a string or None
        suggested_steps = str(steps_raw) if steps_raw else ""

    # 5. Handle C-Suite Matches
    csuite = []
    if watchlist:
        raw_hits = parsed.get("csuite_mentions", [])
        wl = [w.lower() for w in watchlist]
        for hit in raw_hits:
            # Handle if hit is a dict or string
            if isinstance(hit, dict):
                name = hit.get("name", "")
            else:
                name = str(hit)
                
            if any(w in name.lower() or name.lower() in w for w in wl):
                csuite.append(CsuiteHit(name=name, matched_variants=[name]))

    return IntakeResponse(
        categories=[str(c) for c in cats],
        priority_label=p_lbl, 
        priority_score=p_score,
        summary=parsed.get("summary", ""),
        csuite_mentions=csuite,
        suggested_owner=parsed.get("suggested_owner"),
        suggested_next_steps=suggested_steps,       # Sanitized string
        learning_opportunities=parsed.get("learning_opportunities", []), # New field
        raw_model_output=raw,
        original_text=orig
    )

@router.post("/analyze")
async def intake_analyze(req: IntakeRequest):
    # 1. Generate Analysis with LLM
    raw = await call_ollama_generate(settings.DEFAULT_MODEL_NAME, build_intake_prompt(req), json_mode=True)
    
    # 2. Parse JSON safely
    parsed = _safe_parse_intake_json(raw)
    
    # 3. Build Response Object (using robust local builder)
    res = _build_intake_response(parsed, raw, req.email_text, req.csuite_names)
    
    # 4. Assign Team Owner (Skills & Playbook)
    res = assign_team_owner(res, req.team_profile)
    
    # 5. Send Notification (Optional)
    if req.notify_email:
        res.email_status = send_intake_email(req.notify_email, res, req.email_text)
        
    return res