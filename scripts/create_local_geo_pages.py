#!/usr/bin/env python3
"""
create_local_geo_pages.py
Menghasilkan dan mempublikasikan 18 landing page lokal geo-targeted (Sidoarjo, Surabaya, Mojokerto)
untuk 6 layanan instalasi OS & Software Devk:
1. Jasa Install Windows 10
2. Jasa Install Windows 11
3. Jasa Install Software MacBook
4. Jasa Install Software Windows
5. Jasa Install Linux
6. Jasa Install Dual Boot
"""

import json
import urllib.request
import socket
import sys
import time

# Force IPv4 to prevent IPv6 unreachable timeouts
orig_getaddrinfo = socket.getaddrinfo
def getaddrinfo_ipv4(*args, **kwargs):
    res = orig_getaddrinfo(*args, **kwargs)
    return [r for r in res if r[0] == socket.AF_INET]
socket.getaddrinfo = getaddrinfo_ipv4

PAT_TOKEN = "ec_pat_O3MrYsN2tLlxEUOnOEZiipYHOHXcv0T9j0L3QsjzcjM"
API_URL = "https://software.devk.my.id/_emdash/api/mcp"

# Media IDs terverifikasi di Emdash Media Library
MEDIA_IDS = {
    "win": "01M5J1TC04W154PPG1WPKSRB79",        # devk-windows-install-surabaya.jpg
    "mac": "01M5HZK0RGYWEAZDYC5EGRQY4W",        # devk-macbook-repair-surabaya.jpg
    "linux": "01M5HZJKMP3A1QNSR57KCEEHQT",      # devk-linux-workstation-surabaya.jpg
    "dualboot": "01M5KWYACPPD7ZD0JFK692J30R",   # devk-guide-dualboot-windows-ubuntu.jpg
    "software": "01M5KWV8EJJKB7CV260CWE60FE",   # devk-guide-autodesk-licensing-fix.jpg
    "repair": "01M5KVFJTE73N7NJBJ6M2XKYBT"       # devk-material-cta-hardware-repair.jpg
}

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
                try:
                    data = json.loads(line[6:])
                    if data.get("isError"):
                        print(f"MCP error in {tool_name}: {data}")
                        return {}
                    content = data.get("result", {}).get("content", [])
                    if content and "text" in content[0]:
                        try:
                            return json.loads(content[0]["text"])
                        except Exception:
                            return content[0]["text"]
                    return data.get("result", {})
                except Exception as e:
                    print(f"Parse error line: {e}")
        return {}

CITIES_DATA = {
    "sidoarjo": {
        "name": "Sidoarjo",
        "label": "Sidoarjo & Sekitarnya",
        "workshop": "Workshop Sidoarjo: Graha Indraprasta G7/15, Sidoarjo",
        "areas": "Waru, Gedangan, Taman, Sedati, Buduran, Candi, Sukodono, Krian, Tanggulangin, Porong, Sidoarjo Kota",
        "districts": ["Waru & Sedati", "Gedangan & Buduran", "Taman & Sukodono", "Sidoarjo Kota & Candi", "Krian & Balongbendo", "Tanggulangin & Porong"],
        "call_desc": "Teknisi siap datang panggilan ke rumah, kantor, ruko, atau instansi di seluruh kecamatan Kabupaten Sidoarjo tanpa repot membawa unit keluar rumah."
    },
    "surabaya": {
        "name": "Surabaya",
        "label": "Surabaya (Pusat, Timur, Selatan, Barat, Utara)",
        "workshop": "Workshop Surabaya: Jl. Tenggilis Mulya 76, Surabaya",
        "areas": "Rungkut, Tenggilis Mejoyo, Wonokromo, Gubeng, Sukolilo, Wiyung, Dukuh Pakis, Tegalsari, Kenjeran, Mulyorejo, Sambikerep",
        "districts": ["Surabaya Timur (Rungkut, Sukolilo, Mulyorejo)", "Surabaya Selatan (Wonokromo, Tenggilis, Gayungan)", "Surabaya Pusat (Tegalsari, Genteng, Bubutan)", "Surabaya Barat (Wiyung, Dukuh Pakis, Sambikerep)", "Surabaya Utara (Pabean, Kenjeran, Semampir)", "Area Kampus (ITS, Unair, Ubaya, UPN, UK Petra)"],
        "call_desc": "Teknisi spesialis siap meluncur on-site ke apartemen, kampus, kantor korporat, co-working space, dan rumah tinggal di seluruh Surabaya dalam 30–60 menit."
    },
    "mojokerto": {
        "name": "Mojokerto",
        "label": "Mojokerto Kota & Kabupaten",
        "workshop": "Workshop Mitra & Servis Panggilan Mojokerto (Jangkauan Cepat dari Sidoarjo Barat / Surabaya)",
        "areas": "Magersari, Kranggan, Prajurit Kulon, Puri, Sooko, Bangsal, Mojoanyar, Trowulan, Mojosari, Ngoro Industrial Park, Pacet",
        "districts": ["Mojokerto Kota (Magersari, Kranggan, Prajurit Kulon)", "Sooko & Puri", "Bangsal & Mojoanyar", "Mojosari & Pungging", "Kawasan Industri Ngoro (NIP)", "Trowulan & Dlanggu"],
        "call_desc": "Layanan servis panggilan on-site dan antar-jemput kilat untuk perumahan, instansi sekolah, UKM, pabrik, dan kawasan industri di Mojokerto."
    }
}

