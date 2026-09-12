# The Seeds method

Seeds is an operating method for projects carried by agents over many sessions. It is
optimized for work where no single conversation can hold the whole project and where an
agent is expected to proceed autonomously inside clearly stated boundaries. Software was
its first proving ground, not its boundary: the method applies wherever work can be split
into bounded outcomes and verified with meaningful evidence.

It does not require a particular domain, toolchain, planning vocabulary, document name,
team size, or number of specifications. It requires six capabilities:

1. explicit sources of truth;
2. a protocol for material decisions;
3. one bounded active milestone;
4. externally verifiable acceptance criteria;
5. evidence at the layer where behavior can actually fail; and
6. durable history plus a concise current handoff.

The loop is:

```text
Understand -> decide -> slice -> build -> verify -> hand off
```

## 1. Understand before building

A fresh agent must be able to answer, without reconstructing prior conversations:

- What is the product for, and who is it for?
- What is explicitly out of scope?
- Which constraints shape technical choices?
- Which product or platform decisions are already settled?
- Which data, privacy, security, operational, or cost boundaries must never be weakened?
- Which questions remain open, and when do they become blocking?

For a new project, collect this in a short brief and let it become the first project
specification. The brief is input, not a second permanent source of truth. For an existing
project, derive the answers from current documentation and implementation, then ask only
about consequential gaps.

Do not turn every unknown into a question. Ask before choices that materially affect
user-visible semantics, irreversible schema or data changes, deletion or overwrite,
privacy/security exposure, paid services, or architecture that is expensive to reverse.
For ordinary reversible implementation details, choose the simplest compatible option
and keep moving.

When asking, offer a small set of concrete choices, their trade-offs, and a recommended
default. Record the answer when it is made; do not depend on conversational memory.

## 2. Establish sources of truth by concern

There is no useful universal order such as "the current output always wins" or "the
specification always wins." Authority depends on the question:

| Concern | Normal authority |
|---|---|
| Intended product behavior and scope | Product/project specification |
| Current technical contract | Technical specification, schema, or API contract |
| Applied database structure | Migrations |
| Current work boundary | Active milestone |
| Resume state | Current handoff |
| Historical rationale and evidence | Decisions, worklog, and completed outcomes |

The produced work, source material, and checks are evidence of actual reality. They do not
give an agent permission to contradict higher-level intent silently. When output and
intent disagree, determine whether the work is wrong or the plan changed, then reconcile
the lower-level artifacts and record any material decision.

Mark documents by status when ambiguity is possible:

- **canonical** — describes what should be true now;
- **historical** — accurately records what was true at a date and is not an instruction;
- **proposal** — evidence and options awaiting acceptance or rejection.

Historical documents are dated, not silently rewritten. Accepted proposals feed their
decision into canonical documents; the proposal may remain as evidence.

Settled decisions are binding until explicitly superseded through the project's change
protocol. Implementation may expose a real reason to revisit one; that calls for evidence,
an impact assessment, and user direction when material—not a silent divergence in code.

## 3. Create only the documentation the project needs

Seeds requires roles, not seven fixed documents. A small project normally needs:

- an agent entrypoint;
- a project source of truth;
- a plan with one active milestone;
- an append-only decisions record;
- a current handoff; and
- an append-only session worklog.

The project source of truth may combine product intent, architecture, data contracts, and
operations while it remains easy to navigate. Split it when different concerns have
different authorities or the file becomes expensive to reread. Create a dedicated
deployment guide, runbook, data model, safety policy, or design specification only when
the project makes that concern substantial.

Do not duplicate an existing brief, README, decision record, issue tracker, source index,
or operating guide merely to match a Seeds filename. Point the agent entrypoint to
whichever artifact already owns the role.

## 4. Make one milestone executable

A milestone is a bounded, coherent outcome—not a bucket of activity. It may be a feature,
correctness repair, risk-reducing investigation, operational change, or documentation
contract. It should contain:

