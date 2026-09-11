# [PROJECT] — project specification

**Status:** canonical
**Owner:** [OWNER OR TEAM]
**Last reviewed:** [DATE]

This document owns project intent and the project-level contracts that do not yet need a
separate specification. Link any concern that already has a stronger canonical source.

## Purpose and users

[What the product is, who it serves, and the problem it solves. Include the longer-term
direction only when it explains present decisions; state clearly what is not being built.]

## Success

[A small set of observable product outcomes or quality budgets.]

## Scope and non-goals

**In scope:**

- [First-release capability or constraint.]

**Not in scope:**

- [Tempting adjacent work that agents must not add speculatively.]

## Constraints and delegated choices

- Fixed: [platforms, vendors, compatibility, budget, locale, legal or operational limits].
- Delegated: [choices agents may make and what they should optimize for].
- Requires owner/user decision: [known sensitive or hard-to-reverse categories].

## Outcomes and behavior

[Describe the primary outcome or flow and important edge/failure behavior precisely enough
to plan and verify. Add interfaces, publication formats, workflows, or policy sections
only when relevant.]

## Delivery or system shape

```text
[Small component/request/data-flow diagram if it clarifies the system.]
```

| Concern | Choice | Rationale and material alternatives |
|---|---|---|
| [Concern] | [Choice] | [Why; what was rejected and why] |

Canonical specialist sources: [data/source index, API schema, package configuration,
separate technical spec, style guide, research protocol, or other authoritative paths].

## Data, trust, and safety invariants

- [One-sentence guarantee for each real trust/security/data-preservation boundary.]
- Enforcement: [the trusted layer and why a caller cannot bypass it].
- Verification: [how a least-privileged or failure-path check proves it].

[Omit trust/safety machinery that the product does not have. Create a dedicated data model
or policy only when this section can no longer stay precise and navigable.]

## Operations and quality

- Supported environment: [runtime/deployment shape].
- Schema/change mechanism: [migration or equivalent].
- Required quality gates: [commands or links].
- Human-only operations: [accounts, payment, production access, irreversible actions].

## Open questions

| ID | Question | Blocking for | Options / recommendation |
|---|---|---|---|
| O-001 | [Question] | [Milestone or decision point] | [Candidates and recommended default] |
