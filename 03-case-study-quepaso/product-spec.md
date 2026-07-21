# Product Spec — QuePaso (MVP)

## 1. Concept

A public, persistent map of location-anchored threads called **pins**. Anyone can drop a
pin, describe what's happening there, attach photos, and tag it. Others like it
(Waze-style validation), comment on it, and add their own photos. Pins accumulate history:
the 6-month-old pothole shows its original report, photo updates over time, and neighbors
piling on in comments. The map of top pins paints a picture of the city.

Terminology: a **pin** is the content object (the geo-anchored thread); an **issue** in
this document means the real-world problem a pin documents. "Pin" is also the current
user-facing name (Spanish: "pin", plural "pines") — if the brand evolves, only UI strings
change (see `lib/strings.ts` rule), never code or schema.

Long-term direction (explicitly **not** in this MVP): tenant/landlord reviews à la
Glassdoor/tusecreto. That future informs two MVP decisions — anonymity is first-class, and
moderation exists from day one — but the tenant use case is just one example of a pin,
not the schema.

## 2. Scope

- **Geography:** Argentina only. Rosario, Santa Fe is the launch city. Pins can technically
  be placed anywhere in Argentina; the feed and defaults center on Rosario.
- **Language:** Spanish (es-AR) UI. Single-language architecture; don't build i18n
  scaffolding, but keep user-facing strings in one module so extraction later is mechanical.
- **Platforms:** Responsive web (mobile-first). No native apps.
- **Domain:** quepaso.com.ar (final).

## 3. Identity and anonymity

### 3.1 Accounts
- Login: **Google SSO via Supabase Auth** only, for MVP. Supabase's `auth.users` +
  `auth.identities` model already supports multiple providers per user, so adding
  email/password or other OAuth providers later requires no schema rework.
- On first login, a `profiles` row is auto-created: generated unique username (editable),
  display name and avatar from Google.
- **Reading is public.** Browsing the map, pins, and feed requires no account.
  Creating pins, commenting, liking, adding photos, and reporting require login.

### 3.2 Publish as anonymous (core feature)
Every write action — pin, comment, photo, like — carries an `is_anonymous` flag chosen at
submission time (a visible toggle in every composer, default **off**).

**What anonymity protects (decided):** identity is hidden from *other users*, not from the
platform. Concretely:
- The author's user id is stored on every row, anonymous or not.
- Public reads go through database views that null out author fields when
  `is_anonymous = true`. The real author id **never reaches the client** for anonymous
  content — this is enforced in the database layer, not by frontend filtering.
- Admins/moderators can see the real author (for bans, rate limits, spam investigation,
  legal compliance).
- The author themself sees their own anonymous posts as theirs ("Mis pines" includes them,
  marked with an anonymous badge) and can delete them.

**UI honesty requirement:** the anonymous toggle's helper text must state the actual
guarantee, e.g. *"Tu identidad queda oculta para otros usuarios, pero no para el equipo del
sitio."* Never imply stronger anonymity than we provide.

Anonymous likes hide *who* liked from other users; the like still counts and still enforces
one-like-per-user.

## 4. The map (primary screen)

The home screen puts the map at the center, flanked by two lists so the three
zones read as **viewport feed (left) · map (center) · pin detail (right)**:
- **Desktop:** the map is full-bleed; the two lists are overlay rails floating
  over its left and right edges. The left rail (**"En esta zona"**, §4.3) is
  always present; the right detail panel appears only when a pin is selected.
- **Mobile:** the map sits on top (~45 % height, collapsible via a toggle) with
  the viewport feed scrolling below it; the pin detail is a bottom sheet.

The map is centered on the user's location (browser geolocation, with
permission); fallback center is Plaza 25 de Mayo, Rosario (-32.9442, -60.6304),
zoom ~14.

### 4.1 Behavior
- **Pan/zoom freely.** Pins load for the current viewport via a bounding-box query.
- **Pin density / low zoom:** the viewport query returns at most N (~200) pins,
  **prioritized by hot score** (see §7), so at low zoom the most relevant pins win.
  Client-side clustering (MapLibre native clustering) groups nearby pins into count
  bubbles; **clicking a cluster zooms to fit its pins** (`fitBounds` on the leaves), and
  when the pins sit on effectively the same spot it opens a **mini-list** of them instead,
  so a cluster is always "openable" (Sprint E / decisions-log P14).
