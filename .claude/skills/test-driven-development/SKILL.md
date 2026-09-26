---
name: test-driven-development
description: Red-green-refactor workflow - write a failing test that states the requirement, make it pass with the smallest change, then clean up. Use when implementing new behavior with a clear spec, fixing a bug (reproduce first), or when another agent will build against your tests.
---

# Test-driven development

1. **Red**: write one test that states one requirement. Run it and see it
   fail for the right reason (not an import error).
2. **Green**: smallest code that passes. Hard-coding is allowed briefly; the
   next test will force generality.
3. **Refactor**: remove duplication with tests green. Run them.
4. Repeat with the next requirement or edge case.

Bug fixes: first a test that reproduces the bug and fails, then the fix.

A failing test can be the interface for the change: make it pass without
editing the assertion. Disputes about a test change the spec, not the expected
value, until the spec itself is wrong.
