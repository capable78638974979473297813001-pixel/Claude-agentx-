---
name: tax-api-and-scenarios
description: Design the public API and scenario tooling for a tax engine - compute/explain/diff endpoints, input schemas with validation errors users can act on, what-if scenarios, optimizers for elections, batch runs, and stable versioned outputs. Use when exposing a tax engine as a library, CLI, or HTTP service.
---

# Tax engine API and scenarios

## Surface

```python
compute(facts, jurisdiction, period, options=None) -> Result
explain(result, line_key) -> str
diff(result_a, result_b) -> list[LineDelta]     # what changed and why
scenarios(base_facts, variants: dict[str, Patch]) -> dict[str, Result]
optimize(facts, choices: list[Election], metric="total_tax") -> (best, table)
```

HTTP mirrors this: `POST /v1/compute`, `POST /v1/explain`, `POST /v1/scenarios`.

## Input schema

- Money fields are **strings** in JSON (`"12345.67"`), parsed to Decimal.
  Reject numbers with a clear error to prevent float drift from clients.
- Dates ISO-8601. Enums explicit (`filing_status: "married_joint"`).
- Validation returns all errors at once with JSON paths and fix hints.
- Unknown fields are errors (typos in tax inputs are silent money bugs).

## Output

```json
{
  "engine_version": "…", "ruleset": {"id": "…", "hash": "…"},
  "lines": {"taxable_income": {"value": "…", "rule_ref": "…"}, "...": {}},
  "summary": {"total_tax": "…", "refund_or_owed": "…"},
  "warnings": [{"code": "UNVERIFIED_PARAMETER", "detail": "…"}]
}
```

Line keys are a versioned contract: adding is fine, renaming is a breaking change.

## Scenarios

A patch is a small JSON-merge over facts (`{"wages": "+5000"}` style deltas
are convenient but define them precisely). Return per-scenario results plus a
diff against base. Marginal-rate curves = scenarios over a grid; batch them.

## CLI

`taxengine compute facts.json --jurisdiction us-federal --year 2025 --explain tax_owed`
Exit non-zero on validation errors; print warnings to stderr.
