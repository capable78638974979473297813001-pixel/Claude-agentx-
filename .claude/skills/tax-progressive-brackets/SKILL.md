---
name: tax-progressive-brackets
description: Compute progressive (marginal) tax from bracket schedules correctly - the algorithm, tax-table bands vs exact computation, preferential-rate stacking for capital gains, marginal/effective rate reporting, and the boundary tests that catch off-by-one bugs. Use when implementing or testing any tiered or bracketed rate.
---

# Progressive brackets

## Algorithm

Brackets are `(over, rate)` pairs sorted ascending by `over`, first `over = 0`.

```python
from decimal import Decimal

def bracket_tax(income: Decimal, brackets: list[tuple[Decimal, Decimal]]) -> Decimal:
    if income <= 0:
        return Decimal("0")
    tax = Decimal("0")
    for i, (lower, rate) in enumerate(brackets):
        upper = brackets[i + 1][0] if i + 1 < len(brackets) else None
        if income <= lower:
            break
        top = income if upper is None or income < upper else upper
        tax += (top - lower) * rate
    return tax
```

Round per the ruleset **after** summing, unless the law says per-bracket.

Equivalent closed form (useful as a test oracle): precompute the cumulative
tax at each bracket floor, then `tax = base[k] + (income - over[k]) * rate[k]`
where `k` is the bracket containing income. Test that both agree.

## Tax tables vs exact

Some jurisdictions require official tables below a threshold: income is put
in a band (e.g. width 50), tax is computed at the band **midpoint**, then
rounded. Model it as `table_lookup` data or as a band-midpoint rule. Don't
mix exact computation with table-required ranges, results differ by dollars.

## Preferential rates (capital gains / qualified dividends pattern)

Ordinary income fills the brackets first; preferential income "stacks on top"
and is taxed by the preferential schedule based on where it lands. Compute:

1. `ordinary = taxable - preferential` (floor at 0).
2. Tax ordinary with ordinary brackets.
3. Walk the preferential schedule starting from `ordinary` as the floor.
4. Compare with the regular-schedule tax on everything if the rule says
   "the smaller of" (it often does). Keep both as named lines.

## Reported rates

- **Marginal rate**: rate on the next unit of income. Compute numerically as
  `(tax(income + 1) - tax(income)) / 1` too, since phase-outs create hidden
  marginal rates above the bracket rate.
- **Effective rate**: `tax / income` (define which income: gross, AGI, taxable).

## Boundary tests (always)

For each threshold `t`: incomes `t - 0.01`, `t`, `t + 0.01`. Plus 0, negative,
the first bracket only, and something enormous.

Properties to test (see `tax-golden-test-vectors`):

- Monotone: `tax(a) <= tax(b)` for `a <= b`.
- Continuous: no jump at thresholds (difference at `t±0.01` ≤ top rate × 0.02).
- Bounded: `0 <= tax(x) <= x * top_rate`.
- Marginal rate at any point equals some schedule rate (absent phase-outs).
