#!/usr/bin/env python3
"""
publish_fase4_blog_posts.py
Mempublikasikan 5 Artikel Panduan Troubleshooting Teknis & SEO Long-Tail (Fase 4)
ke CMS Emdash koleksi 'posts' lengkap dengan SEO metadata, visual image, dan 4-Point Internal Linking.
"""

import json
import urllib.request
import sys

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

POSTS = [
    # -------------------------------------------------------------------------
    # 1. Autodesk Licensing Error
    # -------------------------------------------------------------------------
    {
        "slug": "panduan-mengatasi-autodesk-licensing-error-adsklicensing",
        "title": "Panduan Mengatasi Autodesk Licensing Error (The License Manager Is Not Functioning or Improperly Installed)",
        "featured_image": "01M5KWV8EJJKB7CV260CWE60FE",
        "excerpt": "Solusi tuntas error Autodesk Licensing Service (AdskLicensing) pada AutoCAD, Revit, dan Inventor. Langkah restart service, reinstall AdskLicensing-installer, perbaikan Visual C++, hingga konfigurasi firewall.",
        "seo": {
            "title": "Cara Mengatasi Autodesk Licensing Error AdskLicensing",
            "description": "Panduan langkah teknis mengatasi error The License manager is not functioning or improperly installed pada AutoCAD & Revit. Bebas crash, 100% tuntas.",
            "canonical": "https://devk.my.id/posts/panduan-mengatasi-autodesk-licensing-error-adsklicensing",
            "image": "/_emdash/api/media/file/01M5KWV86BRV12W60C3T62WQGX.jpg",
            "noIndex": False
        },
        "content": """
Saat membuka AutoCAD, Revit, 3ds Max, atau Inventor, muncul pesan peringatan mendadak: **"The License manager is not functioning or is improperly installed. AutoCAD will now shut down."** atau kode error **ADLSDK_UPDATE_REASON_REGISTRATION_ERROR**? Masalah ini bukan disebabkan oleh file gambar project Anda yang rusak, melainkan karena komponen latar belakang bernama **Autodesk Desktop Licensing Service (ADLS)** mengalami timeout, crash, atau terblokir oleh sistem operasi Windows.

Panduan teknis dari tim teknisi **Devk** ini merangkum metode diagnosa resmi dari Autodesk Knowledge Network dan pengalaman lapangan kami saat menangani ratusan instalasi CAD jarak jauh se-Indonesia.

---

## Memahami Penyebab Utama Error AdskLicensing

Autodesk Desktop Licensing Service adalah daemon sistem lokal yang bertugas memverifikasi hak akses lisensi software setiap kali aplikasi diluncurkan. Komunikasi ini berjalan melalui port IPC lokal (localhost).

Penyebab paling sering kegagalan service ini meliputi:
1. **Service Berhenti Mendadak (Stopped Status):** Layanan `AdskLicensingService` di Windows tidak aktif secara otomatis saat booting.
2. **Konflik Mode Sleep/Hibernate:** Saat laptop masuk ke mode tidur (Sleep), koneksi agent lisensi terputus dan gagal melakukan re-handshake saat sistem dibangunkan.
3. **Kerusakan Runtime Microsoft Visual C++:** Komponen redistributable x86 atau x64 mengalami korupsi akibat update Windows 11/10 yang tidak tuntas.
4. **Pemblokiran oleh Antivirus atau Firewall:** Software keamanan pihak ketiga mencurigai aktivitas komunikasi port internal installer sebagai ancaman false-positive.
5. **Versi Installer Kadaluarsa:** File installer build lama tidak kompatibel dengan patch update Windows terbaru.

---

## Langkah 1: Memeriksa & Menjalankan Ulang Windows Service

Langkah pertama yang paling cepat tanpa perlu mengunduh file baru adalah merestart service perizinan melalui konsol Microsoft Windows Services:

1. Tekan kombinasi tombol **Windows + R** pada keyboard untuk membuka dialog *Run*.
2. Ketik **`services.msc`** lalu tekan **Enter**.
3. Gulir ke bawah hingga Anda menemukan layanan bernama **Autodesk Desktop Licensing Service**.
4. Perhatikan kolom **Status**:
   - Jika statusnya kosong (tidak berjalan), klik kanan pada nama service lalu pilih **Start**.
   - Jika statusnya sudah **Running**, klik kanan dan pilih opsi **Restart**.
5. Klik dua kali pada nama layanan, ubah **Startup type** menjadi **Automatic (Delayed Start)**, lalu klik **Apply** dan **OK**.
6. Buka kembali aplikasi AutoCAD atau Revit Anda.

---

## Langkah 2: Reinstalasi Bersih AdskLicensing Service

Jika service menolak berjalan dengan pesan error *"Error 1053: The service did not respond to the start or control request in a timely fashion"*, komponen internal installer kemungkinan telah korup. Anda wajib melakukan uninstalasi bersih:

1. Tutup seluruh aplikasi produk Autodesk yang sedang terbuka.
2. Buka Windows File Explorer dan arahkan ke direktori berikut:
   ```text
   C:\\Program Files (x86)\\Common Files\\Autodesk Shared\\AdskLicensing
   ```
3. Cari file executable bernama **`uninstall.exe`**.
4. Klik kanan pada file `uninstall.exe` lalu pilih **Run as administrator**.
5. Tunggu hingga seluruh isi folder tersebut terhapus bersih secara otomatis (jendela installer akan tertutup sendiri).
6. Unduh update installer terbaru resmi: **Autodesk Licensing Service v14+** (atau installer bawaan yang ada di master folder instalasi Autodesk Anda pada subfolder `x86\\Licensing\\AdskLicensing-installer.exe`).
7. Klik kanan pada file installer baru, pilih **Run as administrator**, dan selesaikan instruksi pemasangan di layar.
8. Restart komputer Anda lalu buka kembali software CAD.

---

## Langkah 3: Perbaikan (Repair) Microsoft Visual C++ Redistributable

Layanan Autodesk Licensing sangat bergantung pada runtime library Microsoft Visual C++. Kerusakan pustaka ini sering memicu error silent-crash saat service mencoba membaca file DLL sistem:

1. Buka Windows **Settings** > **Apps** > **Installed apps** (atau buka *Control Panel > Programs and Features*).
2. Ketik kata kunci **Visual C++** di kolom pencarian.
3. Cari paket **Microsoft Visual C++ 2015–2022 Redistributable (x64)** dan **(x86)**.
4. Klik ikon titik tiga di sebelah kanan, pilih opsi **Modify**, lalu klik tombol **Repair**.
5. Lakukan hal yang sama untuk kedua versi (x86 dan x64).
6. Lakukan reboot Windows untuk meregistrasikan ulang file DLL ke kernel sistem.

---

## Langkah 4: Konfigurasi Firewall & Antivirus Exclusions

Bila komputer Anda menggunakan antivirus seperti McAfee, Kaspersky, Avast, atau Windows Defender dengan konfigurasi ketat, tambahkan folder dan file proses perizinan ke dalam daftar pengecualian (whitelist):

* **Path Folder:**
  `C:\\Program Files (x86)\\Common Files\\Autodesk Shared\\AdskLicensing\\`
* **File Executable Utama:**
  `AdskLicensingService.exe` dan `AdskLicensingAgent.exe`
* Pastikan komunikasi port localhost pada range **FlexNet Publisher (Port 2080 dan 27000–27009)** tidak diblokir oleh software firewall jaringan kantor Anda.

---

## Tabel Komparasi: Cara Manual vs Jasa Bantuan Teknisi Devk

| Aspek Penanganan | Coba Perbaiki Sendiri | Solusi Remote Teknisi Devk |
| :--- | :--- | :--- |
| **Tingkat Kesulitan** | Perlu mengedit services, registry & runtime DLL | Bebas repot, duduk manis di depan layar |
| **Waktu Pengerjaan** | 2–4 jam riset di forum dan trial error | 15–30 menit via AnyDesk / UltraViewer |
| **Risiko Korupsi Data** | Salah hapus folder lisensi berakibat serial hangus | Penanganan aman berstandar pabrikan Autodesk |
| **Garansi Layanan** | Tidak ada jaminan tidak kambuh lagi | Garansi pendampingan remote 30 hari penuh |

---

## Butuh Bantuan Cepat? Teknisi Devk Siap Remote Sekarang

Jika Anda sedang mengejar deadline proyek rancang bangun arsitektur atau tugas akhir teknik sipil dan tidak ingin membuang waktu berkutat dengan error sistem yang rumit, tim kami siap membantu:

* Cek layanan resmi kami di [Jasa Install Software Online Remote Bergaransi](/jasa-install-software-online).
* Butuh paket software desain lain? Lihat katalog lengkap [Jasa Install AutoCAD Online](/jasa-install-autocad-online) serta [Jasa Install Autodesk Revit Online](/jasa-install-revit-online).
* Jika laptop workstation Anda sering mengalami overheating atau blue screen saat menjalankan CAD, gunakan layanan [jasa servis laptop panggilan Surabaya dan Sidoarjo](/jasa-servis-laptop-panggilan-surabaya-sidoarjo) untuk maintenance pendingin dan thermal paste.

**Hubungi WhatsApp Resmi Devk (Fast Response 15 Menit):**  
[Order Bantuan Instalasi & Fix Error CAD via WhatsApp](https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20butuh%20bantuan%20mengatasi%20Autodesk%20Licensing%20Error)
"""
    },

    # -------------------------------------------------------------------------
    # 2. Lumion 4K Render Crash & TdrDelay
    # -------------------------------------------------------------------------
    {
        "slug": "cara-mengatasi-lumion-crash-saat-render-4k-tdrdelay",
        "title": "Cara Mengatasi Lumion Crash Saat Render 4K: Solusi TdrDelay Registry, VRAM & Virtual Memory",
        "featured_image": "01M5KWY6V97FW9P2HK3DY37ECX",
        "excerpt": "Panduan teknis mengatasi crash 'GPU device instance suspended' saat render gambar 4K atau video di Lumion. Cara edit TdrDelay Registry, alokasi pagefile Windows, driver NVIDIA Studio vs Game-Ready.",
        "seo": {
            "title": "Cara Mengatasi Lumion Crash Render 4K TdrDelay Registry",
            "description": "Solusi tuntas render Lumion crash menutup sendiri dan error GPU device instance suspended. Edit TdrDelay Registry Windows & setting VRAM 4K.",
            "canonical": "https://devk.my.id/posts/cara-mengatasi-lumion-crash-saat-render-4k-tdrdelay",
            "image": "/_emdash/api/media/file/01M5KWY6KH7S63KVQ2JFKJZHZW.jpg",
            "noIndex": False
        },
        "content": """
Bagi arsitek, visualizer 3D, dan desainer interior, tidak ada yang lebih membuat frustrasi daripada Lumion yang tiba-tiba force close (menutup sendiri) tepat di tengah proses render poster 4K atau animasi video 60 FPS. Pesan error yang muncul biasanya berbunyi: **"Your graphics card has run out of memory"**, **"GPU device instance has been suspended"**, atau peringatan **"Low TdrDelay value detected"**.

Kabar baiknya: mayoritas crash ini **bukan berarti GPU kartu grafis Anda rusak**. Masalah ini berakar pada fitur keamanan bawaan sistem operasi Windows yang bernama **Timeout Detection and Recovery (TDR)** yang terlalu sensitif saat memproses beban grafis ekstrem.

---

## Mengapa Windows Memaksa Lumion Berhenti (Crash TDR)?

Secara default di Windows 10 dan Windows 11, sistem operasi memantau kartu grafis melalui scheduler internal. Jika GPU tidak memberikan respons (feedback) balik ke sistem operasi dalam waktu **2 detik**, Windows berasumsi bahwa kartu grafis telah membeku (*freeze* atau *hang*).

Sebagai mekanisme penyelamatan agar komputer tidak mengalami Blue Screen of Death (BSOD), Windows secara otomatis mereset driver grafis. Akibatnya, software render berat seperti Lumion, Enscape, atau V-Ray yang sedang menghitung ray-tracing jutaan poligon akan langsung terputus koneksi grafisnya dan mengalami crash seketika.

---

## Langkah 1: Memperpanjang Batas Waktu TdrDelay di Registry Windows

Solusi paling efektif yang direkomendasikan langsung oleh Lumion Knowledge Base dan Microsoft Developer Network adalah meningkatkan nilai toleransi **TdrDelay** dari 2 detik menjadi 10 atau 60 detik:

1. Tekan tombol **Windows + R**, ketik **`regedit`**, lalu tekan **Enter** untuk membuka Registry Editor.
2. Arahkan direktori registry di bilah kiri ke alamat berikut:
   ```text
   HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers
   ```
3. Di panel sebelah kanan, periksa apakah sudah ada key bernama **`TdrDelay`**:
   - Jika **belum ada**: Klik kanan di area kosong > pilih **New** > pilih **DWORD (32-bit) Value**. Beri nama persis: **`TdrDelay`** (perhatikan huruf besar kecilnya).
4. Klik dua kali pada nama `TdrDelay`, pilih opsi **Decimal**, lalu isi kolom **Value data** dengan angka **`10`** (memberikan toleransi jeda 10 detik) atau **`60`** untuk scene arsitektur skala kawasan kompleks.
5. Selanjutnya, buat satu key DWORD lagi dengan nama **`TdrDdiDelay`**, pilih **Decimal**, dan masukkan nilai yang sama (**`10`** atau **`60`**).
6. Tutup Registry Editor dan **Restart komputer / laptop Anda** agar parameter kernel baru dimuat.

---

## Langkah 2: Alokasi Virtual Memory (Pagefile) Windows

Render 4K membutuhkan ruang buffer memori yang sangat masif. Jika kombinasi VRAM GPU dan RAM fisik Anda habis, Windows akan membuang sisa cache ke Virtual Memory (pagefile pada harddisk/SSD). Jika alokasi pagefile diatur terlalu kecil atau dibatasi oleh sistem, Lumion akan crash out-of-memory:

1. Buka Windows Search, ketik **`sysdm.cpl`** lalu tekan Enter (*System Properties*).
2. Masuk ke tab **Advanced** > pada bagian *Performance*, klik tombol **Settings**.
3. Di jendela baru, masuk ke tab **Advanced** > pada bagian *Virtual memory*, klik tombol **Change**.
4. Hilangkan centang pada opsi *"Automatically manage paging file size for all drives"*.
5. Pilih drive sistem utama Anda (biasanya **C:** bertipe SSD NVMe).
6. Pilih opsi **Custom size**:
   - **Initial size (MB):** Masukkan nilai setara 1.5x RAM fisik (contoh jika RAM 16 GB = 24.576 MB).
   - **Maximum size (MB):** Masukkan nilai setara 2x RAM fisik (contoh jika RAM 16 GB = 32.768 MB).
7. Klik tombol **Set**, lalu klik **OK** dan restart komputer Anda.

---

## Langkah 3: Gunakan NVIDIA Studio Driver (Bukan Game Ready)

Banyak visualizer menggunakan driver kartu grafis standar gaming (*Game Ready Driver*). Driver game diprioritaskan untuk optimalisasi judul game rilisan terbaru yang sering diupdate tiap 2 minggu. Sebaliknya, **NVIDIA Studio Driver** telah melalui ratusan jam pengujian stabilitas ketat pada aplikasi kreatif seperti Autodesk, Lumion, Blender, dan Adobe:

* Buka aplikasi **NVIDIA GeForce Experience** atau **NVIDIA App**.
* Masuk ke tab **Drivers** > klik ikon titik tiga di sebelah kanan tombol *Check for updates*.
* Ubah pilihan dari **Game Ready Driver** menjadi **Studio Driver**.
* Unduh dan lakukan instalasi bersih (*Clean Installation*).

---

## Langkah 4: Optimasi Scene 3D Sebelum Final Render

Sambil menunggu render selesai, terapkan trik optimasi scene berikut agar VRAM kartu grafis tidak tercekik:
- **Gunakan Layering:** Matikan layer tanaman padat (nature items) dan mobil saat merender sudut ruangan interior.
- **Konversi Model High-Poly:** Kurangi poligon furniture hasil import SketchUp yang memiliki geometri lengkung berlebihan.
- **Tekstur Resolusi Proporsional:** Jangan gunakan tekstur 8K untuk material benda kecil di latar belakang yang hanya terlihat beberapa piksel di kamera.

---

## Matriks Rekomendasi Hardware untuk Render Lumion Stabil

| Komponen Hardware | Spesifikasi Minimum (1080p) | Spesifikasi Rekomendasi (4K Rendering) |
| :--- | :--- | :--- |
| **Kartu Grafis (GPU)** | NVIDIA RTX 3060 12GB / RTX 4060 | NVIDIA RTX 4070 Ti Super 16GB / RTX 4080 |
| **VRAM Minimum** | 8 GB GDDR6 | 16 GB GDDR6X (Wajib untuk 4K poster) |
| **Memory RAM** | 16 GB DDR4 | 32 GB – 64 GB DDR5 |
| **Storage Cache** | SSD SATA | SSD M.2 NVMe PCIe 4.0 (Kecepatan 5000+ MB/s) |
| **TdrDelay Registry** | 10 Detik | 60 Detik |

---

## Optimasi Render & Setup PC Kerja Bersama Devk

Jika Anda sering mengalami kendala render macet, butuh instalasi Lumion Pro versi terbaru yang stabil, atau ingin upgrade perangkat keras untuk studio arsitektur Anda:

* Simak katalog lengkap [Jasa Install Software Online Remote](/jasa-install-software-online).
* Pemasangan Lumion siap pakai: [Jasa Install Lumion Pro Online](/jasa-install-lumion-pro-online) dan [Jasa Install SketchUp & V-Ray Online](/jasa-install-sketchup-vray-online).
* Butuh rakitan PC workstation khusus rendering arsitektur di area Jawa Timur? Kunjungi layanan [Jasa Rakit PC Surabaya & Sidoarjo](/jasa-rakit-pc-surabaya-sidoarjo) untuk konsultasi pemilihan GPU VRAM besar dan pendingin water cooling anti-throttle.

**Konsultasi Kendala Render & Order Remote Devk:**  
[Chat WhatsApp Teknisi Devk (Tanya Solusi Render)](https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20mengalami%20kendala%20crash%20render%20Lumion)
"""
    },

    # -------------------------------------------------------------------------
    # 3. SPSS Uji Asumsi Klasik
    # -------------------------------------------------------------------------
    {
        "slug": "panduan-lengkap-uji-asumsi-klasik-regresi-linear-spss",
        "title": "Panduan Lengkap Uji Asumsi Klasik Regresi Linear di SPSS: Normalitas, Multikolinearitas, Heteroskedastisitas & Autokorelasi",
        "featured_image": "01M5KWY7ADW4KJ4NHHT41PZKJA",
        "excerpt": "Langkah demi langkah uji asumsi klasik OLS pada IBM SPSS Statistics untuk skripsi dan riset. Panduan uji Kolmogorov-Smirnov, VIF & Tolerance, Scatterplot ZPRED-SRESID, Glejser, dan Durbin-Watson.",
        "seo": {
            "title": "Panduan Uji Asumsi Klasik SPSS Regresi Linear",
            "description": "Langkah uji asumsi klasik SPSS lengkap: Uji Normalitas K-S, Multikolinearitas VIF, Heteroskedastisitas Glejser & Autokorelasi Durbin Watson untuk skripsi.",
            "canonical": "https://devk.my.id/posts/panduan-lengkap-uji-asumsi-klasik-regresi-linear-spss",
            "image": "/_emdash/api/media/file/01M5KWY74MST7M9TF13SHYDR1G.jpg",
            "noIndex": False
        },
        "content": """
Dalam pengolahan data statistik untuk skripsi, tesis, maupun riset kuantitatif menggunakan metode regresi linear berganda (*Ordinary Least Squares* / OLS), **uji asumsi klasik adalah syarat mutlak**. Pengujian hipotesis melalui Uji t (parsial) dan Uji F (simultan) tidak akan sah dan tidak dapat dipertanggungjawabkan secara akademis apabila model regresi yang Anda gunakan belum terbukti **BLUE (*Best Linear Unbiased Estimator*)**.

Banyak mahasiswa dan peneliti pemula bingung mengenai urutan klik menu di **IBM SPSS Statistics** serta kriteria pengambilan keputusan jika hasil pengujian berada di ambang batas. Berikut adalah panduan komprehensif langkah demi langkah yang praktis dan sesuai kaidah statistik baku.

---

## 1. Uji Normalitas Residual (Kolmogorov-Smirnov)

Kekeliruan paling umum mahasiswa adalah menguji normalitas pada data mentah variabel independen atau dependen. Padahal, asumsi regresi linear menuntut agar **nilai residual (kesalahan pengganggu)** yang berdistribusi normal, bukan data mentahnya.

### Langkah di SPSS:
1. Buka SPSS, masukkan dataset Anda pada lembar kerja *Data View*.
2. Klik menu **Analyze** > **Regression** > **Linear**.
3. Masukkan variabel Y ke kotak **Dependent**, dan seluruh variabel X ke kotak **Independent(s)**.
4. Klik tombol **Save** di bilah kanan dialog > pada bagian *Residuals*, beri centang pada opsi **Unstandardized** > klik **Continue** lalu **OK**.
5. Di jendela data Anda sekarang akan terbentuk satu variabel kolom baru bernama **`RES_1`**.
6. Selanjutnya, klik menu **Analyze** > **Nonparametric Tests** > **Legacy Dialogs** > **1-Sample K-S**.
7. Masukkan variabel **Unstandardized Residual (`RES_1`)** ke dalam kotak *Test Variable List*.
8. Pastikan opsi *Test Distribution* tercentang pada **Normal** > klik **OK**.

### Kriteria Keputusan:
* Lihat nilai **Asymp. Sig. (2-tailed)** pada tabel *One-Sample Kolmogorov-Smirnov Test*:
  * **Nilai Sig. > 0,05:** Model berdistribusi normal (**Asumsi Terpenuhi**).
  * **Nilai Sig. < 0,05:** Model tidak berdistribusi normal (perlu transformasi data seperti Ln/Log10 atau pembersihan data pencilan / *outliers*).

---

## 2. Uji Multikolinearitas (Tolerance & VIF)

Uji ini bertujuan memastikan tidak ada hubungan korelasi linier yang sangat kuat atau sempurna antar variabel independen di dalam model. Multikolinearitas yang tinggi menyebabkan standar error koefisien menjadi sangat besar sehingga variabel bebas tampak tidak signifikan secara statistik.

### Langkah di SPSS:
1. Klik menu **Analyze** > **Regression** > **Linear**.
2. Masukkan variabel terikat (Y) dan variabel bebas (X1, X2, dst).
3. Klik tombol **Statistics** di bilah kanan.
4. Beri centang pada kotak **Collinearity diagnostics** dan **Estimates** > klik **Continue** lalu **OK**.

### Kriteria Keputusan:
Buka tabel output **Coefficients** pada sub-kolom *Collinearity Statistics*:
* **Nilai Tolerance:** Harus lebih besar dari **0,10** (`Tolerance > 0.10`).
* **Nilai VIF (Variance Inflation Factor):** Harus lebih kecil dari **10,00** (`VIF < 10.00`).
* Jika kedua syarat terpenuhi, model dipastikan **bebas dari gangguan multikolinearitas**.

---

## 3. Uji Heteroskedastisitas (Scatterplot & Uji Glejser)

Model regresi yang baik mensyaratkan adanya **homoskedastisitas**, yaitu varians dari residual satu pengamatan ke pengamatan lain tetap konstan. Jika variansnya tidak sama, model mengalami heteroskedastisitas.

### Metode 1: Diagram Scatterplot (ZPRED vs SRESID)
1. Pada menu regresi linear, klik tombol **Plots**.
2. Masukkan variabel **`*SRESID`** ke sumbu **Y** dan variabel **`*ZPRED`** ke sumbu **X**.
3. Klik **Continue** lalu **OK**.
* **Kriteria:** Model bebas heteroskedastisitas jika titik-titik data menyebar secara acak di atas dan di bawah angka 0 pada sumbu Y tanpa membentuk pola teratur bergelombang, corong melebar, atau menyempit.

### Metode 2: Uji Glejser (Lebih Obyektif & Akurat)
Jika dosen pembimbing Anda meminta bukti angka signifikansi numerik (bukan sekadar grafik):
1. Buat variabel absolut residual dengan klik menu **Transform** > **Compute Variable**.
2. Beri nama *Target Variable*: `ABS_RES`, dan pada rumus *Numeric Expression* ketik: `ABS(RES_1)` lalu klik OK.
3. Lakukan regresi linear ulang dengan memasukkan variabel dependen baru: `ABS_RES` dan independen: `X1, X2, dst`.
* **Kriteria Uji Glejser:** Jika nilai **Sig. dari seluruh variabel independen > 0,05**, maka model **bebas dari masalah heteroskedastisitas**.

---

## 4. Uji Autokorelasi (Durbin-Watson)

Uji autokorelasi wajib dilakukan khusus untuk data yang bersifat runtut waktu (*time series*, data harian/bulanan/tahunan). Untuk data cross-section (seperti kuesioner dengan satu waktu pengambilan data), uji autokorelasi umumnya tidak disyaratkan oleh pakar ekonometrika.

### Langkah di SPSS:
1. Pada menu **Analyze** > **Regression** > **Linear** > klik tombol **Statistics**.
2. Centang opsi **Durbin-Watson** di pojok kanan bawah > klik **Continue** lalu **OK**.
3. Perhatikan tabel **Model Summary** pada kolom *Durbin-Watson (DW)*.

### Kriteria Pengambilan Keputusan:
Bandingkan nilai hitung DW dengan nilai tabel Durbin-Watson pada signifikansi 5% berdasarkan jumlah sampel ($n$) dan jumlah variabel bebas ($k$):
* **Tidak Ada Autokorelasi Positif maupun Negatif:** Jika $dU < DW < (4 - dU)$.
* **Aturan Praktis Sederhana:** Nilai Durbin-Watson yang berada di kisaran angka **1,85 s/d 2,15** umumnya dianggap aman dan bebas dari autokorelasi.

---

## Ringkasan Kriteria Kelayakan Uji Asumsi Klasik OLS

| Jenis Pengujian | Parameter Kunci Output SPSS | Syarat Lolos (Kriteria Diterima) |
| :--- | :--- | :--- |
| **Normalitas** | Asymp. Sig. (2-tailed) Kolmogorov-Smirnov | Sig. > 0,05 |
| **Multikolinearitas** | Collinearity Statistics (Tolerance & VIF) | Tolerance > 0,10 dan VIF < 10,00 |
| **Heteroskedastisitas** | Signifikansi Uji Glejser / Scatterplot | Sig. > 0,05 / Titik menyebar tanpa pola |
| **Autokorelasi** | Nilai Durbin-Watson (DW) | $dU < DW < (4 - dU)$ |

---

## Butuh Instalasi Software SPSS Cepat Tanpa Ribet?

Mengalami software SPSS error saat dibuka, lisensi trial kadaluarsa di tengah pengerjaan skripsi, atau installer corrupt? Tim teknisi **Devk** siap membantu instalasi dan aktivasi software statistik Anda dari jarak jauh:

* Cek panduan [Jasa Install Software Online Remote](/jasa-install-software-online).
* Pemasangan paket software olah data: [Jasa Install IBM SPSS Online](/jasa-install-ibm-spss-online) dan [Jasa Install SmartPLS Online](/jasa-install-smartpls-online).
* Untuk perusahaan atau institusi yang membutuhkan otomasi pemrosesan big data atau sistem analitik bisnis terintegrasi, diskusikan bersama divisi [Jasa Pembuatan Software Custom Devk](/jasa-pembuatan-software).

**Chat WhatsApp Resmi Devk untuk Bantuan Install SPSS:**  
[Order Jasa Install SPSS Remote via WhatsApp](https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20butuh%20jasa%20install%20IBM%20SPSS%20online)
"""
    },

    # -------------------------------------------------------------------------
    # 4. Dual-Boot Windows 11 & Ubuntu 24.04 LTS
    # -------------------------------------------------------------------------
    {
        "slug": "panduan-aman-dual-boot-windows-11-ubuntu-24-04-lts",
        "title": "Panduan Aman Dual-Boot Windows 11 & Ubuntu 24.04 LTS: Setup UEFI GPT, BitLocker & GRUB",
        "featured_image": "01M5KWYACPPD7ZD0JFK692J30R",
        "excerpt": "Tutorial lengkap instalasi dual-boot Windows 11 dan Ubuntu 24.04 LTS Noble Numbat tanpa takut kehilangan data. Penanganan BitLocker, Fast Startup, partisi EFI GPT, Secure Boot, dan GRUB menu.",
        "seo": {
            "title": "Panduan Dual Boot Windows 11 & Ubuntu 24.04 LTS",
            "description": "Cara install dual boot Windows 11 & Ubuntu 24.04 LTS aman tanpa hilang data. Setup BitLocker, Fast Startup, partisi EFI GPT & konfigurasi GRUB.",
            "canonical": "https://devk.my.id/posts/panduan-aman-dual-boot-windows-11-ubuntu-24-04-lts",
            "image": "/_emdash/api/media/file/01M5KWYA793T060BR8Q61V8ENV.jpg",
            "noIndex": False
        },
        "content": """
Menggabungkan ekosistem gaming dan aplikasi bisnis Windows 11 dengan lingkungan pengembangan software (*developer environment*), Docker, dan data science di **Ubuntu 24.04 LTS (Noble Numbat)** adalah konfigurasi idaman bagi banyak programmer dan mahasiswa teknik. Namun, kekhawatiran terbesar pengguna adalah **kehilangan data penting atau sistem Windows tidak bisa booting (boot loop)** akibat salah mempartisi harddisk atau bentrok fitur enkripsi.

Dengan memahami standar arsitektur **UEFI GPT modern**, instalasi dual-boot dapat dilakukan dengan 100% aman tanpa merusak partisi Windows Anda. Berikut panduan langkah komprehensif dari tim teknisi sistem operasi **Devk**.

---

## 3 Syarat Wajib di Windows 11 Sebelum Memulai Instalasi

Mayoritas kegagalan instalasi dual-boot bukan disebabkan oleh Ubuntu, melainkan karena fitur keamanan Windows 11 yang mengunci penyimpanan SSD Anda:

### 1. Nonaktifkan Fast Startup (Cegah Partisi Terkunci / Read-Only)
Fitur *Fast Startup* di Windows menggunakan teknik hybrid-hibernation saat komputer dimatikan. Kondisi ini menyebabkan partisi NTFS berstatus *locked*, sehingga installer Ubuntu tidak dapat mengecilkan ukuran partisi atau menulis file bootloader:
* Buka **Control Panel** > pilih **Power Options**.
* Klik tautan **"Choose what the power buttons do"** di bilah kiri.
* Klik **"Change settings that are currently unavailable"** (memerlukan hak administrator).
* Hilangkan centang pada opsi **"Turn on fast startup (recommended)"** lalu klik tombol **Save changes**.

### 2. Tangani Enkripsi BitLocker
Laptop modern keluaran 2022 ke atas sering kali mengaktifkan BitLocker secara otomatis pada drive C:. Installer Linux tidak dapat membaca partisi yang terenkripsi:
* Buka Windows PowerShell dengan klik kanan lalu pilih **Run as administrator**.
* Periksa status enkripsi dengan perintah:
  ```powershell
  Get-BitLockerVolume -MountPoint C:
  ```
* Jika *Protection Status* bernilai **On**, Anda wajib membackup 48-digit *Recovery Key* ke akun Microsoft Anda, lalu lakukan dekripsi sementara sebelum partisi diubah:
  ```powershell
  Disable-BitLocker -MountPoint C:
  ```
* Tunggu persentase dekripsi hingga tuntas 100% (cek dengan perintah `manage-bde -status C:`).

### 3. Buat Ruang Kosong (Unallocated Space) di Disk Management
* Tekan tombol **Windows + X** lalu pilih **Disk Management**.
* Klik kanan pada partisi utama **(C:)** > pilih **Shrink Volume**.
* Masukkan jumlah ruang yang ingin disisihkan untuk Ubuntu (direkomendasikan minimal **50.000 MB** atau 50 GB untuk kenyamanan instalasi SDK dan Docker).
* Biarkan ruang tersebut berlabel warna hitam sebagai **Unallocated Space** (jangan diformat menjadi partisi baru di Windows).

---

## Pengaturan BIOS / UEFI Motherboard

Restart komputer Anda dan tekan tombol akses BIOS (biasanya tombol **F2**, **Del**, atau **F12** tergantung merk laptop/motherboard):
* **SATA Operation / Storage Mode:** Pastikan diatur ke **AHCI** (jika masih *Intel RST / RAID On*, ubah ke AHCI agar kernel Linux dapat mendeteksi storage NVMe).
* **Boot Mode:** Wajib disetel ke **UEFI Only** (matikan opsi Legacy Support / CSM).
* **Secure Boot:** Ubuntu 24.04 LTS telah memiliki tanda tangan digital resmi dari Microsoft (*Canonical Signed Shim*). Anda **tetap dapat membiarkan Secure Boot aktif (Enabled)**. Namun jika flashdisk installer tidak terdeteksi saat booting awal, Secure Boot dapat dinonaktifkan sementara dan diaktifkan kembali setelah driver selesai dikonfigurasi.

---

## Tahap Instalasi Ubuntu 24.04 LTS

1. Buat bootable USB Ubuntu 24.04 LTS menggunakan aplikasi **Rufus** (Pilih skema partisi **GPT** dan target system **UEFI (non CSM)**).
2. Tancapkan flashdisk ke laptop, nyalakan komputer, lalu tekan tombol **Boot Menu** (F12 di Dell/Lenovo, F9 di HP, atau F8 di ASUS).
3. Pilih opsi **Try or Install Ubuntu**.
4. Pada tahap *Installation type*, Anda akan diberikan dua pilihan:
   - **Pilihan Otomatis ("Install Ubuntu alongside Windows Boot Manager"):** Opsi terbaik bagi pemula. Installer akan secara otomatis menggunakan *Unallocated Space* yang telah kita buat sebelumnya.
   - **Pilihan Manual ("Something else / Manual Partitioning"):** Buat partisi Root (`/`) bertipe file system **Ext4** pada sisa unallocated space. Pastikan kolom *Device for boot loader installation* diarahkan ke partisi **EFI System Partition (ESP)** bawaan Windows (biasanya berukuran 100–260 MB dengan format FAT32).
5. Lanjutkan pembuatan username, password, dan tunggu proses instalasi selesai.
6. Klik **Restart Now** dan cabut flashdisk USB ketika muncul perintah di layar.

---

## Mengatur Menu GRUB Bootloader & Default OS

Setelah reboot, komputer akan disambut oleh menu **GRUB Bootloader** berwarna ungu di mana Anda dapat memilih masuk ke *Ubuntu* atau *Windows Boot Manager*.

Jika Anda ingin menjadikan Windows 11 sebagai sistem operasi default yang langsung menyala otomatis tanpa harus menekan keyboard:
1. Masuk ke terminal Ubuntu (Ctrl + Alt + T), lalu jalankan perintah:
   ```bash
   sudo nano /etc/default/grub
   ```
2. Cari baris `GRUB_DEFAULT=0`, lalu ubah angkanya sesuai urutan menu Windows (atau gunakan `GRUB_DEFAULT=saved` dan tambahkan `GRUB_SAVEDEFAULT=true` agar GRUB mengingat pilihan OS terakhir Anda).
3. Anda juga dapat mempercepat durasi hitung mundur tampilan menu dengan mengubah baris:
   ```bash
   GRUB_TIMEOUT=5
   ```
4. Simpan perubahan dengan menekan **Ctrl + O**, tekan **Enter**, lalu keluar dengan **Ctrl + X**.
5. Update konfigurasi bootloader dengan mengeksekusi:
   ```bash
   sudo update-grub
   ```

---

## Pemasangan Driver Kartu Grafis NVIDIA di Ubuntu

Bagi pengguna laptop atau PC dengan kartu grafis diskrit NVIDIA, pasang driver proprietary resmi agar performa grafis optimal dan konsumsi baterai efisien:
```bash
sudo ubuntu-drivers list
sudo ubuntu-drivers install
sudo reboot
```
Periksa keberhasilan instalasi driver kartu grafis dengan menjalankan perintah terminal:
```bash
nvidia-smi
```

---

## Ingin Pasang OS Bersih Tanpa Risiko? Serahkan ke Teknisi Devk

Bagi Anda yang berdomisili di wilayah Surabaya, Sidoarjo, dan sekitarnya serta tidak ingin mengambil resiko kehilangan file skripsi atau dokumen kantor berharga saat melakukan partisi dual-boot:

* Gunakan layanan panggilan teknisi kami di [Jasa Install & Servis Komputer Surabaya Sidoarjo](/jasa-install-komputer-surabaya-sidoarjo).
* Kami melayani instalasi workstation khusus Linux: [Jasa Install Linux Ubuntu / Debian Surabaya](/jasa-install-linux-surabaya) serta [Jasa Install Ulang Windows 11 / 10 Surabaya Sidoarjo](/jasa-install-ulang-windows-surabaya-sidoarjo).
* Setelah sistem operasi dual-boot Anda siap digunakan, manfaatkan [Jasa Install Software Online Remote](/jasa-install-software-online) untuk pemasangan aplikasi teknik, arsitektur, dan desain grafis Anda.

**Booking Teknisi Panggilan ke Rumah / Kantor Anda:**  
[Hubungi WhatsApp Teknisi Devk (Area Surabaya & Sidoarjo)](https://wa.me/6285799520350?text=Halo%20Devk,%20saya%20butuh%20jasa%20install%20dual%20boot%20Windows%20Ubuntu)
"""
    },

    # -------------------------------------------------------------------------
    # 5. Laptop Overheat 90C & Thermal Throttling
    # -------------------------------------------------------------------------
    {
        "slug": "laptop-panas-90-derajat-thermal-throttling-solusi-pasta-kering",
        "title": "Laptop Panas 90°C & Thermal Throttling: Penyebab Pasta Kering, Efek Pump-Out & Solusi Tuntas",
        "featured_image": "01M5KWYDKVW7Z8AC073K7QW5FW",
        "excerpt": "Solusi laptop gaming dan kerja yang panas menyentuh 90-100°C serta FPS drop patah-patah. Memahami thermal throttling, fenomena pump-out pasta encer, pembersihan sirip heatsink tembaga, hingga trik power plan 99%.",
        "seo": {
            "title": "Laptop Panas 90°C Thermal Throttling Solusi Pasta Kering",
            "description": "Cara mengatasi laptop panas 90-100 derajat Celsius & lag patah-patah thermal throttling. Penjelasan pump-out effect pasta thermal & deep clean heatsink.",
            "canonical": "https://devk.my.id/posts/laptop-panas-90-derajat-thermal-throttling-solusi-pasta-kering",
            "image": "/_emdash/api/media/file/01M5KWYDDM82YVQ2QSJXWQQXRP.jpg",
            "noIndex": False
        },
        "content": """
Saat sedang bermain game berat, merender video di Premiere Pro, atau mengekspor 3D di SketchUp, tiba-tiba kipas laptop Anda meraung sangat bising, bodi laptop di dekat keyboard terasa membakar jari, dan performa seketika drop drastis (*stuttering* patah-patah)? Jika Anda mengecek temperatur prosesor melalui aplikasi HWiNFO64 atau HWMonitor dan angka suhu menembus **90°C hingga 100°C**, laptop Anda sedang mengalami kondisi **Thermal Throttling**.

Thermal Throttling adalah mekanisme pertahanan darurat di mana CPU atau GPU memangkas kecepatan frekuensi clock-nya secara paksa agar silikon chip tidak terbakar atau rusak permanen. Mari kita bedah tuntas penyebab teknis di balik panas ekstrem ini serta solusi perbaikannya.

---

## 3 Penyebab Utama Laptop Menjadi Oven Berjalan

Banyak pengguna mengira laptop panas semata-mata karena spesifikasi laptop mereka kurang tinggi. Padahal, masalah utamanya hampir selalu berada pada **kegagalan sistem pembuangan panas mekanis**:

### 1. Jebakan "Debu Karpet" (Dust Carpet) di Sirip Heatsink
Udara dingin disedot oleh kipas dari bawah bodi laptop lalu ditiupkan keluar melewati sirip-sirip tembaga tipis heatsink di bagian samping atau belakang. Seiring pemakaian 6–12 bulan, partikel debu halus dan serat kain akan terperangkap di celah sirip tembaga, membentuk lapisan padat seperti karpet kain. Akibatnya, meski kipas berputar pada 6000 RPM, hembusan udara panas sama sekali tidak dapat keluar dan terperangkap di dalam casing laptop.

### 2. Pasta Thermal Kering & Rusak
Pasta pendingin (thermal paste) berfungsi mengisi celah mikroskopis antara permukaan chip silikon prosesor dengan pelat tembaga heatsink agar transfer panas berlangsung efisien. Di atas suhu operasional 80°C secara berkelanjutan, minyak silikon pada pasta murahan akan menguap, meninggalkan serbuk kering yang justru berubah fungsi menjadi isolator penahan panas.

### 3. Fenomena "Pump-Out Effect" pada Laptop Bare-Die
Berbeda dengan prosesor PC desktop yang dilindungi oleh pelindung logam tebal (*Integrated Heat Spreader* / IHS), prosesor laptop berbentuk **bare die silikon terbuka**. Karena ruang yang sangat sempit dan siklus ekspansi-kontraksi termal yang cepat, thermal paste yang memiliki tingkat kekentalan (*viscosity*) rendah—seperti pasta desktop populer jenis Arctic MX-4 standar—akan tertekan keluar ke pinggir chip hanya dalam waktu 2–4 minggu pemakaian! Fenomena ini dikenal sebagai **Pump-Out Effect**, yang menyebabkan laptop kembali panas membara tak lama setelah baru diservis di tempat sembarangan.

---

## Solusi Darurat: Trik Power Plan "99% Maximum Processor State"

Jika Anda sedang berada di luar kota, memiliki deadline mendesak, dan belum sempat membawa laptop ke bengkel servis, Anda dapat mengaktifkan trik sementara ini untuk menurunkan suhu sebesar **15°C s/d 20°C secara instan**:

1. Buka Windows Search, ketik **`Edit power plan`** lalu tekan Enter.
2. Klik tautan **Change advanced power settings**.
3. Gulir ke bawah dan klik tanda plus pada opsi **Processor power management**.
4. Buka sub-menu **Maximum processor state**:
   - Ubah nilai **On battery** dan **Plugged in** dari **100%** menjadi **`99%`**.
5. Klik tombol **Apply** lalu **OK**.

### Apa yang Terjadi di Balik Angka 99%?
Dengan menurunkan batas dari 100% ke 99%, Windows secara otomatis menonaktifkan fitur **Intel Turbo Boost** atau **AMD Precision Boost**. Prosesor akan dipaksa berjalan pada kecepatan *Base Clock* dasarnya (misalnya bertahan di 2.4 GHz dan tidak melompat ke 4.5 GHz). 

* **Kelebihan:** Suhu prosesor langsung anjlok dari 95°C ke kisaran aman 70°C, suara kipas mendadak senyap, dan thermal throttling berhenti seketika.
* **Kelemahan:** Anda memangkas sekitar 20% s/d 30% potensi performa puncak prosesor Anda. Trik ini hanyalah pertolongan pertama (P3K) dan bukan solusi permanen.

---

## Solusi Tuntas: Standar Perawatan Deep Cleaning & Repasting Berkualitas

Untuk memulihkan performa puncak 100% laptop tanpa harus mengorbankan kecepatan Turbo Boost, langkah perawatan fisik wajib dilakukan:

### 1. Pembongkaran & Pembersihan Jalur Heatsink
* Buka casing belakang laptop dengan obeng presisi.
* Lepaskan konektor baterai utama sebelum menyentuh komponen motherboard untuk mencegah konsleting listrik statis.
* Buka modul heatsink tembaga dan lepas kipas blower.
* Bersihkan debu karpet pada kisi-kisi radiator pendingin menggunakan kuas antistatis dan semprotan kaleng udara bertekanan (*canned compressed air*).
* Lumasi poros bearing kipas dengan pelumas khusus elektronik jika putarannya mulai seret.

### 2. Pembersihan Sisa Pasta Lama
* Gunakan cairan **Isopropyl Alcohol (IPA) dengan kemurnian 90%+** dan kain microfiber bebas serat untuk mengangkat kerak pasta kering lama pada permukaan die prosesor dan heatsink hingga mengkilap sempurna. Hindari penggunaan minyak kayu putih atau alkohol medis 70% yang mengandung kadar air tinggi.

### 3. Pemilihan Material Antarmuka Termal Terbaik untuk Laptop
Gunakan material yang memiliki ketahanan pump-out tinggi dan konduktivitas panas kelas atas:
* **Thermal Paste High-Viscosity (Kental):** *Noctua NT-H2*, *Thermal Grizzly Kryonaut Extreme*, atau *Cooler Master MasterGel Maker*.
* **Phase Change Material (PCM Pad):** *Honeywell PTM7950*. Bahan ini berbentuk padat saat suhu dingin dan mencair mengisi rongga mikro saat suhu mencapai 45°C. Sangat tahan terhadap efek pump-out dengan masa pakai hingga bertahun-tahun tanpa perlu repaste ulang.

### 4. Urutan Pengencangan Baut Heatsink (Diagonal Torque)
Saat memasang kembali pelat heatsink, perhatikan nomor urut yang tertera pada logam heatsink (biasanya angka 1, 2, 3, 4, 5, 6). Kencangkan baut secara bersilang sedikit demi sedikit secara merata agar tekanan pasta tersebar seimbang dan tidak meretakkan kaca silikon prosesor.

---

## Perbandingan Suhu Operasional Sebelum & Sesudah Servis di Devk

| Kondisi Pengujian | Sebelum Servis (Debu + Pasta Kering) | Sesudah Servis (Deep Clean + PTM7950) |
| :--- | :--- | :--- |
| **Suhu Idle (Desktop Ringan)** | 60°C – 70°C (Kipas sering berputar kencang) | 40°C – 48°C (Kipas senyap nyaris tanpa suara) |
| **Suhu Gaming / Render Puncak** | 95°C – 102°C (**Thermal Throttling Ekstrem**) | 72°C – 82°C (Frekuensi Turbo stabil maksimal) |
| **Stabilitas Frame Rate (FPS)** | Drop parah dari 120 FPS ke 25 FPS tiba-tiba | Stabil konsisten tanpa lonjakan lag patah-patah |
| **Suhu Permukaan Keyboard** | Panas menyengat pada telapak tangan | Hangat wajar, sirkulasi udara laptop lancar |

---

## Layanan Servis Laptop & Ganti Pasta Panggilan di Surabaya – Sidoarjo

Tidak memiliki alat pembongkar presisi, takut casing patah, atau khawatir salah memasang heatsink? Teknisi perangkat keras **Devk** siap datang langsung ke rumah atau kantor Anda:

* Konsultasikan langsung di [Jasa Servis Laptop Panggilan Surabaya & Sidoarjo](/jasa-servis-laptop-panggilan-surabaya-sidoarjo).
* Layanan instalasi komputer lengkap: [Jasa Install & Servis Komputer Surabaya Sidoarjo](/jasa-install-komputer-surabaya-sidoarjo) serta [Jasa Rakit PC Gaming & Workstation Surabaya](/jasa-rakit-pc-surabaya-sidoarjo).
* Butuh software pendukung untuk pengetesan beban grafis dan stabilitas sistem? Kunjungi direktori [Jasa Install Software Online Remote](/jasa-install-software-online).

**Panggil Teknisi Servis Laptop Devk ke Lokasi Anda Hari Ini:**  
[Chat WhatsApp Teknisi Laptop Devk (Konsultasi Suhu Panas)](https://wa.me/6285799520350?text=Halo%20Devk,%20laptop%20saya%20panas%2090%20derajat%20dan%20butuh%20ganti%20pasta%20thermal)
"""
    }
]

