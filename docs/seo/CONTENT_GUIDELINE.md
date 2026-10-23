# ✍️ Standar Pedoman Pembuatan Konten (Content Guideline) Devk

> **Dokumen Standarisasi Penulisan Konten, Format Visual, & Blok CMS Emdash**  
> Dibuat untuk memastikan seluruh halaman landing page, pilar, maupun artikel blog di situs Devk memiliki kualitas editorial, konversi tertinggi, dan performa SEO terbaik yang seragam.

---

## 1. Tone of Voice & Karakter Tulisan

* **Authoritative yet Approachable (Pakar yang Ramah)**: Bahasa teknis disampaikan dengan lugas, percaya diri, dan mudah dipahami oleh orang awam tanpa jargon yang membingungkan.
* **Empati & Berorientasi Solusi (Problem-Solver)**: Pahami frustrasi pengguna (contoh: laptop lemot, Blue Screen of Death, software error lisensi/aktivasi, bingung setup server, deadline mepet), lalu tawarkan solusi nyata.
* **Bebas Janji Palsu (No Clickbait)**: Sertakan estimasi waktu pengerjaan yang realistis, spesifikasi teknis riil, jaminan garansi tuntas, dan rincian harga yang jujur tanpa biaya tersembunyi.
* **Bahasa**: Bahasa Indonesia formal-modern (baku komunikatif, ejaan EYD disesuaikan kebutuhan digital profesional).

---

## 2. Standar Struktur & Hierarki Heading

Setiap halaman **WAJIB** mengikuti hierarki berikut demi keterbacaan bot mesin pencari (crawlers) dan kemudahan scanning pembaca manusia:

```
H1: Headline Utama Halaman (HANYA 1 per halaman, pada blok marketing_hero)
├── H2: Seksi Edukasi Masalah / Solusi (marketing_split atau marketing_bento_grid)
│   └── H3: Poin Spesifik / Sub-fitur / Spesifikasi
├── H2: Alur Pengerjaan Transparan (marketing_steps)
├── H2: Tabel Keunggulan Komparatif (marketing_comparison_table)
├── H2: Fitur Utama & Target Pengguna (marketing_features atau marketing_tabs)
├── H2: Pilihan Versi / Paket Layanan (marketing_pricing)
├── H2: Ajakan Booking Langsung (marketing_whatsapp_cta)
├── H2: Pertanyaan yang Sering Diajukan (marketing_faq)
└── H2: Call to Action Penutup (marketing_cta)
```

### Aturan Heading:
1. **H1 Wajib Memuat**: Keyword target utama + Nilai tambah (USP) + Garansi/Kecepatan (Maksimal 65 karakter).
2. **H2 Wajib Memuat**: LSI (*Latent Semantic Indexing*) keywords atau pertanyaan umum search intent pengguna.
3. **Paragraf Pertama**: Wajib menjawab *search intent* dalam 2–3 kalimat pertama (BLUF - *Bottom Line Up Front*).

---

## 3. Matriks Peran Blok Emdash (Extended Ecosystem)

Situs Devk mendukung 20 tipe blok Emdash. Berikut peran masing-masing blok dalam psikologi alur pembeli (*AIDA: Attention, Interest, Desire, Action*):

