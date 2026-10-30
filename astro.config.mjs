import node from "@astrojs/node";
import react from "@astrojs/react";
import tailwindcss from "@tailwindcss/vite";
import icon from "astro-iconset";
import { defineConfig, fontProviders } from "astro/config";
import { betterAuthProvider, betterAuthSettingsPlugin } from "emdash-better-auth";
import { emdashSmtp } from "emdash-smtp";
import { seoPlugin } from "@jdevalk/emdash-plugin-seo";
import emdash, { local } from "emdash/astro";
import { postgres, sqlite } from "emdash/db";
try {
	process.loadEnvFile?.();
} catch {}

const uploadsDirectory = process.env.UPLOADS_DIR || "./uploads";

function getDatabaseAdapter() {
	if (process.env.USE_SQLITE === "true") {
		return sqlite({ url: "file:./data.db" });
	}

	let connectionString = process.env.DATABASE_URL;
	if (!connectionString || connectionString.includes("***")) {
		if (process.env.PGHOST && process.env.PGPASSWORD) {
			const user = process.env.PGUSER || "dokploy";
			const pass = process.env.PGPASSWORD;
			const host = process.env.PGHOST;
			const port = process.env.PGPORT || 5432;
			const db = process.env.PGDATABASE || "emdash";
			connectionString = `postgresql://${user}:${pass}@${host}:${port}/${db}`;
		}
	}

	return postgres({ connectionString });
}

const database = getDatabaseAdapter();

export default defineConfig({
	site: process.env.EMDASH_SITE_URL || process.env.SITE_URL || "https://kotacom.id",
	output: "server",
	i18n: {
		defaultLocale: "id",
		locales: ["id"],
	},
	redirects: {
		"/sitemap-index.xml": "/sitemap.xml",
		"/produk": "/products",
		"/produk/[...slug]": "/products/[...slug]",
		"/contact-us": "/contact",
		"/portfolio": "/projects",
		"/testimonials": "/about",
	},
	security: {
		allowedDomains: [
			{ protocol: "https", hostname: "kotacom.id" },
			{ protocol: "https", hostname: "www.kotacom.id" },
			{ protocol: "https", hostname: "**.kotacom.id" },
			{ protocol: "https", hostname: "staging.devk.my.id" },
			{ protocol: "https", hostname: "kc.devk.my.id" },
			{ protocol: "https", hostname: "devk.my.id" },
			{ protocol: "https", hostname: "**.devk.my.id" },
			{ protocol: "https", hostname: "**.eu.org" },
			{ protocol: "https", hostname: "localhost" },
			{ protocol: "http", hostname: "localhost" }
		],
	},
	adapter: node({
		mode: "standalone",
	}),
	vite: {
		plugins: [tailwindcss()],
		resolve: {
			alias: [
				// emdash-better-auth imports `cloudflare:workers` (a Workers-only
				// virtual module). On the self-hosted Node adapter we alias it to
				// a shim whose `env` is process.env. See src/shims/cloudflare-workers.ts.
				{ find: "cloudflare:workers", replacement: new URL("./src/shims/cloudflare-workers.ts", import.meta.url).pathname },
			],
		},
	},
	session: { cookie: { maxAge: 60 * 60 * 24 * 7 }, ttl: 60 * 60 * 24 * 7 },
	image: {
		layout: "constrained",
		responsiveStyles: true,
		domains: ["kotacom.id", "www.kotacom.id", "staging.kotacom.id", "devk.my.id", "software.devk.my.id", "kc.devk.my.id", "localhost"],
		remotePatterns: [
			{ protocol: "https" },
			{ protocol: "http" },
		],
	},
	integrations: [
		react(),
		icon({
			// Only ship the Phosphor icons actually referenced in templates,
			// not the full @iconify-json/ph set.
			include: {
				ph: [
					"arrow-right",
					"bell-simple",
					"buildings",
					"chart-bar",
					"chat-circle",
					"check",
					"check-circle",
					"clock",
					"cloud",
					"code",
					"currency-dollar",
					"envelope",
					"file-text",
					"gauge",
					"globe",
					"heart",
					"leaf",
					"lifebuoy",
					"lightning",
					"list",
					"lock",
					"map-pin",
					"pause",
					"phone",
					"play",
					"plug",
					"plus",
					"rocket",
					"shield-check",
					"shopping-cart",
					"sparkle",
					"star",
					"storefront",
					"sun",
					"thermometer-simple",
					"trend-up",
					"users-three",
					"wrench",
					"x",
					"x-circle",
					"check-circle-fill",
					"cpu",
					"database",
					"desktop",
					"gear",
					"printer",
					"book-open",
					"whatsapp-logo",
					"magnifying-glass",
					"truck",
					"pen-nib",
				],
			},
		}),
		emdash({
			siteUrl: process.env.EMDASH_SITE_URL || undefined,
			database,
			storage: local({
				directory: uploadsDirectory,
				baseUrl: "/_emdash/api/media/file",
			}),
			authProviders: [betterAuthProvider()],
			plugins: [
				betterAuthSettingsPlugin(),
				emdashSmtp(),
				seoPlugin(),
				{
					id: "bulk-generator",
					version: "1.0.0",
					entrypoint: new URL("./src/plugins/bulk-generator/index.ts", import.meta.url).pathname,
					adminPages: [
						{ path: "/generator", label: "Bulk Generator", icon: "sparkle" },
					],
					capabilities: ["content:read", "content:write", "content:publish"],
				},
				{
					id: "marketing-blocks",
					version: "0.1.0",
					entrypoint: new URL("./src/plugins/marketing-blocks/index.ts", import.meta.url).pathname,
					componentsEntry: new URL("./src/plugins/marketing-blocks/astro/index.ts", import.meta.url).pathname,
				},
			],
		}),
	],
	fonts: [
		{
			provider: fontProviders.google(),
			name: "Inter",
			cssVariable: "--font-body",
			weights: [400, 500, 600, 700],
			fallbacks: ["sans-serif"],
		},
		{
			provider: fontProviders.google(),
			name: "Instrument Serif",
			cssVariable: "--font-display",
			weights: [400],
			styles: ["normal", "italic"],
			fallbacks: ["serif"],
		},
		{
			provider: fontProviders.google(),
			name: "JetBrains Mono",
			cssVariable: "--font-mono",
			weights: [400, 500],
			fallbacks: ["monospace"],
		},
	],
	devToolbar: { enabled: false },
});
