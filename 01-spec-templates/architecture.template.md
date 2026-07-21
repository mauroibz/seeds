# Architecture Spec — {{PROJECT_NAME}}

[Reference: `03-case-study-quepaso/architecture.md` for a fully worked example.]

Backend and frontend component map, plus every delegated technology choice with
rationale. Guiding constraints: [restate the budget/maintenance/scale constraints from
the brief — they justify every row below].

## 1. Technology choices (decided)

[This table is the single highest-value artifact in this document. Every row needs
both a rationale AND an alternatives-considered note — writing down what you rejected
and why is what stops a later session from "helpfully" swapping it back in.]

| Concern | Choice | Rationale / alternatives considered |
|---|---|---|
| Backend platform | | |
| Database | | |
| Frontend framework | | |
| UI | | |
| [Domain-specific: map/rendering, real-time layer, etc.] | | |
| File/media hosting | | |
| Data fetching / caching | | |
| Hosting | | |
| Domain | | |
| Analytics | | |
| Testing | | |

Costs at MVP scale: [state the actual expected number, even if it's ~$0/month plus one
fixed cost like domain registration — this is a real constraint worth restating here].

## 2. System overview

```
[ASCII or simple diagram: client → what it talks to directly → backend services.
Keep it to the actual request paths, not an aspirational future architecture.]
```

[State plainly whether there's a custom API server or not, and why. If there isn't
one — e.g. the database's own security/access-control layer plus generated
views/functions/RPCs is the entire API surface — say so explicitly; it's an
unusual-enough choice that future sessions need it stated, not inferred.]

## 3. Backend components

[Component-level map only — schema detail lives in data-model.md.]

### 3.1 Auth
### 3.2 Data access layers (the trust/security boundary)
[Tiers: base storage → what enforces access control on it → any public-facing
views/derived surfaces that mask sensitive fields. State which layer is the ONE
mechanism that guarantees a sensitive field (e.g. a real identity behind an anonymity
flag) never reaches an unauthorized client. This should be a single sentence you could
quote back during any future code review.]
### 3.3 Storage
### 3.4 [Moderation/abuse machinery, if applicable]

## 4. Frontend components

```
[Directory tree sketch: routes/pages, key components, shared lib modules
(especially the one that owns ALL user-facing strings, per Phase 3 of the
methodology).]
```

Key frontend behaviors:
[Loading/query strategy, URL↔state sync for deep-linkable views, auth-gating pattern
(prompt to log in vs. hide the action — usually prompt, for conversion), the
strings-module rule restated.]

## 5. Cross-cutting decisions

- IDs: [scheme].
- Time: [storage/rendering convention].
- SEO, if relevant.
- Error tracking.
- Secrets: [which env vars actually exist, and the explicit statement of what NEVER
  goes in the repo or the hosting provider's env config — e.g. a service-role/admin key].
