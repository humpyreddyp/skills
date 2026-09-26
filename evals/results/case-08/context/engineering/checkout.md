---
{
  "schema_version": 1,
  "id": "CMP-checkout",
  "kind": "engineering",
  "scope": "checkout",
  "title": "Checkout component",
  "revision": "no-git",
  "sources": [
    {
      "path": "src/checkout.py",
      "section": "FEE and total"
    },
    {
      "path": "tests/test_checkout.py",
      "section": "test_total"
    }
  ],
  "watches": [
    "src/checkout*.py",
    "tests/test_checkout*.py",
    "docs/checkout*.md"
  ],
  "behaviors": [],
  "implements": [
    "PB-001"
  ],
  "depends_on": [
    "CAP-fee"
  ],
  "verification": [
    {
      "behavior": "PB-001",
      "kind": "existing",
      "reference": "tests/test_checkout.py::test_total"
    }
  ]
}
---

# Checkout component

Implements [PB-001](../product/fee.md#pb-001) through `src/checkout.py::total` using `FEE`. The function accepts a subtotal and returns an arithmetic total. Its inspected body has no imports, service calls, or storage calls. The bounded four-file repository supplies no production caller or deployment wiring, so no runtime handoff is inferred.

Existing verification: `tests/test_checkout.py::test_total` asserts total(10) == 13. This test was inspected, not executed. No runner command is configured in pyproject.toml. Before a fee change, execute this check with the project-approved test runner. Currency and caller-integration verification would protect those contracts if they become available; no missing test infrastructure has been implemented.
