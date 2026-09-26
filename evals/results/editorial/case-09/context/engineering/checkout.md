---
{
  "schema_version": 1,
  "id": "CMP-checkout",
  "kind": "engineering",
  "scope": "checkout",
  "title": "Checkout",
  "revision": "no-git",
  "sources": [
    {
      "path": "src/checkout.py"
    },
    {
      "path": "tests/test_checkout.py"
    },
    {
      "path": "docs/checkout.md"
    }
  ],
  "watches": [
    "src/checkout.py",
    "tests/test_checkout.py"
  ],
  "behaviors": [],
  "implements": [
    "PB-012"
  ],
  "depends_on": [
    "CAP-checkout"
  ],
  "verification": [
    {
      "behavior": "PB-012",
      "kind": "existing",
      "reference": "tests/test_checkout.py::test_total"
    }
  ]
}
---

# Checkout calculation

src/checkout.py::total implements [PB-012](../product/checkout.md#pb-012) as subtotal + FEE, where FEE = 3. The caller supplies subtotal and receives the numeric result. This function owns neither inventory availability nor reservation; no service, event, storage, or configuration dependency is present in the inspected function.

Existing check: tests/test_checkout.py::test_total expects total(10) == 13. It was inspected, not executed; no passing result is claimed. A fee change should run this targeted unit test and review docs/checkout.md and its packing-cost rationale. pyproject.toml defines project identity without a test command.

Scope is the supplied checkout implementation; unrelated material was not investigated.
