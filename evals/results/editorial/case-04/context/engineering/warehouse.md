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
    "warehouse/*.py",
    "deploy/*subscriptions*.json",
    "src/checkout*.py",
    "tests/test*warehouse*.py",
    "tests/test*checkout*.py"
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
      "reference": "Consumer contract and subscription integration checks for order.paid id -> inventory.reserve"
    }
  ]
}
---

# Warehouse reservation consumer

`warehouse/worker.py::reserve` implements [PB-002](../product/paid-order.md#pb-002). `deploy/subscriptions.json` maps `order.paid` to this function, establishing the handoff without a Python import from checkout. Input is a message containing `id`; the side effect is a call to injected `inventory.reserve(message["id"])`. The inventory implementation is absent.

Warehouse owns initiating stock reservation; it does not collect payment. This function contains no delivery, retry, or duplicate handling. Runtime guarantees belong to unavailable bus/inventory implementations and cannot be inferred.

Verification gap: add a consumer contract check using a recording inventory double, a producer-payload-to-consumer check, and a subscription routing integration check. No existing test calls this consumer. These checks were not added or run. Any change to message keys, event name, subscription mapping, or order ID semantics requires producer and consumer verification together.
