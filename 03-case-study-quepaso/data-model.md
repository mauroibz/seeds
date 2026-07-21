# Data Model — QuePaso

Authoritative schema reference. Migrations live in `supabase/migrations/`; if this document
and a migration disagree, the migration wins and this doc must be updated.

Naming: the content entity is a **pin** everywhere — tables, columns, RPCs, routes. The
brand may change; code never chases it (only `lib/strings.ts` does).

Conventions: UUID PKs, `timestamptz` UTC, soft lifecycle via `status`, likes/reports as rows
(never bare counters), real `author_id` on everything (anonymity is a *read-side* mask).

## 1. Entity overview

```
profiles ──< pins ──< comments
    │          │  │        └──< photos (comment-attached)
    │          │  └──< photos (pin-attached) ──1 photo_metadata (private)
    │          └──< likes
    ├──< reports >── (pin | comment | photo)
    └──< moderation_actions
```

## 2. Tables

```sql
-- Enable once per project
create extension if not exists postgis;

-- ── profiles ─────────────────────────────────────────────────────────────
create table profiles (
  id           uuid primary key references auth.users(id) on delete cascade,
  username     text unique not null check (username ~ '^[a-z0-9_]{3,24}$'),
  display_name text,
  avatar_url   text,
  role         text not null default 'user' check (role in ('user','admin')),
  is_banned    boolean not null default false,
  created_at   timestamptz not null default now()
);
-- Auto-created by trigger on auth.users insert (username = email prefix + random suffix).

-- ── pins ─────────────────────────────────────────────────────────────────
create table pins (
  id            uuid primary key default gen_random_uuid(),
  author_id     uuid not null references profiles(id),
  is_anonymous  boolean not null default false,
  title         text not null check (char_length(title) between 3 and 120),
  description   text not null check (char_length(description) <= 5000),
  location      geography(point, 4326) not null,
  address_text  text,                          -- user-editable display address
  city          text not null default 'Rosario',
  province      text not null default 'Santa Fe',
  country       text not null default 'AR',    -- ISO 3166-1 alpha-2
  tags          text[] not null default '{}',  -- lowercase, no '#', max 10 (trigger)
  color         text not null default 'red',   -- app-level palette validation
  icon          text not null default 'warning',
  status        text not null default 'published'
                check (status in ('published','hidden','deleted')),
                -- 'resolved' reserved for the deferred resolution feature
  like_count    integer not null default 0,    -- trigger-maintained
  comment_count integer not null default 0,    -- trigger-maintained
  photo_count   integer not null default 0,    -- trigger-maintained (all attached photos)
  expires_at    timestamptz not null default now() + interval '14 days',
                -- activity lifecycle timer (product spec §6.1); trigger-maintained
  created_at    timestamptz not null default now(),
  edited_at     timestamptz
);
create index pins_location_idx on pins using gist (location);
create index pins_feed_idx     on pins (country, province, city, created_at desc)
  where status = 'published';
create index pins_tags_idx     on pins using gin (tags);

-- ── comments ─────────────────────────────────────────────────────────────
create table comments (
  id           uuid primary key default gen_random_uuid(),
  pin_id       uuid not null references pins(id) on delete cascade,
  author_id    uuid not null references profiles(id),
  is_anonymous boolean not null default false,
  body         text not null check (char_length(body) between 1 and 2000),
  status       text not null default 'published'
               check (status in ('published','hidden','deleted')),
  created_at   timestamptz not null default now()
);
create index comments_pin_idx on comments (pin_id, created_at);

-- ── photos ───────────────────────────────────────────────────────────────
-- Attached to a pin directly, or to a comment (photo addition).
create table photos (
  id           uuid primary key default gen_random_uuid(),
  pin_id       uuid not null references pins(id) on delete cascade,
  comment_id   uuid references comments(id) on delete cascade,  -- null = original pin photo
  author_id    uuid not null references profiles(id),
  is_anonymous boolean not null default false,
  full_path    text not null,   -- storage: pins/{pin_id}/{photo_id}-full.webp
  thumb_path   text not null,
  width        integer, height integer,
  status       text not null default 'published'
               check (status in ('published','hidden','deleted')),
  created_at   timestamptz not null default now()
);
create index photos_pin_idx on photos (pin_id, created_at);

-- ── photo_metadata (PRIVATE: admin-only) ─────────────────────────────────
-- Original-file metadata retained for spam/abuse validation. Never public.
create table photo_metadata (
  photo_id          uuid primary key references photos(id) on delete cascade,
  exif              jsonb,            -- full EXIF extracted client-side (may be absent/forged)
  original_filename text,
  original_bytes    integer,
  original_sha256   text,             -- duplicate/reuse detection across accounts
  created_at        timestamptz not null default now()
);
create index photo_metadata_sha_idx on photo_metadata (original_sha256);

-- ── likes ────────────────────────────────────────────────────────────────
create table likes (
  pin_id       uuid not null references pins(id) on delete cascade,
  user_id      uuid not null references profiles(id),
  is_anonymous boolean not null default false,
  created_at   timestamptz not null default now(),
  primary key (pin_id, user_id)
);

-- ── reports ──────────────────────────────────────────────────────────────
create table reports (
  id          uuid primary key default gen_random_uuid(),
  target_type text not null check (target_type in ('pin','comment','photo')),
  target_id   uuid not null,
  reporter_id uuid not null references profiles(id),
  reason      text not null check (reason in
              ('spam','ofensivo','info_personal','lugar_incorrecto','otro')),
  details     text check (char_length(details) <= 1000),
  status      text not null default 'open'
              check (status in ('open','dismissed','actioned')),
  created_at  timestamptz not null default now(),
  unique (target_type, target_id, reporter_id)
);
create index reports_open_idx on reports (status, created_at) where status = 'open';

-- ── moderation_actions ───────────────────────────────────────────────────
create table moderation_actions (
  id          uuid primary key default gen_random_uuid(),
  admin_id    uuid not null references profiles(id),
  action      text not null check (action in
              ('hide','unhide','delete','ban_user','unban_user','dismiss_reports')),
  target_type text not null check (target_type in ('pin','comment','photo','user')),
  target_id   uuid not null,
  note        text,
  created_at  timestamptz not null default now()
);
```

