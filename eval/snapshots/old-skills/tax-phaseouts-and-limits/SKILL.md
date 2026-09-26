---
name: tax-phaseouts-and-limits
description: Implement phase-outs, phase-ins, caps, floors, percentage-of-income limits, carryforwards, and "lesser of / greater of" rules in tax engines, including step-rounding phrases like "or fraction thereof". Use when a deduction, credit, or exemption shrinks, grows, or is limited based on income or other amounts.
---

# Phase-outs and limits

## Patterns

| Pattern | Formula |
|---|---|
| Linear phase-out | `reduction = max(0, base - start) * rate`; `value = max(0, full - reduction)` |
| Ratio phase-out | `value = full * max(0, 1 - (base - start) / width)` (clamp to [0, full]) |
| Step phase-out | `steps = ceil((base - start) / step)`; `reduction = steps * per_step` |
| Phase-in | `value = min(full, max(0, base - start) * rate)` |
| Cap | `min(x, cap)` |
| Floor ("only the part over N% of income") | `max(0, x - pct * income)` |
| Lesser/greater of | named lines for both candidates, then `min`/`max` |

Translate statute phrasing literally:

- "reduced by 5% of the amount by which X exceeds Y" → linear, `rate=0.05`.
- "reduced by $50 for each $1,000 (or fraction thereof)" → step, ceiling.
- "for each $2,500 (or fraction thereof)" vs "for each full $2,500" →
  ceiling vs floor. This one word changes results; put it in data as
  `step_rounding: up|down`.
- "but not below zero" → clamp.
- "exceeds" → strictly greater.

## Implementation notes

- Keep `base` explicit and named: phase-outs key off a specific *modified*
  income (e.g. AGI plus certain exclusions). Compute that modified base as its
  own named line; it is the most common source of bugs.
- Order matters when limits interact (a cap applied before or after a
  phase-out gives different answers). Follow the form/worksheet order and
  write it down in the trace.
- **Carryforwards/carrybacks**: the engine returns the unused amount as an
  output line; the next period's facts take it as input. No hidden state.
- Phase-outs create marginal rates above bracket rates; expose the numeric
  marginal rate so users see the cliff.

## Tests

- base = start − 0.01, start, start + 0.01, start + one full step, fully phased out, and far above.
- Step phrasing: amounts exactly on a step boundary and one cent past it.
- Joint vs single thresholds.
- Property: phase-out value is monotone non-increasing in base.