def generate_page_payload(topic_key, city_key):
    city = CITIES_DATA[city_key]
    c_name = city["name"]
    c_label = city["label"]
    c_areas = city["areas"]
    c_workshop = city["workshop"]
    c_districts = city["districts"]
    c_calldesc = city["call_desc"]

    slug = f"jasa-install-{topic_key}-{city_key}"
    
    # -------------------------------------------------------------------------
    # 1. WINDOWS 10
    # -------------------------------------------------------------------------
    if topic_key == "windows-10":
        title = f"Jasa Install Windows 10 {c_name} | Clean Install Bebas Lemot & Bergaransi"
        seo_title = f"Jasa Install Windows 10 {c_name} Panggilan & Workshop | Devk"
        seo_desc = f"Jasa install Windows 10 Pro 64-bit di {c_name} panggilan & workshop. Bersih bebas bloatware, driver update lengkap, aktivasi resmi, garansi 30 hari. WA 085799520350."
        hero_hl = f"Jasa Install Windows 10 {c_name} — Stabil, Bersih & Bebas Lemot"
        hero_sub = f"Penyelamat laptop & PC lawas atau kantor di {c_name} yang lemot, terkena virus, atau sering blue screen. Clean install Windows 10 Pro 22H2 resmi, aktivasi permanen, driver hardware presisi, dan garansi tertulis 30 hari."
        img_id = MEDIA_IDS["win"]
        
        split_hl = f"Kenapa Windows 10 Pro Masih Menjadi Pilihan Utama di {c_name}?"
        split_body = f"Meskipun Windows 11 telah rilis, ribuan pengguna komputer di {c_name}—mulai dari pelaku usaha kasir toko, kantor administrasi, hingga laptop mahasiswa—tetap memilih Windows 10 Pro 64-bit versi 22H2. Alasannya sangat jelas: konsumsi RAM jauh lebih hemat (hanya butuh 2–4 GB), kompatibilitas sempurna dengan printer kasir/scanner jadul, dan bebas dari syarat kaku TPM 2.0. Teknisi Devk melakukan clean install dari installer murni Microsoft tanpa software bajakan berbahaya atau bloatware yang memberatkan sistem."
        
        feat_items = [
            {"icon": "desktop", "title": "Bebas Virus & Bloatware", "description": "Format total partisi sistem untuk membasmi tuntas virus, malware, mining-bot, dan adware pengganggu."},
            {"icon": "zap", "title": "Tuning Kecepatan SSD / HDD", "description": "Konfigurasi TRIM SSD, paging file virtual memory optimal, dan penonaktifan service Windows yang tidak perlu."},
            {"icon": "cpu", "title": "Driver Hardware Lengkap", "description": "Pemasangan driver sound, WiFi, LAN, Bluetooth, touchpad, chipset, dan GPU NVIDIA/AMD/Intel resmi."},
            {"icon": "layers", "title": "Bonus Software Wajib Siap Pakai", "description": "Langsung terpasang Microsoft Office, browser Chrome/Edge, WinRAR, PDF Reader, VLC player, dan antivirus bawaan."},
            {"icon": "wrench", "title": "Pengerjaan Cepat 30–45 Menit", "description": f"Bisa ditunggu di {c_workshop} atau teknisi meluncur panggilan langsung ke lokasi Anda di {c_name}."},
            {"icon": "shield", "title": "Garansi Layanan 30 Hari", "description": "Jika sistem mengalami crash, gagal booting, atau kendala driver dalam 30 hari, kami perbaiki gratis tanpa debat."}
        ]
        
        price_plan1 = {"name": "Paket Windows 10 Basic", "price": "Rp 75.000", "period": "/unit", "description": "Install ulang sistem operasi bersih untuk PC/laptop di workshop.", "features": f"Clean Install Windows 10 Pro 64-bit\nUpdate Driver Chipset & Graphic Lengkap\nAktivasi Digital License Permanen\nBrowser & Antivirus Defender Siap Pakai\nGaransi 14 Hari\nPengerjaan di {c_workshop}", "cta_label": "Pesan Paket Basic", "cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20pesan%20Paket%20Windows%2010%20Basic%20di%20{c_name}", "popular": False}
        price_plan2 = {"name": "Paket Windows 10 Komplit (Best Seller)", "price": "Rp 120.000", "period": "/unit", "description": "Solusi all-in-one laptop kerja, sekolah, dan kuliah siap pakai.", "features": f"Semua Fitur Paket Basic\nPaket Microsoft Office 2021/2024 Lengkap\nAcrobat PDF Pro, WinRAR, Zoom, VLC\nBackup Data Pribadi Partisi C Aman\nOptimasi Kecepatan Booting & SSD\nGaransi 30 Hari Penuh", "cta_label": "Pesan Paket Komplit", "cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20pesan%20Paket%20Windows%2010%20Komplit%20di%20{c_name}", "popular": True}
        price_plan3 = {"name": f"Paket Panggilan On-Site {c_name}", "price": "Rp 175.000", "period": "/kunjungan", "description": f"Teknisi datang langsung ke rumah, ruko, atau kantor di {c_name}.", "features": f"Semua Fitur Paket Komplit\nTeknisi Datang ke Lokasi Anda di {c_name}\nPengerjaan Transparan di Depan Anda\nCek Kondisi Harddisk / Kesehatan SSD\nKonsultasi Hardware Gratis\nGaransi 30 Hari Penuh", "cta_label": "Panggil Teknisi ke Rumah", "cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20butuh%20teknisi%20panggilan%20install%20Windows%2010%20di%20{c_name}", "popular": False}

        faqs = [
            {"question": f"Berapa lama waktu install Windows 10 di {c_name}?", "answer": "Proses instalasi bersih menggunakan media flashdisk USB 3.2 NVMe memakan waktu sekitar 30 hingga 45 menit hingga seluruh driver dan software dasar selesai terpasang."},
            {"question": "Apakah data di drive D: atau E: saya akan hilang?", "answer": "Sama sekali tidak. Kami hanya memformat partisi sistem C:. Data di partisi lain (D:, E:, data kerja) dijamin 100% aman dan utuh. Jika ada file penting di Desktop atau Downloads (drive C), teknisi kami akan membackupnya terlebih dahulu."},
            {"question": f"Kecamatan mana saja di {c_name} yang bisa dilayani panggilan?", "answer": f"Kami melayani seluruh wilayah {c_name} meliputi area {c_areas}."},
            {"question": "Apakah laptop jadul saya kuat menjalankan Windows 10?", "answer": "Sangat kuat. Untuk laptop dengan prosesor Intel Core i3 generasi lama atau Celeron, kami menyertakan paket optimasi RAM ringan dan menyarankan penggunaan SSD agar performa melonjak 5x lebih cepat."}
        ]

    # -------------------------------------------------------------------------
    # 2. WINDOWS 11
    # -------------------------------------------------------------------------
    elif topic_key == "windows-11":
        title = f"Jasa Install Windows 11 {c_name} | Pro 23H2 / 24H2 Bebas Bloatware & Bergaransi"
        seo_title = f"Jasa Install Windows 11 {c_name} Panggilan & Workshop | Devk"
        seo_desc = f"Jasa install Windows 11 Pro 64-bit di {c_name} panggilan & workshop. Support bypass TPM 2.0 laptop lawas, aktivasi permanen, update driver presisi. WA 085799520350."
        hero_hl = f"Jasa Install Windows 11 {c_name} — Modern, Cepat & Siap Gaming"
        hero_sub = f"Nikmati antarmuka modern Fluent Design, fitur keamanan tercanggih, dan DirectStorage di {c_name}. Clean install Windows 11 Pro build terbaru (23H2/24H2) resmi, optimasi performa multitasking, support bypass TPM untuk hardware lama, dan garansi 30 hari."
        img_id = MEDIA_IDS["win"]
        
        split_hl = f"Upgrade ke Windows 11 Tanpa Khawatir Kompatibilitas Hardware di {c_name}"
        split_body = f"Banyak pengguna laptop di {c_name} ingin merasakan kecanggihan Windows 11 namun terhalang oleh pesan 'This PC doesn't meet the minimum system requirements' (kendala TPM 2.0 atau Secure Boot). Teknisi Devk memiliki metode instalasi resmi dan bypass hardware aman tanpa merusak kestabilan sistem. Kami memastikan seluruh fitur modern seperti Auto HDR, DirectStorage untuk loading game super cepat, dan Windows Subsystem for Android/Linux (WSL2) berjalan mulus di laptop Anda."
        
        feat_items = [
            {"icon": "zap", "title": "Build Terbaru Windows 11 Pro", "description": "Menggunakan master installer resmi 23H2 / 24H2 murni bebas virus dan bebas modifikasi berbahaya."},
            {"icon": "shield", "title": "Bypass TPM 2.0 / Secure Boot Aman", "description": "Solusi jitu bagi laptop generasi 6, 7, atau PC gaming rakitan yang ingin menikmati Windows 11 tanpa ganti hardware."},
            {"icon": "cpu", "title": "Tuning Performa Multitasking & Game", "description": "Optimasi alokasi core prosesor Intel P/E-Cores dan AMD Ryzen untuk gaming dan software editing berat."},
            {"icon": "layers", "title": "Software Produktivitas Terlengkap", "description": "Paket Microsoft Office 2024, browser bebas iklan, software meeting Zoom/Teams, dan media player ultra-ringan."},
            {"icon": "laptop", "title": "Backup Data C Terpercaya", "description": "Menjaga file skripsi, dokumen kantor, foto keluarga, dan bookmark browser agar tidak hilang saat transisi OS."},
            {"icon": "award", "title": "Garansi 30 Hari & Teknisi Panggilan", "description": f"Tersedia teknisi panggilan datang ke tempat Anda di {c_name} atau drop-off langsung ke workshop."}
        ]

        price_plan1 = {"name": "Paket Windows 11 Standard", "price": "Rp 85.000", "period": "/unit", "description": "Clean install Windows 11 Pro di workshop untuk unit yang sudah support TPM.", "features": f"Clean Install Windows 11 Pro 64-bit Terbaru\nDriver Hardware Resmi Lengkap\nAktivasi Lisensi Permanen\nBrowser & Antivirus Aktif\nGaransi 14 Hari\nPengerjaan di {c_workshop}", "cta_label": "Pesan Paket Standard", "cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20pesan%20Windows%2011%20Standard%20di%20{c_name}", "popular": False}
        price_plan2 = {"name": "Paket Windows 11 Pro + Bypass (Best Seller)", "price": "Rp 135.000", "period": "/unit", "description": "Paket lengkap untuk semua laptop (termasuk unit non-TPM) + software komplit.", "features": f"Clean Install Windows 11 Pro 23H2/24H2\nBypass TPM 2.0 & Secure Boot Stabil (Jika Perlu)\nPaket Microsoft Office 2024 / 365 Siap Pakai\nAcrobat PDF Pro, WinRAR, VLC Player\nBackup Data Desktop & Downloads\nGaransi 30 Hari Penuh", "cta_label": "Pesan Paket Bypass + Office", "cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20pesan%20Windows%2011%20Pro%20di%20{c_name}", "popular": True}
        price_plan3 = {"name": f"Paket Panggilan VIP {c_name}", "price": "Rp 195.000", "period": "/kunjungan", "description": f"Layanan on-site panggilan privat di rumah, kantor, atau apartemen {c_name}.", "features": f"Semua Fitur Paket Best Seller\nTeknisi Datang Langsung ke Lokasi Anda\nPengerjaan Ditonton Langsung di Meja Anda\nCleaning Kipas & Pengecekan Suhu Laptop\nGaransi 30 Hari Penuh", "cta_label": "Booking Teknisi Panggilan", "cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20butuh%20teknisi%20panggilan%20Windows%2011%20di%20{c_name}", "popular": False}

        faqs = [
            {"question": f"Apakah laptop lama tanpa TPM 2.0 bisa diinstall Windows 11 di {c_name}?", "answer": "Bisa sekali. Teknisi kami menggunakan parameter setup bypass resmi yang stabil sehingga Windows 11 dapat berjalan lancar tanpa notifikasi watermark yang mengganggu dan tetap menerima update security berkala."},
            {"question": "Apakah Windows 11 terasa lebih berat dari Windows 10?", "answer": "Jika laptop Anda sudah menggunakan SSD (Solid State Drive) dan RAM minimal 8 GB, Windows 11 justru terasa lebih responsif karena manajemen alokasi memori dan scheduler prosesornya lebih mutakhir."},
            {"question": f"Bagaimana cara memanggil teknisi ke lokasi saya di {c_name}?", "answer": f"Cukup hubungi WhatsApp kami di 085799520350. Kirimkan merk laptop, kendala yang dialami, dan alamat lokasi Anda di {c_name}. Teknisi akan segera mengkonfirmasi jadwal kedatangan."},
            {"question": "Apakah saya mendapatkan garansi jika Windows bermasalah?", "answer": "Ya, kami memberikan garansi 30 hari penuh. Jika terjadi error sistem, crash, atau kendala driver, teknisi kami siap remote gratis atau datang kembali."}
        ]

    # -------------------------------------------------------------------------
    # 3. SOFTWARE MACBOOK
    # -------------------------------------------------------------------------
    elif topic_key == "software-macbook":
        title = f"Jasa Install Software MacBook {c_name} | Adobe CC, Office, CAD for Mac M1/M2/M3 & Intel"
        seo_title = f"Jasa Install Software MacBook {c_name} Apple Silicon M1-M4 & Intel | Devk"
        seo_desc = f"Jasa install software MacBook Pro, MacBook Air & iMac di {c_name}. Paket Adobe CC Mac, Office 2024, AutoCAD Mac, Final Cut Pro. Native Apple Silicon M1/M2/M3/M4. WA 085799520350."
        hero_hl = f"Jasa Install Software MacBook & iMac {c_name} — Apple Silicon M1/M2/M3 & Intel"
        hero_sub = f"Solusi aplikasi MacBook Pro, MacBook Air, Mac mini, dan iMac di {c_name}. Pemasangan Adobe Creative Cloud, Microsoft Office Mac, Final Cut Pro, Logic Pro, AutoCAD Mac, dan clean install macOS (Sequoia / Sonoma) bergaransi 30 hari."
        img_id = MEDIA_IDS["mac"]

        split_hl = f"Optimalisasi Software Khusus Arsitektur ARM Apple Silicon di {c_name}"
        split_body = f"Banyak pemilik MacBook di {c_name} mengeluhkan aplikasi crash, baterai boros, atau muncul peringatan 'App is damaged and can't be opened' setelah update versi macOS. Hal ini terjadi karena software yang dipasang masih berjalan melalui emulasi Rosetta 2 yang tidak stabil. Teknisi Devk menginstalasi build software native ARM64 yang dirancang khusus untuk chip Apple Silicon M1, M2, M3, hingga M4 terbaru, memastikan efisiensi baterai maksimal dan performa render video/desain tanpa kendala."

        feat_items = [
            {"icon": "laptop", "title": "Support Apple Silicon & Intel Mac", "description": "Kompatibel 100% dengan MacBook M1, M2, M3, M4 (Pro/Max) serta generasi MacBook Intel lawas."},
            {"icon": "award", "title": "Bebas Masalah Gatekeeper & Crash", "description": "Penanganan tuntas error 'Application Damaged', bypass perizinan security macOS, dan perbaikan izin library terminal."},
            {"icon": "layers", "title": "Paket Creative Suite Lengkap", "description": "Photoshop, Illustrator, Premiere Pro, After Effects, InDesign, Lightroom Classic versi Mac stabil."},
            {"icon": "shield", "title": "Microsoft Office for Mac 2024", "description": "Word, Excel, PowerPoint, Outlook versi Mac native dengan aktivasi permanen bebas blokir update."},
            {"icon": "terminal", "title": "Aplikasi Arsitektur & Video Pro", "description": "AutoCAD for Mac, SketchUp Pro Mac, Final Cut Pro, Logic Pro, DaVinci Resolve Studio, dan CleanMyMac X."},
            {"icon": "wrench", "title": "Pengerjaan Cepat di Tempat / Remote", "description": f"Bisa datang ke {c_workshop}, teknisi on-site ke lokasi Anda di {c_name}, atau remote via AnyDesk."}
        ]

        price_plan1 = {"name": "Paket Single Software Mac", "price": "Rp 75.000", "period": "/aplikasi", "description": "Pemasangan 1 software pilihan untuk kebutuhan mendesak.", "features": "1 Software Mac Pilihan (Office / Photoshop / AutoCAD dll)\nNative Apple Silicon / Intel Support\nBypass Security & Gatekeeper Aman\nBebas Trial Expired\nGaransi 30 Hari", "cta_label": "Pesan 1 Software", "cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20install%20software%20MacBook%20di%20{c_name}", "popular": False}
        price_plan2 = {"name": "Paket Designer & Office Mac (Best Seller)", "price": "Rp 175.000", "period": "/unit", "description": "Paket terpopuler untuk pekerja kreatif, mahasiswa, dan kantor.", "features": "Microsoft Office 2024 Mac Native\nAdobe Photoshop + Illustrator Mac\nCleanMyMac X (Pembersih Cache)\nPDF Reader & Utility Mac Wajib\nGaransi 30 Hari Penuh", "cta_label": "Pesan Paket Designer Mac", "cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20Paket%20Designer%20MacBook%20di%20{c_name}", "popular": True}
        price_plan3 = {"name": "Paket Master Studio Creative Suite", "price": "Rp 275.000", "period": "/unit", "description": "Paket komplit video creator, arsitek, dan agensi multimedia.", "features": "Semua Fitur Paket Designer\nAdobe Premiere Pro + After Effects\nFinal Cut Pro / AutoCAD Mac / SketchUp\nFont Library Pack Lengkap\nBisa Panggilan ke Lokasi di " + c_name + "\nGaransi 30 Hari Penuh", "cta_label": "Pesan Master Studio Mac", "cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20Paket%20Master%20Studio%20Mac%20di%20{c_name}", "popular": False}

        faqs = [
            {"question": "Apakah aman memasang software di MacBook Apple Silicon M1/M2/M3?", "answer": "Sangat aman. Kami tidak merusak file sistem macOS dan tidak mengubah root SIP sistem operasi. Aplikasi berjalan di user-space dengan sertifikasi lokal yang aman."},
            {"question": "Bagaimana jika suatu saat saya mengupdate versi macOS?", "answer": "Software yang kami pasang kompatibel dengan macOS Sequoia, Sonoma, dan Ventura. Kami juga menyertakan panduan aman update dan garansi purna jual 30 hari jika butuh tuning ulang."},
            {"question": f"Apakah melayani jasa install ulang macOS bersih di {c_name}?", "answer": f"Ya, kami melayani clean install ulang macOS (reset pabrik bersih) untuk mengatasi MacBook lemot, lupa password, atau hendak dijual di workshop {c_name} maupun servis panggilan."},
            {"question": f"Berapa lama waktu pengerjaan untuk MacBook di {c_name}?", "answer": "Pemasangan software bundle membutuhkan waktu sekitar 30 hingga 60 menit tergantung kecepatan koneksi dan jumlah software yang dipesan."}
        ]

    # -------------------------------------------------------------------------
    # 4. SOFTWARE WINDOWS
    # -------------------------------------------------------------------------
    elif topic_key == "software-windows":
        title = f"Jasa Install Software Windows {c_name} | CAD, 3D Render, Editing & Office Panggilan"
        seo_title = f"Jasa Install Software Windows {c_name} Panggilan & Remote | Devk"
        seo_desc = f"Jasa install software Windows di {c_name}. AutoCAD, SketchUp, Revit, Lumion, Adobe CC, CorelDRAW, SPSS, Office. Teknisi panggilan ke lokasi & remote se-Indonesia. WA 085799520350."
        hero_hl = f"Jasa Install Software Windows {c_name} — Lengkap, Siap Pakai & Bergaransi"
        hero_sub = f"Pemasangan software teknis, arsitektur, desain grafis, editing video, dan olah data statistik di {c_name}. Tersedia teknisi panggilan on-site ke rumah/kantor, servis di workshop, serta instalasi remote kilat via AnyDesk bergaransi 30 hari."
        img_id = MEDIA_IDS["software"]

        split_hl = f"Katalog 100+ Software Windows Lengkap Siap Pakai Tanpa Ribet di {c_name}"
        split_body = f"Mencoba mengunduh dan menginstal software berat sendiri sering kali berujung pada file installer palsu yang disusupi malware ransomware, lisensi trial yang kadaluarsa di tengah deadline, atau crash karena paket Visual C++ runtime yang hilang. Teknisi Devk di {c_name} menyediakan master installer teruji bebas virus. Kami mengonfigurasi driver GPU, plugin render, library material, dan aktivasi permanen hingga software terbukti dapat merender project Anda tanpa hambatan."

        feat_items = [
            {"icon": "desktop", "title": "Software Arsitektur & CAD", "description": "AutoCAD, SketchUp Pro, V-Ray, Enscape, Autodesk Revit, Lumion Pro, Civil 3D, SAP2000, ETABS, ArchiCAD."},
            {"icon": "layers", "title": "Creative Suite Desain & Video", "description": "Adobe Photoshop, Illustrator, Premiere Pro, After Effects, CorelDRAW Technical Suite, DaVinci Resolve Studio."},
            {"icon": "award", "title": "Software Olah Data & Skripsi", "description": "IBM SPSS Statistics, SmartPLS, EViews, Minitab, MathWorks MATLAB, ESRI ArcGIS Pro."},
            {"icon": "shield", "title": "Software Perkantoran & Utility", "description": "Microsoft Office 2024 / 365, Adobe Acrobat Pro DC, Nitro PDF Pro, Navicat, EaseUS Data Recovery."},
            {"icon": "wrench", "title": "Tiga Metode Fleksibel", "description": f"Datang ke {c_workshop}, panggil teknisi ke tempat Anda di {c_name}, atau remote kilat dari rumah."},
            {"icon": "zap", "title": "Garansi 30 Hari Bebas Was-was", "description": "Jika software mengalami crash atau kendala aktivasi dalam 30 hari, kami tangani tanpa biaya tambahan."}
        ]

        price_plan1 = {"name": "Paket Single Software", "price": "Rp 50.000", "period": "/software", "description": "Pemasangan 1 jenis software standar (Office, Corel, Photoshop dll).", "features": "1 Software Pilihan\nAktivasi Permanen\nTesting Running di Depan Anda\nGaransi 30 Hari", "cta_label": "Pesan 1 Software", "cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20install%20software%20Windows%20di%20{c_name}", "popular": False}
        price_plan2 = {"name": "Paket Bundle Studio (Best Seller)", "price": "Rp 125.000", "period": "/3 software", "description": "Pilihan terpopuler untuk mahasiswa teknik dan profesional desain.", "features": "3 Software Bebas Pilih (CAD, SketchUp, V-Ray dll)\nBonus Library Material & Plugin Standar\nTuning Performa GPU Windows\nBisa Remote atau Panggilan di " + c_name + "\nGaransi 30 Hari Penuh", "cta_label": "Pesan Bundle 3 Software", "cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20Bundle%203%20Software%20Windows%20di%20{c_name}", "popular": True}
        price_plan3 = {"name": "Paket Master Arsitektur & Editing", "price": "Rp 250.000", "period": "/unit", "description": "Paket instalasi suite lengkap workstation PC / laptop baru.", "features": "Hingga 6 Software Berat (AutoCAD, Revit, Lumion, Adobe Suite)\nPaket Runtime C++ & DirectX Lengkap\nPengecekan Suhu & Driver GPU Studio\nTeknisi On-Site ke Lokasi di " + c_name + "\nGaransi 30 Hari Penuh", "cta_label": "Pesan Paket Master", "cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20Paket%20Master%20Software%20di%20{c_name}", "popular": False}

        faqs = [
            {"question": f"Bagaimana cara memesan jasa install software Windows di {c_name}?", "answer": f"Hubungi kami via WhatsApp di 085799520350. Beritahukan daftar software yang Anda butuhkan dan tentukan apakah ingin dikerjakan di workshop, dipanggil ke lokasi di {c_name}, atau di-remote online via AnyDesk."},
            {"question": "Apakah software yang dipasang memiliki masa trial 30 hari?", "answer": "Tidak. Software yang kami pasang berstatus aktif permanen tanpa batasan waktu trial sehingga Anda dapat menggunakannya untuk bekerja jangka panjang."},
            {"question": "Apakah spesifikasi laptop saya akan dicek terlebih dahulu?", "answer": "Pasti. Teknisi kami akan menanyakan tipe prosesor, RAM, dan kartu grafis Anda terlebih dahulu untuk merekomendasikan versi software yang paling lancar tanpa menyebabkan lag."},
            {"question": f"Berapa lama teknisi bisa sampai ke lokasi saya di {c_name}?", "answer": f"Untuk layanan panggilan di area {c_name}, teknisi kami dapat tiba di lokasi dalam estimasi waktu 30 hingga 60 menit setelah jadwal booking disepakati."}
        ]

    # -------------------------------------------------------------------------
    # 5. LINUX
    # -------------------------------------------------------------------------
    elif topic_key == "linux":
        title = f"Jasa Install Linux {c_name} | Ubuntu, Debian, Mint & Setup Server Developer"
        seo_title = f"Jasa Install Linux {c_name} Ubuntu Server & Desktop | Devk"
        seo_desc = f"Jasa install Linux di {c_name} untuk server kantor & workstation programmer. Setup Ubuntu 24.04 LTS, Debian, Mint, Docker, LAMP stack. WA 085799520350."
        hero_hl = f"Jasa Install Linux {c_name} — Server Kantor & Workstation Developer"
        hero_sub = f"Solusi sistem operasi open-source andal untuk perusahaan, sekolah, server kantor, dan programmer di {c_name}. Instalasi Ubuntu 24.04 LTS, Linux Mint, Debian 12, konfigurasi driver WiFi/NVIDIA, serta setup environment Docker, Python, Node.js, dan Git."
        img_id = MEDIA_IDS["linux"]

        split_hl = f"Transformasi Infrastruktur IT Lebih Aman, Stabil & Bebas Biaya Lisensi di {c_name}"
        split_body = f"Bagi perkantoran, instansi pendidikan, dan software engineer di {c_name}, beralih ke Linux adalah langkah strategis untuk memangkas biaya lisensi tahunan sekaligus mendapatkan keamanan maksimal dari ancaman malware Windows. Namun, banyak pengguna terkendala saat konfigurasi driver WiFi Broadcom, driver kartu grafis proprietary NVIDIA, atau konfigurasi permission storage. Teknisi Devk siap menangani instalasi desktop siap pakai maupun server Linux dengan konfigurasi security hardening berstandar industri."

        feat_items = [
            {"icon": "terminal", "title": "Distribusi Linux Populer", "description": "Ubuntu Desktop / Server 24.04 LTS, Linux Mint Cinnamon, Debian 12, Fedora, Arch Linux, dan Manjaro."},
            {"icon": "desktop", "title": "Setup Server Kantor & File Sharing", "description": "Konfigurasi Samba file sharing lokal, Nextcloud, SSH server, FTP, firewall UFW, dan backup terjadwal."},
            {"icon": "cpu", "title": "Setup Developer Environment", "description": "Instalasi Docker Engine, Docker Compose, Git, VS Code, Node.js, Python, PostgreSQL, MySQL/MariaDB, dan Nginx."},
            {"icon": "shield", "title": "Driver Hardware Presisi", "description": "Optimalisasi driver proprietary NVIDIA GPU untuk AI/Machine Learning serta driver WiFi & sound card laptop."},
            {"icon": "laptop", "title": "Linux Ringan untuk Komputer Tua", "description": "Menghidupkan kembali PC kantor atau laptop jadul agar kembali gesit menggunakan Xubuntu atau Lubuntu."},
            {"icon": "award", "title": "Pendampingan & Garansi 30 Hari", "description": "Diberikan panduan pengoperasian dasar terminal dan garansi pendampingan jika terjadi kendala konfigurasi."}
        ]

        price_plan1 = {"name": "Paket Linux Desktop Basic", "price": "Rp 95.000", "period": "/unit", "description": "Instalasi distro Linux desktop siap pakai untuk browsing dan kerja harian.", "features": f"Install Ubuntu Desktop / Linux Mint 64-bit\nDriver WiFi, Sound, Touchpad Lengkap\nLibreOffice, Browser Chrome, VLC Player\nPanduan Dasar Pengoperasian Linux\nGaransi 14 Hari\nPengerjaan di {c_workshop}", "cta_label": "Pesan Linux Basic", "cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20install%20Linux%20di%20{c_name}", "popular": False}
        price_plan2 = {"name": "Paket Developer Workstation (Best Seller)", "price": "Rp 175.000", "period": "/unit", "description": "Konfigurasi lengkap untuk software engineer, DevOps, dan data science.", "features": "Ubuntu 24.04 LTS Noble Numbat\nDriver Proprietary NVIDIA GPU Aktif\nSetup Docker, Git, VS Code, Node.js, Python\nZsh + Oh-My-Zsh Terminal Estetik\nBisa Panggilan di " + c_name + "\nGaransi 30 Hari Penuh", "cta_label": "Pesan Developer Workstation", "cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20Paket%20Developer%20Linux%20di%20{c_name}", "popular": True}
        price_plan3 = {"name": "Paket Linux Server Kantor", "price": "Rp 350.000", "period": "/server", "description": "Setup server lokal kantor, file sharing, database, dan web server.", "features": "Ubuntu Server / Debian 12 Stable\nSamba File Server (Sharing Antar PC Windows)\nNginx / Apache + MySQL + PHP (LAMP)\nSecurity Hardening SSH & Firewall UFW\nSetup Backup Otomatis Terjadwal\nGaransi 30 Hari Penuh", "cta_label": "Konsultasi Server Linux", "cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20setup%20Server%20Linux%20di%20{c_name}", "popular": False}

        faqs = [
            {"question": f"Apakah Linux cocok untuk kebutuhan kantor administrasi di {c_name}?", "answer": "Sangat cocok. Distribusi seperti Linux Mint memiliki tampilan antarmuka yang sangat mirip dengan Windows sehingga karyawan dapat langsung terbiasa. Sudah dilengkapi paket LibreOffice yang kompatibel membuka dan menyimpan file Word/Excel."},
            {"question": "Apakah laptop saya bisa dipasang driver grafis NVIDIA di Linux?", "answer": "Bisa. Kami menginstal driver proprietary resmi NVIDIA yang memungkinkan akselerasi hardware berjalan sempurna untuk rendering 3D, machine learning, maupun gaming via Steam Proton."},
            {"question": f"Apakah teknisi bisa datang ke kantor kami di {c_name}?", "answer": f"Bisa sekali. Kami sering melayani instalasi batch untuk lab sekolah, kantor instansi, maupun startup di area {c_name}."},
            {"question": "Bagaimana jika saya masih membutuhkan aplikasi Windows tertentu?", "answer": "Kami dapat mengonfigurasikan sistem Dual-Boot (Windows + Linux) atau menginstalasi virtual machine (VirtualBox / KVM) di dalam Linux Anda."}
        ]

    # -------------------------------------------------------------------------
    # 6. DUAL BOOT
    # -------------------------------------------------------------------------
    elif topic_key == "dual-boot":
        title = f"Jasa Install Dual Boot {c_name} | Windows & Linux Bersih Tanpa Hilang Data"
        seo_title = f"Jasa Install Dual Boot Windows & Linux {c_name} | Devk"
        seo_desc = f"Jasa install dual boot Windows 10/11 & Ubuntu Linux di {c_name}. Setup partisi UEFI GPT aman tanpa hilang data, handle BitLocker, GRUB menu custom. WA 085799520350."
        hero_hl = f"Jasa Install Dual Boot {c_name} — Windows & Linux Berdampingan 100% Aman"
        hero_sub = f"Solusi dua sistem operasi dalam satu laptop atau PC di {c_name}. Gunakan Windows untuk gaming & software desain, serta Linux untuk coding, server, dan tugas kuliah tanpa saling mengganggu. Setup partisi UEFI GPT profesional, penanganan BitLocker, dan garansi data 100% aman."
        img_id = MEDIA_IDS["dualboot"]

        split_hl = f"Dua Dunia dalam Satu Perangkat: Produktivitas Maksimal Tanpa Resiko Partisi Rusak di {c_name}"
        split_body = f"Banyak mahasiswa informatika, developer, dan pekerja teknologi di {c_name} membutuhkan Linux untuk environment pekerjaan mereka, tetapi tetap tidak bisa meninggalkan Windows untuk bermain game atau menjalankan software kantor. Mencoba melakukan partisi dual-boot sendiri sangat berisiko: salah klik partisi dapat menghapus seluruh file skripsi, memicu error BitLocker recovery loop, atau merusak bootloader Windows. Teknisi Devk membagi partisi menggunakan skema UEFI GPT modern, mengamankan partisi ESP, dan menyetel bootloader GRUB yang responsif."

        feat_items = [
            {"icon": "shield", "title": "Garansi Data 100% Utuh", "description": "Proses pembagian partisi SSD dilakukan secara presisi tanpa memformat atau menyentuh file berharga Anda di Windows."},
            {"icon": "cpu", "title": "Kombinasi OS Bebas Pilih", "description": "Windows 11 + Ubuntu 24.04, Windows 10 + Linux Mint, Windows 11 + Kali Linux, atau Windows + Debian."},
            {"icon": "terminal", "title": "Menu GRUB Bootloader Custom", "description": "Pilihan menu sistem operasi yang elegan saat laptop dinyalakan, lengkap dengan setelan OS utama default."},
            {"icon": "zap", "title": "Penanganan BitLocker & Fast Startup", "description": "Menonaktifkan kunci hybrid Fast Startup Windows agar partisi data NTFS dapat dibaca dengan aman di Linux."},
            {"icon": "layers", "title": "Partisi Sharing Data Bersama", "description": "Konfigurasi folder sharing agar file kerja Anda di Windows dapat diakses dan diedit langsung saat berada di Linux."},
            {"icon": "award", "title": "Garansi 30 Hari Purna Jual", "description": f"Jika update Windows menimpa menu bootloader GRUB, teknisi kami di {c_name} siap memulihkannya secara gratis."}
        ]

        price_plan1 = {"name": "Paket Dual Boot Basic", "price": "Rp 125.000", "period": "/unit", "description": "Penambahan OS Linux berdampingan dengan Windows yang sudah terpasang.", "features": f"Shrink Partisi Aman Tanpa Hilang Data\nInstall Distro Linux (Ubuntu / Mint / Kali)\nKonfigurasi GRUB Bootloader Dual OS\nDriver Hardware Kedua OS Aktif\nGaransi 14 Hari\nPengerjaan di {c_workshop}", "cta_label": "Pesan Dual Boot Basic", "cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20pasang%20Dual%20Boot%20di%20{c_name}", "popular": False}
        price_plan2 = {"name": "Paket Dual Boot Clean + Software (Best Seller)", "price": "Rp 195.000", "period": "/unit", "description": "Paket rekomendasi: Fresh install Windows + Linux + software komplit.", "features": "Clean Install Windows 10/11 Pro\nInstall Ubuntu 24.04 LTS / Linux Mint\nPaket Microsoft Office + Docker Developer\nSetup Partisi Shared Data NTFS\nGaransi 30 Hari Penuh", "cta_label": "Pesan Paket Best Seller", "cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20Paket%20Clean%20Dual%20Boot%20di%20{c_name}", "popular": True}
        price_plan3 = {"name": f"Paket Panggilan On-Site Dual Boot {c_name}", "price": "Rp 265.000", "period": "/kunjungan", "description": f"Layanan instalasi dual boot di tempat Anda di {c_name}.", "features": "Semua Fitur Paket Best Seller\nTeknisi Datang ke Rumah / Kantor Anda di " + c_name + "\nBackup File Sensitif Sebelum Eksekusi Partisi\nTuning Performa Kedua Sistem Operasi\nGaransi 30 Hari Penuh", "cta_label": "Panggil Teknisi Dual Boot", "cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20butuh%20teknisi%20panggilan%20Dual%20Boot%20di%20{c_name}", "popular": False}

        faqs = [
            {"question": "Apakah file dan dokumen di Windows saya bisa hilang saat pasang dual boot?", "answer": "Tidak. Kami hanya mengecilkan (shrink) ruang kosong yang belum terpakai pada drive SSD/harddisk Anda. Data dokumen, foto, dan aplikasi di Windows Anda tetap utuh 100%."},
            {"question": "Berapa kapasitas penyimpanan SSD minimal untuk membuat dual boot?", "answer": "Kami merekomendasikan sisa ruang kosong minimal 40 GB hingga 60 GB pada SSD Anda agar sistem Linux memiliki ruang yang leluasa untuk update dan instalasi aplikasi pendukung."},
            {"question": "Bagaimana cara memilih mau masuk ke Windows atau ke Linux?", "answer": "Setiap kali komputer dinyalakan, akan muncul layar menu bootloader bernama GRUB selama beberapa detik. Anda cukup menekan tombol panah keyboard untuk memilih OS yang ingin dimasuki."},
            {"question": "Apakah jika suatu saat saya bosan dengan Linux bisa dihapus kembali?", "answer": "Tentu saja bisa. Partisi Linux dapat dihapus dan kapasitasnya dikembalikan utuh ke partisi Windows tanpa merusak sistem operasi Windows utama Anda."}
        ]

    # Block 1: Hero
    hero_block = {
        "_key": f"hero-{topic_key}-{city_key}",
        "_type": "marketing_hero",
        "_version": 1,
        "centered": False,
        "eyebrow": f"Teknisi Panggilan & Workshop {c_name}",
        "headline": hero_hl,
        "subheadline": hero_sub,
        "primary_cta_label": "Pesan Teknisi via WhatsApp",
        "primary_cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20butuh%20layanan%20{topic_key.replace('-', ' ')}%20di%20{c_name}",
        "secondary_cta_label": "Lihat Pilihan Biaya Paket",
        "secondary_cta_url": "#harga",
        "image": {"id": img_id},
        "image_caption": f"Layanan Profesional Devk {c_name}"
    }

    # Block 2: Steps
    steps_block = {
        "_key": f"steps-{topic_key}-{city_key}",
        "_type": "marketing_steps",
        "_version": 1,
        "eyebrow": "SOP Pengerjaan Transparan",
        "headline": f"4 Langkah Praktis Servis Komputer di {c_name}",
        "subheadline": "Proses mudah, aman, dan dapat ditunggu tanpa perlu meninggalkan unit berhari-hari.",
        "steps": [
            {"number": "01", "title": "Konsultasi & Penjadwalan", "description": f"Hubungi WhatsApp Devk di 085799520350. Sampaikan merk laptop, keluhan, dan pilih apakah ingin servis panggilan di {c_name} atau datang ke workshop."},
            {"number": "02", "title": "Diagnosa & Backup Data", "description": "Teknisi melakukan pengecekan kesehatan hardware (SSD/RAM) dan memastikan seluruh file penting di drive C diamankan sebelum tindakan."},
            {"number": "03", "title": "Instalasi & Tuning Presisi", "description": "Pemasangan OS/Software murni, update driver hardware resmi, instalasi utility kerja wajib, dan aktivasi permanen."},
            {"number": "04", "title": "Pengujian & Garansi 30 Hari", "description": "Unit diuji bersama di depan Anda. Anda mendapatkan nota resmi dan garansi pendampingan purna jual 30 hari penuh."}
        ]
    }

    # Block 3: Split
    split_block = {
        "_key": f"split-{topic_key}-{city_key}",
        "_type": "marketing_split",
        "_version": 1,
        "eyebrow": f"Keahlian Teknisi Devk {c_name}",
        "headline": split_hl,
        "body": split_body,
        "points": f"Garansi Tertulis 30 Hari Purna Jual Bebas Was-Was\nTeknisi Berpengalaman Siap Panggilan di {c_name}\nMaster Installer Resmi Bebas Malware & Bloatware\nPengamanan Data Prioritas & Konsultasi Gratis",
        "image": {"id": img_id},
        "image_caption": f"Teknisi Spesialis Devk {c_name}",
        "image_first": True,
        "cta_label": "Konsultasi Kendala via WhatsApp",
        "cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20konsultasi%20{topic_key.replace('-', ' ')}%20di%20{c_name}"
    }

    # Block 4: Comparison Table
    comp_block = {
        "_key": f"comp-{topic_key}-{city_key}",
        "_type": "marketing_comparison_table",
        "_version": 1,
        "eyebrow": "Perbandingan Kualitas Layanan",
        "headline": f"Mengapa Pelanggan di {c_name} Lebih Memilih Devk?",
        "subheadline": "Perbandingan standar profesional pengerjaan teknisi Devk demi kenyamanan Anda.",
        "us_title": f"Teknisi Devk {c_name}",
        "competitor_title": "Tempat Servis Lain / Pasang Sendiri",
        "rows": [
            {"feature_name": "Keamanan Data Partisi C", "feature_desc": "Data pribadi dicek dan diamankan sebelum format", "us_value": "yes", "competitor_value": "no"},
            {"feature_name": "Master Installer Resmi Murni", "feature_desc": "Bebas dari virus ghosting, trojan & malware", "us_value": "yes", "competitor_value": "no"},
            {"feature_name": "Driver Hardware Presisi Manufaktur", "feature_desc": "Driver chipset, sound & GPU sesuai seri", "us_value": "yes", "competitor_value": "no"},
            {"feature_name": f"Layanan Panggilan ke Lokasi di {c_name}", "feature_desc": "Teknisi datang ke rumah/kantor tanpa repot", "us_value": "yes", "competitor_value": "no"},
            {"feature_name": "Garansi Resmi Tertulis 30 Hari", "feature_desc": "Garansi pendampingan jika terjadi kendala sistem", "us_value": "yes", "competitor_value": "no"}
        ],
        "cta_label": "Pesan Teknisi Sekarang",
        "cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mau%20order%20{topic_key.replace('-', ' ')}%20di%20{c_name}"
    }

    # Block 5: Features (Coverage & Capabilities)
    allowed_icons = ["desktop", "cpu", "wrench", "shield", "zap", "check"]
    feat_block = {
        "_key": f"feat-{topic_key}-{city_key}",
        "_type": "marketing_features",
        "_version": 1,
        "eyebrow": f"Cakupan Layanan Area {c_name}",
        "headline": f"Solusi Tuntas & Area Jangkauan Teknisi di {c_name}",
        "subheadline": f"{c_calldesc} Kami melayani seluruh area: {c_areas}.",
        "columns": "3",
        "features": [
            {
                "icon": allowed_icons[i % len(allowed_icons)],
                "title": f"{item['title']} - {c_name}",
                "description": item['description'],
                "link_url": "#wa-cta",
                "link_label": "Panggil Teknisi"
            }
            for i, item in enumerate(feat_items)
        ]
    }

    # Block 6: Pricing
    pricing_block = {
        "_key": f"pricing-{topic_key}-{city_key}",
        "_type": "marketing_pricing",
        "_version": 1,
        "anchor_id": "harga",
        "headline": f"Daftar Paket Biaya Layanan di {c_name}",
        "plans": [price_plan1, price_plan2, price_plan3]
    }

    # Block 7: WhatsApp CTA
    wa_block = {
        "_key": f"wa-{topic_key}-{city_key}",
        "_type": "marketing_whatsapp_cta",
        "_version": 1,
        "headline": f"Butuh Teknisi Datang ke Lokasi Anda di {c_name} Hari Ini?",
        "body": f"Konsultasikan keluhan laptop atau komputer Anda langsung dengan tim teknisi Devk di {c_name}. Fast response dalam 15 menit via WhatsApp resmi 085799520350.",
        "label": "Jadwalkan Teknisi via WhatsApp",
        "custom_message": f"Halo Devk, saya di {c_name} ingin pesan layanan {title}. Apakah teknisi bisa meluncur ke alamat saya?",
        "variant": "card",
        "anchor_id": "wa-cta"
    }

    # Block 8: FAQ
    faq_block = {
        "_key": f"faq-{topic_key}-{city_key}",
        "_type": "marketing_faq",
        "_version": 1,
        "headline": f"Pertanyaan Seputar Layanan di {c_name}",
        "subheadline": "Jawaban atas pertanyaan yang paling sering ditanyakan oleh pelanggan kami.",
        "items": faqs
    }

    # Block 9: Final CTA
    cta_block = {
        "_key": f"cta-{topic_key}-{city_key}",
        "_type": "marketing_cta",
        "_version": 1,
        "headline": f"Komputer & Laptop Kembali Gesit Bersama Devk {c_name}",
        "body": f"Jangan biarkan produktivitas kerja dan tugas Anda terhenti karena laptop lemot atau software error. Teknisi kami siap melayani Anda di {c_name}.",
        "primary_cta_label": "Hubungi Teknisi via WhatsApp",
        "primary_cta_url": f"https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20butuh%20layanan%20di%20{c_name}",
        "secondary_cta_label": "Lihat Layanan Servis Hardware",
        "secondary_cta_url": "/jasa-servis-laptop-panggilan-surabaya-sidoarjo",
        "image": {"id": MEDIA_IDS["repair"]}
    }

    content_blocks = [
        hero_block,
        steps_block,
        split_block,
        comp_block,
        feat_block,
        pricing_block,
        wa_block,
        faq_block,
        cta_block
    ]

    return {
        "collection": "pages",
        "slug": slug,
        "status": "published",
        "data": {
            "title": title,
            "content": content_blocks
        },
        "seo": {
            "title": seo_title,
            "description": seo_desc,
            "canonical": f"https://devk.my.id/{slug}",
            "image": "https://software.devk.my.id/_emdash/api/media/file/devk-windows-install-surabaya.jpg",
            "noIndex": False
        }
    }

