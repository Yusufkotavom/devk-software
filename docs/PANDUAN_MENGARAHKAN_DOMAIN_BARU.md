# Panduan Lengkap & Otomasi Migrasi Domain Kotacom EmDash
**Repository:** `kotacom-emdash` (Astro + EmDash CMS + PostgreSQL)  
**Dokumentasi:** Prosedur Cutover / Migrasi Domain (Manual & Otomatis via AI/CLI)

---

## Ringkasan Cepat: Otomasi untuk AI & Developer (1 Perintah)

Untuk mengubah seluruh konfigurasi domain secara menyeluruh (Astro Config, Environment Variables, PostgreSQL Canonical & Media URLs, serta Docker Swarm), cukup jalankan script otomatis:

```bash
# Jalankan migrasi menyeluruh (Code + DB + Swarm + Verifikasi)
python3 scripts/migrate_domain.py <domain-baru.com> --all

# Contoh: migrasi ke domain produksi kotacom.id
python3 scripts/migrate_domain.py kotacom.id --all

# Contoh: preview perubahan tanpa eksekusi (Dry Run)
python3 scripts/migrate_domain.py kotacom.id --dry-run --all
```

---

## Daftar Isi
1. [Arsitektur Domain & Dynamic Origin](#1-arsitektur-domain--dynamic-origin)
2. [Cara Kerja Script Otomasi `scripts/migrate_domain.py`](#2-cara-kerja-script-otomasi-scriptsmigrate_domainpy)
3. [Langkah Manual 1: Konfigurasi Astro (`astro.config.mjs`)](#langkah-manual-1-konfigurasi-astro-astroconfigmjs)
4. [Langkah Manual 2: Environment Variables (`.env` & Swarm)](#langkah-manual-2-environment-variables-env--swarm)
5. [Langkah Manual 3: Pembaruan Database PostgreSQL (`kotacom_emdash`)](#langkah-manual-3-pembaruan-database-postgresql-kotacom_emdash)
6. [Langkah Manual 4: Reverse Proxy (Dokploy / Traefik) & DNS](#langkah-manual-4-reverse-proxy-dokploy--traefik--dns)
7. [Checklist Verifikasi Pasca-Migrasi](#checklist-verifikasi-pasca-migrasi)

---

## 1. Arsitektur Domain & Dynamic Origin

Project ini dirancang untuk menyelesaikan URL origin secara dinamis melalui utilitas [`src/utils/origin.ts`](../src/utils/origin.ts) (`getSiteOrigin(site, requestOrigin)`).

Prioritas penentuan origin:
1. `process.env.EMDASH_SITE_URL` atau `process.env.SITE_URL` (Prioritas tertinggi, ditentukan di runtime).
2. Header request HTTP (`x-forwarded-host` / `host`).
3. Fallback konfigurasi Astro (`https://kotacom.id`).

File-file berikut **sudah dibuat dinamis** sehingga tidak lagi membutuhkan pengubahan manual:
* `src/pages/robots.txt.ts` -> Mengambil sitemap URL dari dynamic origin.
* `src/pages/sitemap.xml.ts` & seluruh sitemap sub-collection (`sitemap-posts.xml.ts`, `sitemap-pages.xml.ts`, `sitemap-products.xml.ts`, `sitemap-projects.xml.ts`).
* `src/pages/llms.txt.ts` & `src/pages/llms-full.txt.ts` -> Menggunakan `getSiteOrigin(site, url.origin)`.
* `src/pages/pricing.md.ts` -> Menggunakan `getSiteOrigin(site, url.origin)`.
* `src/lib/og/og-card.ts` -> Open Graph image URL dinamis.

---

## 2. Cara Kerja Script Otomasi `scripts/migrate_domain.py`

Script [`scripts/migrate_domain.py`](../scripts/migrate_domain.py) dibuat khusus agar AI Agent maupun Sysadmin dapat melakukan migrasi tanpa risiko human error:

| Opsi Flag | Kegunaan |
| :--- | :--- |
| `<domain>` | Domain tujuan (misal: `kotacom.id` atau `staging.kotacom.id`). Prefix `https://` otomatis dibersihkan. |
| `--all` | Menjalankan seluruh tahapan (Astro config + .env + DB update + Swarm update + Test Verifikasi). |
| `--update-code` | Hanya memperbarui `astro.config.mjs` (`security.allowedDomains` & `image.domains`) dan `.env`. |
| `--update-db` | Hanya memperbarui query replace pada PostgreSQL (`_emdash_seo` dan `_emdash_menu_items`). |
| `--update-swarm` | Hanya memperbarui service environment Docker Swarm. |
| `--verify` | Menjalankan tes GET HTTP ke `/robots.txt`, `/sitemap.xml`, `/sitemap-projects.xml`, `/llms.txt`. |
| `--dry-run` | Menampilkan simulasi perubahan tanpa mengubah file, DB, atau service apapun. |

---

## Langkah Manual 1: Konfigurasi Astro (`astro.config.mjs`)

Jika Anda memilih melakukan perubahan manual tanpa script:

### A. Daftarkan Domain pada `security.allowedDomains`
Astro memvalidasi keamanan *Origin* saat ada request form action, mutasi data, dan autentikasi login EmDash/Better-Auth. Jika domain baru tidak terdaftar, request POST ditolak (403 Forbidden).

Buka [`astro.config.mjs`](../astro.config.mjs) dan tambahkan:
```javascript
security: {
    allowedDomains: [
        { protocol: "https", hostname: "kotacom.id" },
        { protocol: "https", hostname: "www.kotacom.id" },
        { protocol: "https", hostname: "staging.devk.my.id" },
        // Tambahkan domain baru:
        { protocol: "https", hostname: "domainbaru.com" },
        { protocol: "https", hostname: "**.domainbaru.com" },
        { protocol: "https", hostname: "localhost" },
        { protocol: "http", hostname: "localhost" }
    ],
},
```

### B. Daftarkan Domain pada `image.domains`
Jika aset media dioptimasi oleh Astro Image Service menggunakan domain baru:
```javascript
image: {
    domains: [
        "kotacom.id",
        "devk.my.id",
        "domainbaru.com", // Tambahkan domain baru
        "localhost"
    ],
},
```

---

## Langkah Manual 2: Environment Variables (`.env` & Swarm)

### A. File `.env` (Lokal & Server Host)
Perbarui baris berikut di `.env`:
```env
# Domain Publik Utama
SITE_URL=https://domainbaru.com
EMDASH_SITE_URL=https://domainbaru.com

# Better-Auth (Wajib persis dengan URL login admin)
BETTER_AUTH_URL=https://domainbaru.com

# EmDash API Client
EMDASH_BASE_URL=https://domainbaru.com
```

### B. Update Service Docker Swarm (Dokploy)
Jalankan perintah ini di shell server:
```bash
sudo docker service update \
  --env-add SITE_URL=https://domainbaru.com \
  --env-add EMDASH_SITE_URL=https://domainbaru.com \
  --env-add BETTER_AUTH_URL=https://domainbaru.com \
  --env-add EMDASH_BASE_URL=https://domainbaru.com \
  app-program-online-application-cfreew
```

---

## Langkah Manual 3: Pembaruan Database PostgreSQL (`kotacom_emdash`)

Di database PostgreSQL, terdapat 3 tabel utama yang menyimpan referensi domain lama:
1. `_emdash_seo.seo_canonical` (116 baris canonical URLs lama)
2. `_emdash_seo.seo_image` (45 baris media image lama)
3. `_emdash_menu_items.custom_url` (3 baris custom link navigasi)

Eksekusi perintah SQL berikut ke container PostgreSQL:

```bash
# Temukan ID container database
DB_CONTAINER=$(sudo docker ps --filter "name=devk-software-db" --format "{{.ID}}")

# Jalankan query SQL penggantian domain
sudo docker exec -i $DB_CONTAINER psql -U dokploy -d kotacom_emdash << 'EOF'
-- 1. Update Canonical URLs
UPDATE _emdash_seo 
SET seo_canonical = REPLACE(seo_canonical, 'staging.devk.my.id', 'domainbaru.com')
WHERE seo_canonical LIKE '%staging.devk.my.id%';

UPDATE _emdash_seo 
SET seo_canonical = REPLACE(seo_canonical, 'devk.my.id', 'domainbaru.com')
WHERE seo_canonical LIKE '%devk.my.id%';

-- 2. Update Media URLs di SEO
UPDATE _emdash_seo 
SET seo_image = REPLACE(seo_image, 'software.devk.my.id', 'domainbaru.com')
WHERE seo_image LIKE '%software.devk.my.id%';

UPDATE _emdash_seo 
SET seo_image = REPLACE(seo_image, 'staging.devk.my.id', 'domainbaru.com')
WHERE seo_image LIKE '%staging.devk.my.id%';

-- 3. Update Menu Items Custom URLs
UPDATE _emdash_menu_items 
SET custom_url = REPLACE(custom_url, 'devk.my.id', 'domainbaru.com')
WHERE custom_url LIKE '%devk.my.id%';
EOF
```

---

## Langkah Manual 4: Reverse Proxy (Dokploy / Traefik) & DNS

1. **DNS Server:**
   Arahkan `A` Record atau `CNAME` dari `domainbaru.com` ke IP publik server Swarm / Traefik.
2. **Dashboard Dokploy:**
   * Buka Dashboard Dokploy -> Proyek `devk-software` / `kotacom-emdash`.
   * Buka tab **Domains**.
   * Tambahkan `domainbaru.com` (Target port: `3000`).
   * Aktifkan sertifikat HTTPS / Let's Encrypt.

---

## Checklist Verifikasi Pasca-Migrasi

Jalankan pengujian cepat untuk memastikan seluruh fungsi telah beralih dengan sempurna:

- [ ] **Home Page:**
  ```bash
  curl -I https://domainbaru.com/
  # Pastikan respon HTTP/2 200
  ```
- [ ] **Robots.txt:**
  ```bash
  curl -s https://domainbaru.com/robots.txt
  # Pastikan tertulis: Sitemap: https://domainbaru.com/sitemap.xml
  ```
- [ ] **Sitemap Index & Projects:**
  ```bash
  curl -s https://domainbaru.com/sitemap.xml | grep "<loc>" | head -n 5
  curl -s https://domainbaru.com/sitemap-projects.xml | grep "<loc>" | head -n 5
  # Pastikan seluruh link sudah menggunakan prefix https://domainbaru.com/
  ```
- [ ] **LLMs & Pricing Endpoints:**
  ```bash
  curl -s https://domainbaru.com/llms.txt | head -n 5
  curl -s https://domainbaru.com/pricing.md | head -n 5
  # Pastikan Canonical URL mengarah ke https://domainbaru.com/
  ```
- [ ] **Admin & Editing CMS:**
  * Login ke `https://domainbaru.com/_emdash/admin`
  * Buka menu **Projects** -> Pilih salah satu project (contoh: `Starlight`).
  * Lakukan edit deskripsi kecil lalu klik **Save Draft** atau **Publish**.
  * Pastikan tidak terjadi error CSRF Origin `403` dan data tersimpan di PostgreSQL.
