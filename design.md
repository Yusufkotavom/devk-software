# design.md — Kotacom (devk-software / EmDash)

> Dokumen arah visual yang **grounded ke referensi situs nyata** dan **dipetakan ke design token yang sudah ada** (`src/styles/tokens.css`, `marketing.css`, `Base.astro`).
> Tujuan: mengubah tampilan yang sekarang monoton (semua `section.band` berlatar putih) menjadi **editorial-print warm** yang khas untuk bisnis percetakan + IT.

---

## 1. Positioning & prinsip

Kotacom = **studio percetakan buku + solusi IT**. Bukan SaaS, bukan agency motion. Audiens: penulis, sekolah, perusahaan yang butuh cetak & sistem. Maka estetika yang tepat:

- **Craft & tactility** (kertas, tinta, jilid) → warm canvas + serif editorial + tekstur halus, bukan gradient-glass/SaaS.
- **Editorial rhythm** → headline serif besar, label mono, section yang punya "bab" jelas (berganti warna/gambar), bukan tumpukan putih.
- **Kredibilitas bisnis** → kontrak yang jelas: harga, proses, portofolio, garansi, FAQ.

3 prinsip kerja:
1. **Satu aksen, konsisten** — merah `#991b1b` (sudah ada) untuk CTA & angka penting; amber `#d97706` sebagai aksen sekunder (highlight/kicker).
2. **Setiap section punya "signature"** — minimal beda di latar (putih ⇄ cream), sesekali band gelap penuh. Tidak ada dua section identik berurutan tanpa jeda visual.
3. **Gambar karena bisnisnya visual** — buku/jilid/kertas adalah produk. Portofolio harus berupa foto/illustrasi, bukan kotak abu kosong.

---

## 2. Referensi (dari situs terkenal / terkurasi)

Diambil dari galeri terkurasi **Palate** (creative-studio), **Awwwards**, dan situs percetakan nyata (Mixam, Pixartprinting, Doxzoo):

| Referensi | Yang diambil |
|---|---|
| **Awwwards site** (awwwards.com) | *Canvas warm abu `#e9e9e9`, satu display title ink-hitam 120px+, eyebrow mono kecil di pojok.* → pola **kanvas warm + headline serif besar + label mono**. |
| **Reform Collective** (palatemcp.com/gallery/reform-collective) | *Krem ` #F9F8EE ` seperti kertas, wordmark serif/grotesk, bentuk organik stiker.* → **kanvas krem "kertas"** sebagai warna dasar. |
| **Miux** (palatemcp.com/gallery/miux) | *Palet cream-and-stone, tipografi editorial tertahan, case-study horizontal.* → **cream + stone**, restraint. |
| **Brand Appart** (palatemcp.com/gallery/brand-appart) | *Display chunky-sans, parchment cream, aksen oranye.* → **aksen hangat (amber/oranye)** di atas krem. |
| **Letude** (palatemcp.com/gallery/letude) | *Latar merah bold + wordmark di atas fotografi.* → **band merah penuh** untuk momen CTA/penutup. |
| **Huge** (palatemcp.com/gallery/huge) | *Brutalist, sudut tajam, blok warna berani.* → **section color-block tegas** (bukan serba lembut). |
| **Geex Arts** (palatemcp.com/gallery/geex-arts) | *Pasangan serif display (Instrument Serif) + grotesk book.* → **Instrument Serif + Inter** (sudah ter-load!). |
| **Mixam / Pixartprinting / Doxzoo** | Anatomi halaman cetak: **kalkulator/instan quote, pilihan jilid-kertas-ukuran, galeri portofolio, proses 1-4 langkah, FAQ**.* → **anatomi blok** di §6. |
| **ui-ux-pro-max** (database) | Rekomendasi tipografi editorial/publishing: **Libre Bodoni / Public Sans** (mood: magazine, editorial, print). Di project digantikan **Instrument Serif / Inter** yang ekuivalen & sudah ada. |

**Yang SENGAJA tidak diambil:** estetika green/biophilic (dari mesin rekomendasi)—tidak cocok untuk percetakan. Juga tidak full-Bauhaus 3-warna (terlalu keras untuk brand hangat ini).

---

## 3. Palet (light mode) — dipetakan ke token

Semua memakai variabel yang SUDAH ada; cukup ubah nilainya (bukan sistem baru). Nilai usulan = token `light`.