def main():
    print("=== MEMULAI PUBLIKASI 5 ARTIKEL BLOG FASE 4 DI EMDASH ===")
    
    # Ambil daftar post yang ada untuk cek duplikasi
    existing = call_mcp("content_list", {"collection": "posts", "limit": 100})
    existing_slugs = {item["slug"]: item["id"] for item in existing.get("items", [])}
    print(f"Post eksisting di Emdash: {list(existing_slugs.keys())}")
    
    published_count = 0
    for post in POSTS:
        slug = post["slug"]
        print(f"\nProcessing post: '{slug}'...")
        
        # Format payload data
        data_payload = {
            "title": post["title"],
            "content": post["content"].strip(),
            "excerpt": post["excerpt"].strip(),
            "featured_image": post["featured_image"]
        }
        
        seo_payload = post["seo"]
        
        if slug in existing_slugs:
            item_id = existing_slugs[slug]
            print(f"Post '{slug}' sudah ada dengan id={item_id}. Memperbarui konten via content_update...")
            res = call_mcp("content_update", {
                "collection": "posts",
                "id": item_id,
                "data": data_payload,
                "seo": seo_payload,
                "status": "published"
            })
            print(f"Updated: {res.get('item', {}).get('id', item_id)}")
            published_count += 1
        else:
            print(f"Membuat post baru '{slug}' via content_create...")
            res = call_mcp("content_create", {
                "collection": "posts",
                "slug": slug,
                "status": "published",
                "data": data_payload,
                "seo": seo_payload
            })
            created_item = res.get("item", {})
            created_id = created_item.get("id")
            print(f"Created: id={created_id}, slug={created_item.get('slug')}")
            
            # Pastikan status published
            if created_id and created_item.get("status") != "published":
                print(f"Publishing {created_id}...")
                call_mcp("content_publish", {
                    "collection": "posts",
                    "id": created_id
                })
            published_count += 1

    print(f"\n=== SUKSES! Seluruh {published_count} artikel telah dipublikasikan di Emdash ===")

if __name__ == "__main__":
    main()
