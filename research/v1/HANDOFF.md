# Bootstrap Context V1 research handoff

Frozen September 26, 2026. Research name: **Bootstrap Context V1**. Skill version:
**v0.1**. Local Git tag: `bootstrap-context-v0.1`.

**Source and evidence commit:** `eb996aa8d59458a3d0d9b411bf4680cbbe9b86fc`.
The handoff, experiment manifest, and downstream design are accompanying research
documents committed afterward; they do not change that source revision.

## Purpose and frozen contents

Bootstrap builds or resumes an evidence-grounded product and engineering baseline
for a bounded capability in an existing repository. It distinguishes observed
behavior from intended behavior, follows dependencies beyond imports, records
questions and explicit human FIX/IGNORE decisions, publishes supported context
incrementally, and preserves resumable state and selective freshness tracking.
It does not implement application changes or prove the truth of model judgments.

The frozen runtime contains exactly these nine files under `bootstrap-context/`:

```text
SKILL.md
agents/openai.yaml
references/evidence.md
references/questions.md
references/state-format.md
references/commands.md
assets/product.md
assets/engineering.md
scripts/bootstrap.py
```

Their SHA-256 hashes are in [experiment-manifest.json](experiment-manifest.json).
The repository ZIP and installed copy matched all nine hashes at freeze. The Git
snapshot is authoritative; a later change to an installed copy cannot redefine V1.
Any future skill change needs a new revision and an explicit evaluation decision.

**Version provenance caveat:** the September 26 behavioral rerun evaluated the
editorial revision. After it finished, one paragraph was added to `commands.md`
explaining that successful helper output is JSON and naming the `behavior` field.
That clarification is included in V1; the full behavioral suite was not rerun
after it. The helper and state schema were unchanged. The exact earlier prose
snapshot was not retained. Do not describe V1 as a byte-for-byte behavioral run
of every final instruction. No correctness issue was found that invalidates the
recorded observations, and no runtime file was changed during the freeze.

## Evaluation method

The local fixture generator creates 14 isolated synthetic brownfield repositories
and their requests. Three evaluating agent sessions handled cases 1–4, 5–8, and
9–14, executing Bootstrap and writing actual context and state. Cases within a
group shared an evaluator session. Human answers and decisions were supplied in
the fixture requests; unresolved questions were recorded as simulated responses.
The parent inspected reports and representative artifacts against the intended
evidence, publication, traceability, and state behavior. This was qualitative,
development-time evaluation, with no blinded external adjudication or statistical
sampling plan.

The record contains a September 25 pass, targeted reruns of cases 1, 5, 8, and 9,
and a complete September 26 editorial rerun. Exact model identifiers, reasoning
settings, seeds, and complete token/tool transcripts were not retained. Those
fields are explicitly unknown in the manifest. The generator and helper tests
are reproducible; the historical model executions are referenceable, not exactly
replayable from this archive alone.

## Behavioral scenarios

All 14 final editorial cases reached the expected outcome. A correct outcome can
be partial, waiting for a human, or needing revalidation; it does not mean every
case produced a complete baseline.

| ID | Scenario | Observed outcome |
|---|---|---|
| 01 | Stale docs/current code | Distinguished retired fee 2 from current v2 fee 3 using the ADR; completed without an unnecessary question. |
| 02 | Current docs/code conflict | Withheld the disputed fee, saved Q-001, and waited without inventing FIX/IGNORE. |
| 03 | Missing product context | Published observed arithmetic, left rationale unknown, and retained partial status. |
| 04 | Hidden dependency | Traced checkout events through deployment subscription to warehouse; distinguished configured wiring from runtime assurance. |
| 05 | Supported human answer | Checked fee/purpose against evidence, recorded the supplied identity, resolved the question, and published linked context. |
| 06 | Conflicting human answer | Preserved the conflict and withheld the requested unsupported rewrite. |
| 07 | FIX | Recorded open remediation; left application code/tests unchanged and the claim unresolved. |
| 08 | IGNORE | Excluded only the specified claim, with fingerprint and recheck trigger; retained independent evidence and a purpose gap. |
| 09 | Resume | Used saved state and PB-012 without an earlier conversation; preserved ID continuity and removed the obsolete checkpoint. |
| 10 | Noisy repository | Narrowed a truncated inventory and inspected four relevant files instead of 1,200 unrelated modules. |
| 11 | Incremental publication | Published receipt context while withholding the conflicting fee and retaining the blocking question. |
| 12 | Traceability | Linked product behavior to components, dependencies, and verification gaps; did not mistake a tautological test for assurance. |
| 13 | Changed source | Marked only the affected fee pages for revalidation; receipt stayed current and Markdown was not rewritten. |
| 14 | Responsibility boundaries | Captured checkout/warehouse ownership, non-ownership, and handoff without inventing fulfillment guarantees. |

