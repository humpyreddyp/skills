---
{
  "schema_version": 1,
  "id": "CAP-checkout",
  "kind": "product",
  "scope": "checkout",
  "title": "Observed checkout behavior",
  "revision": "no-git",
  "sources": [
    {
      "path": "src/checkout.py"
    },
    {
      "path": "tests/test_checkout.py"
    }
  ],
  "watches": [
    "src/checkout*.py",
    "tests/test_checkout*.py",
    "docs/checkout*.md",
    "docs/adr*.md"
  ],
  "behaviors": [
    "PB-001"
  ],
  "implements": [],
  "depends_on": [
    "CMP-checkout"
  ],
  "verification": []
}
---

# Observed checkout behavior

<a id="pb-001"></a>
## PB-001 — Total adds 3

Observed implementation adds a constant fee of 3 to the subtotal. The test asserts subtotal 10 gives 13. Product intent and rationale have not been established.

[Implementation and verification](../engineering/checkout.md). Purpose is outside this baseline pending [Q-001](../../.bootstrap/questions.yaml).
