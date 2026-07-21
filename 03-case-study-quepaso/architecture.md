# Architecture Spec — QuePaso

Backend and frontend component map, plus every delegated technology choice with rationale.
Guiding constraints: PoC/MVP, no fixed budget → **low cost beats premium**, low maintenance,
easy to scale later, and friendly to LLM-assisted development (mainstream, well-documented
tools over clever ones).

## 1. Technology choices (decided)

| Concern | Choice | Rationale / alternatives considered |
|---|---|---|
| Backend platform | **Supabase** (given) | Postgres + PostGIS + Auth + Storage + RLS in one free tier. Usage-based scaling. |
| Database | **Postgres + PostGIS** extension | Real geospatial indexing (GIST) for bbox queries; PostGIS ships enabled-able on Supabase free tier. |
| Frontend framework | **Next.js (App Router) + TypeScript** | Most-documented React meta-framework → best LLM assistance; SSR gives public pins SEO (a real growth channel for "pothole + street name" searches); first-class Vercel deploy. Considered Vite SPA (simpler, but no SEO) and SvelteKit (smaller ecosystem). |
| UI | **Tailwind CSS + shadcn/ui** | Fast to build, easy for LLMs to generate consistently, no design-system maintenance. |
| Map rendering | **MapLibre GL JS** via **react-map-gl** | Open-source vector maps, native clustering, no vendor lock-in. Considered Leaflet (raster, dated) and Google Maps (cost + lock-in). |
| Map tiles | **OpenFreeMap** (`https://tiles.openfreemap.org/styles/liberty`) | Genuinely free vector tiles, no API key, no hard usage cap. Fallback if reliability disappoints: MapTiler free tier (100k loads/mo, API key). |
| Geocoding — search | **Photon** (komoot, `photon.komoot.io`) | Free, no key, typeahead-friendly. Only a convenience for moving the map — the pin is the source of truth, so geocoder quality is not critical-path. |
| Geocoding — reverse | **Nominatim** public API | Free (1 req/s policy, attribution required); used once per pin to suggest `address_text` + derive city/province. Volume is tiny at MVP scale. Upgrade path: LocationIQ/Geoapify free tiers if rate limits bite. |
| Image hosting/CDN | **Supabase Storage** (public bucket, built-in CDN) | Already in the stack; free tier 1 GB. We do **not** use Supabase Image Transformations (Pro-only) — renditions are generated client-side instead. |
| Image processing | **Client-side**: `browser-image-compression` (resize/re-encode) + `exifr` (EXIF extraction) | Zero server cost, and re-encoding strips EXIF for free — which is a product requirement anyway. |
| Data fetching | **TanStack Query** + `supabase-js` | Caching, refetch-on-focus gives the "real-time-ish" feed without websockets. |
| Feed freshness | Polling / refetch-on-focus (MVP) | Supabase Realtime is a later drop-in (subscribe to `pins` inserts); not worth the connection management now. |
| Hosting | **Vercel** Hobby tier | Free, zero-ops Next.js deploys, preview deployments per branch. |
| Domain | **quepaso.com.ar** (final) | Registered via NIC.ar. |
| Analytics | **Plausible-compatible self-host later; MVP: Vercel Analytics free tier** | Don't overthink; swap later. |
| Testing | Vitest + Playwright (smoke only) | Minimal: schema/RPC tests via SQL, one Playwright happy-path. |

Costs at MVP scale: **~$0/month** plus domain registration (Supabase free + Vercel Hobby +
OpenFreeMap + Photon/Nominatim). First real costs appear at ~1 GB of photos or ~50k MAU
(Supabase Pro $25/mo).

## 2. System overview

```
Browser (Next.js app, React)
  ├─ MapLibre GL ── vector tiles ──► OpenFreeMap CDN
  ├─ Photon / Nominatim (geocoding convenience)
  ├─ supabase-js ──► Supabase
  │     ├─ Auth (Google OAuth)
  │     ├─ Postgres + PostGIS  (RLS + views + RPCs = the API)
  │     └─ Storage (public `photos` bucket + CDN)
  └─ Vercel (hosting, SSR for SEO routes)
```

**There is no custom API server.** The database *is* the API: row-level security, public
views, and SQL functions (RPCs) called through supabase-js/PostgREST. Next.js server
components do SSR reads with the same anon key. This is the lowest-maintenance architecture
Supabase enables; if custom endpoints are ever needed (e.g., server-side image work),
Next.js route handlers or Supabase Edge Functions are the escape hatch.

## 3. Backend components

All schema detail lives in `data-model.md`; this section is the component map.

### 3.1 Auth
- Supabase Auth with Google provider. `auth.users` / `auth.identities` natively support
  adding providers later (no rework — decided requirement).
- DB trigger on `auth.users` insert → creates `public.profiles` row (generated username).
- Admin role: `profiles.role in ('user','admin')`, checked by RLS helper `is_admin()`.
  Roles are assigned manually via SQL for MVP.

### 3.2 Data access layers (the anonymity boundary)
Three tiers, enforced in the database:
1. **Base tables** (`pins`, `comments`, `photos`, `likes`, …) — always store the real
   `author_id`. RLS: authors can read/write their own rows; admins read everything;
   **the public cannot select base tables containing author columns.**