## 3. Triggers and functions

| Trigger | On | Effect |
|---|---|---|
| `handle_new_user` | `auth.users` insert | create `profiles` row with generated username |
| `bump_counts` | `likes`/`comments`/`photos` ins/del | maintain denormalized counts on `pins` |
| `enforce_tag_rules` | `pins` ins/upd | ≤10 tags, lowercase, strip `#`, dedupe |
| `enforce_rate_limits` | `pins`/`comments`/`likes`/`reports` insert | daily per-user caps (10/100/300/20); reject with clear error |
| `auto_hide_on_reports` | `reports` insert | 3 open reports from distinct users → target `status='hidden'` |
| `reject_banned` | all content inserts | `is_banned` users cannot write |
| `extend_lifecycle` | `comments`/`photos`/`likes` insert | re-arm `pins.expires_at` (rules below) |

**Activity lifecycle** (product spec §6.1): the state is **derived at read time** —
no cron, no batch updates, revival is automatic.

```sql
-- Tunable constants (single source of truth for the lifecycle):
--   lifecycle_window   = interval '14 days'   -- full re-arm; revisit post-launch
--   lifecycle_like_ext = interval '48 hours'  -- cheap action, cheap extension
--   fading_threshold   = interval '24 hours'

-- extend_lifecycle trigger logic (comments & photos re-arm fully, likes 48h;
-- author self-bumps are ignored — internal author_id, so anonymity-safe):
update pins p
   set expires_at = greatest(p.expires_at, now() + <window-or-like-ext>)
 where p.id = new.pin_id
   and p.author_id <> new.author_id;   -- (new.user_id for likes)

-- Derived state, exposed as `activity_state` on public views:
create or replace function activity_state(expires_at timestamptz)
returns text language sql stable as $$
  select case
    when expires_at <= now()                     then 'dormant'
    when expires_at <= now() + interval '24 hours' then 'fading'
    else 'active'
  end
$$;
```

