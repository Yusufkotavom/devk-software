# design.md — Kotacom Design System v2 · "Modern Warm-Tech"

> **Status:** STANDAR (menggantikan draft "Editorial Print Warm" yang ditolak — terlalu kaku/kertas).
> **Cocok untuk:** bisnis **IT + percetakan**. Modern & hangat, bukan Vercel-mono kaku, bukan paper/editorial.
> **Sumber kebenaran kode:** `src/styles/tokens.css` (default) → di-override `src/styles/theme.css` → polish blok di `src/styles/marketing.css`. Font di `astro.config.mjs`.
> **Preview:** `public/design-sample.v2.html`. **Branch kerja:** `design/v2-warm-tech`.

---

## 1. Prinsip

1. **Modern tapi hangat.** Sudut membulat (8–24px), soft shadow berwarna hangat, bukan garis tipis/kotak kaku.
2. **Dua identitas dijembatani warna.** *Cetak* = merah→oranye; *IT* = ungu/indigo. Disatukan lewat **gradien brand** (bukan 3 warna blok ala Bauhaus, bukan monokrom).
3. **Produk terasa.** Hero & fitur memakai bahasa "app/product" (mockup, bento, chip status), bukan katalog cetak jadul.
4. **Satu aksen gradient, konsisten.** Gradient hanya untuk momen bernilai (headline accent, CTA, tile portofolio, badge populer). Sisanya ink/netral agar tak jadi "swatch sheet".
5. **Gerak halus.** Reveal on-scroll & hover 150–220ms, selalu ada fallback `prefers-reduced-motion`.

---

## 2. Palette (light; dark tersedia via `light-dark()`)

| Peran | Token | Light | Dark | Pakai untuk |
|---|---|---|---|---|
| Kanvas | `--color-bg` | `#FBFAF8` | `#0C0D10` | latar halaman |
| Permukaan | `--color-surface` | `#FFFFFF` | `#141519` | kartu, nav, form |
| Fill | `--color-fill` / `--color-sunken` | `#F3F1EC` | `#16171B` | band selang, chip, input |
| Ink | `--color-night` / `--color-text` | `#0F1013` | `#F2F3F5` | teks utama, band gelap |
| Teks sekunder | `--color-text-secondary` | `#3A3C43` | `#B8BCC4` | body sekunder |
| Muted | `--color-muted` | `#6B6E76` | `#8B90A0` | label, meta |
| Garis | `--color-border` | `rgba(15,16,19,.10)` | `rgba(255,255,255,.10)` | hairline kartu/band |
| Aksen cetak | `--color-brand-accent` | `#F04438` | `#FF6B5E` | CTA sekunder, ikon, harga |
| Aksen hangat | `--color-accent` | `#FB923C` | `#FBBF24` | highlight, eyebrow dot |
| Aksen IT | *(gradient)* | `#6366F1` / `#8B5CF6` | — | ujung gradien, aksen tech |

**Gradien brand**
```
--v2-grad:      linear-gradient(115deg,#F04438 0%,#FB923C 42%,#8B5CF6 100%);
--v2-grad-soft: linear-gradient(115deg, rgba(240,68,56,.14), rgba(139,92,246,.14));
--v2-mesh:      radial-gradient(42% 50% at 16% 6%, rgba(240,68,56,.16), transparent 60%),
                radial-gradient(40% 55% at 84% 0%, rgba(99,102,241,.16), transparent 62%),
                radial-gradient(50% 60% at 60% 28%, rgba(251,146,60,.12), transparent 65%);
```
Aturan: gradient text/CTA **jangan** untuk paragraf. Kontras teks di atas gradient putih `#fff` harus ≥ 4.5:1.

---

## 3. Tipografi (sudah ter-load di `astro.config.mjs`)

- **Display — `--font-display` = Space Grotesk** (400–700). Headline H1/H2, angka besar (harga, stat). Modern/techy tapi tetap hangat oleh warna. `letter-spacing -0.02em`, `line-height 1.05`.
- **Body — `--font-body` = Inter** (400–700). Body, tombol, nav.
- **Mono — `--font-mono` = JetBrains Mono**. Eyebrow/kicker, label kecil, meta ("12 Apr · 3 min").
- *(Opsional legacy)* `--font-serif` = Instrument Serif — hanya untuk aksen italic testimoni/quote.

