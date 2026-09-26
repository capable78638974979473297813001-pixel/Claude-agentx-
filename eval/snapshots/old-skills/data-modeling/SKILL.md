---
name: data-modeling
description: Model domain data - entities, value objects, invariants, immutability, identity, normalization vs denormalization, temporal (effective-dated) records, and schema evolution. Use when designing dataclasses, database tables, JSON schemas, or rule/config files.
---

# Data modeling

- Separate **entities** (have identity, change over time) from **value objects**
  (immutable, compared by value: Money, DateRange, Address).
- Encode **invariants** in constructors: a DateRange with end < start can't exist.
- Make illegal states unrepresentable: enums over strings, required fields
  required, unions for mutually exclusive shapes.
- **Temporal data**: `valid_from`/`valid_to` on records that change by law or
  contract; query "as of" a date; never overwrite history.
- Keep **source/provenance** fields on data entered by humans or researched.
- **Schema evolution**: additive by default; migrations are code with tests;
  version the schema in the file.
- Prefer frozen dataclasses / readonly types for anything passed between stages.
