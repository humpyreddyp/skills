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
  "behaviors": [],
  "implements": [
    "PB-002"
  ],
  "depends_on": [
    "CAP-order-handoff"
  ],
  "verification": [
    {
      "behavior": "PB-002",
      "kind": "gap",
      "reference": "Check reserve passes message id to inventory; contract/integration-check configured order.paid handoff"
    }
  ],
  "id": "CMP-warehouse",
  "kind": "engineering",
  "title": "Warehouse responsibilities"
}
---

# Warehouse responsibilities

## Owns
warehouse/worker.py::reserve implements [PB-002](../product/handoff.md#pb-002). It reads message["id"] and passes the value to inventory.reserve. docs/checkout.md assigns stock reservation to warehouse; the injected inventory adapter owns details unavailable in this fixture.

## Does not own
The documentation explicitly states warehouse does not collect payment. This handler receives an already named paid-order event and does not process a payment result, charge a customer, or set checkout's accepted return. The supplied implementation also does not establish end-to-end fulfillment or durable reservation success; do not infer those guarantees from the method name.

## Handoff
Upstream [checkout](checkout.md) publishes order.paid with id; deploy/subscriptions.json selects warehouse/worker.py:reserve. This is the proven configuration connection. Warehouse's downstream call is inventory.reserve(message["id"]); the adapter implementation and transport runtime are outside the evidence. Changes to consumed payload keys must be coordinated with the producer and subscription contract.

## Verification
The complete seven-file source inventory contains no warehouse test. The checkout test only compares constants, and no tests were run for this fixture. Needed checks: fake-inventory unit check for forwarded id, producer/consumer payload contract check, and configured-bus integration check. Duplicate delivery, malformed messages, and failures would need agreed semantics and corresponding checks if future work changes those cases.
