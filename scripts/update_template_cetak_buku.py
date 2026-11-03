import json, subprocess

BASE_DIR = '/home/ubuntu/projects/kotacom-emdash'
with open(f'{BASE_DIR}/.env') as f:
    for line in f:
        if line.startswith('DATABASE_URL='):
            pw = line.split('://dokploy:')[1].split('@')[0]
            break

def run_psql(sql):
    cmd = ['sudo', 'docker', 'exec', '-i', '-e', f'PGPASSWORD={pw}', 'devk-software-db-hfl2l5.1.mydjd6wgx9s8ledrfqf7chlz6', 'psql', '-U', 'dokploy', '-d', 'kotacom_emdash']
    p = subprocess.run(cmd, input=sql, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"psql error: {p.stderr}\nSQL: {sql[:300]}")
    return p.stdout

# 1. Headline, Subheadline & Hero
hero_block = {
    "_key": "hero_cetak_buku",
    "_type": "marketing_hero",
    "_version": 1,
    "centered": False,
    "eyebrow": "{CETAK BUKU SATUAN & MASSAL|PERCETAKAN BUKU TANGAN PERTAMA|PRINT ON DEMAND & CETAK OFFSET} · KOTACOM",
    "eyebrow_url": "/percetakan/cetak-buku",
    "headline": "{Jasa Cetak Buku di {{kabupaten | title}} — Mulai 1 Eksemplar & Grosir Murah|Cetak Buku Satuan & Oplah Besar Murah untuk Wilayah {{kabupaten | title}}|Percetakan Buku Murah di {{kabupaten | title}} — Kertas Bookpaper & HVS Standar Penerbit}",
    "subheadline": "{Bisa cetak mulai 1 buku untuk naskah pribadi atau ribuan eksemplar untuk instansi dan sekolah di {{kabupaten | title}}. Pilihan kertas Bookpaper krem atau HVS putih, jilid Softcover lem panas maupun Hardcover mewah dengan harga langsung dari produsen.|Cetak naskah Anda tanpa minimal order yang memberatkan. Melayani cetak novel, buku ajar, modul sekolah, hingga antologi komunitas di {{kabupaten | title}} dengan jilid kokoh, hasil tajam 1200 DPI, dan ongkos produksi paling hemat.}",
    "image": {
        "id": "01M665C001STYLE1CETAKBUKU1",
        "alt": "Jasa Cetak Buku {{kabupaten | title}} Murah Satuan & Grosir - Kotacom.id WA 085799520350",
        "src": "/images/cetak-buku-universal/style-1.jpg",
        "previewUrl": "/images/cetak-buku-universal/style-1.jpg",
        "width": 1024,
        "height": 1024,
        "filename": "style-1.jpg",
        "mimeType": "image/jpeg",
        "provider": "local"
    },
    "image_fit": "full",
    "image_caption": "Kotacom.id · WA 085799520350 — Jasa Cetak Buku Satuan & Grosir Murah",
    "primary_cta_label": "{Hitung Biaya Cetak via WA|Konsultasi & Cek Harga WA|Kirim File Naskah via WA}",
    "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Kotacom%20saya%20ingin%20konsultasi%20cetak%20buku%20untuk%20wilayah%20{{kabupaten}}%20(satuan/oplah)",
    "secondary_cta_label": "{Daftar Harga & Pilihan Jilid|Lihat Estimasi Biaya}",
    "secondary_cta_url": "#pricing"
}

