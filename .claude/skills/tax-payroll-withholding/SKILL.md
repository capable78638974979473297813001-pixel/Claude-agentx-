---
name: tax-payroll-withholding
description: Payroll tax and income tax withholding calculations - annualization, pay-frequency conversion, percentage-method tables, wage-base caps for social insurance, employer vs employee shares, year-to-date tracking, and supplemental wages. Use when building payroll engines or paycheck calculators.
---

# Payroll and withholding

## Shape

```
withhold(pay_period_facts, ytd, employee_elections, ruleset) -> PaycheckTaxes
```

`ytd` is an explicit input (wages and taxes so far this year). The function
returns the new YTD as output. No database reads inside.

## Percentage method pattern

1. Gross for period → subtract pre-tax deductions → taxable wages for period.
2. **Annualize**: `× periods_per_year` (weekly 52, biweekly 26, semimonthly 24,
   monthly 12; daily/misc as the rule defines).
3. Apply adjustments from the employee's election form (credits, extra income,
   deductions) per the published worksheet.
4. Look up the annual withholding schedule (a bracket schedule; reuse
   `tax-progressive-brackets`).
5. **De-annualize**: `÷ periods_per_year`, add extra flat withholding, round
   per the rule (often to whole units or cents).

## Wage-base caps

Social-insurance taxes often stop at an annual wage base:

```
taxable_this_period = max(0, min(wages, cap - ytd_wages))
```

Some have an additional rate above a threshold with no employer match. Track
employer and employee shares as separate lines.

## Supplemental wages

Bonuses may use a flat rate or the aggregate method (add to regular wages,
compute, subtract what regular wages alone would withhold). Make method an
input; test both.

## Tests

- Paycheck that crosses the wage-base cap mid-period.
- Each pay frequency gives consistent annual totals (within rounding).
- Zero and negative (correction) paychecks.
- Mid-year rule change: periods paid after the effective date use new rules.
