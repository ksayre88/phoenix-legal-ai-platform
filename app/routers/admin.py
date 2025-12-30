import os
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from app.core.ip_guard import top_ips, blocked_list, block_ip, unblock_ip

router = APIRouter()

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "")


def require_admin(request: Request) -> None:
    # Prefer header auth; allow ?token= for quick testing (remove if you want stricter)
    token = request.headers.get("x-admin-token") or request.query_params.get("token")
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/ips", response_class=HTMLResponse)
async def admin_ips(request: Request):
    require_admin(request)

    blocked = blocked_list()
    top = top_ips(limit=100)

    rows = []
    for ip, data in top:
        rows.append(f"""
          <tr>
            <td style="font-family:monospace">{ip}</td>
            <td>{data.get("count", 0)}</td>
            <td style="font-family:monospace">{data.get("last_seen","")}</td>
            <td style="font-family:monospace">{data.get("last_method","")} {data.get("last_path","")}</td>
            <td>{data.get("last_status","")}</td>
            <td>
              <form method="post" action="/admin/block" style="display:inline">
                <input type="hidden" name="ip" value="{ip}">
                <button type="submit">Block</button>
              </form>
              <form method="post" action="/admin/unblock" style="display:inline;margin-left:6px">
                <input type="hidden" name="ip" value="{ip}">
                <button type="submit">Unblock</button>
              </form>
            </td>
          </tr>
        """)

    blocked_html = "".join([f"<li style='font-family:monospace'>{ip}</li>" for ip in blocked]) or "<li>(none)</li>"

    html = f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8"/>
        <title>Admin IP Guard</title>
        <style>
          body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial; margin: 24px; }}
          table {{ border-collapse: collapse; width: 100%; }}
          th, td {{ border: 1px solid #ddd; padding: 8px; vertical-align: top; }}
          th {{ background: #f5f5f5; text-align: left; }}
          .grid {{ display: grid; grid-template-columns: 1fr 2fr; gap: 24px; }}
          code {{ background: #f2f2f2; padding: 2px 6px; border-radius: 6px; }}
        </style>
      </head>
      <body>
        <h1>Admin: IP Guard</h1>
        <p>Auth: send header <code>X-Admin-Token: ...</code> (or <code>?token=...</code>).</p>

        <div class="grid">
          <section>
            <h2>Blocked IPs</h2>
            <ul>{blocked_html}</ul>

            <h3>Manual block</h3>
            <form method="post" action="/admin/block">
              <input name="ip" placeholder="1.2.3.4" style="width:220px"/>
              <button type="submit">Block</button>
            </form>
          </section>

          <section>
            <h2>Top IPs hitting the app</h2>
            <table>
              <thead>
                <tr>
                  <th>IP</th><th>Count</th><th>Last seen (UTC)</th><th>Last request</th><th>Status</th><th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {''.join(rows)}
              </tbody>
            </table>
          </section>
        </div>
      </body>
    </html>
    """
    return HTMLResponse(content=html)


@router.post("/block")
async def admin_block(request: Request, ip: str = Form(...)):
    require_admin(request)
    block_ip(ip)
    return RedirectResponse(url="/admin/ips", status_code=303)


@router.post("/unblock")
async def admin_unblock(request: Request, ip: str = Form(...)):
    require_admin(request)
    unblock_ip(ip)
    return RedirectResponse(url="/admin/ips", status_code=303)
