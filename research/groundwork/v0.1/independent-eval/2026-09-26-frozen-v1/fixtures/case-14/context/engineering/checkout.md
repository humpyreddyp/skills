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
    "PB-001"
  ],
  "depends_on": [
    "CAP-order-handoff"
  ],
  "verification": [
    {
      "behavior": "PB-001",
      "kind": "existing",
      "reference": "tests/test_checkout.py::test_event_name; constant equality only"
    },
    {
      "behavior": "PB-001",
      "kind": "gap",
      "reference": "Exercise checkout with a fake bus to verify event, id, and return; contract-check subscription and warehouse handler"
    }
  ],
  "id": "CMP-checkout",
  "kind": "engineering",
  "title": "Checkout responsibilities"
}
---

# Checkout responsibilities

## Owns
src/checkout.py::checkout implements [PB-001](../product/handoff.md#pb-001): it reads order.id, calls the supplied bus.publish with order.paid and an id payload, then returns accepted. Documentation supplies the reason for this boundary: isolate payment from slow warehouse work.

## Does not own
Per docs/checkout.md, checkout neither reserves stock nor guarantees fulfillment. The function contains no inventory call, warehouse completion wait, or payment-validation logic. The payment-result caller and bus adapter are not present, so this baseline does not assert how they establish payment validity or event delivery.

## Handoff
Input is the order and bus; output is an event plus the accepted return. deploy/subscriptions.json routes that event to [warehouse.reserve](warehouse.md). The shared contract is event name order.paid and payload key id. Renaming either requires checking producer, deployment mapping, and consumer together. Checkout returning accepted does not establish that reserve has run.

## Verification
Existing tests/test_checkout.py::test_event_name checks only literal equality and never calls checkout. It is not implementation or handoff coverage. CI declares python -m pytest; tests were inspected, not executed for this fixture. Revision is the supplied working tree; the enclosing repository SHA does not identify a dedicated fixture commit.

Missing checks: unit-check exact publication and accepted return using a fake bus; contract-check event and payload against subscription/consumer; integration-check actual delivery where bus and inventory infrastructure are available. A failure or retry requirement needs explicit policy evidence before claiming guarantees.