# 2. Rich Text Editorial Section (Paragraph Spintax & In-depth Trust Copy)
richtext_block = {
    "_key": "editorial_cetak_buku",
    "_type": "marketing_richtext",
    "_version": 1,
    "anchor_id": "panduan-cetak",
    "headline": "{Pilihan Bahan Kertas & Jilid Sesuai Kebutuhan Anda di {{kabupaten | title}}|Cetak Buku Berkualitas Tanpa Biaya Tersembunyi|Fleksibel: Cetak Satuan (POD) Maupun Grosir Partai Besar}",
    "body": "{Bagi Anda penulis pemula, dosen, atau mahasiswa di {{kabupaten | title}} yang ingin mencetak buku dalam jumlah terbatas, sistem Print on Demand (POD) kami memungkinkan pencetakan mulai dari 1 buku saja. Anda tidak perlu mengeluarkan modal jutaan rupiah di awal. Cetak beberapa buku contoh untuk proofing fisik, koreksi naskah, atau keperluan sidang dan koleksi pribadi dengan biaya yang sangat terjangkau.\n\nPilihan kertas isi tersedia lengkap: Bookpaper krem 57/72gsm yang ringan dan nyaman di mata untuk novel dan buku bacaan tebal, atau kertas HVS 70/80gsm putih bersih yang sangat cocok untuk buku ajar, skripsi, lembar kerja siswa (LKS), dan laporan teknis.|Bagi sekolah, pesantren, yayasan, dan komunitas di {{kabupaten | title}} yang membutuhkan cetak buku massal—seperti buku kenangan, majalah sekolah, buku saku santri, hingga laporan instansi—kami menyediakan harga pabrik grosir yang jauh lebih hemat per eksemplarnya. Semakin banyak jumlah yang dicetak, biaya per halaman semakin murah.\n\nUntuk finishing cover, Anda bisa memilih Softcover dengan jilid lem panas (Perfect Binding) lentur yang rapi khas buku Gramedia, atau Hardcover board tebal yang kokoh dengan pilihan laminasi Doff elegan, Glossy mengkilap, hingga sentuhan pita pembatas buku dan sudut presisi.|Banyak penulis di {{kabupaten | title}} ragu mencetak buku karena takut format file berantakan atau potongan teks terpotong. Di Kotacom, tim teknis kami memeriksa berkas PDF naskah Anda secara teliti sebelum naik ke mesin: memastikan margin dalam (gutter) aman untuk jilid, resolusi gambar mencukupi (minimal 300 DPI), dan layout siap cetak tanpa biaya tambahan.\n\nSetiap pesanan buku dikemas dengan pengamanan ganda—masing-masing buku dibungkus plastik shrink wrap anti air, lalu disusun di kardus tebal berlapis bubble wrap berlapis—sehingga paket buku sampai ke alamat Anda di {{kabupaten | title}} dalam kondisi utuh dan mulus tanpa sudut terlipat.}"
}

# 3. Split Block (Spesifikasi Teknis Kertas & Jilid)
split_block = {
    "_key": "split_cetak_buku",
    "_type": "marketing_split",
    "_version": 1,
    "eyebrow": "{PILIHAN BAHAN & JILID LENGKAP|STANDAR PRODUKSI RESMI|SPESIFIKASI BUKU}",
    "headline": "{Tersedia Bookpaper, HVS, Softcover Lem Panas & Hardcover|Kombinasi Bahan Kertas & Jilid Terlengkap}",
    "body": "{Kami menyediakan bahan baku standar penerbit mayor untuk memastikan buku Anda awet dan nyaman dibaca. Anda bebas menentukan ketebalan kertas dan jenis jilid sesuai anggaran dan peruntukan buku di {{kabupaten | title}}.|Dari proofing naskah digital hingga pengepresan lem jilid bertekanan tinggi, setiap eksemplar buku dikerjakan dengan standar mesin industri. Hasil potong tiga sisi presisi dan tidak ada lembar kertas yang mudah tanggal saat buku dibuka lebar.}",
    "points": "{Kertas Bookpaper krem impor 57/72gsm: ringan, tidak silau, khas novel dan buku bacaan|Kertas HVS 70/80gsm putih tajam: ideal untuk modul kuliah, buku sekolah & laporan}\n{Jilid Softcover lem panas (Perfect Binding): lentur, rapi & standar toko buku|Jilid Hardcover mewah: papan board tebal kokoh untuk buku kenangan & karya prestisius}\n{Cover Art Carton 260/310gsm tebal dengan opsi laminasi Doff lembut atau Glossy tajam|Finishing tambahan: jilid spiral kawat, spot UV mengkilap, foil emas/perak}\n{Bebas tentukan jumlah: bisa cetak 1 eksemplar (satuan) hingga ribuan eksemplar (partai murah)|Garansi pengerjaan rapi dan penggantian bila ada cacat cetak atau jilid}",
    "image": {
        "id": "01M665C003STYLE3CETAKBUKU3",
        "alt": "Pilihan Kertas Bookpaper HVS dan Jilid Hardcover Softcover {{kabupaten | title}}",
        "src": "/images/cetak-buku-universal/style-3.jpg",
        "previewUrl": "/images/cetak-buku-universal/style-3.jpg",
        "width": 1024,
        "height": 1024,
        "filename": "style-3.jpg",
        "mimeType": "image/jpeg",
        "provider": "local"
    },
    "image_fit": "full",
    "image_first": False,
    "image_caption": "Kualitas Cetak & Jilid Presisi · Kotacom.id (085799520350)",
    "cta_label": "Lihat Detail Produk Book Printing",
    "cta_url": "/products/book-printing"
}

