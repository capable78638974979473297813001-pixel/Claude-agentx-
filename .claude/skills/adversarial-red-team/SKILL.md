---
name: adversarial-red-team
description: Attack a design or implementation to find where it breaks - hostile and edge inputs, broken assumptions, spec ambiguities, and "the team agreed too easily" checks. Use when reviewing an implementation, when several reviewers converge on one answer, or before trusting a numeric engine.
---

# Adversarial red team

Your job is to make it fail. Success is a reproducible failure, not praise.

- **Inputs**: zero, negative, empty, huge, one cent past each threshold,
  unicode, duplicated items, reordered items, missing optional fields.
- **Assumptions**: list what the implementation assumes (single currency,
  calendar tax year, one employer, resident). Break each.
- **Spec ambiguity**: find sentences in the source/spec with two readings and
  check which one the code took.
- **Consensus check**: if every reviewer used the same formula, derive it
  independently from the source. Shared blind spots are the main risk.
- **Oracle check**: do the tests compare against something independent?
Report each finding with a failing input and the observed vs expected output.
