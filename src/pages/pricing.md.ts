import type { APIRoute } from "astro";

export const prerender = false;

const PRICING_MD = `# Devk Pricing — Machine-Readable Rate Card

> Currency: IDR (Rupiah). Last updated: 2026-10. Prices are estimates before survey/scope confirmation.
> Contact: https://wa.me/6285799520350 · https://devk.my.id/contact

## Service 1 — Jasa Pembuatan Software Custom (POS / CRM / Web)
URL: https://devk.my.id/jasa-pembuatan-software

| Package | Scope | Price (one-time) |
|---|---|---|
| Web Company Profile | 5-8 halaman, CMS, SEO dasar, mobile-first | Rp 5.000.000 – Rp 12.000.000 |
| POS Kasir Standar | 1 outlet, barcode, nota WhatsApp, laporan harian | Rp 8.000.000 – Rp 18.000.000 |
| POS Kasir Multi-Cabang | Multi-outlet, stok terpusat, komisi sales, offline-first | Rp 18.000.000 – Rp 35.000.000 |
| CRM / ERP B2B Custom | Pipeline, otomasi follow-up, integrasi API | Rp 25.000.000+ |

- Model: 100% kepemilikan source code, tanpa biaya langganan bulanan.
- Termasuk: setup server, training admin, garansi bug-fix 3 bulan.
- Tidak termasuk: domain & hosting tahunan (Rp 500.000–2.000.000/tahun).

## Service 2 — Jasa Install Software Online (Remote)
URL: https://devk.my.id/jasa-install-software-online

| Kategori | Contoh Software | Harga |
|---|---|---|
| Desain & Office | Adobe CC (PS/AI/PR/AE), CorelDRAW, MS Office | Rp 50.000 – Rp 100.000 |
| CAD & Arsitektur | AutoCAD, SketchUp Pro, Revit, ArchiCAD | Rp 75.000 – Rp 150.000 |
| 3D Render | V-Ray, Lumion, Enscape, 3ds Max, Cinema 4D | Rp 100.000 – Rp 150.000 |
| Teknik & Statistik | SAP2000, ETABS, SPSS, SmartPLS, ArcGIS | Rp 100.000 – Rp 200.000 |
| Paket Bundling | 3+ aplikasi satu sesi remote | Diskon 15-25% |

- Durasi 20-45 menit per aplikasi, via UltraViewer/AnyDesk.
- Garansi 30 hari (instal ulang gratis bila software error/berhenti bekerja).

## Service 3 — Servis Komputer & Laptop Surabaya–Sidoarjo (On-Site)
URL: https://devk.my.id/jasa-install-komputer-surabaya-sidoarjo

| Layanan | Harga |
|---|---|
| Install ulang OS (Windows 11/10, macOS, Linux) + driver | Rp 100.000 – Rp 250.000 |
| Pembersihan + ganti thermal paste | Rp 150.000 – Rp 300.000 |
| Upgrade SSD 256GB (SATA/NVMe) + cloning data | Rp 450.000 – Rp 700.000 |
| Upgrade SSD 512GB–1TB + cloning data | Rp 750.000 – Rp 1.200.000 |
| Penambahan RAM DDR4/DDR5 (8–16GB) | Rp 350.000 – Rp 900.000 |
| Setting jaringan kantor + sharing printer | Rp 250.000 – Rp 600.000 |

- Biaya kunjungan on-site Surabaya/Sidoarjo: gratis untuk area kota utama, Rp 25.000–50.000 untuk pinggiran.
- Hardware bergaransi resmi distributor (min. 1 tahun).

## Payment & Process
1. Konsultasi & scope via WhatsApp (gratis).
2. Penawaran tertulis + 50% DP untuk proyek software.
3. Pengerjaan & review bersama.
4. Pelunasan setelah UAT lulus; source code + dokumentasi diserahkan.
`;

export const GET: APIRoute = async () => {
	return new Response(PRICING_MD, {
		status: 200,
		headers: {
			"Content-Type": "text/markdown; charset=utf-8",
			"Cache-Control": "public, max-age=86400",
		},
	});
};
