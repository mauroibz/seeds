# Deployment Guide — QuePaso

Path from a blank machine to production at **quepaso.com.ar**. Target cost at launch:
**$0/month** plus domain registration.

## 1. Local development

Prereqs: Node 20+, Docker, Git. The Supabase CLI is a repo-root dev dependency
(`npm install` at the repo root installs it); invoke it as `npx supabase …`. A global
install (`npm i -g supabase`) also works if you prefer.

```bash
git clone <repo> && cd quepaso
npm install                    # repo-root tooling (Supabase CLI)
npx supabase start             # local Postgres+Auth+Storage stack (Docker)
npx supabase db reset          # applies migrations + seed.sql
cd web && cp .env.example .env.local   # fill from `npx supabase status` output
npm install && npm run dev     # http://localhost:3000
```

- `npx supabase status` prints the local URL and anon key for `.env.local`.
- Local ports are set in `supabase/config.toml`. This repo uses the `553xx` range
  (API `55321`, DB `55322`, Studio `55323`) because the default `543xx` range collided
  with another local project on the dev machine; adjust if they collide on yours.
- Local Google OAuth: configure the provider in `supabase/config.toml` with the same
  Google client (add `http://127.0.0.1:55321/auth/v1/callback` as a redirect URI — match
  the configured API port), or use email test users locally and reserve Google for
  hosted envs.
- Schema changes: `supabase migration new <name>` → edit SQL → `supabase db reset`.
  Never modify the hosted database by hand.

## 2. Hosted environments

Two environments, both created in Sprint 0:

| Env | Supabase | Frontend |
|---|---|---|
| Production | Hosted project, region `sa-east-1` (São Paulo — closest to Rosario) | Vercel production (main branch) |
| Preview | same Supabase project (MVP trade-off) | Vercel preview deploys (PR branches) |

A separate staging Supabase project is a post-MVP upgrade; at MVP scale, previews pointing
at production data are an accepted risk — be careful with destructive migrations.

## 3. Supabase project setup (once)

1. Create project (org: personal, free tier, region `sa-east-1`). Save the DB password in a
   password manager.
2. `supabase link --project-ref <ref>` then `supabase db push` to apply migrations.
3. Dashboard → Database → Extensions: confirm `postgis` enabled (migration should do it).
4. Storage: `photos` bucket is created by migration; confirm public read + policies.
5. Auth settings:
   - Site URL: `https://<production-domain>`.
   - Additional redirect URLs: `http://localhost:3000`, `https://*-<team>.vercel.app`
     (preview deploys).
6. **Google OAuth** (Google Cloud Console):
   - New project → OAuth consent screen (external, es-AR, app name, support email).
   - Credentials → OAuth Client ID (web): authorized redirect URI
     `https://<project-ref>.supabase.co/auth/v1/callback`.
   - Paste client id/secret into Supabase → Auth → Providers → Google.
7. Provision the admin: log in once with your Google account, then
   `update profiles set role='admin' where id='<your-uuid>';` via the SQL editor.

## 4. Vercel setup (once)

1. Import the Git repo; root directory `web/`; framework preset Next.js.
2. Env vars (Production + Preview): `NEXT_PUBLIC_SUPABASE_URL`,
   `NEXT_PUBLIC_SUPABASE_ANON_KEY` (from the hosted project). The `service_role` key is
   **never** set in Vercel.
3. Custom domain: **quepaso.com.ar** (register via NIC.ar; requires an AR tax ID —
   CUIT/CUIL — and a fee). Add to Vercel, follow DNS instructions. Then update Supabase
   Site URL and Google OAuth consent/redirects to `https://quepaso.com.ar`.

## 5. Release flow

- Branch → PR → Vercel preview URL → check → merge to `main` → auto-deploy production.
- Migrations are applied manually before merging schema-dependent frontend changes:
  `supabase db push` (this is the one manual step; a GitHub Action running
  `supabase db push` on merge is a nice later upgrade).
- Rollback: Vercel → previous deployment → "Promote". DB rollbacks: write a down
  migration; for disasters, Supabase daily backups (free tier: 1-day retention —
  see risks).

## 6. Production checklist (Sprint 6)

- [ ] quepaso.com.ar live with HTTPS; Google login works on the domain (not just vercel.app).
- [ ] `select * from pins_public` as anon: no author fields on anonymous rows.
- [ ] `photo_metadata` denies non-admin select (test with anon key).
- [ ] Upload a photo in prod; download it; `exiftool` shows no EXIF.
- [ ] Rate limits fire (script 11 rapid pins on a test account).
- [ ] Auto-hide fires with 3 test reports; admin queue usable from a phone.
- [ ] Sentry receiving a test error; Vercel Analytics counting.
- [ ] Footer: contact email, /reglas, privacy note (incl. EXIF retention disclosure).
- [ ] ~15 real founder-created Rosario pins on the map; seed/test data purged.
- [ ] `docs/runbook.md` written (moderation how-to, backup restore, known limits).

## 7. Known free-tier limits and risks

| Risk | Detail | Mitigation |
|---|---|---|
| Supabase free-tier pause | Project pauses after ~1 week of inactivity | Fine pre-launch (restore from dashboard). Post-launch real traffic prevents it; a scheduled uptime ping (cron-job.org) as belt-and-braces. |
| Backup retention | Free tier keeps ~1 daily backup | Weekly manual `supabase db dump` to local disk until Pro ($25/mo) is justified. |
| Storage 1 GB | ~2–4k photos at our compression | Monitor dashboard; Pro raises to 100 GB. |
| Nominatim/Photon rate policy | Public instances, 1 req/s etiquette, no SLA | Volume is one call per submission + debounced search; add LocationIQ free tier (5k/day) if throttled. |
| OpenFreeMap availability | Community-run, no SLA | Style URL is one config line; fallback to MapTiler free (key) in <1 h. |
| Vercel Hobby | Non-commercial terms, 100 GB bandwidth | Fine for MVP; Pro ($20/mo) when the project stops being a hobby. |

**Upgrade path** (in order, as usage grows): Supabase Pro → Vercel Pro → separate staging
project → GitHub Action migration deploys → Supabase Realtime for the feed.
