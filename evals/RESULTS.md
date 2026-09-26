# Evaluation results

Executed September 25, 2026. These are synthetic behavioral exercises and helper
regressions, not a claim of production correctness or cross-host certification.

## Behavioral suite

Three independent evaluating agents performed the actual user requests against
isolated temporary repositories. They received the skill, raw fixtures, and tasks,
not intended answers or proposed fixes. They wrote real context/state artifacts.
The parent reviewed their reports and representative product/engineering outputs.

All 14 required scenarios reached the appropriate outcome after recovery/refinement.
"Pass" includes deliberately remaining partial or waiting for human input.

| # | Scenario | Observed result |
|---|---|---|
| 1 | Stale docs versus current code | Historical v1 fee distinguished from current v2 ADR; no unnecessary human question. |
| 2 | Current docs/code contradiction | Disputed fee withheld; blocking question saved; no invented FIX/IGNORE. |
| 3 | Missing product context | Observed arithmetic published; rationale not invented; scope partial. |
| 4 | Hidden cross-component dependency | Deployment subscription connected event producer and warehouse consumer without a direct import. |
| 5 | Supported human answer | Answer validated against docs/code/test; GitHub identity recorded; linked baseline published. |
| 6 | Conflicting human answer | Conflict preserved; requested baseline rewrite withheld pending human decision. |
| 7 | Human chooses FIX | Open remediation recorded; code/tests unchanged; claim remains blocked. |
| 8 | Human chooses IGNORE | Exact claim excluded with source fingerprint/recheck trigger; independent code/test evidence used; rationale gap remains. |
| 9 | Fresh-session resume | Saved next action used, PB-012 allocated, no historical conversation required; obsolete checkpoint removed. |
| 10 | Large/noisy repository | 1,200 unrelated modules avoided; four relevant files inspected after narrowing the scan. |
| 11 | Incremental publication | Receipt published while conflicting fee stayed unpublished; durable question and final waiting status retained. |
| 12 | Behavior→implementation→verification | Product PB anchors linked to checkout/warehouse and dependency-based verification gaps. |
| 13 | Selective freshness | Changed checkout invalidated fee product/component only; receipt remained current; Markdown unchanged. |
| 14 | Responsibility/negative boundaries | Checkout/warehouse ownership, non-ownership and handoff captured; no runtime fulfillment guarantee invented. |

Reports are in `results/eval-1-4.json`, `eval-5-8.json`, and `eval-9-14.json`.
Saved final baseline/decision snapshots are in `results/case-XX/`; raw source fixtures
are reproducible via the generator. Cases 1, 5, 8 and 9 snapshots use the revised run.

## Failures, corrections, and reruns

- Initial helper suite: **20/21 passed**. A recursive watch missed a deeply nested
  new consumer. Replaced platform-dependent matching with anchored segment matching
  supporting `**` across zero or more directories. Regression now passes.
- Evaluators initially supplied absolute draft paths and invalidated unpublished
  IDs. Calls failed safely. Added explicit command guidance; new-fixture reruns of
  cases **1, 5, 8 and 9 had zero helper errors**.
- Coupled forward document dependencies initially left pages stale, and completion
  was correctly rejected. Explicit reviewed republishing recovered them. Documented
  that final pass; reruns applied it without failures. No trust flag bypass added.
- Artifact inspection found a scope could remain `needs revalidation` after all
  pages became current. The helper now returns it to `partial`, requiring the final
  model checkpoint to decide complete/waiting status. Added a regression; case 11's
  missing final checkpoint was recovered without changing its supported baseline.
- Restricted generated-context skipping to the root output directory so a nested
  `src/context/` package remains discoverable. Added a recursive-watch regression.
- Clarified cleanup ownership across sessions. Case 9's obsolete Bootstrap-owned
  checkpoint was removed; source/context bytes and all other files were unchanged.

Final helper suite: **23/23 passed on Python 3.14.2 and Python 3.9.6**. It covers
selective source/external/dependency invalidation, deletions, recursive watches,
publication blockers, linkage/verification requirements, fresh completion, lock and
schema protection, path traversal/symlinks, missing tracking, working-tree changes,
decision interruption recovery, and resumable IDs/checkpoints.

The bundled skill-creator `quick_validate.py` passed. Its own PyYAML dependency was
installed only into a temporary validation directory; the runtime has no packages.

## September 26 editorial revision

The skill was revised for plainer language and a clearer sequence. Evidence review
and human decisions now have separate references; product and engineering pages
have separate templates. The executable helper and saved-state schema are unchanged.

All **14 behavioral cases were executed again** against fresh fixtures by three
independent evaluating agents. All reached the appropriate supported, partial,
waiting, or revalidation outcome. No helper errors occurred. Initial evaluator
launches were interrupted by service authentication errors before execution;
the subsequent retry succeeded without user credential changes by this task.

One evaluator initially treated the JSON `allocate-pb` response as a bare ID. It
recovered the already reserved PB-012 without resetting state or losing continuity.
The command reference now states the JSON response shape explicitly. The existing
resume/ID regression also checks the parsed response.

The **23 helper tests passed again on Python 3.14**, the skill-creator validator
passed, both templates parsed, and instructional links resolved. The earlier
Python 3.9 compatibility results still apply to the byte-identical helper. Parent
review checked the reports and representative generated pages and decisions.

Reports and final artifacts for this revision are under `results/editorial/`.
These remain synthetic evaluations; the live Claude Code and production-scale
limitations below still apply.

## Reproduce

From the repository root:

```sh
python3 -m unittest discover -s evals -p 'test_*.py' -v
python3 evals/make_fixtures.py /tmp/bootstrap-context-new-eval
```

The generator refuses an existing destination. For behavioral evaluation, give a
fresh executing agent the skill path and an individual request from the generated
`requests.json`, with write access only to its case directory. Ask it to perform the
request, save actual artifacts, and record responses requiring human input rather
than asking real users. Evaluate evidence decisions and observable outputs against
the scenario criteria above; don't grade heading wording or count matching phrases.
Do not supply the result table to the executing agent before it performs the task.

## Remaining weaknesses

- These are two synthetic passes plus targeted reruns, not statistical evaluation across
  models or real brownfield projects. Cases 1–4, 5–8 and 9–14 shared evaluator sessions;
  the resume case started from persisted artifacts without its earlier conversation.
- No live Claude Code run, remote-system integration, or adversarial prompt suite.
- Model judgment still controls intent, materiality, evidence quality, dependency
  completeness, exclusions and completion. Structural checks cannot prove truth.
- Freshness covers declared sources/watches/dependencies. Undeclared edges can be
  missed; external changes require registered revisions or review-date expiry.
- Page-level invalidation is deliberately conservative. It can require reviewing
  unaffected claims on the same page; split independent content when useful.
- No background watcher or host wiring. Readers must run freshness and respect the
  generated index/exclusions; directly opening raw Markdown can bypass that contract.
- JSON-form YAML only; general YAML front matter is rejected. Symlink evidence is
  unsupported, scan exclusions are heuristic, and large watch sets require narrowing.
- No multi-parent collaboration, automatic migration, AST engine, app fixes, or test
  infrastructure implementation. Atomicity is per file with fail-closed recovery.
