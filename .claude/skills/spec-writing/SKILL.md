---
name: spec-writing
description: Turn a fuzzy goal into a short, testable spec - scope, non-goals, inputs/outputs, examples, acceptance commands, and open questions. Use at the start of a large feature, or when people disagree about what to build.
---

# Spec writing

Keep it to one screen:

- **Goal**: one sentence a user would recognize.
- **Non-goals**: what we won't do this round (prevents scope creep in agents).
- **Interfaces**: function signatures / endpoints / file formats with types.
- **Examples**: 3–5 input → output pairs, including an edge case and an error.
- **Acceptance**: the exact commands that prove it works.
- **Open questions**: each with a default we'll use if nobody answers.

Write assumptions as decisions ("Assume single currency USD") so agents stop
re-litigating them.