## Helper coverage and observed results

The 23 standard-library tests cover bounded discovery; nested source packages;
recursive watches; source deletion/change and external revision/expiry; selective
and transitive invalidation; mutual dependencies; edited-page and missing-tracking
trust; publication blockers; behavior/verification links; fresh completion and
scope recovery; scoped IGNORE and FIX boundaries; interruption recovery; stable
IDs, checkpoints, and expansion; locks, schema checks, path traversal, and symlinks.

The historical record reports 23/23 on Python 3.9.6 and 3.14.2, and another 23/23
on 3.14.2 after the editorial revision. A supplemental freeze check also passed
23/23 on Python 3.14.2/macOS arm64. Its durable verbose log and individual test
results are in [evidence/helper-freeze-check](evidence/helper-freeze-check).
This new log is not a recovered transcript of the historical runs. Historical
validator success is retained in the original reports; it is a structural check.

## Failures, corrections, and rerun history

- The initial helper result was **20/21**: recursive matching missed a deeply
  nested consumer. Anchored segment matching fixed it. Later scope-recovery and
  nested-`src/context/` tests brought the suite to 23.
- Initial evaluator calls used absolute draft paths or invalidated unpublished
  IDs. The helper rejected them safely. Command guidance was clarified, and
  cases 1, 5, 8, and 9 were rerun without helper errors.
- Mutual forward links initially left pages stale and completion was rejected.
  Reviewed republishing recovered them; the workflow was documented without a
  trust bypass.
- Scope status could remain stale after all pages were current. The helper was
  corrected to return to partial; case 11's missing final checkpoint was recovered.
  Discovery was also corrected to retain nested source packages named `context`.
- Cleanup ownership was clarified and resume cleanup checked. The editorial
  rewrite then separated evidence/questions and product/engineering templates.
- Editorial evaluator launches hit service authentication failures before task
  execution; a retry succeeded. This is an infrastructure event, not a behavioral
  failure or evidence that the user needed an API key.
- During editorial case 9, evaluator parsing mistook a JSON response for a bare
  ID. It recovered the already allocated PB-012 without resetting state. The
  post-run documentation clarification described above followed.

[The original results narrative](../../evals/RESULTS.md), initial reports, targeted
rerun reports, and editorial reports are retained without rewriting them. Early
pre-fix source versions and complete console transcripts were not retained; this
freeze does not manufacture a historical commit sequence.

## Evidence locations and limitations

- [evals/results](../../evals/results): original reports, targeted reruns, both
  historical hash manifests, and original final artifacts for all 14 cases.
- [evals/results/editorial](../../evals/results/editorial): the three grouped
  reports covering all 14 cases and each case's final context/state artifacts.
- [evidence](evidence): exact retained editorial requests, an archive of remaining
  source fixture files, its inventory, pre-freeze evidence hashes, and helper logs.
  Temporary absolute paths in reports are historical; use the manifest's archive
  mappings. Earlier case snapshots 1, 5, 8, and 9 contain targeted-rerun outputs.
  Full intermediate state snapshots were not saved for every failed attempt.

Limits remain: synthetic cases, shared evaluator sessions, no live Claude Code
or remote integration run, no adversarial suite, and no production-scale sample.
Model judgment determines intent, evidence quality, materiality, dependency
completeness, exclusions, and completion. Freshness sees declared sources and
edges; external changes require registered revisions or review expiry. It has no
background watcher. Consumers must honor the index, exclusions, and freshness.
Page-level invalidation is conservative; JSON-form YAML and symlink restrictions
apply. There is no multi-parent coordination, automatic migration, or AST engine.

## What the evidence establishes

The record demonstrates the observed Bootstrap behavior on these fixtures and
deterministic helper protections on these tests, including recovery from recorded
development failures. It supports using this identifiable artifact as a research
baseline with known limitations.

**It does not establish that Bootstrap improves downstream coding-agent
performance.** No controlled actual software-change tasks compared repository-only
agents with baseline-assisted agents. It also does not establish production
reliability, cross-model/host generalization, exhaustive dependency discovery,
optimal token use, or the truth of every generated claim.

The next session should follow [DOWNSTREAM-DESIGN.md](DOWNSTREAM-DESIGN.md): pin V1,
select held-out software-change tasks, prepare matched A/B/C context bundles and
independent scoring, then lock the protocol before running anything. **No
downstream experiment was run in this freeze session.**
