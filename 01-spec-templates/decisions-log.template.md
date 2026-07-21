# Decisions Log — {{PROJECT_NAME}}

[Reference: `03-case-study-quepaso/decisions-log.md` for a fully worked example,
including how it accumulates over many sessions and how amendments are handled without
deleting history.]

Settled decisions are not relitigated without the owner asking. Dates are decision
dates. "Owner" = product owner; "delegated" = decisions the owner explicitly handed to
the LLM assistant.

## Settled — product (owner, {{DATE}})

| # | Decision | Choice | Rationale |
|---|---|---|---|
| P1 | | | |

[Number sequentially, forever — P1, P2, P3, ... never reuse a number even if a decision
is later superseded. Superseding: add a new row with the new decision, and edit the old
row to note "amended {{DATE}}: superseded by P{{N}}" rather than deleting it — the
history of *why something changed* is often as valuable as the current answer.]

## Settled — technical (delegated, {{DATE}})

| # | Decision | Choice | Alternatives considered |
|---|---|---|---|
| T1 | | | |

[Same numbering discipline. This table mirrors architecture.md's tech-choice table but
is the append-only historical record — architecture.md can be edited to reflect current
state; this log should read like a diff history.]

## Open questions (ask the owner when they become blocking)

| # | Question | Blocking for | Notes / candidate answers |
|---|---|---|---|
| O1 | | | |

[Anything flagged in the brief's "ask me" section that didn't get resolved immediately,
plus anything a later agent session identifies as a real product ambiguity per
AGENTS.md's blocked-protocol. Strike through (`~~O2~~`) and note "Settled as P{{N}}"
when an open question gets answered — never delete the row; the fact that it was once
open, and what the candidates were, is useful history.]

## Change protocol

To change a settled decision: owner states the change → update this table (add a new
row or annotate the old one — never silently delete) → update affected specs → note any
migration/rebuild impact. Any session proposing a change should present trade-offs
*here*, in this document, rather than silently diverging in code.
