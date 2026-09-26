---
{
  "schema_version": 1,
  "id": "CMP-checkout",
  "kind": "engineering",
  "scope": "checkout",
  "title": "Paid-order components and handoff",
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
  "behaviors": [],
  "implements": [
    "PB-001",
    "PB-002"
  ],
  "depends_on": [
    "CAP-checkout"
  ],
  "verification": [
    {
      "behavior": "PB-001",
      "kind": "gap",
      "reference": "Producer behavior check needed: topic, id payload, accepted status; current test_event_name is tautological."
    },
    {
      "behavior": "PB-002",
      "kind": "gap",
      "reference": "Producer-config-consumer contract and runtime delivery/failure checks needed; no handler integration coverage found."
    }
  ]
}
---

# Paid-order components and handoff

[PB-001](../product/checkout.md#pb-001) is implemented by src/checkout.py::checkout: injected bus publishes topic order.paid with {id: order.id}, then returns accepted.

[PB-002](../product/checkout.md#pb-002) crosses a deployment edge: deploy/subscriptions.json maps that exact topic to warehouse/worker.py:reserve, whose handler calls injected inventory.reserve(message["id"]). No direct import is required for this event connection. Bus and inventory implementations are not supplied; delivery, retry, duplicate handling, failure handling and deployment activation are unverified. Do not infer guaranteed fulfillment.

## Verification

CI .github/workflows/check.yml declares python -m pytest. Discovered, not executed. Existing tests/test_checkout.py::test_event_name compares identical string literals and does not exercise producer, configuration or handler; it provides no meaningful handoff regression coverage.

Recommended gap checks: call checkout with a fake bus and verify topic/payload/status; validate deployment topic-to-handler mapping and invoke consumer with producer payload; assert inventory receives the correct id; test runtime delivery and failures/retries against actual bus/inventory contracts once available. These are expectations; no infrastructure was added.
