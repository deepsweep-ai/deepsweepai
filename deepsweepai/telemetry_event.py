from __future__ import annotations
from typing import Dict, List, Optional
import uuid, datetime as dt
from .utils import sha256_hex
from .compliance import owasp_for, nist_for

def _iso_utc() -> str:
    return dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc).isoformat().replace("+00:00", "Z")

def build_validation_event(*,
    client_version: str,
    agent_framework: str,
    llm_provider: str,
    base_model_family: str,
    attack_category: str,
    attack_subcategory: str,
    attack_source: str,
    prompt_text: str,
    response_text: str,
    response_latency_ms: int,
    output_token_count: int,
    output_structure: str,
    test_result: str,
    failure_reason: str,
    confidence: float,
    owasp_list: Optional[List[str]] = None,
    nist_list: Optional[List[str]] = None,
) -> Dict:
    prompt_hash = sha256_hex(prompt_text or "")
    response_hash = sha256_hex(response_text or "")
    owasp_tags = owasp_list if owasp_list is not None else owasp_for(attack_category)
    nist_tags = nist_list if nist_list is not None else nist_for(attack_category)

    return {
        "eventId": str(uuid.uuid4()),
        "eventTimestamp": _iso_utc(),
        "clientVersion": client_version,
        "environmentContext": {
            "agentFramework": agent_framework,
            "llmProvider": llm_provider,
            "baseModelFamily": base_model_family,
        },
        "attackVector": {
            "attackCategory": attack_category,
            "attackSubCategory": attack_subcategory,
            "attackSource": attack_source,
            "promptHash": prompt_hash,
        },
        "agentResponse": {
            "responseHash": response_hash,
            "responseLatencyMs": int(response_latency_ms),
            "outputTokenCount": int(output_token_count),
            "outputStructure": output_structure,
        },
        "validationOutcome": {
            "testResult": test_result,
            "failureReason": failure_reason,
            "confidenceScore": float(confidence),
        },
        "complianceMapping": {
            "nistAiRmf": nist_tags,
            "owaspTop10Llm": owasp_tags,
        },
    }