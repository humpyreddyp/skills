# Groundwork

Understand an existing system before changing it.

Groundwork helps an AI agent build a small, evidence-grounded account of what a
capability does, why it exists, where it is implemented, and what a change might
affect. It gives people and later agents a shared starting point when knowledge
is scattered across code, tests, documents, and conversations.

This is the human guide. [SKILL.md](SKILL.md) contains the agent's instructions.

## When to use it

- You are taking over an unfamiliar repository or preparing a substantial change.
- Documentation, implementation, or stakeholder recollections disagree.
- You need to understand dependencies and ownership across components.
- An investigation must continue in a later session without its full chat history.
- Existing context may have become stale after source changes.

Start with one capability or flow, such as checkout or stock reservation. A useful
baseline can be built in pieces; the whole repository need not be understood first.

## Installation

You need Python 3.9 or later on the agent's execution machine, plus permission to
read repository files, write context, and run local commands. The helper uses only
the Python standard library. Groundwork itself needs no API key; your chosen
agent host has its own sign-in requirements.

The repository's [license decision is pending](../CONTRIBUTING.md#license-decision).
Public visibility alone does not grant general reuse rights.

### Codex

Ask the built-in installer:

```text
$skill-installer Install the groundwork skill from https://github.com/humpyreddyp/skills/tree/main/groundwork
```

For a manual user-level installation, run these commands in a macOS or Linux shell:

```sh
git clone https://github.com/humpyreddyp/skills.git humpy-skills
cd humpy-skills
mkdir -p "$HOME/.agents/skills"
test ! -e "$HOME/.agents/skills/groundwork" && cp -R groundwork "$HOME/.agents/skills/groundwork"
```

The copy stops if that destination already exists. Review an existing installation
before replacing it. For a project-scoped installation, copy the same `groundwork`
folder into the target repository's `.agents/skills/` instead. Install one copy per
intended scope to avoid duplicate skill names. If discovery does not refresh,
restart Codex. See [OpenAI's local skill locations](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

### Claude Code — designed for compatibility, not live-tested

From the cloned `humpy-skills` directory, install the complete folder:

```sh
mkdir -p "$HOME/.claude/skills"
test ! -e "$HOME/.claude/skills/groundwork" && cp -R groundwork "$HOME/.claude/skills/groundwork"
```

For a project-scoped installation, use `.claude/skills/groundwork/` inside the
target repository instead. Start Claude Code there and invoke `/groundwork`.
These locations and slash-command syntax follow the
[Claude Code skills documentation](https://code.claude.com/docs/en/skills).
No live Claude Code evaluation has been performed for Groundwork.

Copy the whole folder: references, templates, and the helper are needed alongside
`SKILL.md`. These shell examples do not establish Windows support.

## Use it

In Codex, select the installed skill or include its name in your prompt:

```text
$groundwork
```

Give a scope when you have one:

```text
$groundwork Baseline the checkout flow, including the handoff to inventory.
```

In Claude Code, the corresponding documented invocation is:

```text
/groundwork Baseline the checkout flow, including the handoff to inventory.
```

Helpful inputs include product requirements, diagrams, architecture decisions,
API or event contracts, runbooks, known stale areas, and the people who can answer
open questions. Bring what you have; missing inputs do not prevent investigation.

## What you get

| Location in the target repository | Purpose |
|---|---|
| `context/product/` | Supported behavior, product purpose, and boundaries. |
| `context/engineering/` | Implementation, dependencies, responsibilities, and verification expectations. |
| `context/index.yaml` | Navigation and the recorded freshness of published context. |
| `.bootstrap/` | Progress, questions, decisions, exclusions, and source tracking for later sessions. |

Product behavior is linked to implementation and verification using stable IDs.
Useful supported portions can be published while other claims remain unresolved.
Readers still need to respect freshness and exclusions: these artifacts are
reviewable conclusions, not a guarantee that every fact or dependency is known.

## Later sessions and human decisions

Use these as ordinary prompt text after invoking Groundwork. They are requests
interpreted by the agent, not formal CLI flags.

| Request | What Groundwork does |
|---|---|
| “Continue” | Resumes the saved next action. |
| “Resolve questions: here are my answers…” | Checks new answers against the evidence. |
| “Show status” | Reports saved progress without changing files. |
| “Revalidate checkout” | Checks changed sources and investigates affected context. |
| “Expand scope to refunds” | Adds a scope while keeping earlier work. |

Groundwork investigates before asking you about a material gap. Questions explain
what was found, why it matters, and which claims are affected. Non-blocking
questions can wait while supported work continues. Human answers are checked,
not accepted automatically as proof.

When a contradiction remains, you choose **FIX** or **IGNORE**. FIX records a
correction for someone to implement; Groundwork does not make the fix. IGNORE
excludes a specific source or claim, with a reason and a trigger for reconsidering
it. Neither decision makes the remaining claim true by itself.

Groundwork does not change application code, implement missing test infrastructure,
choose FIX/IGNORE for you, rewrite unrelated documents, or edit host instruction
files. It does not run a background watcher or automatically wire future agents
to read the baseline. Revalidate before relying on context after sources change.

## Compatibility

| Host or environment | Evidence |
|---|---|
| Codex desktop, macOS arm64 | Behavioral execution tested using an explicit skill path; 14/14 bounded scenarios passed in the independent V1 evaluation. This did not certify automatic discovery or the install flow. |
| Python helper on macOS | 23/23 regression tests passed on Python 3.9.6 and 3.14.2 in the independent evaluation. |
| Codex CLI and IDE extension | Designed for compatible local skill loading; Groundwork has not been live-tested in these hosts. |
| Claude Code | Portable skill structure and installation guidance only; not live-tested. |
| Other hosts and operating systems | No host-level compatibility claim. Helper CI results alone do not certify a host. |

Exact model version and reasoning settings were not exposed to the independent
evaluator. The cases test Groundwork's behavior; they do not prove improved
downstream coding performance. Read the [independent report](../research/groundwork/v0.1/independent-eval/2026-09-26-frozen-v1/REPORT.md)
for partial findings and limitations, or the [research index](../research/README.md)
for frozen versions. This human guide was added after the frozen V1 evaluation;
the nine runtime files are unchanged.
