import { defineMiddleware } from "astro:middleware";

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
	const response = await next();
	const pathname = context.url.pathname;

	// Intercept sitemap XML endpoints to ensure 100% W3C/ISO 8601 compliant <lastmod>
	if (pathname.endsWith(".xml") || pathname.includes("sitemap")) {
		const contentType = response.headers.get("content-type") || "";
		if (contentType.includes("xml")) {
			const text = await response.text();
			const fixed = text.replace(/<lastmod>([^<]+)<\/lastmod>/g, (_match, raw) => {
				return `<lastmod>${cleanLastmod(raw)}</lastmod>`;
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
