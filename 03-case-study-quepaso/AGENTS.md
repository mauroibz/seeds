# AGENTS.md — Operating Manual for QuePaso

You are an autonomous coding agent working on **QuePaso** (quepaso.com.ar): a map of
geo-anchored public threads called **pins**, launching in Rosario, Argentina. The owner
(Mauro) is not a web developer and is not watching in real time. This file tells you how
to work; the `docs/` set tells you what to build.

**Default instruction, unless told otherwise: complete the next milestone, then stop and
report.**

## 1. Orientation — read in this order at session start

1. `docs/implementation-guide.md` — find the **first unchecked sprint** in the Progress
   tracker. That sprint is your milestone.
2. `docs/worklog.md` (if it exists) — read the last entry: where the previous session
   stopped, deviations, warnings.
3. The spec sections referenced by your sprint (`docs/product-spec.md`,
   `docs/data-model.md`, `docs/architecture.md`).
4. `docs/decisions-log.md` — skim the settled tables so you don't relitigate them.
5. `git log --oneline -20` and `git status` — reconcile reality with the worklog.

Authority order when documents disagree: **migrations in `supabase/migrations/` >
data-model.md > product-spec.md/architecture.md > implementation-guide.md details**. If
you find a conflict, fix the lower-authority doc in the same commit and note it in the
worklog — never silently pick one.

## 2. What "a milestone" means

A milestone = one sprint from the implementation guide, done, which requires ALL of:

1. Every numbered step of the sprint is implemented.
2. **Every acceptance criterion is actually verified** — executed, not assumed. If a
   criterion says "verify with exiftool", run exiftool. If it says "in a second browser
   session", use a second (incognito/other-profile) session or a second test user.
3. Standing rules (implementation guide, bottom) checked — especially the **anonymity
   review**: no `author_id` from base tables can reach the client; every `profiles` join
   masked with the `is_anonymous` case (data-model.md §5).
4. Lint and build pass: `npm run lint && npm run build` in `web/`.
5. The Progress tracker checkbox is flipped, the worklog entry is written, and everything
   is committed.

Then **stop** and write the completion report (§7). Do not start the next sprint unless
your instructions explicitly say to continue past a milestone.

If a sprint is too large for one session, that's expected: work in committable increments,
keep the worklog current, and leave the tracker unchecked — the next session resumes from
your worklog entry.

## 3. Recording progress

Two artifacts, both mandatory:

**a) Progress tracker** (`docs/implementation-guide.md`): flip a sprint's checkbox only
when §2 is fully satisfied. Never flip it "optimistically".

**b) Work log** (`docs/worklog.md`): append-only journal. Create it on first use. One
entry per working session, newest at the bottom, format:

```markdown
## 2026-07-06 — Sprint 1 (in progress | MILESTONE COMPLETE)
- Done: steps 1–4; migrations 0001/0002 applied; seed loads 30 pins.
- Verified: bbox RPC returns dormant-last ordering (SQL checked); anon view leaks nothing.
- Deviations: renamed X because Y (docs updated in same commit).
- Blocked/open: none.
- Next: step 5 — pin clustering styles.
```

Record every deviation from the docs, every workaround, and anything the next agent would
otherwise have to rediscover. The worklog is for agents; keep it terse and factual.

## 4. Testing and verification

- Local stack must be running: `supabase start` (Docker), `supabase db reset` after any
  migration change, `npm run dev` in `web/`.
- Schema/RLS checks are done with SQL against local Postgres
  (`supabase status` gives the connection string; `psql` is available). Test RLS by
  setting the role/JWT claims, e.g. `set local role anon;` — verifying as `postgres`
  proves nothing.
- Anonymity checks are **blocking**: after any change to views, RPCs, or queries, verify
  as `anon` that `pins_public` / `comments_public` / `photos_public` return null author
  fields for anonymous rows, and that `photo_metadata` is unreadable.
- UI verification: exercise the real flow in a browser (headless is fine — Playwright).
  Verify mobile at 390 px width before calling a screen done.
