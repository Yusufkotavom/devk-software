import type { APIRoute } from "astro";

export const prerender = false;

const ROBOTS_TXT = `User-agent: *
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
Sitemap: https://devk.my.id/sitemap.xml
`;

export const GET: APIRoute = async () => {
	return new Response(ROBOTS_TXT, {
		status: 200,
		headers: {
			"Content-Type": "text/plain; charset=utf-8",
			"Cache-Control": "public, max-age=86400",
		},
	});
};
