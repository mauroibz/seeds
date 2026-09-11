# Setting up Seeds

Use this procedure only for **bootstrap** or **adopt** mode. Read
[`method.md`](method.md) first.

## Bootstrap a new project

1. Turn the user's idea into a compact brief covering purpose, users, success, scope,
   non-goals, constraints, fixed choices, delegated choices, and open questions.
2. Surface only consequential unknowns: user-visible semantics, irreversible data model,
   privacy/security exposure, destructive behavior, paid services, and expensive
   architecture. Offer concrete alternatives and a recommendation.
3. Confirm the brief with the user before treating it as product intent. Fold the agreed
   content into the project source of truth; do not keep two competing documents.
4. Record settled material choices immediately, including alternatives considered.
5. Choose stable internal vocabulary where renaming would be expensive. Record the rule;
   do not impose a particular strings or localization architecture unless appropriate.
6. Create the smallest useful milestone plan. Detail the first milestone fully and leave
   future milestones as outcome contracts.
7. Create a short project-specific agent entrypoint with actual commands, document roles,
   completion gates, and concrete invariants.
8. Initialize current handoff and append-only worklog. Verify all referenced paths and
   commands that can safely be checked before reporting setup complete.

Use the files under `../assets/templates/` as prompts. Omit irrelevant sections and split
a document only when separate authority or size justifies it.

## Adopt Seeds in an existing repository

Adoption is a mapping exercise, not a rewrite.

1. Inspect before editing:
   - all applicable `AGENTS.md` or equivalent agent instructions;
   - README and contributor documentation;
   - briefs, product/architecture material, source indexes, decisions, plans, issues, and
     operating guides;
   - production tools, validation commands, automation, data inputs, and delivery setup;
   - current branch, worktree status, and recent history.
2. Classify existing artifacts by role and status: canonical, historical, or proposal.
   Determine authority separately for product intent, technical contracts, schema,
   milestone scope, current state, and history.
3. Identify only real gaps:
   - no reliable agent entrypoint or reading order;
   - product intent or non-goals cannot be found;
   - no bounded active milestone with verifiable criteria;
   - material decisions are repeatedly rediscovered;
   - no durable session history or current handoff;
   - verification proves implementation units but cannot observe real flows.
4. Reuse existing filenames and systems. An issue tracker can be the plan; ADRs or a
   decision journal can be the decisions record; an operating guide can own commands.
   Add links from the agent entrypoint instead of cloning content into Seeds-shaped files.
5. Preserve stronger project rules, nested instruction scopes, and established versioning
   conventions. Do not reorganize working material, rename internal concepts, or rewrite
   useful documentation merely to resemble a template.
6. Resolve unambiguous documentation inconsistencies. Ask before choosing among materially
   different product, data, privacy, security, paid-service, or irreversible options.
7. Establish one active milestone. If the user also requested implementation, express that
   request as the milestone and execute it after adoption; otherwise stop after the
   adoption documents and checks are coherent.
8. Validate links and commands, record the adoption decision, write the first handoff and
   worklog entry, and report which existing artifacts satisfy each Seeds role.

## Target shape

For a small repository with no equivalents, use:

```text
AGENTS.md
docs/
  PROJECT.md
  PLAN.md
  DECISIONS.md
  HANDOFF.md
  WORKLOG.md
```

Add individual milestone files, technical specs, safety policies, runbooks, or generated
state only when the project needs them. Fewer truthful documents are better than a full
template set that immediately drifts.
