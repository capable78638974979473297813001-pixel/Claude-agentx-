---
name: tax-filing-status-and-household
description: Model taxpayers, households, filing status, dependents, and qualifying-person tests as data plus explicit eligibility functions. Use when a tax engine needs per-status thresholds, dependent-based amounts, or household composition rules.
---

# Filing status and household

## Data model

```python
@dataclass(frozen=True)
class Person:
    id: str
    birth_date: date
    relationship: str          # self | spouse | child | parent | other
    months_lived_with: int
    is_student: bool = False
    is_disabled: bool = False
    gross_income: Decimal = Decimal("0")
    support_provided_by_taxpayer_pct: Decimal | None = None

@dataclass(frozen=True)
class Household:
    taxpayer: Person
    spouse: Person | None
    others: tuple[Person, ...]
    marital_status_at_year_end: str
    elects_joint: bool | None
```

Filing status and dependency are **derived**, never typed into the facts
without a derivation path (allow an override flag that gets recorded in the
trace).

## Tests as functions

Each qualifying test (age as of year end, residency months, support,
relationship, income limit, joint-return test) is a small function returning
`TestResult(passed, reason, rule_ref)`. A dependent qualifies when the rule's
combination of tests passes. Output the table of results; that is the
explanation users need.

## Pitfalls

- Age computed as of the rule's date (often end of tax year; some rules use
  special birthday conventions). Put the convention in data.
- Status-dependent parameters: every threshold lookup must pass status;
  missing statuses in data should error, not default to single.
- Tie-breaker rules when two taxpayers could claim the same person.
- Year of death/marriage/divorce edge cases: model marital status by date.
