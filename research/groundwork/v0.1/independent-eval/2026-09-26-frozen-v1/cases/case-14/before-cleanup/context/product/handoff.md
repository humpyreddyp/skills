---
{
  "schema_version": 1,
  "scope": "checkout-warehouse",
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
    "warehouse/*.py",
    "deploy/*subscriptions*.json",
    "docs/checkout*.md",
    "tests/test_checkout*.py",
    "tests/test_warehouse*.py",
    "tests/test_*order*.py",
    ".github/workflows/*.yml"
  ],
  "behaviors": [
    "PB-001",
    "PB-002"
  ],
  "implements": [],
  "depends_on": [
    "CMP-checkout",
    "CMP-warehouse"
  ],
  "verification": [],
  "id": "CAP-order-handoff",
  "kind": "product",
  "title": "Checkout and warehouse responsibility boundary"
}
---

# Checkout and warehouse responsibility boundary

## Purpose
The documented handoff decouples payment from slow warehouse operations (docs/checkout.md). Checkout accepts payment results and emits an order.paid event; warehouse owns stock reservation. This states intended ownership. The observed functions corroborate event emission and reservation delegation, but do not themselves demonstrate payment collection or a deployed delivery guarantee.

<a id="pb-001"></a>
## PB-001 — Checkout accepts and emits the handoff
When invoked with an order and bus, checkout publishes order.paid carrying {"id": order.id}, then returns {"status": "accepted"}. Checkout owns creating this event. It does not reserve stock or guarantee fulfillment. An accepted return is not proof of warehouse completion. [Implementation and checks](../engineering/checkout.md).

<a id="pb-002"></a>
## PB-002 — Warehouse owns reservation
Configuration routes order.paid to warehouse/worker.py:reserve. The handler reads message["id"] and delegates to inventory.reserve. Warehouse owns this reservation step and does not collect payment. [Implementation and checks](../engineering/warehouse.md).

## Handoff and limits
The responsibility passes from checkout's bus publication to the configured warehouse handler carrying the order ID. The subscription mapping is direct evidence of that connection; matching names alone are not the basis. The runtime bus, payment-result caller, and inventory implementation are unavailable. Retry, delivery, duplicate-message handling, and actual fulfillment guarantees are not established. Those are coverage limits rather than invented responsibilities for either component.