| Kategori | Tipe Blok Emdash | Peran dalam Funnel | Kapan Digunakan & Elemen Kunci |
| :--- | :--- | :--- | :--- |
| **Attention** | `marketing_hero` | **First Impression** | Wajib di paling atas halaman. Memuat H1, subheadline, tombol CTA WA, anchor harga, dan visual 16:9. |
| **Social Proof** | `marketing_marquee_logos` | **Trust & Authority** | Logo marquee bergulir halus tanpa henti (logo partner, ekosistem teknologi, brand hardware). |
| **Social Proof** | `marketing_stats` | **Credibility** | 4 angka metrik kunci (klien sukses, estimasi pengerjaan, persentase garansi, kompatibilitas OS). |
| **Interest** | `marketing_split` | **Education** | Layout teks berdampingan foto/diagram untuk mengedukasi akar masalah & metode solusi teknisi. |
| **Interest / Tech** | `marketing_bento_grid` | **Modern Showcase** | Grid asimetris (ala Vercel/Linear) untuk menonjolkan fitur unggulan, performa CPU/GPU, dan arsitektur sistem. |
| **Clarity** | `marketing_steps` | **Process Transparency** | Alur pengerjaan berurutan (01, 02, 03, 04) dari pemesanan, pengerjaan (on-site/remote), hingga garansi. |
| **Decision** | `marketing_comparison_table`| **Objection Killer** | Tabel komparasi head-to-head *Devk vs Cara Konvensional / Pasang Sendiri* (centang hijau vs silang abu). |
| **Relevance** | `marketing_features` | **Audience & Variants** | Grid fitur multi-kolom (2/3/4 kolom) dengan 29 opsi ikon SVG resmi dan deskripsi fungsional. |
| **Interactive**| `marketing_tabs` | **Product Switcher** | Tab interaktif untuk mendemonstrasikan versi OS, edisi software, atau paket servis hardware. |
| **Portfolio** | `marketing_slider` | **Visual Evidence** | Slider geser horizontal untuk mendokumentasikan foto hasil instalasi, rakit PC, atau portofolio website. |
| **Decision** | `marketing_pricing` | **Value Evaluation** | 3 paket harga transparan, rincian fitur/garansi, dan badge "Paling Laris" pada paket rekomendasi. |
| **High Action**| `marketing_whatsapp_cta` | **Direct Booking** | Kotak konversi WhatsApp terpusat (`variant: "card"` atau `"banner"`) dengan template pesan dinamis `{title}` & `{url}`. |
| **Trust** | `marketing_faq` | **Overcoming Doubts**| 5–8 tanya-jawab teknis seputar privasi data, spek minimum, durasi kerja, dan klaim garansi. |
| **Final Push** | `marketing_cta` | **Closing Conversion** | Banner penutup kontras tinggi sebelum footer dengan tombol pesan cepat dan konsultasi teknisi. |

---

## 4. Blueprint Komposisi Funnel per Klaster Pilar Bisnis

### A. Klaster Pilar 3: Servis Komputer & OS Lokal (Surabaya – Sidoarjo)
Urutan blok optimal untuk membangun kepercayaan pelanggan lokal:
1. `marketing_hero` — H1 fokus lokasi: Surabaya & Sidoarjo, teknisi panggilan / drop-off ke workshop.
2. `marketing_steps` — Alur 4 langkah mudah: *1. Hubungi WA & Konsultasi Kendala* -> *2. Teknisi ke Lokasi / Bawa ke Workshop* -> *3. Diagnosa & Pengerjaan di Depan Pelanggan* -> *4. Testing & Garansi Nota Resmi*.
3. `marketing_split` (Edukasi) — Risiko membiarkan OS rusak/corrupt atau servis di tempat abal-abal (data hilang, thermal throttling).
4. `marketing_comparison_table` — *Servis di Devk vs Tempat Servis Lain*: Pengerjaan transparan, backup data diprioritaskan, thermal paste grade premium, garansi 30 hari.
5. `marketing_features` — Cakupan area panggilan (Surabaya Timur, Selatan, Pusat, Barat, Utara, Waru, Gedangan, Sidoarjo Kota).
6. `marketing_pricing` — Paket transparan (Paket Standard, Paket Deep Cleaning + OS, Paket Enterprise/Kantor).
7. `marketing_whatsapp_cta` — Banner WhatsApp instan: *"Teknisi Kami Siap Meluncur ke Tempat Anda di Surabaya & Sidoarjo"*.
8. `marketing_faq` — Pertanyaan mengenai estimasi datang, backup data, dan sparepart original.
9. `marketing_cta` — Penutup & ajakan drop-off di Workshop Sidoarjo (Graha Indraprasta) / Surabaya (Tenggilis Mulya).

