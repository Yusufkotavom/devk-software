# Bulk Generator & Programmatic SEO Architecture (Kotacom EmDash)

Dokumentasi lengkap sistem **Bulk Generator**, integrasi Spintax, Token Dataset, AI Injection (`{{ai:...}}`), dan panduan pembuatan Template SEO berkualitas tinggi untuk menghindari penalti *thin content*.

---

## 1. Arsitektur & Cara Kerja Generator

Bulk Generator di EmDash bekerja sebagai native plugin (`src/plugins/bulk-generator`) dengan integrasi langsung ke Custom Post Type (CPT) `page_templates` dan database PostgreSQL.

```
+--------------------------------------------------------------------------+
| 1. Dataset CSV                                                           |
| (kabupaten, provinsi, tipe_layanan, radius_layanan, karakteristik, dll) |
+--------------------------------------------------------------------------+
                                    |
                                    v
+--------------------------------------------------------------------------+
| 2. Template (page_templates CPT)                                         |
| - Title & Slug Pattern: "Jasa {{layanan | title}} {{kabupaten | title}}" |
| - Page Blocks (marketing_hero, split, features, pricing, faq, cta)      |
| - Spintax ({Opsi A|Opsi B|Opsi C})                                       |
| - Dynamic AI Prompt ({{ai:...}})                                         |
+--------------------------------------------------------------------------+
                                    |
                                    v
+--------------------------------------------------------------------------+
| 3. Substitution & AI Engine (tokens.ts / runner.ts)                      |
| - Step 1: Resolve {{ai:...}} prompt via Local AI Gateway (172.18.0.1)    |
| - Step 2: Replace token CSV: {{token}} / {{token | slug/title/upper}}    |
| - Step 3: Resolve Spintax / Word Rotation: {A|B|C}                       |
| - Step 4: Generate unique keys & bind to native blocks                   |
+--------------------------------------------------------------------------+
                                    |
                                    v
+--------------------------------------------------------------------------+
| 4. Dry Run & Execution (runner.ts)                                       |
| - Cek slug unik (mencegah duplikasi)                                     |
| - Drip schedule (opsional: menjadwalkan X halaman per hari)              |
| - Insert / Update ke `ec_pages` (blocks JSON & SEO Metadata)            |
+--------------------------------------------------------------------------+
```

---

## 2. Sintaks & Fitur Token yang Tersedia

### A. Dataset Token
Format: `{{nama_kolom}}`
Mengambil nilai dari kolom CSV dataset secara langsung.

### B. Filter String (Format Modifier)
Format: `{{nama_kolom | filter}}`
Tersedia filter:
- `slug` : Konversi teks ke slug URL ramah SEO (contoh: `Aceh Barat` -> `aceh-barat`).
- `title` : Mengubah teks menjadi Title Case (contoh: `cetak buku murah` -> `Cetak Buku Murah`).
- `lower` : Mengubah teks menjadi huruf kecil semua.
- `upper` : Mengubah teks menjadi HURUF BESAR.

### C. Spintax / Word Rotation (Pemutaran Kata Unik)
Format: `{pilihan_1|pilihan_2|pilihan_3}`
Setiap generasi baris akan memilih salah satu kata secara acak sehingga struktur kalimat antar kota berbeda-beda.
- Mendukung *nested spintax*: `{Pusat {cetak|penerbitan}|Layanan percetakan}`
- **Aturan penting:** Spintax harus mengandung karakter pipe `|`.

Contoh implementasi:
```text
{Spesialis|Pusat|Layanan} Cetak Buku di {{kabupaten}} {Cepat & Bergaransi|Standar Penerbit Resmi|Harga Terjangkau}.
```

### D. AI Injection Prompt (`{{ai:...}}`)
Format: `{{ai:Instruksi prompt Anda di sini}}`
Sistem akan mengirimkan prompt ke model AI lokal secara otomatis sebelum halaman disimpan. Token dataset bisa dimasukkan di dalam prompt AI:

Contoh:
```text
{{ai:Buatkan 1 paragraf unik (maksimal 45 kata) mengenai tantangan logistik atau kebutuhan percetakan buku dan materi edukasi untuk wilayah {{kabupaten}}, {{provinsi}}. Gunakan nada profesional dan solutif.}}
```

---

## 3. SEO Marketing Framework untuk Halaman Programmatic (pSEO)

Untuk mematuhi Google Search Quality Guidelines dan menghindari penalti *Doorway Pages / Thin Content*:

1. **Anti-Thin Content Rule:** Jangan sekadar mengganti nama kota pada teks yang persis sama. Kombinasikan:
   - Variasi Spintax pada Headline & Subheadline.
   - Kolom dataset unik (karakteristik wilayah, estimasi ongkir/durasi, rekomendasi kertas).
   - Injeksi AI paragraf konteks lokal (`{{ai:...}}`).
2. **Search Intent Matching:** Calon pembeli buku di daerah membutuhkan kepastian:
   - Berapa minimal oplah (Bisa satuan / POD).
   - Jenis kertas (Bookpaper krem vs HVS putih).
   - Pengiriman (Packing ekspedisi aman antar pulau/kabupaten).
   - Bukti mutu (Finishing lem panas, laminasi cover, sampel proofing).
3. **Internal Linking & Hub Architecture:**
   - Semua halaman kota harus terhubung kembali ke Hub Utama (`/produk`, `/layanan`, atau `/jasa-cetak-buku`).
   - Breadcrumb otomatis: `Home` > `Percetakan` > `Jasa Cetak Buku {{kabupaten}}`.

---

## 4. Struktur Template Native Block EmDash (`jasa-cetak-buku`)

Daftar blok yang digunakan pada template native:
- **`marketing_hero`**: Value proposition, nama wilayah, dual CTA (WhatsApp + Anchor Pricing).
- **`marketing_split`**: Penjelasan spesifikasi teknis (kertas bookpaper, lem panas, laminasi).
- **`marketing_features`**: Cakupan layanan (buku ajar, novel, company profile, jilid hard/soft cover).
- **`marketing_bento_grid` / `marketing_stats`**: Standar pengerjaan, proofing gratis, packaging aman.
- **`marketing_pricing`**: 3 pilihan paket transparan (Starter/POD, Growth, Custom Oplah).
- **`marketing_faq`**: Jawaban pertanyaan teknis cetak dan pengiriman.
- **`marketing_whatsapp_cta`**: Closing conversion CTA ke CS Kotacom.

---

## 5. Cara Menjalankan Generator

1. Masuk ke Admin Dashboard: `/_emdash/admin/generator`.
2. Pada tab **Dataset**: Upload atau pilih dataset CSV wilayah Indonesia.
3. Pada tab **Generate**:
   - Pilih Template: `Template Cetak Buku Nasional`.
   - Pilih Dataset: `Kabupaten & Kota Indonesia`.
   - Mode: `Update Existing` (untuk merefresh 399 halaman yang sudah ada) atau `Skip Existing`.
   - Klik **Preview** untuk memvalidasi rotasi kata & hasil render.
   - Klik **Run** untuk eksekusi.
