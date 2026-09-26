---
name: refactoring-safe
description: Change code structure without changing behavior - characterization tests first, small mechanical steps, one move at a time, run tests after each. Use when restructuring code, extracting modules, renaming across files, or cleaning up after a swarm integrates.
---

# Safe refactoring

1. **Pin behavior**: if tests are thin, add characterization tests (snapshot
   current outputs, including odd ones) before touching code.
2. **One move at a time**: rename, extract function, move module, inline.
   Run tests after each.
3. **Don't mix** refactors with behavior changes in the same step/commit.
4. **Mechanical tools** over hand edits for renames (grep all call sites,
   including strings, configs, docs).
5. **Stop** when the code is good enough for the next feature, not perfect.
