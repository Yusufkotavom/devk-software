import type { APIRoute } from "astro";

export const prerender = false;

const PRICING_MD = `# Kotacom Indonesia — Percetakan Buku & Solusi Digital
> Canonical: https://staging.devk.my.id/pricing.md
> Updated: 2026-10-26
> Contact: https://wa.me/6285799520350

## Layanan Percetakan Buku
- Cetak Buku Novel & Fiksi (Bookpaper / HVS, Softcover / Hardcover)
- Cetak Al-Qur'an & Kitab (Quran Premium Paper / QPP)
- Cetak Buku Pelajaran, Modul & Non-Fiksi
- Cetak Majalah, Katalog & Company Profile

Untuk estimasi harga custom dan konsultasi spesifikasi bahan/oplah, silakan hubungi tim kami via WhatsApp https://wa.me/6285799520350.
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
