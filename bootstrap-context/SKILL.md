---
name: bootstrap-context
description: Build or resume a product and engineering baseline for an existing repository. Use when preparing repository context for future AI changes, resolving baseline questions, or revalidating changed sources. Does not fix application code.
---

# Bootstrap Context

Give the next agent enough context to change one capability safely: what it does, why it exists, where it lives, and what else a change could affect.

Code, docs, tests, and human answers can all be wrong. Establish what the evidence supports. Keep the difference between **what happens** and **what should happen** clear throughout the baseline.

## Process

### 1. Pick up where the work stands

Read `.bootstrap/state.yaml` and `context/index.yaml` first, if they exist. Show a short status and resume the saved next action. For a status-only request, report what is recorded without changing files. Before using published context for further work, run `freshness` to check its sources.

On a first run, make a cheap repo scan and help the human choose a capability or flow. Use the scope they already gave you. Invite useful context: requirements, product or architecture docs, diagrams, ADRs, contracts, runbooks, stale areas, and known concerns. They do not need to supply all of these before work can start.

Use [commands.md](references/commands.md) for the helper. Read [state-format.md](references/state-format.md) before writing records. A fresh session is useful, but don't restart a session that is already working well.

### 2. Investigate one question at a time

Read [evidence.md](references/evidence.md) before investigating or publishing. Choose one uncertainty that could affect a future change. Load the files needed to answer it, save a compact finding, and move on. An absent import is not an absent dependency: follow APIs, events, config, shared storage, external systems, and manual handoffs where the flow leads.

Keep deep investigations out of the main conversation when isolated agents are available. Give each a scope, source pointers, and a reading budget. Ask it to return only the finding, source references, any contradiction, and any unresolved question. The parent assigns IDs and writes durable state.

Without isolated contexts, use smaller investigations and checkpoint before a fresh session is needed. Saving a summary does not remove the files already loaded into the current conversation.

### 3. Resolve what the evidence leaves open

Investigate before asking the human. Save a question only when the answer matters and available evidence cannot reasonably settle it. Batch questions that do not block progress, and keep working on supported parts.

Use [questions.md](references/questions.md) when asking, validating an answer, or recording a decision. If a contradiction remains, the human chooses **FIX** or **IGNORE**. FIX records work for someone to do. IGNORE excludes a specific source or claim. Neither choice proves the remaining claim true.

### 4. Publish what is ready

Publish useful, supported parts as they become ready. Leave claims with unresolved contradictions out of trusted context. Missing product purpose is a question to investigate, not a reason to invent a story.

Start from the [product template](assets/product.md) or [engineering template](assets/engineering.md). Keep stable behavior IDs such as `PB-001`, and connect each important behavior to its implementation, dependencies, and verification. Record what each capability or component owns, what it does not own, and where work passes to another owner.

Review the evidence before calling `publish`. The helper checks structure, links, source changes, and recorded blockers. It cannot tell whether a claim is true. Add overview pages only when they help someone find their way.

### 5. Leave a clear next step

Save the scope status and next action after each investigation, before asking questions, and before stopping. Keep published Markdown in `context/`, durable records in `.bootstrap/`, and unfinished findings in `.bootstrap/runs/`.

A scope is complete when useful product and engineering context is linked, important dependencies and verification expectations are understood, and no unresolved question prevents safe reasoning about that scope. Non-blocking questions may remain. Remove obsolete Bootstrap-owned drafts and checkpoints after their useful content is saved elsewhere; retain relevant questions, remediation, exclusions, and source fingerprints.

## Later requests

- **Continue:** resume the saved next action.
- **Resolve questions:** check new answers against the evidence.
- **Show status:** report saved progress without changing it.
- **Revalidate:** investigate affected pages and their dependencies; leave unrelated areas alone.
- **Expand scope:** add the new scope without resetting existing work.

New context can change an earlier conclusion. Revisit the affected claims and questions. Use source fingerprints and the generated index to find them; never rewrite conclusions just because a file changed. See [state-format.md](references/state-format.md) for freshness and recovery.

## Boundaries

Bootstrap discovers, investigates, and publishes context. It does not change application code, perform fixes, choose FIX versus IGNORE, clean the repo, rewrite unrelated stale docs, or build missing test infrastructure.

Do not edit `CLAUDE.md` or `AGENTS.md`. A future `wire-context` skill can teach agents to start from the index and respect freshness, exclusions, dependencies, and verification. The core workflow must work without host-specific tools.
