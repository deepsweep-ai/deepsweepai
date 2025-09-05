# DeepSweep AI

[![PyPI version](https://img.shields.io/pypi/v/deepsweepai.svg)](https://pypi.org/project/deepsweepai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Discord](https://img.shields.io/badge/Discord-Join%20Community-7289DA)](https://discord.gg/Db5Zth2RKR)

**Developer-first AI agent security testing** — Find vulnerabilities before they reach production.

```bash
pip install deepsweepai
deepsweepai --provider openai --owasp-top10
```

## Why DeepSweep AI?

**The Problem:** 82% of AI agents deployed without security testing. Average cost of AI failures: $2.3M per incident.

**The Solution:** Automated red-teaming that finds prompt injections, hallucinations, and compliance gaps in minutes, not months.

## Quick Start

```bash
# Install
pip install deepsweepai

# Test with mock provider (no API keys needed)
deepsweepai --provider mock --owasp-top10

# Test real agent
export OPENAI_API_KEY=sk-...
deepsweepai --provider openai --model gpt-4o --owasp-top10
```

## Example Output

```
DeepSweep AI v0.3.0 — Testing gpt-4o against OWASP LLM Top 10

[1/10] LLM01: Prompt Injection .......................... ❌ CRITICAL
[2/10] LLM02: Insecure Output Handling .................. ✅ PASS  
[3/10] LLM03: Training Data Poisoning ................... ⚠️  MEDIUM
...

Security Score: 60% — 2 Critical, 1 High, 3 Medium issues found

Critical Issues:
• Prompt injection bypassed input validation (LLM01)
• Sensitive data exposed in error messages (LLM06)

📊 Full report: ./deepsweep-report-20250905.json
```

## Core Features

### 🔥 **Adversarial Testing**
- **Prompt injection** detection across 50+ attack vectors
- **Jailbreak resistance** testing with evolving techniques  
- **Hallucination assessment** with fact-checking validation
- **Tool misuse** detection for agent frameworks

### 🎯 **Framework Integration**
- **LangChain, CrewAI, AutoGen** — native connectors
- **Custom agents** — REST API integration
- **Multi-provider** — OpenAI, Anthropic, Google, Meta, self-hosted

### 📋 **Compliance Mapping**
- **OWASP LLM Top 10** — complete coverage
- **NIST AI RMF** — Govern/Map/Measure/Manage alignment
- **EU AI Act** — risk assessment artifacts

## Advanced Usage

### CI/CD Integration
```bash
# Fail build if security score < 80%
deepsweepai --provider openai --min-pass 8 --owasp-top10
echo $? # 0 = pass, 1 = fail
```

### Custom Test Suites
```python
from deepsweepai import DeepSweep

sweep = DeepSweep(provider="openai", model="gpt-4o")
results = sweep.test([
    "prompt_injection",
    "hallucination", 
    "tool_misuse"
])
print(f"Security score: {results.score}%")
```

### Framework-Specific Testing
```bash
# LangChain agent
deepsweepai --framework langchain --endpoint http://localhost:8000/chat

# CrewAI multi-agent
deepsweepai --framework crewai --config crew_config.yaml
```

## Pro Features

```bash
export DEEPSWEEP_PRO_TOKEN=dsw_************************
```

- **Advanced attacks** — 500+ synthetic scenarios with ML-generated variants
- **Compliance reports** — PDF/JSON exports for auditors  
- **Enterprise telemetry** — aggregate insights across your org
- **Priority support** — dedicated Slack channel

👉 [Get Pro access](https://deepsweep.ai/pro)

## Architecture

DeepSweep AI is built on three core components:

1. **Guardrail Engine** — Policy evaluation with OPA/Rego
2. **Adversarial Data Engine** — Synthetic attack generation  
3. **Evaluation Harness** — Multi-provider test execution

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Your Agent    │───▶│  DeepSweep AI   │───▶│  Security       │
│                 │    │                 │    │  Report         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  OWASP/NIST     │
                       │  Compliance     │
                       └─────────────────┘
```

## CLI Reference

### Basic Commands
```bash
deepsweepai --provider <PROVIDER> --owasp-top10
deepsweepai --provider <PROVIDER> --custom-tests path/to/tests.yaml
deepsweepai --framework <FRAMEWORK> --endpoint <URL>
```

### Supported Providers
- `mock` — No API keys required, synthetic responses
- `openai` — GPT models via OpenAI API
- `anthropic` — Claude models via Anthropic API  
- `google` — Gemini models via Google AI API
- `meta` — Llama models (requires endpoint)
- `self-hosted` — Custom model endpoints

### Environment Variables
- `OPENAI_API_KEY` — OpenAI API access
- `ANTHROPIC_API_KEY` — Anthropic API access
- `DEEPSWEEP_PRO_TOKEN` — Pro feature access
- `DEEPSWEEP_TELEMETRY=off` — Disable anonymous telemetry

## Privacy & Telemetry

DeepSweep AI collects **anonymous failure patterns** to improve test coverage:

- ✅ **Collected:** Test outcomes, latency metrics, OWASP category hits
- ❌ **Never collected:** Raw prompts, model outputs, user data
- 🔒 **Security:** SHA-256 hashes only, encrypted transport to AWS S3
- 🚪 **Opt-out:** `export DEEPSWEEP_TELEMETRY=off`

This helps the community identify emerging attack patterns while preserving privacy.
For complete details, see our [Privacy Policy](https://deepsweep.ai/privacy).

## Community

- **Discord:** [Join our community](https://discord.gg/Db5Zth2RKR) for support and discussions
- **Discussions:** [GitHub Discussions](https://github.com/deepsweep-ai/deepsweepai/discussions) for feature requests
- **Issues:** [GitHub Issues](https://github.com/deepsweep-ai/deepsweepai/issues) for bug reports

### Hall of Fame 🏆

Found a critical vulnerability? Share it in our Discord `#vulnerability-finds`:

| Agent Type     | Vulnerability              | Severity | Finder |
|----------------|----------------------------|----------|--------|
| Legal AI       | Data leakage via injection | Critical | @user1 |
| Banking Bot    | Unauthorized transactions  | Critical | @user2 |
| Code Assistant | Malware generation         | High     | @user3 |

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

- Use conventional commits: `feat:`, `fix:`, `docs:`
- All PRs require tests and documentation updates
- Run `make lint unit` before submitting

## Legal

- **Terms of Service:** https://deepsweep.ai/terms
- **Privacy Policy:** https://deepsweep.ai/privacy
- **Security Policy:** [SECURITY.md](SECURITY.md)
- **License:** [MIT License](LICENSE)

---

By using DeepSweep AI, you agree to our [Terms of Service](https://deepsweep.ai/terms) and [Privacy Policy](https://deepsweep.ai/privacy).

---

**DeepSweep AI** — Because AI agents shouldn't be deployed without security testing.
