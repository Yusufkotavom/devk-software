# Panduan Lengkap Mengarahkan Project ke Domain Baru
**Repository:** `kotacom-emdash` (Astro + EmDash CMS + PostgreSQL)  
**Dokumentasi:** Prosedur Cutover / Migrasi Domain (Production / Staging)

---

## Daftar Isi
1. [Arsitektur Domain & Resolusi Origin](#1-arsitektur-domain--resolusi-origin)
2. [Langkah 1: Konfigurasi Astro (`astro.config.mjs`)](#langkah-1-konfigurasi-astro-astroconfigmjs)
3. [Langkah 2: Environment Variables (Runtime & Docker Swarm)](#langkah-2-environment-variables-runtime--docker-swarm)
4. [Langkah 3: File Source Code dengan Hardcoded Domain](#langkah-3-file-source-code-dengan-hardcoded-domain)
5. [Langkah 4: Pembaruan Database PostgreSQL (`kotacom_emdash`)](#langkah-4-pembaruan-database-postgresql-kotacom_emdash)
6. [Langkah 5: Routing Reverse Proxy (Traefik / Dokploy) & DNS](#langkah-5-routing-reverse-proxy-traefik--dokploy--dns)
7. [Langkah 6: Checklist Verifikasi Pasca-Migrasi](#langkah-6-checklist-verifikasi-pasca-migrasi)

---

## 1. Arsitektur Domain & Resolusi Origin

Project ini menggunakan fungsi utilitas terpusat di [`src/utils/origin.ts`](../src/utils/origin.ts) (`getSiteOrigin`) untuk membangun Canonical URLs, Open Graph (OG) Images, BreadcrumbList Schema, dan Robots Sitemap.

Prioritas penentuan domain:
1. `process.env.EMDASH_SITE_URL` atau `process.env.SITE_URL` (paling diprioritaskan).
2. Header request HTTP (`x-forwarded-host` / `host`).
3. Fallback default di konfigurasi Astro (`https://kotacom.id`).

Karena itu, sebagian besar halaman otomatis mengikuti domain baru saat Environment Variable diubah. Namun, ada beberapa pengaturan keamanan dan database yang tetap harus diperbarui.

---

## Langkah 1: Konfigurasi Astro (`astro.config.mjs`)

Buka file [`astro.config.mjs`](../astro.config.mjs):

### A. Daftarkan Domain pada `security.allowedDomains`
Astro memvalidasi keamanan *Origin* saat terjadi request form action, mutasi data, dan autentikasi login EmDash/Better-Auth. Jika domain baru tidak terdaftar, request POST akan ditolak (error 403 Forbidden).

Tambahkan domain baru Anda ke dalam array:
```javascript
security: {
    allowedDomains: [
        { protocol: "https", hostname: "kotacom.id" },
        { protocol: "https", hostname: "www.kotacom.id" },
        { protocol: "https", hostname: "**.kotacom.id" },
        { protocol: "https", hostname: "staging.devk.my.id" },
        { protocol: "https", hostname: "devk.my.id" },
        { protocol: "https", hostname: "**.devk.my.id" },
        // TAMBAHKAN DOMAIN BARU DI SINI:
        { protocol: "https", hostname: "domainbaru.com" },
        { protocol: "https", hostname: "www.domainbaru.com" },
        { protocol: "https", hostname: "**.domainbaru.com" },
        { protocol: "https", hostname: "localhost" },
        { protocol: "http", hostname: "localhost" }
    ],
},
```

### B. Daftarkan Domain pada `image.domains`
Jika aset media dimuat menggunakan nama domain baru tersebut:
```javascript
image: {
    layout: "constrained",
    responsiveStyles: true,
    domains: [
        "kotacom.id",
        "www.kotacom.id",
        "devk.my.id",
        "domainbaru.com", // Tambahkan domain baru
        "localhost"
    ],
    remotePatterns: [
        { protocol: "https" },
        { protocol: "http" },
    ],
},
```

---

## Langkah 2: Environment Variables (Runtime & Docker Swarm)

### A. File `.env` (Lokal & Staging Server)
Perbarui file `.env`:
```env
# Domain Publik Utama
SITE_URL=https://domainbaru.com
EMDASH_SITE_URL=https://domainbaru.com

# Better-Auth (Wajib sama persis dengan URL login admin)
BETTER_AUTH_URL=https://domainbaru.com

# EmDash API Client
EMDASH_BASE_URL=https://domainbaru.com
```

### B. Update Service di Docker Swarm (Dokploy)
Jika berjalan di Swarm service `app-program-online-application-cfreew`, perbarui environment variables service:
```bash
sudo docker service update \
  --env-add SITE_URL=https://domainbaru.com \
  --env-add EMDASH_SITE_URL=https://domainbaru.com \
  --env-add BETTER_AUTH_URL=https://domainbaru.com \
  --env-add EMDASH_BASE_URL=https://domainbaru.com \
  app-program-online-application-cfreew
```

---

## Langkah 3: File Source Code dengan Hardcoded Domain

Ada beberapa file endpoint informasi statis yang memuat teks domain lama secara hardcoded. Ganti `https://staging.devk.my.id` atau `https://devk.my.id` dengan domain baru Anda:

1. **`src/pages/llms.txt.ts`**
   * Cari: `https://staging.devk.my.id`
   * Ganti ke: `https://domainbaru.com`
2. **`src/pages/llms-full.txt.ts`**
   * Cari: `staging.devk.my.id` dan link terkait
   * Ganti ke: `domainbaru.com`
3. **`src/pages/pricing.md.ts`**
   * Ganti tag baris 6: `> Canonical: https://domainbaru.com/pricing.md`
4. **`src/components/blocks/BentoGrid.astro`**
   * Ganti teks demo baris 42: `code_snippet: "curl -X GET https://domainbaru.com/api/products"`
5. **`src/pages/compare.astro`**
   * Halaman audit internal pembanding URL. Sesuaikan jika sudah tidak dibutuhkan.

---

## Langkah 4: Pembaruan Database PostgreSQL (`kotacom_emdash`)

### A. Update Canonical URL di Tabel `_emdash_seo`
Sebanyak 116 entri landing page menyimpan canonical URL statis dari hasil migrasi lama. Jalankan query berikut di container PostgreSQL:

```sql
-- Cek jumlah baris yang terdampak
SELECT count(*) FROM _emdash_seo WHERE seo_canonical LIKE '%devk.my.id%' OR seo_canonical LIKE '%staging.devk.my.id%';

-- Update ke domain baru
UPDATE _emdash_seo 
SET seo_canonical = REPLACE(seo_canonical, 'https://staging.devk.my.id', 'https://domainbaru.com')
WHERE seo_canonical LIKE '%staging.devk.my.id%';

UPDATE _emdash_seo 
SET seo_canonical = REPLACE(seo_canonical, 'https://devk.my.id', 'https://domainbaru.com')
WHERE seo_canonical LIKE '%devk.my.id%';
```

### B. Update Konten Demo pada `ec_pages` (Opsional)
Halaman demo `/all-blocks` dan `/blocks` yang berisi teks demo domain:
```sql
UPDATE ec_pages 
SET content = REPLACE(content::text, 'staging.devk.my.id', 'domainbaru.com')::json
WHERE slug IN ('all-blocks', 'blocks');
```

---

## Langkah 5: Routing Reverse Proxy (Traefik / Dokploy) & DNS

1. **DNS Record:**
   Arahkan DNS Record (`A` / `CNAME`) domain baru ke IP server publik instance ini.
2. **Dokploy / Traefik Labels:**
   * Di dashboard Dokploy, masuk ke aplikasi `devk-software` / `kotacom-emdash`.
   * Masuk ke tab **Domains**.
   * Tambahkan domain baru (contoh: `domainbaru.com` atau `www.domainbaru.com`) dengan port target `3000`.
   * Aktifkan HTTPS / Let's Encrypt Certificate.

---

## Langkah 6: Checklist Verifikasi Pasca-Migrasi

Lakukan uji coba berikut setelah domain diarahkan:

- [ ] **Akses Beranda:** `curl -I https://domainbaru.com/` (Pastikan HTTP 200 OK).
- [ ] **Robots.txt:** Buka `https://domainbaru.com/robots.txt` dan pastikan baris sitemap tertulis:
  ```txt
  Sitemap: https://domainbaru.com/sitemap.xml
  ```
- [ ] **Sitemap Index & Children:**
  * Buka `https://domainbaru.com/sitemap.xml`
  * Buka `https://domainbaru.com/sitemap-projects.xml`
  * Pastikan seluruh `<loc>` sudah menggunakan prefix `https://domainbaru.com/...`.
- [ ] **Login & Admin EmDash:**
  * Akses `https://domainbaru.com/_emdash/admin`
  * Coba login dan buka menu **Projects**, **Posts**, dan **Pages**.
  * Coba lakukan edit dan save salah satu entri untuk memastikan tidak ada error CSRF / Origin mismatch.
- [ ] **Open Graph Image:**
  * Buka salah satu halaman project: `https://domainbaru.com/projects/starlight`
  * Periksa tag `<meta property="og:image">` dan pastikan mengarah ke `https://domainbaru.com/og/projects/starlight.png`.
