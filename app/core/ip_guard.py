import os
import json
from ipaddress import ip_address
from datetime import datetime, timezone
from threading import Lock
from typing import Dict, Any, List, Tuple

BLOCKLIST_PATH = os.getenv("IP_BLOCKLIST_PATH", "./ip_blocklist.json")

_lock = Lock()
_blocked = set()  # set[str]
_stats: Dict[str, Dict[str, Any]] = {}  # ip -> {count,last_seen,last_path,last_method,last_status}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_ip(value: str) -> str:
    # Validates and normalizes IPv4/IPv6
    return str(ip_address(value.strip()))


def load_blocklist() -> None:
    global _blocked
    try:
        with open(BLOCKLIST_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        ips = data.get("blocked_ips", [])
        with _lock:
            _blocked = {normalize_ip(x) for x in ips}
    except FileNotFoundError:
        with _lock:
            _blocked = set()
    except Exception:
        # If the file is corrupt, fail safe (empty) rather than crash the app
        with _lock:
            _blocked = set()


def save_blocklist() -> None:
    with _lock:
        data = {"blocked_ips": sorted(_blocked)}
    tmp = BLOCKLIST_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, BLOCKLIST_PATH)


def is_blocked(ip: str) -> bool:
    with _lock:
        return ip in _blocked


def block_ip(ip: str) -> None:
    ip = normalize_ip(ip)
    with _lock:
        _blocked.add(ip)
    save_blocklist()


def unblock_ip(ip: str) -> None:
    ip = normalize_ip(ip)
    with _lock:
        _blocked.discard(ip)
    save_blocklist()


def blocked_list() -> List[str]:
    with _lock:
        return sorted(_blocked)


def record_hit(ip: str, path: str, method: str, status: int) -> None:
    path = (path or "")[:300]
    method = (method or "")[:16]

    with _lock:
        d = _stats.setdefault(
            ip,
            {
                "count": 0,
                "last_seen": None,
                "last_path": None,
                "last_method": None,
                "last_status": None,
            },
        )
        d["count"] += 1
        d["last_seen"] = _now_iso()
        d["last_path"] = path
        d["last_method"] = method
        d["last_status"] = status


def top_ips(limit: int = 50) -> List[Tuple[str, Dict[str, Any]]]:
    with _lock:
        items = list(_stats.items())
    items.sort(key=lambda kv: kv[1].get("count", 0), reverse=True)
    return items[:limit]
