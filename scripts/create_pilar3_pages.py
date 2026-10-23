import json
import base64
import os
import glob
import urllib.request

PAT_TOKEN = "ec_pat_O3MrYsN2tLlxEUOnOEZiipYHOHXcv0T9j0L3QsjzcjM"
API_URL = "https://software.devk.my.id/_emdash/api/mcp"

def call_mcp(tool_name, arguments):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    req = urllib.request.Request(
        API_URL,
        headers={
            "Authorization": f"Bearer {PAT_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
        data=json.dumps(payload).encode("utf-8")
    )
    with urllib.request.urlopen(req) as resp:
        res_bytes = resp.read()
        res_str = res_bytes.decode("utf-8")
        for line in res_str.split("\n"):
            if line.startswith("data: "):
                line = line[6:]
            line = line.strip()
            if line and line.startswith("{"):
                try:
                    data = json.loads(line)
                    if "result" in data:
                        content = data["result"].get("content", [])
                        if content and "text" in content[0]:
                            return json.loads(content[0]["text"])
                        return data["result"]
                    return data
                except Exception:
                    pass
        return json.loads(res_str)

def upload_image(filepath, filename, alt, caption):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None
    with open(filepath, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    res = call_mcp("media_upload", {
        "filename": filename,
        "base64": b64,
        "contentType": "image/jpeg",
        "alt": alt,
        "caption": caption
    })
    print(f"Uploaded {filename}: id={res.get('id')}")
    return res

def find_latest_artifact(pattern):
    files = glob.glob(f"/home/ubuntu/.hermes-web-ui/coding-agent/model/default/global/antigravity/runs/8990e7490a90aa58ee5831d252f8252a0a109ff4eb3c116f53df91ec1c5617f4/.gemini/antigravity-cli/brain/ddf2d975-e743-43d4-be01-3683551b7f8b/{pattern}")
    if not files:
        return None
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

def build_pilar3_pages():
    # 1. Windows Image
    win_img_path = find_latest_artifact("*windows_install*.jpg")
    win_media = upload_image(win_img_path, "devk-windows-install-surabaya.jpg", "Jasa Install Ulang Windows Surabaya dan Sidoarjo", "Teknisi Install Windows 11 Surabaya") if win_img_path else None
    win_media_id = win_media.get("id") if win_media else "01M5J1TC04W154PPG1WPKSRB79"

    # 2. MacBook Image
    mac_img_path = find_latest_artifact("*macbook_repair*.jpg")
    mac_media = upload_image(mac_img_path, "devk-macbook-repair-surabaya.jpg", "Jasa Install MacBook dan iMac Surabaya Sidoarjo", "Spesialis macOS Apple Surabaya") if mac_img_path else None
    mac_media_id = mac_media.get("id") if mac_media else "01M5HZK0RGYWEAZDYC5EGRQY4W"

    # 3. Linux Image
    linux_img_path = find_latest_artifact("*linux_workstation*.jpg")
    linux_media = upload_image(linux_img_path, "devk-linux-workstation-surabaya.jpg", "Jasa Install Linux Ubuntu Server Surabaya", "Setup Linux Developer Workstation") if linux_img_path else None
    linux_media_id = linux_media.get("id") if linux_media else "01M5HZJKMP3A1QNSR57KCEEHQT"

    # 4. Laptop Service Onsite Image
    lap_img_path = find_latest_artifact("*laptop_service*.jpg")
    lap_media = upload_image(lap_img_path, "devk-servis-laptop-panggilan.jpg", "Jasa Servis Laptop Panggilan Surabaya Sidoarjo", "Deep Cleaning dan Repaste Thermal Paste") if lap_img_path else None
    lap_media_id = lap_media.get("id") if lap_media else "01M5J1TC04W154PPG1WPKSRB79"

    # 5. Rakit PC Image
    pc_img_path = find_latest_artifact("*rakit_pc*.jpg")
    pc_media = upload_image(pc_img_path, "devk-rakit-pc-surabaya.jpg", "Jasa Rakit PC Gaming dan Workstation Surabaya", "Custom PC Building dan Cable Management") if pc_img_path else None
    pc_media_id = pc_media.get("id") if pc_media else "01M5HZJ3Q0TPG3939KRD9YNM4G"

    pages = [
        # =========================================================================
        # PAGE 1: Jasa Install Ulang Windows Surabaya & Sidoarjo
        # =========================================================================
        {
            "collection": "pages",
            "slug": "jasa-install-ulang-windows-surabaya-sidoarjo",
            "status": "published",
            "data": {
                "title": "Jasa Install Ulang Windows Surabaya & Sidoarjo | Bersih & Bergaransi",
                "content": [
                    {
                        "_key": "hero-win",
                        "_type": "marketing_hero",
                        "_version": 1,
                        "centered": False,
                        "eyebrow": "Teknisi Panggilan & Workshop Resmi",
                        "headline": "Jasa Install Ulang Windows Surabaya & Sidoarjo — Bersih & Cepat",
                        "subheadline": "Solusi laptop lemot, kena virus, atau blue screen. Clean install Windows 11 & 10 Pro resmi, aktivasi permanen, update driver presisi, dan garansi tertulis 30 hari.",
                        "primary_cta_label": "Pesan Teknisi via WhatsApp",
                        "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20butuh%20jasa%20install%20ulang%20Windows%20di%20Surabaya%20/%20Sidoarjo.%20Apakah%20bisa%20panggilan%20hari%20ini?",
                        "secondary_cta_label": "Lihat Pilihan Paket Biaya",
                        "secondary_cta_url": "#harga",
                        "image": {"id": win_media_id},
                        "image_caption": "Instalasi Windows 11 Pro Bebas Bloatware"
                    },
                    {
                        "_key": "steps-win",
                        "_type": "marketing_steps",
                        "_version": 1,
                        "eyebrow": "Alur Kerja Transparan",
                        "headline": "4 Langkah Praktis Install Ulang Bebas Repot",
                        "subheadline": "Pilih teknisi meluncur ke rumah/kantor Anda atau bawa langsung ke workshop resmi Devk di Surabaya & Sidoarjo.",
                        "steps": [
                            {"step_number": "01", "title": "Konsultasi & Cek Spek", "description": "Hubungi WhatsApp kami, jelaskan merk laptop dan versi Windows yang diinginkan (Windows 11 atau 10)."},
                            {"step_number": "02", "title": "Teknisi Tiba / Drop-off", "description": "Teknisi datang ke lokasi Anda sesuai jam janji, atau Anda bisa datang ke Workshop Graha Indraprasta Sidoarjo / Tenggilis Mulya Surabaya."},
                            {"step_number": "03", "title": "Backup Data & Clean Install", "description": "Seluruh file penting diamankan ke partisi khusus sebelum instalasi bersih (Clean Install) bebas virus & bloatware."},
                            {"step_number": "04", "title": "Finishing & Garansi 30 Hari", "description": "Instalasi software standar (Office, Browser, PDF, WinRAR), pengujian kecepatan boot, dan serah terima garansi resmi."}
                        ]
                    },
                    {
                        "_key": "split-win",
                        "_type": "marketing_split",
                        "_version": 1,
                        "eyebrow": "Standar Pengerjaan Devk",
                        "headline": "Mengapa Clean Install Devk Jauh Lebih Kencang & Stabil?",
                        "body": "Banyak tempat servis memasang Windows dari file image ghosting yang penuh dengan bloatware tersembunyi, driver lawas, dan rentan corrupt saat update online. Di Devk, kami hanya menggunakan installer resmi Microsoft terbaru, disetel khusus sesuai spesifikasi prosesor dan kartu grafis Anda.",
                        "points": "Installer Resmi Microsoft Terbaru (Update 2026 Ready)\nDriver Chipset & VGA Terkonfigurasi Presisi\nPengamanan Data Pribadi Tanpa Risiko Terhapus\nBebas Iklan, Bloatware & Program Jahat Tersembunyi",
                        "image": {"id": win_media_id},
                        "image_caption": "Sistem Operasi Bersih & Respon Cepat",
                        "image_first": True,
                        "cta_label": "Konsultasi Kendala Laptop Anda",
                        "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20tanya%20kondisi%20laptop%20saya"
                    },
                    {
                        "_key": "comp-win",
                        "_type": "marketing_comparison_table",
                        "_version": 1,
                        "eyebrow": "Transparansi Penuh",
                        "headline": "Keunggulan Install Ulang Devk vs Tempat Servis Lain",
                        "subheadline": "Perbandingan standar profesional pengerjaan teknisi Devk demi kenyamanan Anda.",
                        "us_title": "Layanan Devk Surabaya-Sidoarjo",
                        "competitor_title": "Tempat Servis Konvensional",
                        "rows": [
                            {"feature_name": "Prosedur Backup Data", "feature_desc": "Data pribadi dicek dan diamankan sebelum format", "us_value": "yes", "competitor_value": "no"},
                            {"feature_name": "Update Online Tanpa Takut Layar Hitam", "feature_desc": "Aktivasi digital permanen terdaftar", "us_value": "yes", "competitor_value": "no"},
                            {"feature_name": "Layanan Panggilan ke Rumah / Kantor", "feature_desc": "Teknisi datang ke lokasi Anda di Surabaya & Sidoarjo", "us_value": "yes", "competitor_value": "no"},
                            {"feature_name": "Garansi Resmi Tertulis", "feature_desc": "Perlindungan garansi 30 hari penuh", "us_value": "yes", "competitor_value": "no"}
                        ],
                        "cta_label": "Pesan Teknisi Sekarang",
                        "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20order%20install%20Windows"
                    },
                    {
                        "_key": "feat-win",
                        "_type": "marketing_features",
                        "_version": 1,
                        "eyebrow": "Jangkauan Wilayah & Integrasi Layanan",
                        "headline": "Area Servis Panggilan Surabaya & Sidoarjo",
                        "subheadline": "Teknisi kami siap menjangkau seluruh area Surabaya dan Sidoarjo. Anda juga dapat melengkapi laptop dengan software arsitektur atau desain melalui hub kami.",
                        "columns": "3",
                        "features": [
                            {"icon": "desktop", "title": "Surabaya Selatan & Rungkut", "description": "Tenggilis Mulya, Rungkut Industri, Wonokromo, Jemursari, Gunung Anyar.", "link_url": "#wa-cta", "link_label": "Panggil Teknisi"},
                            {"icon": "building", "title": "Surabaya Pusat & Barat", "description": "Tunjungan, Tegalsari, HR Muhammad, Mayjen Sungkono, Wiyung.", "link_url": "#wa-cta", "link_label": "Panggil Teknisi"},
                            {"icon": "globe", "title": "Surabaya Timur & Utara", "description": "Mulyorejo, ITS Keputih, Kertajaya, Kenjeran, Perak.", "link_url": "#wa-cta", "link_label": "Panggil Teknisi"},
                            {"icon": "wrench", "title": "Sidoarjo Utara & Waru", "description": "Waru, Tropodo, Sedati, Aloha, Pondok Tjandra.", "link_url": "#wa-cta", "link_label": "Panggil Teknisi"},
                            {"icon": "storefront", "title": "Sidoarjo Kota & Candi", "description": "Graha Indraprasta, Alun-alun Sidoarjo, Buduran, Candi, Gedangan.", "link_url": "#wa-cta", "link_label": "Panggil Teknisi"},
                            {"icon": "cpu", "title": "Integrasi Software & Hardware", "description": "Butuh install software berat? Cek direktori [52 Software Online](/jasa-install-software-online) atau [Servis Laptop Panggilan](/jasa-servis-laptop-panggilan-surabaya-sidoarjo).", "link_url": "/jasa-install-software-online", "link_label": "Katalog Software"}
                        ]
                    },
                    {
                        "_key": "pricing-win",
                        "_type": "marketing_pricing",
                        "_version": 1,
                        "anchor_id": "harga",
                        "headline": "Pilihan Paket Biaya Install Ulang",
                        "plans": [
                            {
                                "name": "Paket Standard",
                                "price": "Rp 100.000",
                                "period": "/unit",
                                "description": "Cocok untuk laptop lemot yang butuh penyegaran sistem",
                                "features": "Windows 11 / 10 Pro 64-bit\nDriver VGA, Audio & WiFi Lengkap\nPaket Software Esensial (Office, Chrome, PDF)\nGaransi 14 Hari",
                                "cta_label": "Pilih Paket Standard",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Standard%20Windows"
                            },
                            {
                                "name": "Paket Pro + Deep Clean",
                                "price": "Rp 175.000",
                                "period": "/unit",
                                "description": "Paling diminati! Windows baru + suhu laptop dingin kembali",
                                "features": "Windows 11 / 10 Pro Terbaru\nDriver Tuning & Optimasi SSD\nDeep Cleaning Kipas & Heatsink\nThermal Paste Arctic MX-4 Grade Pro\nGaransi 30 Hari Penuh",
                                "cta_label": "Pesan Paket Populer",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Pro%20Clean%20Windows",
                                "highlighted": True,
                                "badge": "Paling Laris"
                            },
                            {
                                "name": "Paket Kantor / Multi-Unit",
                                "price": "Rp 250.000",
                                "period": "/unit",
                                "description": "Solusi komprehensif untuk kantor, studio & sekolah",
                                "features": "Windows Pro Enterprise Setup\nSetting LAN, File Sharing & Printer Sharing\nSystem Backup Image Restore\nGaransi 60 Hari & Free Remote Support",
                                "cta_label": "Pilih Paket Kantor",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Kantor%20Windows"
                            }
                        ]
                    },
                    {
                        "_key": "wa-box-win",
                        "_type": "marketing_whatsapp_cta",
                        "_version": 1,
                        "headline": "Teknisi Kami Siap Datang ke Lokasi Anda Hari Ini",
                        "body": "Tidak perlu repot macet-macetan membawa PC atau laptop. Hubungi teknisi Devk dan jadwalkan kunjungan servis di rumah atau kantor Anda.",
                        "label": "Jadwalkan Teknisi via WhatsApp",
                        "custom_message": "Halo Devk, saya ingin pesan layanan {title}. Apakah teknisi bisa meluncur ke alamat saya?",
                        "variant": "card",
                        "anchor_id": "wa-cta"
                    },
                    {
                        "_key": "faq-win",
                        "_type": "marketing_faq",
                        "_version": 1,
                        "headline": "Pertanyaan Seputar Install Ulang Windows",
                        "subheadline": "Jawaban atas pertanyaan yang sering diajukan pelanggan di Surabaya dan Sidoarjo.",
                        "items": [
                            {"question": "Apakah file data di drive D/E saya akan hilang?", "answer": "Sama sekali tidak. Teknisi kami menerapkan SOP ketat pengamanan data. Hanya partisi sistem C: yang diformat ulang, data dokumen, foto, dan kerjaan di partisi lain 100% aman."},
                            {"question": "Berapa lama proses install ulang selesai?", "answer": "Dengan penyimpanan SSD modern, proses instalasi bersih, driver, dan software standar memakan waktu rata-rata 30 hingga 60 menit."},
                            {"question": "Apakah bisa panggilan ke rumah atau kosan di Surabaya dan Sidoarjo?", "answer": "Ya, teknisi kami melayani panggilan on-site di seluruh kecamatan Surabaya dan Sidoarjo dengan jadwal fleksibel."},
                            {"question": "Apakah saya juga bisa membawa laptop ke workshop Devk?", "answer": "Tentu saja. Anda bisa drop-off unit di Workshop Sidoarjo (Graha Indraprasta G7/15) atau Workshop Surabaya (Jl. Tenggilis Mulya 76)."},
                            {"question": "Bagaimana klaim garansi jika Windows bermasalah setelah instalasi?", "answer": "Kami memberikan garansi 30 hari penuh. Jika ada kendala sistem atau software, teknisi akan membantu via remote gratis atau kunjungan ulang tanpa biaya tambahan."}
                        ]
                    },
                    {
                        "_key": "cta-win",
                        "_type": "marketing_cta",
                        "_version": 1,
                        "headline": "Kembalikan Kecepatan Laptop Anda Seperti Baru Beli",
                        "body": "Pengerjaan transparan, data aman, teknisi ramah, dan garansi resmi. Kunjungi [Hub Servis Komputer Surabaya-Sidoarjo](/jasa-install-komputer-surabaya-sidoarjo) untuk layanan hardware lainnya.",
                        "primary_cta_label": "Hubungi WhatsApp 085799520350",
                        "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20install%20ulang%20Windows",
                        "secondary_cta_label": "Katalog Jasa Rakit PC",
                        "secondary_cta_url": "/jasa-rakit-pc-surabaya-sidoarjo",
                        "image": {"id": win_media_id}
                    }
                ]
            },
            "seo": {
                "title": "Jasa Install Ulang Windows Surabaya & Sidoarjo | Devk",
                "description": "Jasa install ulang Windows 11 & 10 Pro panggilan Surabaya & Sidoarjo. Bersih tanpa bloatware, aktivasi permanen, garansi 30 hari. Hubungi WA 085799520350.",
                "canonical": "https://devk.my.id/jasa-install-ulang-windows-surabaya-sidoarjo",
                "image": "https://software.devk.my.id/_emdash/api/media/file/devk-windows-install-surabaya.jpg",
                "noIndex": False
            }
        },

        # =========================================================================
        # PAGE 2: Jasa Install MacBook & iMac Surabaya
        # =========================================================================
        {
            "collection": "pages",
            "slug": "jasa-install-macbook-imac-surabaya",
            "status": "published",
            "data": {
                "title": "Jasa Install MacBook & iMac Surabaya | macOS Service",
                "content": [
                    {
                        "_key": "hero-mac",
                        "_type": "marketing_hero",
                        "_version": 1,
                        "centered": False,
                        "eyebrow": "Spesialis Apple Silicon M1-M4 & Intel",
                        "headline": "Jasa Install MacBook & iMac Surabaya — Cepat & Bergaransi",
                        "subheadline": "Atasi masalah boot loop folder tanda tanya, stuck logo Apple, atau upgrade ke macOS Sonoma / Sequoia. Penanganan ahli untuk MacBook Pro, MacBook Air, iMac, dan Mac Mini.",
                        "primary_cta_label": "Konsultasi Servis Mac via WA",
                        "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20servis%20install%20MacBook%20di%20Surabaya",
                        "secondary_cta_label": "Pilihan Paket Layanan Mac",
                        "secondary_cta_url": "#harga",
                        "image": {"id": mac_media_id},
                        "image_caption": "Apple macOS Recovery & Optimization"
                    },
                    {
                        "_key": "steps-mac",
                        "_type": "marketing_steps",
                        "_version": 1,
                        "eyebrow": "Standar Presisi Apple",
                        "headline": "Prosedur Pemulihan & Instalasi Mac Profesional",
                        "subheadline": "Keamanan chip T2 dan Secure Enclave Apple Silicon menjadi prioritas utama kami.",
                        "steps": [
                            {"step_number": "01", "title": "Identifikasi Seri Mac", "description": "Pemeriksaan model A-number, chipset (M1/M2/M3/M4 atau Intel), dan kapasitas penyimpanan APFS."},
                            {"step_number": "02", "title": "Pilihan Panggilan / Workshop", "description": "Teknisi siap datang ke lokasi kafe/kantor di Surabaya & Sidoarjo atau pengerjaan di workshop kami."},
                            {"step_number": "03", "title": "Clean Install macOS Resmi", "description": "Format APFS bersih dan instalasi image macOS murni dari server resmi Apple tanpa modifikasi berbahaya."},
                            {"step_number": "04", "title": "Aplikasi & Testing Baterai", "description": "Konfigurasi software pendukung, kalibrasi daya baterai, dan serah terima garansi resmi 30 hari."}
                        ]
                    },
                    {
                        "_key": "split-mac",
                        "_type": "marketing_split",
                        "_version": 1,
                        "eyebrow": "Keahlian Sistem macOS",
                        "headline": "Solusi Tuntas Kendala Boot Loop, Flashing Folder & Lambat",
                        "body": "Perangkat Mac membutuhkan perlakuan firmware khusus, terutama pada generasi Apple Silicon yang mengintegrasikan SSD dan RAM langsung ke chip SOC. Kesalahan instalasi dapat memicu DFU mode lock. Teknisi Devk memahami arsitektur Apple secara mendalam untuk memastikan Mac Anda kembali berfungsi seperti baru.",
                        "points": "Dukungan macOS Sonoma, Sequoia, Ventura hingga Monterey\nPenanganan MacBook Air, MacBook Pro Retina, iMac 4K/5K & Mac Studio\nSetup Dual-Boot BootCamp (untuk Mac Intel) atau Parallels Desktop\nInstalasi Paket Desain Apple (Adobe CC Mac, Final Cut Pro, Office for Mac)",
                        "image": {"id": mac_media_id},
                        "image_caption": "Spesialisasi Apple macOS Surabaya",
                        "image_first": True,
                        "cta_label": "Tanya Teknisi Mac Kami",
                        "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20bisa%20bantu%20kendala%20MacBook%20saya?"
                    },
                    {
                        "_key": "comp-mac",
                        "_type": "marketing_comparison_table",
                        "_version": 1,
                        "eyebrow": "Kenapa Memilih Devk?",
                        "headline": "Standar Servis Mac Devk vs Bengkel Servis Umum",
                        "subheadline": "Keamanan data, privasi Apple ID, dan integritas hardware yang terjamin.",
                        "us_title": "Layanan Devk Mac Surabaya",
                        "competitor_title": "Bengkel Servis Komputer Biasa",
                        "rows": [
                            {"feature_name": "Keahlian Apple Silicon M-Series", "feature_desc": "Paham konfigurasi APFS & DFU recovery mode", "us_value": "yes", "competitor_value": "no"},
                            {"feature_name": "Privasi Apple ID & iCloud", "feature_desc": "Tidak meminta password akun pribadi Apple ID", "us_value": "yes", "competitor_value": "no"},
                            {"feature_name": "Software Khusus Arsitektur ARM64", "feature_desc": "Native speed tanpa boros baterai di emulator Rosetta", "us_value": "yes", "competitor_value": "no"},
                            {"feature_name": "Garansi 30 Hari & Nota Resmi", "feature_desc": "Jaminan pengerjaan tuntas", "us_value": "yes", "competitor_value": "no"}
                        ],
                        "cta_label": "Pesan Servis Mac Sekarang",
                        "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20pesan%20servis%20MacBook"
                    },
                    {
                        "_key": "feat-mac",
                        "_type": "marketing_features",
                        "_version": 1,
                        "eyebrow": "Ekosistem & Software Pendukung",
                        "headline": "Software Kreatif & Kompatibilitas Mac",
                        "subheadline": "Lengkapi MacBook Anda dengan aplikasi penunjang kerja dan perkuliahan. Cek tautan klaster layanan kami di bawah ini.",
                        "columns": "3",
                        "features": [
                            {"icon": "desktop", "title": "Adobe CC Mac Native", "description": "Photoshop, Illustrator, Premiere Pro yang berjalan native cepat di M1/M2/M3. Cek [Adobe CC Master](/jasa-install-adobe-cc-master-collection-online).", "link_url": "/jasa-install-adobe-cc-master-collection-online", "link_label": "Lihat Adobe CC"},
                            {"icon": "chart", "title": "Microsoft Office 365 for Mac", "description": "Word, Excel, PowerPoint terintegrasi mulus dengan cloud dan font standar.", "link_url": "/jasa-install-microsoft-office-online", "link_label": "Lihat Office"},
                            {"icon": "wrench", "title": "CAD & 3D di Mac", "description": "Instalasi [AutoCAD for Mac](/jasa-install-autocad-online) dan SketchUp dengan performa rendering optimal.", "link_url": "/jasa-install-autocad-online", "link_label": "Lihat AutoCAD"},
                            {"icon": "shield", "title": "Deep Cleaning MacBook", "description": "Pembersihan debu dan penggantian pasta pendingin melalui [Servis Laptop Panggilan](/jasa-servis-laptop-panggilan-surabaya-sidoarjo).", "link_url": "/jasa-servis-laptop-panggilan-surabaya-sidoarjo", "link_label": "Servis Laptop"},
                            {"icon": "zap", "title": "Dual-Boot Windows Mac", "description": "Ingin pakai Windows di Mac? Kami sediakan [Install Ulang Windows](/jasa-install-ulang-windows-surabaya-sidoarjo) via BootCamp.", "link_url": "/jasa-install-ulang-windows-surabaya-sidoarjo", "link_label": "Install Windows"},
                            {"icon": "building", "title": "Drop-off Workshop", "description": "Kunjungi workshop kami di Jl. Tenggilis Mulya 76 Surabaya atau Graha Indraprasta G7/15 Sidoarjo.", "link_url": "/jasa-install-komputer-surabaya-sidoarjo", "link_label": "Info Workshop"}
                        ]
                    },
                    {
                        "_key": "pricing-mac",
                        "_type": "marketing_pricing",
                        "_version": 1,
                        "anchor_id": "harga",
                        "headline": "Paket Biaya Servis & Install Mac",
                        "plans": [
                            {
                                "name": "macOS Clean Install",
                                "price": "Rp 150.000",
                                "period": "/unit",
                                "description": "Untuk MacBook/iMac yang butuh pemulihan sistem operasi murni",
                                "features": "Format APFS & macOS Sonoma/Sequoia\nFirmware Apple Update Resmi\nBrowser, VLC, Unarchiver\nGaransi 14 Hari",
                                "cta_label": "Pilih macOS Clean",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20macOS%20Clean"
                            },
                            {
                                "name": "macOS Pro + Productivity",
                                "price": "Rp 250.000",
                                "period": "/unit",
                                "description": "Pilihan terpopuler mahasiswa & profesional kreatif Surabaya",
                                "features": "Clean Install macOS Terbaru\nMicrosoft Office 365 / 2024 for Mac\nPDF Expert & Font Suite Lengkap\nOptimasi Cache & Battery Health\nGaransi 30 Hari Penuh",
                                "cta_label": "Pesan Paket Pro Mac",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Pro%20Mac",
                                "highlighted": True,
                                "badge": "Paling Laris"
                            },
                            {
                                "name": "macOS Studio Master",
                                "price": "Rp 350.000",
                                "period": "/unit",
                                "description": "Paket komplit untuk editor video, arsitek & studio kreatif",
                                "features": "Clean Install macOS Native M-Series\nPaket Adobe Creative Cloud Mac\nFinal Cut Pro / Logic Pro / CAD Setup\nFree Backup Data hingga 100 GB\nGaransi 60 Hari & Free Remote Support",
                                "cta_label": "Pilih Studio Master",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Studio%20Master%20Mac"
                            }
                        ]
                    },
                    {
                        "_key": "wa-box-mac",
                        "_type": "marketing_whatsapp_cta",
                        "_version": 1,
                        "headline": "Konsultasikan Kendala MacBook Anda Sekarang",
                        "body": "Admin teknis Apple kami siap menjawab pertanyaan mengenai tipe Mac, kompatibilitas OS, dan penjadwalan servis dalam 5 menit.",
                        "label": "Chat Teknisi Mac via WhatsApp",
                        "custom_message": "Halo Devk, saya ingin konsultasi servis MacBook / iMac ({title}). Kapan teknisi bisa bantu?",
                        "variant": "card",
                        "anchor_id": "wa-cta"
                    },
                    {
                        "_key": "faq-mac",
                        "_type": "marketing_faq",
                        "_version": 1,
                        "headline": "FAQ Servis & Install Mac Surabaya",
                        "subheadline": "Hal-hal yang sering ditanyakan pemilik MacBook dan iMac.",
                        "items": [
                            {"question": "Apakah MacBook chip M1, M2, M3 dan M4 bisa di-install ulang?", "answer": "Sangat bisa. Kami berpengalaman menangani instalasi macOS Sonoma dan Sequoia pada seluruh lini Apple Silicon secara native tanpa kendala."},
                            {"question": "MacBook saya stuck di ikon folder tanda tanya saat dinyalakan, apa penyebabnya?", "answer": "Itu menandakan macOS tidak mendeteksi sistem boot yang valid atau sistem file APFS corrupt. Clean install kami akan memulihkan struktur partisi dan sistem operasi tanpa merusak SSD internal."},
                            {"question": "Apakah saya perlu memberikan password Apple ID saya?", "answer": "Tidak perlu. Demi privasi dan keamanan Anda, kami tidak meminta password Apple ID atau iCloud. Anda dapat login sendiri setelah instalasi selesai."},
                            {"question": "Apakah melayani servis panggilan ke kantor atau kafe di Surabaya?", "answer": "Ya, teknisi kami melayani panggilan on-site ke berbagai lokasi di Surabaya dan Sidoarjo, atau Anda dapat membawa unit ke workshop kami di Tenggilis Mulya Surabaya."}
                        ]
                    },
                    {
                        "_key": "cta-mac",
                        "_type": "marketing_cta",
                        "_version": 1,
                        "headline": "MacBook Kembali Cepat, Halus & Siap Menemani Produktivitas Anda",
                        "body": "Dapatkan penanganan terbaik dari teknisi spesialis Apple Devk di Surabaya dan Sidoarjo.",
                        "primary_cta_label": "Pesan Servis Mac Sekarang",
                        "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20servis%20MacBook",
                        "secondary_cta_label": "Katalog Software Mac Online",
                        "secondary_cta_url": "/jasa-install-software-online",
                        "image": {"id": mac_media_id}
                    }
                ]
            },
            "seo": {
                "title": "Jasa Install MacBook & iMac Surabaya | Devk",
                "description": "Jasa install ulang macOS Sonoma, Sequoia & perbaikan MacBook / iMac di Surabaya & Sidoarjo. Apple Silicon M1-M4 & Intel, bergaransi resmi. WA 085799520350.",
                "canonical": "https://devk.my.id/jasa-install-macbook-imac-surabaya",
                "image": "https://software.devk.my.id/_emdash/api/media/file/devk-macbook-repair-surabaya.jpg",
                "noIndex": False
            }
        },

        # =========================================================================
        # PAGE 3: Jasa Install Linux Surabaya
        # =========================================================================
        {
            "collection": "pages",
            "slug": "jasa-install-linux-surabaya",
            "status": "published",
            "data": {
                "title": "Jasa Install Linux OS & Server Surabaya | Devk",
                "content": [
                    {
                        "_key": "hero-linux",
                        "_type": "marketing_hero",
                        "_version": 1,
                        "centered": False,
                        "eyebrow": "Solusi Developer, Riset & Enterprise",
                        "headline": "Jasa Install Linux & Konfigurasi Server Surabaya - Sidoarjo",
                        "subheadline": "Setup dual-boot Windows & Linux aman tanpa merusak bootloader, instalasi distro Ubuntu, Debian, Fedora, Arch, serta konfigurasi environment Docker, GPU CUDA, dan web server production.",
                        "primary_cta_label": "Konsultasi Setup Linux via WA",
                        "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20butuh%20jasa%20install%20Linux%20di%20Surabaya",
                        "secondary_cta_label": "Lihat Pilihan Konfigurasi",
                        "secondary_cta_url": "#harga",
                        "image": {"id": linux_media_id},
                        "image_caption": "Linux Dual-Boot & Developer Workstation"
                    },
                    {
                        "_key": "steps-linux",
                        "_type": "marketing_steps",
                        "_version": 1,
                        "eyebrow": "Konfigurasi Presisi",
                        "headline": "4 Tahap Setup Linux Bebas Error",
                        "subheadline": "Penanganan teliti untuk partisi EFI/GPT, driver kartu grafis proprietary, dan keamanan server.",
                        "steps": [
                            {"step_number": "01", "title": "Analisis Hardware & Kebutuhan", "description": "Menentukan distribusi Linux terbaik (Ubuntu LTS, Debian, Fedora, Arch) sesuai kebutuhan coding, riset AI, atau server."},
                            {"step_number": "02", "title": "Partisi Partisi Aman (Dual-Boot)", "description": "Alokasi partisi swap, root, dan home tanpa mengganggu partisi data dan sistem Windows yang sudah ada."},
                            {"step_number": "03", "title": "Instalasi Driver & Dev Stack", "description": "Pemasangan driver NVIDIA proprietary, CUDA toolkit, Docker, Python, Node.js, Git, dan tools CLI favorit Anda."},
                            {"step_number": "04", "title": "Hardening & Uji Stabilitas", "description": "Penyetelan power management TLP untuk laptop, firewall UFW, dan serah terima sistem siap pakai bergaransi."}
                        ]
                    },
                    {
                        "_key": "split-linux",
                        "_type": "marketing_split",
                        "_version": 1,
                        "eyebrow": "Bebas Risiko GRUB Rescue",
                        "headline": "Dual-Boot Sempurna Tanpa Takut Kehilangan Data Windows",
                        "body": "Masalah paling sering dialami pengguna saat mencoba install Linux sendiri adalah terhapusnya partisi Windows atau error GRUB rescue yang membuat komputer tidak bisa masuk ke sistem mana pun. Tim teknisi Devk menguasai arsitektur boot UEFI dan GPT partitioning, memastikan menu boot dual-boot bekerja mulus dan aman.",
                        "points": "Dual-Boot Windows 11 & Linux dengan Menu Boot Elegan\nDriver NVIDIA CUDA & TensorRT Terkonfigurasi untuk Machine Learning\nPenyetelan Manajemen Daya Baterai Laptop Dingin & Awet\nInstalasi Server Headless (Nginx, PostgreSQL, Docker, SSH Key Security)",
                        "image": {"id": linux_media_id},
                        "image_caption": "Linux System Administration Surabaya",
                        "image_first": True,
                        "cta_label": "Konsultasi Setup Distro Anda",
                        "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20mau%20konsultasi%20setup%20distro%20Linux"
                    },
                    {
                        "_key": "comp-linux",
                        "_type": "marketing_comparison_table",
                        "_version": 1,
                        "eyebrow": "Standar Devk",
                        "headline": "Setup Linux Devk vs Pasang Sendiri Tanpa Panduan",
                        "subheadline": "Hemat waktu Anda dari troubleshooting berhari-hari di forum Linux.",
                        "us_title": "Setup Linux Profesional Devk",
                        "competitor_title": "Coba Pasang Sendiri / Otodidak",
                        "rows": [
                            {"feature_name": "Partisi Dual-Boot Aman Anti-Format", "feature_desc": "Data Windows 100% terjaga utuh", "us_value": "yes", "competitor_value": "no"},
                            {"feature_name": "Driver Proprietary NVIDIA / WiFi Siap Pakai", "feature_desc": "Bebas masalah layar hitam (black screen on boot)", "us_value": "yes", "competitor_value": "no"},
                            {"feature_name": "Environment Developer Siap Tempur", "feature_desc": "Docker, Zsh, VS Code, Git terkonfigurasi", "us_value": "yes", "competitor_value": "no"},
                            {"feature_name": "Garansi Troubleshooting & Bimbingan", "feature_desc": "Bantuan teknisi ramah jika ada kendala", "us_value": "yes", "competitor_value": "no"}
                        ],
                        "cta_label": "Pesan Setup Linux Sekarang",
                        "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20order%20setup%20Linux"
                    },
                    {
                        "_key": "feat-linux",
                        "_type": "marketing_features",
                        "_version": 1,
                        "eyebrow": "Integrasi Klaster & Layanan",
                        "headline": "Dukungan Distro & Layanan Terkait",
                        "subheadline": "Dari laptop mahasiswa IT hingga server perusahaan di Surabaya & Sidoarjo.",
                        "columns": "3",
                        "features": [
                            {"icon": "code", "title": "Ubuntu & Debian LTS", "description": "Distro paling stabil untuk workstation riset, data science, dan web developer.", "link_url": "#wa-cta", "link_label": "Setup Ubuntu"},
                            {"icon": "gauge", "title": "Fedora & Arch Linux", "description": "Untuk pengguna yang menginginkan kernel bleeding-edge dan paket software mutakhir.", "link_url": "#wa-cta", "link_label": "Setup Fedora"},
                            {"icon": "database", "title": "Linux Server Production", "description": "Setup server on-premise, database server, dan deployment aplikasi custom [Software House Devk](/about).", "link_url": "/about", "link_label": "Solusi B2B"},
                            {"icon": "desktop", "title": "Dual-Boot Windows", "description": "Kombinasikan dengan [Jasa Install Ulang Windows](/jasa-install-ulang-windows-surabaya-sidoarjo) untuk fleksibilitas kerja.", "link_url": "/jasa-install-ulang-windows-surabaya-sidoarjo", "link_label": "Install Windows"},
                            {"icon": "wrench", "title": "Hardware Rakit PC Linux", "description": "Butuh rig server atau PC dev? Cek [Jasa Rakit PC Surabaya](/jasa-rakit-pc-surabaya-sidoarjo).", "link_url": "/jasa-rakit-pc-surabaya-sidoarjo", "link_label": "Rakit PC"},
                            {"icon": "shield", "title": "Hub Servis Komputer", "description": "Kembali ke [Hub Servis Komputer Surabaya-Sidoarjo](/jasa-install-komputer-surabaya-sidoarjo) untuk opsi lainnya.", "link_url": "/jasa-install-komputer-surabaya-sidoarjo", "link_label": "Hub Pilar 3"}
                        ]
                    },
                    {
                        "_key": "pricing-linux",
                        "_type": "marketing_pricing",
                        "_version": 1,
                        "anchor_id": "harga",
                        "headline": "Paket Biaya Setup Linux OS",
                        "plans": [
                            {
                                "name": "Distro Desktop Setup",
                                "price": "Rp 125.000",
                                "period": "/unit",
                                "description": "Instalasi distro Linux murni atau single OS",
                                "features": "Ubuntu / Debian / Linux Mint 64-bit\nDriver WiFi, Sound & Display Lengkap\nBrowser, LibreOffice, Media Player\nGaransi 14 Hari",
                                "cta_label": "Pilih Distro Desktop",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Distro%20Linux"
                            },
                            {
                                "name": "Dual-Boot + Developer Stack",
                                "price": "Rp 225.000",
                                "period": "/unit",
                                "description": "Paling populer untuk mahasiswa teknik & software engineer",
                                "features": "Dual-Boot Windows & Linux Aman (GRUB)\nDriver GPU NVIDIA / AMD Proprietary\nSetup Docker, Git, VS Code, Node/Python\nOptimasi Power Baterai (TLP / auto-cpufreq)\nGaransi 30 Hari Penuh",
                                "cta_label": "Pesan Paket Developer",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Developer%20Linux",
                                "highlighted": True,
                                "badge": "Paling Laris"
                            },
                            {
                                "name": "Linux Server & Hardening",
                                "price": "Rp 450.000",
                                "period": "/server",
                                "description": "Setup server kantor, sekolah, atau VPS cloud siap produksi",
                                "features": "Ubuntu/Debian Server Headless\nKonfigurasi SSH Key, Fail2Ban, Firewall UFW\nNginx Reverse Proxy & SSL Setup\nAutomated Database Backup Script\nGaransi 60 Hari & Bimbingan Teknis",
                                "cta_label": "Pilih Paket Server",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Server%20Linux"
                            }
                        ]
                    },
                    {
                        "_key": "wa-box-linux",
                        "_type": "marketing_whatsapp_cta",
                        "_version": 1,
                        "headline": "Siapkan Workstation Linux Tangguh Hari Ini",
                        "body": "Diskusikan kebutuhan distro dan software stack Anda bersama tim teknisi Linux Devk di Surabaya & Sidoarjo.",
                        "label": "Konsultasi Linux via WhatsApp",
                        "custom_message": "Halo Devk, saya ingin tanya jasa instalasi Linux ({title}). Apakah bisa dibantu hari ini?",
                        "variant": "card",
                        "anchor_id": "wa-cta"
                    },
                    {
                        "_key": "faq-linux",
                        "_type": "marketing_faq",
                        "_version": 1,
                        "headline": "FAQ Instalasi Linux Surabaya",
                        "subheadline": "Jawaban lengkap seputar dual-boot, hardware, dan dukungan driver Linux.",
                        "items": [
                            {"question": "Apakah instalasi dual-boot akan menghapus file di Windows saya?", "answer": "Tidak. Kami menyusutkan partisi Windows secara hati-hati untuk membuat ruang kosong bagi partisi Linux. Windows Anda tetap berjalan normal seperti biasa."},
                            {"question": "Laptop saya memakai GPU NVIDIA, apakah driver-nya bisa disetel di Linux?", "answer": "Bisa. Kami akan memasang driver proprietary NVIDIA resmi beserta CUDA toolkit dan optimasi Bumblebee / NVIDIA Prime switcher agar baterai tidak boros."},
                            {"question": "Apakah teknisi bisa dipanggil ke kos/rumah di wilayah Rungkut atau Sukolilo?", "answer": "Sangat bisa. Area kampus seperti ITS Keputih, UNAIR, UPN, UBAYA, dan sekitarnya merupakan rute harian teknisi panggilan kami."},
                            {"question": "Berapa lama estimasi pengerjaan setup dual-boot Linux?", "answer": "Proses partisi, instalasi OS, driver, dan developer stack biasanya memakan waktu sekitar 45 hingga 60 menit."}
                        ]
                    },
                    {
                        "_key": "cta-linux",
                        "_type": "marketing_cta",
                        "_version": 1,
                        "headline": "Maksimalkan Efisiensi Coding & Server Anda Bersama Devk",
                        "body": "Pengerjaan rapi, paham kernel Linux, bebas error GRUB, dan bergaransi resmi di Surabaya & Sidoarjo.",
                        "primary_cta_label": "Hubungi WhatsApp 085799520350",
                        "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20setup%20Linux",
                        "secondary_cta_label": "Hub Servis Komputer Surabaya",
                        "secondary_cta_url": "/jasa-install-komputer-surabaya-sidoarjo",
                        "image": {"id": linux_media_id}
                    }
                ]
            },
            "seo": {
                "title": "Jasa Install Linux OS & Server Surabaya | Devk",
                "description": "Jasa instalasi Linux Ubuntu, Debian, Fedora & konfigurasi server di Surabaya - Sidoarjo. Dual-boot, Docker, kernel tuning untuk developer & kantor. WA 085799520350.",
                "canonical": "https://devk.my.id/jasa-install-linux-surabaya",
                "image": "https://software.devk.my.id/_emdash/api/media/file/devk-linux-workstation-surabaya.jpg",
                "noIndex": False
            }
        },

        # =========================================================================
        # PAGE 4: Jasa Servis Laptop Panggilan Surabaya & Sidoarjo
        # =========================================================================
        {
            "collection": "pages",
            "slug": "jasa-servis-laptop-panggilan-surabaya-sidoarjo",
            "status": "published",
            "data": {
                "title": "Jasa Servis Laptop Panggilan Surabaya & Sidoarjo | Devk",
                "content": [
                    {
                        "_key": "hero-servis",
                        "_type": "marketing_hero",
                        "_version": 1,
                        "centered": False,
                        "eyebrow": "Teknisi Datang ke Rumah & Kantor",
                        "headline": "Jasa Servis Laptop Panggilan Surabaya & Sidoarjo — Cepat & Transparan",
                        "subheadline": "Laptop panas, berisik, mati total, atau lemot? Teknisi Devk datang langsung ke lokasi Anda. Deep cleaning fan, ganti pasta pendingin Arctic MX-4, upgrade SSD/RAM, dan perbaikan hardware di depan Anda.",
                        "primary_cta_label": "Panggil Teknisi via WhatsApp",
                        "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20butuh%20jasa%20servis%20laptop%20panggilan%20di%20Surabaya%20/%20Sidoarjo",
                        "secondary_cta_label": "Cek Biaya Layanan Servis",
                        "secondary_cta_url": "#harga",
                        "image": {"id": lap_media_id},
                        "image_caption": "Deep Cleaning & Repaste Laptop On-Site"
                    },
                    {
                        "_key": "steps-servis",
                        "_type": "marketing_steps",
                        "_version": 1,
                        "eyebrow": "Praktis Tanpa Macet",
                        "headline": "4 Alur Mudah Servis Laptop di Tempat Anda",
                        "subheadline": "Tidak perlu menitipkan laptop berhari-hari di toko yang tidak jelas keamanannya.",
                        "steps": [
                            {"step_number": "01", "title": "Hubungi WA & Konsultasi", "description": "Sampaikan merk laptop (Asus, Lenovo, Acer, HP, Dell, MacBook) dan gejala kerusakannya."},
                            {"step_number": "02", "title": "Teknisi Meluncur ke Lokasi", "description": "Teknisi datang ke alamat rumah, kos, atau kantor Anda di Surabaya & Sidoarjo sesuai jam janjian."},
                            {"step_number": "03", "title": "Pengerjaan Transparan di Depan Anda", "description": "Bongkar casing hati-hati, bersihkan debu kipas, ganti thermal paste premium, atau pasang sparepart baru."},
                            {"step_number": "04", "title": "Testing Suhu & Nota Garansi", "description": "Uji suhu dengan software benchmark. Suhu CPU/GPU turun drastis, serah terima nota garansi 30 hari."}
                        ]
                    },
                    {
                        "_key": "split-servis",
                        "_type": "marketing_split",
                        "_version": 1,
                        "eyebrow": "Bahaya Thermal Throttling",
                        "headline": "Mengapa Laptop Perlu Deep Cleaning & Ganti Thermal Paste?",
                        "body": "Pasta pendingin bawaan pabrik biasanya mengering setelah 1-2 tahun pemakaian. Ditambah tumpukan debu di sirip heatsink, panas prosesor terperangkap dan memicu fenomena thermal throttling (laptop tiba-tiba drop FPS saat gaming, kipas meraung kencang, atau mati mendadak). Pengerjaan deep cleaning kami menurunkan suhu hingga 15°C - 25°C seketika.",
                        "points": "Penggunaan Thermal Paste Grade Pro (Arctic MX-4 / Thermal Grizzly)\nPembersihan Total Debu Kipas & Sirip Heatsink Tembaga\nPengecekan Kinerja Baterai & Port Konektor\nPerpanjang Umur Motherboard dan Chipset GPU Laptop",
                        "image": {"id": lap_media_id},
                        "image_caption": "Perawatan Hardware Laptop Profesional",
                        "image_first": True,
                        "cta_label": "Cek Jadwal Kunjungan Teknisi",
                        "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20bisa%20cek%20jadwal%20teknisi%20panggilan?"
                    },
                    {
                        "_key": "comp-servis",
                        "_type": "marketing_comparison_table",
                        "_version": 1,
                        "eyebrow": "Jaminan Keamanan",
                        "headline": "Servis Panggilan Devk vs Bawa ke Toko Konvensional",
                        "subheadline": "Kenyamanan dan kepastian pengerjaan tanpa rasa was-was.",
                        "us_title": "Servis Panggilan Devk",
                        "competitor_title": "Toko Servis Komputer Biasa",
                        "rows": [
                            {"feature_name": "Pengerjaan Langsung di Depan Anda", "feature_desc": "Anda melihat langsung setiap baut dan komponen", "us_value": "yes", "competitor_value": "no (harus ditinggal berhari-hari)"},
                            {"feature_name": "Keamanan Komponen & Data Pribadi", "feature_desc": "Bebas risiko sparepart ditukar atau data diintip", "us_value": "yes", "competitor_value": "no"},
                            {"feature_name": "Thermal Paste Grade Profesional", "feature_desc": "Hanya menggunakan Arctic MX-4 asli bersertifikat", "us_value": "yes", "competitor_value": "no (sering pasta putih kiloan)"},
                            {"feature_name": "Garansi 30 Hari Tertulis Resmi", "feature_desc": "Klaim tanpa ribet", "us_value": "yes", "competitor_value": "no"}
                        ],
                        "cta_label": "Panggil Teknisi Sekarang",
                        "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20servis%20laptop%20panggilan"
                    },
                    {
                        "_key": "feat-servis",
                        "_type": "marketing_features",
                        "_version": 1,
                        "eyebrow": "Solusi Servis Terintegrasi",
                        "headline": "Layanan Kerusakan Hardware yang Kami Tangani",
                        "subheadline": "Mendukung laptop gaming (ROG, Legion, Predator, TUF), ultrabook tipis, hingga laptop kerja kantor.",
                        "columns": "3",
                        "features": [
                            {"icon": "thermometer", "title": "Overheat & Kipas Berisik", "description": "Deep cleaning total sirip pendingin dan repaste thermal compound premium.", "link_url": "#harga", "link_label": "Lihat Biaya"},
                            {"icon": "gauge", "title": "Upgrade SSD NVMe & RAM", "description": "Upgrade storage cepat agar boot 5 detik dan multitasking tanpa lag.", "link_url": "#harga", "link_label": "Lihat Biaya"},
                            {"icon": "desktop", "title": "Ganti Keyboard & Layar LCD", "description": "Penggantian sparepart keyboard macet, layar bergaris, atau engsel patah.", "link_url": "#wa-cta", "link_label": "Tanya Part"},
                            {"icon": "wrench", "title": "Install Ulang Windows Bersih", "description": "Kombinasikan dengan [Jasa Install Windows Surabaya](/jasa-install-ulang-windows-surabaya-sidoarjo) untuk performa maksimal.", "link_url": "/jasa-install-ulang-windows-surabaya-sidoarjo", "link_label": "Install Windows"},
                            {"icon": "cpu", "title": "Servis MacBook & iMac", "description": "Untuk pengguna perangkat Apple, kunjungi halaman [Jasa Install MacBook Surabaya](/jasa-install-macbook-imac-surabaya).", "link_url": "/jasa-install-macbook-imac-surabaya", "link_label": "Servis MacBook"},
                            {"icon": "building", "title": "Dua Workshop Fisik", "description": "Drop-off langsung di Tenggilis Mulya 76 Surabaya atau Graha Indraprasta G7/15 Sidoarjo.", "link_url": "/jasa-install-komputer-surabaya-sidoarjo", "link_label": "Cek Lokasi"}
                        ]
                    },
                    {
                        "_key": "pricing-servis",
                        "_type": "marketing_pricing",
                        "_version": 1,
                        "anchor_id": "harga",
                        "headline": "Estimasi Biaya Servis Laptop Panggilan",
                        "plans": [
                            {
                                "name": "Servis Ringan & Software",
                                "price": "Rp 120.000",
                                "period": "/unit",
                                "description": "Pembersihan virus, perbaikan driver & optimasi sistem lambat",
                                "features": "Pembersihan Malware & Startup Tuning\nPengecekan Kesehatan SSD/HDD\nUpdate Driver & Patch Keamanan\nGaransi 14 Hari",
                                "cta_label": "Pilih Servis Ringan",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Servis%20Ringan%20Laptop"
                            },
                            {
                                "name": "Deep Clean + Repaste MX-4",
                                "price": "Rp 180.000",
                                "period": "/unit",
                                "description": "Paket favorit pecinta gaming & pekerja berat! Laptop kembali dingin",
                                "features": "Bongkar Total Casing & Fan Cleaning\nThermal Paste Arctic MX-4 Grade Pro\nPembersihan Port USB & Keyboard\nBenchmark Tes Suhu CPU/GPU\nGaransi 30 Hari Penuh",
                                "cta_label": "Pesan Deep Clean",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Deep%20Clean%20Laptop",
                                "highlighted": True,
                                "badge": "Paling Laris"
                            },
                            {
                                "name": "Komplit Hardware + Install OS",
                                "price": "Rp 260.000",
                                "period": "/unit",
                                "description": "Penyegaran total hardware dan sistem operasi laptop",
                                "features": "Deep Cleaning & Repaste MX-4\nClean Install Windows 11/10 Pro\nPemasangan Upgrade SSD/RAM (jasa pasang free)\nFull Software Esensial & Office\nGaransi 45 Hari Penuh",
                                "cta_label": "Pilih Paket Komplit",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Paket%20Komplit%20Laptop"
                            }
                        ]
                    },
                    {
                        "_key": "wa-box-servis",
                        "_type": "marketing_whatsapp_cta",
                        "_version": 1,
                        "headline": "Laptop Bermasalah? Teknisi Meluncur ke Alamat Anda",
                        "body": "Layanan panggilan cepat mencakup Surabaya Barat, Timur, Selatan, Pusat, Utara, Waru, Gedangan, hingga Sidoarjo Kota.",
                        "label": "Panggil Teknisi Sekarang via WhatsApp",
                        "custom_message": "Halo Devk, saya mau panggil teknisi servis laptop ({title}) ke alamat saya. Apakah tersedia hari ini?",
                        "variant": "card",
                        "anchor_id": "wa-cta"
                    },
                    {
                        "_key": "faq-servis",
                        "_type": "marketing_faq",
                        "_version": 1,
                        "headline": "Pertanyaan Seputar Servis Laptop Panggilan",
                        "subheadline": "Informasi transparan mengenai teknisi panggilan dan keamanan pengerjaan.",
                        "items": [
                            {"question": "Apakah pengerjaan benar-benar dilakukan langsung di rumah saya?", "answer": "Ya, 100% pengerjaan servis seperti ganti thermal paste, pembersihan kipas, ganti LCD/keyboard, dan instalasi software dikerjakan langsung di depan Anda."},
                            {"question": "Berapa biaya ongkos transportasi teknisi ke lokasi saya?", "answer": "Untuk wilayah perkotaan Surabaya dan Sidoarjo, biaya kunjungan teknisi sangat terjangkau (Rp 20.000 - Rp 35.000 tergantung jarak) dan dikomunikasikan transparan di awal."},
                            {"question": "Merk laptop apa saja yang bisa ditangani?", "answer": "Kami menangani seluruh merk: Asus (ROG, TUF, ZenBook, VivoBook), Lenovo (Legion, ThinkPad, IdeaPad), Acer (Predator, Nitro, Swift), HP (Omen, Victus, Pavilion), Dell (Alienware, XPS), MSI, hingga Apple MacBook."},
                            {"question": "Bagaimana jika laptop saya mengalami kerusakan IC power di motherboard?", "answer": "Jika kerusakan membutuhkan solder mikroskopis BGA, teknisi akan memberikan tanda terima nota resmi untuk dibawa ke workshop laboratorium kami di Sidoarjo atau Surabaya."}
                        ]
                    },
                    {
                        "_key": "cta-servis",
                        "_type": "marketing_cta",
                        "_version": 1,
                        "headline": "Laptop Cepat Panas dan Lemot? Selesaikan Hari Ini",
                        "body": "Percayakan perawatan laptop Anda kepada teknisi berpengalaman Devk. Cepat, bersih, dingin, dan bergaransi resmi.",
                        "primary_cta_label": "Hubungi Teknisi WA 085799520350",
                        "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20butuh%20servis%20laptop",
                        "secondary_cta_label": "Lihat Jasa Rakit PC",
                        "secondary_cta_url": "/jasa-rakit-pc-surabaya-sidoarjo",
                        "image": {"id": lap_media_id}
                    }
                ]
            },
            "seo": {
                "title": "Jasa Servis Laptop Panggilan Surabaya & Sidoarjo | Devk",
                "description": "Jasa servis laptop panggilan datang ke rumah/kantor di Surabaya & Sidoarjo. Deep cleaning, ganti pasta thermal Arctic MX-4, perbaikan lambat & panas. WA 085799520350.",
                "canonical": "https://devk.my.id/jasa-servis-laptop-panggilan-surabaya-sidoarjo",
                "image": "https://software.devk.my.id/_emdash/api/media/file/devk-servis-laptop-panggilan.jpg",
                "noIndex": False
            }
        },

        # =========================================================================
        # PAGE 5: Jasa Rakit PC Surabaya - Sidoarjo
        # =========================================================================
        {
            "collection": "pages",
            "slug": "jasa-rakit-pc-surabaya-sidoarjo",
            "status": "published",
            "data": {
                "title": "Jasa Rakit PC Gaming & Workstation Surabaya - Sidoarjo | Devk",
                "content": [
                    {
                        "_key": "hero-pc",
                        "_type": "marketing_hero",
                        "_version": 1,
                        "centered": False,
                        "eyebrow": "Spesialis Gaming & 3D Workstation",
                        "headline": "Jasa Rakit PC Surabaya - Sidoarjo — Rapi, Dingin & Teruji Stabil",
                        "subheadline": "Konsultasi spek sesuai budget tanpa bottleneck, manajemen kabel presisi kelas pameran, tuning BIOS & XMP, serta uji stres benchmark AIDA64 / FurMark sebelum serah terima.",
                        "primary_cta_label": "Konsultasi Spek & Budget via WA",
                        "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20konsultasi%20rakit%20PC%20di%20Surabaya%20/%20Sidoarjo",
                        "secondary_cta_label": "Pilihan Paket Perakitan PC",
                        "secondary_cta_url": "#harga",
                        "image": {"id": pc_media_id},
                        "image_caption": "Custom PC Build & Cable Management"
                    },
                    {
                        "_key": "steps-pc",
                        "_type": "marketing_steps",
                        "_version": 1,
                        "eyebrow": "Proses Rapi & Terencana",
                        "headline": "4 Tahapan Membangun PC Impian Anda",
                        "subheadline": "Dari pemilihan komponen hingga kabel rapi dan performa maksimal.",
                        "steps": [
                            {"step_number": "01", "title": "Konsultasi Kebutuhan & Budget", "description": "Diskusikan tujuan penggunaan (Gaming 144Hz, Rendering 3D Lumion/Blender, Video Editing 4K, atau Office)."},
                            {"step_number": "02", "title": "Pemilihan Part Bergaransi Resmi", "description": "Komponen Anda yang sediakan sendiri atau kami bantu carikan dari distributor resmi dengan harga terbaik."},
                            {"step_number": "03", "title": "Perakitan & Manajemen Kabel Estetik", "description": "Pemasangan presisi, pasta pendingin premium, orientasi fan airflow optimal, dan cable routing rapi di belakang tray casing."},
                            {"step_number": "04", "title": "Tuning BIOS, Stres Tes & Garansi", "description": "Aktivasi XMP/EXPO RAM, tuning kurva kipas agar senyap, stres tes 2 jam bebas blue screen, dan nota garansi resmi."}
                        ]
                    },
                    {
                        "_key": "split-pc",
                        "_type": "marketing_split",
                        "_version": 1,
                        "eyebrow": "Standar Estetika & Airflow",
                        "headline": "Mengapa Cable Management & Airflow Sangat Menentukan Umur PC?",
                        "body": "Banyak PC rakitan toko asal sambung kabel sehingga menghalangi sirkulasi udara dingin dari intake fan ke kartu grafis dan prosesor. Akibatnya, suhu komponen melonjak dan memicu throttling. Di Devk, kami memperlakukan setiap rig PC bagaikan karya seni: jalur kabel disembunyikan rapi, thermal paste diaplikasikan presisi, dan tekanan udara (positive air pressure) diatur seimbang untuk mencegah debu masuk.",
                        "points": "Airflow Positif Seimbang: Suhu Prosesor & VGA Tetap Dingin\nManajemen Kabel Rapi Memaksimalkan Estetika Casing Tempered Glass\nPemasangan AIO Liquid Cooler Bebas Gelembung Udara\nTuning XMP RAM & Resizable BAR untuk Tambahan 10-15% FPS Gaming",
                        "image": {"id": pc_media_id},
                        "image_caption": "Perakitan PC Workstation Surabaya",
                        "image_first": True,
                        "cta_label": "Diskusikan Racikan Spek PC Anda",
                        "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20bisa%20bantu%20racik%20spek%20PC%20budget%20saya?"
                    },
                    {
                        "_key": "comp-pc",
                        "_type": "marketing_comparison_table",
                        "_version": 1,
                        "eyebrow": "Kualitas Perakitan",
                        "headline": "Rakit PC Devk vs Rakit Sendiri Tanpa Pengalaman",
                        "subheadline": "Hindari risiko pin soket motherboard bengkok atau kabel konslet.",
                        "us_title": "Jasa Rakit Profesional Devk",
                        "competitor_title": "Rakit Sendiri / Toko Grosir Biasa",
                        "rows": [
                            {"feature_name": "Manajemen Kabel Belakang Tray Rapi", "feature_desc": "Tiap kabel diikat velcro rapi tanpa kusut", "us_value": "yes", "competitor_value": "no (kabel sering disumpal sembarangan)"},
                            {"feature_name": "Tuning XMP & BIOS Optimal", "feature_desc": "Kecepatan RAM berjalan di frekuensi maksimal pabrik", "us_value": "yes", "competitor_value": "no (sering dibiarkan di default 2133MHz)"},
                            {"feature_name": "Stres Test Bebas Crash FurMark / AIDA64", "feature_desc": "Pengujian stabilitas daya PSU dan suhu", "us_value": "yes", "competitor_value": "no"},
                            {"feature_name": "Garansi Perakitan & Free Troubleshooting", "feature_desc": "Didampingi jika ada kendala pasca rakit", "us_value": "yes", "competitor_value": "no"}
                        ],
                        "cta_label": "Pesan Jasa Rakit Sekarang",
                        "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20pesan%20jasa%20rakit%20PC"
                    },
                    {
                        "_key": "feat-pc",
                        "_type": "marketing_features",
                        "_version": 1,
                        "eyebrow": "Integrasi Ekosistem Software & OS",
                        "headline": "Kategori PC yang Kami Bangun & Layanan Terkait",
                        "subheadline": "Selesai dirakit, PC langsung kami isi dengan OS dan software siap kerja sesuai kebutuhan Anda.",
                        "columns": "3",
                        "features": [
                            {"icon": "desktop", "title": "PC Gaming Kompetitif & AAA", "description": "Racikan optimal untuk eSports 240Hz dan game AAA 1440p / 4K ray-tracing.", "link_url": "#harga", "link_label": "Lihat Paket"},
                            {"icon": "cpu", "title": "Workstation Arsitektur & 3D", "description": "Siap rendering berat dengan dukungan [Lumion](/jasa-install-lumion-online), [3ds Max](/jasa-install-3ds-max-online) & [Blender](/jasa-install-blender-online).", "link_url": "/jasa-install-lumion-online", "link_label": "Software 3D"},
                            {"icon": "chart", "title": "PC Office & Bisnis POS", "description": "Hemat daya, tahan banting 24 jam untuk toko dan kantor. Terhubung dengan [Aplikasi POS Kasir Devk](/about).", "link_url": "/about", "link_label": "Software POS"},
                            {"icon": "wrench", "title": "Install Ulang Windows Pro", "description": "Semua PC rakitan siap dilengkapi [Install Ulang Windows](/jasa-install-ulang-windows-surabaya-sidoarjo) resmi bebas bloatware.", "link_url": "/jasa-install-ulang-windows-surabaya-sidoarjo", "link_label": "Install Windows"},
                            {"icon": "thermometer", "title": "Perawatan & Deep Clean", "description": "Jadwalkan pembersihan rutin via [Servis Laptop & PC Panggilan](/jasa-servis-laptop-panggilan-surabaya-sidoarjo).", "link_url": "/jasa-servis-laptop-panggilan-surabaya-sidoarjo", "link_label": "Servis PC"},
                            {"icon": "building", "title": "Hub Servis Surabaya-Sidoarjo", "description": "Kembali ke pusat informasi [Hub Servis Komputer](/jasa-install-komputer-surabaya-sidoarjo) untuk rincian workshop kami.", "link_url": "/jasa-install-komputer-surabaya-sidoarjo", "link_label": "Hub Pilar 3"}
                        ]
                    },
                    {
                        "_key": "pricing-pc",
                        "_type": "marketing_pricing",
                        "_version": 1,
                        "anchor_id": "harga",
                        "headline": "Pilihan Paket Biaya Jasa Rakit PC",
                        "plans": [
                            {
                                "name": "Rakit PC Office / Budget",
                                "price": "Rp 150.000",
                                "period": "/unit",
                                "description": "Untuk kebutuhan komputer kasir, kantor, atau PC belajar daring",
                                "features": "Perakitan Komponen Motherboard, CPU & RAM\nManajemen Kabel Standar Rapi\nUpdate BIOS & Aktivasi XMP\nGaransi Perakitan 14 Hari",
                                "cta_label": "Pilih Rakit Office",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Rakit%20PC%20Office"
                            },
                            {
                                "name": "Rakit PC Gaming & Airflow Tuning",
                                "price": "Rp 250.000",
                                "period": "/unit",
                                "description": "Paling populer untuk PC gaming dual-chamber & casing RGB",
                                "features": "Perakitan Komplit + AIO Liquid Cooler\nManajemen Kabel Kelas Kontes (Velcro Binding)\nTuning BIOS, Fan Curve & Resizable BAR\nStres Test Suhu 2 Jam Bebas Crash\nGaransi Perakitan 30 Hari Penuh",
                                "cta_label": "Pesan Rakit Gaming",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Rakit%20PC%20Gaming",
                                "highlighted": True,
                                "badge": "Paling Laris"
                            },
                            {
                                "name": "Custom Workstation / Multi-GPU",
                                "price": "Rp 400.000",
                                "period": "/unit",
                                "description": "Untuk rig server AI, render farm, dan PC dual processor / multi-GPU",
                                "features": "Perakitan Rig Kompleks & Custom Loop/Multi-Fan\nKonfigurasi Storage RAID / PCIe Gen 5 SSD\nSetup Dual-OS (Windows & Linux CUDA)\nBenchmark Render 3D & Stress Test Maksimal\nGaransi Perakitan 60 Hari & Pendampingan",
                                "cta_label": "Pilih Custom Workstation",
                                "cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20pesan%20Rakit%20Workstation"
                            }
                        ]
                    },
                    {
                        "_key": "wa-box-pc",
                        "_type": "marketing_whatsapp_cta",
                        "_version": 1,
                        "headline": "Sudah Punya Part atau Ingin Konsultasi Budget Dulu?",
                        "body": "Teknisi rakit PC Devk siap merekomendasikan racikan komponen terbaik yang seimbang, hemat budget, dan tahan pakai bertahun-tahun.",
                        "label": "Konsultasi Rakit PC via WhatsApp",
                        "custom_message": "Halo Devk, saya mau rakit PC ({title}). Budget saya sekitar Rp... Apakah bisa bantu rekomendasi part?",
                        "variant": "card",
                        "anchor_id": "wa-cta"
                    },
                    {
                        "_key": "faq-pc",
                        "_type": "marketing_faq",
                        "_version": 1,
                        "headline": "FAQ Jasa Rakit PC Surabaya & Sidoarjo",
                        "subheadline": "Semua yang perlu Anda ketahui sebelum merakit komputer bersama Devk.",
                        "items": [
                            {"question": "Apakah saya boleh membeli komponennya sendiri dari toko online?", "answer": "Boleh sekali. Anda bebas membeli part dari e-commerce (Tokopedia/Shopee) atau toko offline favorit Anda. Teknisi kami akan datang merakit atau Anda bawa seluruh kotak komponen ke workshop kami."},
                            {"question": "Apakah Devk bisa bantu carikan part jika saya tidak mau pusing?", "answer": "Bisa. Kami memiliki jaringan toko distributor resmi di Surabaya (THR Mall, Hitech Mall, dsb) untuk mendapatkan harga part terbaik dengan garansi resmi distributor Indonesia (distro resmi 3-5 tahun)."},
                            {"question": "Apakah jasa rakit sudah termasuk instalasi Windows dan game/software?", "answer": "Paket rakit sudah mencakup instalasi sistem operasi Windows 11 Pro trial untuk pengujian benchmark. Anda dapat menambahkan paket software komplit atau software arsitektur/editing dengan harga khusus bundle."},
                            {"question": "Berapa lama proses merakit PC sampai siap digunakan?", "answer": "Perakitan standar beserta cable management estetik dan stres tes memakan waktu sekitar 2 hingga 3 jam di workshop kami."}
                        ]
                    },
                    {
                        "_key": "cta-pc",
                        "_type": "marketing_cta",
                        "_version": 1,
                        "headline": "Bangun PC Impian Anda Bersama Teknisi Berpengalaman Devk",
                        "body": "Manajemen kabel rapi, suhu dingin, performa optimal, dan kepuasan terjamin di Surabaya & Sidoarjo.",
                        "primary_cta_label": "Hubungi WhatsApp 085799520350",
                        "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20rakit%20PC",
                        "secondary_cta_label": "Katalog Software Desain & 3D",
                        "secondary_cta_url": "/jasa-install-software-online",
                        "image": {"id": pc_media_id}
                    }
                ]
            },
            "seo": {
                "title": "Jasa Rakit PC Gaming & Workstation Surabaya - Sidoarjo | Devk",
                "description": "Jasa rakit PC gaming & rendering workstation di Surabaya & Sidoarjo. Manajemen kabel rapi, konsultasi spek, tuning BIOS/XMP, bergaransi. WA 085799520350.",
                "canonical": "https://devk.my.id/jasa-rakit-pc-surabaya-sidoarjo",
                "image": "https://software.devk.my.id/_emdash/api/media/file/devk-rakit-pc-surabaya.jpg",
                "noIndex": False
            }
        }
    ]

    for p in pages:
        slug = p["slug"]
        print(f"Creating page: {slug}...")
        res = call_mcp("content_create", p)
        print(f"Result for {slug}: {res}")

if __name__ == "__main__":
    build_pilar3_pages()
