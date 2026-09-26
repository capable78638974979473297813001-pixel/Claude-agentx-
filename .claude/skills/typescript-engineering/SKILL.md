---
name: typescript-engineering
description: TypeScript conventions - strict mode, discriminated unions, zod-style boundary validation, no number for money, vitest, and ESM packaging. Use when writing or reviewing TypeScript/JavaScript code.
---

# TypeScript engineering

- `"strict": true`, `noUncheckedIndexedAccess: true`.
- Model states as discriminated unions; exhaustive `switch` with `never` check.
- Validate external input at the boundary (zod or hand-written guards);
  internal code trusts types.
- Money: integer minor units (`bigint` for large) or a decimal library. Never
  do arithmetic on `number` money.
- `readonly` arrays/props for data passed between modules.
- Tests with vitest/jest; table tests via `it.each`.
- ESM, explicit exports, no default exports for libraries.
