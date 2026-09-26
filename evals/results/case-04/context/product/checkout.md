---
{
  "schema_version": 1,
  "id": "CAP-checkout",
  "kind": "product",
  "scope": "checkout",
  "title": "Paid-order flow",
  "revision": "no-git",
  "sources": [
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
    "tests/test_checkout*.py",
    "docs/checkout*.md",
    "docs/adr*.md",
    "warehouse/*.py",
    "deploy/*.json",
    ".github/workflows/*.yml"
  ],
  "behaviors": [
    "PB-001",
    "PB-002"
  ],
  "implements": [],
  "depends_on": [
    "CMP-checkout"
  ],
  "verification": []
}
---

# Paid-order flow

<a id="pb-001"></a>
## PB-001 — Checkout publishes the paid-order handoff

Documented intent is to accept payment results and decouple them from slow warehouse work. Observed checkout(order, bus) publishes order.paid with the order id, then returns status accepted. It does not inspect payment state; payment validation is outside the supplied function.

<a id="pb-002"></a>
## PB-002 — Warehouse handles stock reservation

Deployment configuration maps order.paid to warehouse/worker.py:reserve. The handler passes message[id] to inventory.reserve. This proves configured wiring and handler behavior, not successful live delivery.

Checkout does not reserve stock or guarantee fulfillment; warehouse does not collect payment, as stated in docs/checkout.md and consistent with these functions. [Components and verification](../engineering/checkout.md).
