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
    "PB-001"
  ],
  "verification": [
    {
      "behavior": "PB-001",
      "kind": "existing",
      "reference": "tests/test_checkout.py::test_event_name (tautological; no implementation coverage)"
    },
    {
      "behavior": "PB-001",
      "kind": "gap",
      "reference": "Unit-check checkout publishes order.paid with order.id and returns accepted; contract-check payload against subscription and reserve consumer"
    }
  ],
  "depends_on": [
    "CAP-paid-order"
  ],
  "id": "CMP-checkout",
  "kind": "engineering",
  "title": "Checkout event producer"
}
---

# Checkout event producer

## Responsibilities
src/checkout.py::checkout implements [PB-001](../product/paid-order.md#pb-001). It emits an event and returns acceptance. Per docs/checkout.md it does not reserve stock or guarantee fulfillment. It does not itself validate or collect payment; the documented payment-result precondition belongs to a caller absent from this fixture.

## Implementation and dependencies
Input: order with an id attribute and a supplied bus. Output: bus.publish("order.paid", {"id": order.id}), then an accepted status. deploy/subscriptions.json maps that exact event to warehouse/worker.py:reserve, which consumes the id key; see [warehouse](warehouse.md). This config is the evidence for the connection despite no import. The bus and inventory adapters are injected and their implementation is unavailable. Exceptions before the return are not caught here; no end-to-end delivery guarantee is established.

## Verification
Existing tests/test_checkout.py::test_event_name asserts one constant string equals itself. It neither invokes checkout nor verifies the event, payload, routing, or return value. CI declares python -m pytest in .github/workflows/check.yml. A local working-tree attempt, python3 -m pytest -p no:cacheprovider, failed before collection: No module named pytest. No tests passed and no dependency was installed. The enclosing repository SHA is not a dedicated fixture revision.

Needed checks: call checkout with a stub bus and order to assert the exact event, id payload, and accepted return; contract-check the emitted event against deploy/subscriptions.json and warehouse.reserve; check behavior when publish fails if future changes need an error guarantee. A producer schema/event-name change must include the consumer and subscription, even if their files would otherwise stay unchanged.
