# Saved state and published pages

Save enough for a fresh session to continue without the earlier conversation. Keep findings and decisions; leave out reading transcripts and model reasoning.

## File format

Published pages are Markdown with YAML front matter. Machine-readable data uses **JSON syntax, a subset of YAML 1.2**. That includes the front matter and `.yaml` state files. This lets the helper run without a YAML package. Use double-quoted strings, no comments, and no trailing commas; general YAML is not supported.

Paths are repository-relative POSIX paths. Keep schema version 1 and preserve unknown fields when editing existing records. An unsupported version needs an explicit migration, never a reset.

## Where things live

| File | What to keep there |
|---|---|
| `.bootstrap/state.yaml` | `schema_version: 1`, a `scopes` mapping, and integer `next_pb` / `next_question` counters. |
| `.bootstrap/questions.yaml` | Questions and checked answers. |
| `.bootstrap/remediation.yaml` | Work requested through FIX decisions. |
| `.bootstrap/exclusions.yaml` | Sources/claims excluded through IGNORE decisions. |
| `.bootstrap/external.yaml` | External evidence IDs mapped to document or answer records. |
| `.bootstrap/tracking.yaml` | Reviewed source/watch fingerprints, dependency snapshots, and freshness reasons for each page. |
| `.bootstrap/runs/` | Temporary scans, drafts, and the current unfinished finding. |
| `context/index.yaml` | Generated page navigation, IDs, links, freshness, and pointers to exclusions/questions. |

`init --scope <slug>` creates missing files and preserves earlier work.

Keep `state.yaml` small. Each scope has a `status`, `next_action`, and optional `checkpoint` pointing to its current finding. Put inventories and source evidence elsewhere. A finding needs only the scope, conclusion, source pointers, unresolved edge, and next action.

Scope statuses are `not started`, `partial`, `waiting for human`, `needs revalidation`, and `complete`. Page freshness is either `current` or `needs revalidation`. Current pages do not automatically make a scope complete. After its stale pages are reviewed, the helper returns a scope to `partial`; make the final completion decision and save it explicitly.

## Published front matter

Use the [product](../assets/product.md) or [engineering](../assets/engineering.md) template. Replace its example values and drafting instructions with the actual supported content; omit body sections that do not help.

| Field | Meaning |
|---|---|
| `schema_version` | `1`. |
| `id` | Stable document ID, such as `CAP-checkout` or `CMP-worker`. |
| `kind` | `product` or `engineering`. |
| `scope` | A saved scope slug. |
| `title` | A short page title. |
| `revision` | The inspected commit/revision, or `working-tree` / `no-git` when accurate. |
| `sources` | Nonempty list of source references, described below. |
| `watches` | Narrow glob patterns for relevant files that might appear, change, or disappear. |
| `behaviors` | PB IDs owned by a product page; empty on engineering pages. |
| `implements` | PB IDs implemented by an engineering page; empty on product pages. |
| `depends_on` | IDs of baseline documents this page relies on. |
| `verification` | Check/gap entries for implemented behaviors; empty on product pages. |

A local source looks like `{ "path": "src/checkout.py", "section": "submit" }`. An external source looks like `{ "external": "requirements-v2", "section": "Checkout" }`. The section is optional. Use exact source files and pointers rather than excerpts. Documents outside the repo belong in external records. Generated context and state are not primary evidence; register human answers as external evidence when they support a claim.

Choose watches around the claim, such as `services/*/subscriptions.json`, rather than the whole repo. Source hashes detect working-tree edits even when HEAD is unchanged; the revision alone does not establish freshness.

Give each product behavior a stable ID and an explicit anchor such as `<a id="pb-001"></a>`. Never recycle IDs. Engineering pages must link to the actual product page and anchor, then explain the implementation and checks.

A verification entry has `behavior`, `kind` (`existing` or `gap`), and `reference`. For example:

```json
{"behavior": "PB-001", "kind": "existing", "reference": "tests/test_checkout.py::test_total"}
```

Every implemented PB needs an entry. A gap's reference describes the missing check. Whether an existing check was run belongs in the body with its result and revision.

