---
{
  "schema_version": 1,
  "id": "CMP-checkout",
  "kind": "engineering",
  "scope": "checkout",
  "title": "Checkout calculation implementation",
  "revision": "working-tree",
  "sources": [
    {
      "path": "src/checkout.py"
    },
    {
      "path": "tests/test_checkout.py"
    }
  ],
  "watches": [
    "src/checkout.py",
    "tests/test_checkout*.py"
  ],
  "behaviors": [],
  "implements": [
    "PB-001"
  ],
  "depends_on": [
    "CAP-checkout-observed"
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

# Checkout calculation implementation

`src/checkout.py::total` implements [PB-001](../product/checkout.md#pb-001) by adding the module constant `FEE = 3` to its supplied subtotal. It owns the arithmetic, returning the result to its caller; no payment or packing action appears here. No downstream integration is established by the available sources.

## Verification
`tests/test_checkout.py::test_total` asserts that subtotal 10 returns 13. The discovered test was executed through Python runpy on the current working-tree fixture: PASS. It verifies the observed calculation, not why the fee exists. Review Q-001 before changing fee policy. Broader input-domain checks would need an established input contract first.