Skala: hero `clamp(2.5rem,1.6rem+4.6vw,5rem)`; H2 `clamp(2rem,1.4rem+2.4vw,3.2rem)`; body `1rem–1.125rem`; eyebrow `0.78rem` uppercase.

---

## 4. Bentuk, radius, shadow

- Radius: `--radius-sm 8` · `--radius 12` · `--radius-lg 16` · `--radius-xl 20` · `--radius-sheet 20–28` · pill `999`.
- Shadow hangat lembut:
  - `--shadow-card: 0 1px 2px rgba(15,16,19,.04), 0 12px 30px -12px rgba(15,16,19,.16)`
  - `--shadow-card-hover: … 0 30px 60px -24px rgba(15,16,19,.28)`
- Kartu: 1px border `--color-border` + `--shadow-card`; hover → naik 3px + `--shadow-card-hover`.

---

## 5. Layout & ritme section (band)

Sistem `.page-blocks > .band` (garis/crosshair rail dipertahankan sebagai identitas, warna garis dibuat hangat).

- **Selang-seling**: band ganjil = kanvas (`--color-bg`), band genap = `--color-sunken` (auto lewat `.band:nth-child(even)`). Tujuannya: **tidak ada dua section putih identik berurutan**.
- **Band gelap**: `CTA` & `WhatsAppCTA` = `.band--dark` (`--color-night`) ATAU panel gradient (`.cta-section` → `--v2-grad`). Ini "closing statement".
- **Hero/intro**: diberi `--v2-mesh` (radial lembut) + boleh grid halus. Beda jelas dari section isi.
- Container: `--frame` ~1180px, `--frame-padding`. Spacing `--section-space clamp(3.5rem…6rem)`.
- Grid fitur → **bento** (2/3 + 1/3 + 3-up) untuk kesan produk modern, bukan 3 kolom rata kaku.

Target urutan 1 halaman:
`Hero (mesh + mockup)` → `Proof/logos` → `Layanan (bento)` → `Stats` → `Portofolio (tile bergradien)` → `Harga (kartu, 1 di-highlight gradient border)` → `Testimoni (panel gelap)` → `FAQ` → `CTA (gradient)` → `Footer`.

---

## 6. Komponen

| Komponen | Spesifikasi |
|---|---|
| **Header/nav** | Sticky, **glass** (`backdrop-blur`, bg `color-mix(bg 78%)`), border bawah hairline. CTA kanan = **pill gradient**. |
| **Button** | Pill (`999`). `btn-primary` = ink solid; `btn--grad` = gradient; `btn--glass` = glass. Hover translateY(-1/-2px) + shadow. |
| **Hero** | Mesh bg + grid halus; eyebrow pill ber-dot; H1 besar (gradient accent kata kunci via `{kata}`); 2 CTA; **mockup produk** (order-estimate card / buku + chip 1200 DPI & POS ready) + float chips. |
| **Bento fitur** | Kartu rounded, ikon tile `--v2-grad-soft`, 1 kartu hero (span 4) + 1 tall (span 2) + 3-up. |
| **Stats** | 4 kolom; angka Space Grotesk besar; 1–2 angka pakai gradient text. |
| **Portofolio** | Grid 3×2 tile bergradien (g1..g6) + chip kategori; **hindari kotak abu**. Idealnya foto asli bila ada aset. |
| **Harga** | Kartu; paket populer = gradient **border** (`background padding-box/border-box`) + badge gradient; CTA gradient. Ratakan tinggi kartu. |
| **Testimoni** | Panel gelap rounded + mesh sudut; bintang amber; quote Space Grotesk; atribusi mono terang (≥ opacity .85). |
| **FAQ** | Accordion kartu rounded ber-shadow; ikon +/− aksen merah; sejajar kiri dengan heading (jangan center-only). |
| **CTA** | Panel gradient penuh; teks putih; tombol putih/ink. |
| **Footer** | Ink (`--color-night`) atau terang; heading kolom uppercase muted; legal mono. |
| **Floating WhatsApp** | Green bubble tetap; jangan dobel dengan CTA sticky. |

---

## 7. Motion & aksesibilitas

- Reveal on-scroll boleh; **wajib** `@media (prefers-reduced-motion: reduce){ opacity:1 !important; transform:none !important; }` dan jangan pernah `opacity:0` permanen bila JS gagal.
- Hover 150–220ms ease-out. Focus ring terlihat (jangan hapus outline).
- Kontras body ≥ 4.5:1; teks di atas gradient cek dulu.
- Uji responsif 375/768/1024/1440.

