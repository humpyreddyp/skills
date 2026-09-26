---
{
  "schema_version": 1,
  "id": "CMP-warehouse",
  "kind": "engineering",
  "scope": "paid-order",
  "title": "Warehouse reservation consumer",
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
    "src/*checkout*.py",
    "warehouse/*.py",
    "deploy/*subscriptions*.json",
    "tests/test*checkout*.py",
    "tests/test*warehouse*.py",
    "tests/test*order*.py",
    ".github/workflows/*.yml",
    "docs/*checkout*.md"
  ],
  "behaviors": [],
  "implements": [
    "PB-002"
  ],
  "depends_on": [
    "CAP-paid-order"
  ],
  "verification": [
    {
      "behavior": "PB-002",
      "kind": "gap",
      "reference": "Contract check routing order.paid payload id through warehouse.reserve to a fake inventory reserve call; reservation failure/idempotency expectations require the external inventory contract."
    }
  ]
}
---

# Warehouse reservation consumer

`warehouse/worker.py::reserve(message, inventory)` implements [PB-002](../product/paid-order.md#pb-002). It owns extracting `message["id"]` and forwarding it to `inventory.reserve`. Warehouse does not collect payment; inventory implementation is a supplied dependency outside the available code.

The incoming connection is established by `deploy/subscriptions.json`: event `order.paid` selects `warehouse/worker.py:reserve`. Checkout produces the required `id` field in `src/checkout.py`; imports are not the connection. Changes to event name or payload require review of producer, deployment mapping, and consumer together.

## Verification
No discovered check exercises the consumer or configured mapping. A contract/integration check should connect checkout's published event and payload through the mapping to the worker and assert the same id reaches inventory.reserve. Add isolated handler checks for the agreed payload contract. Delivery, retries, idempotency, and successful allocation cannot be verified without bus/inventory implementations and contracts; do not infer those guarantees.

