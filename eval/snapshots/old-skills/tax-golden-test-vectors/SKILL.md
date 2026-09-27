---
name: tax-golden-test-vectors
description: Testing strategy for tax engines - sourced golden test vectors from official worked examples, property-based invariants (monotonicity, continuity, bounds, symmetry), boundary generators, differential testing against an independent implementation, and regression snapshots of full traces. Use when writing or reviewing tests for any tax or financial calculation.
---

# Tax test strategy

Tax bugs are silent: the code returns a plausible number. Layer tests so a
wrong number has to get past several independent checks.

## 1. Golden vectors (sourced)

```yaml
# tests/golden/us_federal_2025/single_wages_only.yaml
source: "<official publication / worksheet example, section, page>"
facts: {filing_status: single, wages: "<n>"}
expect:
  taxable_income: "<n>"
  tax: "<n>"
tolerance: "0.00"      # exact unless the source rounds differently; explain if not
```

- Only numbers from a real source or a hand computation shown step by step in
  the file. Never generate expectations by running the engine.
- One vector per distinctive path (each status, each credit, each worksheet
  branch), plus the source's own examples.

## 2. Properties (hypothesis / fast-check)

- **Monotone**: more income never lowers tax (where the law guarantees it;
  cliffs are real in some regimes, document exceptions).
- **Continuity** at bracket thresholds.
- **Bounds**: `0 <= tax <= income × top_marginal_rate` (+ surtaxes).
- **Rounding sanity**: result has the ruleset's precision.
- **Split invariance**: splitting one wage item into two equal items doesn't change tax.
- **Order invariance**: input item order doesn't matter.
- **Inclusive/exclusive consistency** for VAT.
- **Allocation sums exactly** to totals.

## 3. Boundaries (generated)

For every threshold in the ruleset data, auto-generate `t - 0.01, t, t + 0.01`.
Read thresholds from the data, so a new year gets boundary tests for free.

## 4. Differential testing

Write a second, deliberately naive implementation (closed-form bracket math,
a straight transcription of the worksheet) and compare on thousands of random
inputs. Two implementations by different agents with different skill loadouts
are the swarm's best bug detector.

## 5. Trace snapshots

Snapshot the full named-line trace for a set of representative returns. A
diff shows *which* line changed when rules or code change. Review snapshot
updates line by line; never bulk-accept.

## Test hygiene

- Money in tests is strings → Decimal.
- Test names state the rule: `test_step_phaseout_rounds_partial_step_up`.
- A failing golden test is a bug until proven that the source is wrong;
  record source disputes on the board.
