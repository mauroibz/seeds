---
name: seeds
description: Set up a new project for long-running agent work, adapt an existing repository or workspace to the Seeds methodology without duplicating its conventions, or operate an already-adopted Seeds project one verified milestone at a time. Use when the user explicitly asks for Seeds, agent-ready project setup, durable multi-session workflow, or adoption of this methodology.
version: 1.0.0
---

# Seeds

Seeds makes work durable across agent sessions. It establishes sources of truth,
records material decisions, scopes one milestone at a time, requires executable evidence,
and leaves the next session a current handoff.

## Choose the mode

- **Bootstrap** — the project workspace is empty or the outcome is still a rough idea.
- **Adopt** — substantial work or project documentation already exists, but Seeds has not
  been established.
- **Operate** — the project already has a Seeds-style `AGENTS.md`, active milestone,
  decisions record, and handoff.

When bootstrapping or adopting, read [the method](references/method.md) and then
[the setup procedure](references/setup.md). Use only the templates needed from
`assets/templates/`.

When operating, follow the repository's own `AGENTS.md` and active milestone. Read the
method only if those instructions are incomplete or conflict about Seeds behavior.
Read [the optional patterns](references/patterns.md) only when making a related design
decision; none of them is a default requirement.

## Shared constraints

- Preserve the user's intent, scope, permissions, and existing project
  instructions. Seeds does not authorize unrelated work or code changes, external actions,
  deployment, pushing, spending, or destructive recovery.
- Treat the templates as roles and prompts, not a required taxonomy. Reuse an existing
  artifact that already performs a role; link to it rather than copying its contents.
- Do not silently decide product behavior, irreversible data changes, privacy/security
  boundaries, paid services, or architecture that would be expensive to reverse.
  Present concrete options and a recommendation when such a choice is genuinely needed.
- For reversible implementation details, choose the simplest option consistent with the
  project, verify it, and record material reasoning without blocking unnecessarily.
- Treat settled decisions as binding until the user or the recorded change protocol
  explicitly supersedes them. Do not relitigate or diverge from them silently.
- A milestone is complete only when every acceptance criterion has been executed and the
  required evidence exists. User-visible behavior requires a real walkthrough against
  realistic data. Never treat a mock of the unit or boundary being proved as proof.
- Preserve history. Decisions and worklogs are append-only; supersede or correct them
  with new entries. `HANDOFF.md` is intentionally rewritten because it represents only
  current reality.
- Stop after one milestone unless the user explicitly asks for broader continuation.
- Do not push, deploy, purchase, create external accounts, or perform destructive
  recovery unless the user's current request authorizes it.

If the request is only to set up or adopt Seeds, stop after the project is coherent
and report the resulting roles. If the request also includes implementation, finish the
adoption first and then execute the requested milestone under the new protocol.