Document dependencies may point both ways when product and engineering conclusions rely on each other. Record real dependencies, not every nearby page. Forward links can require a final reviewed republish once both pages exist; see [commands.md](commands.md).

## Questions and decisions

Question fields:

- `id` (`Q-001`), `scope`, `found`, `sources`, `why`, `affects` (document/PB IDs), `question`, `blocking` (boolean), and `status`.
- Status is `open`, `answered`, `conflicting`, `needs evidence`, or `resolved`.
- An answer uses `{ "summary": "...", "github_id": null, "sources": [] }`.
- `validation` records a short comparison with evidence. Resolve only after that review supports the answer or independently settles the question.
- `decision` may point to a FIX/IGNORE record while the question still blocks a claim. Reuse question IDs instead of duplicating questions.

Remediation fields: `id`, `question_id`, `scope`, `affects`, `sources`, `action`, `status` (`open` or `verified`), and `decision`. A decision holds `choice`, `human_statement`, and `github_id`.

Verified remediation means a completed fix was checked; Groundwork does not implement it. The associated question records whether the unresolved work blocks safe reasoning for the scope.

Exclusion fields: `id`, `question_id`, `scope`, `affects`, `source`, `claim`, `rationale`, `recheck_when`, `status` (`active`, `needs review`, or `retired`), `source_snapshot`, and `decision`. The source uses the same shape as page provenance.

Follow [questions.md](questions.md) when creating or changing decisions. Claim-level exclusions need judgment when other claims still use the same source. Review a changed source before extending its exclusion, and never silently broaden or retire the human's choice.

## External and newly supplied evidence

Each external evidence ID maps to `label`, `location`, `revision`, and `review_after` (`YYYY-MM-DD`). Use a concrete version or digest, not “latest.” The location can be a document URL/path or an answer reference. Keep imported content and raw answers out of tracking.

For human intent evidence, an external record may point to `.bootstrap/questions.yaml#Q-001` with a digest of the versioned answer summary. Registering it preserves provenance; it does not make the answer true.

When new material arrives, identify the affected documents or the scope needing investigation. Register the evidence and use `invalidate` for affected published IDs. For unpublished claims, update the question/finding. Compare the new material before changing conclusions.

External evidence needs a review date because local Git cannot detect remote changes. Updated records invalidate pages that cite them; expired dates require review and never renew themselves. Record inaccessible or missing external evidence as a coverage limit.

## Freshness and the index

Markdown is the canonical baseline. Generate `context/index.yaml` from its front matter and tracking; do not maintain it by hand or copy whole page bodies into it.

Before trusting a page, run `freshness` and read the index plus active or review-needed exclusions. The helper checks source content, file watches, published page content, document dependencies, external records, and exclusions. It marks affected pages and their dependents; it does not rewrite their claims or re-bootstrap unrelated areas.

Revalidation means investigating the changed claims and explicitly republishing those that pass review. A changed hash does not justify a new conclusion. Complete scopes can become `needs revalidation`.

Raw Markdown records what was reviewed at a particular revision. The future `wire-context` skill must teach readers to use this index/freshness/exclusion check; Groundwork does not write host instructions.

## Recover and clean up

Writes are atomic per file. If publication stops between page, tracking, and index writes, run `freshness` and `index`; mismatched or missing tracking stays untrusted until reviewed. If `.bootstrap/` is lost, preserve the Markdown and rebuild trust through evidence review and `publish`.

The helper allows one writer through `.bootstrap/.lock`. After a crash, check that its recorded process has stopped before removing the lock. One parent allocates IDs and writes state; isolated investigators return findings. Do not run multiple parent sessions against the same baseline. Reserve PB IDs with `allocate-pb`; gaps are fine.

After each investigation, save the finding or its durable outcome and one next action. Remove obsolete Groundwork-owned temporary files once their useful content is published or recorded elsewhere. This includes previous-session checkpoints no longer needed by a saved action. Retain relevant questions, open remediation, exclusions, fingerprints, and resume state. Never delete user files or perform cleanup during a status-only request.
