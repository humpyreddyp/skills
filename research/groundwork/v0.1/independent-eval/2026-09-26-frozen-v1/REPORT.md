# Independent frozen Groundwork evaluation

**Result:** All 14 bounded behavioral cases PASS; the additional fresh-session cleanup case PASS. The 23 unchanged helper tests pass on both Python 3.14.2 and 3.9.6. No Groundwork or helper defect was established in these executions. Broader context-management validation is **PARTIAL**, and exact model reproducibility is incomplete. These results support keeping the artifact frozen as a V1 research baseline, with the limitations below; they do not establish production-scale reliability or coding-performance benefit.

## 1. Exact artifact and integrity

Repository: `https://github.com/humpyreddyp/skills`. Evaluated commit: **`52e6d91eebdb0973bc18dfcdc0deb0b97f4a16e3`**. The runtime was read and executed only from the separate detached worktree `/Users/humpyreddypininti/.codex/worktrees/groundwork-independent-eval/skilly`. No evaluation branch was created and no frozen skill file was edited. Initial Git status was empty. Final status, commit, detached HEAD, and file hashes are recorded in [freeze-verification.json](freeze-verification.json).

Evaluation artifacts are separate from development-time `evals/results/`. The output directory is a dedicated untracked directory in the primary checkout; its generated fixtures do not execute the development skill. Their inherited parent Git revision is a documented fixture limitation. A supplemental fresh-session fixture and portability probes ran outside any Git checkout under `/private/tmp`.

## 2. Environment, model, and independence

Evaluation date: **2026-09-26**, beginning 15:18 UTC, America/New_York local timezone. Host: Codex desktop, macOS 15.7.9 arm64; Git 2.50.1 (Apple Git-155). Primary interpreter: `/opt/homebrew/opt/python@3.14/bin/python3.14`, Python 3.14.2; additional interpreter: `/usr/bin/python3`, Python 3.9.6. Network restricted; workspace-write sandbox. No dependencies installed.

Model identity available to this evaluator: **GPT-6 family**. Exact model/version, reasoning effort, and token usage were **not exposed**. Agents inherited the parent configuration. These fields are unknown, not defaults or zero. This prevents an exact model/settings replication claim. [Environment record](environment.json), [runtime addendum](raw/runtime-addendum.json), and [method](METHOD.md).

Three fresh executing agents ran groups 1–4/10/11, 5–8, and 9/12–14. Case 9 was the first case in its agent context. Cases had fresh filesystem state but other cases within a group shared accumulated executor context. A fourth fresh agent later exercised resume/cleanup. Agents received prompts and frozen skill instructions, not prior results. The parent inspected actual source agreement, state, and generated pages. This is a single synthetic validation pass, not 14 independent model samples.

Independent judgments were sealed at **2026-09-26T15:26:05.423594+00:00** before any historical conclusions were read. [Locked judgment](independent-judgment-before-comparison.json) and its [SHA-256](raw/independent-judgment-lock.txt) remain unchanged. Historical comparison reads are separately logged.

## 3. Behavioral evaluation

PASS means the observed response and artifacts fulfilled the bounded request. A correctly unresolved human decision is a successful outcome. Artifact links include generated context, saved state, exact prompt, raw logs, execution drivers, snapshots, and case responses.

