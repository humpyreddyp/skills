---
{
  "schema_version": 1,
  "scope": "checkout",
  "revision": "working-tree",
  "watches": [
    "src/checkout.py",
    "tests/test_checkout.py",
    "docs/checkout.md"
  ],
  "sources": [
    {
      "path": "src/checkout.py",
      "section": "FEE and total"
    },
    {
      "path": "tests/test_checkout.py",
      "section": "test_total"
    },
    {
      "external": "checkout-owner-answer",
      "section": "Q-001 checked answer"
    }
  ],
  "id": "CAP-fee",
  "kind": "product",
  "title": "Checkout fee",
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

# Checkout fee

## Purpose and evidence

Observed: checkout adds a fixed fee of 3. Q-001 is resolved after independently checking code and test and recording the narrow human-authorized exclusion X-001. Fee purpose remains a coverage gap in Q-002; no rationale is inferred.

<a id="pb-001"></a>
### PB-001 — Add the checkout fee

For a supplied subtotal, `total(subtotal)` returns `subtotal + 3`; the existing check uses subtotal 10 and expects 13. The sources do not define currency or an input-validation contract. See [implementation and checks](../engineering/checkout.md).

## Ownership and handoff

Checkout owns addition of the fee to a supplied subtotal and returns the result to its caller. The function does not perform payment collection or inventory operations. Caller identity and owners of those downstream responsibilities are not established in the available evidence.

## Exclusion

X-001 excludes only the sentence “The fee is 2.” in docs/checkout.md. Other claims remain usable; no unrelated claim is currently present in that document. Review the exclusion when fee documentation changes.
