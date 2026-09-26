---
name: tax-credits-engine
description: Model tax credits - nonrefundable vs refundable vs partially refundable, statutory ordering, limitation by liability, per-person/per-dependent credits, earned-income style phase-in/plateau/phase-out curves, and credit carryforwards. Use when implementing or reviewing any credit logic in an income tax engine.
---

# Credits

## Kinds

- **Nonrefundable**: can reduce tax to zero, not below. Excess is lost or
  carried forward (per rule).
- **Refundable**: paid out even with zero liability; treated like a payment.
- **Partially refundable**: a nonrefundable portion plus a refundable portion
  capped by its own formula (often based on earned income over a threshold).

## Ordering

Nonrefundable credits apply in a **statutory order** because each is limited
by the liability remaining after the previous ones. Encode the order in data:

```yaml
credit_order: [credit_a, credit_b, credit_c]   # cite the ordering rule
```

Algorithm:

```
remaining = tax_before_credits
for c in order:
    allowed = min(c.tentative, remaining, c.own_limit)
    remaining -= allowed
    carryforward[c] = c.tentative - allowed if c.carries_forward else 0
refundable_total = sum(r.amount for r in refundable)
balance = remaining - payments - refundable_total
```

Each `allowed`, `carryforward`, and `remaining` is a named trace line.

## Curves (earned-income style)

Three zones: phase-in (`rate_in * earned`), plateau (max), phase-out
(`max - rate_out * (max(earned, agi) - start_out)`). Parameters vary by number
of qualifying children and filing status; keep them all in data. Official
tables often use bands; check whether table or formula is authoritative.

## Eligibility

Eligibility is a separate, testable function returning `(eligible, reasons)`.
Never bury eligibility checks inside the amount formula; reviewers need to
see *why* someone got zero.

## Tests

- Liability smaller than one credit, smaller than the sum, zero liability.
- Order swap test: prove ordering changes results where it should.
- Refundable with zero tax.
- Curve boundaries: start of plateau, start of phase-out, exact zero point.
