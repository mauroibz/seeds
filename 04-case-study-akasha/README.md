# Case study: Akasha

The real, unedited Akasha artifacts, pulled from the live repo on 2026-08-18 — reference
only, not meant to be copied into a new project. Same rule as `03-case-study-quepaso/`:
when a template section here feels underspecified, open the matching Akasha file and see
how much detail it actually needed after thirty real sprints, not three.

## What it is

[Akasha](https://github.com/mauroibz/akasha) is a self-hosted personal library —
"records what you thought of a book or a record" — one user, no accounts, LAN-only,
AGPL v3. FastAPI/SQLAlchemy/SQLite backend, React/Vite/TypeScript/Tailwind frontend,
one container. It's a live, ongoing build (30 sprints completed as of this snapshot,
Sprint 030 active), not a finished-and-abandoned MVP, which is what makes it a useful
second data point: quepaso shows the methodology at MVP scale (6 sprints); Akasha shows
what the same discipline looks like stretched over months, a mid-project architecture
pivot (single-domain → multi-domain), and one real, documented failure.

Akasha's owner is the same person who wrote this kit, running the same discipline this
repo describes — orient from `AGENTS.md`, execute one sprint, verify for real, append a
worklog entry, hand off — independently rediscovered and extended rather than copy-pasted
from a template, because Akasha predates `04-case-study-akasha/` existing at all. Where
it diverges from `02-agent-manual/AGENTS.template.md`, that divergence is signal, not
noise: it's what the manual's shape looks like after it met a real multi-month project's
actual pressure. See "What Akasha changed" below.

## Where each file came from

Flattened out of `docs/` for consistency with the quepaso folder; paths below are
relative to the Akasha repo root.

| File here | Source path |
|---|---|
| `AGENTS.md` | `AGENTS.md` |
| `WORKFLOW.md` | `docs/agent/WORKFLOW.md` |
| `HANDOFF.md` | `docs/agent/HANDOFF.md` |
| `state.json` | `docs/agent/state.json` |
| `worklog.md` | `docs/agent/worklog.md` |
| `docs-map.md` | `docs/README.md` |
| `decisions.md` | `docs/decisions.md` |
| `product-spec.md` | `docs/specs/product-spec.md` |
| `technical-spec.md` | `docs/specs/technical-spec.md` |
| `roadmap.md` | `docs/sprints/ROADMAP.md` |
| `sprint-template.md` | `docs/sprints/TEMPLATE.md` |
| `sprint-001-foundation.md` | `docs/sprints/001-foundation.md` — the first sprint, for comparison against quepaso's Sprint 1 |
| `sprint-028-the-domain-contract.md` | `docs/sprints/028-the-domain-contract.md` — a mid-project architecture sprint, for contrast |
| `assessment.md` | `docs/assessment.md` — the incident report behind the walkthrough gate (see below) |
| `domain-architecture-proposal.md` | `docs/domain-architecture-proposal.md` — a worked example of the "proposal" doc status |
| `brand.md` | `docs/brand/BRAND.md` |
| `adding-a-domain.md` | `docs/guides/adding-a-domain.md` |
| `runbook.md` | `docs/operations/runbook.md` |
| `contributing.md` | `CONTRIBUTING.md` |

Not pulled in: 27 of the 30 sprint files (two are included as bookends), per-release
notes, and a few narrower proposal/assessment docs — real but redundant with what's
already here for the purpose of this folder. The live repo has all of it.

## What matches the methodology, unchanged

- The same document shape answering the same questions: a product spec, a technical
  spec, a decisions log, and an agent operating manual, in that authority order.
