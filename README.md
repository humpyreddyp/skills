# Skills

A growing public collection of reusable skills for AI-assisted software engineering.

These skills give a coding agent a repeatable way to understand software, work
through decisions, and leave useful context for the next change. Start with a
skill below, install it in your agent, and use it in the repository you work on.

## Skill catalog

| Skill | What it does | Status |
|---|---|---|
| [Groundwork](groundwork/README.md) | Builds an evidence-grounded product and engineering baseline for an existing software system. | V0.1 |

## Start with Groundwork

Use Groundwork before changing an unfamiliar codebase, when product intent and
implementation disagree, or when another agent needs to pick up an investigation.
It connects what the system does and why with the code, dependencies, and checks
that matter. It records questions instead of inventing missing answers.

Groundwork writes context and investigation records; it does not change your
application code. You need Python 3.9 or later and an agent that can read and write
repository files and run local commands. Its helper has no package dependencies.

### Install in Codex

Ask Codex's built-in skill installer:

```text
$skill-installer Install the groundwork skill from https://github.com/humpyreddyp/skills/tree/main/groundwork
```

Then open the repository you want to understand and invoke it:

```text
$groundwork Build a baseline for checkout. Start with the repository's existing docs, code, and tests.
```

These are prompts to the agent, not terminal commands. If the skill does not appear,
restart Codex. See the [Groundwork guide](groundwork/README.md#installation) for
manual installation and Claude Code instructions. Codex installation conventions
are documented in [OpenAI's skills guide](https://learn.chatgpt.com/docs/build-skills).

### Tested hosts

Groundwork's behavior has been evaluated in **Codex desktop on macOS** using the
skill's explicit path. Codex CLI/IDE and Claude Code are intended compatibility
targets, but have **not been live-tested for Groundwork**. The documented install
and discovery flows have not been certified end to end. See the
[compatibility table](groundwork/README.md#compatibility) for the precise scope.

## Find your way

| You want to… | Start here |
|---|---|
| Install and use a skill | [Groundwork guide](groundwork/README.md) |
| Read the agent's instructions | [Groundwork source](groundwork/SKILL.md) |
| Propose a change or add a skill | [Contributing](CONTRIBUTING.md) |
| Run the helper tests | [Development checks](CONTRIBUTING.md#checks) |
| Inspect evidence, frozen versions, or experiments | [Research index](research/README.md) |

## License and downloads

**A license has not been chosen yet.** The intent is public reuse, but making a
repository public does not itself grant general reuse, modification, or
redistribution rights. See [GitHub's licensing explanation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).
MIT and Apache-2.0 are [proposed options](CONTRIBUTING.md#license-decision); neither
has been adopted.

The current ZIPs remain available as historical artifacts. Use the source-folder
installation above for current documentation. Future packaged downloads should
use [GitHub Releases](https://github.com/humpyreddyp/skills/releases); no release
has been published yet. See [packaging guidance](CONTRIBUTING.md#packaged-downloads).
