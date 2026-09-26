---
name: code-review-rigorous
description: Review code for correctness bugs first, then design, tests, and clarity, producing ranked findings with concrete failure scenarios. Use when reviewing a diff, a PR, another agent's output, or before declaring work done.
---

# Rigorous code review

## Order of attention

1. **Correctness**: wrong results, crashes, data loss, races, boundary errors,
   wrong units, silent fallbacks.
2. **Contract**: does it do what the spec/board says? Missing cases?
3. **Tests**: do they fail if the code is wrong? (Tests comparing the code
   to itself prove nothing.)
4. **Design**: coupling, naming, needless abstraction.
5. **Style**: only if it hurts reading.

## A finding must have

- Location (`path:line`).
- The defect in one sentence.
- A concrete failure scenario: input/state → wrong output.
- Severity: blocking / should-fix / nit.
- A suggested fix when it's cheap to give.

No failure scenario → it's a question, not a finding. Say so.

## Method

- Read the tests first to learn intended behavior, then the code.
- For each branch, ask what input reaches it and whether that's tested.
- Trace one realistic input end to end by hand.
- Re-run the tests yourself when you can.