| Peran | Token | Sekarang | Usulan | Dipakai untuk |
|---|---|---|---|---|
| Kanvas dasar | `--color-bg` | `#fafafa` | **`#F7F3EC`** (warm paper) | latar halaman, band default |
| Permukaan (card) | `--color-surface` | `#ffffff` | `#FFFFFF` | card, form, nav |
| Sunken / band selang | `--color-sunken` | `#f2f1ee` | **`#EFE8DD`** (cream stone) | band selang-seling, panel fitur |
| Night / band gelap | `--color-night` | `#141312` | **`#17110D`** (ink hangat) | CTA band, footer aksen |
| Teks utama | `--color-text` | `#171717` | `#1A1712` (ink) | headline, body |
| Teks sekunder | `--color-text-secondary` | `#525252` | `#5B5347` (warm gray) | body sekunder |
| Muted/label | `--color-muted` | `#6b6b6b` | `#877C6B` | label mono, meta |
| Aksen utama | `--color-brand-accent` | `#991b1b` | **`#B42318`** (red) | CTA, angka, ikon kunci |
| Aksen sekunder | `--color-accent` | `#d97706` | **`#D97706`** (amber) | eyebrow, highlight harga, underline |
| Garis | `--color-border` | `#e5e5e5` | **`#E4DBCB`** (warm line) | pembatas band, hairline |

Aturan kontras: body teks pada kanvas krem harus ≥ 4.5:1 (ink `#1A1712` di `#F7F3EC` = aman). Aksen merah hanya untuk elemen besar/bold atau ikon + label pendamping (jangan teks paragraf).

Dark mode: pertahankan dukungan `light-dark()`; nilainya disesuaikan sewarna (kanvas gelap hangat `#141210`, teks krem, aksen merah/amber di-boost).

---

## 4. Tipografi

Yang **sudah ter-load** di `astro.config.mjs` — manfaatkan, tak perlu font baru:
- `--font-display`: **Instrument Serif** → headline H1/H2, angka besar (harga).
- `--font-body`: **Inter** → body, tombol, nav.
- `--font-mono`: **JetBrains Mono** → *eyebrow/kicker*, label kecil, metadata ("12 Apr 2026 · 3 min").

Skala (sesuaikan token `--font-size-*`):
- Display hero: `clamp(2.75rem, 2rem + 3.4vw, 5rem)`, `--font-weight-display` 400 (serif tebal-lebar via optical size), `letter-spacing -0.02em`, `line-height 0.98`.
- H2 section: `clamp(2rem, 1.4rem + 2.2vw, 3.25rem)` serif.
- Body: 1rem–1.125rem Inter, `line-height 1.6`, warna `--color-text-secondary`.
- Eyebrow: JetBrains Mono 0.75rem, uppercase, `letter-spacing .14em`, warna amber atau muted, dengan prefix `→`/titik merah.

Aturan: **jangan** set headline pakai Inter bold lagi untuk hero/section — ganti ke serif display agar ada kontras "editorial". Minimal satu elemen mono per section sebagai penanda.

---

## 5. Ritme section (band system)

Sistem `.band` sudah ada (garis + crosshair rail). Yang kurang: **variasi latar**. Aturan:

- **Selang-seling**: band default (kanvas krem) → band `--sunken` (cream stone) → dst. Terapkan lewat utility optional di block (mis. `.band--tint`), atau auto `nth-of-type` ganjil/genap untuk band non-hero.
- **Dark anchor**: `CTA` dan `WhatsAppCTA` jadi **band penuh gelap** (`--color-night` + `--glow-dusk`, teks `--color-on-night`, tombol merah). Sebelum footer → menutup halaman dengan kontras kuat.
- **Signature hero**: hero beda dari semua — latar kanvas + blob/gradient halus (`--glow-daylight`) + display serif besar + eyebrow mono + visual (foto buku / diagram orbital yang sudah ada diberi warna aksen).
- Spacing: `--section-space` tetap; tapi **beri jeda visual** lewat perubahan latar, bukan hanya whitespace.

Target ritme satu halaman (tak ada dua section identik berturut-turut):
`Hero (kanvas+visual)` → `Proof/logos (sunken)` → `Solusi grid (kanvas)` → `Proses 1-4 (sunken)` → `Portofolio galeri (kanvas, imagery)` → `Harga (sunken atau panel)` → `Testimoni (kanvas)` → `FAQ (sunken)` → `CTA (gelap)` → `Footer`.

---

## 6. Anatomi blok (komponennya sudah ada)

