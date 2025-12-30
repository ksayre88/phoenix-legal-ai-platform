from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class QueryRequest(BaseModel):
    question: str
    personas: List[str]
    use_rag: bool = True

class PersonaAnswer(BaseModel):
    persona: str
    label: str
    answer: str

class CsuiteHit(BaseModel):
    name: str
    matched_variants: List[str] = []
    contexts: List[str] = []

class IntakeRequest(BaseModel):
    email_text: str
    reference_notes: Optional[str] = ""
    csuite_names: List[str] = []
    organization_name: Optional[str] = ""
    max_categories: int = 5
    notify_email: Optional[str] = None
    team_profile: Optional[Dict[str, Any]] = None

class IntakeResponse(BaseModel):
    categories: List[str]
    priority_label: str
    priority_score: Optional[float] = None
    summary: str
    csuite_mentions: List[CsuiteHit]
    suggested_owner: Optional[str] = None
    suggested_backup: Optional[str] = None
    suggested_next_steps: Optional[str] = None
    learning_opportunities: Optional[List[str]] = []
    assigned_owner: Optional[str] = None
    assigned_backup: Optional[str] = None
    original_text: Optional[str] = None
    raw_model_output: str
    email_status: Optional[str] = None

class ContractRedlineRequest(BaseModel):
    counterparty_text: str
    template_text: Optional[str] = None
    mode: str = "template_only"
    persona: str = "General Counsel"
    role: str = "Buyer"

class ContractRedlineExportRequest(BaseModel):
    original_docx_base64: str
    diff: Any 

class ContractReportRequest(BaseModel):
    diff: Any

class PersonaUpdateRequest(BaseModel):
    name: str
    instructions: str

class MapperReportRequest(BaseModel):
    image_base64: str
    flows: List[Dict[str, Any]]
    controller: str