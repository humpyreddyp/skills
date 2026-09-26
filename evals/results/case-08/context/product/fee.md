---
{
  "schema_version": 1,
  "id": "CAP-fee",
  "kind": "product",
  "scope": "checkout",
  "title": "Checkout fee",
  "revision": "no-git",
  "sources": [
    {
      "path": "src/checkout.py",
      "section": "FEE and total"
    },
    {
      "path": "tests/test_checkout.py",
      "section": "test_total"
    }
  ],
  "watches": [
    "src/checkout*.py",
    "tests/test_checkout*.py",
    "docs/checkout*.md"
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

# Checkout fee

<a id="pb-001"></a>
## PB-001 — Add fixed fee

Observed: checkout returns the caller-supplied subtotal plus 3. Subtotal 10 produces total 13. Currency and numeric unit are not established by these sources.

Consult the claim-specific [exclusion](../../.bootstrap/exclusions.yaml) and freshness index before relying on this baseline. Fee purpose remains an unresolved coverage item outside this supported arithmetic claim.

[Implementation and verification](../engineering/checkout.md).