| # | Case | Rating | Actual behavior and reason | Human input still needed | Unexpected behavior / limit | Artifacts |
|---|---|---|---|---|---|---|
| 1 | Stale docs versus implementation | **PASS** | Used retired-v1 label and accepted v2 ADR to reconcile fee 2 versus 3; published two current linked pages. | None | Historical records correctly retained rather than treated as contradictions. | [Evidence](cases/case-01/); [state/context](fixtures/case-01/) (2 pages) |
| 2 | Current docs/code contradiction | **PASS** | Persisted conflicting Q-001 with sources/impact; no trusted fee page; waiting for human. | Explicit correction/exclusion decision or further evidence | No choice invented. | [Evidence](cases/case-02/); [state/context](fixtures/case-02/) (0 pages) |
| 3 | Missing product context | **PASS** | Published observed-only calculation and engineering pages; persisted purpose question and partial scope. | Purpose and intended policy | Question targets a separate purpose claim; observed calculation remains usable. | [Evidence](cases/case-03/); [state/context](fixtures/case-03/) (2 pages) |
| 4 | Hidden cross-component dependency | **PASS** | Traced event producer through subscription mapping to warehouse handler; three pages and explicit coverage gaps. | None for configured flow; runtime contracts needed for stronger guarantees | Executed tautological existing assertion but explicitly rejected it as handoff coverage. | [Evidence](cases/case-04/); [state/context](fixtures/case-04/) (3 pages) |
| 5 | Supported human answer | **PASS** | Validated answer against docs/code/test, captured product-owner, resolved Q-001 and published linked context with external answer provenance. | None | Direct assertion invocation passed; no suite pass claimed. | [Evidence](cases/case-05/); [state/context](fixtures/case-05/) (2 pages) |
| 6 | Conflicting human answer | **PASS** | Retained supplied fee-2 answer as conflicting with fee-3 evidence, captured attribution, withheld disputed publication. | FIX/IGNORE choice or additional evidence; may remain unresolved | No automatic preference for stakeholder or code. | [Evidence](cases/case-06/); [state/context](fixtures/case-06/) (0 pages) |
| 7 | Human chooses FIX | **PASS** | Recorded open R-001 with exact decision and attribution, preserved conflict, changed no application/test source. | Engineering must perform fix and later evidence must verify it | Remediation did not imply resolution. | [Evidence](cases/case-07/); [state/context](fixtures/case-07/) (0 pages) |
| 8 | Human chooses IGNORE | **PASS** | Recorded narrow X-001 with source fingerprint/recheck trigger; independently verified remaining fee-3 claim, published two pages, kept nonblocking Q-002. | Fee purpose remains needed for completion | Fixture has no second substantive doc claim; preservation of other same-file claims is not fully exercised. | [Evidence](cases/case-08/); [state/context](fixtures/case-08/) (2 pages) |
| 9 | Fresh-session resume | **PASS** | Fresh agent followed saved next action, allocated PB-012 from counter 12, published two linked pages and removed obsolete completed checkpoints. | None | Initial request-path lookup error retained; parent Git revision not attributed to fixture. | [Evidence](cases/case-09/); [state/context](fixtures/case-09/) (2 pages) |
| 10 | Large/noisy bounded investigation | **PASS** | Scan limited displayed paths, narrowed src/docs/tests, read four relevant source files and zero noise content, published two pages. | None | 1,300 irrelevant noise/dependency files avoided; nested subagent behavior not exercised because slots were occupied. | [Evidence](cases/case-10/); [state/context](fixtures/case-10/) (2 pages) |
| 11 | Incremental publishing | **PASS** | Published independent receipt PB-002 and engineering gap while fee PB-001 stayed blocked by saved Q-001. | Resolve fee contradiction | No blocking-record downgrade or whole-scope publication stall. | [Evidence](cases/case-11/); [state/context](fixtures/case-11/) (2 pages) |
| 12 | Behavior/implementation/dependency/verification | **PASS** | Published two PB anchors linked to producer/consumer pages, deployment wiring, existing-test limitations and missing contract/integration checks. | No input for bounded baseline; contracts needed for stronger guarantees | pytest attempt failed before collection because pytest is absent; not reported as passing and not installed. | [Evidence](cases/case-12/); [state/context](fixtures/case-12/) (3 pages) |
| 13 | Selective freshness/revalidation | **PASS** | Marked only CAP-fee/CMP-fee stale; receipt pages stayed current; all four Markdown baselines byte-identical; saved mismatch investigation next. | Resolve newly observed code/docs/test mismatch before publishing changed fee | Agent also read unrelated receipt source/pages for comparison; retrieval was less selective than invalidation. | [Evidence](cases/case-13/); [state/context](fixtures/case-13/) (4 pages) |
| 14 | Responsibility and negative boundaries | **PASS** | Published checkout/warehouse ownership, non-ownership and handoff, distinguishing accepted event from successful stock reservation. | None for established ownership; missing runtime contracts remain limits | Tests inspected only; no unsupported live delivery claims. | [Evidence](cases/case-14/); [state/context](fixtures/case-14/) (3 pages) |

The read-only parent audit found **27 final pages, of which 23 were newly authored and 4 were seeded freshness-fixture pages**. All 14 structural checks passed. Every original application/document/test/configuration source remained byte-identical, and no new application files or test infrastructure were created. The four case-13 Markdown pages also remained byte-identical. [Parent audit](parent-artifact-audit.json).

## 4. Context management

**PASS for bounded discovery, persisted resume, and compact findings; PARTIAL for the broader isolation/scale claims.** Saved state carries small scope/status/next-action records. The new-session executor recovered the saved action and next PB ID without earlier chat. The cleanup executor began with state/index, ran freshness, read relevant decisions and pages, and retained unresolved work.

