---
name: tax-engine-architecture
description: Architecture for a tax calculation engine - pipeline stages, pure-function calculators, rules-as-data, jurisdiction/year versioning, and a traceable result object. Use when designing or restructuring any income, payroll, sales/VAT, or property tax engine, or when deciding module boundaries for a tax codebase.
---

# Tax engine architecture

## Core shape

A tax engine is a **pure function**:

```
compute(facts, ruleset) -> Result(lines, trace, warnings)
```

- `facts`: what happened (income items, household, purchases, location, dates).
  Validated, normalized, immutable.
- `ruleset`: the law for one jurisdiction and one period, loaded from data
  (see `tax-rules-as-data`). No rates or thresholds in code.
- `Result`: named output lines (e.g. `taxable_income`, `tax_before_credits`),
  plus a trace that explains each line (see `tax-explainability-audit-trail`).

No I/O, clock reads, or globals inside `compute`. That single property makes
the engine testable, cacheable, reproducible, and safe to run "what-if".

## Pipeline (income tax)

Each stage is a small function taking the previous stage's lines:

1. **Normalize** facts: currency, dates, allocate to tax period, attach IDs.
2. **Classify** income: wages, interest, dividends (ordinary/qualified),
   capital gains (short/long), business, pass-through, exempt.
3. **Aggregate** to gross income.
4. **Adjustments** ("above-the-line") → adjusted gross income.
5. **Deductions**: max(standard, itemized) with limits and phase-outs.
6. **Taxable income** = max(0, AGI − deductions − other exclusions).
7. **Tax**: ordinary brackets, preferential-rate worksheets, surtaxes, AMT-like
   parallel computations (compute both, take the rule's combination).
8. **Credits**: nonrefundable (limited to liability, in statutory order),
   then refundable.
9. **Payments**: withholding, estimates.
10. **Balance**: refund or amount owed; penalties/interest are a separate module.

Sales/VAT and payroll use the same skeleton with different stages
(see `tax-sales-and-vat`, `tax-payroll-withholding`).

## Module layout (suggested)

```
engine/
  money.py          # Decimal helpers, rounding modes (tax-money-math)
  facts.py          # input dataclasses + validation
  rules/            # loader + schema; data lives in rules_data/
  calc/             # one file per stage; pure functions
  trace.py          # line/trace objects
  jurisdictions/    # composition of stages per jurisdiction (federal, state…)
  api.py            # thin facade: compute(), explain(), diff_scenarios()
rules_data/<jurisdiction>/<year>.yaml|json
tests/golden/       # sourced worked examples (tax-golden-test-vectors)
```

## Design rules

- **Stages don't know about jurisdictions**; jurisdictions compose stages and
  pass parameters. A state that "conforms to federal AGI with modifications"
  is a composition, not a fork.
- **Every intermediate is a named line.** If a worksheet has 12 lines, the
  engine has 12 named values. This is what makes explanation and review work.
- **Parallel regimes** (AMT, alternative minimum, minimum tax, exemption vs
  credit choice): compute each fully, then apply the combining rule.
- **Elections** (itemize vs standard, filing jointly vs separately) are inputs,
  with an optional optimizer that tries each and picks by an explicit metric.
- **Effective dating**: rules resolve by the fact's date, not `today()`. Mid-year
  changes produce two rule segments, and the engine prorates by the law's
  method.
- **Versioning**: the result records ruleset id + hash and engine version.

## Anti-patterns

- `if year == 2024:` in calculation code.
- Floats anywhere near money.
- One giant function that mirrors the form top to bottom with no named lines.
- Rounding "at the end" when the law rounds per line (or vice versa).
- Mutating facts inside stages.
