---
{
  "schema_version": 1,
  "id": "CAP-paid-order",
  "kind": "product",
  "scope": "paid-order",
  "title": "paid-order",
  "revision": "no-git",
  "sources": [
    {
      "path": "src/checkout.py"
    },
    {
      "path": "warehouse/worker.py"
    },
    {
      "path": "deploy/subscriptions.json"
    },
    {
      "path": "docs/checkout.md"
    }
  ],
  "watches": [
    "src/*.py",
    "warehouse/*.py",
    "deploy/*.json",
    "docs/*.md"
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
# Paid-order capability
<a id="pb-001"></a>
## PB-001 — Checkout acceptance
Observed: checkout publishes order.paid with id from order.id, then returns status accepted when publish returns. Intended: docs/checkout.md describes accepting payment results. The function does not prove payment succeeded. [Checkout component](../engineering/checkout.md).
<a id="pb-002"></a>
## PB-002 — Reservation handoff
Observed: deploy/subscriptions.json maps order.paid to warehouse/worker.py:reserve, which delegates inventory.reserve(message["id"]). This proves configured connectivity, not runtime delivery or successful reservation. [Warehouse component](../engineering/warehouse.md).
## Ownership and rationale
Intended: warehouse owns stock reservation and does not collect payment. Checkout does not reserve stock or guarantee fulfillment. The documented rationale is decoupling payment from slow warehouse operations. Implementations agree with these local boundaries. Bus and inventory internals are outside supplied evidence.
