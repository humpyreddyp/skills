---
{
  "schema_version": 1,
  "id": "CAP-checkout",
  "kind": "product",
  "scope": "checkout",
  "title": "Current checkout fee",
  "revision": "working-tree",
  "sources": [
    {
      "path": "docs/adr-004.md"
    },
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
    "docs/adr-*.md",
    "src/checkout.py",
    "tests/test_checkout*.py"
  ],
  "behaviors": [
    "PB-001"
  ],
  "implements": [],
  "depends_on": [],
  "verification": []
}
---

# Current checkout fee

## Purpose
The accepted v2 decision states that the fee covers packing costs. The checkout document explicitly describes the retired v1 endpoint; its fee of 2 is historical and does not contradict the current v2 decision.

<a id="pb-001"></a>
## PB-001 — Add the current fee
Intended and observed: checkout adds a fixed fee of 3 to the supplied subtotal. The observed example is subtotal 10 returning total 13. Currency, payment collection, and endpoint routing are not established by this fixture.

## Ownership and handoffs
The checkout function owns total calculation from its supplied subtotal. It returns that total to its caller; this scope establishes no caller, payment system, or packing implementation. The packing purpose does not establish those integrations.

[Implementation and checks](../engineering/checkout.md)

