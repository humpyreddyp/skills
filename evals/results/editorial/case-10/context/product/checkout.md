---
{
  "schema_version": 1,
  "id": "CAP-checkout",
  "kind": "product",
  "scope": "checkout",
  "title": "Checkout",
  "revision": "no-git",
  "sources": [
    {
      "path": "src/checkout.py"
    },
    {
      "path": "tests/test_checkout.py"
    },
    {
      "path": "docs/checkout.md"
    }
  ],
  "watches": [
    "src/checkout.py",
    "tests/test_checkout.py"
  ],
  "behaviors": [
    "PB-001"
  ],
  "implements": [],
  "depends_on": [],
  "verification": []
}
---

# Checkout fee

Documented purpose: cover packing costs (docs/checkout.md).

<a id="pb-001"></a>
## PB-001 — Fixed checkout fee

Observed and intended: total(subtotal) adds a fixed fee of 3. The test expects subtotal 10 to produce 13. The evidence does not specify currency or additional validation policy.

Checkout owns this total calculation. It does not determine inventory availability, as explicitly documented. No downstream handoff is established by the bounded fee implementation. [Implementation and checks](../engineering/checkout.md).
