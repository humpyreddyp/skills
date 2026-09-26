---
{
  "schema_version": 1,
  "id": "CMP-checkout",
  "kind": "engineering",
  "scope": "paid-order",
  "title": "checkout",
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
    "src/*.py",
    "warehouse/*.py",
    "deploy/*.json",
    "docs/*.md",
    "tests/*.py",
    ".github/workflows/*.yml"
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
      "kind": "existing",
      "reference": "tests/test_checkout.py::test_event_name (constant-only; no implementation coverage)"
    },
    {
      "behavior": "PB-001",
      "kind": "gap",
      "reference": "Checkout topic/payload/response and subscription-to-handler contract checks"
    }
  ]
}
---
# Checkout component
Implements [PB-001](../product/paid-order.md#pb-001). Entry checkout(order,bus) emits order.paid with {id: order.id}, then returns {status: accepted}. It does not perform payment validation or stock reservation. The documented component boundary excludes fulfillment guarantees.
Dependency edge: deploy/subscriptions.json binds this topic to [warehouse](warehouse.md), whose message["id"] matches the emitted payload. Bus implementation, durability, retries, deployment state, and caller payment checks are not supplied.
Verification: CI .github/workflows/check.yml declares python -m pytest. tests/test_checkout.py::test_event_name compares constant strings and exercises no implementation or configuration; no flow assurance follows. No checks were run. Propose invoking checkout with a fake bus to assert event name, ID payload and response, plus a subscription-to-handler contract check.
