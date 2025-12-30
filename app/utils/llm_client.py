import httpx
import json
from app.core.config import settings

async def call_ollama_generate(model: str, prompt: str, json_mode: bool = False, num_predict: int = 1024) -> str:
    url = f"{settings.OLLAMA_URL}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "num_predict": num_predict, 
        "num_ctx": 8192,
    }
    if json_mode:
        payload["format"] = "json"

    async with httpx.AsyncClient(timeout=600.0) as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        return resp.json().get("response", "").strip()