Case 10 scanned 1,209 entries, reported 1,204 visible files with displayed paths truncated to 40, then narrowed to `src`, `docs`, and `tests`. It read **4 primary content files**, **0 of the 1,200 noise modules**, and **0 of 100 node_modules files**. Directory enumeration is distinct from loading content into model context. No attempt to comprehend the entire repository was observed. Compact findings point to evidence rather than reproduce source dumps.

All three initial executor slots were occupied during the relevant investigations. Agents used the documented small-investigation/checkpoint fallback. This demonstrates isolated *case execution* and fresh-session resume, but does **not** demonstrate the skill automatically splitting a genuinely file-heavy investigation into child contexts. The noise fixture has only four relevant source files; it is not a large relevant architecture. Case 13 also read the unrelated receipt pages/source for comparison, even though only fee context was invalidated. This is a small retrieval-efficiency weakness, not an invalidation failure.

| Case | Primary content files inspected | Recorded command steps |
|---|---:|---:|
| 1 | 5 | 13 |
| 2 | 4 | 11 |
| 3 | 3 | 14 |
| 4 | 7 | 17 |
| 5 | 4 | 32 |
| 6 | 4 | 11 |
| 7 | 4 | 13 |
| 8 | 4 | 26 |
| 9 | 4 | 23 |
| 10 | 4 | 16 |
| 11 | 6 | 17 |
| 12 | 7 | 23 |
| 13 | 4 | 9 |
| 14 | 7 | 22 |

These are observable command records, not standardized cognitive steps. Group B counts wrapper and nested commands separately; group A separately logs authored writes/deletions. Skill/reference reads (seven files per executor), state reads, helper fingerprint reads, and final integrity hashing are distinct from primary model-content reads. Use each case’s metrics definition and raw log for exact interpretation. Tokens/context occupancy are unavailable; no token savings percentage is claimed.

## 5. Published-context review

Representative pages reviewed: case 1 fee/v2 rationale; case 3 observed-only calculation; cases 4/12 event flow; case 5 checked human answer; case 8 scoped exclusion; case 11 receipt; case 14 ownership. Newly authored Markdown bodies range from **90 to 241 words**. They use ordinary explanatory prose, supported intent/observation distinctions, PB anchors, relative component links, specific source paths, and explicit limits.

Product/engineering linkage is functional: product PB IDs map to engineering `implements` and links; producer → subscription config → consumer relationships lead to concrete verification expectations. Checkout acceptance is not represented as successful reservation. The producer’s tautological test is identified as insufficient. Unknown payment, transport, retry/idempotency and inventory semantics remain coverage limits. Contradictory current fee claims are withheld from trusted pages in cases 2/6/7/11. Missing rationale is not invented in cases 3/8.

`context/index.yaml` is **925–1,616 bytes** for cases containing pages and holds navigation/IDs/links/freshness plus pointers to questions/exclusions, not duplicated page bodies. Provenance uses source pointers and fingerprints rather than copied evidence; checked human answers have external IDs, a digest revision, attribution, and a review date. Metadata is proportionally substantial in these tiny examples, and several coupled pages share broad source lists, but it remains navigational/provenance data.

Limit: the helper cannot verify truth. These semantic findings are parent judgments based on synthetic source inspection, not proofs of dependency completeness. Case-13 pre-seeded pages are fixture inputs, not examples of the executing agent’s prose quality.

## 6. Human questions, resume, cleanup, and freshness

Investigation preceded human questions; questions captured findings, sources, why they matter, affected IDs, and requested decisions. Supplied GitHub ID `product-owner` was preserved; no local Git identity was substituted. The supported answer was validated, while the conflicting answer remained conflicting. FIX recorded open remediation and did not resolve the claim or alter code. IGNORE retained an exact source/claim, rationale, review trigger, decision, and fingerprint, then separately checked remaining evidence.

Case 8’s nonblocking Q-002 persisted while supported observed pages remained current and the scope stayed partial. Its document contains only the excluded claim, so retaining a second meaningful claim in the same document is **not fully exercised**. The helper regression independently checks scoped exclusions and changed-source review.

The additional [fresh-session cleanup](supplemental/resume-cleanup/) recovered from persisted state with no earlier chat, retained Q-002, X-001, unrelated tax Q-003/R-001, external records and fingerprints **byte-for-byte**, preserved user notes and application files, removed two obsolete Groundwork drafts, and saved a next action. A draft’s stale `fee.md` pointers were checked against actual `checkout.md` pages rather than trusted. Completed case 9 also disposed of obsolete saved checkpoints after publication. Raw before/after snapshots remain in evaluation evidence.

