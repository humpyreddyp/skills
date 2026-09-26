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
      "path": "docs/adr-004.md"
    },
    {
      "path": "docs/checkout.md"
    }
  ],
  "watches": [
    "src/checkout*.py",
    "tests/test_checkout*.py",
    "pyproject.toml"
  ],
  "behaviors": [],
  "implements": [
    "PB-001"
  ],
  "depends_on": [
    "CAP-checkout"
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

# Checkout arithmetic

`src/checkout.py::total` implements [PB-001](../product/checkout.md#pb-001) by adding module constant `FEE` to the caller-supplied subtotal. It performs no I/O and has no imports. It owns this addition, not construction or validation of the subtotal. No other consumer or external dependency is present in the complete repository inventory.

`tests/test_checkout.py::test_total` imports the real function and checks `total(10) == 13`. This existing function was executed directly with Python 3, `-B`, and `runpy.run_path` at revision `no-git`: passed. This was not a full pytest run. No test runner configuration or CI command is supplied. A future fee change must update and execute this expectation against the intended policy; numeric input edge cases have no supplied checks.
