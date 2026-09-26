---
{
  "schema_version": 1,
  "id": "CMP-fee",
  "kind": "engineering",
  "scope": "checkout",
  "title": "CMP-fee",
  "revision": "no-git",
  "sources": [
    {
      "path": "src/checkout.py"
    }
  ],
  "watches": [],
  "behaviors": [],
  "implements": [
    "PB-001"
  ],
  "depends_on": [],
  "verification": [
    {
      "behavior": "PB-001",
      "kind": "gap",
      "reference": "Add a targeted contract check."
    }
  ]
}
---
Implements [PB-001](../product/fee.md#pb-001) in src/checkout.py.
