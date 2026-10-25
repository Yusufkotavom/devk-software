import type { APIRoute } from "astro";
import { getEmDashEntry, getSiteSettings, decodeSlug } from "emdash";
import { buildSquareCard, renderSquareOgPng, type SquareCardData } from "../../../../lib/og/square-card";
import { resolveBlogSiteIdentity } from "../../../../utils/site-identity";

export const prerender = false;

const COLLECTIONS = new Set(["posts", "pages", "page_templates", "products"]);

function canonicalOrigin(url: URL): string {
	const configured = import.meta.env.SITE || process.env.EMDASH_SITE_URL || process.env.SITE_URL;
	if (configured) return String(configured).replace(/\/$/, "");
	return url.origin;
}

function pngResponse(png: Buffer, etagSeed: string): Response {
	let h = 0x811c9dc5;
	for (let i = 0; i < etagSeed.length; i++) {
		h ^= etagSeed.charCodeAt(i);
		h = Math.imul(h, 0x01000193);
	}
	const etag = `"og-sq-${(h >>> 0).toString(36)}"`;
	return new Response(new Uint8Array(png), {
		status: 200,
		headers: {
			"Content-Type": "image/png",
			"Cache-Control": "public, max-age=3600, s-maxage=604800, stale-while-revalidate=86400",
			ETag: etag,
		},
	});
}

export const GET: APIRoute = async ({ params, request, url }) => {
	const collection = String(params.collection ?? "");
	const slug = decodeSlug(String(params.slug ?? ""));
	if (!COLLECTIONS.has(collection) || !slug) {
		return new Response("Not found", { status: 404 });
	}

	const origin = canonicalOrigin(url);

	let entry: Awaited<ReturnType<typeof getEmDashEntry>> | null = null;
	try {
		const { entry: e } = await getEmDashEntry(collection, slug);
		entry = e;
	} catch {
		entry = null;
	}

	const { siteTitle } = resolveBlogSiteIdentity(await getSiteSettings());

	if (!entry) {
		const node = buildSquareCard({
			siteTitle,
			title: siteTitle,
			excerpt: "Layanan Cetak Buku Profesional Standar Penerbit",
			domain: new URL(origin).host,
		});
		return pngResponse(await renderSquareOgPng(node), "fallback");
	}

	const data = entry.data as Record<string, unknown>;
	const rawTitle = typeof data.title === "string" ? data.title : siteTitle;
	const excerpt = typeof data.excerpt === "string" ? data.excerpt : "Bisa cetak mulai 1 buku tanpa beban master plat. Kualitas penerbit nasional.";

	const card: SquareCardData = {
		siteTitle,
		title: rawTitle,
		excerpt,
		category: collection === "posts" ? "Artikel Penerbitan" : "Layanan Percetakan Buku",
		priceText: "Mulai Rp 14.000 / eks",
		domain: new URL(origin).host,
	};

	const png = await renderSquareOgPng(buildSquareCard(card));
	const seed = `sq|${collection}|${slug}|${siteTitle}|${rawTitle}`;
	const res = pngResponse(png, seed);

	const inm = request.headers.get("if-none-match");
	const etag = res.headers.get("ETag");
	if (inm && etag && inm === etag) {
		return new Response(null, { status: 304, headers: { ETag: etag } });
	}
	return res;
};
