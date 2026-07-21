# Implementation Guide — QuePaso

**This is the primary working document.** It mirrors the flow of real development: sprints
in order, each with concrete steps, references to the specs, and acceptance criteria that
must pass before moving on. It is written to be ingested by LLMs across many sessions.
Agent operating rules (commits, work log, blocking protocol) live in `../AGENTS.md`.

How to use in a session:
1. Find the first sprint whose acceptance criteria are not yet met (check the tracker below).
2. Re-read the referenced spec sections for that sprint.
3. Build, verify criteria, update the tracker checkboxes, commit.
4. Behavior questions → `product-spec.md`. Schema questions → `data-model.md`. Settled
   decisions → `decisions-log.md` (don't relitigate). New ambiguity → add to the
   decisions log's open list and ask the owner.

## Progress tracker

- [x] Sprint 0 — Foundations *(local skeleton done + verified; hosted deploy — step 7 — deferred by owner 2026-07-06, see worklog "Pending owner tasks")*
- [x] Sprint 1 — Schema + read-only map
- [x] Sprint 2 — Auth + pin composer
- [x] Sprint 3 — Threads: panel, comments, photos, likes
- [x] Sprint 4 — Feed, profiles, search
- [x] Sprint 5 — Moderation + hardening
- [x] Sprint B — Branding & visual identity *(extra sprint before launch; see `docs/brand-guide.md` + decisions-log P11)*
- [x] Sprint C — UX/UI polish *(extra sprint before launch; map locate-on-load, teardrop pins, panel declutter, topbar — decisions-log P12)*
- [x] Sprint D — Social UX/UI pass *(extra sprint before launch; rail feed modes, decluttered thread, Waze-style composer, warm accent — decisions-log P13)*
- [x] Sprint E — Map "feel alive" pass *(extra sprint before launch; category glyphs on teardrops, cluster zoom-to-fit + mini-list, looser clustering — decisions-log P14)*
- [x] Sprint F — Shareable pins *(extra sprint before launch; CTA share menu + native sheet/X-intent, base62 short links — decisions-log P15)*
- [ ] Sprint 6 — Production launch (see `deployment-guide.md`)

---

## Sprint 0 — Foundations

**Goal:** running skeleton: Next.js app + local Supabase + CI-less deploy pipeline.

1. `git init`; commit the docs set and `prompt.txt`.
2. Scaffold: `npx create-next-app@latest web --typescript --tailwind --app --eslint`
   (project lives in `web/`, Supabase config at repo root).
3. Add shadcn/ui (`npx shadcn@latest init`) and base deps:
   `@supabase/supabase-js @supabase/ssr @tanstack/react-query maplibre-gl react-map-gl
   browser-image-compression exifr`.
4. Install Supabase CLI; `supabase init`; `supabase start` (requires Docker). Record local
   URLs/keys in `web/.env.local` (`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`).
5. Create `lib/supabase/` client helpers (browser + server, per `@supabase/ssr` docs) and
   `lib/strings.ts` (all Spanish copy lives here — architecture §4).
6. App shell: layout with bottom nav on mobile / top nav on desktop — Mapa, Novedades,
   Nuevo (+ placeholder routes). Static `/acerca`, `/reglas` pages.
7. Create the hosted Supabase project (region: `sa-east-1` São Paulo — closest to Rosario)
   and the Vercel project linked to the repo; set env vars for the hosted instance in
   Vercel. Deploy the skeleton.

**Acceptance:** app runs locally against local Supabase; deployed skeleton loads on a
Vercel URL; nav works on mobile viewport; all copy renders from `strings.ts`.

---

## Sprint 1 — Schema + read-only map

**Goal:** the full database exists; the map shows seeded pins. *(Spec: product §4, §6.1, data-model all.)*

1. Migration 1: `create extension postgis;` + all tables from `data-model.md` §2.
2. Migration 2: triggers/functions (§3) — including `extend_lifecycle` and
   `activity_state()` for the activity lifecycle (product §6.1) — RLS policies + public
   views (§5), read RPCs (`pins_in_bbox`, `nearby_pins`, `feed`).
3. Seed script (`supabase/seed.sql`): ~30 realistic Rosario pins (varied locations around
   the centro/Pichincha/zona sur, tags like `bache`, `basura`, `alumbrado`, mixed
   anonymous/named, varied ages for hot-score spread) + 3 fake users + comments + likes.
   Include lifecycle variety: several `dormant` pins (past `expires_at`) and at least
   one `fading` (expiring within 24h).
4. `MapView`: MapLibre via react-map-gl, OpenFreeMap `liberty` style, initial center
   Plaza 25 de Mayo (-60.6304, -32.9442) zoom 14; geolocate control that recenters on the
   user (product §4).
5. Viewport loading: `moveend` → debounced `pins_in_bbox` → GeoJSON source with
   `cluster: true`; cluster bubbles click-to-zoom; individual pins colored/iconed
   (`color`/`icon` → sprite or styled marker). Lifecycle pin styles (product §6.1):
   `fading` = amber pulse; `dormant` = desaturated gray ghost, ~70% size, ~50% opacity,
   sorted under active pins.
6. Desktop hover popup (title, thumb placeholder, like count, relative age). Skip on touch.
7. Clicking a pin routes to `/p/{id}` (shallow) and opens a placeholder panel.

**Acceptance:** panning/zooming loads pins for the viewport only (network tab shows bbox
RPC); clusters split on zoom; hover popup works on desktop and doesn't break mobile; a
seeded low-zoom view shows the highest-hot-score pins (verify against SQL directly);
seeded dormant pins render as ghosts and sort below active ones in the RPC result.
`select * from pins_public` as `anon` returns no author fields for anonymous seed rows.

---

## Sprint 2 — Auth + pin composer

**Goal:** a real user can log in with Google and publish a pin with photos.
*(Spec: product §3, §5, §9.)*

1. Google OAuth: configure in Google Cloud Console + Supabase dashboard (and
   `supabase/config.toml` for local). Login button in nav; `handle_new_user` trigger
   verified (profile row appears).
2. Auth-gate pattern: attempting a gated action while logged out opens a login dialog
   (product §11 note — buttons visible, gated on click).
3. Composer `/nuevo` as a two-step wizard:
   - **Step 1 Location:** full-screen map with fixed center crosshair; Photon search box
     to jump the map; on confirm, reverse-geocode via Nominatim → prefill editable
     `address_text`, derive `city`/`province` (fallback: Rosario/Santa Fe).
   - **Step 2 Details:** title, description, `TagInput` (normalize per data-model trigger
     rules client-side too), `PinStylePicker` (8 colors × 12 icons — define the sets in
     `strings.ts`/constants), `PhotoUploader`, `AnonToggle` with the honesty copy
     (product §3.2 — exact wording matters).
4. `PhotoUploader` pipeline (product §9, in this order): validate type/size/count →
   `exifr.parse()` full EXIF + SHA-256 of original → `browser-image-compression` to
   full (≤2048px webp) and thumb (≤400px) → upload both to `photos` bucket →
   `register_photo` RPC with EXIF JSON + hash. Show per-file progress; failures removable.
5. Submit via `create_pin` RPC; on success route to `/p/{id}`.
6. Author affordances: 24 h edit (title/description/tags, `edited_at` badge), delete with
   confirm. "Publicado como anónimo" badge for own anonymous content.

**Acceptance:** end-to-end publish from a phone-sized viewport in <2 min; uploaded files
contain zero EXIF (verify with `exiftool`); `photo_metadata` row has the EXIF (verify as
admin); anonymous pin shows "Anónimo" in a second browser session; rate-limit trigger
rejects the 11th pin of the day with a friendly Spanish error.

---

## Sprint 3 — Threads: panel, comments, photos, likes

**Goal:** the detail panel is the product's heart — full history view + pile-on actions.
*(Spec: product §6, §6.1, §7.)*

1. `PinPanel`: desktop right side panel over the map / mobile draggable bottom sheet.
   SSR the `/p/{id}` route for OpenGraph tags (title, description excerpt, first photo).
2. Header per product §6 (AuthorChip, like button, share = copy link, report placeholder).
3. `PhotoGallery`: chronological, attributed, lightbox on tap; pin photos + comment
   photos interleaved by date — this is the "history of the pothole" view.
4. Comments: list + composer (text, ≤4 photos via the same uploader, AnonToggle). No
   nesting. Pagination beyond 50.
5. Likes: `toggle_like` RPC with optimistic update; count on pin popup, panel, and cards.
6. `NearbyList` ("Otros pines cerca") via `nearby_pins` RPC; clicking swaps the panel.
7. Lifecycle UI in the panel (product §6.1): `fading` banner ("Este pin se archivará
   mañana. ¿Sigue pasando?") and `dormant` banner ("Archivado por inactividad. Comentá o
   subí una foto para reactivarlo."); state badge in the header.
8. Verify hot-score behavior end to end: like/comment/photo actions should visibly
   reprioritize pins at low zoom after refetch.

**Acceptance:** a second account can comment with a photo (counts toward `photo_count` and
hot score); anonymous comment shows "Anónimo" to others but "vos (anónimo)" to its author
in Mis pines; like toggles optimistically and survives refresh; deep link `/p/{id}`
shows a social card preview (test with an OG debugger); back button closes the panel.
Lifecycle: a non-author comment on a seeded dormant pin revives it (ghost → normal pin
after refetch); a non-author like extends `expires_at` by 48h; the author's own comment
does not move `expires_at` (verify in SQL, including on an anonymous pin).

---

## Sprint 4 — Feed, profiles, search

**Goal:** the doomscroll surface and identity pages. *(Spec: product §8, §11.)*

1. `/novedades`: tabs **Nuevos** (reverse-chron) / **Populares** (hot score), both via the
   `feed` RPC with cursor pagination + infinite scroll. Card per product §8. City filter
   UI: fixed to Rosario for MVP but read from the RPC param (no hardcoding below the UI).
2. Freshness: TanStack Query `staleTime` ~30 s + refetch on focus; pull-to-refresh feel on
   mobile ("real-time-ish" — architecture §1, no websockets).
3. Tag search: search box filtering the feed by exact tag; tapping a hashtag anywhere
   routes here pre-filtered.
4. `/perfil`: username edit (uniqueness error handling), Mis pines (includes anonymous,
   badged), Mis comentarios.
5. `/u/{username}`: public profile — **non-anonymous content only** (must come from public
   views; re-verify no anonymous leakage via this surface).
6. Empty states everywhere (Spanish, friendly): empty map area, no results for tag, etc.

**Acceptance:** feed paginates smoothly on a mid-range phone; new pin from another
session appears after tab refocus without hard reload; tag tap → filtered feed; dormant
pins appear in neither feed tab but do appear in tag search and profiles; public
profile of a user with anonymous posts shows only their named content (verify with a user
that has both).

---

## Sprint 5 — Moderation + hardening

**Goal:** the abuse baseline the product must not launch without. *(Spec: product §10,
`moderation-policy.md`.)*

1. `ReportDialog` on pins, comments, photos: reason picker + optional details;
   `create_report` RPC; "gracias" confirmation; duplicate report by same user → friendly
   "ya lo denunciaste".
2. Auto-hide trigger verified: 3 distinct-user open reports → content hidden, author sees
   "en revisión" notice on their own content.
3. `/admin` (role-gated by `profiles.role`, plus middleware check):
   - Queue of open reports grouped by target, newest first; full content preview
     **including real author of anonymous content** (this is the one sanctioned surface).
   - Actions: dismiss (unhides if auto-hidden), hide, delete, ban user — each via admin
     RPC, each writing `moderation_actions`.
   - Simple moderation log view.
4. Hardening pass: rate limits verified for all four caps; banned user gets clear error;
   `photo_metadata` inaccessible to non-admins (write a SQL test); orphan upload check
   documented as a manual chore; Sentry (free tier) wired into Next.js.
5. Legal/footer: contact email, links to `/reglas` (content from `moderation-policy.md`)
   and a minimal privacy note that states the anonymity guarantee and EXIF retention
   policy in plain Spanish. **The EXIF retention must be disclosed.**
6. Playwright smoke test: login (mocked/test user) → publish pin with photo → comment
   anonymously → like → report → admin dismisses.

**Acceptance:** the smoke test passes; a non-admin hitting `/admin` is redirected; every
admin action appears in the log; report → 3 accounts → auto-hidden → admin dismiss →
visible again, all through the UI.

---

## Sprint 6 — Production launch

Follow `deployment-guide.md` end to end. Definition of done for the MVP:

- Production URL on **quepaso.com.ar**, Google OAuth working on that domain.
- Seed data replaced by ~15 real, hand-created Rosario pins (founder-generated content —
  the map must not be empty on day one).
- Admin account provisioned; moderation queue reachable from a phone.
- Backups confirmed (Supabase daily backups active), Sentry receiving events,
  analytics counting visits.
- A `docs/runbook.md` written during this sprint: how to moderate, how to ban, how to
  restore a backup, known limits (free-tier pause, Nominatim rate policy).

---

## Standing rules for all sprints

- **Anonymity review** on every PR that touches queries/views: no `author_id` from base
  tables to the client; every `profiles` join masked (data-model §5 checklist).
- Migrations only via `supabase/migrations/` — never hand-edit the hosted DB.
- All Spanish copy in `lib/strings.ts`; code/comments in English. The entity is `pin` in
  code regardless of any future brand rename.
- Mobile-first: verify each feature at 390 px width before calling it done.
- Update the progress tracker and `decisions-log.md` as part of each sprint's final commit.
