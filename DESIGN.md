# Bootstrap Context V1: specification critique and choices

Written before implementation. Preserve the two connected baselines and the narrow
discover/investigate/publish purpose.

| Risk | Concrete V1 improvement |
|---|---|
| Context pollution | Small scope state; bounded scan; one investigation at a time; compact investigator output; disposable drafts/findings separate from durable decisions. |
| False confidence | Separate observed implementation from intended product behavior. No source hierarchy that automatically makes code, tests, docs, or human claims true. Structural validation explicitly cannot certify semantics. |
| Stale baselines | Hash actual working-tree sources, not only commits; watch relevant file sets for new dependencies; detect manual page edits; external evidence expires; propagate through declared doc dependencies. |
| Human interruption | Investigate first; reuse saved questions; batch non-blockers; only scope selection and material unresolved decisions interrupt. |
| Hidden dependencies | Trace events, config, shared storage, jobs, external/manual handoffs as well as imports. Preserve inaccessible coverage limits. |
| Weak product linkage | Stable PB anchors, explicit implementing PB lists, dependency links, per-behavior verification. Check linked product/engineering coverage at completion. |
| Token waste | Index is navigation, not copied knowledge; no full evidence dumps; no empty document hierarchy; selective reference loading. |
| Poor resumability | Idempotent initialization, stable ID allocation, atomic files, serialized writes, saved next action; missing or mismatched tracking is untrusted. |
| Generated-doc noise | Publish supported slices only; unresolved propositions stay in questions; overviews are optional. |
| Portability | Standard SKILL.md, relative resources, Python standard library; JSON-form YAML 1.2 removes package requirements. Host adapters are optional; no CLAUDE.md/AGENTS.md changes. |

Additional decisions: FIX records work without making the disputed claim trusted;
IGNORE is source-and-claim scoped and expires for review when evidence changes.
Freshness is checked on invocation, not by an installed daemon or git hook. There is
no guarantee that unwired readers opening raw Markdown will honor freshness. The
index contract makes that limitation explicit for the future wire-context skill.

Build the portable folder in this workspace, keep evals beside it, then install
the validated runtime folder in the default Codex skills directory. No app code
or global host instruction files are part of this work.
