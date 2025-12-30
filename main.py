from __future__ import annotations

import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

# Import Routers
from app.routers import legal, intake, contracts, mapper, ui
from app.routers import admin_local  # NEW

# IP guard middleware
from app.middleware.ip_guard_middleware import IPGuardMiddleware

app = FastAPI(title=settings.APP_TITLE)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(IPGuardMiddleware)

# --- Routes ---
app.include_router(ui.router)
app.include_router(legal.router, prefix="/api/legal", tags=["Legal Research"])
app.include_router(intake.router, prefix="/api/intake", tags=["Intake"])
app.include_router(contracts.router, prefix="/api/contracts", tags=["Contracts"])
app.include_router(mapper.router, prefix="/api/mapper", tags=["Mapper"])

# Local-only admin router (Material Design UI)
app.include_router(admin_local.router, prefix="/admin", tags=["Admin"])


@app.get("/api/health")
async def health():
    return {"status": "ok", "app": settings.APP_TITLE}


# quiet browser noise
@app.get("/favicon.ico")
async def favicon():
    return HTMLResponse("", status_code=204)


# --- Startup printout ---
@app.on_event("startup")
async def _startup_banner():
    host = os.getenv("BIND_HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))

    print("\n" + "=" * 72)
    print(f"{settings.APP_TITLE} starting:")
    print(f"Local UI:    http://{host}:{port}/")
    if os.getenv("ADMIN_TOKEN"):
        print(f"IP Admin:    http://{host}:{port}/admin/ips?token=<ADMIN_TOKEN>")
    else:
        print("IP Admin:    set ADMIN_TOKEN to enable /admin/ips")
    print("=" * 72 + "\n")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("BIND_HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
    )
