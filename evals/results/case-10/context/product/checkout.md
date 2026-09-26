---
{
  "schema_version": 1,
  "id": "CAP-checkout",
  "kind": "product",
  "scope": "checkout",
  "title": "checkout",
  "revision": "no-git",
  "sources": [
    {
      "path": "src/checkout.py"
    },
    {
      "path": "docs/checkout.md"
    },
    {
      "path": "tests/test_checkout.py"
    }
  ],
  "watches": [
    "src/*.py",
    "docs/*.md",
    "tests/*.py"
  ],
  "behaviors": [
    "PB-001"
  ],
  "implements": [],
  "depends_on": [],
  "verification": []
}
---
# Checkout
<a id="pb-001"></a>
PB-001 — Observed and intended: total adds fixed fee 3 to subtotal. docs/checkout.md explains its purpose as packing costs. It states checkout does not determine inventory availability; inspected total agrees with this boundary. Currency and input-domain rules are unspecified. [Implementation](../engineering/checkout.md).
