---
{
  "schema_version": 1,
  "id": "CMP-checkout",
  "kind": "engineering",
  "scope": "paid-order",
  "title": "Checkout paid-order producer",
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
    "PB-001"
  ],
  "depends_on": [
    "CAP-paid-order",
    "CMP-warehouse"
  ],
  "verification": [
    {
      "behavior": "PB-001",
      "kind": "existing",
      "reference": "tests/test_checkout.py::test_event_name (literal equality only)"
    },
    {
      "behavior": "PB-001",
      "kind": "gap",
      "reference": "Exercise checkout with a fake bus; assert event name, id payload and accepted return; validate subscription and warehouse consumer contract."
    }
  ]
}
---

# Checkout paid-order producer

`src/checkout.py::checkout(order, bus)` implements [PB-001](../product/paid-order.md#pb-001). It publishes `order.paid` with `id` then returns accepted. It owns event creation, not stock reservation, fulfillment, or payment validation. Both order and bus come from its caller; the caller and bus implementation are absent from the available fixture.

## Handoff and change impact
`deploy/subscriptions.json` names the [warehouse consumer](warehouse.md) for `order.paid`; `warehouse/worker.py::reserve` requires the payload id. Changing event names, payload fields, or timing requires coordinated mapping/consumer review despite no direct import. The documentation states that this split isolates slow warehouse operations.

## Verification
CI in `.github/workflows/check.yml` declares `python -m pytest`. No install or CI run was performed. The discovered `test_event_name` was executed directly through Python runpy in the working-tree fixture: PASS, but it compares the same string literal to itself and does not exercise checkout. It provides no evidence that event production or routing works.

Verification gaps: test checkout using a fake bus and assert its event, payload and return value; add a producer-to-subscription-to-consumer contract check; test failures only against an established bus/inventory contract. No new test infrastructure was created and no live bus or warehouse action was invoked.

