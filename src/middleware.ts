import { defineMiddleware } from "astro:middleware";
import prunedCityRedirects from "./data/pruned_city_redirects.json";

function cleanLastmod(raw: string): string {
	const trimmed = raw.trim();
	// Normalize postgres timestamp: "2026-10-22 22:33:00.591227+00" -> "2026-10-22T22:33:00.591227Z"
	let norm = trimmed.replace(" ", "T");
	if (norm.endsWith("+00") || norm.endsWith("-00")) {
		norm = norm.slice(0, -3) + "Z";
	}
	const d = new Date(norm);
	if (!Number.isNaN(d.getTime())) {
		return d.toISOString();
	}
	return trimmed;
}

export const onRequest = defineMiddleware(async (context, next) => {
	const pathname = context.url.pathname;

	// Public origin of THIS request (Cloudflare/Traefik forward the real host).
	// EmDash builds sitemap <loc> values from a fixed site URL, so a site served
	// on more than one hostname emitted cross-host sitemaps, which Google refuses
	// to read. Rewrite them to the host the crawler actually asked for.
	const forwardedProto = context.request.headers.get("x-forwarded-proto");
	const proto = (forwardedProto ? forwardedProto.split(",")[0].trim() : "") ||
		(context.url.protocol ? context.url.protocol.replace(":", "") : "https");
	const rawHost = context.request.headers.get("x-forwarded-host") ||
		context.request.headers.get("host") ||
		context.url.host;
	const host = (rawHost || "").split(",")[0].trim();
	const requestOrigin =
		host && host.includes(".") && !host.startsWith("localhost")
			? `${proto}://${host}`
			: null;

	// Canonicalise www → apex: one canonical host per site, so a domain-property
	// GSC setup (which spans www + apex) never hits a 404 sitemap on www.
	if (
		host.toLowerCase().startsWith("www.") &&
		!pathname.startsWith("/.well-known/")
	) {
		const apex = `${proto}://${host.toLowerCase().slice(4)}`;
		return context.redirect(`${apex}${pathname}${context.url.search}`, 301);
	}

	// 301 Permanent Redirect semua subhalaman kota kalender ke pilar utama
	if (pathname.startsWith("/percetakan/cetak-kalender/") && pathname !== "/percetakan/cetak-kalender") {
		return context.redirect("/percetakan/cetak-kalender", 301);
	}

	// 301 Permanent Redirect semua subhalaman provinsi cetak buku ke pilar utama
	if (pathname.startsWith("/percetakan/cetak-buku/") && pathname !== "/percetakan/cetak-buku") {
		return context.redirect("/percetakan/cetak-buku", 301);
	}

	// 301 Permanent Redirect kabupaten cetak buku 0 impresi ke Pilar Utama /percetakan/cetak-buku
	const cityRedirectTarget = (prunedCityRedirects as Record<string, string>)[pathname];
	if (cityRedirectTarget) {
		return context.redirect(cityRedirectTarget, 301);
	}

	const response = await next();

	// Long cache for hashed/static assets
	if (/\.(css|js|woff2?|png|jpg|jpeg|webp|avif|svg|ico|gif)$/i.test(pathname) &&
	    (pathname.startsWith("/_astro/") || pathname.startsWith("/brand/") || pathname.startsWith("/fonts/"))) {
		const h = new Headers(response.headers);
		h.set("Cache-Control", "public, max-age=31536000, immutable");
		return new Response(response.body, { status: response.status, statusText: response.statusText, headers: h });
	}
	if (pathname.endsWith(".xml") || pathname.includes("sitemap")) {
		const contentType = response.headers.get("content-type") || "";
		if (contentType.includes("xml")) {
			const text = await response.text();
			let fixed = text.replace(/<lastmod>([^<]+)<\/lastmod>/g, (_match, raw) => {
				return `<lastmod>${cleanLastmod(raw)}</lastmod>`;
			});

			// Re-point every <loc>/<image:loc> at the origin the crawler requested,
			// so a sitemap served on an alias host references its own URLs.
			if (requestOrigin) {
				const originRe = /(<(?:loc|image:loc)>)(https?:\/\/[^/<]+)([^<]*)(<\/(?:loc|image:loc)>)/g;
				fixed = fixed.replace(originRe, (_m, open, _origin, path, close) => {
					return `${open}${requestOrigin}${path}${close}`;
				});
			}

			const h = new Headers(response.headers);
			h.delete("content-length");
			h.delete("etag");
			h.delete("content-encoding");
			return new Response(fixed, {
				status: response.status,
				statusText: response.statusText,
				headers: h,
			});
		}
	}

	return response;
});
