---
{
  "schema_version": 1,
  "id": "CMP-warehouse",
  "kind": "engineering",
  "scope": "paid-order",
  "title": "Warehouse",
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
    },
    {
      "path": "tests/test_checkout.py"
    },
    {
      "path": ".github/workflows/check.yml"
    }
  ],
  "watches": [
    "src/checkout.py",
    "warehouse/worker.py",
    "deploy/subscriptions.json",
    "tests/test_checkout.py"
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
      "reference": "Test id forwarding to inventory.reserve and producer-subscription-consumer contract with fake inventory."
    }
  ]
}
---

# Warehouse reservation

warehouse/worker.py::reserve implements [PB-002](../product/paid-order.md#pb-002) by calling inventory.reserve(message["id"]). deploy/subscriptions.json routes order.paid to this handler; [checkout](checkout.md) produces the required id field.

Warehouse owns the reservation request and does not collect payment. Inventory is injected; its storage, allocation success, and fulfillment semantics are not established. Transport retry, deduplication and delivery guarantees are also unavailable and need investigation before changing those guarantees.

No test invokes reserve. The existing literal equality test does not verify the handoff. Gaps: handler unit test asserting id forwarding and an integration/contract check sending checkout's emitted payload through configured routing to fake inventory. Review producer, subscription and consumer together for id or route changes. CI specifies python -m pytest; no tests were executed.
