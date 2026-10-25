import type { APIRoute } from "astro";

export const prerender = false;

export const GET: APIRoute = async ({ request, url }) => {
	const proto = request.headers.get("x-forwarded-proto") || (url.protocol ? url.protocol.replace(":", "") : "https");
	const host = request.headers.get("x-forwarded-host") || request.headers.get("host") || url.host;
	const siteOrigin = `${proto}://${host}`;

	const robotsTxt = `User-agent: *
Allow: /
Disallow: /_emdash/

# AI Search & Answer Engine Crawlers (Explicitly Allowed)
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Cohere-ai
Allow: /

User-agent: Omgilibot
Allow: /

# Canonical Sitemaps & Machine-Readable Knowledge
Sitemap: ${siteOrigin}/sitemap.xml
`;

	return new Response(robotsTxt, {
		status: 200,
		headers: {
			"Content-Type": "text/plain; charset=utf-8",
			"Cache-Control": "public, max-age=300",
		},
	});
};
