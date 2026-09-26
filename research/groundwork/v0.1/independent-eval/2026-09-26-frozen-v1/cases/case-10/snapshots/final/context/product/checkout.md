---
{
  "schema_version": 1,
  "id": "CAP-checkout",
  "kind": "product",
  "scope": "checkout",
  "title": "Checkout fee",
  "revision": "working-tree",
  "sources": [
    {
      "path": "docs/checkout.md"
    },
    {
      "path": "src/checkout.py"
    },
    {
      "path": "tests/test_checkout.py"
    }
  ],
  "watches": [
    "docs/*checkout*.md",
    "src/*checkout*.py",
    "tests/test*checkout*.py"
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

## Purpose
Intended: docs/checkout.md specifies a fixed fee of 3 to cover packing costs. It explicitly excludes determining inventory availability from checkout's responsibility.

<a id="pb-001"></a>
## PB-001 — Add a fixed fee to the subtotal
Intended fee and observed calculation agree: the implementation adds 3 to the supplied subtotal, with the test example 10 producing 13. The document describes collection; this fixture's code establishes calculation only, not payment collection or a payment gateway.

## Ownership and coverage
Checkout calculates a total for its caller and does not determine inventory availability. No inventory or payment integration is established within the bounded checkout sources. Unrelated modules were deliberately not inspected; this baseline makes no claims about them.

[Implementation and checks](../engineering/checkout.md)

