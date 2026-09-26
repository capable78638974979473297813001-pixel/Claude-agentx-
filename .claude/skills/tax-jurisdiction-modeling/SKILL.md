---
name: tax-jurisdiction-modeling
description: Model multiple taxing jurisdictions - federal/state/local stacking, conformity and decoupling from a base jurisdiction, residency and part-year allocation, credits for taxes paid to other jurisdictions, and adding a new jurisdiction by composition. Use when an engine must support more than one country, state, province, or locality.
---

# Jurisdictions

## Composition over forks

A jurisdiction is a **pipeline definition**: a list of stages plus parameters.

```python
STATE_X = Pipeline(
    start_from=("federal", "agi"),                    # conformity anchor
    stages=[additions(STATE_X_ADDS), subtractions(STATE_X_SUBS),
            deductions("state_x"), bracket_tax("state_x"),
            credits("state_x"), other_state_credit()],
)
```

Conformity kinds (record which in data):

- **Rolling**: follows the base law as amended.
- **Static/fixed-date**: follows the base law as of a date; needs its own
  snapshot of the base parameters.
- **Selective**: follows except listed decoupled items (additions/subtractions).

## Dependency graph

Jurisdictions depend on each other's lines (state starts from federal AGI;
a credit for taxes paid to another state needs that state's tax). Build a
DAG, compute in topological order, and fail on cycles. Some pairs have
circular rules (mutual credits); resolve with the rule's specified order.

## Residency and allocation

- Resident: taxed on all income; nonresident: only on sourced income;
  part-year: split by period.
- Common method: compute tax on total income as if resident, then multiply by
  `sourced_income / total_income` (ratio method). Other jurisdictions tax
  sourced income directly. Parameterize the method.
- Sourcing rules (wages by work location, business by apportionment
  factors, investment income by domicile) are data + small functions.

## Local taxes

Localities often piggyback: a percentage of the state tax or a flat rate on a
state base. Treat them as tiny pipelines that read state lines.

## Adding a jurisdiction checklist

- [ ] Ruleset data with sources (see `tax-rules-as-data`).
- [ ] Pipeline definition, conformity type, and decoupled items.
- [ ] Residency/sourcing method.
- [ ] Golden tests from official examples.
- [ ] Interaction tests with its base and neighbor jurisdictions.
