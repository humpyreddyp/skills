---
{
  "schema_version": 1,
  "scope": "paid-order",
  "revision": "working-tree",
  "sources": [
    {
      "path": "docs/checkout.md"
    },
    {
      "path": "src/checkout.py"
    },
    {
      "path": "deploy/subscriptions.json"
    },
    {
      "path": "warehouse/worker.py"
    },
    {
      "path": "tests/test_checkout.py"
    },
    {
      "path": ".github/workflows/check.yml"
    }
  ],
  "watches": [
    "src/checkout*.py",
    "deploy/*subscriptions*.json",
    "warehouse/*.py",
    "tests/test_checkout*.py",
    "tests/test_warehouse*.py",
    "tests/test_*order*.py",
    "docs/checkout*.md",
    ".github/workflows/*.yml"
  ],
  "behaviors": [
    "PB-001",
    "PB-002"
  ],
  "implements": [],
  "verification": [],
  "depends_on": [
    "CMP-checkout",
    "CMP-warehouse"
  ],
  "id": "CAP-paid-order",
  "kind": "product",
  "title": "Paid-order handoff"
}
---

# Paid-order handoff

## Purpose
Documented intent: separate payment results from slow warehouse operations. Checkout accepts payment results; warehouse owns stock reservation. Source: docs/checkout.md. The implementation demonstrates event publication and reservation delegation, not payment processing or successful fulfillment.

<a id="pb-001"></a>
## PB-001 — Publish an accepted order handoff
Observed: when checkout(order, bus) is called, it publishes order.paid with a payload containing id=order.id, then returns status=accepted. The function contains no payment validation or receipt of a warehouse result. The caller is responsible for the precondition described in the documentation; the fixture does not establish that caller. [Checkout implementation and checks](../engineering/checkout.md).

<a id="pb-002"></a>
## PB-002 — Delegate stock reservation
Observed configuration: deploy/subscriptions.json maps order.paid to warehouse/worker.py:reserve. That handler passes message["id"] to inventory.reserve. This establishes the intended routing and consumer contract; no running broker or real inventory outcome was verified. [Warehouse implementation and checks](../engineering/warehouse.md).

## Ownership and handoffs
Checkout owns emitting the paid-order event, not stock reservation or guaranteed fulfillment. It hands the order ID to the configured warehouse consumer through the bus. Warehouse owns reservation delegation, not collecting payment. Inventory implementation and bus delivery semantics are outside the supplied evidence. No guarantee about retries, duplicate delivery, atomicity, or eventual reservation is established by this baseline.
