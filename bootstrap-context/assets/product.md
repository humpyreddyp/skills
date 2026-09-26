---
{
  "schema_version": 1,
  "id": "CAP-example",
  "kind": "product",
  "scope": "example",
  "title": "Capability name",
  "revision": "working-tree",
  "sources": [{"path": "src/example.py", "section": "handle"}],
  "watches": ["src/example*.py"],
  "behaviors": ["PB-001"],
  "implements": [],
  "depends_on": [],
  "verification": []
}
---

# Capability name

Replace the example metadata and these drafting instructions before publishing. Use the allocated behavior IDs. Omit sections without supported content; keep unresolved claims in questions.

## Purpose

Explain the supported purpose, intended outcomes, and why the important behaviors exist. Mark intent and observed behavior clearly.

## Behavior

<a id="pb-001"></a>
### PB-001 — Behavior name

Describe the behavior, when it applies, and its rules. Link the implementing component once its page is published: [implementation and checks](../engineering/example.md).

## Ownership and handoffs

Describe what this capability does and meaningful things it does not do. Name related capabilities and explain supported handoffs: what leaves this capability, who takes over, and where its responsibility ends.
