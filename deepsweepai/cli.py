from __future__ import annotations
import argparse, sys
from .scanner import run_scan, RUNNERS
from .report import write_report
from .pro import ProRequiredError
from . import __version__

def main():
    providers = sorted(RUNNERS.keys())
    p = argparse.ArgumentParser(
        prog="deepsweepai",
        description="DeepSweep AI - The first independent AI agent security testing & compliance platform",
    )
    p.add_argument("--version", action="version", version=f"deepsweepai {__version__}")
    p.add_argument("--provider", default="mock", choices=providers,
                   help=f"Choose LLM provider ({', '.join(providers)}). Plugins extend this list.")
    p.add_argument("--model-family", default="GPT-4o",
                   help="Model family (e.g., GPT-4o|Claude-3.5|Llama-3|Gemini-2.5|...).")
    p.add_argument("--framework", default="custom",
                   help="LangChain|CrewAI|AutoGen|Custom (for context tagging).")
    p.add_argument("--owasp-top10", action="store_true",
                   help="Run OWASP Top 10 baseline adversarial cases.")
    p.add_argument("--advanced-attacks", action="store_true",
                   help="(Pro) Include server-side advanced attacks if entitled. Falls back silently if unavailable.")
    p.add_argument("--min-pass", type=int, default=None,
                   help="Require at least N passes (non-zero exit if unmet).")
    p.add_argument("-q", "--quick", action="store_true",
                   help="Quick mode (smaller subset).")
    p.add_argument("--export", metavar="PATH", default=None,
                   help="(Pro) Write a compliance report (md/json) to PATH.")
    p.add_argument("--export-format", choices=["md", "json"], default="md",
                   help="(Pro) Report format (md/json).")
    args = p.parse_args()

    print(f"DeepSweep AI v{__version__} — provider={args.provider}, model={args.model_family}")

    try:
        res = run_scan(
            provider=args.provider,
            model_family=args.model_family,
            framework=args.framework,
            run_owasp=args.owasp_top10,
            quick=args.quick,
            min_pass=args.min_pass,
            advanced_attacks=args.advanced_attacks,
        )
    except ProRequiredError as e:
        print(str(e))
        sys.exit(3)

    if args.min_pass is not None and res["summary"].get("ci_violation"):
        print(f"✘ CI gate: need >= {args.min_pass} passes, got {res['summary'].get('tests_passed', 0)}")
        sys.exit(2)

    s = res["summary"]
    print(f"✔ Ran {s['tests_total']} | Failed: {s['tests_failed']} | Critical: {s['critical']}")

    if args.export:
        path = write_report(s, res["results"], fmt=args.export_format, path=args.export)
        print(f"⬇ Report written: {path}")

if __name__ == "__main__":
    main()