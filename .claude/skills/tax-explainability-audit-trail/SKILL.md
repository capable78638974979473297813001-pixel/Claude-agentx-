---
name: tax-explainability-audit-trail
description: Make every number a tax engine produces explainable and auditable - named lines, calculation traces with inputs, rule references and formulas, provenance (ruleset hash, engine version), warnings, and human-readable explanations. Use when designing result objects, debugging a wrong number, building "why is my tax X" features, or preparing an engine for audit.
---

# Explainability and audit trail

## Line object

```python
@dataclass(frozen=True)
class Line:
    key: str               # "taxable_income"
    value: Decimal
    formula: str           # "max(0, agi - deduction)"
    inputs: tuple[str, ...]  # ("agi", "deduction")
    rule_ref: str | None   # "us-federal-income/2025#standard_deduction"
    note: str | None = None
```

A `Trace` is an ordered dict of lines. `explain(key)` walks inputs
recursively and prints a tree:

```
tax_owed = 1,234.00  = tax_after_credits - payments
├─ tax_after_credits = 5,234.00  = max(0, tax_before_credits - nonrefundable_credits)
│  ├─ tax_before_credits = ...   [rule us-federal-income/2025#ordinary_brackets]
...
```

## Provenance

Every result carries: engine version (git sha), ruleset id + content hash,
input hash, computed-at timestamp (outside the pure function), and all
warnings (unverified parameters, overrides, clamped values).

## Warnings are first-class

Clamping a negative to zero, using an override, a parameter marked
`verified: false`, an input outside the tested range: each adds a warning with
a code. Surfaces must show them.

## Debugging a wrong number

1. Get the trace for the bad result and the expected source worksheet.
2. Align worksheet lines to trace keys; find the first diverging line.
3. That line's `formula`, `inputs`, and `rule_ref` point at code or data.
4. Add a golden test for that path before fixing.

## Review checklist

- [ ] No unnamed intermediate values in calc code that affect results.
- [ ] Every rate/threshold used in a line has a `rule_ref`.
- [ ] Results are reproducible from (facts, ruleset hash, engine version).
