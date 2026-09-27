---
name: tax-source-research
description: Research tax law parameters from primary sources and record them with citations - how to find official tables, revenue procedures, statutes, and agency publications, how to cross-check values, and how to mark anything unverified. Use before entering any rate, bracket, threshold, or rule into a tax ruleset.
---

# Tax source research

## Source hierarchy (highest first)

1. Statute / enacted legislation text.
2. Official regulations and binding guidance (e.g. annual inflation-adjustment
   notices, revenue procedures, ministerial orders).
3. Official forms, instructions, and publications (best for worksheets,
   rounding rules, and worked examples).
4. Official calculators and tables.
5. Secondary sources (firms, blogs, encyclopedias): **only for leads**, never
   the cited value.

## Procedure

1. State exactly what you need: parameter, jurisdiction, period, filing status.
2. Find it in the highest available source; record title, section/table,
   URL, and retrieval date.
3. Cross-check against a second official source (e.g. the form instructions
   vs the inflation-adjustment notice). Record both.
4. Copy numbers exactly as strings. Note rounding language verbatim
   ("rounded to the next lowest multiple of $50").
5. Enter into data with `verified: false`. A different agent verifies.

## When you can't reach sources

If web access is unavailable or the source is ambiguous:

- Use a clearly fake placeholder or a value from memory marked
  `UNVERIFIED: from model memory, check <expected source>` in the data.
- Add a Blockers entry on the board.
- The final report must list every unverified value.

Never present a remembered number as sourced.

## Law changes

Record effective dates and whether a change is retroactive. If legislation
is pending, model the current law and add a note; don't guess outcomes.
