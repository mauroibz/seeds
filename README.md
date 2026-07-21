# Project Kickstart Kit

This repo is two things, bundled together because they were discovered together on one
project (QuePaso), but genuinely separable — know which one you're reaching for.

1. **The agentic execution scaffold** — how to get an autonomous LLM coding agent to
   build a real, multi-week project across many sessions with no standing human
   supervision: a milestone-then-stop cadence, criteria that must be *verified* not
   assumed, an append-only worklog so no session re-derives what a previous one already
   learned, a decisions log treated as settled law, and guardrails aimed at specific
   failure modes rather than generic caution. **This part is domain-independent** — it
   doesn't know or care what you're building. It's the actual reusable asset.
2. **A spec-generation methodology** — a repeatable way to turn a rough product idea
   into a product spec, architecture spec, data model, sprint plan, deployment guide,
   and trust & safety policy, by asking clarifying questions instead of guessing. Useful,
   but its *output* is different every time by design — a future project's specs won't
   look like QuePaso's, and that's fine.

If you only want #1, go straight to `02-agent-manual/AGENTS.template.md` — fill in the
placeholders against whatever spec set your next project already has (even one written
by hand, or by a different process entirely) and you have the same operating discipline
that ran QuePaso's build. Everything else in this repo exists to help you get *to* a
spec set worth building an agent manual around, not to constrain what that spec set
contains.

## What's here

```
METHODOLOGY.md               ← read this first. Both halves, phase by phase, plus the
                                generalized patterns list (security boundaries live in
                                the data layer, store raw rows not counters, derive
                                lifecycle state at read time, etc.)
00-initial-brief/
  brief-template.md           ← annotated skeleton for your next project's initial brief
01-spec-templates/            ← skeletons for the 7-doc spec set (product, architecture,
                                data model, implementation guide, deployment, trust &
                                safety, decisions log) — placeholders only, no QuePaso
                                content baked in
02-agent-manual/
  AGENTS.template.md          ← THE reusable artifact: genericized operating manual for
                                an autonomous build agent, independent of any spec set
03-case-study-quepaso/        ← the real, unedited QuePaso artifacts — reference only,
                                not meant to be copied into a new project
skill/
  SKILL.md                    ← draft Claude Code skill automating brief → spec set →
                                AGENTS.md (the spec-generation half, not the agent-manual
                                half — see METHODOLOGY.md before using it unattended)
```

## Genericity guarantee

Every file outside `03-case-study-quepaso/` uses bracketed placeholders
(`[like this]`, `{{LIKE_THIS}}`) instead of real content. Where QuePaso is mentioned in
`METHODOLOGY.md` or the templates, it's always a backward-pointing example ("QuePaso's
rule was X — see the case study") explaining *why* a section exists, never content
meant to be reused as-is. `03-case-study-quepaso/` is the one folder that's
intentionally QuePaso-specific — it's there so an underspecified template section has
a real worked example to compare against, and it's meant to be read, not copied.

## The one-paragraph version (full pipeline)

Write a brief that describes the product and explicitly flags which decisions you want
to be *asked* about rather than have silently made for you. Feed it to a fresh LLM
session and have it produce the spec set — asking clarifying questions along the way
instead of guessing. Then have it write an `AGENTS.md` that turns that spec set into
instructions an autonomous coding agent can follow, one milestone at a time, forever,
without you in the loop. Spawn an agent, point it at `AGENTS.md`, say "complete the next
milestone." Repeat.

## Why a case study folder exists

Templates alone lose the texture that made QuePaso's docs actually usable — the
rationale columns, the "why we rejected X" notes, the exact tone of an acceptance
criterion. `03-case-study-quepaso/` is the real, unedited output. When a template
section feels underspecified, open the matching QuePaso file and see how much detail
that section actually needed in practice.
