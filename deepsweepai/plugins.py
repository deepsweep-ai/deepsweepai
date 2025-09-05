from __future__ import annotations
from typing import Callable, Dict, Optional
import importlib.metadata as im

ENTRY_GROUP = "deepsweepai.providers"

def discover_providers() -> Dict[str, Callable[[str, Optional[str]], str]]:
    runners: Dict[str, Callable] = {}
    try:
        eps = im.entry_points()
        select = getattr(eps, "select", None)
        selected = eps.select(group=ENTRY_GROUP) if callable(select) else eps.get(ENTRY_GROUP, [])
        for ep in selected:
            try:
                fn = ep.load()
                if callable(fn):
                    runners[ep.name.lower()] = fn
            except Exception:
                continue
    except Exception:
        pass
    return runners