---
name: tax-rules-as-data
description: Model tax law parameters (brackets, rates, thresholds, phase-outs, caps, inflation indexing, effective dates) as versioned, schema-validated data with citations, instead of code. Use when adding a tax year or jurisdiction, designing a ruleset schema, or reviewing hard-coded tax numbers.
---

# Rules as data

## Principle

Code says **how** a rule works (a bracket schedule, a linear phase-out).
Data says **which numbers** apply for a jurisdiction, period, and status.
Adding next year should be a data PR with citations, not a code change.

## Schema sketch (YAML)

```yaml
ruleset: us-federal-income
period: {start: 2025-01-01, end: 2025-12-31}
status: draft            # draft | verified | superseded
sources:
  - id: src1
    title: "<primary source title, e.g. revenue procedure / statute / official table>"
    url: "<link>"
    retrieved: 2026-01-15
parameters:
  ordinary_brackets:
    type: bracket_schedule
    by: filing_status
    values:
      single:
        - {over: "0",     rate: "0.10"}
        - {over: "<n>",   rate: "0.12"}
    rounding: {step: "0.01", mode: half_up}
    source: src1#table-1
    verified: false      # flips to true only after a second agent checks the source
  standard_deduction:
    type: amount
    by: filing_status
    values: {single: "<n>", married_joint: "<n>"}
    source: src1#sec-3
  some_credit_phaseout:
    type: linear_phaseout
    start: {single: "<n>"}
    rate: "0.05"          # reduce by 5 cents per dollar over start
    step: "1000"          # or: reduce per $1,000 (or fraction) over start
    step_rounding: up     # "or fraction thereof" means ceiling
    source: src1#sec-7
```

`<n>` placeholders are deliberate: fill them only from the cited source.

## Parameter types (reuse these; add new ones rarely)

`amount`, `rate`, `bracket_schedule`, `linear_phaseout`, `step_phaseout`,
`cap`, `floor`, `table_lookup` (e.g. official tax tables with bands),
`indexed_amount` (base amount + indexing method + rounding-down-to rule),
`boolean_conformity` (state follows federal item X or not).

## Loader requirements

- Validate against a schema at load; fail loudly on unknown keys.
- Resolve by `(jurisdiction, date, filing_status)`; error if no ruleset covers
  the date instead of silently using the latest.
- Parse all numbers as Decimal from strings.
- Expose `ruleset.id`, `ruleset.hash` for result provenance.
- A `status: draft` or `verified: false` parameter produces a warning in the
  result, which the UI/report must surface.

## Verification workflow

1. Researcher agent enters values with `source` and `verified: false`.
2. A **different** agent re-reads the source and flips `verified: true`,
   recording its name. Disagreements go to the board's Blockers.
3. A test asserts no `verified: false` remains in any `status: verified` ruleset.

## Anti-patterns

- Numbers from memory. If you "know" a bracket threshold, you still cite it.
- One ruleset file with `if` logic in it (templating law is code; keep it in code).
- Silent fallback to a previous year.
