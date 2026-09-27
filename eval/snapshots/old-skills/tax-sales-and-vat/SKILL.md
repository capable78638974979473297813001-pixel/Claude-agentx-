---
name: tax-sales-and-vat
description: Build sales tax, VAT, and GST calculation - tax-inclusive vs exclusive pricing, multiple rates and stacked jurisdictions, product taxability categories, exemptions, rounding per line vs per invoice, discounts, shipping, returns, and reverse charge. Use for any transaction/indirect tax engine or checkout tax logic.
---

# Sales tax / VAT / GST

## Model

```
Invoice(lines, ship_from, ship_to, customer{type, exemptions, tax_id}, date, currency)
Line(id, amount, quantity, product_category, discount, is_tax_inclusive)
```

Result per line: `taxable_base`, per-jurisdiction `tax` components, and
invoice totals. Keep jurisdiction components separate (state, county, city,
district; or VAT standard/reduced/zero/exempt), because filing reports need them.

## Steps

1. **Determine jurisdictions** from the sourcing rule (origin vs destination,
   place-of-supply for services). Data, not code.
2. **Taxability**: `(jurisdiction, product_category, customer_type) → rate class`
   (standard, reduced, zero, exempt, not taxable). Zero-rated and exempt are
   different: exempt affects input-VAT recovery.
3. **Base**: price after line discounts; allocate invoice-level discounts to
   lines (largest-remainder, see `tax-money-math`); shipping taxable or not
   per jurisdiction.
4. **Rate**: sum stacked rates or compute each component; the rounding rule
   decides which.
5. **Rounding**: per line or per invoice per jurisdiction. They give different
   totals; make it a ruleset parameter and test both.
6. **Inclusive prices**: `net = gross / (1 + rate)`, round net, `tax = gross - net`.
7. **Reverse charge / B2B cross-border**: tax 0 on the invoice with a flag
   and legend; the buyer self-assesses.
8. **Returns/credit notes**: negate using the **original** transaction's
   rates and date, not today's.

## Tests

- Inclusive and exclusive give consistent totals for the same base.
- Per-line vs per-invoice rounding with many small lines (1,000 × 0.01).
- Discount allocation sums exactly.
- Exempt customer, exempt product, zero-rated product.
- Rate change on a date boundary.
- Return of a partially refunded line.
