# Using the helper

Run `scripts/bootstrap.py` from this skill with Python 3.9 or later. It uses the standard library; Git is optional and supplies revision metadata. It does not need packages, network access, or model APIs.

Resolve the script path from the skill folder, not the target repo. For example:

```sh
python3 /path/to/bootstrap-context/scripts/bootstrap.py --repo /path/to/repo scan
```

Every path argument except `--repo` is relative to the repo, including `--draft`. The commands below show the part after `--repo /path/to/repo`.

Successful commands print JSON. For example, `allocate-pb` returns `{"behavior": "PB-001"}`; read the `behavior` field rather than treating the whole response as an ID.

## Find your starting point

| Command | What it does |
|---|---|
| `scan --limit 200` | Prints a bounded path inventory and category hints; does not read file contents or write files. |
| `scan --within src/checkout` | Narrows discovery to a directory. |
| `init --scope checkout` | Creates missing state or adds a scope; preserves earlier work. |
| `status` | Reports saved progress, questions, and freshness without changing files. |
| `freshness` | Checks sources, marks affected pages/scopes, and regenerates the index. |
| `allocate-pb` | Reserves the next stable behavior ID; the parent agent owns allocation. |

Scans skip common generated files, caches, dependencies, root context/state output, version-control metadata, binary outputs, and common secret filenames. The output includes counts, samples, a revision, and truncation information. It is a map for choosing where to investigate, not a complete architecture. Narrow incomplete scans before drawing conclusions about absence.

## Publish a reviewed page

Save the draft in `.bootstrap/runs/`, then publish it after reviewing its evidence:

```text
publish --draft .bootstrap/runs/checkout.md --to context/product/checkout.md
check
```

`publish` checks metadata, source availability and expiry, recorded blockers, and product links. `check` checks structure and links across pages. Neither command establishes that the content is true.

Publish product pages before the engineering pages that link to their behavior anchors. A forward or mutual dependency may leave the first page marked stale until both targets exist. Review the completed links, then republish the earlier page to capture its dependency. An unchanged page can be its own draft:

```text
publish --draft context/product/checkout.md --to context/product/checkout.md
freshness
```

Do not remove a real dependency or edit fingerprints to clear a warning. Resolve pending references before completing the scope. If a blocker covers only part of a proposed page, separate the independently supported content and record the affected IDs accurately. Never downgrade a blocker just to publish.

`index` rebuilds navigation without granting new trust. Editing published Markdown outside `publish` marks the page for review on the next freshness check.

## Save progress or mark changed context

```text
checkpoint --scope checkout --status partial --next "Trace the inventory handoff" --finding .bootstrap/runs/current.md
invalidate --ids CAP-checkout CMP-worker --reason "New requirements need review"
```

`checkpoint` saves the next action and optional finding path. Use `--status complete` only after reviewing the completion criteria; the helper also checks freshness, blockers, and product/engineering linkage.

`invalidate` accepts published document IDs and marks their dependents too. If new evidence concerns unpublished claims, update the saved question or finding directly. Model-authored questions, answers, and external records follow [state-format.md](state-format.md); after editing them, run `freshness` and `check`.

## Record an explicit human decision

FIX records remediation:

```text
decision --question Q-001 --choice FIX --statement "Fix the refund window" --action "Align the handler and tests with the agreed policy" --github-id owner
```

IGNORE records an exclusion:

```text
decision --question Q-001 --choice IGNORE --statement "Ignore the old refund limit" --source docs/refunds.md --claim "Refund window is 7 days" --rationale "This claim covers the retired policy" --recheck-when "The refund document changes" --github-id owner
```

Use the human's actual statement and target. These examples do not authorize either choice. `--github-id` is optional. For external evidence, use `--external ID` instead of `--source path`. Both commands leave the underlying question unresolved until its evidence has been checked.
