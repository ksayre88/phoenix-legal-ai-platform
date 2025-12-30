from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.templates import HTML_MAIN, HTML_INTAKE, HTML_CONTRACTS, HTML_MAPPER

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
@router.get("/ui", response_class=HTMLResponse)
async def ui_main(): return HTML_MAIN

@router.get("/ui/intake", response_class=HTMLResponse)
async def ui_intake(): return HTML_INTAKE

@router.get("/ui/contracts", response_class=HTMLResponse)
async def ui_contracts(): return HTML_CONTRACTS

@router.get("/ui/mapper", response_class=HTMLResponse)
async def ui_mapper(): return HTML_MAPPER