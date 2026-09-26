---
{
  "schema_version": 1,
  "scope": "checkout",
  "revision": "working-tree",
  "sources": [
    {
      "path": "src/checkout.py",
      "section": "total"
    },
    {
      "path": "tests/test_checkout.py",
      "section": "test_total"
    },
    {
      "path": "docs/checkout.md"
    }
  ],
  "watches": [
    "src/checkout*.py",
    "tests/test_checkout*.py",
    "docs/checkout*.md"
  ],
  "verification": [
    {
      "behavior": "PB-012",
      "kind": "existing",
      "reference": "tests/test_checkout.py::test_total"
    }
  ],
  "implements": [
    "PB-012"
  ],
  "behaviors": [],
  "depends_on": [
    "CAP-checkout"
  ],
  "id": "CMP-checkout",
  "kind": "engineering",
  "title": "Checkout total calculation"
}
---

# Checkout total calculation

## Responsibilities
src/checkout.py::total implements [PB-012](../product/checkout.md#pb-012). It owns adding the module-level FEE (3) to its input subtotal and returning the result. Inventory availability belongs outside checkout, according to docs/checkout.md; this function performs no inventory lookup or payment operation.

## Implementation and dependencies
The input subtotal is provided by a caller whose identity is not supplied. The function depends on the module constant and numeric addition. The test imports total directly. There are no external calls or other component handoffs in this function; repository evidence does not establish a broader checkout architecture.

## Verification
Existing: tests/test_checkout.py::test_total asserts total(10) == 13. The test was inspected, not executed, against the supplied working-tree fixture. pyproject.toml contains project metadata but no declared verification command. A fee change requires checking both total and its expected test value against packing-fee intent. Input-domain and boundary checks are not present in the supplied test; supported domains are not established. No new infrastructure was added. The enclosing Git revision is not a dedicated fixture revision.
