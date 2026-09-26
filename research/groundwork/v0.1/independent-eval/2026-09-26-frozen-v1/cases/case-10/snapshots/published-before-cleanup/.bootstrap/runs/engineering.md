---
{
  "schema_version": 1,
  "id": "CMP-checkout",
  "kind": "engineering",
  "scope": "checkout",
  "title": "Checkout total implementation",
  "revision": "working-tree",
  "sources": [
    {
      "path": "docs/checkout.md"
    },
    {
      "path": "src/checkout.py"
    },
    {
      "path": "tests/test_checkout.py"
    }
  ],
  "watches": [
    "docs/*checkout*.md",
    "src/*checkout*.py",
    "tests/test*checkout*.py"
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

# Checkout total implementation

`src/checkout.py::total` implements [PB-001](../product/checkout.md#pb-001) by adding module constant `FEE = 3` to the supplied subtotal. It owns this arithmetic and returns the result; the function has no inventory lookup or payment side effect. The caller is outside the established scope.

## Verification and change impact
`tests/test_checkout.py::test_total` asserts total(10)==13. Executed the discovered test through Python runpy against this working-tree fixture: PASS. A fee change needs coordinated review of docs/checkout.md, the implementation constant and this expected result. Additional input-domain checks require a defined input contract; no new test infrastructure was built.

## Investigation coverage
The root path list was truncated by the output limit. Narrow src, docs and tests inventories were complete. Only four primary content files were loaded, including the minimal manifest; no noise module was opened. No conclusions about the unrelated repository material are implied.

