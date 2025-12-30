import json
import re
import smtplib
from email.message import EmailMessage
from typing import Dict, Any, List, Optional
from app.models.schemas import IntakeRequest, IntakeResponse, CsuiteHit
from app.core.config import settings

# ---------------------------------------------------------
# PROMPT ENGINEERING
# ---------------------------------------------------------
def build_intake_prompt(req: IntakeRequest) -> str:
    """
    Constructs the detailed prompt for the Intake LLM.
    """
    base = (
        "You are an expert Legal Intake Triage Assistant. Your job is to analyze incoming requests, "
        "categorize them, assign a priority, and extract key details.\n\n"
        
        "### PRIORITY LEVELS (Select ONE)\n"
        "- Critical (10): Law enforcement, Data Breach, 'Urgent' in subject, restraining orders.\n"
        "- High (8): C-Suite requests, threatened litigation, imminent deadlines (< 24 hrs).\n"
        "- Medium (5): Standard contract reviews, compliance questions, tax issues.\n"
        "- Low (2): General info requests, spam, internal FYI.\n\n"
        
        "### OUTPUT FORMAT (Strict JSON)\n"
        "Return strictly valid JSON. Do not add markdown formatting.\n"
        "{\n"
        "  \"categories\": [\"Litigation\", \"Contracts\"],\n"
        "  \"priority_label\": \"High\",\n"
        "  \"priority_score\": 8,\n"
        "  \"summary\": \"One sentence summary of the request\",\n"
        "  \"csuite_mentions\": [{ \"name\": \"Detected Name\", \"matched_variants\": [\"Detected Name\"] }],\n"
        "  \"suggested_owner\": \"Optional name based on context\",\n"
        "  \"suggested_next_steps\": \"Bullet points of immediate actions\",\n"
        "  \"learning_opportunities\": [\"List of 1-2 training topics relevant to this request (e.g. 'Phishing Awareness', 'Contract Basics')\"]\n"
        "}\n\n"
    )
    
    # Inject Context
    if req.csuite_names: 
        base += f"### WATCHLIST (Detect these names)\n{', '.join(req.csuite_names)}\n\n"
    
    if req.reference_notes: 
        base += f"### PLAYBOOK & REFERENCE NOTES\n{req.reference_notes}\n\n"
        
    if req.organization_name:
        base += f"### CLIENT/ORG\n{req.organization_name}\n\n"

    base += f"### INCOMING MESSAGE\n{req.email_text}\n"
    
    return base

def _safe_parse_intake_json(model_output: str) -> Dict[str, Any]:
    """
    Robust JSON parser.
    """
    try: 
        return json.loads(model_output)
    except: 
        pass
    
    try:
        m = re.search(r"\{.*\}", model_output, re.DOTALL)
        if m: 
            return json.loads(m.group(0))
    except: 
        pass
        
    return {
        "categories": ["Uncategorized"], 
        "priority_label": "Medium", 
        "priority_score": 5,
        "summary": "Could not parse analysis.", 
        "csuite_mentions": []
    }

# ---------------------------------------------------------
# TEAM ASSIGNMENT LOGIC
# ---------------------------------------------------------
def _skill_match_score(skill: str, category: str) -> float:
    s, c = skill.lower().strip(), category.lower().strip()
    if not s or not c: return 0.0
    if s == c: return 1.0
    if set(s.split()) & set(c.split()): return 1.0 
    if s in c or c in s: return 0.8
    return 0.0

def assign_team_owner(result: IntakeResponse, team_profile: Optional[Dict[str, Any]]) -> IntakeResponse:
    if not team_profile or not team_profile.get("members"): 
        return result
    
    members = team_profile.get("members", [])
    
    # Playbook Check
    suggestion = (result.suggested_owner or "").split("(")[0].strip().lower()
    member_map = {m["name"].lower(): m["name"] for m in members}
    
    if suggestion and suggestion in member_map:
        result.assigned_owner = member_map[suggestion]
        result.suggested_owner = f"{result.assigned_owner} (Playbook Rule)"
        result.assigned_backup = None
        return result
        
    # Skill Scoring
    scores = []
    cats = [c.lower() for c in result.categories]
    
    for m in members:
        score = 0.0
        for skill in m.get("skills", []):
            label = skill.get("label", "")
            mastery = float(skill.get("mastery", 0))
            best_cat_match = max([_skill_match_score(label, c) for c in cats], default=0.0)
            if best_cat_match > 0:
                score += best_cat_match * (0.5 + mastery/200)
                
        if score > 0:
            scores.append((score, m["name"]))
        
    scores.sort(key=lambda x: x[0], reverse=True)
    
    if scores:
        result.assigned_owner = scores[0][1]
        result.assigned_backup = scores[1][1] if len(scores) > 1 else None
        result.suggested_owner = f"{result.assigned_owner} (Skill Match: {scores[0][0]:.1f})"
    else:
        result.assigned_owner = "Unassigned"
        result.suggested_owner = "Unassigned (No skill match)"
        
    return result

# ---------------------------------------------------------
# NOTIFICATIONS
# ---------------------------------------------------------
def send_intake_email(to_email: str, result: IntakeResponse, original_text: str) -> str:
    if not settings.SMTP_HOST: return "not_configured"
    try:
        msg = EmailMessage()
        msg["Subject"] = f"[Phoenix] {result.priority_label} - {', '.join(result.categories)}"
        msg["From"] = settings.INTAKE_EMAIL_FROM
        msg["To"] = to_email
        msg.set_content(
            f"Priority: {result.priority_label} ({result.priority_score}/10)\n"
            f"Summary: {result.summary}\n\nOriginal:\n{original_text}"
        )
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as s:
            if settings.SMTP_PORT == 587: s.starttls()
            if settings.SMTP_USERNAME: s.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            s.send_message(msg)
        return "sent"
    except Exception as e:
        return f"error: {e}"