Case 13’s generator changed the supporting fee source from 3 to 4 after publication. Execution marked only CAP-fee/CMP-fee `needs revalidation`, left both receipt pages current, and changed no Markdown claims. It saved the newly visible code/docs/test mismatch for investigation. Incremental changed-claim republishing and dependency propagation are covered by the deterministic suite; a complete human-resolution-and-republish behavioral roundtrip was **not** executed because this request explicitly prohibited rewriting the baseline yet. A separate status-only smoke test proved all saved files unchanged.

## 7. Helper/regression results

| Runtime | Unique tests | Passed | Failed | Test-reported duration |
|---|---:|---:|---:|---:|
| Python 3.14.2 | 23 | 23 | 0 | 3.556 s |
| Python 3.9.6 | 23 | 23 | 0 | 2.723 s |

That is **23 unique tests, 46 successful executions**, not 46 distinct tests. Commands used the unchanged frozen `evals/test_runtime.py` via unittest discovery with bytecode writes disabled. No warnings or errors were emitted by either helper suite. Coverage includes path safety, lock/schema preservation, missing tracking, decision interruption recovery, blockers, anchors/verification linkage, recursive watches, source/external/dependency changes, scope completion, and resumable IDs. [3.14 raw log](raw/helper-suite.jsonl), [3.9 raw log](raw/helper-suite-python39.jsonl).

No helper failure required a repair or behavioral-case rerun. Application verification is separate: some simple assertions were invoked directly; case 12’s pytest attempt failed before collection because pytest was absent, and cases 9/14 explicitly marked tests as inspected rather than executed.

## 8. Rename and portability

PASS: front-matter name `groundwork`, display name `Groundwork`, README invocation `$groundwork`, all 15 instructional resource links, script/template/reference availability, and packaged-file equality. No runtime reference to the old folder name appears in the nine runtime files. An arbitrary relocated installation folder successfully ran the helper. `groundwork.zip` exactly matches the committed skill files.

The old archived helper is byte-identical. A saved run created with that helper resumed using the new path; `init` preserved state/checkpoint, and allocation continued PB-001 → PB-002. `.bootstrap/` and schema remained compatible. Historical `bootstrap-context` names in REPORT/research/old package were explicitly treated as preserved history, not defects.

A naive link probe reports two missing template example output links; these are drafting placeholders explicitly meant to be replaced, not missing runtime resources. The raw negative result and its separate interpretation are preserved. Native skill installation/discovery in other hosts was not exercised; no live Claude Code or Windows/Linux run is claimed. [Portability report](portability-report.json), [raw probe](raw/portability.jsonl), [interpretation](raw/portability-interpretation.json).

## 9. Comparison with earlier development evaluations

Only after all executions and the independent judgment lock, the parent read `evals/RESULTS.md`, `REPORT.md`, `research/groundwork-rename.json`, and README from the frozen worktree. [Timestamped read log](raw/post-run-history-comparison.jsonl). No historical summary was supplied to executing agents.

The 14 bounded outcomes agree with the earlier development results. Their initial recursive-watch failure and later absolute-draft/unpublished-ID/JSON-ID invocation errors did not recur. Mutual document dependencies sometimes required the already documented reviewed republish; the new runs reached current pages without bypassing trust checks. Both Python runtimes independently reproduced 23/23. Earlier agent authentication interruptions did not occur here.

Differences in this pass: missing pytest in case 12; explicit fixture-parent Git-revision limitation; case-13 over-reading of unrelated receipt context; stronger separate durable-record cleanup exercise; unavailable exact model/settings/tokens. These differences limit comparison but do not reverse any core case outcome. The rename record says it had **no new behavioral evaluation**; this pass supplies fresh behavioral evidence for the renamed SHA, separately from the old V1 evidence.

## 10. Failures, partial evidence, and newly observed weaknesses

| Classification | Finding | Consequence |
|---|---|---|
| Groundwork skill failure | None established in executed bounded cases. | Do not infer universal correctness. |
| Helper/runtime failure | None; both 23-test runs and behavioral helper commands succeeded. | Structural checks still cannot prove truth. |
| Evaluation-fixture / harness failure | All three initial agents tried an ambiguous requests path at the evidence root; actual file is `fixtures/requests.json`. Reads failed and were corrected before task execution. | Failures retained; no skill change. |
| Evaluation-fixture limitation | Nested fixtures inherit parent Git HEAD; IGNORE fixture lacks a second substantive same-file claim; the noise case has tiny relevant scope. | Working-tree provenance used; no cross-file-scale or full claim-retention claim. |
| Evaluation-probe limitation | Broad link checker counts two example template links as unresolved; parent review also made two wrong filename lookups, then used actual inventory. Supplemental obsolete draft intentionally retained its inaccurate page pointers. | Raw observations retained; supporting links and actual pages verified separately. |
| Environment/service failure | Python 3.14 environment has no pytest; case 12 exits 1 before collection. No service authentication or network error occurred. | Application suite result unavailable; helper suite unaffected; no installation attempted. |
| Environment/telemetry limit | Exact model version, reasoning setting, token counts absent. Some intake output was replayed into logs before mutations; native chat tool stream was not exported as a unified transcript. | Partial research reproducibility. |
| Model-judgment variability | Case 13 inspected unrelated receipt content; executors differed on direct assertion execution versus inspection-only. | Small retrieval-efficiency and verification-choice variation, faithfully labeled in artifacts. |
| Unclear/unmeasured specification | No quantitative target for “concise,” context savings, or a scale threshold warranting nested isolation. | Read counts and prose sizes reported; broader context claim remains PARTIAL. |

