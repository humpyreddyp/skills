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

<a id="pb-001"></a>
## PB-001 — Add fixed fee

Observed: checkout returns the caller-supplied subtotal plus 3. Subtotal 10 produces total 13. Currency and numeric unit are not established by these sources.

Intended: documentation states the fee covers packing costs. It also says checkout does not determine inventory availability; the inspected total function performs fee arithmetic only.

[Implementation and verification](../engineering/checkout.md).
