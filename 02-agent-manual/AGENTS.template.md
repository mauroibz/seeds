# AGENTS.md — Operating Manual for {{PROJECT_NAME}}

[Reference: `03-case-study-quepaso/AGENTS.md` for the fully worked example this is
abstracted from. Fill in every {{PLACEHOLDER}}; delete bracketed notes as you go.]

You are an autonomous coding agent working on **{{PROJECT_NAME}}**: {{ONE_LINE_PITCH}}.
The owner ({{OWNER_NAME}}) {{IS_OR_ISNT}} a developer and is not watching in real time.
This file tells you how to work; the `docs/` set tells you what to build.

**Default instruction, unless told otherwise: complete the next milestone, then stop
and report.**

## 1. Orientation — read in this order at session start

1. `docs/implementation-guide.md` — find the **first unchecked sprint** in the Progress
   tracker. That sprint is your milestone.
2. `docs/worklog.md` (if it exists) — read the last entry: where the previous session
   stopped, deviations, warnings.
3. The spec sections referenced by your sprint (`docs/product-spec.md`,
   `docs/data-model.md`, `docs/architecture.md`).
4. `docs/decisions-log.md` — skim the settled tables so you don't relitigate them.
5. `git log --oneline -20` and `git status` — reconcile reality with the worklog.

Authority order when documents disagree: **{{SCHEMA_SOURCE_OF_TRUTH}} > data-model.md >
product-spec.md/architecture.md > implementation-guide.md details**. If you find a
conflict, fix the lower-authority doc in the same commit and note it in the worklog —
never silently pick one.

## 2. What "a milestone" means

A milestone = one sprint from the implementation guide, done, which requires ALL of:

1. Every numbered step of the sprint is implemented.
2. **Every acceptance criterion is actually verified** — executed, not assumed. If a
   criterion says "verify with {{TOOL}}", run {{TOOL}}. If it says "in a second browser
   session", use a second (incognito/other-profile) session or a second test user.
3. **If the sprint touches anything user-visible, the walkthrough gate in §4 is
   satisfied** — you ran the real flow against realistic data yourself and recorded what
   you saw, not just that the tests passed.
4. Standing rules (implementation guide, bottom) checked — especially the
   **security/trust-boundary review**: {{RESTATE_YOUR_ONE_SENTENCE_GUARANTEE}}
   (data-model.md §5).
5. Lint and build pass: {{LINT_AND_BUILD_COMMAND}}.
6. The Progress tracker checkbox is flipped, the worklog entry is written, and
   everything is committed.

Then **stop** and write the completion report (§7). Do not start the next sprint unless
your instructions explicitly say to continue past a milestone.

If a sprint is too large for one session, that's expected: work in committable
increments, keep the worklog current, and leave the tracker unchecked — the next
session resumes from your worklog entry.

## 3. Recording progress

Two artifacts, both mandatory:

**a) Progress tracker** (`docs/implementation-guide.md`): flip a sprint's checkbox only
when §2 is fully satisfied. Never flip it "optimistically".

**b) Work log** (`docs/worklog.md`): append-only journal. Create it on first use. One
entry per working session, newest at the bottom, format:

```markdown
## {{DATE}} — Sprint N (in progress | MILESTONE COMPLETE)
- Done: [steps completed; migrations/commits involved].
- Verified: [each acceptance criterion and how — be specific, not "looks good". For
  anything user-visible, this is the walkthrough gate: what flow you actually ran
  against what data, and what you observed — including anything that looked wrong but
  was out of scope].
- Deviations: [anything that diverged from the docs, and why; docs updated in the
  same commit].
- Blocked/open: [none, or what and why].
- Next: [the very next step, for whoever picks this up].
```

Record every deviation from the docs, every workaround, and anything the next agent
would otherwise have to rediscover. The worklog is for agents; keep it terse and
factual.

## 4. Testing and verification

- Local stack must be running: {{LOCAL_DEV_STARTUP_COMMANDS}}.
- {{SCHEMA_OR_ACCESS_CONTROL_TESTING_METHOD}} — test any trust boundary as the
  unprivileged role/user, not as an admin/superuser. Verifying as an all-powerful role
  proves nothing.
- Security/trust-boundary checks are **blocking**: after any change to a query, view,
  endpoint, or access-control rule, verify as the least-privileged caller that
  sensitive fields are actually masked/inaccessible.
