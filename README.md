# Skills

## Groundwork

[Groundwork](groundwork/SKILL.md) builds or resumes a product and engineering
baseline for an existing repository. It investigates evidence, records unresolved
questions and human decisions, and publishes linked context for future changes.
It does not modify application code.

The portable skill is in [`groundwork/`](groundwork/), with a packaged copy in
[`groundwork.zip`](groundwork.zip). Its name and invocation are `groundwork` and
`$groundwork`. The Python helper requires Python 3.9 or later and no packages.

Groundwork is the renamed Bootstrap Context skill. The rename changes its folder,
skill identity, displayed name, and prose references. The executable helper remains
byte-identical: `scripts/bootstrap.py`, `.bootstrap/` state, and the saved-state
schema retain their existing names and behavior for compatibility.

## Frozen research baseline

Bootstrap Context V1 / v0.1 is preserved at Git tag `bootstrap-context-v0.1`, commit
`eb996aa8d59458a3d0d9b411bf4680cbbe9b86fc`. Tag
`bootstrap-context-v0.1-research` includes the accompanying research documents.
Those tags retain the original `bootstrap-context/` directory and evaluation code.
The historical [`bootstrap-context.zip`](bootstrap-context.zip) also remains intact.

- [Research handoff](research/v1/HANDOFF.md)
- [Experiment manifest](research/v1/experiment-manifest.json)
- [Behavioral evidence, development failures, and reruns](evals/RESULTS.md)
- [Prepared downstream experiment design](research/v1/DOWNSTREAM-DESIGN.md)
- [Groundwork rename provenance and validation](research/groundwork-rename.json)

Historical paths, names, hashes, and reports are intentionally unchanged. To
reproduce the original V1 exactly, check out its research tag in a separate clone;
the frozen evidence index describes that revision, not the renamed working tree.
The Groundwork rename has helper and structural validation but no new behavioral
evaluation. No downstream coding-performance experiment has been run.

## Current helper checks

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s evals -p 'test_*.py' -v
```

To prepare fresh synthetic fixtures without executing any model evaluation:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 evals/make_fixtures.py /tmp/groundwork-new-eval
```

The fixture destination must not already exist. Historical research tools under
`research/v1/` belong to the frozen revision; use its tag when replaying them.