- **Desktop hover:** mousing over a pin shows a compact summary popup (title, first photo
  thumbnail, like count, age). Hover does not exist on mobile — this is a desktop
  enhancement only.
- **Click/tap a pin:** opens the **detail panel** — a side panel on desktop, a bottom sheet
  on mobile — with the full thread (see §6). The map stays visible behind/beside it.
- Each pin renders as a **colored teardrop with its category glyph in the head** (its
  submission-chosen color + icon, §5), modulated by activity state (§6.1): `fading` pins get
  an amber pulse; `dormant` pins render as desaturated, smaller, semi-transparent ghosts and
  sort below all active pins in the viewport query.

### 4.2 Pin model (decided)
**One pin per report.** Two reports at the same address are two pins and two independent
threads; no automatic deduplication or shared "place" entity. Duplicates are handled:
- socially — users are expected to like/comment the existing pin instead;
- by the detail panel showing an **"Otros pines cerca"** list (pins within ~500 m —
  widened from 150 m at launch, 2026-07-08, because 150 m left the list almost always empty;
  tunable, tighten as the map fills in);
- later (v2, logged) — an admin merge tool.

### 4.3 Viewport feed ("En esta zona")

> **Sprint D update (P13):** the rail is now the single browsing surface. A
> **Cerca · Nuevos · Populares** segmented control (plus a tag search) lets the
> user switch between the map viewport (this section) and the city-wide feed
> (§8) *without leaving the map*. "Cerca" is the behavior described below;
> "Nuevos"/"Populares" render the `feed` RPC (paginated, with cover thumbs).
> Novedades is therefore folded into this rail rather than a separate screen.

A live list of the pins currently in the map viewport, sharing the exact same
data as the map markers (the hot-ordered bounding-box query, §4.1 / §7 — no extra
fetch). It re-syncs as the user pans/zooms.
- **Card** = the same card as the feed (§8): icon/color, title, address, byline
  ("Anónimo" when anonymous), activity badge, like/comment counts. No cover
  thumbnail in this rail (a viewport can hold ~200 pins and refetches on every
  pan; thumbnails are a later, throttled enhancement).
