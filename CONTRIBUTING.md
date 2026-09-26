# Contributing

Small, focused improvements are welcome. Open an issue to describe a problem or
propose a new skill, or submit a pull request with the change and relevant checks.
Explain what users will be able to do and which hosts you actually tested.

## Where things live

| Area | Location |
|---|---|
| Groundwork instructions and implementation | [`groundwork/`](groundwork/) |
| Human installation and usage guide | [`groundwork/README.md`](groundwork/README.md) |
| Helper regression tests | [`evals/test_runtime.py`](evals/test_runtime.py) |
| Synthetic fixture generator | [`evals/make_fixtures.py`](evals/make_fixtures.py) |
| Development and independent evidence | [Research index](research/README.md) |
| Push and pull-request CI | [Helper tests workflow](.github/workflows/helper-tests.yml) |

`SKILL.md` is the agent instruction file. Keep user setup and explanations in the
human README. Do not treat a documentation change as a new behavioral evaluation.

## Checks

Python 3.9 or later is sufficient; the suite needs no installed packages:

```sh
python3 -m unittest discover -s evals -p 'test_*.py' -v
```

The GitHub Actions workflow runs this same suite on Ubuntu with Python 3.9 and
3.14 for pushes and pull requests. It tests the current checkout, uses read-only
repository permissions, and does not modify or rerun the frozen research record.
See [Actions](https://github.com/humpyreddyp/skills/actions/workflows/helper-tests.yml)
for actual run status; a green helper job is not a full behavioral evaluation.

For documentation changes, check relative links and instruction/resource paths.
For runtime changes, test the affected behavior and record new evaluation results
separately. Never overwrite a frozen result, move a frozen tag, or change a ZIP
that identifies an evaluated version. See the [research index](research/README.md)
before working with historical artifacts.

## Add a skill

Create a top-level folder named after the skill, using lowercase words and hyphens.
Include a focused `SKILL.md` with its name and description, a short human README,
and only the scripts, references, and assets it needs. Add a row to the root
catalog with installation guidance and an honest tested-host status. Put relevant
tests under `evals/`, keeping each skill's fixtures and results distinguishable.

## License decision

No license has been selected. Public visibility permits discovery and GitHub
forking, but does not itself provide a general license to reuse, modify, or
redistribute the contents. [GitHub explains the distinction](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).
The maintainer must choose before this repository claims open-source reuse rights.

- **MIT — recommended for simplicity:** short permissive terms, with copyright
  and license notices retained. See the [MIT terms](https://choosealicense.com/licenses/mit/).
- **Apache-2.0 — an alternative for explicit patent terms:** permissive terms
  with an express patent grant and additional notice requirements. See the
  [Apache-2.0 terms](https://choosealicense.com/licenses/apache-2.0/).

These are recommendations, not adopted terms. No LICENSE file has been added.

## Packaged downloads

Use GitHub Releases for future versioned skill ZIPs and checksums, associated with
the commit they package. [Release assets](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
keep downloads discoverable without accumulating binaries in the repository root.
Package the whole skill folder, including its human guide, references, templates,
and helper; exclude caches and evaluation fixtures.

The existing [`groundwork.zip`](groundwork.zip) contains the nine runtime files
from the independently evaluated Groundwork commit. [`bootstrap-context.zip`](bootstrap-context.zip)
preserves the earlier name. Neither ZIP includes the human guide added later.
Both are retained unchanged for reproducibility. No GitHub Release is created by
this repository-documentation change.

## Suggested repository metadata

Description: **Reusable skills for reliable AI-assisted software engineering.**

Topics: `agent-skills`, `software-engineering`, `ai-sdlc`, `coding-agents`,
`brownfield`, `codex`.

These are recommendations for the repository's About panel. Omit `claude-code`
until a live Groundwork test supports that association; its current status remains
documented as untested compatibility. Repository metadata is not changed by this
documentation update.
