---
{
  "schema_version": 1,
  "id": "CMP-checkout-receipt",
  "kind": "engineering",
  "scope": "checkout",
  "title": "Receipt mapping implementation",
  "revision": "working-tree",
  "sources": [
    {
      "path": "docs/receipt.md"
    },
    {
      "path": "src/receipt.py"
    }
  ],
  "watches": [
    "docs/*receipt*.md",
    "src/*receipt*.py",
    "tests/test*receipt*.py"
  ],
  "behaviors": [],
  "implements": [
    "PB-002"
  ],
  "depends_on": [
    "CAP-checkout-receipt"
  ],
  "verification": [
    {
      "behavior": "PB-002",
      "kind": "gap",
      "reference": "Unit check that receipt(order) preserves order.id in the order_id field; no receipt test exists in the inspected fixture."
    }
  ]
}
---

# Receipt mapping implementation

`src/receipt.py::receipt(order)` implements [PB-002](../product/receipt.md#pb-002) by returning a dictionary with `order_id` taken directly from `order.id`. It owns the returned representation, not order-id creation, persistence, payment checks, fee calculation, or customer delivery.

## Dependencies and impact
Its only established dependency is a caller-supplied object exposing `id`; its output contract uses key `order_id`. No import or field in this function couples it to the checkout fee. Changing the identifier or output key would require the caller/consumer contract, which is not present in the available fixture. No downstream integration is asserted.

## Verification
The bounded inventory discovered no receipt-specific test. A unit check should assert that a representative order id is preserved under `order_id`. Establish accepted input types before adding validation expectations. No receipt check was run or authored. The separate checkout total test passed, but that does not verify this receipt behavior. The gap is recorded without building test infrastructure.