- Ordered by hot score like the map query, so active/new pins surface first;
  **dormant ghosts are included** here (they're visible on the map). No sort
  toggle in v1.
- Clicking a card opens that pin's detail panel in place and flies the map to it;
  the selected card is highlighted. Cards remain real `/p/{id}` links, so
  middle-click / open-in-new-tab still work.

## 5. Creating a pin

Composer flow (requires login):
1. **Location** — the source of truth is a point the user places by tapping the map /
   dragging a crosshair. An address search box (geocoder) is a convenience to move the map,
   and reverse geocoding suggests a display address (`address_text`), which the user can
   edit freely as text. City/province are derived from the reverse geocode and stored as
   plain text columns for feed filtering (default: Rosario / Santa Fe).
2. **Title** — required, ≤120 chars.
3. **Description** — required free text, ≤5,000 chars.
4. **Photos** — 0–10 images. Processed client-side before upload (see §9).
5. **Hashtags** — optional, ≤10, normalized to lowercase without `#` (e.g. `bache`,
   `alquiler`). Free-form; **no fixed categories exist**.
6. **Pin style** — the only categorization: choose a pin **color** (from a fixed palette
   of ~8) and **icon** (from a fixed set of ~12 generic glyphs: warning, trash, water,
   road, building, food, tree, light, noise, animal, security, other).
7. **Anonymous toggle** (§3.2).

Publishing is immediate — **all pins are public** (decided: no drafts, no private or
unlisted states). The only lifecycle states are `published`, `hidden` (by moderation), and
`deleted`. Authors can edit title/description/tags for 24h (edited badge) and delete anytime.

## 6. Threads (pin detail)

The detail panel shows:
- Header: title, pin icon/color, address text, age ("hace 6 meses"), author (or "Anónimo"),
  like button with count, share button (copies deep link `/p/{id}`), report button.
- Photo gallery: original photos plus later photo additions, in chronological order, each
  attributed (or "Anónimo") and dated — this *is* the visual history of the pin.
- Description.
- Hashtags (tappable → search).
- Comments: flat chronological list (no nesting in MVP). Each comment: text ≤2,000 chars,
  optional photos (≤4), anonymous toggle, report button.
- **Photo additions count toward relevance:** a comment with photos contributes extra hot
  score (§7), because fresh photo evidence is the strongest "this is still real" signal.
- "Otros pines cerca" list (§4.2).

Comments are enabled on every pin, always; there is no way to close a thread in MVP.

### 6.1 Activity lifecycle (expiry) — ships in MVP

Pins carry a sliding activity timer. When it runs out they **never disappear — they go
dormant** ("archivado"), and any new interaction revives them. This reconciles the
declutter goal with the permanence goal (§1's 6-month pothole survives *because* neighbors
keep piling on).

**States** (derived from `expires_at` at read time — no background jobs):

| State | Condition | Behavior |
|---|---|---|
| `active` ("activo") | `expires_at` > now + 24h | Normal pin, in feed, normal ranking |
| `fading` ("por archivarse") | `expires_at` within 24h | Amber pulsing pin; thread banner: *"Este pin se archivará mañana. ¿Sigue pasando?"* — the keep-alive nudge. Still in feed and ranking. |
| `dormant` ("archivado") | `expires_at` in the past | Ghost pin: desaturated gray, ~70% size, ~50% opacity, ranked below all active pins in viewport queries. **Excluded from the feed** (both tabs). Still reachable via deep link, tag search, profiles, and "Otros pines cerca". Thread banner: *"Archivado por inactividad. Comentá o subí una foto para reactivarlo."* |

**Timer rules (weighted: content > likes):**
- Creation arms the timer: **14 days** at launch (tunable constant; tighten toward 7 as the
  community grows — revisit post-launch).
- A **comment or photo from someone other than the pin author** re-arms the full window:
  `expires_at = greatest(expires_at, now() + 14 days)`.
- A **like** from a non-author extends only **48 hours** under the same `greatest()` rule.
- **Author self-bumps extend nothing.** The check uses the internal `author_id`, so it
  works on anonymous content too.
- Deleting an interaction does not retract time already granted.
- **Revival is automatic and uniform:** the same `greatest()` rule applied to a dormant
  pin brings it back — a comment/photo revives it for a full window; a like revives it
  for 48h (a brief second life is acceptable and keeps the rule simple).

**Expiry is not resolution.** A dormant pothole is an ignored pothole, not a fixed one.
The "mark as solved" flow remains deferred (decisions log O1); when it arrives, `resolved`
will be a `status` value, visually distinct from `dormant`.

## 7. Likes and ranking

- One like per user per pin (comment likes: **no — likes are pin-level only in MVP**).
- Likes are stored as rows (`user_id`, `pin_id`, `is_anonymous`, `created_at`), never as
  a bare counter — this is deliberate, so v2 anti-gaming (bot detection, brigading analysis,
  weighting) has raw material. A denormalized `like_count` on the pin is maintained by
  trigger for cheap reads.
- **Hot score** (HN-style time-decayed): used to prioritize pins at low zoom and to rank
  any "top" lists.

  ```
  points = like_count*3 + comment_count*2 + photo_addition_count*2
  hot    = points / (age_hours + 2)^1.5
  ```

  Tune the constants freely; the shape (points over polynomial age decay) is the decision.
- Ranking interacts with the activity lifecycle (§6.1): viewport queries return active
  (including fading) pins first, then dormant, each group ordered by hot score.
- **Anti-gaming is a known, accepted v2 gap**: no bot detection, no vote-ring analysis, no
  per-IP limits in MVP beyond basic per-user rate limits (§10). The schema (likes-as-rows,
  private EXIF retention, internal author links on anonymous content) is designed so
  defenses can be added without migration pain.

## 8. Feed ("Novedades")

Twitter-style doomscroll, optimized for short frequent opens. City-wide and
place-name filtered, whereas the map's "Cerca" rail is scoped to what's currently
on screen. Both reuse the same card component.

> **Sprint D update (P13):** Novedades is no longer a separate screen — it lives
> as the **Nuevos / Populares** modes of the map rail (§4.3). The `/novedades`
> route still exists (deep links, shared feed URLs, `?tag=` filters) but renders
> the map home with the rail pre-set to the feed; hashtag taps land there too.
- Reverse-chronological list of newly published pins. Each card: title, first photo,
  pin icon/color, relative time, like/comment counts, address text, author or "Anónimo".
- **Dormant pins are excluded from both tabs** (§6.1); fading pins appear normally.
- Filtered by **place-name only** — country/province/city text columns. Default filter:
  Rosario. **No geolocation or distance math in this view** (decided in brief).
- Tapping a card deep-links to the pin (map centered on it, panel open).
- A secondary tab "Populares" ranks by hot score (same filter). Cheap to add, drives the
  voyeuristic-browsing goal.
- Freshness: MVP uses polling/refetch-on-focus (~30s stale time), not websockets.
  "Real-time-ish" is the bar; Supabase Realtime is a drop-in upgrade later.
- Hashtag search: a search box that filters the feed by tag (exact tag match, GIN-indexed).

## 9. Photos

Decided model: **anonymity in public images, private retention of original metadata.**

Client-side pipeline (before anything is uploaded):
1. Accept JPEG/PNG/WebP/HEIC input, ≤10 MB per file, up to 10 per pin / 4 per comment.
2. **Extract full EXIF** (via `exifr`) into a JSON blob.
3. **Re-encode** to WebP (JPEG fallback): `full` rendition ≤2048 px long edge (~q80) and
   `thumb` rendition ≤400 px. Re-encoding via canvas drops *all* EXIF — GPS, timestamps,
   device — from the public files.
4. Upload both renditions to the **public** storage bucket; insert the EXIF JSON, original
   filename, byte size, and a content hash into a **private** `photo_metadata` table
   readable only by admins.

Purpose of the private metadata: spam/abuse validation (e.g., detecting stock photos, files
reused across accounts, timestamp implausibility) — not public evidence. The client can lie
or strip EXIF before we see it; treat it as a heuristic signal, never proof.

Public photo URLs carry no user-identifying path segments (paths are keyed by pin id and
photo id, not user id).

## 10. Moderation and abuse (MVP baseline)

Decided model: **flag button + admin queue, with auto-hide threshold.**

- Every pin, comment, and photo has a **"Denunciar"** button (login required). Reporter
  picks a reason: `spam`, `contenido ofensivo`, `información personal`, `no corresponde al
  lugar`, `otro` (+ optional free text).
- Content stays live while reported, **except**: when a target accumulates **3 open reports
  from distinct users**, it auto-flips to `hidden` pending review (visible to author and
  admins only, with an "en revisión" notice for the author).
- **Admin queue** at `/admin` (role-gated): list of open reports grouped by target, with
  full context including the real author of anonymous content. Actions: dismiss (restores
  if auto-hidden), hide, delete, ban user. Every action is recorded in a moderation log.
- Baseline abuse limits enforced in the database: per-user daily caps (e.g., 10 pins,
  100 comments, 300 likes, 20 reports) via triggers. Crude, but stops trivial spam.
- Footer contact email for takedown/legal requests.
- Full policy text: see `moderation-policy.md`.

## 11. Screens inventory

| Route | Screen | Auth |
|---|---|---|
| `/` | Map (center) + viewport feed rail (left) + detail panel (right) | public |
| `/p/{id}` | Deep link → map centered on pin, panel open | public |
| `/novedades` | Feed (Nuevos / Populares tabs, tag search) | public |
| `/nuevo` | Pin composer (map-pick step + form) | required |
| `/perfil` | Own profile: username edit, "Mis pines" (incl. anonymous) | required |
| `/u/{username}` | Public profile: non-anonymous pins/comments only | public |
| `/admin` | Report queue + moderation log | admin role |
| `/acerca`, `/reglas` | About + content rules (static) | public |

## 12. Non-goals for MVP (explicit)

- No "mark as solved"/resolution flow (deferred; schema-ready). Note: the activity
  lifecycle (§6.1) *is* in MVP — what's deferred is verified resolution, not expiry.
- No native apps, no push notifications, no email digests.
- No DMs, follows, or user-to-user features beyond public threads.
- No categories/taxonomy beyond pin color+icon and free hashtags.
- No i18n, no multi-country.
- No automated content moderation (ML/vision) — human queue only.
- No anti-gaming beyond rate limits (logged as v2).
- No tenant/landlord-specific features (structured landlord entities, verified tenancy).
