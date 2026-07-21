# Data Model — {{PROJECT_NAME}}

[Reference: `03-case-study-quepaso/data-model.md` for a fully worked example, including
the anonymity-enforcement pattern (§5 there) and the lifecycle/state-derivation pattern
(§3 there) at real depth.]

Authoritative schema reference. Migrations live in `{{MIGRATIONS_PATH}}`; if this
document and a migration disagree, **the migration wins** and this doc must be updated
in the same commit.

Naming: the core content entity is **{{ENTITY_NAME}}** everywhere — tables, columns,
routes, generated API surface. The brand may change; code never chases it (only the
strings module does — Phase 3 of the methodology).

Conventions: [ID scheme, timestamp convention, soft-delete/status convention, and the
rule that any score-relevant signal (likes, reports, votes) is stored **as rows, never
a bare counter** — see METHODOLOGY.md's patterns section for why].

## 1. Entity overview

```
[ER-sketch: parent ── < child ── < grandchild, one line per relationship]
```

## 2. Tables

```sql
-- One table per entity. For each: PK, FKs, the fields that matter for behavior
-- (not just "text, text, text" — comment WHY a constraint exists if it's not obvious),
-- and any status/lifecycle column.
```

## 3. Triggers and functions

| Trigger | On | Effect |
|---|---|---|
| | | |

[If the entity has a time-decay/lifecycle property (product-spec §6.1 equivalent):
document the state-derivation function here, and the trigger(s) that move whatever
timestamp the state is derived from. Prefer "derived at read time" over a batch job
that flips a status column — see METHODOLOGY.md's patterns section for why.]

[If there's a ranking/hot-score formula: it belongs here as a function, not a stored
column, unless read volume genuinely requires caching it — recomputing beats
invalidating at MVP scale.]

## 4. API surface

[However your backend exposes behavior to the frontend — generated views/functions,
hand-written endpoints, RPC-style calls. List every read and write operation the
frontend needs, grouped by reads / writes / admin-only, with just enough of a
signature that intent is clear.]

## 5. Security / trust boundary (the critical section)

**Rule: state the one sentence that must always hold**, e.g. "the real identity behind
an anonymous post must never leave the database" or "a free-tier user must never be
able to read another tenant's data." Then show the mechanism:

1. What the base storage layer enforces (who can read/write raw rows).
2. What the public-facing surface does differently (masks fields, filters rows) and
   why that's the ONE place the guarantee is enforced — never the frontend.
3. A one-line checklist for reviewing any *new* query/view/endpoint against this rule
   (quepaso's: "does it join the identity table? then it must apply the anonymity
   mask"). Put this checklist here so it's impossible to miss during a review.

## 6. Storage layout

[If there's file/media storage: bucket/path scheme, and whether the scheme itself leaks
anything it shouldn't (e.g. a user id in a path when the content is meant to be
anonymous).]

## 7. Schema headroom for known v2 features (do not build now)

[Anything explicitly deferred by the decisions log's open questions — note here what,
if anything, the current schema already does to keep the door open (a reserved status
value, a column that exists but is unused, a table structure that wouldn't need to
change). This is where "we didn't build it, but we didn't paint ourselves into a
corner" gets proven, not just claimed.]
