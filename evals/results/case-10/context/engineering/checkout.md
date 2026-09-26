---
{
  "schema_version": 1,
  "id": "CMP-checkout",
  "kind": "engineering",
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
  "behaviors": [],
  "implements": [
    "PB-001"
  ],
  "depends_on": [
    "CAP-checkout"
  ],
  "verification": [
    {
      "behavior": "PB-001",
      "kind": "existing",
      "reference": "tests/test_checkout.py::test_total"
    }
  ]
}
---
# Checkout implementation
Implements [PB-001](../product/checkout.md#pb-001): src/checkout.py::total returns subtotal + FEE, where FEE=3. This function has no external calls or storage; no wider independence is inferred. Existing tests/test_checkout.py::test_total invokes the function and asserts total(10)==13. Discovered, not executed; pyproject.toml declares no command. Relevant future fee changes should update this check. Only checkout sources were read; unrelated noise was excluded from investigation.
