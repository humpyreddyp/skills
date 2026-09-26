---
{
  "schema_version": 1,
  "id": "CAP-fee",
  "kind": "product",
  "scope": "checkout",
  "title": "Checkout fee",
  "revision": "no-git",
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
      "external": "answer-Q-001"
    },
    {
      "path": "docs/checkout.md",
      "section": "Checkout"
    }
  ],
  "watches": [
    "src/checkout*.py",
    "tests/test_checkout*.py",
    "docs/checkout*.md"
  ],
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

The documented purpose of the fee is to cover packing costs. The product-owner answer agrees with docs/checkout.md.

<a id="pb-001"></a>
## PB-001 — Add the fixed checkout fee

Observed: `total(subtotal)` returns the subtotal plus 3. For subtotal 10, the result is 13. The documented fee and human-confirmed intent agree with the implementation.

The capability calculates the charged total from a caller-supplied subtotal. It does not determine inventory availability (docs/checkout.md). The inspected total function takes a numeric input and returns a numeric result; no stock, persistence, or payment handoff is present in this implementation.

See [implementation and verification](../engineering/checkout.md).
