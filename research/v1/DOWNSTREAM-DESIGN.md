# Downstream experiment design — prepared, not run

Status: **design only**. No downstream coding run, baseline generation for a new
task, pilot, or scoring experiment has been executed under this plan. Bootstrap
V1 stays frozen at `eb996aa8d59458a3d0d9b411bf4680cbbe9b86fc`.

## Question and conditions

Does context produced by Bootstrap improve actual software changes, and does
explicit product context add value beyond engineering context?

| Condition | Available context |
|---|---|
| A | Repository only, including its original documentation. |
| B | Same repository plus engineering baseline. |
| C | Same repository plus the identical engineering baseline and product baseline. |

The primary contrast is **C minus B**. Secondary contrasts are B minus A and C
minus A. Use the same starting repository revision, change request, acceptance
criteria, model/reasoning configuration, tools, permissions, and resource budget
for every condition of a task. Every coding run gets a fresh checkout and session.

## Constructing a fair B versus C comparison

1. Pin each repository and source set. Produce a baseline with frozen V1 before
   exposing the generator to the target change request, hidden tests, or solution.
   Keep product and engineering generation costs and any human review separately.
   Retain the raw baseline and verify its freshness against the pinned revision.
2. Derive B and C from that **same** baseline. Do not generate two independent
   engineering baselines: quality differences would confound the comparison.
3. Make a documented, mechanical research projection of engineering pages that
   is byte-identical in B and C. Preserve technical content, behavior IDs, source
   references, verification gaps, and ownership boundaries. Convert hyperlinks
   to withheld product pages into plain behavior IDs in **both** conditions, so
   B has no broken-link navigation penalty. C's index additionally resolves IDs
   to product pages. Hash the projected engineering files to prove equality.
4. Supply a condition-specific, accurate navigation index; include only relevant
   engineering freshness/exclusion metadata in both B and C. C also receives the
   product pages and their relevant metadata. Hide raw `.bootstrap` discussions,
   questionnaires, full indexes, generator transcripts, evaluator reports, and
   working drafts from all coding runs. These can leak product content into B.
   Publish the projection rules and audit the bundles before randomization.
5. Engineering pages naturally contain some behavioral facts. Do not strip them
   until B becomes unusable. Record how much product intent is already present;
   interpret C–B as the value of **additional explicit product context**, not
   product knowledge versus no product knowledge. Report overlap by task.
6. For the primary study, derive baselines from sources available in the common
   repository to all three conditions. If baseline creation requires external
   documents or private human knowledge, either provide equivalent source access
   to every condition under a predeclared policy or put those tasks in a separate
   knowledge-transfer study. Otherwise information availability and organization
   are inseparable. Retain unsupported claims rather than silently repairing
   them after seeing coding outcomes.

This projection is a research packaging step, not a change to frozen skill files.
Test the projection on a separate pilot task. Do not run Bootstrap's publication
checker on intentionally product-free B and penalize it for required product links.
Archive a valid raw baseline, then separately validate bundle contents and hashes.

## Tasks and run protocol

Use held-out tasks on realistic repositories with independently verifiable
solutions. Include local behavior changes, cross-component/event/config changes,
changes with meaningful product invariants or non-ownership boundaries, and
negative-control tasks where product rationale is unlikely to help. Exclude the
14 development fixtures and near-duplicates from confirmatory conclusions.

A proposed feasibility pilot is six tasks × three conditions × two independent
replicates (36 runs). It is **not approved or started by this document**, and it
does not establish statistical power. Use separate pilot tasks to assess bundle
quality, grading reliability, budget adequacy, and outcome variance. Before a
confirmatory study, lock its held-out task set, sample size, replication count,
minimum worthwhile effect, budget, and analysis plan. Do not stop when results
look favorable or carry pilot tasks into confirmatory inference.

Block randomization by task and replicate; randomize condition order and record
the randomization seed. Keep model/provider version and reasoning setting fixed
within a comparison; treat a model change as a new block or study. Record sampling
settings and seeds where supported, without assuming seeds make execution exact.
No conversation, memory, filesystem, background agent, cache of answers, or final
patch may be shared between conditions. Disable globally installed skills and
automatic context that could reveal the other bundles; keep ordinary repository
agent instructions identical. Restrict tools to assigned sources and common
dependencies. Log deviations and accidental access.

Give every coding agent the same change request and neutral instruction to inspect
available context, implement the change, verify it, and explain assumptions and
affected behavior/dependencies. A common instruction may say an optional context
index is available when present; do not add special coaching only to B or C.
Set an equal total input/output/reasoning token allowance and wall-clock ceiling;
count supplied baseline context toward the coding budget. Record tool limits and
context-window size. Handle provider usage fields consistently; unknown is null.