# 4. Features Section (3 Model Pemesanan)
features_block = {
    "_key": "features_cetak_buku",
    "_type": "marketing_features",
    "_version": 1,
    "columns": "3",
    "eyebrow": "{CAKUPAN LAYANAN CETAK|VARIASI KEBUTUHAN BUKU}",
    "headline": "{3 Pilihan Cetak Buku Fleksibel untuk {{kabupaten | title}}|Kategori Pemesanan Sesuai Kebutuhan Anda}",
    "subheadline": "Pilih spesifikasi cetak satuan atau massal sesuai target pembaca dan anggaran Anda.",
    "features": [
        {
            "icon": "star",
            "title": "{Cetak Satuan & Uji Naskah (POD)|Print on Demand (Mulai 1 Buku)}",
            "description": "{Cetak mulai dari 1 buku saja untuk keperluan proofing, buku kado, atau cetak terbatas tanpa modal besar bagi penulis di {{kabupaten | title}}.|Solusi hemat tanpa minimal order. Cocok untuk uji coba cetak sebelum naskah diterbitkan dalam jumlah banyak.}",
            "image_url": "/images/cetak-buku-universal/style-4.jpg",
            "link_label": "Rincian Biaya Cetak Satuan →",
            "link_url": "/blog/berapa-biaya-cetak-buku-sendiri-panduan-lengkap-untuk-penulis-pemula"
        },
        {
            "icon": "file",
            "title": "{Buku Ajar, Modul & Komunitas|Oplah Sedang (50-200 Eks)}",
            "description": "{Paket paling diminati dosen, sekolah, dan komunitas literasi di {{kabupaten | title}}. Harga per eksemplar jauh lebih ekonomis dengan kualitas kertas Bookpaper pilihan.|Lengkap dengan gratis bookmark custom dan pembungkus plastik per buku untuk distribusi rapi.}",
            "image_url": "/images/cetak-buku-universal/style-2.jpg",
            "link_label": "Panduan Mengurus ISBN Online →",
            "link_url": "/blog/panduan-lengkap-mudah-mengurus-isbn-online-untuk-penulis-mandiri"
        },
        {
            "icon": "shield",
            "title": "{Cetak Massal / Hardcover Mewah|Oplah Besar & Proyek Instansi}",
            "description": "{Harga grosir tangan pertama untuk pesanan instansi, penerbit indie, dan yayasan di {{kabupaten | title}}. Pilihan hardcover papan tebal dan pengiriman ekspedisi cargo terpercaya.|Dukungan administrasi penawaran harga dan faktur resmi untuk pengadaan instansi.}",
            "image_url": "/images/cetak-buku-universal/style-5.jpg",
            "link_label": "5 Ide Finishing Cover Buku →",
            "link_url": "/blog/5-ide-finishing-cover-buku-yang-bikin-pembaca-jatuh-cinta-pada-pandangan-pertama"
        }
    ]
}

