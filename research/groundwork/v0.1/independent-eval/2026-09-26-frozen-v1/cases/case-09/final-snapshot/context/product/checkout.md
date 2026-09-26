---
{
  "schema_version": 1,
  "scope": "checkout",
  "revision": "working-tree",
  "sources": [
    {
      "path": "src/checkout.py",
      "section": "total"
    },
    {
      "path": "tests/test_checkout.py",
      "section": "test_total"
    },
    {
      "path": "docs/checkout.md"
    }
  ],
  "watches": [
    "src/checkout*.py",
    "tests/test_checkout*.py",
    "docs/checkout*.md"
  ],
  "verification": [],
  "implements": [],
  "behaviors": [
    "PB-012"
  ],
  "depends_on": [
    "CMP-checkout"
  ],
  "id": "CAP-checkout",
  "kind": "product",
  "title": "Checkout fee"
}
---

# Checkout fee

## Purpose
The checkout documentation states that the fixed fee covers packing costs. This is documented intent; the implementation and test corroborate the fee amount.

<a id="pb-012"></a>
## PB-012 — Add the packing fee
Observed and intended behavior agree: checkout adds 3 to the supplied subtotal. For example, subtotal 10 produces 13. No currency is specified by the supplied evidence. [Implementation and verification](../engineering/checkout.md).

## Ownership and handoffs
Checkout owns this fee calculation. It does not determine inventory availability, per docs/checkout.md. The inspected function accepts a subtotal and returns a total to its caller. No caller or inventory integration is established by this bounded fixture; this baseline makes no claim about payment collection or inventory orchestration.
