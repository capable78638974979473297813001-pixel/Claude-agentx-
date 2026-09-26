---
name: verify-before-claiming
description: Never report work as done, correct, or passing without running a command that proves it, and report exactly what was and wasn't verified. Use at the end of every task and every agent handoff.
---

# Verify before claiming

- "Done" = the acceptance command ran and passed in this session. Paste the
  command and the summary line of its output.
- "Should work" is not a status. Either run it or list it as unverified.
- Report failures verbatim (first error, not a paraphrase).
- Distinguish: built, ran, tested, reviewed. Each is a separate claim.
- If a step was skipped (no network, missing tool), say so and what it blocks.