# 5. Visual Slider Gallery
slider_block = {
    "_key": "slider_visual_cetak_buku",
    "_type": "marketing_slider",
    "_version": 1,
    "anchor_id": "galeri-cetak",
    "eyebrow": "GALERI & INSPIRASI CETAK · KOTACOM.ID",
    "headline": "5 Gaya & Inspirasi Produksi Buku untuk {{kabupaten | title}}",
    "subheadline": "Semua lini produksi cetak buku Kotacom.id (WA 085799520350) terhubung dengan panduan teknis & katalog layanan resmi.",
    "slides": [
        {
            "title": "1. Cetak Buku Satuan & Oplah Besar",
            "description": "Layanan cetak buku mulai 1 eksemplar hingga ribuan buku dengan standar jilid rapi toko buku untuk {{kabupaten | title}}.",
            "image_url": "/images/cetak-buku-universal/style-1.jpg",
            "link_label": "Katalog Book Printing",
            "link_url": "/products/book-printing"
        },
        {
            "title": "2. Standar Format File & Tata Letak",
            "description": "Pastikan file PDF naskah dan cover Anda siap cetak dengan margin dalam yang cukup dan resolusi 300 DPI.",
            "image_url": "/images/cetak-buku-universal/style-2.jpg",
            "link_label": "Cara Menyiapkan File Cetak",
            "link_url": "/blog/cara-menyiapkan-file-siap-cetak-untuk-buku-anti-ditolak"
        },
        {
            "title": "3. Pilihan Kertas Bookpaper & HVS",
            "description": "Perbandingan cetak menggunakan kertas bookpaper krem klasik vs HVS putih cerah agar anggaran cetak di {{kabupaten | title}} lebih hemat.",
            "image_url": "/images/cetak-buku-universal/style-3.jpg",
            "link_label": "Tips Cetak Buku Hemat",
            "link_url": "/blog/berapa-biaya-cetak-buku-sendiri-ini-rincian-simulasinya"
        },
        {
            "title": "4. Jilid Softcover Lem Panas & Hardcover",
            "description": "Pilihan jilid lem panas elastis untuk novel dan jilid hardcover kokoh untuk buku kenangan atau karya ilmiah.",
            "image_url": "/images/cetak-buku-universal/style-4.jpg",
            "link_label": "Pilihan Finishing Cover",
            "link_url": "/blog/5-ide-finishing-cover-buku-yang-bikin-pembaca-jatuh-cinta-pada-pandangan-pertama"
        },
        {
            "title": "5. Al-Quran, Yasin & Kalender",
            "description": "Selain buku naskah, Kotacom melayani cetak mushaf Al-Quran wakaf, buku yasin tahlil, majalah, dan kalender promosi.",
            "image_url": "/images/cetak-buku-universal/style-5.jpg",
            "link_label": "Katalog Quran Printing",
            "link_url": "/products/quran-printing"
        }
    ]
}

# 6. Pricing Block (Transparan & Termurah)
pricing_block = {
    "_key": "pricing_cetak_buku",
    "_type": "marketing_pricing",
    "_version": 1,
    "anchor_id": "pricing",
    "headline": "{Paket Biaya Cetak Buku Termurah di {{kabupaten | title}}|Pilihan Paket Cetak Sesuai Kebutuhan Oplah Anda}",
    "plans": [
        {
            "name": "{Paket Satuan (POD)|Satuan / Sample Naskah}",
            "price": "Mulai 15rb",
            "period": "/ buku",
            "description": "{Paling pas untuk cetak 1 - 20 buku naskah pribadi atau proofing di {{kabupaten | title}}.|Solusi tanpa minimal order untuk penulis mandiri dan mahasiswa.}",
            "features": "Bisa cetak mulai 1 eksemplar\nPilihan kertas Bookpaper atau HVS\nCover Art Carton 260gsm full color\nLaminasi Doff atau Glossy bebas pilih\nJilid Softcover lem panas rapi\nEstimasi produksi 3-5 hari kerja",
            "cta_label": "Pilih Cetak Satuan",
            "cta_url": "https://wa.me/6285799520350?text=Halo%20Kotacom%20saya%20minat%20cetak%20buku%20satuan%20untuk%20{{kabupaten}}",
            "highlighted": False
        },
        {
            "name": "{Paket Komunitas (Grosir)|Oplah Komunitas / Sekolah}",
            "badge": "Paling Hemat",
            "price": "Mulai 10rb",
            "period": "/ buku",
            "description": "{Biaya produksi per buku jauh lebih murah untuk antologi komunitas, sekolah, dan modul di {{kabupaten | title}}.|Pilihan terbaik untuk menghemat anggaran penerbitan komunitas.}",
            "features": "Harga per eksemplar jauh lebih murah\nPilihan Bookpaper krem atau HVS 70gsm\nGratis pembatas buku (bookmark) custom\nGratis cek layout & proofing digital PDF\nPlastik shrink wrap pelindung per buku\nPrioritas jadwal produksi lebih cepat",
            "cta_label": "Pilih Paket Komunitas",
            "cta_url": "https://wa.me/6285799520350?text=Halo%20Kotacom%20saya%20minat%20paket%20komunitas%20cetak%20buku%20{{kabupaten}}",
            "highlighted": True
        },
        {
            "name": "{Paket Hardcover / Oplah Besar|Partai Besar & Instansi}",
            "price": "Custom Murah",
            "period": "harga pabrik",
            "description": "{Harga pabrik langsung tangan pertama untuk pesanan ratusan hingga ribuan eksemplar atau jilid Hardcover mewah.|Pilihan instansi pemerintah, yayasan, dan penerbit independen.}",
            "features": "Harga grosir langsung tangan pertama\nOpsi Hardcover board tebal mewah\nPilihan jahit benang + lem panas kokoh\nFinishing foil emas, emboss, & pita baca\nPengiriman via kargo hemat bergaransi\nBisa terbitkan SPK / Invoice resmi instansi",
            "cta_label": "Konsultasi Oplah Besar",
            "cta_url": "https://wa.me/6285799520350?text=Halo%20Kotacom%20saya%20minat%20penawaran%20oplah%20besar%20hardcover%20{{kabupaten}}",
            "highlighted": False
        }
    ]
}

