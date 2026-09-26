---
{
  "schema_version": 1,
  "id": "CMP-checkout",
  "kind": "engineering",
  "scope": "checkout",
  "title": "Checkout implementation",
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
    "src/checkout*.py",
    "tests/test_checkout*.py",
    "docs/checkout*.md",
    "docs/adr*.md"
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

# Checkout implementation

Implements [PB-012](../product/checkout.md#pb-012) with src/checkout.py::total and constant FEE = 3. This function adds the fixed fee and invokes no external service or storage dependency.

## Verification

Existing tests/test_checkout.py::test_total asserts total(10) == 13, protecting fee addition for that example. The test was inspected, not executed. pyproject.toml provides no runner command. Currency and rounding requirements are not established here.
