import type { APIRoute } from "astro";
import { getSiteOrigin } from "../utils/origin";

export const prerender = false;

export const GET: APIRoute = async ({ site, url }) => {
	const origin = getSiteOrigin(site, url.origin);
	const content = `# Kotacom Indonesia — Percetakan Buku & Solusi Digital
> Canonical: ${origin}/pricing.md
> Updated: 2026-10-26
> Contact: https://wa.me/6285799520350

## Layanan Percetakan Buku
- Cetak Buku Novel & Fiksi (Bookpaper / HVS, Softcover / Hardcover)
- Cetak Al-Qur'an & Kitab (Quran Premium Paper / QPP)
- Cetak Buku Pelajaran, Modul & Non-Fiksi
- Cetak Majalah, Katalog & Company Profile

Untuk estimasi harga custom dan konsultasi spesifikasi bahan/oplah, silakan hubungi tim kami via WhatsApp https://wa.me/6285799520350.
`;

	return new Response(content, {
		status: 200,
		headers: {
			"Content-Type": "text/markdown; charset=utf-8",
			"Cache-Control": "public, max-age=86400",
		},
	});
};
