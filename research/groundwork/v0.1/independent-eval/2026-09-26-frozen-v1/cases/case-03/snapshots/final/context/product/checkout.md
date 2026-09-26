---
{
  "schema_version": 1,
  "id": "CAP-checkout-observed",
  "kind": "product",
  "scope": "checkout",
  "title": "Observed checkout fee calculation",
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
    "tests/test_checkout*.py",
    "docs/*checkout*",
    "docs/adr-*"
  ],
  "behaviors": [
    "PB-001"
  ],
  "implements": [],
  "depends_on": [],
  "verification": []
}
---

# Observed checkout fee calculation

<a id="pb-001"></a>
## PB-001 — Add the observed fixed fee
Observed: `total(subtotal)` returns the subtotal plus 3; the discovered example maps 10 to 13. This is implementation behavior, not an established product requirement.

## Ownership and coverage
Checkout calculates a value and returns it to its caller. The fixture establishes no payment or fulfillment handoff. The fee's purpose and intended policy remain a coverage gap in [Q-001](../../.bootstrap/questions.yaml), outside this page's supported claim. Scope remains partial because that intent matters to future changes.

[Implementation and checks](../engineering/checkout.md)

