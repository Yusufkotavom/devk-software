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
   - Menggunakan `<FadeInText>` (`duration: 1.2s`, `distance: 24px`, easing cubic-bezier).
2. **Stats (`marketing_stats`):**
   - Menggunakan `<ScaleIn>` (`initialScale: 0.88`, `duration: 1.0s`, stagger delay `0.15s`).
3. **Features (`marketing_features`):**
   - Menggunakan `<ScaleIn>` (`initialScale: 0.90`, `duration: 1.0s`, stagger delay `0.12s`).
4. **Pricing (`marketing_pricing`):**
   - Menggunakan `<ScaleIn>` (`initialScale: 0.90`, `duration: 1.0s`, stagger delay `0.15s`).
5. **CTA Banner (`marketing_cta`):**
   - Menggunakan `<FadeInText>` (`duration: 1.2s`, `distance: 30px`).

## 4. Struktur SEO & Schema.org Dinamis (`StructuredData.astro`)

SEO dikelola secara terpusat dan dinamis melalui CMS EmDash (`seo_settings` collection) tanpa hardcoded value:
- **Schema.org Graph Otomatis:**
  - `ProfessionalService` / `Organization` / `LocalBusiness` (tipe entitas dapat diatur di admin).
  - Kontak resmi: `telephone`, `email`, dan alamat terstruktur (`addressLocality`, `addressRegion`, `addressCountry`).
  - `hasOfferCatalog`: Otomatis meng-generate `Service` catalog dari daftar baris layanan yang diinput di CMS.
  - Social proof: Menghubungkan profil media sosial via `sameAs`.
  - `WebSite` dengan `SearchAction` dinamis.
  - `WebPage` / `ItemPage` / `Article` sesuai konteks halaman dan artikel.
- **OpenGraph & Dynamic Cards:** Menggunakan endpoint `/og/card.png` dan `/og/[collection]/[slug].png` otomatis terhubung dengan identitas site.

## 5. Katalog Produk & Model Block Tambahan
- **Collection Products:** Didukung routing lengkap di `/products` dan `/products/[slug]`, tersinkronisasi 100 entitas produk hardware/PC.
- **Model Block Marketing Baru:**
  - `Steps.astro` (`marketing_steps`): Numbered sequence workflow (01, 02, 03) untuk panduan alur kerja / onboarding didukung animasi `@astroanimate/core`.
  - `Tabs.astro` (`marketing_tabs`): Tab switcher interaktif untuk memamerkan fitur/produk tanpa library runtime berat.
- **Breakout Embed Block:** Block section yang di-embed di dalam field RichText otomatis breakout 100% mengikuti kontainer `.frame` 1200px.
