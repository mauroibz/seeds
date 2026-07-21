# Initial brief template

Annotated skeleton for the document you hand to a fresh LLM session to kick off Phase 1.
Write it as plain prose (a `.txt` or `.md` is fine — quepaso's was a `.txt`), not a form;
the annotations below (in `[brackets]`) are instructions to you, the author — delete them
as you fill each section in. See `03-case-study-quepaso/quepaso-initial-brief.txt` for the
real thing this is abstracted from.

---

I want to develop a [product], tentatively called "[working name — it's fine if this
changes]".

## Concept and origin

[What is it, in plain language? If there's a longer-term vision this MVP is a stepping
stone toward, say so explicitly, and say explicitly that the bigger version is *not*
being built yet — this context explains later decisions (e.g. "we're being cautious
about X now because of where this eventually goes") without expanding scope now.]

[Am I not technical in the stack I'm asking for? Say so plainly — it changes how much
the assistant should explain vs. just decide, and it's the reason later phases include
plain-language completion reports instead of terse engineering updates.]

This is a [PoC/MVP/other] with [budget constraint — e.g. "no fixed budget, favor
low-cost/low-maintenance choices over premium ones" or a real number]. [Team size /
who else is involved, if anyone.]

## Scope for first release

- [Market/locale/language constraints, if any.]
- [Anything you know you explicitly do NOT want scope creep on yet — e.g. "single
  language is fine for MVP, don't build i18n scaffolding, but don't paint us into a
  corner either."]

## Platform decisions you already have an opinion on

[Name anything you're already committed to — a backend platform you've chosen, a
regulatory constraint, an existing account/vendor relationship. Everything else: say
"your choice" explicitly, with a steer (e.g. "something simple to maintain," "favor
mainstream well-documented tools over clever ones" — that steer matters more than it
looks like it does, because it's what an LLM should optimize for when picking among
otherwise-equal options).]

## Identity, privacy, and any trust boundary the product needs

[If the product has any notion of anonymous vs. identified, admin vs. user, private vs.
public, or anything where one party needs to be protected from another — describe the
intent even if you don't know the mechanism. Explicitly ask: what does this protection
actually mean? Hidden from other users only, or from the platform/moderators too? This
is exactly the kind of question that's cheap to answer now and expensive to get wrong
after a schema exists.]

## Product decisions

[Write down anything you're already sure about, as decisions, not questions — the core
user flow, the main screen, what the primary and secondary engagement goals are (if you
have competing goals, name the priority order — quepaso's brief named "permanence of a
persistent thread" as primary and "doomscroll discovery feed" as secondary, and that
ordering shaped later trade-offs). Include anything explicitly *undecided* that you
want proposals for, even if it's not privacy-sensitive (e.g. "there should be some kind
of resolution/expiry mechanic, mechanism TBD").]

## Open questions to resolve before or while writing specs

[This is the highest-leverage section. List every decision that: touches the data
model, is hard to reverse once real data exists, or is privacy/moderation/legal
adjacent. For each, ask the assistant to propose 2–3 concrete alternatives and a
recommendation rather than deciding silently. Number them — you'll refer back to them
by number in the decisions log later. Categories worth checking for any product:
moderation/abuse handling, how duplicate/overlapping content is modeled, what's public
vs. private/draft, any user-uploaded-content metadata handling (EXIF, location, etc.),
anti-gaming/anti-abuse for anything with a public score or ranking.]

## Deliverable

Design and write specs alongside an implementation plan: [list the documents you want —
default to the seven in `01-spec-templates/` unless you have a reason to drop one].
This guide will be ingested by you and other LLMs as we build toward an MVP.

Feedback on the proposals above is welcome. Ask for clarification as many times as
needed before locking in the plan.
