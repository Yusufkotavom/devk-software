# 📋 Template Skema Pembuatan Halaman Baru Emdash (Page Blueprint)

> **Cetak Biru Payload JSON Standar untuk MCP `content_create` & `content_update`**  
> Gunakan template ini setiap kali agen AI atau tim developer membuat landing page layanan baru agar struktur data, metadata SEO, dan blok marketing seragam serta memanfaatkan ekosistem blok terbaru.

---

## 1. Daftar Ikon Resmi yang Diizinkan

### A. Ikon Blok `marketing_features` (29 Ikon Resmi):
```
zap | shield | users | chart | code | globe | heart | star | check | lock | 
clock | cloud | building | leaf | gauge | thermometer | plug | bell | file | sun | trend |
storefront | cart | desktop | database | cpu | wrench | gear | rocket
```

### B. Ikon Blok `marketing_bento_grid` (12 Ikon Resmi):
```
zap | shield | users | chart | code | globe | sparkle | cpu | database | rocket | lock | check
```

*(Menggunakan nilai di luar daftar di atas akan memicu error `[VALIDATION_ERROR]`)*.

---

## 2. Struktur Payload Standar Halaman Layanan (`content_create`)

Blueprint teruji untuk konversi tinggi (menggabungkan alur kerja, edukasi, komparasi, pricing, dan WhatsApp CTA box):

