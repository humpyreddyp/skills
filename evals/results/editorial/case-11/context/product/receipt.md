---
{
  "schema_version": 1,
  "id": "CAP-receipt",
  "kind": "product",
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
  "behaviors": [
    "PB-002"
  ],
  "implements": [],
  "depends_on": [],
  "verification": []
}
---

# Purchase receipt

Intended purpose: let customers reference their purchase (docs/receipt.md).

<a id="pb-002"></a>
## PB-002 — Expose order identity

Observed and intended: receipt(order) returns order_id equal to order.id. [Implementation and checks](../engineering/receipt.md).

The function constructs the receipt record; the caller supplies order identity. It does not calculate the checkout fee. Delivery to the customer and caller workflow are not established here. Fee policy remains outside trusted context pending Q-001.
