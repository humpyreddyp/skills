# Bootstrap Context V1

The portable runtime is `bootstrap-context/`. Specification critique and concrete
improvements are in [DESIGN.md](DESIGN.md); evaluation evidence and limitations are
in [evals/RESULTS.md](evals/RESULTS.md).

## Final structure

```text
bootstrap-context/
  SKILL.md
  agents/openai.yaml
  references/
    evidence.md
    questions.md
    state-format.md
    commands.md
  assets/
    product.md
    engineering.md
  scripts/bootstrap.py
evals/                         # separate from the runtime skill
  make_fixtures.py
  test_runtime.py
  RESULTS.md
  results/
DESIGN.md
REPORT.md
bootstrap-context.zip          # runtime folder only
```

`SKILL.md` is 64 lines. There is one user-facing skill, one standard-library Python
helper, four purpose-specific references, two drafting templates, and optional Codex
display metadata. Automatic discovery remains enabled. No host instruction files
are modified.

## Workflow

The September 26 editorial revision uses plain language and a five-step process:
pick up the work, investigate, resolve questions, publish, and leave a next step.
Evidence guidance and human decisions have separate references. Product and
engineering pages have separate templates. Commands are grouped by task, with
long examples in code blocks instead of wide table cells. The Python helper and
saved-state schema are unchanged.

Inspect state first. On first invocation, perform cheap bounded discovery, help the
human select a capability unless already specified, and invite relevant evidence.
Investigate one bounded uncertainty at a time; use isolated investigators when
available and useful. Separate observed implementation from intended behavior.

Publish supported slices with stable PB IDs and product→component→dependency→
verification links. Keep unresolved material claims in questions rather than trusted
pages. Compare human answers against evidence. Only the human chooses FIX or IGNORE;
persist remediation or precise exclusions without changing application code.

Natural-language modes map to continue, resolve questions, show status, revalidate,
and expand scope. Scope completion is distinct from individual-page freshness.

## Deterministic versus model-driven

| Helper | Agent judgment |
|---|---|
| Bounded path inventory, category hints, Git revision | Capability selection, focused source/AST/LSP exploration |
| Stable PB allocation, schema/link/blocker checks | Claim interpretation, intent versus observation, materiality |
| Source hashes, recursive discovery watches, dependency propagation | Missing edges, evidence reconciliation, relevant test expectations |
| Atomic state/decision recording, writer lock | Human answer validation and honoring actual FIX/IGNORE choices |
| Derived context index and completion structure checks | Publication truth gate and final scope completion decision |

The helper discovers verification locations; it does not execute repository code or
implement tooling. Checks prove structural invariants, not semantic correctness.

## Resume and state

`.bootstrap/state.yaml` keeps small per-scope status, next action and current
checkpoint pointers, plus ID counters. Questions, remediation, exclusions, external
evidence and reviewed source fingerprints live in separate durable files. Temporary
findings/drafts live in `.bootstrap/runs/` and are removed when obsolete.

Markdown is canonical. `context/index.yaml` is generated from front matter and
freshness metadata. Working-tree edits, deletions, relevant new files, changed
external evidence, and dependency changes invalidate only affected pages and
dependents. The helper never rewrites conclusions automatically. Existing state is
preserved; unknown schemas and interrupted/missing tracking fail closed.

## Portability

The core uses standard `SKILL.md`, relative resource links, Markdown, YAML 1.2 data
in JSON syntax, and Python 3.9+ with no installed packages. Git is optional. There are
no required Codex tools, Claude tools, connectors, network calls or model APIs.
`agents/openai.yaml` is optional host display metadata; the workflow does not depend
on it. Copy the entire runtime folder to the receiving host's skill location.

Python 3.9.6 and 3.14.2 were exercised. Live Claude Code execution was not tested.
The future `wire-context` skill can use the documented index/exclusions/freshness
contract; V1 does not edit `CLAUDE.md` or `AGENTS.md`.

## Evaluation and limits

All **14 requested behavioral scenarios** reached their expected supported,
partial, or waiting outcome. Four targeted new-fixture reruns completed without
helper errors after instruction refinements. **23 runtime tests passed on both
tested Python versions**; the skill-creator validator passed.

After the September 26 editorial revision, all 14 behavioral scenarios were run
again with fresh fixtures and reached the appropriate outcomes. The 23 helper
tests passed again, and the revised skill, templates, and links passed validation.
The evaluator authentication interruption was resolved on retry. One recovered
evaluator JSON-parsing mistake led to a small command-documentation clarification;
the helper and its behavior did not change. See the editorial section of the eval
results for details and saved artifacts.

The first run exposed a real recursive-watch bug and recoverable invocation/state
friction; fixes and rerun evidence are documented in the results. V1 remains limited
by model evidence judgment, declared dependency coverage, page-level invalidation,
manually registered external revisions, JSON-form YAML, and explicit freshness
checks. It has no live Claude validation or production-scale evaluation yet.
