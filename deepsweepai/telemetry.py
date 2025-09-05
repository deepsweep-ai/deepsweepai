from __future__ import annotations
import os, json, urllib.request
from typing import Dict, Optional
from .utils import getenv_bool

_TELEMETRY_URL = os.getenv("DEEPSWEEP_TELEMETRY_URL", "https://api.deepsweep.ai/telemetry")

def send_validation_event(event: Dict, *, jwt: Optional[str] = None) -> None:
    if not getenv_bool("DEEPSWEEP_TELEMETRY", True):
        return
    try:
        payload = json.dumps({
            "consent": True,
            "event": event,
        }).encode()
        headers = {"Content-Type": "application/json", "User-Agent": "deepsweepai-telemetry/1"}
        if jwt:
            headers["Authorization"] = f"Bearer {jwt}"
        req = urllib.request.Request(_TELEMETRY_URL, method="POST", data=payload, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as r:
            _ = r.read()
    except Exception:
        # graceful: never block or crash scans
        pass