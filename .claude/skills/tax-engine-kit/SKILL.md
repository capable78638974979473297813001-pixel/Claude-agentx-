---
name: tax-engine-kit
description: One-command launch of the tax-engine swarm - spins up architect, researcher, calc engineers, test oracle, auditor, and API builder agents with the tax skill pack to build a tax calculation engine. Use when the user says "build a tax engine", "tax calculator", "/tax-engine-kit", or "go" with a tax goal.
---

# Tax engine kit

Follow the `swarm` skill with this ready-made plan. Adjust scope to what the
user asked for (income tax only? payroll? VAT? which jurisdiction/year?).
If they didn't say, default to: **a Python income-tax engine with one
jurisdiction, pluggable rulesets, full trace, golden + property tests, and a
CLI**, and state that assumption in the board.

Build in `projects/tax-engine/` (or `projects/<name>/`); every path below is
relative to that directory. Print the machine-readable plan with
`python3 tools/skillforge.py kit tax-engine`, and forge each listed blend into
`.swarm/skills/<agent>.md` so the agent can read it alongside its preloaded skills.

## Phase 0 — spine (sequential, lead or `tax-architect`)

`tax-architect` writes:

- `engine/money.py`, `engine/trace.py`, `engine/facts.py` interfaces.
- The ruleset schema and loader stub in `engine/rules/`.
- The stage list and named-line catalog in `.swarm/board.md` → Interfaces.
- `pyproject.toml` with pytest (and hypothesis if available).

Done when `python -c "import engine"` works and the board lists interfaces.

## Phase 1 — fan out (parallel, one message)

| Agent | Owns | Delivers |
|---|---|---|
| `tax-rules-researcher` | `rules_data/` | Ruleset data with citations, `verified: false` |
| `tax-calc-engineer` | `engine/calc/` | Brackets, deductions, phase-outs, credits stages |
| `tax-test-oracle` | `tests/` | Golden vectors, properties, boundary generator, naive differential impl |
| `tax-api-builder` | `engine/api.py`, `engine/cli.py` | compute/explain/diff/scenarios + CLI |

Optional, if in scope: `tax-indirect-engineer` (`engine/indirect/`),
`tax-payroll-engineer` (`engine/payroll/`).

## Phase 2 — verify (parallel)

- `tax-rules-researcher` (second instance, prompted as verifier) re-checks
  every value the first entered and flips `verified: true` only on a match.
- `tax-auditor` reviews the whole diff: money math, trace completeness,
  hard-coded numbers, rounding sites, tests that assert engine output against
  itself.

## Phase 3 — integrate (lead)

Run `pytest -q` and a CLI demo. Route failures to the owning agent. Loop
until green and the auditor has no blocking findings.

## Report template

- Built: modules and what each computes.
- Verified: test counts, the commands, a sample `explain` tree.
- Unverified: every `verified: false` parameter and every `UNVERIFIED` note.
- Next: jurisdictions/years/features not yet covered.

Reminder: the engine is software, not tax advice; the report should say so
where users will read results.
