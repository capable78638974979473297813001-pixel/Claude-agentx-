---
name: api-design
description: Design library and HTTP APIs that are hard to misuse - small surfaces, explicit types, consistent naming, actionable errors, versioning, idempotency, and pagination. Use when publishing an interface other agents, services, or users will call.
---

# API design

- **Small surface**: few entry points, each doing one thing. Options objects
  over long positional parameter lists.
- **Types at the boundary**: validate once at the edge; inside, trust types.
- **Names** say units and meaning: `amount_cents`, `rate`, `effective_date`.
- **Errors**: machine code + human message + where (field path) + how to fix.
  Collect all validation errors, not just the first.
- **Versioning**: `/v1/`; additive changes are fine; renames/removals are breaking.
- **Idempotency** for writes (client-supplied idempotency key).
- **Pagination** with opaque cursors, not offsets, for mutable collections.
- **Determinism**: same input, same output; no hidden clock or randomness.
- Write the usage example before the implementation. If the example is
  awkward, the API is.
