---
name: security-review-lite
description: Quick security pass for application code - input validation, injection, authn/authz, secrets, PII handling, dependency risk, and logging. Use before shipping an API or when code handles personal or financial data (e.g. tax returns).
---

# Security review (lite)

- **Input**: validated at the boundary; size limits; no eval/pickle on untrusted data.
- **Injection**: parameterized SQL; no shell string building; escape output in HTML.
- **Authn/authz**: every endpoint checks who and whether they may access *this* record.
- **Secrets**: none in code or logs; loaded from env/secret store.
- **PII / financial data**: minimize fields collected; encrypt at rest; never log
  full identifiers (tax IDs, account numbers); mask in traces and errors.
- **Dependencies**: pinned, few, maintained.
- **Logging**: security events logged; sensitive values redacted.
Report findings with an exploit scenario, same format as `code-review-rigorous`.
