# Implementation Guide — {{PROJECT_NAME}}

[Reference: `03-case-study-quepaso/implementation-guide.md` for a fully worked example
of sprint breakdown and acceptance-criteria depth.]

**This is the primary working document.** It mirrors the flow of real development:
sprints in order, each with concrete steps, references to the other specs, and
acceptance criteria that must pass before moving on. It is written to be ingested by
LLM agents across many sessions. Agent operating rules (commits, work log, blocking
protocol) live in `../AGENTS.md`.

How to use in a session:
1. Find the first sprint whose acceptance criteria are not yet met (check the tracker
   below).
2. Re-read the referenced spec sections for that sprint.
3. Build, verify criteria, update the tracker checkboxes, commit.
4. Behavior questions → `product-spec.md`. Schema questions → `data-model.md`. Settled
   decisions → `decisions-log.md` (don't relitigate). New ambiguity → add to the
   decisions log's open list and, if it's genuinely blocking, ask the owner.

## Progress tracker

- [ ] Sprint 0 — Foundations
- [ ] Sprint 1 — Schema + read-only core view
- [ ] Sprint 2 — Auth + create flow
- [ ] Sprint 3 — Core interaction loop (the detail/thread surface)
- [ ] Sprint 4 — Discovery surface, profiles, search
- [ ] Sprint 5 — Moderation + hardening
- [ ] Sprint 6 — Production launch

[This ordering is a default, not a law — quepaso inserted extra polish sprints (B–F)
between 5 and 6 once real usage revealed UX gaps. Insert sprints as needed; never
renumber past sprints, just letter or number the new ones in sequence and note why in
the decisions log.]

---

## Sprint 0 — Foundations

**Goal:** running skeleton: framework scaffold + local backend + a deploy pipeline that
works, even if the app does nothing yet.

1. `git init`; commit the docs set and the initial brief.
2. Scaffold the frontend framework.
3. Install the base dependency set decided in `architecture.md`.
4. Stand up the backend locally (whatever "local dev" means for your chosen backend —
   Docker-based emulation, a local DB, etc.).
5. Create the client helper layer and the strings module (Phase 3 — ALL user-facing
   copy lives there from commit one, not retrofitted later).
6. App shell: nav, placeholder routes for every screen in the product spec's screens
   inventory.
7. Create the hosted backend project and the hosting provider project; deploy the
   skeleton. [If this genuinely requires owner accounts/credentials the agent can't
   have, say so here and mark it a hand-off step — see AGENTS.template.md §6.]

**Acceptance:** app runs locally against the local backend; deployed skeleton loads on
a real URL; nav works on the smallest target viewport; all copy renders from the
strings module (grep for hardcoded user-facing strings outside it — should find none).

---

## Sprint 1 — Schema + read-only core view

**Goal:** the full database exists; the primary screen shows seeded data.
*(Spec: product §[primary screen], data-model.md all.)*

1. Migration: every table from `data-model.md` §2.
2. Migration: triggers/functions, security boundary enforcement, read-only API surface.
3. Seed script: enough realistic fake data to make ranking/clustering/lifecycle
   behavior visible — not just 3 rows. Include variety in every dimension a later
   acceptance criterion will check (ages, states, anonymous vs. named, etc.).
4. Primary screen renders seeded data via the real read API — no hardcoded fixtures.
5. [Domain-specific: viewport/pagination loading, ranking-influenced ordering.]

**Acceptance:** [State the actual verifiable checks — e.g. "loading only fetches what
the current view needs, verified in the network tab"; "a security-boundary check as the
unprivileged role returns no leaked fields, verified by literally running the query as
that role, not as an admin/superuser."]

---

## Sprint 2 — Auth + create flow

**Goal:** a real user can log in and create the core content object.
*(Spec: product §3, §5.)*

1. Auth provider setup (local + hosted).
2. Auth-gate pattern: attempting a gated action while logged out should prompt login,
   not hide the action.
3. Create-flow composer, field by field per product-spec §5.
4. [Any UGC pipeline — upload, processing, metadata handling — per product-spec §9.]
5. Submit via the real write API; route to the new object's detail view on success.
6. Author affordances: edit window, delete, "posted as anonymous" badge if applicable.

**Acceptance:** end-to-end create flow completes on the smallest target viewport in a
reasonable time; any UGC processing claims (e.g. "metadata stripped") are verified with
a real tool against a real uploaded file, not assumed from reading the code; anonymous
content shows correctly masked in a second, independent session.

---

## Sprint 3 — Core interaction loop

**Goal:** the detail/thread surface — the product's actual heart.
*(Spec: product §6[, §6.1].)*

1. Detail view layout per product-spec §6.
2. Every "pile-on" interaction (comment/reply/like/react) wired to the real write API.
3. [If applicable: lifecycle/state UI — banners, visual decay, revival on interaction.]
4. Verify ranking behavior end to end: interactions should visibly change
   ordering/prioritization after a refetch, not just in theory.

**Acceptance:** a second account can interact and it's reflected for the first account
after refresh; anonymous interactions mask correctly to a second session; [if
applicable] a decayed/dormant object revives on a new interaction, verified in the
database directly, not just in the UI.

---

## Sprint 4 — Discovery surface, profiles, search

**Goal:** the secondary browsing surface and identity pages.
*(Spec: product §8, §11.)*

1. Discovery/feed surface: the ordering modes named in product-spec, real pagination.
2. Freshness strategy per architecture.md (polling/refetch-on-focus is a fine MVP
   default; don't build a real-time layer until product actually needs the latency).
3. Search/filter, if in scope.
4. Own-profile and public-profile pages — **re-verify the security boundary here**:
   a public profile must only ever surface content through the masked/public API
   surface, never the raw one, even for a user who has both public and protected
   content.
5. Empty states, everywhere, in the target language.

**Acceptance:** discovery surface paginates smoothly on the target device class; new
content from another session appears after refocus without a hard reload; a public
profile of a user with both public and protected content leaks nothing protected
(verify with a real mixed-content test user, not a synthetic all-public one).

---

## Sprint 5 — Moderation + hardening

**Goal:** the abuse baseline the product must not launch without.
*(Spec: product §10, `trust-and-safety-policy.md`.)*

1. Report/flag flow on every reportable content type.
2. Auto-hide threshold, if decided; admin queue with the actions from the policy doc.
3. Rate limits verified for every capped action.
4. Any private-metadata surface (e.g. retained EXIF) confirmed inaccessible to
   non-admins — write an actual test for this, not a code-review assumption.
5. Legal/footer basics: contact channel, policy page, any required disclosures.
6. A smoke test covering the full happy path: create → interact anonymously →
   like/react → report → admin action.

**Acceptance:** the smoke test passes; a non-admin hitting the admin surface is
rejected; every admin action is logged; the report → auto-hide → admin review →
restore cycle works end to end through the real UI, not just via direct API calls.

---

## Sprint 6 — Production launch

Follow `deployment-guide.md` end to end. Definition of done:

- Production URL live on the real domain, auth working on that domain (not just a
  preview/staging URL).
- Seed data replaced with real founder-created content — the product must not be
  empty on day one.
- Admin account provisioned and reachable from the device class an admin will actually
  use.
- Backups confirmed, error tracking receiving events, analytics counting.
- A runbook written during this sprint: how to moderate, how to restore a backup,
  known limits.

---

## Standing rules for all sprints

- **Security/trust-boundary review** on every change that touches a query, view, or
  API endpoint: restate the data-model.md §5 checklist here so it's unmissable.
- Schema changes only via migrations — never hand-edit a hosted database.
- All user-facing copy in the strings module; the entity is {{ENTITY_NAME}} in code
  regardless of any future brand rename.
- Verify each feature at the smallest target viewport before calling it done.
- Update the progress tracker and `decisions-log.md` as part of each sprint's final
  commit.
