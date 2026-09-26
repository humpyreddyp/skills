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
  "behaviors": [],
  "implements": [
    "PB-002"
  ],
  "verification": [
    {
      "behavior": "PB-002",
      "kind": "gap",
      "reference": "Unit-check reserve forwards message id; integration/contract-check order.paid subscription and producer-to-consumer handoff"
    }
  ],
  "depends_on": [
    "CAP-paid-order"
  ],
  "id": "CMP-warehouse",
  "kind": "engineering",
  "title": "Warehouse reservation consumer"
}
---

# Warehouse reservation consumer

## Responsibilities
warehouse/worker.py::reserve implements [PB-002](../product/paid-order.md#pb-002). Warehouse owns stock reservation, delegating it to supplied inventory.reserve. It does not collect payment, according to docs/checkout.md. It does not establish payment validity or guarantee fulfillment in the supplied implementation.

## Implementation and dependencies
The handler reads message["id"] and calls inventory.reserve with that value. deploy/subscriptions.json routes order.paid to this handler; src/checkout.py::checkout supplies that event and key. See [producer](checkout.md). An event name or payload change therefore crosses both components and deployment wiring. The inventory adapter and running bus are not provided, so actual reservation completion, persistence, duplicate handling, and delivery semantics remain outside this baseline.

## Verification
There is no warehouse test in the complete seven-file inventory. tests/test_checkout.py::test_event_name provides no consumer or handoff coverage. CI's pytest command could not run locally because pytest is unavailable; no runtime result is claimed.

Needed checks: unit-check that reserve forwards the exact order ID to a fake inventory; contract-check producer payload and subscription target; integration-check delivery through the configured bus to inventory when that infrastructure is available. Changes to the message shape should also verify checkout, not just this handler. Retry/idempotency and failure handling require additional specification and checks if they become part of a future change.
