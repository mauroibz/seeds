# [PROJECT] — delivery plan

**Status:** canonical
**Plan revision:** 1
**Active milestone:** [M-001 or link]

## Delivery rule

One milestone must leave a demonstrably usable or risk-reducing increment, every required
criterion verified, canonical documentation reconciled, history recorded, and the
repository in its required end state.

## Milestones

| Milestone | Outcome contract | Depends on | Status |
|---|---|---|---|
| M-001 | [One measurable outcome] | — | ready |
| M-002 | [Thin future outcome; expand when activated] | M-001 | planned |

Exactly one milestone is `ready`, `in_progress`, or `blocked` in one worktree. Completed
milestones never return to `in_progress`; later regressions become prerequisite repairs or
new milestones.

## Active milestone

[For a small plan, paste the adapted `MILESTONE.md` structure here. When the plan becomes
costly to reread, move milestones to separate files and keep this section as a pointer.]

## Future intent

[Ideas that are not scheduled. Naming something here does not authorize building it.]

## Cross-milestone definition of done

- Every acceptance criterion is satisfied or the milestone remains incomplete.
- Required tests and real-flow verification run at the appropriate layer.
- Data, security, privacy, and operational invariants remain true.
- Changed contracts and downstream assumptions are reconciled.
- Decisions, worklog, outcome, and current handoff are updated.
- The project-wide checks pass and the worktree meets repository policy.