# 7. FAQ Block (Practical objection handling)
faq_block = {
    "_key": "faq_cetak_buku",
    "_type": "marketing_faq",
    "_version": 1,
    "headline": "Tanya Jawab Seputar Cetak Buku di {{kabupaten | title}}",
    "subheadline": "Informasi penting sebelum mengirimkan naskah untuk dicetak di Kotacom.id (085799520350).",
    "items": [
        {
            "question": "Berapa minimal pemesanan cetak buku untuk wilayah {{kabupaten | title}}?",
            "answer": "Tidak ada minimal order. Anda bisa mencetak mulai dari 1 eksemplar saja (Print on Demand) hingga ribuan eksemplar. Kami melayani penulis pemula yang ingin melihat contoh buku fisiknya terlebih dahulu."
        },
        {
            "question": "Apa perbedaan kertas Bookpaper dan HVS?",
            "answer": "Bookpaper memiliki warna krem kekuningan yang lembut, berbobot ringan, dan tidak memantulkan cahaya sehingga sangat nyaman dibaca berjam-jam (standar novel dan buku bacaan toko buku). Sedangkan kertas HVS berwarna putih bersih dengan tekstur lebih halus, sangat pas untuk buku ajar, skripsi, dan buku yang memiliki banyak diagram atau tabel."
        },
        {
            "question": "Apakah bisa mencetak dengan jilid Hardcover?",
            "answer": "Tentu bisa. Kami menyediakan dua pilihan jilid: Softcover (jilid lem panas lentur dan rapi) serta Hardcover (menggunakan board tebal berlapis laminasi dengan opsi jahit benang) yang kokoh dan memberikan kesan mewah."
        },
        {
            "question": "Bagaimana cara pengiriman file naskah dan apakah ada biaya pengecekan?",
            "answer": "Anda cukup mengirimkan file PDF naskah isi dan cover melalui WhatsApp 085799520350 atau tautan Google Drive. Tim pra-cetak kami akan memeriksa margin dalam (gutter), resolusi gambar, dan bleed cover secara gratis sebelum cetak dimulai."
        },
        {
            "question": "Apakah pengiriman paket buku ke {{kabupaten | title}} dijamin aman?",
            "answer": "Setiap buku dibungkus plastik shrink wrap individual agar terlindung dari kelembapan, kemudian dikemas ke dalam kardus tebal berlapis bubble wrap berlapis. Kami bekerjasama dengan ekspedisi kargo terpercaya untuk memastikan ongkir tetap terjangkau dan paket tiba dengan aman."
        }
    ]
}

# 8. Feed Posts (Articles)
feed_posts_block = {
    "_key": "feed_posts_cetak_buku",
    "_type": "marketing_feed",
    "_version": 1,
    "anchor_id": "panduan-terkait",
    "eyebrow": "PANDUAN & EDUKASI PENULIS",
    "headline": "Artikel & Tips Cetak Buku Terkait",
    "subheadline": "Pelajari panduan teknis persiapan naskah, kalkulasi biaya cetak, dan tips memilih spesifikasi kertas terbaik.",
    "source": "posts",
    "mode": "random",
    "term": "buku",
    "limit": 3,
    "layout": "grid",
    "cta_label": "Semua Artikel & Panduan",
    "cta_url": "/blog"
}

