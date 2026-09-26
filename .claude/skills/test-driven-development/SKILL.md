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

In a swarm, a test-owning agent can publish failing tests as the interface;
the implementing agent's job is to make them pass without editing them.
Disputes about a test go on the board, not into an edited assertion.