- one measurable objective;
- required context, including exact source sections and known work or code paths;
- the observed implementation baseline;
- deliverables or vertical slices;
- externally verifiable acceptance criteria;
- required test and verification layers;
- canonical documents or sections the milestone is expected to change, named when known;
- explicit non-scope;
- risks or decisions that may need surfacing; and
- an outcome section completed with actual evidence.

Plan in build order and keep future milestones thinner than the active one. Detail written
too early fossilizes guesses. Expand a future milestone when it becomes active, using the
implementation and earlier outcomes as evidence.

A criterion is testable when a fresh agent could execute it without asking what it
means: one observable behavior per criterion, the layer at which it must be checked, and
— wherever the behavior is subtle, stateful, or easy to satisfy vacuously — a concrete
given/when/then example. If no evidence the milestone could produce could observe the
failure a criterion exists to prevent, rewrite the criterion or the evidence before
implementation.

A milestone is cheapest to correct before implementation starts. Review it in the order
that lets you stop earliest: the objective first — if it targets the wrong problem, stop
there — then the acceptance criteria, then the explicit non-scope. The most valuable
catch is the missing criterion: the case the owner cares about most that no acceptance
criterion mentions.

Exactly one milestone should be active in a single worktree. Parallel work requires
explicitly isolated branches/worktrees and project-specific coordination; Seeds does not
infer that setup.

Slicing happens twice. At planning time, the backlog is cut to one bounded milestone —
the slice step of the loop: choosing the next outcome and writing its deliverables,
acceptance criteria, and verification. During implementation, the milestone itself is
cut into coherent, verifiable increments — sub-deliverables that can be completed and
checked in sequence, leaving the worktree in a working state at each point. The first
slice chooses what to build; the second keeps every intermediate state green and
reviewable.

## 5. Operate one milestone at a time

At the start of a session:

1. inspect repository status and recent history;
2. read the agent entrypoint, current handoff, active milestone, and only the canonical
   sections and decisions it references;
3. inspect the actual source material, existing work, and checks named by the milestone;
4. reconcile unexplained worktree changes before editing; and
5. confirm the milestone is ready and its prerequisites are satisfied.

During implementation:

- stay inside the milestone;
- work in coherent, verifiable increments;
- use test-first development when behavior can be specified before implementation;
- use measurement-first investigation when the milestone exists to answer whether or how
  something should be built;
- do not weaken, skip, delete, or mark flaky a test merely to obtain a green result;
- preserve unknown user or prior-agent changes; and
- update nearby canonical documentation while context is fresh.

When the repository uses Git and the task permits commits, make small coherent commits in
working states. Do not rewrite prior-session commits, and do not push unless the user asks.

If a prerequisite defect blocks the milestone, repair it when the fix is bounded and
necessary, then record the deviation. Do not pull future scope forward just because it
is convenient.

Consequences of the milestone's own changes are in scope wherever they surface, even
when the plan did not name them. Address a discovered impact when the fix is bounded —
a backend change that alters frontend behavior, for example — or surface it with
evidence as a risk or decision when it is not. Explicit non-scope fences off adjacent
work, not the reach of the milestone's own changes.

### Small work outside the active milestone

A user may direct small work no milestone covers — a quick fix, a setting, a one-file
patch. It follows the light path instead of milestone ceremony:

1. Record it in the worklog with how it was verified, or `NOT RUN` if it was not.
2. Verify it narrowly in the session, at the cheapest layer that can observe the change.
3. Side work that is unverified, or that the next milestone builds on, is fully
   verified before that milestone starts — a baseline must not stand on unverified
   changes. All other side work is covered by that milestone's project-wide checks; if
   no further milestone is planned, the handoff names the verification still owed.

Work that outgrows a session-sized change stops being light-path: surface it and plan
it as a milestone. Light-path work is recorded, never planned, so exactly one milestone
stays active.

