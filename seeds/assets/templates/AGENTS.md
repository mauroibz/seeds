# Agent operating contract for [PROJECT]

[Replace every bracketed instruction. Keep this file short; link to detail instead of
copying it here.]

Default instruction: complete exactly one active milestone, then stop and report unless
the user explicitly asks for more.

## Establish context

1. Run `[STATUS COMMAND]` and inspect recent history.
2. Read, in order:
   - this file;
   - `[CURRENT HANDOFF]`;
   - `[PLAN OR ACTIVE-MILESTONE POINTER]` and the active milestone;
   - only the canonical sections and decisions named by that milestone;
   - the latest relevant entry in `[WORKLOG]`.
3. Inspect the source material, existing work, and checks named by the milestone. Do not
   rely on a prior summary in place of current evidence.
4. Reconcile unexplained workspace or version-control changes before editing. Preserve
   user and prior-agent work; never discard unknown changes.

## Execute the milestone

- Stay within its objective, acceptance criteria, and explicit non-scope.
- Work in coherent, verifiable increments using the repository's established conventions.
- Use test-first development when behavior can be specified before implementation and
  measurement-first work when the milestone exists to answer an uncertain question.
- A bounded prerequisite repair is allowed when necessary; record it. Do not pull future
  scope forward for convenience.
- Treat settled decisions as binding until explicitly superseded. If implementation
  exposes a real conflict, document the evidence and follow the change protocol instead
  of silently diverging.
- Never weaken, skip, delete, or mark flaky a test merely to obtain a green result. Never
  fabricate verification output.
- If commits are part of repository policy, commit coherent working increments. Do not
  rewrite prior-session commits or push unless the user asks.

## Verify

- Run every check named by the active milestone plus `[PROJECT-WIDE CHECK COMMANDS]`.
- Every acceptance criterion must be executed at a layer capable of observing the claim.
  A mock of the exact unit or boundary under examination is not proof.
- Test access/security boundaries as `[LEAST-PRIVILEGED RELEVANT CALLER]`.
- User-visible changes require the walkthrough gate: run the application against
  realistic data, perform the real flow, and record what happened and anything that
  looked wrong. Passing automated tests alone is insufficient.
- A required check that cannot run must be recorded as `NOT RUN` with the reason and
  normally leaves the milestone incomplete.

## Reconcile and hand off

Before completion:

1. Update canonical documentation for changed behavior or contracts.
2. Append material choices and deviations to `[DECISIONS]`; never rewrite history.
3. Record delivered behavior and concise evidence in the milestone outcome.
4. Review future milestones for affected assumptions.
5. Append `[WORKLOG]` and rewrite `[HANDOFF]` as current reality and the exact next step.
6. Advance the milestone pointer only after verification passes.
7. Run final checks and leave the worktree `[REQUIRED END STATE]`.

Then report: what completed, how each criterion was verified, deviations, anything that
needs the user, and what comes next.

## Authority by concern

| Concern | Authority |
|---|---|
| Product behavior and scope | `[PROJECT OR PRODUCT SPEC]` |
| Technical contracts | `[TECHNICAL SOURCES]` |
| Applied schema | `[MIGRATIONS OR N/A]` |
| Current scope | `[ACTIVE MILESTONE]` |
| Resume state | `[HANDOFF]` |
| Historical rationale | `[DECISIONS, WORKLOG, OUTCOMES]` |

Produced work, sources, and checks show actual reality; they do not silently override
intended behavior. Resolve conflicts at the appropriate authority and record material
changes.

## Clarification and blockers

Ask before decisions that materially change user-visible behavior, irreversible data,
deletion/overwrite semantics, privacy/security exposure, paid services, or expensive
architecture. Offer concrete options and a recommendation. For reversible implementation
details, choose the simplest compatible option, verify it, and record material reasoning.

If interrupted or blocked, preserve coherent work, append the worklog, update the handoff
with exact evidence and next action, and do not advance the milestone.

## Project invariants and commands

- [Concrete project-specific invariant and the check that protects it.]
- [Destructive/external actions that require the user.]
- [Secrets, generated files, migrations, or deployment rules.]

```text
[Install, development, focused-test, full-test, lint/type/build, walkthrough, and any
environment-recovery commands a fresh agent genuinely needs.]
```
