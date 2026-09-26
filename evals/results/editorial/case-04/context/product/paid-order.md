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
      "path": "deploy/subscriptions.json"
    },
    {
      "path": "warehouse/worker.py"
    }
  ],
  "watches": [
    "src/checkout*.py",
    "warehouse/*.py",
    "deploy/*subscriptions*.json",
    "docs/*checkout*",
    "tests/test*checkout*.py"
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

Intended purpose: separate payment results from slow warehouse operations (docs/checkout.md). The document assigns payment-result acceptance and event production to checkout, and stock reservation to warehouse.

<a id="pb-001"></a>
## PB-001 — Announce an accepted order

Observed: checkout publishes `order.paid` with an `id` taken from `order.id`, then returns status `accepted`. Its code does not itself validate payment; accepting payment results is the documented caller contract. [Checkout implementation](../engineering/checkout.md).

<a id="pb-002"></a>
## PB-002 — Hand the order ID to stock reservation

Observed configuration maps `order.paid` to `warehouse/worker.py:reserve`. The consumer passes `message["id"]` to `inventory.reserve`. This establishes the configured producer-to-consumer contract, not proof of runtime delivery or successful inventory reservation. [Warehouse implementation](../engineering/warehouse.md).

Checkout does not reserve stock or guarantee fulfillment. Warehouse does not collect payment. Responsibility passes through the event payload and subscription mapping; the injected bus and inventory implementations are unavailable. Delivery reliability, retries, duplicates, and completed fulfillment are outside the supported claims.
