# Deployment Guide — {{PROJECT_NAME}}

[Reference: `03-case-study-quepaso/deployment-guide.md` for a fully worked example.]

Path from a blank machine to production at **{{DOMAIN}}**. Target cost at launch:
{{TARGET_COST}}.

## 1. Local development

Prereqs: [runtime versions, Docker if the backend needs local emulation, any CLI
tools]. [Exact clone/install/start command sequence — this should be copy-pasteable
and actually tested by whoever writes it, not aspirational.]

- [Any local-vs-hosted config gotchas worth flagging up front — e.g. a nonstandard
  local port range chosen to avoid colliding with another project on the same machine.]
- [OAuth or third-party provider local setup, if applicable.]
- Schema changes: [the migration workflow]. Never modify the hosted database by hand.

## 2. Hosted environments

| Env | Backend | Frontend |
|---|---|---|
| Production | | |
| Preview/staging | | |

[State the MVP trade-off explicitly if preview and production share infrastructure —
e.g. "same backend project, be careful with destructive migrations" — so nobody
discovers this the hard way.]

## 3. Backend project setup (once)

[Numbered, concrete steps: create project, apply migrations, confirm any required
extensions/features enabled, storage bucket setup, auth provider setup including exact
redirect URIs, admin account provisioning.]

## 4. Frontend hosting setup (once)

[Import repo, root directory, env vars — and explicitly which secrets NEVER go here
(an admin/service-role-equivalent key, restated from architecture.md §5). Domain setup,
including any real-world friction — a tax ID requirement, a registrar's fee, DNS
propagation time.]

## 5. Release flow

[Branch → PR/preview → check → merge → deploy. Migration application step — is it
manual or automated? Rollback plan for both frontend and database.]

## 6. Production checklist (Sprint 6)

- [ ] Production domain live with HTTPS; auth works on that domain, not just a preview
      URL.
- [ ] Security/trust boundary re-verified as the unprivileged role in production,
      not just locally.
- [ ] Any privacy-sensitive processing (metadata stripping, etc.) verified against a
      real production upload, not assumed from the local test.
- [ ] Rate limits fire.
- [ ] Moderation auto-hide fires; admin queue usable from the device class an admin
      will actually use.
- [ ] Error tracking and analytics both confirmed receiving real events.
- [ ] Footer/legal basics live (contact, policy page, any required disclosure).
- [ ] Real seed content in place; test/dev data purged.
- [ ] Runbook written.

## 7. Known free-tier limits and risks

| Risk | Detail | Mitigation |
|---|---|---|
| | | |

**Upgrade path** (in order, as usage grows): [the realistic sequence of "next thing you
pay for" as the product succeeds].
