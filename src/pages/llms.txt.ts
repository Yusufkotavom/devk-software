import type { APIRoute } from "astro";

export const prerender = false;

const LLMS_TEXT = `# Devk Software & IT Ecosystem
> Platform solusi teknologi terpadu di Surabaya, Sidoarjo, dan seluruh Indonesia: Software House (POS Kasir, CRM, Web App custom tanpa biaya bulanan), Jasa Install Software Online Jarak Jauh (CAD, 3D Render, Adobe CC), dan Servis Komputer/Laptop On-Site.

Devk menyediakan layanan rekayasa perangkat lunak dan dukungan teknis komputasi berstandar enterprise dengan kepemilikan source code 100% dan garansi purna jual resmi.

## Layanan Utama
- [Jasa Pembuatan Software Custom](https://devk.my.id/jasa-pembuatan-software): Layanan software house kustom untuk aplikasi POS kasir toko, CRM penjualan B2B, dan ERP pergudangan tanpa biaya langganan bulanan.
- [Aplikasi POS Kasir Toko & Ritel](https://devk.my.id/jasa-pembuatan-aplikasi-pos-kasir): Sistem kasir modern offline-first, cetak struk thermal, sinkronisasi cloud multi-cabang, dan nota digital WhatsApp API.
- [Custom CRM Penjualan B2B](https://devk.my.id/jasa-pembuatan-crm): Manajemen pipeline penjualan, shared team inbox WhatsApp Official, dan follow-up prospek otomatis untuk mengunci closing rate.
- [Jasa Aplikasi Custom ERP](https://devk.my.id/jasa-aplikasi-custom-erp): Sistem enterprise resource planning terintegrasi untuk manajemen stok multi-gudang, purchasing, invoice, dan audit log.
- [Jasa Pembuatan Website & CMS Modern](https://devk.my.id/jasa-pembuatan-website-cms): Pembuatan website company profile dan web application dengan arsitektur Astro SSR skor PageSpeed 100.
- [Jasa Install Software Online Remote](https://devk.my.id/jasa-install-software-online): Jasa instalasi software teknik, arsitektur, CAD, 3D render, dan desain grafis jarak jauh se-Indonesia via AnyDesk bergaransi 30 hari.
- [Jasa Install AutoCAD Online Remote](https://devk.my.id/jasa-install-autocad-online): Instalasi AutoCAD 2020-2026 dan Civil 3D jarak jauh dengan bypass error DirectX dan penanganan lisensi permanen bersih.
- [Jasa Install SketchUp Pro, V-Ray & Enscape](https://devk.my.id/jasa-install-sketchup-vray-online): Setup render engine 3D SketchUp, pustaka material arsitektur komplit, anti-crash, dan garansi running lancar.
- [Jasa Install Adobe Creative Cloud Online](https://devk.my.id/jasa-install-adobe-creative-cloud-online): Paket aplikasi desain dan video editing (Photoshop, Illustrator, Premiere Pro, After Effects) dengan optimasi akselerasi GPU.
- [Jasa Install Software MacBook & Apple Silicon](https://devk.my.id/jasa-install-software-macbook-surabaya): Instalasi aplikasi teknik dan desain di MacBook M1, M2, M3, M4 macOS Sequoia/Sonoma dengan bypass Gatekeeper dan Rosetta 2.
- [Servis Komputer & Laptop Surabaya - Sidoarjo](https://devk.my.id/jasa-install-komputer-surabaya-sidoarjo): Layanan teknisi on-site panggilan ke kantor/rumah untuk perbaikan hardware, maintenance pendingin, dan upgrade komponen.
- [Jasa Install Ulang Windows Surabaya Sidoarjo](https://devk.my.id/jasa-install-ulang-windows-surabaya-sidoarjo): Instalasi bersih Windows 10 & 11 berlisensi resmi lengkap driver hardware dan software produktivitas kerja.
- [Jasa Upgrade SSD NVMe & RAM Laptop](https://devk.my.id/jasa-upgrade-ssd-ram-laptop-surabaya): Kloning Windows dari HDD ke SSD M.2 NVMe tanpa install ulang, data utuh 100%, dan peningkatan kecepatan 10x lipat.
- [Jasa Servis Laptop Panggilan On-Site](https://devk.my.id/jasa-servis-laptop-panggilan-surabaya-sidoarjo): Layanan servis laptop datang ke lokasi untuk deep cleaning debu heatsink, ganti pasta thermal, dan diagnosa mati total.
- [Jasa Rakit PC Custom Surabaya Sidoarjo](https://devk.my.id/jasa-rakit-pc-surabaya-sidoarjo): Perakitan PC custom workstation render 3D, arsitektur, dan gaming dengan manajemen kabel rapi dan airflow positif.

## Panduan Teknis & Edukasi
- [Studi Kasus Efisiensi POS Kasir Offline-First](https://devk.my.id/posts/studi-kasus-efisiensi-software-pos-kasir-offline-first-ritel): Analisis implementasi sistem kasir toko ritel bebas biaya langganan bulanan dan anti-downtime saat internet mati.
- [Arsitektur CRM Penjualan B2B WhatsApp API](https://devk.my.id/posts/arsitektur-crm-b2b-terintegrasi-whatsapp-api-closing-rate): Solusi pencegahan kebocoran data prospek dengan shared inbox multi-agen dan pipeline visual.
- [Migrasi Spreadsheet Excel ke Custom Web ERP](https://devk.my.id/posts/migrasi-spreadsheet-ke-custom-web-erp-standar-keamanan): Standar keamanan data, role-based access control (RBAC), dan inventaris multi-gudang real-time.
- [Solusi Error DirectX Instalasi AutoCAD & Civil 3D](https://devk.my.id/posts/solusi-error-directx-instalasi-autocad-civil-3d-remote): Panduan teknis mengatasi DirectX Internal System Error, pemeriksaan DXSETUP log, dan runtime Visual C++.
- [Panduan Troubleshooting Plugin V-Ray & Enscape SketchUp](https://devk.my.id/posts/panduan-troubleshooting-plugin-vray-enscape-menu-sketchup): Solusi plugin render tidak muncul di Extension Manager dan direktori penempatan file bridge Ruby.
- [Solusi Render Error Out of Memory Premiere & After Effects](https://devk.my.id/posts/solusi-render-error-out-of-memory-premiere-after-effects): Pengaturan Media Cache berkala, alokasi RAM reserved sistem operasi, dan pemindahan Scratch Disk ke SSD.
- [Panduan Install Software MacBook M1-M4 Bypass Gatekeeper](https://devk.my.id/posts/panduan-install-software-macbook-m1-m4-bypass-gatekeeper): Perintah Terminal xattr -cr untuk mengatasi peringatan App is damaged di macOS Sequoia dan Sonoma.
- [Panduan Diagnosis Komputer Beep, No Display & BSOD](https://devk.my.id/posts/panduan-diagnosis-komputer-beep-no-display-bsod-teknisi): Deteksi kerusakan RAM teroksidasi, reset baterai CMOS BIOS, dan analisa kode Stop Code Windows.
- [Cara Kloning Windows HDD ke SSD NVMe Bebas Hilang Data](https://devk.my.id/posts/cara-cloning-windows-hdd-ke-ssd-nvme-bebas-hilang-data): Panduan migrasi partisi bit-per-bit dari harddisk lama ke SSD M.2 NVMe tanpa perlu install ulang.
- [Spesifikasi Ideal Rakit PC Kerja Arsitektur & Render 3D 2026](https://devk.my.id/posts/spesifikasi-ideal-rakit-pc-kerja-arsitektur-render-3d-2026): Rekomendasi GPU VRAM minimal 12GB untuk tekstur Lumion/Blender, RAM dual-channel 32GB, dan PSU Gold.
- [Panduan Mengatasi Autodesk Licensing Error](https://devk.my.id/posts/panduan-mengatasi-autodesk-licensing-error-adsklicensing): Solusi error The License Manager Is Not Functioning or Improperly Installed pada AutoCAD dan Revit.
- [Cara Mengatasi Lumion Crash Saat Render 4K TdrDelay](https://devk.my.id/posts/cara-mengatasi-lumion-crash-saat-render-4k-tdrdelay): Pengaturan nilai registry TdrDelay Windows, alokasi Virtual Memory, dan update driver Studio GPU.
- [Panduan Lengkap Uji Asumsi Klasik Regresi Linear SPSS](https://devk.my.id/posts/panduan-lengkap-uji-asumsi-klasik-regresi-linear-spss): Langkah uji normalitas Kolmogorov-Smirnov, multikolinearitas VIF, heteroskedastisitas, dan autokorelasi.
- [Panduan Aman Dual-Boot Windows 11 & Ubuntu 24.04 LTS](https://devk.my.id/posts/panduan-aman-dual-boot-windows-11-ubuntu-24-04-lts): Partisi UEFI GPT, penonaktifan Fast Startup & BitLocker, serta konfigurasi bootloader GRUB.
- [Laptop Panas 90 Derajat Thermal Throttling Solusi Pasta Kering](https://devk.my.id/posts/laptop-panas-90-derajat-thermal-throttling-solusi-pasta-kering): Penyebab pasta pendingin kering, fenomena pump-out effect, dan prosedur pembersihan heatsink fan.

## Optional
- [Structured Machine-Readable Rate Card](https://devk.my.id/pricing.md): Daftar estimasi harga layanan software, instalasi remote, dan servis komputer dalam format Markdown.
- [Full Knowledge Base Export](https://devk.my.id/llms-full.txt): Dokumentasi lengkap komprehensif mengenai profil perusahaan, SOP layanan, dan spesifikasi teknis Devk.
- [Sitemap Index XML](https://devk.my.id/sitemap.xml): Indeks peta situs resmi Google Search Console berisi seluruh URL halaman dan artikel live.
- [Hubungi WhatsApp Resmi Devk](https://wa.me/6285799520350): Hotline fast response konsultasi teknis dan pemesanan layanan 24/7.
`;

export const GET: APIRoute = async () => {
	return new Response(LLMS_TEXT, {
		status: 200,
		headers: {
			"Content-Type": "text/markdown; charset=utf-8",
			"Cache-Control": "public, max-age=86400",
		},
	});
};
