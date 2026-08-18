<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/seeds-logo-tagline-dark.svg">
    <img src="assets/seeds-logo-tagline.svg" alt="Seeds — for agentic builds" width="480">
  </picture>
</p>

A methodology and a reusable operating manual for building a real project with an
autonomous LLM coding agent — sprint by sprint, across many sessions, with no standing
human supervision.

It's two things, bundled together because they were discovered together on one project,
but genuinely separable: **the agent operating manual** (domain-independent —
it doesn't know or care what you're building) and **the spec-generation methodology**
that gets you to a spec set worth building one around. You don't need the second to use
the first.

## Learn about it

Read [`METHODOLOGY.md`](METHODOLOGY.md) — phase by phase, why each document exists, and
the patterns that generalize past this exact stack (security boundaries live in the data
layer, store raw rows not counters, decisions are law until superseded, etc.).

Then see how it actually played out — two real, unedited examples at different scales:

- **[`03-case-study-quepaso/`](03-case-study-quepaso/)** — MVP scale: 6 sprints,
  closed-source. The methodology's first run, and the source every template in this repo
  was generalized from.
- **[`04-case-study-akasha/`](04-case-study-akasha/)** — larger scale: 30+ sprints,
  open-source, still active. What the same discipline looks like stretched over months,
  including a real documented failure and the verification gate it produced. Its own
  [README](04-case-study-akasha/README.md) compares it point-by-point against the
  templates — what held, what scale forced, what the failure forced.

Templates alone lose the texture that makes a spec set actually usable — the rationale
columns, the "why we rejected X" notes, the exact tone of an acceptance criterion. When a
template section feels underspecified, open the matching file in either case study and
see how much detail it needed in practice.

## Use it

Pick whichever matches where you're starting from:

- **You already have (or are writing) your own specs** and just want the operating
  discipline that keeps an agent honest across sessions — verifying instead of assuming,
  remembering across sessions, never relitigating settled decisions. Take
  [`02-agent-manual/AGENTS.template.md`](02-agent-manual/AGENTS.template.md), fill in
  the placeholders against whatever spec set you've got, and go. That's the whole
  reusable asset; nothing else here is required reading.
- **You're starting from a rough idea with nothing written yet.** Write a brief from
  [`00-initial-brief/brief-template.md`](00-initial-brief/brief-template.md); feed it to
  a fresh LLM session to generate the spec set from
  [`01-spec-templates/`](01-spec-templates/), asking clarifying questions instead of
  guessing; then have it write `AGENTS.md` from the template above. Or run
  [`skill/SKILL.md`](skill/SKILL.md), which automates brief → spec set → `AGENTS.md` —
  read `METHODOLOGY.md` first if you're going to let it run unattended, since the
  judgment calls in Phase 1 and Phase 4 are worth reviewing by hand at least once.

Either way, once `AGENTS.md` exists: spawn an agent, point it at `AGENTS.md`, say
"complete the next milestone." Repeat.

## Repo map

```
METHODOLOGY.md               ← the how and why, phase by phase — start here to learn it
00-initial-brief/
  brief-template.md           ← annotated skeleton for your next project's initial brief
01-spec-templates/            ← skeletons for the 7-doc spec set (product, architecture,
                                data model, implementation guide, deployment, trust &
                                safety, decisions log) — placeholders only
02-agent-manual/
  AGENTS.template.md          ← THE reusable artifact: genericized operating manual for
                                an autonomous build agent, independent of any spec set
03-case-study-quepaso/        ← real, unedited artifacts — MVP scale, closed-source,
                                the first run this kit was generalized from
04-case-study-akasha/         ← real, unedited artifacts — larger scale, open-source,
                                still active; its README notes where it diverged and why
skill/
  SKILL.md                    ← draft Claude Code skill automating brief → spec set →
                                AGENTS.md (the spec-generation half, not the agent-manual
                                half — see METHODOLOGY.md before using it unattended)
```

## Genericity guarantee

Every file outside the two case-study folders uses bracketed placeholders (`[like this]`,
`{{LIKE_THIS}}`) instead of real content. Where QuePaso or Akasha is mentioned in
`METHODOLOGY.md` or the templates, it's always a backward-pointing example ("QuePaso's
rule was X — see the case study") explaining *why* a section exists, never content meant
to be reused as-is. The case-study folders are intentionally project-specific — they're
there to be read, not copied.