Deleting an interaction does not retract granted time. `dormant` is orthogonal to
`status` — a hidden or deleted pin is never shown regardless of its timer.

**Hot score** is a SQL function, not a column (recomputing beats invalidating at this scale):

```sql
-- NB: `stable`, not `immutable` — it reads now(). (Corrected in migration 2;
-- the migration is authority.)
create or replace function hot_score(like_count int, comment_count int,
                                     photo_count int, created_at timestamptz)
returns double precision language sql stable as $$
  select (like_count*3 + comment_count*2 + photo_count*2)::float
         / power(extract(epoch from (now() - created_at))/3600 + 2, 1.5)
$$;
```

## 4. RPCs (the app's API surface)

```sql
-- Map viewport: capped, hot-ordered → low zoom shows most relevant pins.
-- Order: active/fading first, then dormant ghosts; hot_score desc within each group.
pins_in_bbox(min_lng float, min_lat float, max_lng float, max_lat float,
             max_results int default 200)
  returns setof pins_public
  -- ST_MakeEnvelope && location,
  -- order by (activity_state(expires_at) = 'dormant'), hot_score desc

-- "Otros pines cerca": published pins within radius_m of the given pin.
nearby_pins(p_pin_id uuid, radius_m int default 500, max_results int default 10)

-- Feed: place-name filter only (no geo math — product decision).
-- Excludes dormant pins while browsing (both tabs; fading included) BUT includes
-- them when p_tag is set — a tag query is an explicit lookup (product §8/§11).
feed(p_city text default 'Rosario', p_tab text default 'nuevos',  -- 'nuevos'|'populares'
     p_tag text default null, p_cursor timestamptz default null, p_limit int default 20)
  returns setof pins_public

-- Profiles (product §11). Public surfaces expose NON-anonymous content only;
-- anonymous pins have a null author_id in pins_public so they self-exclude.
profile_pins(p_username text, p_cursor timestamptz default null, p_limit int default 20)
  returns setof pins_public  -- a user's named pins, INCLUDES dormant, created_at desc
profile_comments(p_username text, p_cursor timestamptz default null, p_limit int default 20)
  -- a user's named+published comments (id, pin_id, pin_title, body, created_at)
my_comments(p_cursor timestamptz default null, p_limit int default 50)
  -- caller's OWN comments incl. anonymous (badged); where author_id = auth.uid()

-- Writes (security definer; validate auth.uid() inside):
create_pin(...)      -- transactional: pin row (+ normalized tags)
update_pin(p_pin_id uuid, p_title text, p_description text, p_tags text[])
                     -- author-only, 24 h window; stamps edited_at; tags re-normalized
delete_pin(p_pin_id uuid)  -- author-only soft delete (status='deleted'), any time
create_comment(p_pin_id uuid, p_body text, p_is_anonymous boolean)  -- returns comment id
register_photo(...)  -- photos row + photo_metadata row in one transaction
toggle_like(p_pin_id uuid, p_is_anonymous boolean)  -- returns resulting liked state (bool)
create_report(p_target_type text, p_target_id uuid, p_reason text, p_details text default null)
                     -- returns report id; unique(target,reporter) → friendly duplicate.
                     -- auto_hide_on_reports trigger hides the target at 3 distinct reporters.

-- Admin (assert is_admin() inside; each logs a moderation_actions row):
admin_set_status(target_type, target_id, new_status, note)   -- hide/unhide/delete
admin_ban_user(user_id, ban boolean default true, note)      -- ban/unban
admin_dismiss_reports(target_type, target_id, note)          -- dismiss + restore if auto-hidden

-- Admin reads (is_admin()-gated; the ONE surface that reveals the real author of
-- anonymous content — product §10):
admin_report_queue()             -- open reports grouped by target, with author + reporters
admin_moderation_log(p_limit int default 100)   -- recent moderation_actions + admin username
```

