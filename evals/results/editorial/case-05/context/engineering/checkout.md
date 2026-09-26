---
{
  "schema_version": 1,
  "id": "CMP-checkout",
  "kind": "engineering",
  "scope": "checkout",
  "title": "Checkout total calculation",
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
    },
    {
      "behavior": "PB-001",
      "kind": "gap",
      "reference": "No caller/integration contract is supplied; review input numeric types and total consumers before broadening this calculation."
    }
  ]
}
---

# Checkout total calculation

`src/checkout.py::total` implements [PB-001](../product/fee.md#pb-001) by adding module constant `FEE = 3` to its argument. It owns arithmetic only; no imports, I/O, configuration, storage, inventory operation, or payment call occurs. The caller supplies the subtotal and receives the resulting number. Caller contracts and downstream consumers are outside the supplied evidence.

`tests/test_checkout.py::test_total` checks that total(10) equals 13. After inspecting the test for side effects, it was executed directly with `python3 -B -c "import runpy; runpy.run_path('tests/test_checkout.py')['test_total']()"`: passed at revision `no-git`. This executes the single test; no test runner configuration is supplied. A fee change should update and rerun this check and investigate caller/integration contracts. No such contracts or broader boundary-value checks are present in the inspected fixture; this baseline does not create them.