## 6. Verify behavior, not plausibility

A milestone is fully verified, not fully attempted. Every acceptance criterion must be
executed using evidence capable of observing the claimed behavior.

- A database access boundary is tested as the least-privileged relevant caller, not as an
  administrator.
- A migration is applied to a realistic disposable database, not only read as text.
- A container contract is verified with a built and running container.
- An external adapter is proved at its boundary with recorded real responses or a safe
  live check when authorized, not by mocking the adapter itself.
- User-visible work is exercised in the running application against realistic data at
  the relevant viewport/device and accessibility conditions.
- Research claims are checked against authoritative sources, data work against real or
  representative inputs, and documents or media in their rendered final form.

Passing tests prove only what the tests can observe. A test that replaces the exact unit
or boundary under examination does not satisfy a correctness criterion. Mock transport,
time, randomness, filesystem, or an external service at its edge; do not mock the thing
being claimed as working.

### Walkthrough gate

Any milestone that changes user-visible behavior remains incomplete until the agent runs
the application, performs the real flow end to end, and records:

- what data and environment were used;
- what actions were performed;
- what was observed; and
- anything that looked wrong, even if it was outside milestone scope.

An observed defect left unrecorded is a handoff failure. A skipped required check must be
reported as `NOT RUN` with the reason, and normally prevents completion.

## 7. Reconcile and hand off

Before closing a milestone:

1. update canonical documents for every implemented contract that actually changed. The
   milestone's named canonical updates are a floor, not a ceiling: impacts discovered
   during implementation are reconciled too, and updates the plan did not name are
   recorded as deviations;
2. append material choices or deviations to the decisions record;
3. fill the milestone outcome with delivered behavior, concise verification results,
   deviations, and relevant commits;
4. review downstream milestones for affected assumptions;
5. append a worklog entry for the session;
6. rewrite the handoff as concise current reality and the exact next action;
7. update the active-milestone pointer only after implementation is verified; and
8. run the project's final checks and leave the worktree in the state its repository
   policy requires.

Then stop and report in language appropriate to the owner: what completed, how each
criterion was verified, deviations, anything requiring a human, and what comes next.

The decisions record and worklog are append-only history. Correct them with later entries.
The handoff is different: it is deliberately rewritten because stale current-state notes
are dangerous.

## 8. Blocked and interrupted work

When product intent is ambiguous, log the open question with options and a recommendation.
Stop only if no safe useful work remains. When the environment is broken, attempt bounded
self-repair and record what was tried before declaring a blocker.

If a session ends before the milestone closes, preserve coherent green work, append the
worklog, and update the handoff with the exact next action, known dirty files, commands
run, results, and blocker if any. The next session resumes from evidence; it does not
restart from a summary or discard unexplained changes.

## 9. Scale the mechanism only when pressure appears

- Start with one plan. Split one file per milestone when the plan becomes costly to read
  or historical paths begin to confuse current instructions.
- Keep the handoff short even when the worklog grows. Agents read the latest relevant
  history, not the entire journal. Large worklogs may be rolled into dated archives
  without rewriting entries.
- Add a machine-readable state pointer only when prose state is genuinely unreliable.
  The pointer must be generated from one authoritative source; never require agents to
  hand-edit the same state twice. Validate the derived output independently.
- Use a proposal or a gated investigation milestone when cost or viability is unknown.
  A measured "do not build" verdict is a complete, correct result.
- Split recovery detail out of `AGENTS.md` when the entrypoint stops being quick to reread.
  The entrypoint remains the binding map; an expanded workflow handles interruption and
  rare recovery cases.

## Definition of done

A Seeds milestone is done only when scope is delivered, every required criterion is
verified at the right layer, user-visible work passes the walkthrough gate, canonical
documentation matches reality, material decisions and deviations are recorded, current
state is handed off, and the repository is left coherent. Otherwise it remains in
progress or is truthfully blocked.