---

## 8. Do / Don't

**Do:** selang-seling band; satu gradient untuk momen penting; Space Grotesk untuk display; foto/tile berwarna (bukan abu); soft shadow hangat.

**Don't:** semua section putih identik ❌ · monokrom kaku ala Vercel ❌ · paper/editorial krem-kaku ❌ · 3 warna solid Bauhaus ❌ · gradient di mana-mana ❌ · teks abu di atas gradient ❌ · emoji sebagai ikon produksi ❌.

---

## 9. Peta file (di mana mengubah apa)

- **Token & override tema** → `src/styles/theme.css` (palette, radius, shadow, glass header, gradient text). *File utama retheme.*
- **Default token** (jangan edit kecuali reset) → `src/styles/tokens.css`.
- **Polish blok** (band rhythm, hero mesh, CTA gradient) → `src/styles/marketing.css` (bagian "v2 Modern Warm-Tech" di akhir).
- **Font** → `astro.config.mjs` (`fonts:[…]`). `--font-display`=Space Grotesk, `--font-serif`=Instrument Serif (opsional).
- **Header/footer markup** → `src/layouts/Base.astro`.
- **Blok** → `src/components/blocks/*.astro` (Hero, Features, Pricing, FAQ, CTA, Feed, …). Pakai `formatAccentWords()` (dari `src/utils/text.ts`) untuk accent `{kata}` → `.text-accent-gradient`.

## 10. Cara menambah/menyesuaikan satu blok (standar)

1. Pakai token yang ada (`--color-*`, `--radius-*`, `--shadow-*`, `--v2-grad`). Jangan hardcode warna kecuali kebutuhan sekali (dokumentasikan).
2. Beri `class="band"` (+ `band--tint`/`band--dark` bila perlu jeda tonal).
3. Headline: `<h2 class="section-headline"><Fragment set:html={formatAccentWords(headline)} /></h2>` agar accent jalan.
4. Kartu: `.card` + otomatis dapat radius/shadow v2 (lihat theme.css).
5. Verifikasi: `pnpm build` + `astro check` bersih; render lokal & screenshot; cek kontras & mobile.

---

## 11. Status & riwayat
- v1 "Editorial Print Warm" (krem/kertas/serif) → **ditolak** (kaku, salah konteks).
- **v2 "Modern Warm-Tech"** → dipilih & diterapkan di branch `design/v2-warm-tech`: token di `theme.css`, band/hero/CTA di `marketing.css`, Space Grotesk sebagai display. Build lolos.
- Dark mode disiapkan via `light-dark()`; perlu pass QA terpisah.

## Block styling standard (EmDash marketing blocks)

All blocks live in `src/components/blocks/*.astro`. Theme them via overrides in
`src/styles/marketing.css` (unlayered, wins over `@layer base`) — do not rewrite markup.

- **Cards** (`.post`, `.plan`, `.card`, `.bento-card`, `.step-card`, `.faq__item`, `.testimonials__card`, `.comparison-card`, `.contact__card`): `--color-surface` bg, `1px --color-border`, `--radius-lg/xl` (12–20px), `--shadow-card`; hover lifts `translateY(-3px)` + `--shadow-card-hover`.
- **Icons/media fallback**: `.icon-tile`, `.post__media`, empty media → `--v2-grad-soft` so blanks read as intentional, not broken.
- **Pricing**: `.plan--highlighted` = 2px `--v2-red` ring + glow shadow + `translateY(-4px)`; `.plan__badge` & featured CTA = `--v2-grad`.
- **Buttons**: primary = `--color-brand` (ink) + white label. On the gradient CTA panel primary stays ink; secondary = translucent white (bg `.14`, border `.55`, white text). Never white-bg + inherited-white-text.
- **Stats**: `.stats__list` is a card with a 4px top `--v2-grad` bar; `.stats__value` is `--font-display`, `white-space: nowrap`, 4 columns with hairline dividers.
- **Headings**: `--font-display` (Space Grotesk), `letter-spacing: -0.02em`.
- **Anchors**: `section[id]{scroll-margin-top:92px}` so sticky header never covers a heading.
- **Content caveat**: typos/placeholder copy/duplicate link lists are CMS data, not theme — fix in admin, not CSS.
