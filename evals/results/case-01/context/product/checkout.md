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
    },
    {
      "path": "docs/adr-004.md"
    }
  ],
  "watches": [
    "src/checkout*.py",
    "tests/test_checkout*.py",
    "docs/checkout*.md",
    "docs/adr*.md"
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
## PB-001 — Checkout adds a fixed fee of 3

Observed total(subtotal) returns subtotal plus FEE = 3. Accepted ADR-004 states the current version is v2 and the fee covers packing costs. The fee of 2 in docs/checkout.md explicitly applies to retired v1; there is no current conflict.

[Implementation and verification](../engineering/checkout.md). Currency and rounding behavior are not specified by these sources.
