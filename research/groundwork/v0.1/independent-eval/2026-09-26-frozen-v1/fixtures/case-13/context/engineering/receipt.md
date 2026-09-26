---
{
  "schema_version": 1,
  "id": "CMP-receipt",
  "kind": "engineering",
  "scope": "checkout",
  "title": "CMP-receipt",
  "revision": "no-git",
  "sources": [
    {
      "path": "src/receipt.py"
    }
  ],
  "watches": [],
  "behaviors": [],
  "implements": [
    "PB-002"
  ],
  "depends_on": [],
  "verification": [
    {
      "behavior": "PB-002",
      "kind": "gap",
      "reference": "Add a targeted contract check."
    }
  ]
}
---
Implements [PB-002](../product/receipt.md#pb-002) in src/receipt.py.
