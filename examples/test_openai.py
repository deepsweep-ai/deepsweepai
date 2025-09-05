from __future__ import annotations
import sys
from deepsweepai.cli import main as cli_main

if __name__ == "__main__":
    sys.argv = ["deepsweepai", "--provider", "openai", "--owasp-top10"]
    cli_main()