---
{
  "schema_version": 1,
  "scope": "checkout",
  "revision": "working-tree",
  "watches": [
    "src/checkout.py",
    "tests/test_checkout.py",
    "docs/checkout.md"
  ],
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
  "id": "CMP-checkout",
  "kind": "engineering",
  "title": "Checkout calculation",
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
      "reference": "Caller integration and numeric/input contract coverage require caller and contract evidence"
    }
  ]
}
---

# Checkout calculation

## Responsibilities

`src/checkout.py::total` implements [PB-001](../product/checkout.md#pb-001): it accepts a subtotal, adds the module constant `FEE = 3`, and returns the result to the caller. No payment, inventory, persistence, or remote I/O occurs in the inspected function. The fixture does not establish its callers or their contracts.

## Dependencies and verification

The function depends on its supplied subtotal and the local `FEE` constant. `tests/test_checkout.py::test_total` imports this function and asserts `total(10) == 13`. That existing assertion passed by direct Python invocation on the inspected working-tree snapshot; a test runner suite was not run. `pyproject.toml` declares the sample project but no test command.

A fee change must review the product intent, constant, and existing expectation together. Verification gap: the available test does not establish input validation, currency/precision rules, or callers’ expectations. Caller integration checks require caller evidence, which is unavailable here. No missing test infrastructure was created.
