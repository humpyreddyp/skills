---
{
  "schema_version": 1,
  "id": "CAP-receipt",
  "kind": "product",
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
  "behaviors": [
    "PB-002"
  ],
  "implements": [],
  "depends_on": [],
  "verification": []
}
---
# Receipt
<a id="pb-002"></a>
PB-002 — Both intended and observed: receipt exposes order.id as order_id. docs/receipt.md explains that customers can reference their purchase. No delivery, persistence, or format guarantee is established. [Implementation](../engineering/receipt.md). Fee coverage is pending [Q-001](../../.bootstrap/questions.yaml).
