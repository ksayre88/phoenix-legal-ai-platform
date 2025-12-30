from __future__ import annotations

import os
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from app.core.ip_guard import top_ips, blocked_list, block_ip, unblock_ip

router = APIRouter()

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "")


def _is_local_direct(request: Request) -> bool:
    host = request.client.host if request.client else ""
    if host not in {"127.0.0.1", "::1", "localhost"}:
        return False

    # If nginx is proxying, it should set X-Forwarded-For.
    # This keeps /admin reachable only when you browse directly on the server.
    if request.headers.get("x-forwarded-for"):
        return False

    return True


def _require_local_admin(request: Request) -> None:
    if not _is_local_direct(request):
        raise HTTPException(status_code=404, detail="Not found")

    token = request.headers.get("x-admin-token") or request.query_params.get("token")
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/ips", response_class=HTMLResponse)
async def admin_ips(request: Request):
    _require_local_admin(request)

    token = request.query_params.get("token", "")
    qs = f"?token={token}" if token else ""

    blocked = blocked_list()
    top = top_ips(limit=200)

    blocked_chips = "".join(
        f"""
        <div class="chip">
          <span class="mono">{ip}</span>
          <form method="post" action="/admin/unblock{qs}" style="display:inline;margin-left:8px;">
            <input type="hidden" name="ip" value="{ip}">
            <button class="btn-flat waves-effect waves-teal" type="submit" title="Unblock" style="padding:0 6px;">
              <i class="material-icons" style="font-size:18px; line-height: 32px;">close</i>
            </button>
          </form>
        </div>
        """
        for ip in blocked
    ) or "<div class='grey-text'>No blocked IPs yet.</div>"

    rows = []
    for ip, data in top:
        last_seen = data.get("last_seen", "") or ""
        last_req = f"{data.get('last_method','')} {data.get('last_path','')}".strip()
        count = data.get("count", 0)
        status = data.get("last_status", "")

        rows.append(f"""
          <tr>
            <td class="mono">{ip}</td>
            <td>{count}</td>
            <td class="mono">{last_seen}</td>
            <td class="mono">{last_req}</td>
            <td>{status}</td>
            <td style="white-space:nowrap;">
              <form method="post" action="/admin/block{qs}" style="display:inline">
                <input type="hidden" name="ip" value="{ip}">
                <button class="btn waves-effect waves-light" type="submit" title="Block">
                  <i class="material-icons left">block</i>Block
                </button>
              </form>
              <form method="post" action="/admin/unblock{qs}" style="display:inline;margin-left:8px;">
                <input type="hidden" name="ip" value="{ip}">
                <button class="btn grey lighten-1 waves-effect waves-light" type="submit" title="Unblock">
                  <i class="material-icons left">undo</i>Unblock
                </button>
              </form>
            </td>
          </tr>
        """)

    table_body = "".join(rows) or """
      <tr>
        <td colspan="6" class="grey-text">No traffic recorded yet.</td>
      </tr>
    """

    html = f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <title>IP Guard Admin</title>

        <!-- Material Icons -->
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <!-- Materialize CSS (Material Design) -->
        <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" rel="stylesheet">

        <style>
          html, body {{
            height: 100%;
          }}
          body {{
            background: #fafafa;
            margin: 0;
          }}

          /* Fullscreen container */
          .app-shell {{
            min-height: 100vh;
            display: flex;
            flex-direction: column;
          }}

          /* Full-width content area */
          .content {{
            flex: 1;
            width: 100%;
            padding: 18px 18px 48px;
            box-sizing: border-box;
          }}

          /* Materialize container is max-width; we are intentionally not using it */
          .mono {{
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            font-size: 0.95rem;
          }}

          .topbar {{
            border-radius: 0; /* true full width */
          }}
          nav .nav-wrapper {{
            padding: 0 18px;
          }}
          nav .brand-logo {{
            position: relative;  /* prevent Materialize from centering & clipping */
            left: 0;
            transform: none;
            font-size: 1.15rem;
          }}

          .card {{
            border-radius: 14px;
            overflow: visible; /* avoid clipping shadows/content */
          }}

          .badge-pill {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 10px;
            border-radius: 999px;
            background: #e3f2fd;
            color: #0d47a1;
            font-weight: 600;
          }}

          .helptext {{
            margin-top: 6px;
            font-size: 0.95rem;
          }}

          .chip {{
            margin: 6px 6px 0 0;
          }}

          table.striped > tbody > tr:nth-child(odd) {{
            background-color: rgba(0,0,0,0.03);
          }}

          /* Make the table area never clip; allow horizontal scroll */
          .table-scroll {{
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
          }}

          /* On smaller screens, reduce padding a bit */
          @media (max-width: 600px) {{
            .content {{
              padding: 12px 12px 32px;
            }}
            nav .nav-wrapper {{
              padding: 0 12px;
            }}
          }}
        </style>
      </head>

      <body>
        <div class="app-shell">
          <nav class="blue darken-2 topbar">
            <div class="nav-wrapper">
              <a href="/admin/ips{qs}" class="brand-logo">
                <i class="material-icons left">security</i>IP Guard Admin
              </a>
              <ul class="right">
                <li><a href="/admin/ips{qs}"><i class="material-icons left">refresh</i>Refresh</a></li>
              </ul>
            </div>
          </nav>

          <main class="content">
            <div class="row" style="margin-bottom: 10px;">
              <div class="col s12">
                <div class="badge-pill">
                  <i class="material-icons">info</i>
                  Direct local-only admin (won't work through nginx proxy)
                </div>
                <div class="helptext grey-text">
                  Auth is via <span class="mono">?token=...</span> or header <span class="mono">X-Admin-Token</span>.
                </div>
              </div>
            </div>

            <div class="row">
              <!-- Left column -->
              <div class="col s12 m12 l4">
                <div class="card">
                  <div class="card-content">
                    <span class="card-title">
                      <i class="material-icons left">block</i>Blocked IPs
                    </span>
                    <div style="margin-top: 10px;">
                      {blocked_chips}
                    </div>
                  </div>
                </div>

                <div class="card">
                  <div class="card-content">
                    <span class="card-title">
                      <i class="material-icons left">add</i>Manual block
                    </span>
                    <form method="post" action="/admin/block{qs}">
                      <div class="input-field">
                        <input id="ip" name="ip" type="text" placeholder="93.123.72.132" required>
                        <label for="ip">IP address (IPv4/IPv6)</label>
                      </div>
                      <button class="btn waves-effect waves-light" type="submit">
                        <i class="material-icons left">block</i>Block IP
                      </button>
                    </form>
                    <div class="grey-text" style="margin-top: 10px;">
                      Tip: block repeat scanners (LuCI probes, /.git/config probes, etc.)
                    </div>
                  </div>
                </div>
              </div>

              <!-- Right column -->
              <div class="col s12 m12 l8">
                <div class="card">
                  <div class="card-content">
                    <span class="card-title">
                      <i class="material-icons left">analytics</i>Top IPs hitting the app
                    </span>

                    <div class="input-field" style="margin-top: 12px;">
                      <i class="material-icons prefix">search</i>
                      <input id="filter" type="text" placeholder="Filter by IP or path…">
                      <label for="filter">Filter</label>
                    </div>

                    <div class="table-scroll">
                      <table class="striped highlight responsive-table" id="ipsTable">
                        <thead>
                          <tr>
                            <th>IP</th>
                            <th>Count</th>
                            <th>Last seen (UTC)</th>
                            <th>Last request</th>
                            <th>Status</th>
                            <th>Actions</th>
                          </tr>
                        </thead>
                        <tbody>
                          {table_body}
                        </tbody>
                      </table>
                    </div>

                    <div class="grey-text" style="margin-top: 10px;">
                      Counts are lifetime since app start.
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </main>
        </div>

        <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
        <script>
          document.addEventListener('DOMContentLoaded', function() {{
            M.updateTextFields();

            const filter = document.getElementById('filter');
            const table = document.getElementById('ipsTable');
            if (!filter || !table) return;

            filter.addEventListener('input', function() {{
              const q = filter.value.toLowerCase();
              const rows = table.querySelectorAll('tbody tr');
              rows.forEach(r => {{
                const text = r.innerText.toLowerCase();
                r.style.display = text.includes(q) ? '' : 'none';
              }});
            }});
          }});
        </script>
      </body>
    </html>
    """
    return HTMLResponse(content=html)


@router.post("/block")
async def admin_block(request: Request, ip: str = Form(...)):
    _require_local_admin(request)
    block_ip(ip)

    token = request.query_params.get("token", "")
    url = f"/admin/ips?token={token}" if token else "/admin/ips"
    return RedirectResponse(url=url, status_code=303)


@router.post("/unblock")
async def admin_unblock(request: Request, ip: str = Form(...)):
    _require_local_admin(request)
    unblock_ip(ip)

    token = request.query_params.get("token", "")
    url = f"/admin/ips?token={token}" if token else "/admin/ips"
    return RedirectResponse(url=url, status_code=303)
