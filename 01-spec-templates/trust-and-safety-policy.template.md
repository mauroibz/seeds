# Trust & Safety Policy — {{PROJECT_NAME}} (MVP stub)

[Reference: `03-case-study-quepaso/moderation-policy.md` for a fully worked example.
Ship this even as a deliberately minimal stub for any product with user-generated
content — "no policy yet" is a worse position than "minimal policy, known gaps logged."]

Working document. The user-facing version of §2 becomes a real policy page in the
sprint that builds moderation UI. This stub grows if the product later adds a
higher-legal-risk layer (name it here if one is planned, per the brief's "later, not
now" framing).

## 1. Principles

- [What the product protects/allows — restate the core content-vs-people distinction
  if applicable, e.g. "this hosts reports about X, not a tool for harassing people."]
- Content stays up by default; removal requires an actual rule violation, not mere
  disagreement.
- [Restate the anonymity/identity guarantee from product-spec §3.2 here in one line:
  what it protects from whom, and that the platform can still act on abuse despite it.]
- Moderation posture at MVP: [human/reactive vs. automated — usually human+reactive
  at MVP].

## 2. Content rules (basis for the public policy page)

Not allowed:
1. [Personal data of third parties, if relevant to the content type.]
2. [Harassment/targeting of individuals.]
3. [Deliberately false/misattributed content.]
4. [Commercial spam / disguised advertising.]
5. [Illegal/explicit content per your jurisdiction.]
6. [Impersonation.]

## 3. Enforcement pipeline

1. Report flow: reason categories, who can report.
2. Auto-hide threshold, if any (e.g. N distinct-user reports).
3. Admin review actions and where they're logged.
4. Review SLA (aspirational is fine at MVP with a single admin).
5. Repeat-offender / ban policy.

## 4. Takedown and legal requests

- Contact channel for affected-party disputes.
- [Any real jurisdiction-specific legal context worth naming now, even briefly — e.g.
  defamation exposure, data-protection law — so the "not building the risky layer yet"
  decision from the brief has a documented reason.]

## 5. Known gaps (accepted for MVP, logged)

- [No automated detection — name what the future hook would be, if the data model
  already retains anything useful for it, e.g. content hashes.]
- [No reporter feedback loop.]
- [No appeal flow beyond direct contact.]
- [Bus-factor risk of a single admin, if applicable.]