# 9. Feed Pages (Other Cities Link Graph)
feed_pages_block = {
    "_key": "feed_pages_wilayah_lain",
    "_type": "marketing_feed",
    "_version": 1,
    "anchor_id": "wilayah-terkait",
    "eyebrow": "JARINGAN PERCETAKAN NASIONAL KOTACOM",
    "headline": "Layanan Jasa Cetak Buku di Wilayah Lainnya",
    "subheadline": "Selain melayani {{kabupaten | title}}, Kotacom juga melayani pengiriman pesanan cetak buku ke berbagai kota dan kabupaten di seluruh Indonesia.",
    "source": "pages",
    "mode": "random",
    "term": "jasa-cetak-buku-",
    "limit": 6,
    "layout": "grid",
    "cta_label": "Pusat Layanan Percetakan",
    "cta_url": "/percetakan/cetak-buku"
}

# 10. WhatsApp CTA Card
whatsapp_cta_block = {
    "_key": "cta_cetak_buku",
    "_type": "marketing_whatsapp_cta",
    "_version": 1,
    "headline": "{Konsultasikan Judul & Spesifikasi Buku Anda Hari Ini|Siap Menerbitkan Naskah Anda Menjadi Buku Fisik Rapi di {{kabupaten | title}}?}",
    "body": "Hubungi tim percetakan Kotacom via WhatsApp 085799520350. Kami bantu hitungkan simulasi biaya cetak paling murah sesuai jumlah halaman, pilihan kertas Bookpaper/HVS, dan jenis jilid Anda.",
    "label": "Hubungi Percetakan via WhatsApp (085799520350)",
    "variant": "card",
    "custom_message": "Halo Kotacom, saya ingin konsultasi cetak buku untuk wilayah {{kabupaten}} (tanya harga satuan dan oplah)."
}

# 11. Hub Ecosystem CTA
cta_hub_block = {
    "_key": "cta_hub_percetakan",
    "_type": "marketing_cta",
    "_version": 1,
    "anchor_id": "ekosistem-kotacom",
    "headline": "Butuh Layanan Percetakan & Solusi Digital Lainnya di {{kabupaten | title}}?",
    "body": "Jelajahi layanan lengkap Kotacom mulai dari cetak buku, Al-Quran, kalender, kemasan produk, hingga pembuatan website profesional.",
    "primary_cta_label": "Eksplorasi Pusat Percetakan Buku",
    "primary_cta_url": "/percetakan/cetak-buku",
    "secondary_cta_label": "Katalog Produk Lengkap",
    "secondary_cta_url": "/products"
}

all_blocks = [
    hero_block,
    richtext_block,
    split_block,
    features_block,
    slider_block,
    pricing_block,
    faq_block,
    feed_posts_block,
    feed_pages_block,
    whatsapp_cta_block,
    cta_hub_block
]

# Update ec_page_templates
json_content = json.dumps(all_blocks)
escaped_content = json_content.replace("'", "''")

title_pattern = "Jasa Cetak Buku {{kabupaten | title}}"
excerpt_pattern = "{Cetak buku murah mulai 1 eksemplar hingga grosir di {{kabupaten | title}}. Pilihan Bookpaper & HVS, Softcover & Hardcover standar penerbit mayor.|Layanan percetakan buku di {{kabupaten | title}} tanpa minimal order. Tersedia kertas novel bookpaper krem, HVS modul, dan jilid lem panas presisi.}"
seo_title_pattern = "Jasa Cetak Buku {{kabupaten | title}} Murah Satuan & Grosir | Kotacom"
seo_desc_pattern = "Jasa cetak buku di {{kabupaten | title}} mulai 1 eks (satuan) hingga ribuan eks. Pilihan kertas Bookpaper/HVS, jilid Softcover lem panas & Hardcover. Cek harga via WA."

sql_update = f"""
UPDATE ec_page_templates 
SET 
  title = '{title_pattern}',
  excerpt_pattern = '{excerpt_pattern}',
  seo_title_pattern = '{seo_title_pattern}',
  seo_desc_pattern = '{seo_desc_pattern}',
  content = '{escaped_content}'::json
WHERE slug = 'template-cetak-buku-nasional';
"""

run_psql(sql_update)
print("Template 'template-cetak-buku-nasional' BERHASIL diperbarui dengan 11 blok kaya konten, copywriting antislop, dan deep spintax!")
