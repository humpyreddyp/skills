---
{
  "schema_version": 1,
  "id": "CAP-checkout",
  "kind": "product",
  "scope": "checkout",
  "title": "Checkout fee",
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
    "src/checkout*.py",
    "tests/test_checkout*.py",
    "docs/checkout*.md",
    "docs/adr*.md"
  ],
  "behaviors": [
    "PB-012"
  ],
  "implements": [],
  "depends_on": [
    "CMP-checkout"
  ],
  "verification": []
}
---

# Checkout fee

<a id="pb-012"></a>
## PB-012 — Checkout adds a fixed fee of 3

Observed total(subtotal) returns subtotal plus FEE = 3. docs/checkout.md states the intended fixed fee of 3 covers packing costs. It also states checkout does not determine inventory availability; the supplied calculation function has no inventory calls.

[Implementation and verification](../engineering/checkout.md). Currency and rounding behavior are not specified by these sources.
