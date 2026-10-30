import json
import os
import urllib.request
import time

PAT_TOKEN = os.environ.get("EMDASH_PAT", "")
API_URL = "https://software.devk.my.id/_emdash/api/mcp"

def call_mcp(tool_name, arguments):
    req = urllib.request.Request(
        API_URL,
        headers={
            "Authorization": f"Bearer {PAT_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
        data=json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments}
        }).encode("utf-8")
    )
    with urllib.request.urlopen(req) as resp:
        res_str = resp.read().decode("utf-8")
        for line in res_str.split("\n"):
            if line.startswith("data: "):
                data = json.loads(line[6:])
                content = data.get("result", {}).get("content", [])
                if content and "text" in content[0]:
                    try:
                        return json.loads(content[0]["text"])
                    except Exception:
                        return content[0]["text"]
                return data.get("result", {})
        return {}

def build_pilar1_pages():
    # Material Design CTA Media IDs
    pos_media_id = "01M5KVFFP9ZP0CZ3VJTCGFK484" # devk-material-cta-pos-business.jpg
    crm_media_id = "01M5KVFCRDV9XRGJGFC3TSEBE8" # devk-material-cta-software-hub.jpg
    web_media_id = "01M5KVFR3K84T6Q3219AH5SHBR" # devk-material-cta-universal-hotline.jpg
    erp_media_id = "01M5KVFQN88NR8FTZ62MX60AG6" # devk-material-cta-maintenance-contract.jpg

    pages = [
        # =========================================================================
        # PAGE 1: Jasa Pembuatan Aplikasi POS Kasir
        # =========================================================================
        {
            "collection": "pages",
            "slug": "jasa-pembuatan-aplikasi-pos-kasir",
            "status": "published",
            "data": {
                "title": "Jasa Pembuatan Aplikasi POS Kasir Toko & Ritel | Devk",
                "content": [
                    {
                        "_key": "hero-pos",
                        "_type": "marketing_hero",
                        "_version": 1,
                        "centered": False,
                        "eyebrow": "Software House & Sistem Kasir Kustom",
                        "headline": "Jasa Pembuatan Aplikasi POS Kasir — Tanpa Biaya Langganan Bulanan",
                        "subheadline": "Solusi kasir modern untuk toko ritel, minimarket, cafe, resto, dan grosir. Sinkronisasi multi-cabang realtime, cetak struk thermal, laporan laba rugi otomatis, dan 100% kepemilikan source code.",
                        "primary_cta_label": "Konsultasi & Demo via WA",
                        "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20tertarik%20pembuatan%20aplikasi%20POS%20kasir%20untuk%20usaha%20saya",
                        "secondary_cta_label": "Pilihan Paket Biaya POS",
                        "secondary_cta_url": "#harga",
                        "image": {"id": pos_media_id},
                        "image_caption": "Sistem Kasir Modern & Realtime Cloud"
                    },
                    {
                        "_key": "bento-pos",
                        "_type": "marketing_bento_grid",
                        "_version": 1,
                        "eyebrow": "Arsitektur Kustom",
                        "headline": "Fitur Lengkap Dirancang Sesuai SOP Usaha Anda",
                        "subheadline": "Tinggalkan software kasir sewa yang kaku dan lambat. Miliki sistem yang fleksibel dan berkembang bersama bisnis Anda.",
                        "items": [
                            {
                                "title": "Bebas Biaya Royalti & Langganan Bulanan",
                                "description": "Cukup bayar sekali di awal. Tidak ada biaya bulanan per kasir atau komisi transaksi.",
                                "tag": "COST EFFICIENCY",
                                "badge": "One-Time Payment",
                                "col_span": "2",
                                "row_span": "1",
                                "icon": "zap",
                                "link_url": "#harga",
                                "link_label": "Lihat Paket"
                            },
                            {
                                "title": "Dukungan Mode Offline",
                                "description": "Transaksi kasir tetap lancar meski internet mati, data otomatis sync saat online.",
                                "tag": "RELIABILITY",
                                "col_span": "1",
                                "row_span": "1",
                                "icon": "shield"
                            },
                            {
                                "title": "Multi-Cabang & Manajemen Inventori Terpusat",
                                "description": "Pantau stok antar gudang dan omzet puluhan cabang toko langsung dari dashboard HP pemilik secara realtime.",
                                "tag": "ENTERPRISE SCALE",
                                "col_span": "3",
                                "row_span": "1",
                                "icon": "database",
                                "code_snippet": "SELECT outlet_name, SUM(total_sales) AS daily_revenue, COUNT(*) AS transactions\nFROM pos_orders WHERE transaction_date = CURRENT_DATE GROUP BY outlet_name;"
                            }
                        ]
                    },
                    {
                        "_key": "tabs-pos",
                        "_type": "marketing_tabs",
                        "_version": 1,
                        "eyebrow": "Fleksibilitas Modul",
                        "headline": "Modul Aplikasi Kasir yang Kami Bangun",
                        "subheadline": "Setiap modul disesuaikan dengan jenis industri bisnis Anda.",
                        "tabs": [
                            {
                                "label": "Modul Front-Office (Kasir)",
                                "title": "Antarmuka Kasir Cepat & Mudah Dipelajari",
                                "description": "Scan barcode presisi, pencarian nama barang instan, dukungan pembayaran cash, QRIS, transfer bank, dan cetak struk thermal 58mm/80mm.",
                                "cta_label": "Konsultasi Fitur Kasir",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20tanya%20fitur%20kasir"
                            },
                            {
                                "label": "Modul Gudang & Inventori",
                                "title": "Kontrol Stok Otomatis & Notifikasi Habis",
                                "description": "Pengurangan stok otomatis saat transaksi, kartu stok digital, mutasi antar cabang, opname stok dengan scanner barcode, dan peringatan batas minimum.",
                                "cta_label": "Konsultasi Modul Stok",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20tanya%20fitur%20gudang"
                            },
                            {
                                "label": "Modul Owner & Finansial",
                                "title": "Laporan Laba Rugi Bersih Realtime",
                                "description": "Rekap shift kasir, audit void/pembatalan, laporan omzet harian/bulanan, margin laba kotor vs HPP produk, dan export laporan ke format Excel.",
                                "cta_label": "Konsultasi Laporan Owner",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20tanya%20fitur%20laporan"
                            }
                        ]
                    },
                    {
                        "_key": "steps-pos",
                        "_type": "marketing_steps",
                        "_version": 1,
                        "eyebrow": "Metodologi Agile",
                        "headline": "4 Tahapan Pengembangan POS Tanpa Ganggu Operasional",
                        "subheadline": "Kami mendampingi proses implementasi hingga kasir dan staf Anda mahir mengoperasikannya.",
                        "steps": [
                            {"step_number": "01", "title": "Analisis Kebutuhan & Desain Alur", "description": "Tim Business Analyst kami mengkaji proses bisnis toko, jenis printer/scanner, dan struktur harga grosir/eceran Anda."},
                            {"step_number": "02", "title": "Development & Integrasi Hardware", "description": "Pengembangan aplikasi menggunakan teknologi modern (Node.js/Go/PostgreSQL) dan pengujian integrasi printer thermal & barcode scanner."},
                            {"step_number": "03", "title": "Migrasi Data Produk & Pelatihan", "description": "Import ribuan master data produk dari Excel, setup hak akses user, dan training langsung kepada kasir & admin."},
                            {"step_number": "04", "title": "Go-Live & SLA Maintenance", "description": "Peluncuran sistem operasional toko didampingi teknisi Devk serta garansi perbaikan bug dan support teknis."}
                        ]
                    },
                    {
                        "_key": "comp-pos",
                        "_type": "marketing_comparison_table",
                        "_version": 1,
                        "eyebrow": "Analisis Biaya & Investasi",
                        "headline": "Aplikasi Kasir Kustom Devk vs Software Sewa Berlangganan",
                        "subheadline": "Hemat puluhan juta rupiah dalam jangka panjang untuk investasi aset digital perusahaan Anda.",
                        "us_title": "Aplikasi Kustom Devk",
                        "competitor_title": "Software Kasir Sewa Cloud Lain",
                        "rows": [
                            {"feature_name": "Biaya Pemakaian Jangka Panjang", "feature_desc": "Beli putus tanpa biaya sewa bulanan", "us_value": "yes (Rp 0 selamanya)", "competitor_value": "no (wajib bayar Rp 300rb-1jt/bulan)"},
                            {"feature_name": "Kepemilikan Source Code & Database", "feature_desc": "Data pelanggan dan kode 100% milik Anda", "us_value": "yes", "competitor_value": "no (data tersandera di server vendor)"},
                            {"feature_name": "Kustomisasi Format Nota & Diskon Khusus", "feature_desc": "Bebas minta modifikasi fitur unik usaha Anda", "us_value": "yes", "competitor_value": "no (fitur template kaku)"},
                            {"feature_name": "Integrasi Hardware Bebas Merk", "feature_desc": "Kompatibel printer EPSON, Iware, Kassen, Sunmi", "us_value": "yes", "competitor_value": "no (sering dikunci ke hardware vendor)"}
                        ],
                        "cta_label": "Mulai Bangun POS Usaha Anda",
                        "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20buat%20aplikasi%20kasir"
                    },
                    {
                        "_key": "pricing-pos",
                        "_type": "marketing_pricing",
                        "_version": 1,
                        "anchor_id": "harga",
                        "headline": "Paket Investasi Pembuatan Aplikasi Kasir",
                        "plans": [
                            {
                                "name": "Paket Starter UMKM",
                                "price": "Rp 1.500.000",
                                "period": "sekali bayar",
                                "description": "Cocok untuk 1 toko/kafe yang ingin pencatatan digital rapi",
                                "features": "Aplikasi Kasir Desktop/Web Single Outlet\nModul Kasir & Cetak Struk Thermal\nLaporan Penjualan & Kas Harian\nGaransi Bug 3 Bulan & Free Training",
                                "cta_label": "Pilih Paket Starter",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Starter%20POS"
                            },
                            {
                                "name": "Paket Bisnis Pro",
                                "price": "Rp 3.500.000",
                                "period": "sekali bayar",
                                "description": "Pilihan terpopuler toko ritel, resto, & bisnis multi-kasir",
                                "features": "Multi-Kasir & Multi-Cabang Cloud Sync\nModul Stok Gudang & Supplier Purchasing\nDashboard Owner di Android/iOS Browser\nIntegrasi QRIS Dinamis & Diskon Member\nGaransi 6 Bulan & Source Code Diserahkan",
                                "cta_label": "Pesan Paket Populer",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Bisnis%20Pro%20POS",
                                "highlighted": True,
                                "badge": "Paling Laris"
                            },
                            {
                                "name": "Paket Enterprise Custom",
                                "price": "Rp 7.500.000",
                                "period": "sekali bayar",
                                "description": "Solusi rantai toko grosir, manufaktur, & franchise besar",
                                "features": "Custom Alur Bisnis 100% Sesuai SOP\nIntegrasi Mesin Timbangan & Barcode Industri\nIntegrasi API Akuntansi & ERP\nServer On-Premise / Private Cloud Setup\nGaransi 1 Tahun Penuh & SLA Priority",
                                "cta_label": "Konsultasi Enterprise",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Enterprise%20POS"
                            }
                        ]
                    },
                    {
                        "_key": "wa-box-pos",
                        "_type": "marketing_whatsapp_cta",
                        "_version": 1,
                        "headline": "Siap Tingkatkan Efisiensi dan Hentikan Kebocoran Kas Toko?",
                        "body": "Diskusikan kebutuhan sistem kasir Anda bersama Software Architect Devk. Kami sediakan live demo gratis dan estimasi rancangan anggaran.",
                        "label": "Jadwalkan Demo Kasir via WhatsApp",
                        "custom_message": "Halo Devk, saya ingin konsultasi pembuatan aplikasi POS kasir ({title}). Bisakah jadwalkan demo online?",
                        "variant": "card",
                        "anchor_id": "wa-cta"
                    },
                    {
                        "_key": "faq-pos",
                        "_type": "marketing_faq",
                        "_version": 1,
                        "headline": "Pertanyaan Seputar Pembuatan Aplikasi Kasir",
                        "subheadline": "Hal-hal yang sering ditanyakan pemilik bisnis sebelum memesan software POS.",
                        "items": [
                            {"question": "Apakah aplikasi kasir ini benar-benar tidak ada biaya bulanan?", "answer": "Benar. Sistem kami berbasis beli putus (one-time license). Anda tidak akan ditagih biaya sewa bulanan atau tahunan. Jika menggunakan cloud server, Anda hanya membayar biaya hosting server Anda sendiri yang sangat terjangkau."},
                            {"question": "Apakah bisa berjalan di komputer atau tablet yang sudah saya miliki?", "answer": "Bisa. Kami merancang arsitektur aplikasi kasir yang ringan dan cross-platform, dapat dijalankan di PC Windows, laptop, maupun tablet Android / iPad."},
                            {"question": "Apakah saya membutuhkan perangkat PC baru?", "answer": "Jika Anda membutuhkan perangkat komputer baru yang andal untuk kasir, kami juga menyediakan layanan [Jasa Rakit PC Surabaya](/jasa-rakit-pc-surabaya-sidoarjo) dan paket hardware siap pakai."},
                            {"question": "Bagaimana jika ada staf kasir yang berganti dan butuh pelatihan ulang?", "answer": "Kami menyediakan video panduan operasional lengkap serta dokumentasi SOP penggunaan sistem untuk memudahkan pelatihan karyawan baru Anda."},
                            {"question": "Apakah software ini bisa terhubung dengan sistem ERP atau CRM bisnis saya?", "answer": "Sangat bisa. Sistem kasir kami dilengkapi REST API terbuka sehingga dapat dihubungkan dengan modul [Jasa Pembuatan CRM](/jasa-pembuatan-crm) atau [Custom ERP](/jasa-aplikasi-custom-erp)."}
                        ]
                    },
                    {
                        "_key": "cta-pos",
                        "_type": "marketing_cta",
                        "_version": 1,
                        "headline": "Wujudkan Sistem Kasir Profesional & Otomatis untuk Bisnis Anda",
                        "body": "Solusi terpercaya dari Devk Software House. Cek juga induk [Hub Jasa Pembuatan Software](/jasa-pembuatan-software) untuk solusi B2B lainnya.",
                        "primary_cta_label": "Hubungi WhatsApp 085799520350",
                        "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20buat%20aplikasi%20kasir",
                        "secondary_cta_label": "Hub Software Development",
                        "secondary_cta_url": "/jasa-pembuatan-software",
                        "image": {"id": pos_media_id}
                    }
                ]
            },
            "seo": {
                "title": "Jasa Pembuatan Aplikasi POS Kasir Toko & Ritel | Devk",
                "description": "Jasa pembuatan aplikasi POS kasir toko, ritel, & F&B kustom. Multi-cabang, cetak struk bluetooth, sinkronisasi cloud realtime, tanpa biaya langganan bulanan. WA 085799520350.",
                "canonical": "https://devk.my.id/jasa-pembuatan-aplikasi-pos-kasir",
                "image": "https://software.devk.my.id/_emdash/api/media/file/devk-enterprise-pos-software.jpg",
                "noIndex": False
            }
        },

        # =========================================================================
        # PAGE 2: Jasa Pembuatan CRM
        # =========================================================================
        {
            "collection": "pages",
            "slug": "jasa-pembuatan-crm",
            "status": "published",
            "data": {
                "title": "Jasa Pembuatan Aplikasi CRM Bisnis Kustom | Devk",
                "content": [
                    {
                        "_key": "hero-crm",
                        "_type": "marketing_hero",
                        "_version": 1,
                        "centered": False,
                        "eyebrow": "Otomasi Penjualan & Database Pelanggan",
                        "headline": "Jasa Pembuatan Aplikasi CRM Bisnis Kustom — Tingkatkan Omzet & Retensi",
                        "subheadline": "Kelola ribuan prospek, otomatisasi follow-up WhatsApp, pantau kinerja tim sales secara transparan, dan bangun loyalitas pelanggan tanpa biaya lisensi per user yang mahal.",
                        "primary_cta_label": "Konsultasi CRM via WhatsApp",
                        "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20tertarik%20pembuatan%20aplikasi%20CRM%20untuk%20perusahaan%20saya",
                        "secondary_cta_label": "Pilihan Paket Biaya CRM",
                        "secondary_cta_url": "#harga",
                        "image": {"id": crm_media_id},
                        "image_caption": "Visual Pipeline CRM & Lead Management"
                    },
                    {
                        "_key": "bento-crm",
                        "_type": "marketing_bento_grid",
                        "_version": 1,
                        "eyebrow": "Solusi Omnichannel",
                        "headline": "Fitur Strategis untuk Melesatkan Produktivitas Sales",
                        "subheadline": "Semua interaksi pelanggan dari chat, telepon, hingga deal penawaran tercatat rapi dalam satu dashboard.",
                        "items": [
                            {
                                "title": "Integrasi WhatsApp Gateway & Auto-Responder",
                                "description": "Kirim pesan follow-up otomatis, blast informasi promo resmi, dan simpan riwayat chat calon pembeli.",
                                "tag": "AUTOMATION",
                                "badge": "High Conversion",
                                "col_span": "2",
                                "row_span": "1",
                                "icon": "zap",
                                "link_url": "#harga",
                                "link_label": "Lihat Fitur"
                            },
                            {
                                "title": "Bebas Biaya Per-User / Seat",
                                "description": "Gunakan untuk 10, 50, atau 100 sales tanpa biaya langganan membengkak setiap bulan.",
                                "tag": "UNLIMITED USERS",
                                "col_span": "1",
                                "row_span": "1",
                                "icon": "users"
                            },
                            {
                                "title": "Pipeline Prospek Visual (Kanban Deals)",
                                "description": "Geser prospek dari tahap Baru Masuk, Follow-Up, Kirim Proposal, hingga Closing Deal dengan drag & drop intuitif.",
                                "tag": "SALES FUNNEL",
                                "col_span": "3",
                                "row_span": "1",
                                "icon": "chart",
                                "code_snippet": "pipeline.moveDeal(dealId, 'CLOSED_WON');\nnotificationService.sendWhatsApp(customerPhone, 'Terima kasih atas pesanan Anda!');"
                            }
                        ]
                    },
                    {
                        "_key": "steps-crm",
                        "_type": "marketing_steps",
                        "_version": 1,
                        "eyebrow": "Implementasi Terstruktur",
                        "headline": "4 Tahapan Implementasi CRM Devk",
                        "subheadline": "Memastikan sistem CRM diadopsi dengan mudah dan efektif oleh tim operasional Anda.",
                        "steps": [
                            {"step_number": "01", "title": "Pemetaan Alur Prospek Bisnis", "description": "Menganalisis darimana calon klien Anda datang (iklan, website, referral) dan tahapan negosiasi tim sales."},
                            {"step_number": "02", "title": "Development & Integrasi Channel", "description": "Membangun antarmuka CRM kustom, integrasi WhatsApp API, integrasi email, dan form website prospek."},
                            {"step_number": "03", "title": "Migrasi Database & Pengujian", "description": "Pembersihan dan import database kontak lama dari spreadsheet atau buku catatan ke sistem CRM terenkripsi."},
                            {"step_number": "04", "title": "Pelatihan Tim Sales & SLA Maintenance", "description": "Simulasi pengerjaan lead bersama tim penjualan, serah terima source code, dan pendampingan pasca go-live."}
                        ]
                    },
                    {
                        "_key": "comp-crm",
                        "_type": "marketing_comparison_table",
                        "_version": 1,
                        "eyebrow": "Efisiensi Investasi",
                        "headline": "Custom CRM Devk vs Aplikasi CRM Langganan Luar Negeri",
                        "subheadline": "Perbandingan fleksibilitas dan biaya pemakaian jangka panjang.",
                        "us_title": "Custom CRM Devk",
                        "competitor_title": "CRM Sewa (Salesforce / HubSpot)",
                        "rows": [
                            {"feature_name": "Biaya Lisensi per Karyawan", "feature_desc": "Bebas tambah user tanpa tagihan bulanan", "us_value": "yes (Rp 0 flat unlimited)", "competitor_value": "no ($50 - $150 per user per bulan)"},
                            {"feature_name": "Integrasi WhatsApp Lokal Indonesia", "feature_desc": "Dukungan gateway WA lokal & template fleksibel", "us_value": "yes", "competitor_value": "no (fokus ke email, WA ribet & mahal)"},
                            {"feature_name": "Kerahasiaan Database Prospek", "feature_desc": "Data disimpan di private server milik Anda", "us_value": "yes (aman 100%)", "competitor_value": "no (tersimpan di cloud publik vendor)"},
                            {"feature_name": "Bahasa & Alur Kerja Lokal", "feature_desc": "Disesuaikan dengan kebiasaan tim di Indonesia", "us_value": "yes", "competitor_value": "no (kaku & berbelit-belit)"}
                        ],
                        "cta_label": "Miliki CRM Kustom Bisnis Anda",
                        "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20buat%20aplikasi%20CRM"
                    },
                    {
                        "_key": "pricing-crm",
                        "_type": "marketing_pricing",
                        "_version": 1,
                        "anchor_id": "harga",
                        "headline": "Paket Biaya Pembuatan Aplikasi CRM",
                        "plans": [
                            {
                                "name": "Paket Sales CRM Basic",
                                "price": "Rp 2.500.000",
                                "period": "sekali bayar",
                                "description": "Untuk tim sales 1-5 orang yang butuh sentralisasi kontak prospek",
                                "features": "Manajemen Database Prospek & Pelanggan\nPipeline Penjualan Visual Kanban\nCatatan Riwayat Interaksi & Follow-Up\nGaransi 3 Bulan & Free Training",
                                "cta_label": "Pilih CRM Basic",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20CRM%20Basic"
                            },
                            {
                                "name": "Paket Omnichannel Pro",
                                "price": "Rp 5.000.000",
                                "period": "sekali bayar",
                                "description": "Paling populer untuk bisnis layanan, properti, & distributor B2B",
                                "features": "Integrasi WhatsApp Gateway & Auto Follow-Up\nMulti-User Role (Sales, Leader, Manajer, Direktur)\nLaporan Rasio Konversi & Performa Tim\nExport/Import Excel & Notifikasi Reminder\nGaransi 6 Bulan & Source Code Milik Anda",
                                "cta_label": "Pesan Paket Populer",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Omnichannel%20CRM",
                                "highlighted": True,
                                "badge": "Paling Laris"
                            },
                            {
                                "name": "Paket Enterprise CRM & Automation",
                                "price": "Rp 10.000.000",
                                "period": "sekali bayar",
                                "description": "Solusi korporasi dengan ratusan sales & cabang nasional",
                                "features": "Custom Pipeline & Algoritma Distribusi Lead\nIntegrasi [Aplikasi POS Kasir](/jasa-pembuatan-aplikasi-pos-kasir) & [Custom ERP](/jasa-aplikasi-custom-erp)\nAPI Terbuka & Dedicated VPS Private Cloud\nSLA Support 1 Tahun Penuh & Prioritas 24/7",
                                "cta_label": "Pilih Paket Enterprise",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Enterprise%20CRM"
                            }
                        ]
                    },
                    {
                        "_key": "wa-box-crm",
                        "_type": "marketing_whatsapp_cta",
                        "_version": 1,
                        "headline": "Siap Menghentikan Kehilangan Prospek Berharga Bisnis Anda?",
                        "body": "Hubungi tim konsultan software Devk untuk presentasi sistem CRM dan demo alur kerja follow-up interaktif.",
                        "label": "Jadwalkan Live Demo CRM via WA",
                        "custom_message": "Halo Devk, saya ingin tanya pembuatan aplikasi CRM ({title}). Bisakah diskusi alur tim sales saya?",
                        "variant": "card",
                        "anchor_id": "wa-cta"
                    },
                    {
                        "_key": "faq-crm",
                        "_type": "marketing_faq",
                        "_version": 1,
                        "headline": "Pertanyaan Seputar Aplikasi CRM",
                        "subheadline": "Jawaban lengkap seputar fitur otomasi, keamanan database, dan integrasi WhatsApp.",
                        "items": [
                            {"question": "Apakah CRM ini bisa dihubungkan ke akun WhatsApp resmi bisnis saya?", "answer": "Bisa. Kami dapat mengintegrasikannya dengan WhatsApp Business Cloud API resmi Meta maupun gateway WhatsApp pihak ketiga sesuai preferensi anggaran Anda."},
                            {"question": "Apakah data prospek dan kontak pelanggan saya aman dari kebocoran?", "answer": "Sangat aman. Seluruh database diinstal di server private milik perusahaan Anda dengan enkripsi database dan kontrol hak akses bertingkat (hanya owner/manajer yang bisa mengekspor data)."},
                            {"question": "Apakah CRM ini bisa diakses dari HP oleh tim sales di lapangan?", "answer": "Ya, kami merancang antarmuka mobile-responsive yang nyaman digunakan dari smartphone Android dan iPhone tanpa perlu download aplikasi berat."},
                            {"question": "Apakah CRM bisa diintegrasikan dengan website marketing saya?", "answer": "Tentu. Prospek yang mengisi formulir di [Jasa Pembuatan Website](/jasa-pembuatan-website-cms) Anda akan langsung masuk ke pipeline CRM dan memicu notifikasi instan ke WhatsApp sales."}
                        ]
                    },
                    {
                        "_key": "cta-crm",
                        "_type": "marketing_cta",
                        "_version": 1,
                        "headline": "Bangun Sistem Penjualan yang Bekerja Otomatis untuk Anda",
                        "body": "Kendalikan penjualan dengan data nyata. Jelajahi juga solusi [Jasa Pembuatan Aplikasi POS Kasir](/jasa-pembuatan-aplikasi-pos-kasir) dan [Custom ERP](/jasa-aplikasi-custom-erp).",
                        "primary_cta_label": "Hubungi WhatsApp 085799520350",
                        "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20buat%20aplikasi%20CRM",
                        "secondary_cta_label": "Hub Software Development",
                        "secondary_cta_url": "/jasa-pembuatan-software",
                        "image": {"id": crm_media_id}
                    }
                ]
            },
            "seo": {
                "title": "Jasa Pembuatan Aplikasi CRM Bisnis Kustom | Devk",
                "description": "Jasa pembuatan aplikasi CRM & otomasi penjualan kustom. Pipeline prospek, integrasi WhatsApp API, tracking performa sales, & manajemen database pelanggan. WA 085799520350.",
                "canonical": "https://devk.my.id/jasa-pembuatan-crm",
                "image": "https://software.devk.my.id/_emdash/api/media/file/devk-software-ecosystem.jpg",
                "noIndex": False
            }
        },

        # =========================================================================
        # PAGE 3: Jasa Pembuatan Website Company Profile & CMS
        # =========================================================================
        {
            "collection": "pages",
            "slug": "jasa-pembuatan-website-cms",
            "status": "published",
            "data": {
                "title": "Jasa Pembuatan Website Company Profile & CMS | Devk",
                "content": [
                    {
                        "_key": "hero-web",
                        "_type": "marketing_hero",
                        "_version": 1,
                        "centered": False,
                        "eyebrow": "Web Development & CMS Modern",
                        "headline": "Jasa Pembuatan Website Company Profile & CMS — Skor PageSpeed 100",
                        "subheadline": "Tingkatkan kredibilitas korporat dengan website super kencang, desain eksklusif mobile-first, optimasi SEO menyeluruh, serta CMS mandiri yang mudah diupdate sendiri tanpa koding.",
                        "primary_cta_label": "Konsultasi Website via WA",
                        "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20tertarik%20pembuatan%20website%20company%20profile%20untuk%20perusahaan%20saya",
                        "secondary_cta_label": "Pilihan Paket Website",
                        "secondary_cta_url": "#harga",
                        "image": {"id": web_media_id},
                        "image_caption": "Modern High-Performance Web Architecture"
                    },
                    {
                        "_key": "bento-web",
                        "_type": "marketing_bento_grid",
                        "_version": 1,
                        "eyebrow": "Keunggulan Teknologi",
                        "headline": "Standar Teknologi Web Modern Tanpa Kompromi",
                        "subheadline": "Kami tidak menggunakan template WordPress murahan yang lemot dan rentan malware. Kami membangun website dengan arsitektur modern.",
                        "items": [
                            {
                                "title": "Google PageSpeed Skor 100",
                                "description": "Loading instan di bawah 1 detik, meningkatkan peringkat Google dan rasio konversi pengunjung.",
                                "tag": "PERFORMANCE",
                                "badge": "Core Web Vitals",
                                "col_span": "2",
                                "row_span": "1",
                                "icon": "zap",
                                "link_url": "#harga",
                                "link_label": "Lihat Hasil"
                            },
                            {
                                "title": "CMS Mandiri & Intuitif",
                                "description": "Ubah teks, tambah artikel blog, atau ganti foto semudah mengetik di Word tanpa butuh programmer.",
                                "tag": "EASY TO USE",
                                "col_span": "1",
                                "row_span": "1",
                                "icon": "code"
                            },
                            {
                                "title": "Keamanan Kelas Enterprise & Perlindungan Cloudflare",
                                "description": "Bebas celah keamanan plugin, gratis sertifikat SSL HTTPS permanen, dan proteksi anti-DDoS.",
                                "tag": "SECURITY",
                                "col_span": "3",
                                "row_span": "1",
                                "icon": "shield",
                                "code_snippet": "curl -I https://devk.my.id\nHTTP/2 200 OK\nstrict-transport-security: max-age=31536000\ncf-cache-status: HIT"
                            }
                        ]
                    },
                    {
                        "_key": "steps-web",
                        "_type": "marketing_steps",
                        "_version": 1,
                        "eyebrow": "Proses Rapi & Terjadwal",
                        "headline": "4 Tahapan Pembuatan Website Devk",
                        "subheadline": "Transparan dari penyusunan konsep hingga website live dan siap diakses publik.",
                        "steps": [
                            {"step_number": "01", "title": "Brief & Perancangan Wireframe", "description": "Menentukan struktur menu, target audiens, dan referensi desain visual yang sesuai citra brand Anda."},
                            {"step_number": "02", "title": "Coding Frontend & Integrasi CMS", "description": "Pembangunan website berbasis framework modern (Astro/Next.js/Tailwind) yang responsif di seluruh gadget."},
                            {"step_number": "03", "title": "Audit SEO On-Page & PageSpeed", "description": "Pemasangan metadata OpenGraph, Rich Schema JSON-LD, sitemap XML, dan optimasi gambar berformat WebP."},
                            {"step_number": "04", "title": "Setup Domain, Hosting & Serah Terima", "description": "Konfigurasi domain resmi (.com/.id/.co.id), email korporat (nama@perusahaan.com), dan video tutorial panduan admin."}
                        ]
                    },
                    {
                        "_key": "comp-web",
                        "_type": "marketing_comparison_table",
                        "_version": 1,
                        "eyebrow": "Kualitas Pengerjaan",
                        "headline": "Website Standar Devk vs Jasa Website Template Murahan",
                        "subheadline": "Investasi website yang benar-benar menghasilkan reputasi dan lead bisnis nyata.",
                        "us_title": "Website Modern Devk",
                        "competitor_title": "Jasa Website Template Biasa",
                        "rows": [
                            {"feature_name": "Kecepatan Loading Halaman", "feature_desc": "Skor Google PageSpeed 95-100", "us_value": "yes (< 1 detik instan)", "competitor_value": "no (5-8 detik lemot)"},
                            {"feature_name": "Keamanan Kode & Bebas Malware", "feature_desc": "Arsitektur static / SSR modern bebas hack", "us_value": "yes (kebal serangan plugin)", "competitor_value": "no (rentan redirect judi online)"},
                            {"feature_name": "Optimasi SEO & Rich Snippets", "feature_desc": "Schema markup lengkap untuk Google Rich Results", "us_value": "yes", "competitor_value": "no (hanya pasang plugin gratisan)"},
                            {"feature_name": "Garansi Teknis & Pendampingan", "feature_desc": "Dukungan teknis responsif", "us_value": "yes (resmi tertulis)", "competitor_value": "no (ditinggal pasca bayar)"}
                        ],
                        "cta_label": "Pesan Website Profesional",
                        "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20buat%20website"
                    },
                    {
                        "_key": "pricing-web",
                        "_type": "marketing_pricing",
                        "_version": 1,
                        "anchor_id": "harga",
                        "headline": "Pilihan Paket Pembuatan Website",
                        "plans": [
                            {
                                "name": "Landing Page Konversi",
                                "price": "Rp 950.000",
                                "period": "sekali bayar",
                                "description": "Cocok untuk promosi produk tunggal, event, atau portofolio pribadi",
                                "features": "1 Halaman Landing Page Panjang (One-Page)\nMobile Responsive & Fast Loading\nDirect WhatsApp CTA Button\nFree Domain .com & Hosting 1 Tahun\nGaransi Teknis 3 Bulan",
                                "cta_label": "Pilih Landing Page",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Landing%20Page"
                            },
                            {
                                "name": "Company Profile Corporate",
                                "price": "Rp 2.250.000",
                                "period": "sekali bayar",
                                "description": "Paling diminati! Standar profesional perusahaan, kantor & instansi",
                                "features": "Hingga 5-7 Halaman Utama (Home, About, Services, Contact, dll)\nCMS Mandiri untuk Update Artikel & Konten\nSetup Email Bisnis Resmi (nama@perusahaan.com)\nStruktur SEO On-Page Lengkap & Google Indexing\nFree Domain & High Speed Hosting 1 Tahun\nGaransi 6 Bulan & Video Panduan Admin",
                                "cta_label": "Pesan Paket Populer",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Company%20Profile",
                                "highlighted": True,
                                "badge": "Paling Laris"
                            },
                            {
                                "name": "Custom Web Portal & Integrasi",
                                "price": "Rp 4.500.000",
                                "period": "sekali bayar",
                                "description": "Website kustom dengan fitur katalog dinamis, portal klien & API",
                                "features": "Halaman Tidak Terbatas & Multi-Bahasa (i18n)\nFitur Katalog Interaktif & Filter Pencarian\nIntegrasi Form WhatsApp ke [Aplikasi CRM](/jasa-pembuatan-crm)\nOptimasi Cloudflare CDN & Server Dedicated\nGaransi 1 Tahun Penuh & Prioritas Support",
                                "cta_label": "Pilih Web Portal",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Web%20Portal"
                            }
                        ]
                    },
                    {
                        "_key": "wa-box-web",
                        "_type": "marketing_whatsapp_cta",
                        "_version": 1,
                        "headline": "Siap Tampilkan Wajah Terbaik Perusahaan Anda di Internet?",
                        "body": "Diskusikan rancangan website bisnis Anda bersama tim pengembang Devk. Kami siap memberikan preview konsep visual gratis.",
                        "label": "Konsultasi Website via WhatsApp",
                        "custom_message": "Halo Devk, saya ingin tanya jasa pembuatan website ({title}). Bisakah kirimkan portofolio?",
                        "variant": "card",
                        "anchor_id": "wa-cta"
                    },
                    {
                        "_key": "faq-web",
                        "_type": "marketing_faq",
                        "_version": 1,
                        "headline": "Pertanyaan Seputar Pembuatan Website",
                        "subheadline": "Jawaban lengkap mengenai domain, kepemilikan, dan kemudahan pengelolaan website.",
                        "items": [
                            {"question": "Berapa lama proses pembuatan website company profile?", "answer": "Untuk Paket Landing Page memakan waktu 3-5 hari kerja, sedangkan Paket Company Profile Corporate rata-rata selesai dalam 7-14 hari kerja setelah materi konten diterima."},
                            {"question": "Apakah saya bisa mengubah tulisan atau foto di website sendiri nanti?", "answer": "Sangat bisa. Kami menyediakan dashboard CMS yang sangat mudah digunakan di komputer maupun HP, tanpa perlu keahlian koding sama sekali."},
                            {"question": "Apakah harga sudah termasuk domain dan hosting?", "answer": "Ya, seluruh paket kami sudah termasuk sewa domain resmi (.com / .id) dan hosting berkecepatan tinggi selama 1 tahun pertama."},
                            {"question": "Apakah website ini bisa dihubungkan ke sistem software internal kami?", "answer": "Tentu saja. Karena dibangun dengan kode modern, website dapat dihubungkan dengan [Aplikasi POS Kasir](/jasa-pembuatan-aplikasi-pos-kasir), [Sistem CRM](/jasa-pembuatan-crm), atau sistem database internal Anda."}
                        ]
                    },
                    {
                        "_key": "cta-web",
                        "_type": "marketing_cta",
                        "_version": 1,
                        "headline": "Miliki Website Berkinerja Tinggi yang Menghasilkan Kepercayaan Klien",
                        "body": "Percayakan kepada tim developer Devk. Kunjungi [Hub Jasa Pembuatan Software](/jasa-pembuatan-software) untuk solusi aplikasi lainnya.",
                        "primary_cta_label": "Hubungi WhatsApp 085799520350",
                        "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20buat%20website%20perusahaan",
                        "secondary_cta_label": "Hub Software Development",
                        "secondary_cta_url": "/jasa-pembuatan-software",
                        "image": {"id": web_media_id}
                    }
                ]
            },
            "seo": {
                "title": "Jasa Pembuatan Website Company Profile & CMS | Devk",
                "description": "Jasa pembuatan website company profile modern, landing page performa tinggi, & CMS mandiri. Cepat, PageSpeed skor 100, SEO ready, mobile-first. WA 085799520350.",
                "canonical": "https://devk.my.id/jasa-pembuatan-website-cms",
                "image": "https://software.devk.my.id/_emdash/api/media/file/devk-universal-hero.jpg",
                "noIndex": False
            }
        },

        # =========================================================================
        # PAGE 4: Jasa Aplikasi Custom ERP
        # =========================================================================
        {
            "collection": "pages",
            "slug": "jasa-aplikasi-custom-erp",
            "status": "published",
            "data": {
                "title": "Jasa Pembuatan Aplikasi Custom ERP & Inventori | Devk",
                "content": [
                    {
                        "_key": "hero-erp",
                        "_type": "marketing_hero",
                        "_version": 1,
                        "centered": False,
                        "eyebrow": "Sistem ERP Terpadu & Otomasi Operasional",
                        "headline": "Jasa Pembuatan Aplikasi Custom ERP — Pas dengan SOP Bisnis Anda",
                        "subheadline": "Satukan seluruh operasional manufaktur, distribusi, inventori gudang, purchasing, penjualan, hingga akuntansi dalam satu sistem terpusat tanpa kompromi vendor lock-in.",
                        "primary_cta_label": "Konsultasi ERP via WhatsApp",
                        "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20tertarik%20pembuatan%20custom%20ERP%20untuk%20perusahaan%20saya",
                        "secondary_cta_label": "Pilihan Skema Biaya ERP",
                        "secondary_cta_url": "#harga",
                        "image": {"id": erp_media_id},
                        "image_caption": "Enterprise Resource Planning Architecture"
                    },
                    {
                        "_key": "bento-erp",
                        "_type": "marketing_bento_grid",
                        "_version": 1,
                        "eyebrow": "Arsitektur Enterprise",
                        "headline": "Sistem Informasi Terpadu Tanpa Pembatas Data (Silo)",
                        "subheadline": "Keputusan manajemen diambil berdasarkan data valid detik itu juga.",
                        "items": [
                            {
                                "title": "100% Menyesuaikan SOP & Alur Kerja Anda",
                                "description": "Bukan perusahaan Anda yang dipaksa tunduk pada alur software kaku, melainkan sistem yang dirancang mengikuti keunikan bisnis Anda.",
                                "tag": "TAILOR-MADE",
                                "badge": "Custom Workflow",
                                "col_span": "2",
                                "row_span": "1",
                                "icon": "cpu",
                                "link_url": "#harga",
                                "link_label": "Lihat Modul"
                            },
                            {
                                "title": "Hak Akses Bertingkat (RBAC)",
                                "description": "Batasi data sensitif: staf hanya melihat modulnya, manajer melakukan approval, owner memegang kontrol penuh.",
                                "tag": "SECURITY",
                                "col_span": "1",
                                "row_span": "1",
                                "icon": "lock"
                            },
                            {
                                "title": "Audit Trail Lengkap & Anti-Manipulasi",
                                "description": "Setiap perubahan data stok, jurnal kas, dan invoice tercatat dengan timestamp, user ID, dan log histori yang tidak bisa dihapus.",
                                "tag": "DATA INTEGRITY",
                                "col_span": "3",
                                "row_span": "1",
                                "icon": "database",
                                "code_snippet": "CREATE TRIGGER audit_inventory_update AFTER UPDATE ON inventory_items\nFOR EACH ROW EXECUTE FUNCTION log_audit_trail(NEW.sku, OLD.quantity, NEW.quantity);"
                            }
                        ]
                    },
                    {
                        "_key": "tabs-erp",
                        "_type": "marketing_tabs",
                        "_version": 1,
                        "eyebrow": "Integrasi Komprehensif",
                        "headline": "Modul ERP yang Dapat Disesuaikan",
                        "subheadline": "Pilih modul yang paling krusial bagi bisnis Anda terlebih dahulu.",
                        "tabs": [
                            {
                                "label": "Modul Supply Chain & Gudang",
                                "title": "Manajemen Stok Multi-Lokasi & Batch Tracking",
                                "description": "Penomoran lot/batch, sistem FIFO/LIFO/Average, alur transfer barang antar cabang, opname stok dengan barcode scanner, dan reorder point otomatis.",
                                "cta_label": "Konsultasi Modul Gudang",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20mau%20konsultasi%20modul%20gudang%20ERP"
                            },
                            {
                                "label": "Modul Purchasing & Vendor",
                                "title": "Purchase Order (PO) & Evaluasi Supplier",
                                "description": "Alur pengajuan permintaan barang (Purchase Request), persetujuan bertingkat (Approval Matrix), pencatatan invoice supplier, dan jadwal hutang dagang.",
                                "cta_label": "Konsultasi Modul Purchasing",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20mau%20konsultasi%20modul%20purchasing%20ERP"
                            },
                            {
                                "label": "Modul Akuntansi & Keuangan",
                                "title": "Jurnal Otomatis, Neraca & Laba Rugi",
                                "description": "Setiap transaksi penjualan kasir atau pembelian barang langsung membentuk jurnal akuntansi otomatis, buku besar, neraca saldo, dan laporan arus kas.",
                                "cta_label": "Konsultasi Modul Finansial",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20mau%20konsultasi%20modul%20akuntansi%20ERP"
                            }
                        ]
                    },
                    {
                        "_key": "steps-erp",
                        "_type": "marketing_steps",
                        "_version": 1,
                        "eyebrow": "Metodologi Teruji",
                        "headline": "4 Fase Penerapan Custom ERP Devk",
                        "subheadline": "Pendekatan profesional untuk memastikan transisi sistem berjalan mulus tanpa downtime operasional.",
                        "steps": [
                            {"step_number": "01", "title": "Business Process Assessment", "description": "Wawancara mendalam dengan pimpinan departemen (gudang, sales, finance) untuk memetakan alur dokumen dan approval matrix."},
                            {"step_number": "02", "title": "Prototyping & Custom Engineering", "description": "Pembangunan arsitektur database relasional, antarmuka kerja, dan modul logika bisnis yang fleksibel."},
                            {"step_number": "03", "title": "User Acceptance Testing (UAT)", "description": "Pengujian skenario transaksi nyata bersama staf inti, pembersihan data historis, dan simulasi neraca saldo."},
                            {"step_number": "04", "title": "Deployment, Training & SLA Support", "description": "Pemasangan di private cloud server atau server lokal kantor, pelatihan menyeluruh per divisi, dan garansi SLA."}
                        ]
                    },
                    {
                        "_key": "comp-erp",
                        "_type": "marketing_comparison_table",
                        "_version": 1,
                        "eyebrow": "Kalkulasi Nilai Bisnis",
                        "headline": "Custom ERP Devk vs Software ERP Jadi (SAP/Odoo Enterprise)",
                        "subheadline": "Perbandingan biaya implementasi, fleksibilitas, dan kepemilikan aset digital.",
                        "us_title": "Custom ERP Devk",
                        "competitor_title": "Software ERP Lisensi Sewa",
                        "rows": [
                            {"feature_name": "Biaya Lisensi Tahunan", "feature_desc": "Bebas royalti tanpa tagihan tahunan berulang", "us_value": "yes (Rp 0 flat selamanya)", "competitor_value": "no (puluhan hingga ratusan juta/tahun)"},
                            {"feature_name": "Kemudahan Adaptasi Alur Kerja", "feature_desc": "Dibuat mengikuti SOP unik perusahaan Anda", "us_value": "yes (100% pas)", "competitor_value": "no (perusahaan harus ubah SOP)"},
                            {"feature_name": "Kepemilikan Source Code & Hak Cipta", "feature_desc": "Aset digital menjadi milik perusahaan Anda", "us_value": "yes", "competitor_value": "no (sewa pakai, terkunci vendor)"},
                            {"feature_name": "Integrasi Sistem Lain (POS & Web)", "feature_desc": "Terhubung mulus dengan [Aplikasi POS](/jasa-pembuatan-aplikasi-pos-kasir)", "us_value": "yes (native terhubung)", "competitor_value": "no (biaya integrasi API mahal)"}
                        ],
                        "cta_label": "Konsultasi ERP Kustom Sekarang",
                        "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20konsultasi%20ERP"
                    },
                    {
                        "_key": "pricing-erp",
                        "_type": "marketing_pricing",
                        "_version": 1,
                        "anchor_id": "harga",
                        "headline": "Skema Investasi Pengembangan Custom ERP",
                        "plans": [
                            {
                                "name": "Paket Modul Inventori & Supply",
                                "price": "Rp 4.500.000",
                                "period": "sekali bayar",
                                "description": "Fokus kontrol gudang, mutasi barang & purchasing untuk distributor",
                                "features": "Modul Multi-Warehouse & Multi-Branch\nPencatatan PO, DO, Surat Jalan & Kartu Stok\nApproval Matrix Pemesanan Barang\nGaransi 6 Bulan & Source Code Diserahkan",
                                "cta_label": "Pilih Modul Supply",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20ERP%20Supply"
                            },
                            {
                                "name": "Paket Integrated Business ERP",
                                "price": "Rp 8.500.000",
                                "period": "sekali bayar",
                                "description": "Paling diminati! Menghubungkan penjualan, gudang & akuntansi",
                                "features": "Integrasi Penjualan, Gudang & Pembelian\nModul Akuntansi & Jurnal Finansial Otomatis\nIntegrasi [Aplikasi POS Kasir](/jasa-pembuatan-aplikasi-pos-kasir)\nMulti-Level Role & Audit Trail Keuangan\nGaransi 1 Tahun Penuh & Pendampingan UAT",
                                "cta_label": "Pesan Paket Populer",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Integrated%20ERP",
                                "highlighted": True,
                                "badge": "Paling Laris"
                            },
                            {
                                "name": "Paket Enterprise Scale Custom",
                                "price": "Rp 15.000.000+",
                                "period": "disesuaikan",
                                "description": "Sistem ERP komplit untuk manufaktur, logistik & holding company",
                                "features": "Modul Bill of Materials (BOM) & Work Order Manufaktur\nIntegrasi API Eksternal & Bank Payment Gateway\nDedicated On-Premise Server / Private Cloud Setup\nSLA Priority Support & Kontrak Perawatan Jangka Panjang",
                                "cta_label": "Konsultasi Enterprise Scale",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Enterprise%20ERP"
                            }
                        ]
                    },
                    {
                        "_key": "wa-box-erp",
                        "_type": "marketing_whatsapp_cta",
                        "_version": 1,
                        "headline": "Siap Mewujudkan Efisiensi Total Operasional Perusahaan Anda?",
                        "body": "Diskusikan roadmap sistem ERP bisnis Anda bersama Lead Solution Architect Devk. Kami sediakan proposal spesifikasi teknis dan estimasi jadwal kerja.",
                        "label": "Jadwalkan Diskusi Teknis via WhatsApp",
                        "custom_message": "Halo Devk, saya ingin konsultasi pengembangan sistem ERP ({title}). Bisakah diskusi dengan Business Analyst?",
                        "variant": "card",
                        "anchor_id": "wa-cta"
                    },
                    {
                        "_key": "faq-erp",
                        "_type": "marketing_faq",
                        "_version": 1,
                        "headline": "Pertanyaan Seputar Custom ERP",
                        "subheadline": "Jawaban lengkap mengenai migrasi data, infrastruktur server, dan lisensi.",
                        "items": [
                            {"question": "Apakah data lama dari Excel bisa dipindahkan ke sistem ERP baru?", "answer": "Bisa. Tim kami menyediakan skrip pembersihan dan import otomatis untuk memindahkan master data barang, customer, supplier, dan saldo awal akuntansi Anda."},
                            {"question": "Apakah sistem ERP ini diinstal di kantor kami atau di cloud?", "answer": "Fleksibel sesuai kebijakan privasi Anda. Kami mendukung instalasi di server lokal on-premise kantor Anda (jaringan LAN tanpa internet) maupun di server cloud VPS pribadi yang dapat diakses aman dari mana saja."},
                            {"question": "Apakah butuh komputer server khusus?", "answer": "Untuk perusahaan skala menengah, PC workstation dengan spesifikasi tepat sudah sangat mumpuni. Kami juga dapat membantu penyediaan dan konfigurasi melalui [Jasa Install Linux Server](/jasa-install-linux-surabaya) atau [Jasa Rakit PC](/jasa-rakit-pc-surabaya-sidoarjo)."},
                            {"question": "Bagaimana jika suatu saat perusahaan kami membutuhkan penambahan fitur baru?", "answer": "Karena source code 100% diserahkan kepada Anda dan dibangun dengan standar kode bersih, fitur baru dapat ditambahkan kapan saja oleh tim Devk maupun tim internal IT Anda sendiri."}
                        ]
                    },
                    {
                        "_key": "cta-erp",
                        "_type": "marketing_cta",
                        "_version": 1,
                        "headline": "Bangun Sistem ERP Kustom yang Mempercepat Pertumbuhan Bisnis Anda",
                        "body": "Aset digital berharga milik perusahaan Anda sendiri. Jelajahi juga induk [Hub Jasa Pembuatan Software](/jasa-pembuatan-software) untuk solusi lainnya.",
                        "primary_cta_label": "Hubungi WhatsApp 085799520350",
                        "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20konsultasi%20sistem%20ERP",
                        "secondary_cta_label": "Hub Software Development",
                        "secondary_cta_url": "/jasa-pembuatan-software",
                        "image": {"id": erp_media_id}
                    }
                ]
            },
            "seo": {
                "title": "Jasa Pembuatan Aplikasi Custom ERP & Inventori | Devk",
                "description": "Jasa pembuatan sistem ERP kustom untuk manufaktur, distribusi, & perkantoran. Modul inventori, purchasing, invoicing, & laporan keuangan terpadu. WA 085799520350.",
                "canonical": "https://devk.my.id/jasa-aplikasi-custom-erp",
                "image": "https://software.devk.my.id/_emdash/api/media/file/devk-enterprise-pos-software.jpg",
                "noIndex": False
            }
        }
    ]

    for idx, p in enumerate(pages):
        slug = p["slug"]
        print(f"Creating page {idx+1}: {slug}...")
        res = call_mcp("content_create", p)
        success = isinstance(res, dict) and "item" in res
        print(f"Status {slug}:", "SUCCESS" if success else f"FAILED: {res}")
        time.sleep(1)

if __name__ == "__main__":
    build_pilar1_pages()
