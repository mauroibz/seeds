# Changelog

The Seeds method bundle is versioned in [`seeds/SKILL.md`](seeds/SKILL.md) frontmatter.
Adopters can compare their installed copy's version against this list.

## 1.2.1 — 2026-10-01

From a two-branch trial run.

- Parallel branches: the branch closes its milestone and lists in the outcome what the
  main line must change in shared files; the main line applies that list at merge.
- An interpretation awaiting owner confirmation is a pending decision and does not hold
  the milestone open.
- Append-only starts at merge; a branch extends shared tooling by adding files.

## 1.2.0 — 2026-10-01

Parallel work by several people, from external feedback.

- Parallel branches layout, used only when branches carry milestones at the same time:
  one milestone file per branch, resume state inside the milestone, no standalone
  handoff between deliveries, one file per worklog entry and per decision.
- `Branch` column in the plan index; handoff section in the milestone template.
- The method states where history lives; the handoff is never history.
- FAQ: history versus handoff, teams, and composing with OpenSpec.

## 1.1.0 — 2026-09-27

From the retrospective of a 40-milestone project (Pliego).

- Feedback batches for iterating with the owner: sort, adjust with focused checks,
  rewrite the rule a decision changes, verify fully once at acceptance.
- Verification cadence: focused checks while working, full checks once per boundary,
  last full green run recorded in the handoff and reused as baseline.
- `accepted-pending` status for milestones held only by human checks, with a list of
  what the owner owes in the handoff.
- Decisions carry origin and strength; only invariants go in the entrypoint's invariant
  list; one decision may supersede several.
- Canonical documents are rewritten and state each fact once; only decisions and
  worklogs are append-only. Open questions move from the decisions template to the
  project specification.
- Closed milestones move to an archive at close; rough read budgets for session start.
- Non-scope names who picks it up; milestones group by shared human verification round.
- Periodic audit milestone; invariant checks enumerated from the catalog (pattern).

## 1.0.0 — 2026-09-12

First distribution candidate of the streamlined method.

- Testable acceptance-criteria grammar: one observable behavior per criterion, the layer
  that checks it, and a given/when/then example where behavior is subtle.
- Named canonical updates: a milestone plans its documentation reconciliation as a floor,
  not a ceiling; discovered impacts stay in scope wherever they surface.
- Owner review order for milestone review before execution.
- Light path for small user-directed work outside the active milestone.
- Consequences of a milestone's own changes are in scope even when unplanned.
- Owner FAQ (`docs/faq.md`) and one-milestone evaluation on-ramp.
- Annotated loop glosses in the README and site; slicing is defined at both planning
  and implementation time.