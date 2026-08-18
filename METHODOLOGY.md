# Methodology

How QuePaso went from a three-paragraph idea to a fully-specced, sprint-planned,
agent-buildable codebase — generalized so it repeats for the next project.

## When this applies

This process fits a specific shape of project: a **solo or near-solo owner who is not
deeply technical in the stack being used**, building an **MVP with no fixed budget**,
who wants to **delegate technology choices** but stay in control of **product and
privacy/safety decisions**, and who will hand the actual coding to **LLM agents across
many sessions** rather than a standing human team.

If your next project doesn't have that shape — say, a technical cofounder pair
programming daily, or an enterprise integration with a pre-existing architecture — the
phases still apply, but you'll lean less on Phase 0's "ask me" framing and more on
Phase 1 being a straight technical handoff.

## Phase 0 — Write the brief

Don't start with code. Start with a document a stranger (or a fresh LLM with no memory
of you) could read and understand the product, its constraints, and its unknowns.
Template: `00-initial-brief/brief-template.md`. Worked example:
`03-case-study-quepaso/quepaso-initial-brief.txt`.

A good brief has five things the quepaso brief had, in this order:

1. **Concept and origin** — what it is, and honestly, what it *isn't yet* (quepaso's
   brief named the long-term tenant/landlord idea explicitly as "later, not now" — this
   matters because it explains why some MVP decisions lean cautious without those
   decisions being in scope).
