---
name: kickstart-project
description: Turn a rough product idea into a full spec set (product spec, architecture, data model, implementation guide, deployment guide, trust & safety policy, decisions log) and an AGENTS.md operating manual, ready to hand to an autonomous build agent. Use when the user has a new project idea and wants the QuePaso-style docs-first kickoff — a brief, clarifying questions, a settled spec set, and a sprint plan — rather than jumping straight to code.
---

# Kickstart a new project from a spec

This skill runs Phases 0–4 of `METHODOLOGY.md` (in the same kit this file ships
with) for a new project idea: brief → clarified spec set → locked terminology →
agent operating manual. It deliberately does **not** start writing application code —
its output is the docs set and `AGENTS.md` that a *separate* agent session then builds
from (Phase 5, run by the user separately: "spawn an agent, point it at AGENTS.md, say
complete the next milestone").

Read `../METHODOLOGY.md` in full before using this skill for the first time — it has
the reasoning behind every step below, and the patterns list that should inform
judgment calls this skill can't fully script.

## Inputs this skill needs from the user

If the user hasn't already provided these, ask before proceeding:
- A rough description of the product (even unstructured — this skill's first job is to
  turn it into a proper brief).
- Their technical background (are they going to read/write code themselves, or is
  everything delegated?).
- Any platform/vendor choices already fixed vs. fully delegated.
- Budget/scale constraints.
- Whether they already know of any sensitive/hard-to-reverse decisions they want to be
  consulted on (moderation, privacy, data visibility) — if they don't know yet, that's
  fine, this skill's job includes surfacing the likely candidates.

## Procedure

1. **Write the brief.** Use `../00-initial-brief/brief-template.md` as the skeleton.
   Fill it from the user's input; do not leave a section as a bracketed instruction —
   either fill it in or explicitly ask the user for what's missing. Pay special
   attention to the "open questions to resolve" section: actively look for
   moderation/abuse, data aggregation/dedup, visibility (public vs. private/draft),
   any user-uploaded-content metadata handling, and anti-gaming concerns even if the
   user didn't mention them — these are the categories that bit quepaso hardest when
   left unstated. Show the user the finished brief before proceeding; it's their
   product, and this is the cheapest point to correct a misunderstanding.

2. **Generate the spec set, asking as you go.** For each open question in the brief,
   use AskUserQuestion with 2–4 concrete options and a recommendation — do not silently
   decide anything flagged as sensitive. Expect multiple rounds; don't rush to a single
   pass. As answers land, write the seven documents using `../01-spec-templates/*` as
   the skeleton for each (`product-spec.md`, `architecture.md`, `data-model.md`,
   `implementation-guide.md`, `deployment-guide.md`, `trust-and-safety-policy.md`,
   `decisions-log.md`), replacing every bracketed instruction with real content specific
   to this product — the templates are shapes, not filler text to leave in place.
   Record every answered question as a settled row in `decisions-log.md` immediately;
   don't batch this for later.

3. **Lock terminology (Phase 3).** Before writing a single line of the implementation
   guide, decide the one internal name for the core content entity and record it as a
   settled decisions-log row: code/schema/routes use that name permanently regardless
   of future branding, and all user-facing copy lives in exactly one strings module.
   Use this name consistently across every doc from this point on.

4. **Write `AGENTS.md`.** Use `../02-agent-manual/AGENTS.template.md`, filling every
   placeholder with specifics from the spec set just written — especially the
   one-sentence trust/security-boundary guarantee (pull it verbatim from
   `data-model.md` §5) and the command cheatsheet (pull it from `deployment-guide.md`
   and whatever local-dev setup was decided in `architecture.md`). This file is what
   lets the user later say "spawn an agent, point it at AGENTS.md, complete the next
   milestone" and have that actually work — verify every placeholder was filled before
   calling it done.

5. **Hand off, don't continue into code.** End by telling the user the doc set is
   ready, listing the seven docs + AGENTS.md, and stating the Phase-5 instruction
   they'll give a fresh agent session. Do not scaffold the actual application — that's
   a separate, later agent invocation working from `implementation-guide.md` Sprint 0,
   exactly as this skill's own methodology prescribes.

## Judgment calls this skill should not fully automate

- Which brief details count as "sensitive enough to ask about" vs. safe to decide —
  when genuinely unsure, ask rather than guess; a false-positive question costs the
  user one AskUserQuestion round, a silently wrong guess costs a schema rework later.
- Whether a lifecycle/state-decay section (product-spec §6.1 / data-model §3 pattern)
  applies at all — only include it if the product has a genuinely time-decaying
  entity; don't force the pattern onto a product that doesn't need it.
- How much of `AGENTS.md`'s guardrail list is generic (keep it) vs. needs a
  project-specific addition (e.g. a domain with its own regulatory guardrail).

## When this skill is NOT the right tool

If the user already has a codebase and wants a feature added, or wants code written
right now rather than specced first, this skill doesn't apply — just do the work
directly.