2. **Public views** (`pins_public`, `comments_public`, `photos_public`) — expose only
   `status = 'published'` rows and **null out author fields when `is_anonymous`**. These are
   `security definer`-style views (owned by a privileged role) with SELECT granted to
   `anon` and `authenticated`. This is the single mechanism that guarantees anonymous
   authorship never reaches a client. They also expose the derived `activity_state`.
3. **RPCs** for anything beyond CRUD: `pins_in_bbox(...)` (viewport query, hot-score
   ordered, capped, dormant last), `nearby_pins(pin_id)`, `feed(...)` (place-name filter +
   pagination, dormant excluded), `create_pin(...)` (transactional insert of pin + tags),
   plus moderation actions.

### 3.3 Storage
- Bucket `photos` (public read). Path scheme: `pins/{pin_id}/{photo_id}-full.webp`
  and `...-thumb.webp` — **no user id in paths** (anonymity requirement).
- Upload policy: authenticated users only; mime allowlist; ≤5 MB per object (post-compression
  files are ~200–500 KB). The `photos` DB row is the authority; a periodic orphan-cleanup
  script is a v2 chore (logged).
- `photo_metadata` (private table): EXIF JSON, original filename/size, SHA-256 of original.
  Admin-only RLS. Written by the same `register_photo` RPC that registers the upload.

### 3.4 Moderation machinery
- `reports` table + trigger: 3 open reports from distinct users on one target → target
  `status = 'hidden'`.
- `moderation_actions` log table (who, what, target, when, note).
- Rate-limit triggers on insert into `pins`, `comments`, `likes`, `reports` (daily caps
  per user).

## 4. Frontend components

```
app/
  layout.tsx            shell: nav (Mapa | Novedades | Nuevo), auth state
  page.tsx              MAP SCREEN (client component wrapping MapView)
  p/[id]/page.tsx       deep link → map + open panel (SSR metadata for SEO/social cards)
  novedades/page.tsx    feed (tabs Nuevos/Populares, tag search)
  nuevo/page.tsx        composer wizard (auth-gated)
  perfil/page.tsx       own profile + Mis pines
  u/[username]/page.tsx public profile
  admin/page.tsx        report queue (role-gated)
  acerca/, reglas/      static
components/
  map/MapView.tsx           MapLibre instance, viewport→bbox query, clustering;
                            hosts the three zones: map (center), viewport feed
                            (left rail / mobile below), detail panel (right)
  map/PinMarker.tsx         colored/iconed marker + lifecycle styles (fading pulse, ghost)
  map/HoverPopup.tsx        desktop-only summary popup
  feed/ViewportFeed.tsx     "En esta zona" — pins in the current viewport (§4.3),
                            fed by MapView's bbox query; reuses pin/PinCard
  feed/FeedScreen.tsx       /novedades doomscroll (tabs + tag search)
  pin/PinCard.tsx           shared list card (viewport feed, /novedades, profiles)
  pin/PinPanel.tsx          detail panel (desktop right rail / mobile bottom sheet)
  pin/PhotoGallery.tsx      chronological gallery w/ attribution
  pin/CommentList.tsx       comments + composer
  pin/LikeButton.tsx
  pin/NearbyList.tsx        "Otros pines cerca"
  pin/LifecycleBanner.tsx   fading ("¿Sigue pasando?") / dormant ("Archivado") banners
  pin/ReportDialog.tsx      shared by pin/comment/photo
  composer/LocationPicker.tsx   crosshair map + Photon search + reverse geocode
  composer/PhotoUploader.tsx    exifr extract → compress → upload → register
  composer/PinStylePicker.tsx   color + icon
  composer/TagInput.tsx
  shared/AnonToggle.tsx     the anonymous switch + honesty copy
  shared/AuthorChip.tsx     avatar+name or "Anónimo"
lib/
  supabase/ (client, server, middleware helpers)
  queries/  (TanStack Query hooks wrapping RPCs/views)
  images.ts (compression pipeline), geo.ts, strings.ts (ALL Spanish UI copy)
```

Key frontend behaviors:
- **Viewport querying:** map `moveend` → debounce 300 ms → `pins_in_bbox` RPC → GeoJSON
  source with `cluster: true`. Max ~200 pins/query, hot-score ordered with dormant pins
  last, so low zoom shows the most relevant pins (product requirement).
- **Map ↔ panel state via URL:** open pin id lives in the route (`/p/{id}`), so links,
  back button, and SSR all work.
- **Auth-gated actions** prompt a login dialog rather than hiding buttons (conversion).
- **Strings module:** every user-facing string in `lib/strings.ts` — cheap future i18n
  exit, and the only place a brand/terminology change ever touches.

## 5. Cross-cutting decisions

- **IDs:** UUIDv4 everywhere (client-generatable, no enumeration leaks).
- **Coordinates:** `geography(Point, 4326)`, WGS84 lng/lat.
- **Time:** `timestamptz`, UTC in DB; client renders relative Spanish ("hace 3 días").
- **SEO:** `/p/{id}` SSRs title/description/first-photo OpenGraph tags; map itself is
  client-only.
- **Error tracking:** Sentry free tier, added in the polish sprint.
- **Secrets:** only two runtime env vars (`NEXT_PUBLIC_SUPABASE_URL`,
  `NEXT_PUBLIC_SUPABASE_ANON_KEY`); the anon key is public by design — RLS is the security
  boundary. The `service_role` key is never used by the app (only by admin scripts/CI).
