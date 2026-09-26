---
name: tax-money-math
description: Correct money arithmetic for tax and finance code - Decimal or integer minor units, explicit rounding modes and points, allocation without losing cents, percentage and rate math, and currency handling. Use whenever code adds, multiplies, rounds, splits, or compares monetary amounts.
---

# Money math

## Representation

- Python: `decimal.Decimal` built from **strings** (`Decimal("0.07")`, never
  `Decimal(0.07)`), or `int` cents. JS/TS: integer minor units or a decimal
  library (`decimal.js`, `big.js`); never `number` for money math.
- Store the currency with the amount when more than one currency can exist.
- Rates are Decimals too: `Decimal("0.2200")`.

## Rounding is a rule, not a formatting step

Each rounding needs three answers, and the law/spec gives them:

1. **Where**: per line item, per line on the form, per invoice, or once at the end.
2. **To what**: cents, whole units, nearest 10/50/100 (tax tables often use bands).
3. **Mode**: half-up (common in tax), half-even (banker's; common in
   accounting/ledgers), down/truncate (some withholding and "disregard
   cents" rules), up/ceiling (some fees).

Put these in the ruleset and call one helper:

```python
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN, ROUND_DOWN, ROUND_UP

MODES = {"half_up": ROUND_HALF_UP, "half_even": ROUND_HALF_EVEN,
         "down": ROUND_DOWN, "up": ROUND_UP}

def round_money(x: Decimal, step: str = "0.01", mode: str = "half_up") -> Decimal:
    step_d = Decimal(step)
    return (x / step_d).quantize(Decimal("1"), rounding=MODES[mode]) * step_d
```

Always test the tie cases: `x.xx5`, negative values (`-2.5` half_up →
`-3` in Decimal, which rounds away from zero; confirm that matches the rule),
and exact multiples.

## Allocation (splitting without losing cents)

Splitting 100.00 three ways must sum to 100.00. Use largest-remainder:

```python
def allocate(total: Decimal, weights: list[Decimal], step=Decimal("0.01")):
    raw = [total * w / sum(weights) for w in weights]
    floored = [(r // step) * step for r in raw]
    leftover = int((total - sum(floored)) / step)
    order = sorted(range(len(raw)), key=lambda i: raw[i] - floored[i], reverse=True)
    for i in order[:leftover]:
        floored[i] += step
    return floored
```

State the tie-break (index order) so results are deterministic.

## Common traps

- `sum()` of Decimals starts at int 0: fine. Mixing Decimal and float: raises
  in Python (good), silently wrong in JS (bad).
- Percent vs rate: store `0.0725`, display `7.25%`. Name fields `*_rate`.
- Tax-inclusive back-calculation: `net = gross / (1 + rate)`, then round, then
  `tax = gross - net` so the parts sum exactly.
- Comparisons against thresholds: decide `<` vs `<=` from the statute text
  ("exceeds" means `>`; "at least" means `>=`).
- Negative amounts: refunds/credits/returns. Test them.
- Division by zero on empty weights, zero income, zero quantity.

## Checklist

- [ ] No floats in money paths (grep for `float(` and literal `0.` in calc code).
- [ ] Every rounding site names its rule source.
- [ ] Splits sum exactly to the total.
- [ ] Tie, negative, zero, and huge (1e12) values tested.
