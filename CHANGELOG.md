## [0.3.4] - 2025-09-05
### Added
- `deepsweep mock` zero-setup command (no API keys).
- URL shorthand: `deepsweep https://... --key ...`.
- `--key` support on `scan` (sets OPENAI_API_KEY for providers).
- `examples/test_openai.py` now *actually* uses OPENAI_API_KEY.

### Fixed
- CLI flags alignment with README (`--output`).
- Scanner stability + report formatting.
- CI/CD workflows

### Docs
- Tiered README Quickstart (mock, OpenAI, URL).
- `/pro` flow documented with Stripe links.
- Minor reference updates/corrections