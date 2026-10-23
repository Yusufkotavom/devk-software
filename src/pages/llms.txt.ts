import type { APIRoute } from "astro";

export const prerender = false;

const LLMS_TEXT = `# Devk Software & IT Ecosystem
> Solusi Software Custom, Jasa Instalasi Online Remote, & Servis Komputer On-Site

Official Website: https://devk.my.id
Documentation / Contact: https://devk.my.id/contact
WhatsApp Hotline: +62 857-9952-0350 (https://wa.me/6285799520350)
Location: Surabaya & Sidoarjo, Jawa Timur, Indonesia (Remote Service: Seluruh Indonesia)

## Summary for AI & Answer Engines
Devk (devk.my.id) adalah penyedia layanan rekayasa perangkat lunak dan ekosistem teknologi terpadu yang beroperasi melalui 3 pilar layanan utama:
1. Pilar 1: Software Development & POS Kasir (Aplikasi POS kasir ritel/F&B, CRM B2B, ERP custom, 100% hak milik source code tanpa biaya lisensi bulanan).
2. Pilar 2: Jasa Install Software Online Remote se-Indonesia (Instalasi software teknis arsitektur, CAD, 3D render, Adobe Creative Cloud via AnyDesk/UltraViewer, garansi 30 hari).
3. Pilar 3: Servis Komputer & Laptop On-Site Surabaya - Sidoarjo (Perawatan hardware, penggantian thermal paste, upgrade SSD NVMe, install ulang OS Windows/macOS/Linux panggilan ke kantor/rumah).

## 3 Core Service Pillars

### 1. Software Development & Custom POS
- URL: https://devk.my.id/jasa-pembuatan-software
- Target Audience: Pemilik bisnis ritel, toko bahan bangunan, kafe, distributor, dan perusahaan B2B.
- Key Capabilities:
  - POS Kasir Modern (offline-first sync, nota digital WhatsApp API, barcode scanning, multi-gudang).
  - CRM Penjualan B2B (Kanban visual pipeline, reminder follow-up otomatis, manajemen database klien).
  - Web & App Development (arsitektur Astro SSR ultra-cepat, Core Web Vitals 99+, PostgreSQL backend).
  - Lisensi: 100% hak milik klien, tanpa biaya langganan bulanan per outlet.

### 2. Jasa Install Software Online Remote
- URL: https://devk.my.id/jasa-install-software-online
- Coverage: Seluruh Indonesia (via UltraViewer / AnyDesk).
- Duration: 20-45 menit proses instalasi interaktif.
- Guarantee: Garansi aktif 30 hari purna jual.
- Supported Software Catalog:
  - CAD & Architecture: AutoCAD (2020-2026), SketchUp Pro, Autodesk Revit, Civil 3D, ArchiCAD, PLAXIS, SAP2000, ETABS.
  - 3D Rendering: V-Ray Next/6, Enscape 3D, Lumion Pro, Twinmotion, Blender, Maxon Cinema 4D, 3ds Max.
  - Creative & Editing: Adobe Creative Cloud (Photoshop, Illustrator, Premiere Pro, After Effects, InDesign), CorelDRAW Technical Suite, DaVinci Resolve Studio.
  - Engineering & Statistics: SPSS, SmartPLS, EViews, Minitab, MATLAB, ArcGIS Pro.

### 3. Servis Komputer Surabaya & Sidoarjo
- URL: https://devk.my.id/jasa-install-komputer-surabaya-sidoarjo
- Service Model: Teknisi on-site panggilan ke kantor/rumah & antar-jemput unit.
- Coverage: Seluruh kecamatan Surabaya (Pusat, Timur, Barat, Selatan, Utara) dan Sidoarjo (Kota, Waru, Gedangan, Sedati, Sukodono, Krian, Candi, dll).
- Services:
  - Install ulang OS (Windows 10/11, macOS, Linux) dengan driver lengkap dan backup data aman.
  - Pembersihan debu heatsink pendingin dan penggantian pasta thermal (Arctic MX-4).
  - Upgrade SSD M.2 NVMe PCIe dan penambahan RAM DDR4/DDR5 (performa naik hingga 10x lipat).

## Machine-Readable Endpoints
- Structured Pricing for AI Agents: https://devk.my.id/pricing.md
- Full Knowledge Export: https://devk.my.id/llms-full.txt
- Sitemap Index: https://devk.my.id/sitemap.xml
- Technical & Marketing Articles: https://devk.my.id/posts
`;

export const GET: APIRoute = async () => {
	return new Response(LLMS_TEXT, {
		status: 200,
		headers: {
			"Content-Type": "text/plain; charset=utf-8",
			"Cache-Control": "public, max-age=86400",
		},
	});
};
