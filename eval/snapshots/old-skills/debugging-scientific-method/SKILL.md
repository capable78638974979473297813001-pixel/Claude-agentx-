---
name: debugging-scientific-method
description: Debug by hypothesis and experiment - reproduce, minimize, form ranked hypotheses, run discriminating experiments, fix root cause, add a regression test. Use for any failing test, wrong output, crash, or flaky behavior.
---

# Debugging

1. **Reproduce** with one command. No repro, no fix.
2. **Minimize** the input until removing anything makes the bug vanish.
3. **Read the actual error** fully, including the first frame in your code.
4. **Hypothesize**: list 2–4 causes ranked by likelihood × cheapness to test.
5. **Experiment**: pick the check that best separates hypotheses (a print, an
   assertion, bisecting commits or inputs). Predict the result before running.
6. **Fix the root cause**, not the symptom. If you clamp, catch, or retry,
   explain why the underlying cause is acceptable.
7. **Regression test** that fails before the fix.

"Flaky" is a symptom. Look for ordering, time, randomness, shared state, and
concurrency.