```json
{
  "collection": "pages",
  "slug": "jasa-[nama-layanan-target]",
  "status": "published",
  "data": {
    "title": "[Judul Halaman Lengkap]",
    "content": [
      {
        "_key": "hero-section",
        "_type": "marketing_hero",
        "_version": 1,
        "centered": false,
        "eyebrow": "[Badge Kategori / Nilai Tambah]",
        "headline": "[H1 Headline Utama - Maks 65 Karakter]",
        "subheadline": "[Subheadline Penjelas Solusi & Garansi]",
        "primary_cta_label": "Pesan via WhatsApp",
        "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20tertarik%20dengan%20[NAMA_LAYANAN]",
        "secondary_cta_label": "Lihat Pilihan Paket",
        "secondary_cta_url": "#harga",
        "image": {
          "id": "[ID_MEDIA_HERO_DARI_MEDIA_UPLOAD]"
        },
        "image_caption": "[Caption Ringkas Gambar Hero]"
      },
      {
        "_key": "steps-workflow",
        "_type": "marketing_steps",
        "_version": 1,
        "eyebrow": "Transparan & Bebas Khawatir",
        "headline": "4 Langkah Mudah Penanganan Layanan",
        "subheadline": "Proses cepat dan terstruktur tanpa membuang waktu produktif Anda.",
        "steps": [
          { "step_number": "01", "title": "Konsultasi & Diagnosa", "description": "Hubungi admin via WhatsApp, jelaskan kendala atau kebutuhan software/hardware Anda." },
          { "step_number": "02", "title": "Penjadwalan / Kedatangan", "description": "Teknisi meluncur ke lokasi (Surabaya/Sidoarjo) atau setup remote via TeamViewer secara aman." },
          { "step_number": "03", "title": "Pengerjaan & Optimasi", "description": "Proses instalasi, pembersihan, atau konfigurasi tuntas dikerjakan langsung di depan Anda." },
          { "step_number": "04", "title": "Testing & Garansi Resmi", "description": "Uji coba performa bersama, serah terima nota, dan perlindungan garansi hingga 30 hari." }
        ]
      },
      {
        "_key": "split-edukasi",
        "_type": "marketing_split",
        "_version": 1,
        "eyebrow": "Standar Profesional",
        "headline": "Solusi Tuntas untuk Kendala [Topik Layanan]",
        "body": "[Paragraf edukasi mendalam mengenai fungsi, keunggulan teknis, dan standar industri.]",
        "points": "[Poin Keunggulan 1]\n[Poin Keunggulan 2]\n[Poin Keunggulan 3]\n[Poin Keunggulan 4]",
        "image": {
          "id": "[ID_MEDIA_ILUSTRASI_DARI_MEDIA_UPLOAD]"
        },
        "image_caption": "[Caption Gambar Split]",
        "image_first": true,
        "cta_label": "Konsultasikan Kebutuhan Anda",
        "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20ingin%20konsultasi%20layanan%20[NAMA_LAYANAN]"
      },
      {
        "_key": "comparison-table",
        "_type": "marketing_comparison_table",
        "_version": 1,
        "eyebrow": "Kenapa Memilih Devk?",
        "headline": "Keunggulan Nyata Dibandingkan Servis Konvensional",
        "subheadline": "Kualitas pengerjaan, transparansi, dan jaminan keamanan data yang membuat ribuan pelanggan percaya.",
        "us_title": "Layanan Resmi Devk",
        "competitor_title": "Tempat Servis Lain / Pasang Sendiri",
        "rows": [
          {
            "feature_name": "Garansi Resmi & Klaim Cepat",
            "feature_desc": "Garansi hingga 30 hari tanpa ribet jika terjadi kendala.",
            "us_value": "yes",
            "competitor_value": "no"
          },
          {
            "feature_name": "Keamanan Data Pribadi",
            "feature_desc": "Prosedur backup ketat, pengerjaan transparan di depan pemilik.",
            "us_value": "yes",
            "competitor_value": "no"
          },
          {
            "feature_name": "Spesifikasi & File Bersih 100%",
            "feature_desc": "Bebas malware, bloatware, atau ransomware tersembunyi.",
            "us_value": "yes",
            "competitor_value": "no"
          },
          {
            "feature_name": "Thermal Paste & Tools Grade Pro",
            "feature_desc": "Penggunaan thermal paste premium (Arctic MX-4/Noctua) untuk performa dingin.",
            "us_value": "yes",
            "competitor_value": "no"
          }
        ],
        "cta_label": "Dapatkan Layanan Terbaik Sekarang",
        "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20order"
      },
      {
        "_key": "features-cakupan",
        "_type": "marketing_features",
        "_version": 1,
        "eyebrow": "Cakupan Layanan",
        "headline": "Area & Varian Layanan yang Didukung",
        "subheadline": "[Rincian spesifikasi, varian OS, atau jangkauan wilayah.]",
        "columns": "3",
        "features": [
          { "icon": "desktop", "title": "[Fitur/Area 1]", "description": "[Uraian detail]", "link_url": "#", "link_label": "Selengkapnya" },
          { "icon": "wrench", "title": "[Fitur/Area 2]", "description": "[Uraian detail]", "link_url": "#", "link_label": "Selengkapnya" },
          { "icon": "shield", "title": "[Fitur/Area 3]", "description": "[Uraian detail]", "link_url": "#", "link_label": "Selengkapnya" },
          { "icon": "zap", "title": "[Fitur/Area 4]", "description": "[Uraian detail]", "link_url": "#", "link_label": "Selengkapnya" },
          { "icon": "gauge", "title": "[Fitur/Area 5]", "description": "[Uraian detail]", "link_url": "#", "link_label": "Selengkapnya" },
          { "icon": "clock", "title": "[Fitur/Area 6]", "description": "[Uraian detail]", "link_url": "#", "link_label": "Selengkapnya" }
        ]
      },
      {
        "_key": "pricing-section",
        "_type": "marketing_pricing",
        "_version": 1,
        "anchor_id": "harga",
        "headline": "Pilihan Paket Biaya Layanan",
        "plans": [
          {
            "name": "Paket Standar",
            "price": "Rp [Harga 1]",
            "period": "/unit",
            "description": "[Deskripsi paket standar]",
            "features": "[Fitur 1]\n[Fitur 2]\n[Fitur 3]\nGaransi 14 Hari Penuh",
            "cta_label": "Pilih Paket Ini",
            "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Standar"
          },
          {
            "name": "Paket Lengkap & Optimasi",
            "price": "Rp [Harga 2]",
            "period": "/unit",
            "description": "[Deskripsi paket rekomendasi]",
            "features": "[Fitur 1]\n[Fitur 2]\n[Fitur 3]\n[Fitur 4]\nGaransi 30 Hari Penuh",
            "cta_label": "Pesan Paket Populer",
            "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Lengkap",
            "highlighted": true,
            "badge": "Paling Laris"
          },
          {
            "name": "Paket Komplit / Multi-Unit",
            "price": "Rp [Harga 3]",
            "period": "/unit",
            "description": "[Deskripsi paket bisnis/kantor]",
            "features": "[Fitur 1]\n[Fitur 2]\n[Fitur 3]\n[Fitur 4]\nGaransi 60 Hari Penuh",
            "cta_label": "Pilih Paket Ini",
            "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Multi"
          }
        ]
      },
      {
        "_key": "whatsapp-box",
        "_type": "marketing_whatsapp_cta",
        "_version": 1,
        "headline": "Butuh Bantuan Mendesak Hari Ini?",
        "body": "Teknisi kami siap merespons via WhatsApp dalam 5 menit untuk konsultasi gratis atau penjadwalan langsung ke lokasi Anda di Surabaya & Sidoarjo.",
        "label": "Chat WhatsApp Sekarang",
        "custom_message": "Halo Devk, saya ingin konsultasi atau pesan layanan {title}. Apakah teknisi tersedia hari ini?",
        "variant": "card",
        "anchor_id": "wa-cta"
      },
      {
        "_key": "faq-section",
        "_type": "marketing_faq",
        "_version": 1,
        "headline": "Pertanyaan yang Sering Diajukan (FAQ)",
        "subheadline": "Jawaban lengkap seputar alur booking, keamanan data, dan jaminan pengerjaan.",
        "items": [
          { "question": "[Pertanyaan Alur Order]?", "answer": "[Jawaban alur 1-2-3-4-5]" },
          { "question": "[Pertanyaan Durasi / Waktu Datang]?", "answer": "[Jawaban durasi]" },
          { "question": "[Pertanyaan Keamanan Data Pribadi]?", "answer": "[Jawaban backup & privasi data]" },
          { "question": "[Pertanyaan Klaim Garansi]?", "answer": "[Jawaban klaim garansi tanpa biaya]" },
          { "question": "[Pertanyaan Lokasi Workshop & On-Site]?", "answer": "[Jawaban workshop Graha Indraprasta Sidoarjo & Tenggilis Mulya Surabaya]" }
        ]
      },
      {
        "_key": "cta-bottom",
        "_type": "marketing_cta",
        "_version": 1,
        "headline": "Solusi Tuntas Kendala Komputer & Software Anda Hari Ini",
        "body": "Percayakan pada teknisi profesional Devk. Cepat, aman, bergaransi resmi, dan didukung ribuan pelanggan puas di Surabaya & Sidoarjo.",
        "primary_cta_label": "Hubungi WhatsApp Sekarang",
        "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20order",
        "secondary_cta_label": "Konsultasi Gratis",
        "secondary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20mau%20tanya-tanya%20dulu",
        "image": {
          "id": "[ID_MEDIA_HERO_DARI_MEDIA_UPLOAD]"
        }
      }
    ]
  },
  "seo": {
    "title": "[Judul SEO 50-60 Karakter] | Devk",
    "description": "[Meta deskripsi 130-155 karakter dengan CTA dan keunggulan].",
    "canonical": "https://devk.my.id/jasa-[nama-layanan-target]",
    "image": "https://software.devk.my.id/_emdash/api/media/file/[STORAGE_KEY_GAMBAR].jpg",
    "noIndex": false
  }
}
```

