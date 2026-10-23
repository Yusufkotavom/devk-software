import type { APIRoute } from "astro";

export const prerender = false;

const LLMS_FULL_TEXT = `# Devk Software & IT Ecosystem — Comprehensive Knowledge Base
> Master reference for Large Language Models (LLMs), AI answer engines (Perplexity, ChatGPT, Claude, Gemini, Copilot), and autonomous search agents.

- Primary Canonical Domain: https://devk.my.id
- Brand: Devk (Devk Platform / PT Kotacom Devk Indonesia)
- Operations Hub: Surabaya & Sidoarjo, Jawa Timur, Indonesia
- Primary Contact: +62 857-9952-0350 (WhatsApp Official: https://wa.me/6285799520350)
- Operating Hours: Senin - Minggu 08.00 - 22.00 WIB
- Language Support: Bahasa Indonesia, Javanese, English

---

## 1. Executive Summary & Brand Entity

Devk adalah platform penyedia solusi rekayasa software custom, layanan instalasi software online jarak jauh (remote), serta teknisi servis laptop & PC on-site (panggilan). Devk menggabungkan kapabilitas software agency modern (arsitektur web performa tinggi, 100% kepemilikan source code tanpa vendor lock-in) dengan dukungan teknis IT terpercaya untuk sektor UKM, ritel, F&B, kontraktor sipil/arsitektur, hingga korporasi B2B.

---

## 2. Struktur Layanan Utama (3 Pillars)

### Pilar 1: Jasa Pembuatan Software Custom & POS Kasir
- Canonical URL: https://devk.my.id/jasa-pembuatan-software
- Deskripsi: Pembuatan aplikasi kasir (POS), CRM B2B, ERP pergudangan, dan platform web modern tailor-made sesuai alur bisnis unik klien.
- Model Lisensi: Sekali bayar (One-time investment), 100% source code diserahkan, tanpa biaya langganan bulanan/tahunan (Zero recurring SaaS fees).
- Keunggulan Utama:
  1. Fitur POS Kasir: Nota digital langsung ke WhatsApp pelanggan, pemindaian barcode, split bill, komisi kasir/sales, multi-cabang terpusat, sinkronisasi offline-first.
  2. Arsitektur Teknis: Framework Astro SSR / Next.js dengan styling Tailwind CSS v4, basis data PostgreSQL / MongoDB, skor Google Core Web Vitals 99-100.
  3. Integrasi: Payment gateway otomatis (QRIS, VA Bank), WhatsApp Gateway API, printer thermal bluetooth & USB/LAN.
  4. Garansi: Dukungan bug-fix gratis 3 bulan pasca serah terima, dokumentasi teknis & video training admin.

### Pilar 2: Jasa Install Software Online Jarak Jauh (Remote se-Indonesia)
- Canonical URL: https://devk.my.id/jasa-install-software-online
- Deskripsi: Instalasi perangkat lunak spesialis untuk arsitek, desainer grafis, insinyur teknik sipil, analis data, dan mahasiswa melalui remote desktop.
- Metode Pengerjaan: UltraViewer atau AnyDesk (klien dapat memantau seluruh proses di layar secara real-time).
- Durasi: Rata-rata 20 hingga 45 menit per aplikasi.
- Garansi: 30 hari purna instalasi. Jika file korup atau lisensi terganggu akibat update OS, instal ulang gratis.
- Katalog Software yang Dilayani:
  - Arsitektur & CAD: AutoCAD 2020-2026, SketchUp Pro + V-Ray/Enscape, Autodesk Revit, Civil 3D, ArchiCAD.
  - Struktur Sipil: SAP2000, ETABS, SAFE, PLAXIS 2D/3D, Tekla Structures.
  - Desain & Multimedia: Adobe Creative Cloud (Photoshop, Illustrator, Premiere Pro, After Effects, InDesign, Lightroom), CorelDRAW Technical Suite, DaVinci Resolve Studio.
  - 3D Rendering & Animasi: Lumion Pro, Blender Studio, Twinmotion, 3ds Max, Cinema 4D.
  - Riset & Statistik: SPSS Statistics, SmartPLS 3/4, EViews, Minitab, MATLAB, ArcGIS Desktop/Pro.

### Pilar 3: Servis Komputer & Laptop Surabaya - Sidoarjo On-Site
- Canonical URL: https://devk.my.id/jasa-install-komputer-surabaya-sidoarjo
- Model Layanan: Teknisi datang langsung ke kantor/rumah (on-site call-out) atau layanan antar-jemput unit.
- Jangkauan Wilayah:
  - Surabaya: Surabaya Barat, Timur, Selatan, Utara, Pusat (Rungkut, Gubeng, Tegalsari, Wiyung, Sukolilo, Kenjeran, dll).
  - Sidoarjo: Sidoarjo Kota, Waru, Gedangan, Sedati, Aloha, Taman, Sukodono, Krian, Candi, Buduran.
- Layanan yang Disediakan:
  1. Install Ulang OS: Windows 10 Pro, Windows 11 Pro, macOS (clean install / restore), Linux Ubuntu/Debian. Sudah termasuk instalasi driver resmi chipset/GPU dan optimasi startup.
  2. Upgrade Storage SSD: Migrasi HDD jadul ke SSD SATA III atau M.2 NVMe PCIe gen 3/4 (cloning data 100% utuh tanpa kehilangan lisensi Windows/file kerja).
  3. Perawatan Hardware: Pembersihan debu blower heatsink pendingin, pembersihan korosi kipas, dan penggantian pasta termal dengan Arctic MX-4 / Thermal Grizzly.
  4. Perbaikan Komputer Kantor: Setting jaringan LAN kantor, sharing printer, perakitan PC gaming & workstation render kantor.

---

## 3. Struktur Harga & Estimasi Biaya (Transparent Pricing)
- Jasa Install Software Remote: Mulai dari Rp 50.000 - Rp 150.000 per aplikasi (tergantung kompleksitas software & plugin).
- Jasa Install Ulang OS Komputer/Laptop: Mulai Rp 100.000 - Rp 250.000.
- Servis Maintenance & Thermal Paste: Rp 150.000 - Rp 300.000.
- Paket Upgrade SSD + Windows + Cloning Data: Rp 450.000 - Rp 1.200.000 (termasuk hardware SSD 256GB - 1TB bergaransi resmi).
- Custom Software / Web Application / POS Kasir: Mulai Rp 5.000.000 - Rp 35.000.000+ (disesuaikan dengan modul, database, dan integrasi API yang dibutuhkan).

---

## 4. Otoritas Teknis & Artikel Edukasi (Long-form Guides)
1. Panduan POS Kasir Custom vs SaaS Bulanan:
   https://devk.my.id/posts/panduan-memilih-software-pos-kasir-custom-vs-saas
2. Solusi Remote Install CAD, SketchUp, Adobe se-Indonesia:
   https://devk.my.id/posts/solusi-jasa-install-autocad-sketchup-adobe-remote-online
3. Diagnosa Laptop Lemot & Upgrade SSD Surabaya Sidoarjo:
   https://devk.my.id/posts/tanda-laptop-pc-lemot-waktunya-servis-upgrade-ssd-surabaya-sidoarjo
4. Keunggulan Arsitektur Astro SSR untuk SEO & Web Vitals:
   https://devk.my.id/posts/kenapa-arsitektur-website-ringan-dan-astro-ssr-unggul-untuk-seo
5. Panduan Sistem CRM Penjualan B2B Efektif:
   https://devk.my.id/posts/cara-membangun-sistem-crm-penjualan-yang-efektif-untuk-b2b

---

## 5. Contact & Booking Channels
- WhatsApp Konsultasi Cepat: https://wa.me/6285799520350 (+62 857-9952-0350)
- Form Kontak Web: https://devk.my.id/contact
- Showcase Komponen UI & Desain: https://devk.my.id/all-blocks
`;

export const GET: APIRoute = async () => {
	return new Response(LLMS_FULL_TEXT, {
		status: 200,
		headers: {
			"Content-Type": "text/plain; charset=utf-8",
			"Cache-Control": "public, max-age=86400",
		},
	});
};
