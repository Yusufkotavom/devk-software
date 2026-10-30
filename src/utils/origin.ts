/**
 * Resolves the canonical site origin across server and client environments.
 * Prioritizes EMDASH_SITE_URL / SITE_URL environment variables to prevent
 * reverse-proxy loopback leaking "http://localhost:3000" into production metadata.
 */
export function getSiteOrigin(astroSite?: URL | string, astroUrlOrigin?: string): string {
	const envUrl = process.env.EMDASH_SITE_URL || process.env.SITE_URL;
	if (envUrl && typeof envUrl === "string" && envUrl.trim()) {
		return envUrl.trim().replace(/\/$/, "");
	}
	if (astroUrlOrigin && typeof astroUrlOrigin === "string") {
		const o = astroUrlOrigin.trim().replace(/\/$/, "");
		if (o && !o.includes("localhost") && !o.includes("127.0.0.1")) {
			return o;
		}
	}
	if (astroSite) {
		const s = astroSite.toString().trim().replace(/\/$/, "");
		if (s && !s.includes("localhost") && !s.includes("127.0.0.1")) {
			return s;
		}
	}
	return "https://kotacom.id";
}
