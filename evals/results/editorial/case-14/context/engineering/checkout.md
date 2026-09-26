---
{
  "schema_version": 1,
  "id": "CMP-checkout",
  "kind": "engineering",
  "scope": "paid-order",
  "title": "Checkout",
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
    "PB-001"
  ],
  "depends_on": [
    "CAP-paid-order"
  ],
  "verification": [
    {
      "behavior": "PB-001",
      "kind": "gap",
      "reference": "Producer event/payload/response unit test and producer-subscription-consumer contract check; existing literal equality assertion provides no behavioral coverage."
    }
  ]
}
---

# Checkout producer

src/checkout.py::checkout implements [PB-001](../product/paid-order.md#pb-001). It passes order.id as id in bus.publish("order.paid", payload), then returns status accepted. It owns event production, not stock reservation or guaranteed fulfillment. Payment processing itself is not implemented in this function.

The injected bus and order are inputs. deploy/subscriptions.json establishes the downstream [warehouse handler](warehouse.md) relationship. Changes to event name, id shape or routing therefore require consumer verification even when warehouse source is unchanged. Transport implementation and runtime guarantees are unavailable.

Existing tests/test_checkout.py::test_event_name compares identical string literals; it exercises neither producer nor consumer. CI specifies python -m pytest. No tests were run. Gaps: unit-test actual published name/payload and acceptance response; contract-test producer payload through subscription routing into reserve. Bootstrap records gaps without building infrastructure.
