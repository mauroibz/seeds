# QuePaso — Brand Guide

The single source of truth for QuePaso's visual identity, realized from
`mood.png` (Sprint B). UI copy stays in `web/lib/strings.ts`; this doc governs
color, type, logo, and assets. The content object is a `pin` in code regardless
of branding (decisions-log P9).

## 1. Logo & marks

Generated from the **Pacifico** outline font (OFL) by
`web/scripts/gen-brand-assets.mjs`. Regenerate after any change:

```bash
cd web && node scripts/gen-brand-assets.mjs
```

Assets (in `web/public/brand/`, plus Next file-metadata icons in `web/app/`):

| Asset | Use |
|---|---|
| `wordmark.svg` | Primary logo — cursive "quepaso" + map-pin. Monochrome (`currentColor`). |
| `mark-q.svg` | Compact `q°` mark for tight spaces / avatars. Monochrome. |
| `app-icon.svg` | Rounded-square `q` tile (white on brand blue) — seeds all raster icons. |
| `icon-192/512.png` | PWA / maskable icons (`app/manifest.ts`). |
| `app/icon.png`, `app/apple-icon.png`, `app/favicon.ico` | Browser tab + iOS home-screen. |

The same generator also emits the **teardrop map pins** (`public/map/pin-{color}.png`
+ `pin-dormant.png`) used by the map's unclustered symbol layer — colored per pin
category, kept in sync with `PIN_COLORS` in `lib/pin-style.ts`.

**In code:** use `<Logo variant="wordmark"|"mark" height={px} />`
(`web/components/brand/logo.tsx`). It's a CSS mask filled with `currentColor`, so
set its color with a text-color class on the wrapper (e.g. `text-primary` in
light, `text-foreground` on dark surfaces) and it flips with the theme.

**Rules:** keep clear-space ≈ the pin's width around the wordmark; never recolor
mid-glyph, add effects, or stretch (mask uses `contain`, so aspect is locked).
The logo is not pixel-identical to `mood.png` (Pacifico approximation, owner-
approved); a future hand-drawn SVG can drop into `public/brand/` unchanged.

## 2. Color

Tokens live in `web/app/globals.css` (`:root` = light default, `.dark` = toggle)
and flow through the shadcn semantic variables, so components use
`bg-primary`, `text-muted-foreground`, `border-border`, etc. — never raw hex.

| Role | Light | Dark | Moodboard |
|---|---|---|---|
| Primary | `#1E40AF` | `#3B82F6` | Azul Principal / Secundario |
| Ring / focus | `#3B82F6` | `#60A5FA` | Azul Secundario |
| Background | `#F8FAFC` | `#0F172A` | Fondo Claro / Profundo |
| Foreground | `#0F172A` | `#F8FAFC` | — |
| Accent (light blue) | `#DBE6FF` | `#24304D` | Azul Claro `#93C5FD` |

`theme_color` (PWA / address bar) = `#1E40AF`. The **pin category palette** (8
colors in `web/lib/pin-style.ts`) is a separate semantic system and is *not*
part of the brand palette — do not fold it into these tokens.

## 3. Typography

- **Poppins** (500/600/700) → headings (`--font-heading`). Applied to `h1–h4`
  and `.font-heading` via the base layer.
- **Inter** → body / UI (`--font-sans`).

Both loaded with `next/font/google` in `web/app/layout.tsx`. Scale: `h1`
3xl→4xl, `h2` 2xl→3xl, `h3` xl, body base. Static TTFs in `web/assets/fonts/`
are used only for OG image rendering.

## 4. Iconography

**Lucide** (`lucide-react`), matching the moodboard icon set. Pin category icons
map in `web/lib/pin-style.ts`.

## 5. Map

The basemap follows the theme (`web/components/map/map-view.tsx`):
`MAP_STYLE_LIGHT` = OpenFreeMap "liberty", `MAP_STYLE_DARK` = a recolored dark
style at `web/public/map/dark.json`. Regenerate the dark style with:

```bash
cd web && node scripts/gen-dark-map-style.mjs   # needs network for the base style
```

Both use OpenFreeMap's free tiles/glyphs/sprite — no paid map provider.

## 6. Social share cards

- Default site card: `web/app/opengraph-image.tsx` / `twitter-image.tsx`
  (branded wordmark + tagline on brand blue), built with `next/og`.
- Pins: photo-first; a pin without a photo gets a branded title card at
  `web/app/p/[id]/og/route.tsx`. Both share `web/lib/og/brand-card.tsx`.
- Set `NEXT_PUBLIC_SITE_URL` in production so OG image URLs are absolute.