---

## 3. Katalog Payload Blok Tambahan (Extended Blocks)

### A. `marketing_bento_grid` (Bento Grid Showcase)
```json
{
  "_key": "bento-grid",
  "_type": "marketing_bento_grid",
  "_version": 1,
  "eyebrow": "Teknologi & Keunggulan",
  "headline": "Arsitektur Sistem Modern Berstandar Enterprise",
  "subheadline": "Kombinasi performa tinggi, keamanan data mutakhir, dan kemudahan operasional.",
  "items": [
    {
      "title": "Enkripsi Database Tingkat Bank",
      "description": "Seluruh transaksi dan data pelanggan diamankan dengan enkripsi AES-256.",
      "tag": "SECURITY",
      "badge": "Enterprise Ready",
      "col_span": "2",
      "row_span": "1",
      "icon": "shield",
      "link_url": "#",
      "link_label": "Pelajari Keamanan"
    },
    {
      "title": "Sinkronisasi Realtime Cloud",
      "description": "Multi-cabang terhubung langsung tanpa delay data.",
      "tag": "SPEED",
      "col_span": "1",
      "row_span": "1",
      "icon": "zap"
    },
    {
      "title": "Optimasi GPU & Akselerasi Hardware",
      "description": "Konfigurasi driver studio eksklusif untuk rendering 3D tanpa bottleneck.",
      "tag": "PERFORMANCE",
      "col_span": "3",
      "row_span": "1",
      "icon": "cpu",
      "code_snippet": "nvidia-smi --query-gpu=utilization.gpu,temperature.gpu --format=csv\n# Devk Tuned: Max Efficiency, 0 Thermal Throttling"
    }
  ]
}
```

