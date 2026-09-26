---
{
  "schema_version": 1,
  "scope": "checkout",
  "revision": "working-tree",
  "watches": [
    "src/checkout.py",
    "tests/test_checkout.py",
    "docs/checkout.md"
  ],
  "sources": [
    {
      "path": "src/checkout.py",
      "section": "FEE and total"
    },
    {
      "path": "tests/test_checkout.py",
      "section": "test_total"
    },
    {
      "external": "checkout-owner-answer",
      "section": "Q-001 checked answer"
    },
    {
      "path": "docs/checkout.md"
    }
  ],
  "id": "CAP-fee",
  "kind": "product",
  "title": "Checkout fee",
  "behaviors": [
    "PB-001"
  ],
  "implements": [],
  "depends_on": [
    "CMP-checkout"
  ],
  "verification": []
}
---

# Checkout fee

## Purpose and evidence

Intended and observed: checkout adds a fixed fee of 3. docs/checkout.md and the checked product-owner answer identify its purpose as covering packing costs.

<a id="pb-001"></a>
### PB-001 — Add the checkout fee

For a supplied subtotal, `total(subtotal)` returns `subtotal + 3`; the existing check uses subtotal 10 and expects 13. The sources do not define currency or an input-validation contract. See [implementation and checks](../engineering/checkout.md).

## Ownership and handoff

Checkout owns the fee addition to a supplied subtotal. It does not determine inventory availability, as stated in docs/checkout.md. src/checkout.py::total returns the computed total to its caller; caller identity, payment collection, and inventory ownership are not established by this fixture.
