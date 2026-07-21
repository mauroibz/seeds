# Moderation Policy — QuePaso (MVP stub)

Working document. The user-facing Spanish version of §2 becomes the `/reglas` page in
Sprint 5. This stub is deliberately minimal; it grows when the tenant/landlord layer
(higher legal risk) is built.

## 1. Principles

- QuePaso hosts reports about **places and conditions**, in public interest. It is
  not a tool for harassing **people**.
- Content stays up by default; removal requires a rule violation, not mere disagreement.
- Anonymity protects authors from the public, not from accountability: the platform can
  identify, rate-limit, and ban anonymous abusers (see product spec §3.2).
- Moderation is human and reactive for MVP: users report, one admin reviews.

## 2. Content rules (basis for /reglas)

Not allowed:
1. **Datos personales de terceros** — publishing names, phone numbers, plates, faces of
   private individuals as the *target* of a complaint. Complaints target places,
   businesses, and conditions. (Public officials acting publicly and business names are
   acceptable.) Incidental faces in photos are tolerated at MVP; blurring is a v2 feature.
2. **Acoso o agresión** — threats, slurs, incitement, campaigns against an individual.
3. **Contenido falso deliberado** — staged or misattributed photos, wrong-location spam.
4. **Spam comercial** — ads disguised as pins, coordinated promotion or defamation of
   competitors.
5. **Contenido ilegal o explícito** — anything unlawful in Argentina, sexual content,
   gore beyond what documenting the issue requires.
6. **Suplantación** — impersonating other people, officials, or organizations.

## 3. Enforcement pipeline (implemented in Sprint 5)

1. Any logged-in user reports content with a reason
   (`spam` / `ofensivo` / `info_personal` / `lugar_incorrecto` / `otro`).
2. **3 open reports from distinct users** auto-hide the content pending review (author
   sees "en revisión"; the public doesn't see it).
3. Admin reviews in `/admin`: **dismiss** (restore) / **hide** / **delete** / **ban user**.
   All actions logged in `moderation_actions`.
4. Review SLA (aspirational, single admin): 48 h.
5. Repeat offenders: second deliberate violation → ban. Ban = `profiles.is_banned`,
   blocks all writes; content stays unless it violates rules itself.

## 4. Takedown and legal requests

- Footer contact email for removal requests from affected parties (e.g., a business owner
  disputing a claim). MVP handling: manual, case-by-case, err toward keeping factual
  complaints and removing personal attacks.
- Argentina context to keep in mind (this is why the tenant/landlord layer waits):
  defamation exposure (calumnias e injurias) and personal-data law (Ley 25.326). For MVP's
  pothole/street-level content, risk is low; escalate to actual legal review before
  building landlord reviews.

## 5. Known gaps (accepted for MVP, logged)

- No automated detection (CSAM/NSFW scanning, perceptual duplicate detection) — the
  `photo_metadata` hashes are the future hook.
- No reporter feedback loop ("tu denuncia fue aceptada").
- No appeal flow beyond emailing the contact address.
- Single admin is a bus-factor and burnout risk; community moderators are a v2 topic.
