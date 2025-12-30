from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from app.models.schemas import MapperReportRequest
from app.utils.file_parsing import preprocess_document_from_upload
from app.core.config import settings
from app.utils.llm_client import call_ollama_generate
from app.core.knowledge_base import STANDARD_DATA_TYPES
from app.services.mapper import (
    extract_definitions, 
    chunk_text, 
    classify_chunks_parallel, 
    detect_company, 
    extract_flows, 
    build_swimlane_diagram,
    generate_mapper_report_docx # New import
)
import io

router = APIRouter()

def extract_entities(text: str, controller: str):
    return {
        "user": "User", "controller": controller, 
        "vendors": "Vendors", "partners": "Partners", 
        "government": "Government"
    }

def prompt_builder(chunk: str, definitions: str) -> str:
    """
    Robust Prompt: Combines Definitions + Standard Registry + Strict Extraction.
    """
    return (
        "You are an expert Data Privacy Auditor. Map data flows in the text below.\n\n"
        
        "### 1. INTERNAL DEFINITIONS (Context)\n"
        f"{definitions}\n\n"
        
        "### 2. STANDARD DATA CATEGORIES (Use these names for granularity)\n"
        f"{STANDARD_DATA_TYPES}\n\n"
        
        "### TASK\n"
        "1. **EXTRACT**: List every specific data type collected or shared.\n"
        "   - Use the **Standard Categories** names if applicable (e.g. use 'Internet Activity' for logs/cookies).\n"
        "   - Unpack broad terms like 'Personal Information' into specific elements (Name, Email, etc.) found in the text.\n"
        "2. **SHARING**: Identify Third Party Recipients.\n"
        "   - Look for: 'Ad Networks', 'Analytics Providers', 'Affiliates', 'Government'.\n\n"
        
        "### OUTPUT FORMAT (Strict JSON)\n"
        "{\n"
        "  \"findings\": [\n"
        "    { \"data_type\": \"Credit Card Number\", \"action\": \"Collection\", \"recipient\": null },\n"
        "    { \"data_type\": \"Cookies\", \"action\": \"Sharing\", \"recipient\": \"Google Analytics\" }\n"
        "  ]\n"
        "}\n\n"
        f"TEXT:\n{chunk}"
    )

def verification_prompt_builder(chunk: str, previous_json: str) -> str:
    return (
        "Audit the findings against the text. Remove hallucinations.\n"
        "1. If a data type is listed but NOT mentioned (or implied by definition) in the text, REMOVE it.\n"
        "2. Ensure entities (e.g. 'Affiliates') are not listed as Data Types.\n"
        f"TEXT:\n{chunk}\n\n"
        f"FINDINGS:\n{previous_json}\n\n"
        "Return corrected JSON."
    )

# --- ROUTES ---

@router.post("")
async def mapper_route(
    file: UploadFile = File(None), 
    payload_text: str = Form(None)
):
    cleaned_text = ""
    if file:
        content = await file.read()
        processed = preprocess_document_from_upload(file.filename, content)
        cleaned_text = processed["clean_text"]
    elif payload_text:
        lines = [l.strip() for l in payload_text.split("\n") if len(l.strip()) > 25]
        cleaned_text = "\n".join(lines)
    else:
        return {"error": "No input provided."}

    if not cleaned_text.strip(): return {"error": "Empty text."}

    # 1. Definitions
    definitions = await extract_definitions(cleaned_text)
    
    # 2. Chunking
    chunks = chunk_text(cleaned_text) 
    
    # 3. Analysis
    classified = await classify_chunks_parallel(
        chunks, 
        definitions,
        prompt_builder=prompt_builder,
        verification_builder=verification_prompt_builder
    )
    
    # 4. Graph Construction
    controller = detect_company(cleaned_text)
    entities = extract_entities(cleaned_text, controller)
    flows = extract_flows(classified, controller)
    diagram = build_swimlane_diagram(entities, flows)

    return {
        "controller_detected": controller,
        "clean_text": cleaned_text[:200] + "...", 
        "definitions_found": definitions[:200] + "...",
        "flows": flows,
        "diagram": diagram,
        "raw_analysis_count": len(classified)
    }

@router.post("/export-report")
async def export_mapper_report(req: MapperReportRequest):
    """
    Generates a Word Document report of the data map.
    """
    try:
        # Use the service function (ensure it's imported above)
        docx_bytes = generate_mapper_report_docx(req.controller, req.flows, req.image_base64)
        
        return StreamingResponse(
            io.BytesIO(docx_bytes), 
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment; filename=Privacy_Map_Report.docx"}
        )
    except Exception as e:
        print(f"Export Error: {e}")
        # Return error as detail so frontend can alert
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")