- One sprint = one milestone, done only when verified, never assumed
  (`AGENTS.md` §2–3, near-identical wording to quepaso's).
- An append-only worklog, one entry per session, same fixed format
  (done / verified / deviations / blocked / next).
- A decisions log that's law until superseded, never rewritten — `decisions.md` has 80+
  entries and not one is edited in place.
- Internal names locked on day one regardless of branding: quepaso's rule was
  `pin` in code forever; Akasha's is `book_tracker`/`items`/`entries` forever, stated in
  `AGENTS.md`'s non-negotiable invariants in almost the same sentence.
- No trust-and-safety-policy equivalent — and that's correct, not a gap. There's no UGC,
  no other users, no moderation surface. The spec set flexes to what the product needs;
  it isn't filled out by rote.

## What Akasha changed

None of this contradicts the methodology — it's what several of `METHODOLOGY.md`'s own
patterns look like once a project runs long enough to need them worked out in detail.
Item 6 has since been generalized back into `METHODOLOGY.md` and
`02-agent-manual/AGENTS.template.md`; the rest are still just observations here, not
yet folded into the templates:

1. **The operating manual split in two.** `AGENTS.md` (103 lines) is now a thin,
   fast-to-reread entrypoint — orientation, five numbered execution steps, authority
   order, invariants. `WORKFLOW.md` (`docs/agent/WORKFLOW.md`) carries the material that
   only matters on interruption/recovery: state machine, claiming a dirty worktree,
   context-budget discipline, the blocked-handoff and interrupted-work procedures. The
   kit's single-file `AGENTS.template.md` is the right shape at quepaso's scale; past
   maybe sprint 10, splitting the recovery procedures out keeps the file a coding agent
   actually rereads every session instead of skims.

2. **A documentation map with an explicit status per file** (`docs-map.md`, source
   `docs/README.md`): every doc is tagged **canonical** (true now — code disagreeing is
   a bug), **historical** (true *at a date*, never edited to match later reality), or
   **proposal** (written to be accepted or rejected). This is the single highest-value
   addition relative to the kit as it stands. Quepaso's docs never went stale enough
   inside a 6-sprint build to need this; Akasha's did, and the failure mode it prevents
   is concrete — a closed sprint file describing a since-refactored file path getting
   mistaken for a current instruction. Worth adding to `AGENTS.template.md` regardless
   of project size, since it costs one column and prevents a real failure mode.

3. **`HANDOFF.md` as a distinct artifact from the worklog.** The worklog stays
   append-only chronological history; `HANDOFF.md` is rewritten every session close to
   be the *current* state only — what's true right now, read this first, in the order it
   matters. The kit's worklog does both jobs today (last entry = current state). That
   works until the worklog is 1,766 lines deep, at which point "read the last entry"
   still works but "here's everything still true and still worth knowing" doesn't fit in
   one entry. Akasha's `HANDOFF.md` is that second thing.

4. **A machine-readable state pointer, checked by a script.**
   `docs/agent/state.json` plus `scripts/validate_project.py` (not pulled into this
   folder — it's code, not a doc) makes "which sprint is active, what's it waiting on"
   parseable and lint-checked instead of living only in prose. The kit's progress
   tracker (a checklist inside `implementation-guide.md`) is the same idea without the
   parseability; fine at 6 sprints, worth automating past ~15.

5. **Sprints as one file each** (`docs/sprints/NNN-name.md`) plus a `ROADMAP.md` holding
   contracts for sprints not yet active and a `TEMPLATE.md` to expand the next one from —
   instead of the kit's single `implementation-guide.md` holding every sprint. Scale
   call, not a philosophy change: past a certain sprint count a single growing file gets
   unwieldy to reread each session, and per-sprint files with a lightweight roadmap index
   scale better. Quepaso's 6 sprints didn't hit that wall; Akasha's 30 did.

6. **The walkthrough gate — the one addition that came from a real failure, not from
   scale.** `assessment.md` (2026-08-08) is the audit after thirteen sprints closed
   green — 122 backend tests, 38 frontend tests, 86% coverage, all passing honestly —
   on a product the owner correctly called a failure: three required frontend libraries
   were never installed, background enrichment had never once succeeded, and no gate
   could see either, because the tests mocked the exact boundary that was broken. That
   produced `AGENTS.md`'s Walkthrough gate: a sprint touching user-visible behavior isn't
   complete until the agent has run the app against realistic data, performed the actual
   user flow, and *recorded what it saw, including what looked wrong but was out of
   scope*. `METHODOLOGY.md` already said "verified not assumed" was the single
   highest-value sentence in the manual — this is that principle after it failed once in
   a way unit tests couldn't catch, made concrete enough to act on: a green test suite is
   not evidence a flow works, only running it is. Now folded into `METHODOLOGY.md`'s
   Phase 4 and `AGENTS.template.md` §2 and §4 as a general gate, independent of this
   project.

7. **A named "proposal" document status**, for a design question big enough to need
   measurement before a decision (`domain-architecture-proposal.md`: real request/latency
   numbers against MusicBrainz, before committing to the multi-domain architecture).
   Accepted proposals are kept afterward for the measurements, not for the decision
   itself — the decisions log and technical spec absorb the decision; the proposal stays
   as the evidence. The kit's Phase 2 ("handle mid-stream feature requests the same way")
   describes the same loop in miniature; Akasha's version is that loop run at
   architecture scale, with a document type to match.

## Reading order, if you want the texture

`assessment.md` first — it's the shortest path to why several of the invariants in
`AGENTS.md` and `WORKFLOW.md` exist. Then `sprint-001-foundation.md` next to quepaso's
Sprint 1 in `implementation-guide.md`, to see the same acceptance-criteria discipline at
day one. Then `HANDOFF.md` as-is — it's a live snapshot, not a template, and it's the
clearest demonstration of what "a fresh agent with no memory of this project" actually
needs handed to it.
