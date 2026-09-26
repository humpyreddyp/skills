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

The fee’s purpose and intended policy are not established by the available repository. Q-001 in [.bootstrap/questions.yaml](../../.bootstrap/questions.yaml) tracks this completion-blocking gap separately. The following claim describes observed behavior only.

<a id="pb-001"></a>
## PB-001 — Add a fixed fee

Observed: `total(subtotal)` returns the supplied subtotal plus 3. For subtotal 10, the result is 13. The repository does not establish a currency, tax policy, or rounding rule. [Implementation and checks](../engineering/checkout.md).

The inspected capability owns total arithmetic. The function does not calculate the input subtotal, collect payment, reserve stock, or perform fulfillment. It returns a numeric total to its caller; no caller or downstream handoff is present in the inspected repository.
