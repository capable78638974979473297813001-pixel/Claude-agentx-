---
name: ecommerce-checkout
description: E-commerce checkout domain pack.
---

- Cart → shipping → tax → payment; tax depends on ship-to address, product category, and customer exemptions.
- Show tax-inclusive prices where required; recompute on address change.
- Cache tax quotes with the inputs that produced them; commit tax on order, reverse on refund.

Never enter a rate, threshold, or date from memory as verified; cite a primary source or mark it UNVERIFIED.