### B. `marketing_tabs` (Content / Feature Tabs)
```json
{
  "_key": "service-tabs",
  "_type": "marketing_tabs",
  "_version": 1,
  "eyebrow": "Pilihan Fleksibel",
  "headline": "Pilih Sistem Operasi Sesuai Kebutuhan Perangkat",
  "subheadline": "Kami mendukung seluruh ekosistem komputasi modern.",
  "tabs": [
    {
      "label": "Windows 11 / 10 Pro",
      "title": "Instalasi Windows Original & Optimasi Driver",
      "description": "Instalasi bersih (Clean Install) bebas bloatware, aktivasi permanen, update patch keamanan terbaru, dan paket software esensial.",
      "cta_label": "Order Servis Windows",
      "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20install%20Windows"
    },
    {
      "label": "macOS (Apple Silicon & Intel)",
      "title": "macOS Sonoma / Sequoia & Restore iMac/MacBook",
      "description": "Penanganan khusus MacBook Air, Pro, Mac Mini, dan iMac. Termasuk migrasi Apple ID, bypass iCloud recovery, dan kalibrasi baterai.",
      "cta_label": "Order Servis MacBook",
      "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20servis%20Mac"
    },
    {
      "label": "Linux Desktop & Server",
      "title": "Ubuntu, Debian, Fedora & Server Production",
      "description": "Setup dual-boot, kernel tuning, Docker environment, dan konfigurasi server headless untuk kebutuhan developer & korporasi.",
      "cta_label": "Order Setup Linux",
      "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20setup%20Linux"
    }
  ]
}
```

### C. `marketing_marquee_logos` (Logo Marquee - Infinite Scroll)
```json
{
  "_key": "logo-marquee",
  "_type": "marketing_marquee_logos",
  "_version": 1,
  "headline": "Didukung oleh Kompatibilitas Software & Brand Hardware Terkemuka",
  "logos": [
    { "name": "Autodesk", "logo_url": "https://software.devk.my.id/_emdash/api/media/file/autodesk-logo.svg" },
    { "name": "Adobe", "logo_url": "https://software.devk.my.id/_emdash/api/media/file/adobe-logo.svg" },
    { "name": "Microsoft", "logo_url": "https://software.devk.my.id/_emdash/api/media/file/microsoft-logo.svg" },
    { "name": "Chaos V-Ray", "logo_url": "https://software.devk.my.id/_emdash/api/media/file/chaos-logo.svg" },
    { "name": "Asus ROG", "logo_url": "https://software.devk.my.id/_emdash/api/media/file/asus-logo.svg" },
    { "name": "Lenovo Legion", "logo_url": "https://software.devk.my.id/_emdash/api/media/file/lenovo-logo.svg" }
  ]
}
```

### D. `marketing_slider` (Horizontal Slider)
```json
{
  "_key": "portfolio-slider",
  "_type": "marketing_slider",
  "_version": 1,
  "eyebrow": "Dokumentasi Riil",
  "headline": "Galeri Pengerjaan Teknisi Kami di Lapangan",
  "subheadline": "Bukti pengerjaan rapi, transparan, dan terpercaya oleh tim teknisi Devk.",
  "slides": [
    {
      "title": "Clean Install & Cable Management PC Gaming",
      "description": "Rakit PC workstation Surabaya Barat dengan airflow optimal dan instalasi Windows 11 Pro.",
      "image_url": "https://software.devk.my.id/_emdash/api/media/file/rakit-pc-case.jpg",
      "link_label": "Lihat Layanan Rakit PC",
      "link_url": "/jasa-rakit-pc-surabaya-sidoarjo"
    },
    {
      "title": "Deep Cleaning & Repaste Laptop Panas",
      "description": "Penggantian pasta pendingin Arctic MX-4 menurunkan suhu prosesor hingga 22°C.",
      "image_url": "https://software.devk.my.id/_emdash/api/media/file/repaste-laptop.jpg",
      "link_label": "Lihat Layanan Servis Laptop",
      "link_url": "/jasa-servis-laptop-panggilan-surabaya-sidoarjo"
    }
  ]
}
```