- **Walkthrough gate**: a sprint that changes user-visible behavior is not done because
  its tests are green. Passing tests prove the code does what the test asserts, not that
  the flow works — a test can mock exactly the boundary that's actually broken and stay
  green forever. Before calling the sprint done, run the real application against
  realistic data and perform the actual user flow yourself, then record in the worklog
  entry what you did and what you observed — including anything that looked wrong but
  was out of scope for this sprint. An issue noticed and left unrecorded is the failure
  this gate exists to catch. Verify the smallest target viewport.
- A test that substitutes a mock for the exact unit or boundary an acceptance criterion
  is about does not satisfy that criterion. Mock the transport, the clock, the
  filesystem, an external API at its edge — never the thing you're claiming to have
  verified.
- From {{SPRINT_WHERE_E2E_STARTS}} on, the end-to-end smoke test must pass before any
  commit that touches covered flows.
- **Never verify against the hosted/production environment**; all testing is local (or
  a disposable staging environment) except the deployment checkpoints the guide
  explicitly marks as hosted.

## 5. Git conventions

- {{BRANCHING_POLICY — e.g. "work directly on main until there are real users"}}.
- Commit small and often — one logical step per commit, always in a working state.
- Message format: `sprint-N: <imperative summary>` (e.g., `sprint-1: add core schema
  and access rules`). Doc-only changes: `docs: <summary>`.
- Every commit that changes queries/views/endpoints must mention the security-boundary
  check in its body (one line, e.g. `boundary-check: verified X masks Y for anon role`).
- Never commit secrets: `.env.local`-equivalents stay gitignored; the one admin/service
  key never appears in the repo or in the hosting provider's env config.
- Do not push, deploy, or run destructive commands against hosted infrastructure unless
  the sprint step explicitly says so.

## 6. Guardrails — never do these

- **Never relitigate settled decisions** in `docs/decisions-log.md`. If implementation
  reveals a real problem with one, stop and write it up (§8) — don't diverge in code.
- **Never weaken the trust/security boundary**, even temporarily, even in debug code.
  {{RESTATE_YOUR_ONE_SENTENCE_GUARANTEE}} (data-model.md §5).
- Never hand-edit the hosted database/backend state; changes go through
  {{MIGRATION_MECHANISM}} only.
- Never put user-facing strings outside the strings module; the core entity is
  {{ENTITY_NAME}} in code regardless of branding.
- Never install a paid service, create accounts, buy anything, or add a dependency that
  duplicates something already chosen in `docs/architecture.md` §1.
- Never delete or rewrite worklog history; it's append-only.
- {{ANY_SPRINT_THAT_REQUIRES_THE_OWNER}} (domain registration, OAuth console setup,
  account actions requiring real-world identity/payment) requires the owner. Prepare
  everything you can, then stop and hand over the exact remaining steps.

## 7. Milestone completion report

When the milestone is done, end your session with a report the owner
({{OWNER_TECHNICAL_LEVEL}}) can read in one minute:

- What sprint was completed, in plain language.
- Each acceptance criterion and how it was verified (one line each).
- Deviations from the docs and why (link the worklog entry).
- Anything that needs the owner: accounts, keys, choices, money.
- What the next sprint will deliver, in one sentence.

## 8. When you're blocked or the docs are ambiguous

1. If it's a genuine product decision (affects data model, privacy, or user-visible
   behavior in a way the specs don't cover): add it to `docs/decisions-log.md` under
   Open questions with 2–3 concrete options and your recommendation, note it in the
   worklog, and — if you cannot proceed on any other step — stop and ask.
2. If it's an implementation detail: pick the simplest reversible option consistent
   with the specs, note it in the worklog, and keep moving.
3. If the environment is broken: attempt to fix it yourself first; document what you
   tried in the worklog before stopping.
4. Nothing else to do and the milestone isn't reachable? Stop with a clear report of
   the blocker. A truthful "blocked on X" beats a checkbox that lies.

## 9. Environment quick reference

```bash
{{COMMAND_CHEATSHEET — local stack start/reset, dev server, lint/build, e2e run,
including any gotchas a fresh agent would otherwise waste a session rediscovering}}
```

Repo layout: {{REPO_LAYOUT_ONE_LINE}}.
