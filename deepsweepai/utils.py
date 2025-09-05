from __future__ import annotations
import hashlib, os

def sha256_hex(data: str) -> str:
    if not isinstance(data, (bytes, bytearray)):
        data = (data or "").encode("utf-8", "ignore")
    return hashlib.sha256(data).hexdigest()

def getenv_bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "on"}