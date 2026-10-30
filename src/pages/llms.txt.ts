import type { APIRoute } from "astro";

export const prerender = false;

const LLMS_TEXT = `# Kotacom Indonesia — Percetakan Buku & Solusi Digital
> Platform percetakan buku dan solusi IT profesional di Surabaya, Jawa Timur, dan seluruh Indonesia. Melayani cetak buku novel, Al-Qur'an, majalah, profil perusahaan, hingga software & website modern.

Kotacom Indonesia menghadirkan layanan percetakan berkualitas tinggi dengan standar kertas terbaik (Bookpaper, QPP, Art Paper) dan finishing profesional (Hardcover, Softcover, Emboss, Spot UV).

## Layanan Utama
- [Katalog Produk Cetak](https://staging.devk.my.id/products): Layanan cetak buku novel, Al-Qur'an wakaf/custom, majalah, buku tahunan, dan profil perusahaan.
- [Artikel & Panduan Cetak](https://staging.devk.my.id/posts): Panduan teknis persiapan naskah, pemilihan jenis kertas, tips negosiasi percetakan, dan manajemen layout buku.
- [Profil Kotacom](https://staging.devk.my.id/about): Informasi profil, visi, dan layanan percetakan serta solusi IT Kotacom Indonesia.

## Layanan & Kontak
- [Machine-Readable Rate Card](https://staging.devk.my.id/pricing.md): Ringkasan layanan cetak dan kontak pemesanan.
- [Hubungi WhatsApp Resmi Kotacom](https://wa.me/6285799520350): Hotline konsultasi spesifikasi naskah dan pemesanan cetak.
`;

export const GET: APIRoute = async () => {
	return new Response(LLMS_TEXT, {
		status: 200,
		headers: {
			"Content-Type": "text/markdown; charset=utf-8",
			"Cache-Control": "public, max-age=86400",
		},
	});
};
