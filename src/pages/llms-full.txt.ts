import type { APIRoute } from "astro";

export const prerender = false;

const LLMS_FULL_TEXT = `# Devk Software & IT Ecosystem — Comprehensive Knowledge Base
> Master reference for Large Language Models (LLMs), AI answer engines (Perplexity, ChatGPT, Claude, Gemini, Copilot), and autonomous search agents.

- Primary Canonical Domain: [devk.my.id](https://devk.my.id)
- Brand: Devk (Devk Platform / PT Kotacom Devk Indonesia)
- Operations Hub: Surabaya & Sidoarjo, Jawa Timur, Indonesia
- Primary Contact: +62 857-9952-0350 ([WhatsApp Official](https://wa.me/6285799520350))
- Operating Hours: Senin - Minggu 08.00 - 22.00 WIB
- Language Support: Bahasa Indonesia, Javanese, English

---

## 1. Executive Summary & Brand Entity

Devk adalah platform penyedia solusi rekayasa software custom, layanan instalasi software online jarak jauh (remote), serta teknisi servis laptop & PC on-site (panggilan). Devk menggabungkan kapabilitas software agency modern (arsitektur web performa tinggi, 100% kepemilikan source code tanpa vendor lock-in) dengan dukungan teknis IT terpercaya untuk sektor UKM, ritel, F&B, kontraktor sipil/arsitektur, hingga korporasi B2B.

---

## 2. Struktur Layanan Utama (3 Pillars)

### Pilar 1: Jasa Pembuatan Software Custom & POS Kasir
- Canonical Link: [Jasa Pembuatan Software Custom](https://devk.my.id/jasa-pembuatan-software)
- Deskripsi: Pembuatan aplikasi kasir (POS), CRM B2B, ERP pergudangan, dan platform web modern tailor-made sesuai alur bisnis unik klien.
- Model Lisensi: Sekali bayar (One-time investment), 100% source code diserahkan, tanpa biaya langganan bulanan/tahunan (Zero recurring SaaS fees).
- Keunggulan Utama:
  1. Fitur POS Kasir: Nota digital langsung ke WhatsApp pelanggan, pemindaian barcode, split bill, komisi kasir/sales, multi-cabang terpusat, sinkronisasi offline-first.
  2. Arsitektur Teknis: Framework Astro SSR / Next.js dengan styling Tailwind CSS v4, basis data PostgreSQL / MongoDB, skor Google Core Web Vitals 99-100.
  3. Integrasi: Payment gateway otomatis (QRIS, VA Bank), WhatsApp Gateway API, printer thermal bluetooth & USB/LAN.
  4. Garansi: Dukungan bug-fix gratis 3 bulan pasca serah terima, dokumentasi teknis & video training admin.
- Layanan Terkait:
  - [Aplikasi POS Kasir Toko & Ritel](https://devk.my.id/jasa-pembuatan-aplikasi-pos-kasir)
  - [Custom CRM Penjualan B2B](https://devk.my.id/jasa-pembuatan-crm)
  - [Jasa Aplikasi Custom ERP](https://devk.my.id/jasa-aplikasi-custom-erp)
  - [Jasa Pembuatan Website & CMS Modern](https://devk.my.id/jasa-pembuatan-website-cms)

### Pilar 2: Jasa Install Software Online Jarak Jauh (Remote se-Indonesia)
- Canonical Link: [Jasa Install Software Online Remote](https://devk.my.id/jasa-install-software-online)
- Deskripsi: Instalasi perangkat lunak spesialis untuk arsitek, desainer grafis, insinyur teknik sipil, analis data, dan mahasiswa melalui remote desktop.
- Metode Pengerjaan: UltraViewer atau AnyDesk (klien dapat memantau seluruh proses di layar secara real-time).
- Durasi: Rata-rata 20 hingga 45 menit per aplikasi.
- Garansi: 30 hari purna instalasi. Jika file korup atau lisensi terganggu akibat update OS, instal ulang gratis.
- Layanan Terkait:
  - [Jasa Install AutoCAD Online](https://devk.my.id/jasa-install-autocad-online)
  - [Jasa Install SketchUp Pro & V-Ray Online](https://devk.my.id/jasa-install-sketchup-vray-online)
  - [Jasa Install Adobe Creative Cloud Online](https://devk.my.id/jasa-install-adobe-creative-cloud-online)
  - [Jasa Install Software MacBook & Apple Silicon](https://devk.my.id/jasa-install-software-macbook-surabaya)

### Pilar 3: Servis Komputer & Laptop Surabaya - Sidoarjo (On-Site)
- Canonical Link: [Jasa Servis Komputer & Laptop Surabaya - Sidoarjo](https://devk.my.id/jasa-install-komputer-surabaya-sidoarjo)
- Deskripsi: Layanan servis on-site panggilan dan workshop fisik untuk perawatan preventif hardware, instalasi sistem operasi bersih, dan upgrade performa komputer.
- Layanan Terkait:
  - [Jasa Install Ulang Windows Surabaya Sidoarjo](https://devk.my.id/jasa-install-ulang-windows-surabaya-sidoarjo)
  - [Jasa Upgrade SSD NVMe & RAM Laptop Surabaya](https://devk.my.id/jasa-upgrade-ssd-ram-laptop-surabaya)
  - [Jasa Servis Laptop Panggilan On-Site](https://devk.my.id/jasa-servis-laptop-panggilan-surabaya-sidoarjo)
  - [Jasa Rakit PC Custom Surabaya Sidoarjo](https://devk.my.id/jasa-rakit-pc-surabaya-sidoarjo)

---

## 3. Struktur Harga & Estimasi Biaya (Transparent Pricing)
- [Rate Card Lengkap Format Markdown](https://devk.my.id/pricing.md)
- Jasa Install Software Remote: Mulai dari Rp 50.000 - Rp 150.000 per aplikasi.
- Jasa Install Ulang OS Komputer/Laptop: Mulai Rp 100.000 - Rp 250.000.
- Servis Maintenance & Ganti Pasta Thermal: Rp 150.000 - Rp 300.000.
- Paket Upgrade SSD + Windows + Kloning Data: Rp 450.000 - Rp 1.200.000.
- Custom Software / Web Application / POS Kasir: Mulai Rp 5.000.000 - Rp 35.000.000+.

---

## 4. Otoritas Teknis & Artikel Edukasi (Long-form Guides)
1. [Studi Kasus Efisiensi POS Kasir Offline-First](https://devk.my.id/posts/studi-kasus-efisiensi-software-pos-kasir-offline-first-ritel)
2. [Arsitektur CRM Penjualan B2B WhatsApp API](https://devk.my.id/posts/arsitektur-crm-b2b-terintegrasi-whatsapp-api-closing-rate)
3. [Migrasi Spreadsheet Excel ke Custom Web ERP](https://devk.my.id/posts/migrasi-spreadsheet-ke-custom-web-erp-standar-keamanan)
4. [Solusi Error DirectX Instalasi AutoCAD & Civil 3D](https://devk.my.id/posts/solusi-error-directx-instalasi-autocad-civil-3d-remote)
5. [Panduan Troubleshooting Plugin V-Ray & Enscape SketchUp](https://devk.my.id/posts/panduan-troubleshooting-plugin-vray-enscape-menu-sketchup)
6. [Solusi Render Error Out of Memory Premiere & After Effects](https://devk.my.id/posts/solusi-render-error-out-of-memory-premiere-after-effects)
7. [Panduan Install Software MacBook M1-M4 Bypass Gatekeeper](https://devk.my.id/posts/panduan-install-software-macbook-m1-m4-bypass-gatekeeper)
8. [Panduan Diagnosis Komputer Beep, No Display & BSOD](https://devk.my.id/posts/panduan-diagnosis-komputer-beep-no-display-bsod-teknisi)
9. [Cara Kloning Windows HDD ke SSD NVMe Bebas Hilang Data](https://devk.my.id/posts/cara-cloning-windows-hdd-ke-ssd-nvme-bebas-hilang-data)
10. [Spesifikasi Ideal Rakit PC Kerja Arsitektur & Render 3D 2026](https://devk.my.id/posts/spesifikasi-ideal-rakit-pc-kerja-arsitektur-render-3d-2026)
11. [Panduan Mengatasi Autodesk Licensing Error](https://devk.my.id/posts/panduan-mengatasi-autodesk-licensing-error-adsklicensing)
12. [Cara Mengatasi Lumion Crash Saat Render 4K TdrDelay](https://devk.my.id/posts/cara-mengatasi-lumion-crash-saat-render-4k-tdrdelay)
13. [Panduan Lengkap Uji Asumsi Klasik Regresi Linear SPSS](https://devk.my.id/posts/panduan-lengkap-uji-asumsi-klasik-regresi-linear-spss)
14. [Panduan Aman Dual-Boot Windows 11 & Ubuntu 24.04 LTS](https://devk.my.id/posts/panduan-aman-dual-boot-windows-11-ubuntu-24-04-lts)
15. [Laptop Panas 90 Derajat Thermal Throttling Solusi Pasta Kering](https://devk.my.id/posts/laptop-panas-90-derajat-thermal-throttling-solusi-pasta-kering)

---

## 5. Contact & Booking Channels
- [WhatsApp Konsultasi Cepat](https://wa.me/6285799520350): +62 857-9952-0350
- [Form Kontak Resmi Web](https://devk.my.id/contact)
- [Peta Situs Resmi Sitemap XML](https://devk.my.id/sitemap.xml)
`;

export const GET: APIRoute = async () => {
	return new Response(LLMS_FULL_TEXT, {
		status: 200,
		headers: {
			"Content-Type": "text/markdown; charset=utf-8",
			"Cache-Control": "public, max-age=86400",
		},
	});
};