| Blok (file `src/components/blocks/…`) | Treatment target |
|---|---|
| **Hero.astro** | Serif display besar + eyebrow mono + 2 CTA (merah solid + outline). Visual: foto buku/jilid atau diagram orbital diberi aksen merah/amber (bukan garis abu). Latar kanvas + glow halus. |
| **Features/Stats** | Panel `--sunken` (sekali) atau `--night` (sekali) — bukan putih semua. Ikon aksen merah, angka besar serif. |
| **Process/Steps** | Nomor besar serif + garis penghubung; latar sunken. Wajib ada (ekspektasi halaman cetak: 1 upload → 2 proof → 3 produksi → 4 kirim). |
| **Pricing.astro** | Kartu harga di atas latar kontras; harga pakai serif besar + aksen amber untuk "Mulai 15rb"; highlight paket populer dengan border merah. |
| **Feed/Portofolio** | **Ganti kotak abu → gambar**: pakai gradient brand yang sudah ada (`marketing.css` L625–657) sebagai placeholder berwarna, idealnya foto sampul/jilid. Grid 2–3 kolom, rasio konsisten. |
| **Testimonials** | Band kontras (sunken/night), kartu putih, tanda kutip serif besar, aksen merah pada nama. |
| **FAQ.astro** | Accordion; item aktif dapat border/aksen merah; latar sunken. |
| **Tab/Comparison** | Tabel dengan header berwarna (bukan abu), baris stripe `--sunken`, aksen untuk kolom rekomendasi. |
| **CTA / WhatsAppCTA** | **Band gelap penuh** + tombol merah/amber. Ini "closing statement". |
| **Footer (Base.astro)** | Boleh ink gelap atau tetap terang dengan aksen merah pada heading kolom; jaga keterbacaan. |

Hindari: kartu-berisi-kartu berlapis (card-in-card) — lihat aturan "surface rule" di skill.

---

## 7. Gambar, motif, & tekstur

- **Imagery wajib** di hero & portofolio. Kalau belum ada aset: pakai **gradient brand** (merah→amber) + label mono sebagai "tempat sampul buku" — jauh lebih hidup daripada abu.
- **Motif**: garis/crosshair rail dipertahankan (itu identitas), tapi warna garis disesuaikan warm (`--color-border` krem). Boleh tambah bentuk geometris kecil (lingkaran/segitiga) warna aksen sebagai "stempel".
- **Tekstur halus** (opsional): noise/paper grain sangat rendah opasitas pada hero — memperkuat kesan cetak. Jangan berlebihan.

---

## 8. Motion

- Reveal-on-scroll boleh, **tapi wajib fallback**: `@media (prefers-reduced-motion: reduce)` → tampil langsung (opacity 1, transform none). Dan jangan pernah `opacity:0` permanen bila JS gagal.
- Transisi 150–300ms ease-out; hover pada kartu/tombol.

---

## 9. Do / Don't

Do:
- Selang-seling latar tiap section; minimal 1 band gelap per halaman panjang.
- Serif display untuk headline; mono untuk label; satu aksen konsisten.
- Foto produk/portofolio; angka & harga besar.
- Kontras teks ≥ 4.5:1; focus state jelas.

Don't:
- Semua section putih identik. ❌
- Gradient-glass / aurora SaaS, emoji sebagai ikon. ❌
- Kotak placeholder abu sebagai "gambar". ❌
- Tiga warna solid penuh (Bauhaus) — terlalu keras untuk brand ini. ❌

---

## 10. Peta implementasi (langkah teknis)

1. **Token** (`src/styles/tokens.css` light + dark): ubah `--color-bg`, `--color-sunken`, `--color-night`, `--color-border`, `--color-brand-accent`→`#B42318`, `--color-accent`→amber sesuai §3.
2. **Tipografi**: arahkan `.section-headline`/hero ke `--font-display` (Instrument Serif); eyebrow ke `--font-mono`.
3. **Band**: tambah util `.band--tint` & `.band--dark` di `marketing.css`; auto-alternate untuk band non-hero; set `CTA`/`WhatsAppCTA` = `.band--dark`.
4. **Feed/Portofolio**: ganti placeholder → gradient/foto (pakai warna di `marketing.css` L625–657).
5. **Hero**: terapkan glow + serif display + aksen diagram.
6. **Motion**: audit `opacity:0` → tambah reduced-motion fallback.
7. **Verifikasi**: build + `astro check` bersih; screenshot before/after (home + service); cek kontras & mobile 375/768/1024/1440.

Acceptance: halaman tidak lagi punya ≥2 section putih berturut tanpa jeda; hero punya visual; portofolio bergambar; ada 1 band gelap; semua kontras lulus.

---

## 11. Status saat init dokumen ini
- Desain live: **monoton** — semua `.band` putih, satu kolom, warna aksen hampir tak terpakai, card abu. (Audit 2026-11-17.)
- Token warm (`--color-sunken`, `--color-night`, amber) **sudah ada** tapi belum dipakai blok.
- Font editorial (Instrument Serif) **sudah ter-load** tapi headline masih Inter.
→ Semua lever di atas bisa dicapai tanpa menambah dependency.
