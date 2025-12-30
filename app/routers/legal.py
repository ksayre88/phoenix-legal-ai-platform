from fastapi import APIRouter
from app.models.schemas import QueryRequest
from app.services.legal_rag import get_rag_context_for_persona, PERSONAS, build_prompt
from app.utils.llm_client import call_ollama_generate

router = APIRouter()

@router.post("/query")
async def legal_query(req: QueryRequest):
    requested = req.personas or ["mi"]
    answers = []
    used_rag = False
    all_sources = []
    
    if req.use_rag:
        for pid in requested:
            ctx, srcs = get_rag_context_for_persona(req.question, pid)
            all_sources.extend(srcs)
            ans = await call_ollama_generate(PERSONAS[pid]["model"], build_prompt(pid, req.question, ctx))
            answers.append({"persona": pid, "label": PERSONAS[pid]["label"], "answer": ans})
        if all_sources: used_rag = True
            
    return {"answers": answers, "used_rag": used_rag, "sources": all_sources}