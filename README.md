<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/seeds-logo-tagline-dark.svg">
    <img src="assets/seeds-logo-tagline.svg" alt="Seeds — for agentic builds" width="480">
  </picture>
</p>

Seeds is a lightweight operating method for projects carried by agents across many
sessions. It grew out of software development, but the loop applies to any agentic
project that can be divided into bounded outcomes and verified with evidence.

The loop is deliberately small — one pass, one milestone:

> Understand → decide → slice → build → verify → hand off

- **Understand** — a fresh agent rebuilds context from the repository — the handoff,
  the plan, the code — not from chat history.
- **Decide** — choices that are costly or hard to reverse reach the owner with options
  and a recommendation; reversible ones proceed autonomously and are recorded.
- **Slice** — cut the backlog to one bounded milestone: a measurable outcome with
  explicit deliverables and executable acceptance criteria.
- **Build** — implement that milestone and nothing else, in verifiable increments that
  keep every intermediate state green.
- **Verify** — prove it at the layer where the behavior can actually fail: the running
  application, the real database, never a mock of the thing claimed.
- **Hand off** — record the evidence and rewrite the handoff, so the next session
  starts from current reality, not archaeology.

Small loop, high leverage: nothing lives only in chat history, green means the thing
actually works, and any agent — in any session — picks up where the last one stopped.

## Start here

Give an agent one of these instructions.

**New project**

```text
Use Seeds (github.com/mauroibz/seeds) to set up this project from the following idea: …
```

**Existing project or workspace**

```text
Adopt Seeds (github.com/mauroibz/seeds) in this project. Reuse its existing conventions;
add only what is missing.
```

**Continue a Seeds project**

```text
Follow this repository's Seeds protocol and complete the next milestone.
```

**Evaluate on one milestone before adopting**

```text
Adopt Seeds in this project, then plan and execute one small milestone I actually
need. Stop and report after it.
```

Agents that support skills can install the self-contained [`seeds/`](seeds/) directory.
Otherwise, point the agent at [`seeds/SKILL.md`](seeds/SKILL.md); it contains the same
routing and links only to files inside that directory.

## Install per agent

The bundle is plain markdown — no CLI, no lock-in. Any of these works:

```text
npx skills add mauroibz/seeds
```

The [skills](https://skills.sh) CLI installs the bundle into Claude Code, Codex,
Cursor, OpenCode, Gemini CLI, Copilot, Windsurf, and 70+ other agents (project or
global scope, pick when prompted).

<details>
<summary>Manual install for a few common agents</summary>

```text
git clone https://github.com/mauroibz/seeds ~/.agent-skills/seeds
ln -s ~/.agent-skills/seeds/seeds  ~/.claude/skills/seeds        # Claude Code
ln -s ~/.agent-skills/seeds/seeds  ~/.codex/skills/seeds         # Codex
ln -s ~/.agent-skills/seeds/seeds  ~/.config/agents/skills/seeds # Amp / Replit / universal
ln -s ~/.agent-skills/seeds/seeds  ~/.hermes/skills/seeds        # Hermes Agent
```

Or simply commit the `seeds/` directory to the project (any agent that discovers
`skills/*/SKILL.md` picks it up), or paste the repo URL into the agent and say
"follow this repository's Seeds protocol".

</details>

A tool without a skills mechanism is not excluded: point it at `seeds/SKILL.md` in
its first prompt, and it operates the same loop from the same documents.

## What Seeds establishes

Seeds describes document **roles**, not a mandatory folder layout. On a new project it
normally creates these small artifacts; on an existing project it maps the roles onto
what is already there and adds only genuine gaps.

| Role | Default artifact | Purpose |
|---|---|---|
| Agent entrypoint | `AGENTS.md` | Reading order, completion rules, commands, and project invariants |
| Project truth | `docs/PROJECT.md` | Intent, non-goals, delivery shape, and important contracts |
| Delivery plan | `docs/PLAN.md` | Milestone index and the one active milestone |
| Decisions | `docs/DECISIONS.md` | Material choices, alternatives, and supersession history |
| Current handoff | `docs/HANDOFF.md` | Rewritable statement of what is true and what happens next |
| Session history | `docs/WORKLOG.md` | Append-only evidence, deviations, dead ends, and verification |

Larger projects may split technical specifications, runbooks, policies, or individual
milestones into separate files. Small projects should not create them by rote.

## The rules that matter

1. Establish explicit sources of truth.
2. Ask before costly or hard-to-reverse product, data, privacy, security, or service
   decisions; make simple reversible implementation choices autonomously.
3. Work on one bounded milestone at a time.
4. Give it externally verifiable acceptance criteria.
5. Verify real behavior at the correct layer. User-visible work requires a walkthrough;
   a mock of the thing being proved is not proof.
6. Reconcile the plan and canonical documentation, record what happened, and leave a
   clean handoff.

Read the full [`method`](seeds/references/method.md) for the reasoning and scaling rules.
The optional [`patterns`](seeds/references/patterns.md) are design heuristics learned
while using Seeds; they are not universal requirements. The short history of
[`why walkthroughs are required`](docs/why-walkthroughs.md) shows the failure that made
that gate load-bearing.

## Repository map

```text
seeds/
  SKILL.md                  adaptive entrypoint: bootstrap, adopt, or operate
  references/
    method.md               the durable methodology
    setup.md                greenfield and existing-repository setup procedure
    patterns.md             optional architecture heuristics
  assets/templates/         minimal artifacts an agent adapts rather than copies blindly
docs/
  why-walkthroughs.md       the failure that made real-flow verification non-negotiable
  faq.md                    answers to the predictable adoption questions
  index.html                tryseeds.dev — one-page companion site (GitHub Pages)
  assets/                   site styles, favicon, and social card
scripts/check_repo.py       internal-link and skill-package checks
```

## Example project

[`Akasha`](https://github.com/mauroibz/akasha) is a self-hosted personal library built
with this method across dozens of agent sessions. Its history includes the verification
failure that produced Seeds' walkthrough gate and shows how the method scales beyond an
initial project plan.

## License

The Seeds methodology, documentation, templates, and visual assets are licensed under
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
You may use, share, modify, and build on them for any purpose, including commercially,
provided you credit Seeds, link this repository and the license, and identify changes.
The small validation script is MIT licensed. See [`LICENSE`](LICENSE) for the attribution
format and complete scope.

The original QuePaso and Akasha artifacts remain available in Git history at commit
`0682db0`. They were removed from the default branch because historical evidence should
not dominate the reusable method.
