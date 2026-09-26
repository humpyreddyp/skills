---
{
  "schema_version": 1,
  "id": "CAP-paid-order",
  "kind": "product",
  "scope": "paid-order",
  "title": "Paid-order handoff",
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

## Purpose and boundaries
Intended, per docs/checkout.md: checkout accepts payment results and the event handoff decouples payment from slow warehouse operations. Checkout does not reserve stock or guarantee fulfillment; warehouse owns reservation and does not collect payment. The code establishes the configured handoff below, not payment validation, successful fulfillment, or runtime delivery guarantees.

<a id="pb-001"></a>
## PB-001 — Publish an order identifier
Observed: checkout calls its supplied bus with event `order.paid` and payload `{"id": order.id}`, then returns `{"status": "accepted"}` if publishing returns. Its input is an order; the implementation does not establish that payment has been validated.

<a id="pb-002"></a>
## PB-002 — Hand the identifier to inventory reservation
Configured and observed in the consumer: `deploy/subscriptions.json` routes `order.paid` to `warehouse/worker.py:reserve`. That handler passes `message["id"]` to its supplied inventory object's `reserve` method. This establishes the reservation request, not that inventory allocation succeeds.

## Ownership and handoffs
Checkout owns event production; deployment configuration owns the event-to-handler mapping; the warehouse handler owns translating the incoming identifier to the inventory call. The supplied bus and inventory services form the remaining runtime boundary. Their internals and operational delivery/retry guarantees are unavailable in this fixture.

[Checkout implementation](../engineering/checkout.md) · [Warehouse implementation](../engineering/warehouse.md)