## 5. Anonymity enforcement (the critical design)

**Rule: the real author id of anonymous content must never leave Postgres.**

1. Base tables carry `author_id` always. RLS on base tables:
   - `select`: own rows (`author_id = auth.uid()`), or admin.
   - `insert`: own rows only, not banned, rate-limited.
   - `update/delete`: own rows (author can delete own content; 24 h edit window on pins
     enforced in the RPC), or admin.
   - `photo_metadata`: **admin select only**; insert via `register_photo` RPC.
2. Public reads go exclusively through views:

```sql
create view pins_public as
select n.id, n.title, n.description, n.location,
       ST_X(n.location::geometry) as lng, ST_Y(n.location::geometry) as lat,
       -- lng/lat because PostgREST serializes geography as EWKB hex (client needs coords)
       n.address_text,
       n.city, n.province, n.country, n.tags, n.color, n.icon,
       n.like_count, n.comment_count, n.photo_count, n.created_at, n.edited_at,
       n.expires_at, activity_state(n.expires_at) as activity_state,
       n.is_anonymous,
       case when n.is_anonymous then null else n.author_id end as author_id,
       case when n.is_anonymous then null else p.username  end as author_username,
       case when n.is_anonymous then null else p.avatar_url end as author_avatar
from pins n join profiles p on p.id = n.author_id
where n.status = 'published';
-- Default (security definer) view semantics: executes with owner privileges, so it can
-- read the RLS-protected base table. Grant SELECT to anon, authenticated.
-- comments_public and photos_public follow the identical pattern.

-- profiles_public: the ONLY public window onto profiles. Exposes identity fields
-- but never role/is_banned (moderation state stays server-side).
create view profiles_public as
select id, username, display_name, avatar_url, created_at from profiles;
-- Grant SELECT to anon, authenticated.
```

3. `likes` are never publicly listed per-user in MVP; only counts are exposed. The
   authenticated user can check *their own* like via RLS (`user_id = auth.uid()`).
4. "Mis pines" reads the base table (own rows pass RLS), so authors see their anonymous
   posts marked as such.

**Review checklist for any new query/view:** does it join `profiles`? Then it must apply
the `case when is_anonymous` mask. Never expose `author_id` from a base table publicly.

## 6. Storage layout

```
bucket: photos (public read)
  pins/{pin_id}/{photo_id}-full.webp    ≤2048px, q~80
  pins/{pin_id}/{photo_id}-thumb.webp   ≤400px
```

Policies: public `select`; `insert` for authenticated users, mime `image/webp|jpeg`,
≤5 MB. No `update`; `delete` via admin/service role only. No user ids in paths.

## 7. Schema headroom for known v2 features (do not build now)

- **Resolution flow (deferred):** add `'resolved'` to `pins.status` + a
  `resolution_events` table later; nothing today blocks it. Note the activity lifecycle
  (`expires_at`, above) is **built in MVP** and is orthogonal — dormant ≠ resolved.
- **Anti-gaming:** likes-as-rows with timestamps, `photo_metadata.original_sha256`, and
  internal author links on anonymous content are the raw material; add heuristics later.
- **Pin merging:** admin tool that moves comments/photos/likes to a canonical pin and
  tombstones the duplicate (`status='deleted'` + future `merged_into` column).
- **Per-thread pseudonyms** ("Vecino 3"): derivable at read time from
  `hash(author_id, pin_id)` — requires no schema change, only view changes.
- **i18n / multi-country:** `country/province/city` are already columns, not assumptions.
