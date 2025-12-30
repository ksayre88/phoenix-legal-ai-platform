import os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from app.core.ip_guard import is_blocked, record_hit, load_blocklist

# Comma-separated list of proxy IPs you trust to set X-Forwarded-For
TRUSTED_PROXIES = {
    x.strip()
    for x in os.getenv("TRUSTED_PROXIES", "").split(",")
    if x.strip()
}

load_blocklist()


def get_client_ip(request: Request) -> str:
    peer = request.client.host if request.client else "unknown"

    xff = request.headers.get("x-forwarded-for")
    if xff and (not TRUSTED_PROXIES or peer in TRUSTED_PROXIES):
        # First IP in XFF is the original client
        return xff.split(",")[0].strip()

    return peer


class IPGuardMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ip = get_client_ip(request)

        if ip != "unknown" and is_blocked(ip):
            record_hit(ip, request.url.path, request.method, 403)
            return JSONResponse({"detail": "IP blocked"}, status_code=403)

        response: Response = await call_next(request)

        if ip != "unknown":
            record_hit(ip, request.url.path, request.method, response.status_code)

        return response
