---
{
  "schema_version": 1,
  "id": "CAP-checkout-receipt",
  "kind": "product",
  "scope": "checkout",
  "title": "Receipt order reference",
  "revision": "working-tree",
  "sources": [
    {
      "path": "docs/receipt.md"
    },
    {
      "path": "src/receipt.py"
    }
  ],
  "watches": [
    "docs/*receipt*.md",
    "src/*receipt*.py",
    "tests/test*receipt*.py"
  ],
  "behaviors": [
    "PB-002"
  ],
  "implements": [],
  "depends_on": [],
  "verification": []
}
---

# Receipt order reference

## Purpose
Intended: expose the order ID so a customer can reference their purchase, as stated in docs/receipt.md.

<a id="pb-002"></a>
## PB-002 — Expose the supplied order identifier
Intended and observed: `receipt(order)` returns `{"order_id": order.id}`. The function reads the supplied identifier; it does not generate or persist one, calculate a fee, or establish that a purchase was paid.

## Ownership and handoffs
Receipt owns shaping an order reference for its caller. The caller supplies an order with an id and receives the returned object. Receipt delivery to a customer is intended by the purpose document, but a delivery component is not established in this fixture. This behavior is independent of the disputed checkout fee, tracked separately in [Q-001](../../.bootstrap/questions.yaml).

[Implementation and verification gap](../engineering/receipt.md)

