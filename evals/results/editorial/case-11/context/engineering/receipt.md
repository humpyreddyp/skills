---
{
  "schema_version": 1,
  "id": "CMP-receipt",
  "kind": "engineering",
  "scope": "checkout",
  "title": "Receipt",
  "revision": "no-git",
  "sources": [
    {
      "path": "src/receipt.py"
    },
    {
      "path": "docs/receipt.md"
    }
  ],
  "watches": [
    "src/receipt.py"
  ],
  "behaviors": [],
  "implements": [
    "PB-002"
  ],
  "depends_on": [
    "CAP-receipt"
  ],
  "verification": [
    {
      "behavior": "PB-002",
      "kind": "gap",
      "reference": "Unit check preserving order.id as order_id; caller order-shape contract when available."
    }
  ]
}
---

# Receipt record

src/receipt.py::receipt implements [PB-002](../product/receipt.md#pb-002) by returning a record with order_id from order.id. It depends on the caller supplying an order with an id attribute; it performs no fee calculation, storage or messaging.

No receipt test was found in this bounded repository. Gap: a unit check should prove order.id is preserved in order_id, and caller contract changes need verification. No tests were run. tests/test_checkout.py addresses only the disputed fee.
