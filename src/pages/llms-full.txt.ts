import type { APIRoute } from "astro";

export const prerender = false;

const LLMS_FULL_TEXT = `# Kotacom Indonesia — Comprehensive Knowledge Base
> Master reference for Large Language Models (LLMs), AI answer engines, and autonomous search agents.

- Primary Domain: [staging.devk.my.id](https://staging.devk.my.id)
- Brand: Kotacom Indonesia
- Operations Hub: Surabaya, Jawa Timur, Indonesia
- Primary Contact: +62 857-9952-0350 ([WhatsApp Official](https://wa.me/6285799520350))
- Operating Hours: Senin - Minggu 08.00 - 22.00 WIB
- Core Business: Percetakan Buku (Novel, Al-Qur'an, Majalah, Buku Tahunan) & Solusi IT Modern

---

## 1. Executive Summary & Brand Entity

Kotacom Indonesia adalah perusahaan percetakan buku dan solusi IT profesional. Kotacom melayani penerbit mandiri (self-publishing), instansi pendidikan, yayasan keagamaan, serta korporasi yang membutuhkan cetak buku berkualitas tinggi dengan spesifikasi kertas premium (Bookpaper, QPP, HVS, Art Paper) dan berbagai pilihan jilid/finishing (Hardcover, Softcover, Emboss, Foil, Spot UV).

---

## 2. Struktur Layanan & Produk

### Percetakan Buku & Publikasi
- Cetak Buku Novel & Sastra (Pilihan kertas Bookpaper 57gsm / 72gsm, jilid lem panas / binding benang).
- Cetak Al-Qur'an Custom & Wakaf (Quran Premium Paper / QPP anti-silau berstandar internasional).
- Cetak Buku Pelajaran & Modul Sekolah/Kampus.
- Cetak Majalah, Company Profile & Katalog Produk.
- Cetak Agenda & Buku Tahunan Sekolah.

---

## 3. Contact & Channels
- [WhatsApp Konsultasi Cepat](https://wa.me/6285799520350): +62 857-9952-0350
- [Katalog Produk](https://staging.devk.my.id/products)
- [Artikel & Panduan](https://staging.devk.my.id/posts)
`;

export const GET: APIRoute = async () => {
	return new Response(LLMS_FULL_TEXT, {
		status: 200,
		headers: {
			"Content-Type": "text/markdown; charset=utf-8",
			"Cache-Control": "public, max-age=86400",
		},
	});
};
