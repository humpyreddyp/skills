# Research index

For installation and everyday use, start with the [skill catalog](../README.md)
or [Groundwork guide](../groundwork/README.md). This index is for inspecting what
was evaluated, reproducing a particular version, and planning further research.

## Groundwork V1 / v0.1

The independently evaluated Groundwork artifact is commit
[`52e6d91eebdb0973bc18dfcdc0deb0b97f4a16e3`](https://github.com/humpyreddyp/skills/commit/52e6d91eebdb0973bc18dfcdc0deb0b97f4a16e3).
The nine runtime files remain unchanged in the current source. The human README,
public navigation, and CI are later repository additions, not part of that evaluation.

| Record | What it contains |
|---|---|
| [Independent report](groundwork/v0.1/independent-eval/2026-09-26-frozen-v1/REPORT.md) | 14 bounded behavioral scenarios, helper results on two Python versions, supplemental checks, partial findings, failures, and limitations. |
| [Method and environment](groundwork/v0.1/independent-eval/2026-09-26-frozen-v1/METHOD.md) | Independence procedure, session grouping, provenance, and reproduction limits. |
| [Preserved evidence](groundwork/v0.1/independent-eval/) | Original directory, ZIP, raw logs, generated artifacts, and intermediate states. |
| [Preservation receipt](groundwork/v0.1/independent-eval/PRESERVATION.json) | Source/copy inventory, SHA-256 hashes, and copy-verification results. |
| [Rename provenance](groundwork-rename.json) | Naming changes from Bootstrap Context to Groundwork and unchanged-helper verification. |

The independent report supports keeping this artifact as a research baseline.
Its broader context-management assessment is partial, and exact model settings
were unavailable. Passing these scenarios does **not** demonstrate that Groundwork
improves downstream coding-agent performance.

## Earlier development history

These records retain the original Bootstrap Context name, paths, and conclusions.
They describe the versions at which they were written; do not reinterpret them as
new results for the current checkout.

| Record | Version or purpose |
|---|---|
| [`bootstrap-context-v0.1`](https://github.com/humpyreddyp/skills/tree/bootstrap-context-v0.1) | Original frozen source/evidence commit `eb996aa8d59458a3d0d9b411bf4680cbbe9b86fc`. |
| [`bootstrap-context-v0.1-research`](https://github.com/humpyreddyp/skills/tree/bootstrap-context-v0.1-research) | Original research packet at `ced0ddb086520288ce99f6dcfa119b43af22e2cf`. |
| [Handoff](v1/HANDOFF.md) and [experiment manifest](v1/experiment-manifest.json) | Original scope, methodology, version hashes, outcomes, and limitations. |
| [Development results](../evals/RESULTS.md) and [raw records](../evals/results/) | Earlier failures, corrections, reruns, and generated cases. |
| [Design notes](../DESIGN.md) and [implementation report](../REPORT.md) | Historical design and development documents retained at their original paths. |

## Reproduce or extend the research

For exact independent-evaluation inputs, use a separate checkout of the Groundwork
commit above. For original Bootstrap Context paths and tools, use the corresponding
historical tag. Keep new outputs in a new result location and record the revision,
environment, model/settings when available, prompts, and all failed attempts.

The [next-stage experiment design](v1/DOWNSTREAM-DESIGN.md) proposes repository-only,
engineering-context, and product-plus-engineering-context conditions. That design
is **not an executed downstream study**. Preserve it as the original proposal;
record any later protocol changes separately.

The source and evidence stay at their existing paths so historical references,
checksums, and ZIPs remain useful. Current CI evaluates the current helper only;
it does not replace or amend any frozen evaluation.
