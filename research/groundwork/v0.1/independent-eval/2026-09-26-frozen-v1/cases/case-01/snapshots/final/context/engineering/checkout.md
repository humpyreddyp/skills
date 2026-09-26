---
{
  "schema_version": 1,
  "id": "CMP-checkout",
  "kind": "engineering",
  "scope": "checkout",
  "title": "Checkout total calculation",
  "revision": "working-tree",
  "sources": [
    {
      "path": "docs/adr-004.md"
    },
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
    "src/checkout.py",
    "tests/test_checkout*.py",
    "docs/adr-*.md",
    "docs/*checkout*.md"
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

# Checkout total calculation

## Responsibilities
`src/checkout.py::total` implements [PB-001](../product/checkout.md#pb-001) by adding module constant `FEE = 3` to `subtotal`. It calculates and returns a value; the inspected function does not collect payment or perform packing.

## Dependencies and ownership boundary
The only established input is the caller-supplied subtotal and the only output is the calculated total. No runtime dependency or downstream consumer is declared in the inspected implementation. The minimal project manifest supplies package identity, without a test-runner command.

## Verification
Discovered `tests/test_checkout.py::test_total`, asserting `total(10) == 13`. Executed the test function through Python runpy against the current working-tree fixture; PASS. A fee change must review the accepted v2 decision and update this expectation together. Additional subtotal/input-domain checks would protect a broader contract, but the fixture does not establish that broader contract.

