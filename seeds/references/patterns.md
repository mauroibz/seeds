# Optional design patterns

These heuristics emerged from projects run with Seeds. They are not the Seeds operating
method and must not be applied without checking the domain, scale, and existing design.

## Put trust boundaries in a trusted layer

Authorization, tenant separation, protected identity, and paid/free access should be
enforced where an untrusted caller cannot bypass them. Frontend filtering is presentation,
not a security boundary. State the guarantee in one sentence and test it as the
least-privileged relevant caller.

This does not mean every project must enforce access in a database. Use the server,
database policies, gateway, or other layer that actually controls access, and document why
it is trusted.

## Preserve raw signals when future interpretation matters

Votes, reports, reactions, and audit events are often more useful as rows/events than as a
bare counter. Raw records retain provenance and allow later anti-abuse or reconciliation
logic. A counter may still be appropriate when individual signals have no product,
privacy, audit, or correction value.

## Derive time-based state when practical

If a state is purely a function of timestamps, deriving it at read time can avoid a batch
job, lag, and special-case revival logic. Materialize or batch it only when measured read
cost, query capabilities, or external side effects justify doing so.

## Stabilize expensive internal vocabulary

Choose durable names for core entities before migrations and public APIs make renaming
costly. Keep user-facing terminology replaceable through the localization or presentation
mechanism appropriate to the stack. A single strings module is one option, not a universal
architecture requirement.

## Record rejected alternatives

A technology choice without its rejected alternatives invites a later agent to reintroduce
an option that was already considered. Record alternatives when the trade-off is material;
do not create decision records for routine choices.

## Measure before committing to uncertain architecture

When feasibility, provider behavior, performance, or migration cost is unknown, use a
gated investigation milestone. Phase A measures and produces a verdict. Phase B happens
only if the evidence and user authorization justify it. "Do not build" is a successful
outcome when the measurement supports it.
