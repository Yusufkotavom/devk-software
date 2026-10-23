import { defineMiddleware } from "astro:middleware";

export const onRequest = defineMiddleware(async (context, next) => {
	const response = await next();
	const pathname = context.url.pathname;

	// Intercept sitemap XML endpoints to ensure 100% W3C/ISO 8601 compliant <lastmod>
	if (pathname.endsWith(".xml") || pathname.includes("sitemap")) {
		const contentType = response.headers.get("content-type") || "";
		if (contentType.includes("xml")) {
			const text = await response.text();
			const fixed = text.replace(/<lastmod>([^<]+)<\/lastmod>/g, (match, raw) => {
				const trimmed = raw.trim();
				// If already strict ISO 8601 with Z
				if (/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/.test(trimmed)) {
					return match;
				}
				// Fix Postgres timestamp: "2026-10-22 22:33:00.591227+00" -> "2026-10-22T22:33:00.591227Z"
				const m = trimmed.match(/^(\d{4}-\d{2}-\d{2})[ T](\d{2}:\d{2}:\d{2}(?:\.\d+)?)(?:[+-]\d{2}(?::?\d{2})?|Z)?$/);
				if (m) {
					return `<lastmod>${m[1]}T${m[2]}Z</lastmod>`;
				}
				const d = new Date(trimmed.replace(" ", "T"));
				if (!Number.isNaN(d.getTime())) {
					return `<lastmod>${d.toISOString()}</lastmod>`;
				}
				return match;
			});

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
