# Product Spec — {{PROJECT_NAME}}

[Reference: `03-case-study-quepaso/product-spec.md` for a fully worked example of every
section below at real depth.]

## 1. Concept

[One paragraph: what it is, what the core content object is and what it does over
time (accumulates history? gets consumed once? decays?). Define terminology here if
the internal/code name differs from the current brand name (Phase 3 of the
methodology) — state the rule explicitly: code/schema use {{ENTITY_NAME}} permanently;
only the UI-strings module changes if the brand changes.]

[If there's an explicit long-term direction this MVP is a step toward but is NOT
building yet, restate it here and name which current decisions it's informing.]

## 2. Scope

- Geography/locale/language constraints.
- Platforms (web/mobile/native).
- Domain/product name, if decided.

## 3. Identity and any trust boundary

### 3.1 Accounts
[Auth method(s), what happens on first login, what's public without an account vs.
gated.]

### 3.2 [Anonymity / admin vs. user / any other protected-identity feature]
[State exactly what the protection covers and doesn't — hidden from whom? State the
enforcement mechanism at a product level here (detail goes in data-model.md's security
boundary section). State the UI-honesty requirement: never imply a stronger guarantee
than what's actually enforced.]

## 4. The [primary screen]

[Describe the main screen's layout and behavior in enough detail that a frontend dev
could build it without guessing. Call out what's different on mobile vs. desktop.]

### 4.1 Behavior
[Pagination/loading strategy, ranking/ordering if any, real-time-ish freshness
strategy.]

### 4.2 [Core content-object model decisions]
[E.g., dedup/aggregation model, one-object-per-submission vs. merged entities — whatever
was flagged as an open question in the brief and has now been settled.]

## 5. Creating [the core content object]

[Composer flow, step by step. Field-by-field validation limits. What's required vs.
optional. Any anonymity/visibility toggle and its default.]

## 6. [Detail view / thread / core interaction surface]

[What the detail view shows, in what order. Comment/reply model if any (nesting?
limits?). Anything that "counts toward" a ranking score, and why.]

### 6.1 [Lifecycle/expiry/state-decay section — OMIT if not applicable]
[Only include this section if the content object has a genuine time-decay property.
States table (condition → behavior), timer/re-arm rules, and the explicit statement
that decay ≠ deletion ≠ resolution if those are three different things in your domain.
See quepaso product-spec.md §6.1 for the full worked pattern — states derived at read
time, weighted re-arm rules, "revival" handled by the same rule that created the state.]

## 7. [Ranking / scoring, if applicable]

[The formula and its rationale, even if approximate: what inputs, what decay function.
State explicitly whether the underlying signals are stored as rows (recommended, see
METHODOLOGY.md's patterns section) or as bare counters, and why.]

## 8. [Discovery / feed surface, if separate from the primary screen]

[What ordering(s), what filters, freshness strategy.]

## 9. [User-generated content handling — photos/files/etc., if applicable]

[Size/format/count limits. Any metadata stripping or retention policy — state the
"what's public vs. what's retained privately and why" split explicitly if there is one.]

## 10. Moderation and abuse (MVP baseline)

[Point to `trust-and-safety-policy.md` for the full policy; summarize the mechanism
here: report/flag flow, auto-hide threshold if any, admin queue, rate limits.]

## 11. Screens inventory

| Route | Screen | Auth |
|---|---|---|
| | | |

## 12. Non-goals for MVP (explicit)

[Everything you're deliberately not building yet, one line each, so nobody "helpfully"
builds it mid-sprint. Cross-reference anything deferred in the decisions log by its
open-question number.]
