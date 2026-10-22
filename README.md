# devk-software (Kotacom Software Platform)

Platform resmi software & web engineering Kotacom berbasis [EmDash CMS](https://github.com/emdash-cms/emdash) & [Astro](https://astro.build/).

- **Live URL:** [https://software.devk.my.id/](https://software.devk.my.id/)
- **Repository:** `Yusufkotavom/devk-software` (branch `main`)
- **Hosting / Deploy:** Dokploy (App: `devk-software`, Service: `app-devk-software-67j6h1`)
- **Database:** PostgreSQL di Dokploy container (`devk-software-db`)
- **Styles & Theme:** Warm editorial minimalism ("Ink" style)

## Architecture & Tech Stack

- **Framework:** Astro SSR (`@astrojs/node` standalone)
- **CMS:** EmDash CMS with Block Kit (`ec_pages`, `marketing-blocks`)
- **Animations:** `@astroanimate/core` (Zero-runtime JS, pure CSS hardware-accelerated animations)
- **Icons:** `astro-iconset` with Phosphor icons dynamic fallback (`ph:*`)
- **Database Client:** PostgreSQL adapter via `DATABASE_URL`

## Block & CMS Architecture

Halaman utama (`/`) dan semua sub-halaman dimotori 100% oleh CMS block tanpa hardcoded markup:
- `marketing_hero`: Hero banner dengan headline animasi, announcement badge, & dual CTAs.
- `marketing_logos`: Endless marquee client logos dengan hover pause & reduced motion support.
- `marketing_features`: Grid kartu fitur dengan dukungan icon Phosphor atau gambar (`imageUrl`).
- `marketing_split`: Layout 2-kolom editorial image & checklist.
- `marketing_stats`: Grid metrik & statistik dengan entrance scale transition.
- `marketing_pricing`: Tier pricing dengan visual highlight & badge.
- `marketing_faq`: Accordion FAQ interaktif native `<details>`.
- `marketing_cta`: Full-width banner call-to-action.
- `marketing_feed`: Feed artikel / blog card grid otomatis dari CMS.

## Animation Guidelines (`@astroanimate/core`)

Animasi pada block dirancang menjaga Page Speed (Lighthouse 95+):
- **Zero runtime overhead:** Dijalankan murni via CSS keyframes & view-timeline.
- **GPU Compositor only:** Menggunakan `transform` dan `opacity` (menghindari reflow / layout shifts).
- **Reduced motion:** Otomatis disable ketika sistem pengguna mengaktifkan `prefers-reduced-motion`.

## Getting Started

```bash
pnpm install
pnpm dev
```

Server lokal berjalan di `http://localhost:4321` dan admin CMS di `http://localhost:4321/_emdash/admin`.
