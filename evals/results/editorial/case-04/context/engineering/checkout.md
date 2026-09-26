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
      "path": "src/checkout.py"
    },
    {
      "path": "deploy/subscriptions.json"
    },
    {
      "path": "docs/checkout.md"
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
    "tests/test*checkout*.py",
    "tests/test*warehouse*.py",
    ".github/workflows/*.yml"
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
      "kind": "gap",
      "reference": "Actual checkout event/payload/status unit test plus consumer contract and subscription integration test"
    }
  ]
}
---

# Checkout event producer

`src/checkout.py::checkout` implements [PB-001](../product/paid-order.md#pb-001). It calls injected `bus.publish("order.paid", {"id": order.id})` before returning `{"status": "accepted"}`. It neither validates payment nor reserves stock. The documented entry contract is an accepted payment result; the calling payment system is absent.

`deploy/subscriptions.json` routes the event to [warehouse](warehouse.md), which consumes the `id`. This config mapping is the dependency evidence; no direct import is required. Bus delivery and runtime deployment are not verified by the repository.

Existing `tests/test_checkout.py::test_event_name` compares the literal `order.paid` with itself. It passed when directly executed using Python 3 -B/runpy at no-git, but provides no evidence about production behavior. CI declares `python -m pytest`; a full CI or pytest run was not performed.

Verification gaps: a producer test must assert the actual publish call, payload, and returned status with a fake bus and order. A contract/integration test must connect that payload through subscription routing to inventory reservation. Producer changes need these downstream checks even if warehouse files are unchanged. No tests or missing infrastructure were added.
