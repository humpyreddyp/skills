---
{
  "schema_version": 1,
  "id": "CMP-receipt",
  "kind": "engineering",
  "scope": "checkout",
  "title": "receipt",
  "revision": "no-git",
  "sources": [
    {
      "path": "src/receipt.py"
    },
    {
      "path": "docs/receipt.md"
    }
  ],
  "watches": [
    "src/*.py",
    "docs/*.md",
    "tests/test_receipt*.py"
  ],
  "behaviors": [],
  "implements": [
    "PB-002"
  ],
  "depends_on": [
    "CAP-receipt"
  ],
  "verification": [
    {
      "behavior": "PB-002",
      "kind": "gap",
      "reference": "Targeted receipt order_id propagation check"
    }
  ]
}
---
# Receipt component
Implements [PB-002](../product/receipt.md#pb-002): src/receipt.py::receipt returns a dictionary containing order_id copied from order.id. The function has no fee dependency. No supplied test covers receipt. Proposed verification: check returned order_id equals the input ID. This check is a gap, not implemented or run.
