from __future__ import annotations
from typing import Callable
from functools import wraps
from .licensing import get_jwt, is_token_valid, get_entitlements

class ProRequiredError(RuntimeError): pass

def has_pro() -> bool:
    return is_token_valid(get_jwt())

def has_entitlement(ent: str) -> bool:
    return ent in get_entitlements(get_jwt())

def gate(feature: str) -> Callable:
    def _wrap(fn: Callable) -> Callable:
        @wraps(fn)
        def _inner(*args, **kwargs):
            if not has_pro() or not has_entitlement(feature):
                raise ProRequiredError(
                    f"DeepSweep AI Pro required: missing entitlement '{feature}'. "
                    f"Set DEEPSWEEP_PRO_TOKEN or save token to ~/.deepsweepai/token "
                    f"(get one at https://deepsweep.ai/pro)."
                )
            return fn(*args, **kwargs)
        return _inner
    return _wrap