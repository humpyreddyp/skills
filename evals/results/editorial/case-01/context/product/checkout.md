---
{
  "schema_version": 1,
  "id": "CAP-checkout",
  "kind": "product",
  "scope": "checkout",
  "title": "Checkout",
  "revision": "no-git",
  "sources": [
    {
      "path": "src/checkout.py"
    },
    {
      "path": "tests/test_checkout.py"
    },
    {
      "path": "docs/adr-004.md"
    },
    {
      "path": "docs/checkout.md"
    }
  ],
  "watches": [
    "src/checkout*.py",
    "tests/test_checkout*.py",
    "docs/*checkout*",
    "docs/adr-*.md"
  ],
  "behaviors": [
    "PB-001"
  ],
  "implements": [],
  "depends_on": [],
  "verification": []
}
---

# Checkout fee

Intended purpose: the accepted v2 decision says the fee covers packing costs (docs/adr-004.md). This agrees with the observed implementation. The fee of 2 in docs/checkout.md belongs to retired v1 and is not the current contract.

<a id="pb-001"></a>
## PB-001 — Add a fixed fee

Observed: `total(subtotal)` returns the supplied subtotal plus 3. For subtotal 10, the result is 13. The repository does not establish a currency, tax policy, or rounding rule. [Implementation and checks](../engineering/checkout.md).

The inspected capability owns total arithmetic. The function does not calculate the input subtotal, collect payment, reserve stock, or perform fulfillment. It returns a numeric total to its caller; no caller or downstream handoff is present in the inspected repository.
