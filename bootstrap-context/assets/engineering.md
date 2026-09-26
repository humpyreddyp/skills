---
{
  "schema_version": 1,
  "id": "CMP-example",
  "kind": "engineering",
  "scope": "example",
  "title": "Component name",
  "revision": "working-tree",
  "sources": [{"path": "src/example.py", "section": "handle"}],
  "watches": ["src/example*.py", "tests/test_example*.py"],
  "behaviors": [],
  "implements": ["PB-001"],
  "depends_on": ["CAP-example"],
  "verification": [
    {"behavior": "PB-001", "kind": "gap", "reference": "Describe the missing check for this behavior"}
  ]
}
---

# Component name

Replace the example metadata and these drafting instructions before publishing. Use real product page paths and behavior IDs. Omit sections without supported content.

## Responsibilities

Explain what this component owns and what it does not own. Connect its responsibility to [PB-001](../product/example.md#pb-001).

## Implementation and dependencies

Point to the implementing files and useful symbols. Explain relevant upstream/downstream relationships, APIs/events, data/control flows, storage/configuration, and external systems. Give source pointers for the relationships; keep unestablished ones in questions.

## Verification

For each implemented behavior, describe the existing checks and the checks a change would need across its dependencies. Separate checks discovered, checks actually run with revision/results, and missing checks worth adding. Keep the front-matter entries in sync with this account.
