from __future__ import annotations
from typing import Dict, List, Literal
import json, pathlib, datetime as dt
from .pro import gate

@gate("compliance_reports")
def write_report(summary: Dict, results: List[Dict], *, fmt: Literal["json","md"]="md", path: str|None=None) -> str:
    out = pathlib.Path(path or f"deepsweep_report_{dt.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{fmt}")
    out.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "json":
        out.write_text(json.dumps({"summary": summary, "results": results}, indent=2), encoding="utf-8")
        return str(out)
    lines = []
    lines.append("# DeepSweep AI Compliance Report\n")
    lines.append(f"**Provider**: `{summary.get('provider')}`  ")
    lines.append(f"**Model**: `{summary.get('model')}`  ")
    lines.append(f"**Total**: {summary.get('tests_total')} — **Passed**: {summary.get('tests_passed')} — **Failed**: {summary.get('tests_failed')} — **Critical**: {summary.get('critical')}\n")
    lines.append("## Findings (OWASP/NIST mapping)")
    lines.append("| ID | Category | Sub | Result | Reason | OWASP | NIST | Latency(ms) | Tokens |")
    lines.append("|---|---|---|---|---|---|---|---:|---:|")
    for r in results:
        lines.append(f"| {r['id']} | {r['category']} | {r['sub']} | {r['result']} | {r['reason'] or ''} | "
                     f"{','.join(r['owasp'] or [])} | {','.join(r['nist'] or [])} | {r['response_latency_ms']} | {r['tokens']} |")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(out)