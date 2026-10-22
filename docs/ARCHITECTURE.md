# Arsitektur & Dokumentasi Teknis devk-software

Dokumen ini mendeskripsikan implementasi teknis situs resmi platform software Kotacom (`https://software.devk.my.id/`).

## 1. Ikhtisar Sistem
- **Aplikasi Dokploy:** `devk-software` (Swarm service: `devk-software-app-vavdlg`)
- **Database:** PostgreSQL container Dokploy (`devk-software-db-hfl2l5`)
- **Repository:** `Yusufkotavom/devk-software` (Branch: `main`)
- **Framework:** Astro SSR dengan `@astrojs/node` standalone
- **CMS:** EmDash headless CMS dengan Block Kit terpadu

## 2. Standar Animasi & Page Speed (`@astroanimate/core`)
Untuk menjamin skor Core Web Vitals dan Page Speed (skor 95-100), seluruh efek visual diatur dengan kaidah:
- Zero-runtime / ultra-lightweight IntersectionObserver (aktif via `enhance={true}`).
- Animasi terpicu saat elemen masuk ke viewport ketika pengguna scroll.
- Hardware-accelerated properties: `transform` dan `opacity` murni.
- **A11y & Motion:** Terbungkus query `@media (prefers-reduced-motion)` bawaan.

### Komponen Animasi per Block
1. **Hero (`marketing_hero`):**
   - Menggunakan `<FadeInText>` pada `hero__headline` (`duration: 0.7s`, `distance: 16px`).
2. **Stats (`marketing_stats`):**
   - Menggunakan `<ScaleIn>` pada item statistik (`initialScale: 0.95`, `duration: 0.5s`).
3. **Features (`marketing_features`):**
   - Menggunakan `<ScaleIn>` pada masing-masing kartu fitur (`initialScale: 0.96`, `duration: 0.45s`).
4. **Pricing (`marketing_pricing`):**
   - Menggunakan `<ScaleIn>` pada kartu tier paket (`initialScale: 0.96`, `duration: 0.5s`).
5. **CTA Banner (`marketing_cta`):**
   - Menggunakan `<FadeInText>` pada judul headline banner (`duration: 0.6s`).

## 3. Pola Komponen & Integrasi Konten (Zero-Hardcode)
- Seluruh halaman utama (`/`) dibangun secara modular dari database CMS (`ec_pages`).
- `MarketingBlocks.astro` mengonsumsi single source of truth dari `src/plugins/marketing-blocks/astro`.
- Repeater fitur mendukung:
  - Fallback icon Phosphor dinamis (`icon` -> `ph:<nama>`).
  - Gambar kustom via `imageUrl` (otomatis switch dari icon ke `<img>` dengan `loading="lazy"`).