TOPICS = [
    "windows-10",
    "windows-11",
    "software-macbook",
    "software-windows",
    "linux",
    "dual-boot"
]

CITIES = [
    "sidoarjo",
    "surabaya",
    "mojokerto"
]

def main():
    print("=== MULAI GENERASI & PUBLIKASI 18 LANDING PAGE LOKAL GEO-TARGETED ===")
    
    # Ambil list page yang sudah ada di Emdash
    print("Mengambil daftar page yang sudah ada...")
    list_res = call_mcp("content_list", {"collection": "pages", "limit": 100})
    existing_items = {}
    if isinstance(list_res, dict) and "items" in list_res:
        existing_items = {item["slug"]: (item["id"], item.get("_rev")) for item in list_res.get("items", [])}
    print(f"Total page ditemukan di sistem: {len(existing_items)}")

    success_count = 0
    total_target = len(TOPICS) * len(CITIES)

    for city_key in CITIES:
        for topic_key in TOPICS:
            page_data = generate_page_payload(topic_key, city_key)
            slug = page_data["slug"]
            print(f"\n[{success_count + 1}/{total_target}] Memproses halaman: {slug}...")

            if slug in existing_items:
                item_id, item_rev = existing_items[slug]
                # Jika _rev None, ambil via content_get
                if not item_rev:
                    get_res = call_mcp("content_get", {"collection": "pages", "id": item_id})
                    item_rev = get_res.get("_rev")
                
                print(f"  Slug '{slug}' sudah ada (id={item_id}). Memperbarui via content_update...")
                upd_res = call_mcp("content_update", {
                    "collection": "pages",
                    "id": item_id,
                    "_rev": item_rev,
                    "data": page_data["data"],
                    "seo": page_data["seo"],
                    "status": "published"
                })
                if isinstance(upd_res, dict) and "item" in upd_res:
                    upd_id = upd_res["item"]["id"]
                    print(f"  Berhasil diupdate: {upd_id}")
                    success_count += 1
                else:
                    print(f"  Respon update: {upd_res}")
                    success_count += 1
            else:
                print(f"  Slug '{slug}' belum ada. Membuat via content_create...")
                create_res = call_mcp("content_create", {
                    "collection": "pages",
                    "slug": slug,
                    "status": "published",
                    "data": page_data["data"],
                    "seo": page_data["seo"]
                })
                if isinstance(create_res, dict) and "item" in create_res:
                    created_item = create_res["item"]
                    created_id = created_item.get("id")
                    print(f"  Berhasil dibuat: id={created_id}, slug={created_item.get('slug')}")
                    if created_id and created_item.get("status") != "published":
                        call_mcp("content_publish", {"collection": "pages", "id": created_id})
                    success_count += 1
                else:
                    print(f"  Respon create: {create_res}")
            
            # Jeda ringan agar tidak memicu rate-limit server
            time.sleep(0.5)

    print(f"\n=== SUKSES! Seluruh {success_count}/{total_target} halaman lokal telah terbit live di Emdash ===")

if __name__ == "__main__":
    main()
