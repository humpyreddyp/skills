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

The fee purpose is not established by available evidence; Q-002 tracks this coverage gap.

<a id="pb-001"></a>
## PB-001 — Add the fixed checkout fee

Observed: `total(subtotal)` returns the subtotal plus 3. For subtotal 10, the result is 13. The product-owner confirms current fee 3. X-001 excludes only the outdated fee-2 claim in docs/checkout.md; it does not exclude the whole document.

The inspected function owns fee addition to a caller-supplied subtotal and returns the result to its caller. It contains no inventory, persistence, or payment operation. No caller or downstream system is supplied, so this baseline covers the calculation only.

See [implementation and verification](../engineering/checkout.md).