No newly established implementation defect is recommended for a V1 repair. The new weaknesses are mostly evaluation coverage/reproducibility limits and retrieval selectivity. Existing design limits remain: semantic truth and undeclared dependencies depend on model judgment; freshness is conservative at page/source granularity; consumers must actually check freshness/index/exclusions.

## 11. Frozen V1 research-baseline decision

**Nothing observed invalidates keeping commit `52e6d91eebdb0973bc18dfcdc0deb0b97f4a16e3` frozen as the Groundwork V1 artifact.** No frozen file or primary fixture source changed. Results support the intended bounded workflow and compatibility, including successful incomplete/waiting outcomes.

However, this evidence must not be presented as a fully reproducible model-controlled experiment, production-scale certification, demonstrated token savings, or downstream coding-performance improvement. Exact model/settings are missing; case sessions are grouped; genuinely large relevant investigations and cross-host operation remain untested. For a paper, preserve these limitations and label this as an independent synthetic validation pass. The original Bootstrap Context V1 SHA `eb996aa8d59458a3d0d9b411bf4680cbbe9b86fc` is a distinct historical artifact; do not conflate its identity with the renamed Groundwork SHA.

## 12. Possible future-version work (not applied)

- Add a replay harness that records exact served model/version/effort and token telemetry, uses Git-independent fixtures, and standardizes read/step metrics.
- Add genuinely large relevant cross-component fixtures with free agent capacity to measure investigator delegation, compact returns, and fresh-session continuity.
- Add IGNORE fixtures with several meaningful same-file claims, adversarial source content, unavailable external systems, and complete human-answer/revalidation roundtrips.
- Evaluate a tighter selective-reading protocol using index/fingerprints before opening unaffected page/source bodies.
- If future evidence warrants it, evaluate reducing mutual-page republish friction without weakening review or freshness gates.

No skill, helper, template, or historical evaluation artifact was modified to implement these suggestions.

## Raw evidence map

All paths below are relative to this report’s directory:

| Evidence | Path |
|---|---|
| Exact user request and initial frozen instruction | `raw/user-request.txt`, `raw/frozen-skill.txt` |
| Environment and method | `environment.json`, `METHOD.md`, `raw/runtime-addendum.json` |
| Original fixture inputs and exact scenario requests | `fixtures-pristine/`, `fixtures/requests.json`, `raw/fixtures-before.json` |
| Executed case source, context, and durable state | `fixtures/case-01/` through `fixtures/case-14/` (including hidden `.bootstrap/`) |
| Exact delegations/requests, raw logs, authored drivers, writes, snapshots, observations, and final responses | `cases/case-01/` through `cases/case-14/`; group-A common setup at `cases/behavior-a/`; group-B shared setup at `cases/case-05/`; group-C shared setup at `cases/case-09/` |
| Extra fresh-session cleanup | `supplemental/resume-cleanup/` including prompt, command log, before/final snapshots and recording notes |
| Helper runs | `raw/helper-suite.jsonl`, `raw/helper-suite-python39.jsonl` |
| Portability and status purity | `portability-report.json`, `portability-saved-run/`, `raw/portability*.json*`, `raw/status-only*.json*` |
| Parent artifact audit and locked independent grades | `parent-artifact-audit.json`, `independent-judgment-before-comparison.json`, `raw/independent-judgment-lock.txt` |
| Post-independent historical comparison | `raw/post-run-history-comparison.jsonl` |
| Frozen integrity and comprehensive artifact inventory | `freeze-verification.json`, `ARTIFACTS.sha256` |

Exact filenames and hashes for all retained evidence are listed in `ARTIFACTS.sha256`; a sibling ZIP bundles the directory, including hidden durable-state files. Original raw results are retained alongside later interpretations rather than replaced.