### B. Klaster Pilar 2: Jasa Install Software Online (Remote Service)
Urutan blok optimal untuk konversi cepat:
1. `marketing_hero` — Solusi software siap pakai via TeamViewer / UltraViewer tanpa ribet.
2. `marketing_marquee_logos` — Marquee deretan software yang kompatibel.
3. `marketing_stats` — 500+ instalasi sukses, 15-30 menit selesai, garansi 100% uang kembali.
4. `marketing_split` — Edukasi fitur software & konfigurasi performa hardware/GPU.
5. `marketing_comparison_table` — *Install di Devk vs Coba Download Sendiri* (bebas ransomware, lisensi permanen, bonus library/plugin).
6. `marketing_features` — Varian versi software yang didukung (2022, 2023, 2024, 2025/2026).
7. `marketing_pricing` — Pilihan paket (Single Software, Bundle 3 Software, Master Studio Suite).
8. `marketing_whatsapp_cta` — Box WhatsApp dengan prefill nama software.
9. `marketing_faq` — Keamanan remote, garansi update, dan tes render/running.
10. `marketing_cta` — Hubungi admin untuk jadwal instalasi instan.

### C. Klaster Pilar 1: Software House & Solusi IT B2B
Urutan blok optimal untuk audiens enterprise/bisnis:
1. `marketing_hero` — H1 value proposition sistem custom (POS, ERP, CRM, Custom Web).
2. `marketing_bento_grid` — Asymmetric feature grid (Database terenkripsi, Realtime Sync, Cloud Scale, Modern UI).
3. `marketing_tabs` — Demo modul sistem (Modul Kasir, Modul Inventory, Modul Laporan Akuntansi, Modul Multi-Cabang).
4. `marketing_steps` — Metodologi pengerjaan agile: *Brief & Mockup -> Development -> UAT & Training Karyawan -> SLA Maintenance*.
5. `marketing_comparison_table` — *Custom Software Devk vs Aplikasi Template Jadi*.
6. `marketing_pricing` — Paket estimasi implementasi.
7. `marketing_whatsapp_cta` — Jadwalkan demo / konsultasi gratis dengan Project Manager.
8. `marketing_faq` — Source code ownership, server deployment, integrasi API.
9. `marketing_cta` — Hubungi untuk proposal resmi.

---

## 5. Standar Gambar & Media Visual

Untuk menjaga estetika dan skor Core Web Vitals (LCP < 2.5 detik):

1. **Rasio Aspek & Dimensi**:
   * Format standar: **16:9** (Dimensi optimal: `1376x768` px atau `1920x1080` px).
   * Format file: **WebP** atau **JPEG terkompresi** (ukuran file di bawah 400 KB per gambar).
2. **Alt Text Berbasis SEO**:
   * Wajib mendeskripsikan isi visual secara alami + memuat kata kunci relevan.
   * *Contoh*: `alt="Teknisi Jasa Install Ulang Windows Surabaya dan Sidoarjo"`
3. **Caption Gambar**:
   * Cantumkan keterangan ringkas 3–6 kata pada `image_caption` untuk badge visual elegan.
4. **Struktur Input Emdash**:
   * Kolom gambar blok Emdash menerima ID media: `{"image": {"id": "ID_DARI_MEDIA_LIBRARY"}}`.

---

## 6. Checklist Validasi Pra-Publikasi (Pre-Flight Checklist)

Sebelum mempublikasikan (`published`) halaman baru:

- [ ] **SEO Title**: 50–60 karakter, memuat keyword utama + nama brand (`| Devk`).
- [ ] **Meta Description**: 130–155 karakter, memuat manfaat unik dan ajakan klik/CTA.
- [ ] **Canonical URL**: Terisi URL absolut `https://devk.my.id/<slug>` tanpa query parameters.
- [ ] **OpenGraph Image**: Terisi URL gambar thumbnail yang valid.
- [ ] **Tautan Internal (4-Point Rule)**:
  - Minimal 1 link ke Pilar Hub induk.
  - Minimal 2 link ke klaster saudara (*lateral siblings*).
  - Minimal 1 link jembatan antar pilar (*cross-pillar link*).
  - Minimal 1 link tombol WhatsApp dengan teks pre-filled khusus layanan.
- [ ] **Cek Validasi Blok**: Hanya gunakan blok resmi dan ikon yang ada dalam daftar Emdash.
- [ ] **Uji Tampilan Responsif**: Pastikan tampilan tabel komparasi, langkah (steps), dan bento grid rapi pada perangkat mobile & desktop.
