---
{
  "schema_version": 1,
  "id": "CAP-paid-order",
  "kind": "product",
  "scope": "paid-order",
  "title": "Paid Order",
  "revision": "no-git",
  "sources": [
    {
      "path": "docs/checkout.md"
    },
    {
      "path": "src/checkout.py"
    },
    {
      "path": "warehouse/worker.py"
    },
    {
      "path": "deploy/subscriptions.json"
    }
  ],
  "watches": [
    "src/checkout.py",
    "warehouse/worker.py",
    "deploy/subscriptions.json"
  ],
  "behaviors": [
    "PB-001",
    "PB-002"
  ],
  "implements": [],
  "depends_on": [],
  "verification": []
}
---

# Paid-order handoff

Intended purpose: decouple payment results from slow warehouse operations (docs/checkout.md). Scope is the supplied producer, subscription and reservation handler.

<a id="pb-001"></a>
## PB-001 — Publish the paid-order handoff

Docs describe checkout accepting payment results. Observed checkout(order,bus) publishes order.paid with an id payload from order.id, then returns status accepted. It does not validate payment in the supplied function. [Checkout implementation](../engineering/checkout.md).

<a id="pb-002"></a>
## PB-002 — Request stock reservation

deploy/subscriptions.json maps order.paid to warehouse/worker.py:reserve, which passes message["id"] to inventory.reserve. This establishes configured routing and the reservation request, not live delivery or successful fulfillment. [Warehouse implementation](../engineering/warehouse.md).

Checkout owns event production and acceptance response. It does not reserve stock or guarantee fulfillment. Warehouse owns the reservation request and does not collect payment. Responsibility passes through order.paid and its id payload. Concrete bus delivery and inventory implementation are unavailable; do not infer retry, idempotency, ordering, or transaction guarantees.
