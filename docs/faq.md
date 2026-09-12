# Seeds — frequently asked questions

**Status:** canonical

Short answers for people evaluating the method. The durable reasoning lives in
[the method](../seeds/references/method.md); the walkthrough incident lives in
[why-walkthroughs.md](why-walkthroughs.md).

## Isn't this overhead for a small project?

Seeds requires capabilities, not a fixed set of files. A small project carries them in a
handful of short documents, and adoption maps roles onto what already exists instead of
creating Seeds-shaped copies. Small user-directed fixes follow the light path — a worklog
entry plus narrow verification — not milestone ceremony. The ceremony that remains is
proportional to blast radius.

## Does Seeds mandate a folder layout or specific file names?

No. Seeds specifies document roles — agent entrypoint, project truth, delivery plan,
decisions, handoff, worklog — and reuses any artifact that already performs one. The
templates are prompts, not a taxonomy.

## How is this different from just writing an AGENTS.md?

An AGENTS.md is one role: the entrypoint and reading order. Seeds adds the loop around
it — one active milestone with verifiable criteria, a decision protocol, verification at
the layer where behavior can actually fail, and resume state for the next session. A
lone instructions file has no mechanism for staying true as the work evolves.

## Does it replace my issue tracker, ADRs, or existing documentation?

No. Adoption is a mapping exercise: an issue tracker can be the plan, an ADR log can be
the decisions record, an operating guide can own the commands. The entrypoint links to
them; nothing is rewritten to fit a template.

## Why require a walkthrough when the test suite passes?

Because green suites have shipped broken products. In one real incident, 122 passing
backend tests, 38 passing frontend tests, 86% coverage, and a green validator coexisted
with a product that failed its basic purpose — no check had ever run the application and
watched the flow. The full story is in [why-walkthroughs.md](why-walkthroughs.md). A mock
of the thing being proved is not proof.

## Can a required gate be skipped?

Honestly, or not at all. A check that cannot run is recorded as `NOT RUN` with the reason
and normally leaves the milestone incomplete. An owner can waive a gate; the waiver is
recorded as waived, never as passed.

## Does the agent stop after one milestone?

By default, yes: one verified increment, then a report the owner can check. The owner can
always direct continuation. The stop keeps verification and review cheap relative to what
was built.

## How does Seeds relate to spec-driven development frameworks?

Spec-driven frameworks center a living requirements corpus and agreement before
implementation; Seeds centers execution evidence, decision governance, and resume state
across sessions — including everything that happens after the code is written. The two
compose; Seeds does not require a requirements corpus or a fixed taxonomy, while they overlap
in the middle: plan-as-markdown in the repository, and human review before work. 

## What if the project doesn't use Git?

The method is toolchain-agnostic. Commit and history rules apply where version control
exists; everything else — roles, criteria, verification, handoff — works unchanged.

## How much must a fresh agent read at session start?

The entrypoint, the current handoff, the active milestone, the decisions and canonical
sections it names, and the latest relevant worklog entry. Not the whole journal. That
bounded read is the point: any session, any agent, the same context.