Define a common human-answer protocol before execution: equal question allowance,
the same prerecorded answer for semantically equivalent questions, and an explicit
unknown response when no approved answer exists. Record question text, answer,
latency, and whether it was necessary. Blind the responder to condition where
practical. Do not reward fewer questions if the agent merely guesses incorrectly.
Alternatively use a no-answer arm, but do not mix interaction policies within the
primary comparison. Record use of human answers as a possible mediator of effects.

## Outcomes and scoring

Before agents run, an independent task author defines requirements, preserved
product invariants, affected dependency/impact sets, and a relevant test plan from
authoritative evidence. Bootstrap output is not the grading oracle. Pin hidden
acceptance/regression tests and verify they distinguish the starting behavior
from a valid solution. Graders should review patches and outputs without condition
labels or context bundle paths where feasible; record cases where blinding fails.

| Measure | Operational definition |
|---|---|
| Correctness — primary | Binary completion of the full preregistered acceptance rubric, supported by hidden tests and review; also retain per-requirement scores. |
| Product behavior preserved | Fraction of specified unchanged invariants preserved; report each violation and severity separately. |
| Dependencies identified | Precision/recall against the predeclared affected set, with an adjudication route for valid discoveries missing from the oracle. |
| Downstream impact recognized | Evidence-backed impacts explicitly identified; rubric per impact: 0 missed/incorrect, 1 named, 2 correctly explained and addressed or verified. |
| Verification selected | Relevance and coverage of proposed and executed checks, recorded separately; include command results and untested risks. |
| Regressions | Newly failing pinned checks or independently confirmed behavior failures relative to the starting checkout; do not count pre-existing failures as new. |
| Incorrect assumptions | Unsupported consequential assertions or decisions, classified by type/severity; do not count clearly labeled unknowns as confident errors. |
| Files/context inspected | Unique files and repeated reads, bytes or token estimates actually returned, baseline/source split, and truncated reads. Tool logs measure observed exposure, not comprehension. |
| Tokens and time | Input, output, cached, and reasoning usage when available; avoid double-counting nested provider totals. Record wall time and unavailable fields. |
| Human questions | Count, necessity/quality, answer availability, and resulting delays or unresolved blockers. |

Use two independent reviewers for subjective product/impact/assumption judgments
on a predeclared portion (ideally all pilot runs); record agreement and resolve
disagreements before condition labels are revealed. Retain patches, tests, logs,
questions, negative results, and all reruns. Do not use an uncalibrated model judge
as the only correctness or product-preservation assessor.

Report coding cost and baseline creation/review/maintenance cost separately.
Provide both first-task total cost and amortized cost across a declared number
of changes using the same baseline. A coding-token reduction alone does not show
that total cost fell. Equal-budget results test usefulness under that budget;
an additional budget-matched sensitivity study must be labeled separately.

## Analysis, failures, and interpretation

Analyze matched within-task differences, with C–B first. Treat tasks/repositories
as the units of generalization; repeated agent runs are nested observations, not
independent tasks. Report absolute success-rate differences, per-task outcomes,
uncertainty intervals using a predeclared task/cluster-aware method, and resource
distributions. Keep exploratory task-category/model interactions separate from
confirmatory findings. Preserve all conditions even when one performs poorly.

Set retry rules before execution. An infrastructure failure before any model task
work may be retried under the same assigned condition with a new attempt ID and
the failure retained. Coding errors, budget exhaustion, and unsuccessful solutions
are outcomes, not grounds for a clean replacement. Predetermine how missing runs
enter the primary analysis and report attrition by condition. Baseline preparation
failures must also be reported; distinguish conditional performance on prepared
bundles from end-to-end deployability.

A positive C–B result would support incremental value for explicit product context
on the sampled tasks, configurations, and packaging. It would not prove that all
Bootstrap claims are true, that this is the best possible baseline, or that all
models/projects benefit. A null result may reflect overlap, task choice, baseline
quality, budgets, or statistical uncertainty; do not automatically equate it with
no product-context value.

## Fresh-session checklist and run record

The next fresh evaluation session should:

1. Read the handoff and manifest; verify the frozen Git commit and nine file hashes.
2. Select the task/repository sample and evidence-access policy; freeze requests,
   independent oracles, tests, model settings, budget, and human-answer policy.
3. Prepare and audit A/B/C bundles, including identical B/C engineering hashes,
   no solution leakage, and condition isolation. Record preparation cost.
4. Finalize pilot or confirmatory scope and preregister randomization, stopping,
   scoring, retries, missing-data handling, and analysis before starting runs.
5. Only then execute the separately authorized study in fresh sessions and store
   results outside this V1 evidence archive. Never update V1 in response to results.

Each future run record needs study/task/repository IDs and revision; change-request
hash; V1 commit and generator/projection versions; A/B/C condition and bundle hashes;
replicate, randomization seed and order; host/model/provider/reasoning/sampling
settings; tools, budget and permissions; timestamps; human exchanges; complete
tool/usage records; final patch; acceptance/regression outputs; grader identities,
rubric version, scores and disagreements; deviations, failure class, attempt ID,
and links to every retry. Unavailable fields must be null with a reason.
