from __future__ import annotations
from typing import Dict, List

_OWASP_MAP: Dict[str, List[str]] = {
    "PromptInjection": ["LLM01"],
    "DataLeakage": ["LLM02"],
    "ModelMisuse": ["LLM03"],
    "SupplyChain": ["LLM04"],
}

_NIST_MAP: Dict[str, List[str]] = {
    "PromptInjection": ["Test/Eval-2", "Protect-1"],
    "DataLeakage": ["Govern-3", "Protect-1"],
    "ModelMisuse": ["Map-5", "Test/Eval-2"],
    "SupplyChain": ["Test/Eval-2"],
}

def owasp_for(category: str) -> List[str]:
    return _OWASP_MAP.get(category, [])

def nist_for(category: str) -> List[str]:
    return _NIST_MAP.get(category, [])