- From Sprint 5 on, the Playwright smoke test must pass before any commit that touches
  covered flows.
- Never verify against the hosted/production Supabase project; all testing is local
  except the deployment checkpoints that the guide explicitly marks as hosted.

## 5. Git conventions

- Work directly on `main` until the app has real users (solo project, no PR reviewers).
- Commit small and often — one logical step per commit, always in a working state.
- Message format: `sprint-N: <imperative summary>` (e.g., `sprint-1: add pins schema and
  RLS policies`). Doc-only changes: `docs: <summary>`.
- Every commit that changes queries/views must mention the anonymity check in its body
  (one line: `anonymity: verified pins_public masks author`).
- Never commit secrets: `web/.env.local` stays gitignored; only the two
  `NEXT_PUBLIC_SUPABASE_*` vars exist, and the `service_role` key never appears in the
  repo or in Vercel.
- Do not push, deploy, or run destructive commands against hosted infrastructure unless
  the sprint step explicitly says so.

## 6. Guardrails — never do these

- **Never relitigate settled decisions** in `docs/decisions-log.md`. If implementation
  reveals a real problem with one, stop and write it up (§8) — don't diverge in code.
- **Never weaken the anonymity boundary**, even temporarily, even in debug code. The real
  author id of anonymous content must never leave Postgres (data-model.md §5).
- Never hand-edit the hosted database; schema changes go through
  `supabase/migrations/` only.
- Never put user-facing strings outside `lib/strings.ts`; UI copy is Spanish (es-AR),
  code/comments/docs are English. The entity is `pin` in code regardless of branding.
- Never install a paid service, create accounts, buy anything, or add a dependency that
  duplicates something already chosen in `docs/architecture.md` §1.
- Never delete or rewrite worklog history; it's append-only.
- Sprint 6 (production launch) requires the owner: domain registration (NIC.ar needs his
  CUIT/CUIL), Google OAuth console, Supabase/Vercel account actions. Prepare everything
  you can, then stop and hand him the exact steps.

## 7. Milestone completion report

When the milestone is done, end your session with a report the owner (a non-developer)
can read in one minute:

- What sprint was completed, in plain language ("people can now log in and publish a pin
  with photos").
- Each acceptance criterion and how it was verified (one line each).
- Deviations from the docs and why (link the worklog entry).
- Anything that needs the owner: accounts, keys, choices, money.
- What the next sprint will deliver, in one sentence.

## 8. When you're blocked or the docs are ambiguous

1. If it's a genuine product decision (affects data model, privacy, or user-visible
   behavior in a way the specs don't cover): add it to `docs/decisions-log.md` under
   Open questions with 2–3 concrete options and your recommendation, note it in the
   worklog, and — if you cannot proceed on any other step — stop and ask.
2. If it's an implementation detail: pick the simplest reversible option consistent with
   the specs, note it in the worklog, and keep moving.
3. If the environment is broken (Docker down, Supabase CLI failing): attempt to fix it
   yourself first; document what you tried in the worklog before stopping.
4. Nothing else to do and the milestone isn't reachable? Stop with a clear report of the
   blocker. A truthful "blocked on X" beats a checkbox that lies.

## 9. Environment quick reference

```bash
supabase start                      # local stack (Docker required)
supabase status                     # URLs + keys for web/.env.local
supabase db reset                   # re-apply migrations + seed.sql
supabase migration new <name>       # new migration file
cd web && npm run dev               # app on http://localhost:3000
cd web && npm run lint && npm run build
cd web && npm run e2e               # Playwright smoke (from Sprint 5). NOT `npx
                                    # playwright test` — npx pulls a different
                                    # version and fails with "test() … not
                                    # expected here". `npm run e2e` uses the
                                    # pinned local @playwright/test. Needs local
                                    # Supabase up; `supabase db reset` first if
                                    # prior-run rate limits bite.
```

Repo layout: `web/` (Next.js app) · `supabase/` (config, migrations, seed) ·
`docs/` (specs — keep them true) · `AGENTS.md` (this file).
