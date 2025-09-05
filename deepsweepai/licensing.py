from __future__ import annotations
import os, json, time, urllib.request
from typing import Tuple, List, Optional

_VERIFY_URL = os.getenv("DEEPSWEEP_VERIFY_URL", "https://api.deepsweep.ai/verify")
_cache = {"token": None, "valid": False, "exp": 0, "entitlements": []}

def get_jwt() -> Optional[str]:
    tok = os.getenv("DEEPSWEEP_PRO_TOKEN", "").strip()
    if tok:
        return tok
    path = os.path.expanduser("~/.deepsweepai/token")
    try:
        if os.path.exists(path):
            return open(path, "r", encoding="utf-8").read().strip()
    except Exception:
        pass
    return None

def _remote_verify(token: str) -> Tuple[bool, int, List[str]]:
    """
    Server supports GET with Bearer token; returns:
      { "active": bool, "exp": int, "entitlements": [..] }
    """
    req = urllib.request.Request(
        _VERIFY_URL + "?exp=1&entitlements=1",
        method="GET",
        headers={"Authorization": f"Bearer {token}", "User-Agent": "deepsweepai/verify"}
    )
    with urllib.request.urlopen(req, timeout=6) as r:
        data = json.loads(r.read().decode() or "{}")
        active = bool(data.get("active") or data.get("valid") or False)
        exp = int(data.get("exp", int(time.time()) + 300))
        ents = list(data.get("entitlements", []))
        return active, exp, ents

def is_token_valid(token: Optional[str]) -> bool:
    now = int(time.time())
    if _cache["token"] == token and _cache["exp"] > now:
        return _cache["valid"]
    if not token:
        _cache.update({"token": None, "valid": False, "exp": now + 300, "entitlements": []})
        return False
    try:
        active, exp, ents = _remote_verify(token)
        _cache.update({"token": token, "valid": active, "exp": exp, "entitlements": ents})
        return active
    except Exception:
        # network/5xx → fail closed but cache briefly so we don't hammer the API
        _cache.update({"token": token, "valid": False, "exp": now + 120, "entitlements": []})
        return False

def get_entitlements(token: Optional[str]) -> List[str]:
    if not is_token_valid(token):
        return []
    return list(_cache.get("entitlements", []))