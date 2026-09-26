---
{
  "schema_version": 1,
  "id": "CMP-warehouse",
  "kind": "engineering",
  "scope": "paid-order",
  "title": "warehouse",
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
    },
    {
      "path": "tests/test_checkout.py"
    },
    {
      "path": ".github/workflows/check.yml"
    }
  ],
  "watches": [
    "src/*.py",
    "warehouse/*.py",
    "deploy/*.json",
    "docs/*.md",
    "tests/*.py",
    ".github/workflows/*.yml"
  ],
  "behaviors": [],
  "implements": [
    "PB-002"
  ],
  "depends_on": [
    "CAP-paid-order",
    "CMP-checkout"
  ],
  "verification": [
    {
      "behavior": "PB-002",
      "kind": "gap",
      "reference": "Handler ID propagation and checkout/event/subscription/warehouse integration contract; bus/inventory behavior if available"
    }
  ]
}
---
# Warehouse component
Implements [PB-002](../product/paid-order.md#pb-002). deploy/subscriptions.json routes order.paid from [checkout](checkout.md) to warehouse/worker.py:reserve. Handler reserve(message,inventory) invokes inventory.reserve(message["id"]). It owns stock reservation, not payment collection, per docs/checkout.md; code corroborates that local boundary. Inventory implementation/storage and runtime bus delivery are unavailable. No guarantee of successful reservation or fulfillment is established.
Verification: CI declares python -m pytest. The sole supplied test compares constant event strings and tests no warehouse or integration behavior. No checks were executed. Gaps: invoke reserve with a fake inventory to verify ID propagation; route actual checkout event payload through subscription to handler. Delivery, retries and duplicates need bus/inventory contract evidence if brought into scope. These checks are proposed only.