2. **Constraints that shape every later choice** — budget ("no fixed budget, favor
   low-cost/low-maintenance"), team (non-developer owner), locale/market.
3. **What you're delegating vs. deciding** — name the platform you already know you
   want (quepaso's brief hard-coded "Supabase" for backend), and explicitly say
   "your choice" for everything else, with a steer ("something simple to maintain").
4. **Product decisions you already have opinions on** — write them as decisions, not
   questions, when you're sure. The brief stated the map-centric UX, the like/comment
   model, and the anonymity requirement as settled, not open.
5. **An explicit "ask me" list** — the single highest-leverage section. Naming exactly
   which decisions are sensitive (data model impact, privacy, moderation, anything hard
   to reverse post-launch) and asking the LLM to *stop and ask* instead of silently
   deciding is what kept quepaso's spec from baking in a wrong guess about, say,
   anonymity semantics or photo EXIF handling. **Bad decisions made silently at spec
   time are the expensive kind** — they're load-bearing by the time an agent starts
   writing migrations against them.
6. **The deliverable list**, explicit: which documents you want out the other end.

## Phase 1 — Generate the spec set

Paste the brief into a fresh session. Ask for the documents named in the brief's
deliverable section. Expect — and invite — multiple rounds of `AskUserQuestion`-style
clarification before anything is "locked." Quepaso took two full rounds (moderation,
aggregation, visibility, photo/EXIF handling in round one; anonymity semantics and
resolution-flow ownership in round two) before the spec set was written.

**Answer with recommendations in mind, but override when you have a real opinion.**
Ask the assistant to present 2–4 concrete options *with a recommendation* for each open
question — this is faster than an open-ended "what should we do about X?" and it forces
the assistant to have actually thought about trade-offs rather than punting the
thinking back to you. You are not obligated to take the recommendation; quepaso's
owner took the recommended option on most sub-decisions but explicitly overrode one
(shipping the activity-lifecycle feature in the MVP rather than deferring it) because
he had a real product opinion the "safe" recommendation didn't capture.

Target artifact set (templates in `01-spec-templates/`):

| Doc | Answers |
|---|---|
| `product-spec` | What are we building, screen by screen, decision by decision? |
| `architecture` | What's the stack, and *why this over the alternatives*? |
| `data-model` | The actual schema, security boundary, and API surface |
| `implementation-guide` | Sprints, in build order, each with acceptance criteria |
| `deployment-guide` | Local dev → hosted, cost/limits, release flow |
| `trust-and-safety-policy` | Content rules and enforcement, even a stub |
| `decisions-log` | Settled decisions (don't relitigate) + open questions (revisit later) |

Two of these matter more than their length suggests:

- **`decisions-log`** is what makes a multi-week, multi-session, multi-agent project
  coherent. Every settled call gets a row with a rationale; every unresolved one gets
  logged as open rather than silently decided by whichever agent hits it first. Session
  N+40 should never re-argue something session 3 already settled.
- **`architecture`**'s tech-choice table should always have a rationale *and* an
  alternatives-considered column (see the template). Writing down what you didn't pick,
  and why, is what stops a later session from "helpfully" swapping in a different
  library because it seemed reasonable in isolation.

## Phase 2 — Handle mid-stream feature requests the same way

Specs aren't finished when Phase 1 ends — real design questions surface later too.
Quepaso's expiry/resolution mechanism is the model case: the owner had a rough idea
("Reddit-style expiry, a color change near the deadline, extended by interactions") but
was explicitly unsure of the exact mechanism. The pattern that worked:

1. State your rough idea and flag exactly which part is unresolved.
2. Ask for a concrete implementation proposal, not just validation of your idea.
3. Get the proposal back as another small set of recommended options
   (what happens at expiry? what re-arms the timer, and by how much? what's the
   starting window? does it ship now or later?).
4. Decide, and have the decision + rationale appended to the decisions log
   immediately — not batched for later, since "later" is a different session with no
   memory of this conversation.

This is the same Phase-1 loop, just triggered by a feature idea instead of the initial
brief. Any time you have a half-formed mechanism in your head, that's the shape to use.

## Phase 3 — Lock terminology before it costs anything

Rename/rebrand once, deliberately, and build in a seam so it never costs anything
again. Quepaso's rule: the content entity is called `pin` in code, schema, routes, and
migrations **permanently**, regardless of what the product is branded as. All
user-facing copy lives in one module (`lib/strings.ts`). A brand change is a one-file
diff; an internal-name change never happens because nothing depends on it being
correct except that one file.

Apply this pattern to your next project's core entity on day one, before any code
exists: pick the internal name once, isolate all user-facing strings behind one module,
and write the rule down in the decisions log so no later session "helpfully"
renames the table to match the current brand.

## Phase 4 — Write the agent operating manual

Once the spec set is settled, write `AGENTS.md` — not another spec, but the *process*
document: how an agent that has never seen this project before should orient itself,
what counts as a finished milestone, how it proves criteria are met rather than assumed,
how progress is recorded so the next session (which remembers nothing) can resume, and
what it must never do unsupervised. Template: `02-agent-manual/AGENTS.template.md`.
Worked example: `03-case-study-quepaso/AGENTS.md`.

The load-bearing sections, in order of how often they prevented real problems in
quepaso:

1. **Milestone = fully verified, not fully attempted.** Every acceptance criterion must
   be *executed* (run the tool, open the second browser session, query the DB as the
   restricted role) — never marked done because it plausibly would pass. This is the
   single highest-value sentence in the whole manual.
2. **A walkthrough gate for anything user-visible.** A green test suite answers "does
   the code do what the test asserts", not "does the flow work" — a test can mock
   exactly the boundary that's actually broken and stay green indefinitely, and a
   project can close many milestones this way before anyone notices the product itself
   doesn't work. Before a sprint that changes user-visible behavior can close, the agent
   has to actually run the application against realistic data and perform the real user
   flow end to end, then record in the worklog what it did and what it saw — including
   anything that looked wrong but was out of scope for the sprint. An issue noticed and
   left unrecorded is the exact failure this gate exists to catch. The same logic applies
   one level down: a test that substitutes a mock for the very unit or boundary an
   acceptance criterion is about doesn't satisfy that criterion, no matter how green it
   is — mock the transport, the clock, the filesystem; never mock the thing you're
   claiming to have verified.
3. **An append-only worklog**, one entry per session, fixed format (done / verified /
   deviations / blocked / next). This is the agent's memory across sessions — without
   it, session N+1 re-derives everything session N already learned, or worse, silently
   redoes it differently.
4. **Never relitigate the decisions log; never weaken a security/privacy boundary, even
   in debug code.** Guardrails that name the exact failure mode you're most afraid of,
   not generic "be careful" language.
5. **A completion report format aimed at the actual owner** — plain language, one line
   per acceptance criterion and how it was verified, what needs the owner (accounts,
   money, irreversible choices), one sentence on what's next. If the owner isn't a
   developer, the report has to be readable without becoming one.
6. **An explicit blocked/ambiguous protocol**: product ambiguity gets logged as an open
   question with options and a recommendation (same Phase-1/2 pattern, self-service);
   implementation ambiguity gets the simplest reversible choice and a worklog note;
   environment breakage gets a self-fix attempt before giving up. "Blocked on X,
   truthfully" beats a checkbox that lies.

## Phase 5 — Run the loop

Spawn an agent, point it at `AGENTS.md`, and say "complete the next milestone." It
reads the implementation guide's progress tracker, finds the first unchecked sprint,
reads the worklog for where the last session left off, builds, verifies, commits, and
stops. Repeat this for every session. The owner's job during this phase is almost
entirely: read the completion report, answer anything logged as a blocking open
question, and hand over anything that genuinely needs a human (a domain purchase, an
OAuth console, a credit card) at the one sprint that's designed to require it.

## Patterns worth reusing outside this exact stack

These generalize past "map app on Supabase" — they're really about building anything
agent-buildable and privacy-sensitive:

- **Ask, don't assume, on anything hard to reverse.** Moderation posture, data
  visibility, and identity/privacy semantics are the recurring category — get them
  wrong in the schema and every later sprint inherits the mistake.
- **Security/privacy boundaries belong in the data layer, never the frontend.**
  Quepaso's rule ("the real author id of anonymous content must never leave Postgres")
  was enforced by database views, not by a client-side check. Frontend filtering is not
  a boundary — it's a suggestion. This generalizes to any system with a trust
  distinction (admin vs. user, owner vs. public, paid vs. free): enforce it where the
  untrusted party has no code-execution access.
- **Store the raw signal, not just the aggregate.** Likes-as-rows instead of a bare
  counter, reports-as-rows instead of a flag — you don't know today what anti-abuse
  heuristic you'll need in six months, but a counter has already thrown away the data
  it would need.
- **State derived at read time beats state maintained by a batch job**, whenever the
  state is a function of a timestamp (active/fading/dormant; trial/expired;
  stale/fresh). No cron job to fail silently, no lag between a batch run and reality,
  and "revival" (an old entity becoming active again) falls out for free instead of
  needing special-case code.
- **Decisions log with a change protocol**, not just meeting notes. Settled decisions
  are law until explicitly revisited; open questions are logged with candidates the
  moment they're identified, even if answering them isn't urgent yet. This is what lets
  a decisions log outlive any one session's context window.
- **One module owns all user-facing strings.** Cheap i18n later, and the only file a
  rebrand ever touches.
- **Tech-choice tables always carry "alternatives considered."** Prevents later
  "cleanup" that quietly reintroduces a rejected option.

## Adapting the templates to a different stack or domain

The templates in `01-spec-templates/` mirror quepaso's actual stack (Postgres/RLS
backend, no custom server, client-side data enrichment) because that's the real,
tested example. If your next project's shape is different — a mobile app, a
job-queue-heavy backend, a different database with no row-level security equivalent —
keep the *document shape* (what question each doc answers) and swap the *content*:

- `architecture.template.md`'s tech-choice-table pattern and system-diagram slot are
  stack-agnostic — fill them with your real stack.
- `data-model.template.md`'s "security boundary" section assumes a database-enforced
  boundary is available (true for Postgres+RLS, Firebase security rules, etc.). If your
  backend has no such mechanism, that section becomes "which layer enforces this, and
  why do we trust it" — still ask the question, just answer it differently.
- The lifecycle/state-derivation pattern is optional — include it only if your domain
  has a genuinely time-decaying entity.
- `AGENTS.template.md`'s testing section assumes a local-first dev loop
  (Docker/local backend, never verify against hosted). If your stack can't run fully
  local, replace it with "always verify against a disposable/staging environment,
  never production" — the principle (never let an agent's verification step touch
  real user data) is what has to survive, not the specific commands.

## A second worked example, at a different scale

`03-case-study-quepaso/` is an MVP snapshot — six sprints, closed-source. It doesn't
show what this discipline needs once a project runs for months instead of weeks.
`04-case-study-akasha/` does: a real, ongoing, open-source build (30+ sprints as of its
snapshot date) run by the same owner under the same discipline this document describes,
independently extended rather than copied from a template. Full comparison, file by
file, is in that folder's `README.md`; the short version:

- **What held unchanged**: the document shape, the milestone-then-verify cadence, the
  append-only worklog, the decisions log as settled law, and the day-one internal-naming
  lock (quepaso's `pin`, Akasha's `book_tracker`/`items`/`entries`) all survived thirty
  sprints without modification.
- **What scale forced**: the operating manual split into a thin entrypoint (`AGENTS.md`)
  plus an expanded recovery/interruption manual (`WORKFLOW.md`); sprints became one file
  each instead of one growing `implementation-guide.md`; a machine-readable state
  pointer (`state.json`) got a validating script instead of living only in a prose
  checklist.
- **What a real failure forced**: after thirteen sprints closed green on a product that
  didn't work — tests mocking the exact boundary that was broken — Akasha added a
  **walkthrough gate**: a sprint touching user-visible behavior isn't complete until the
  agent has actually run the app against realistic data and recorded what it saw. This
  is Phase 4's "verified not assumed" principle in its sharpest documented form, and it's
  now folded into Phase 4 above and `AGENTS.template.md` §2 and §4 as a general gate —
  see `04-case-study-akasha/assessment.md` for the incident it came from.
- **What a design question at architecture scale looks like**: Akasha's single-domain →
  multi-domain pivot (`domain-architecture-proposal.md`) is Phase 2's mid-stream-feature
  loop run on a decision big enough to need real measurement first, with a named
  "proposal" document status added to hold the evidence once the decision moved into the
  decisions log.

## Turning this into a Claude Code skill

`skill/SKILL.md` is a first draft that automates Phases 0–2 (brief → spec set →
decisions log) and Phase 4 (AGENTS.md generation) as an invokable skill. It's
deliberately left as a draft, not a finished skill, because the highest-value part of
this whole methodology is the *judgment calls* in Phase 1 (what counts as
"sensitive enough to ask about") and Phase 4 (what guardrail actually would have
prevented a real mistake) — calls worth reviewing by hand at least once more before
you let a skill run them unattended. Read it, adjust anything that's too
quepaso-specific, and it's ready to install.
