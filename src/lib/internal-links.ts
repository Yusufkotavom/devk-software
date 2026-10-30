/**
 * Automatic internal-linking graph for generated (pSEO) pages.
 *
 * Implements the "4-Point Linking Rule" from docs/seo/LINKING_MATRIX.md:
 *   1. Upward link  -> the family hub / pillar page
 *   2. Lateral links -> sibling pages of the same family (ring order, so every
 *      page also *receives* inbound links from its neighbours)
 *   3. Cross-pillar -> the same city/topic in a different service family
 *      (e.g. "jasa-cetak-buku-bandung" <-> "pembuatan-website/bandung")
 *   4. Conversion CTA -> WhatsApp (rendered by the component)
 *
 * The graph is derived from published page slugs only, so new pages generated
 * by the Bulk Generator are wired up automatically without any manual curating.
 *
 * Only two columns are read (slug, title) through a tiny dedicated pool, and the
 * whole graph (~750 rows today) is cached in module memory for a few minutes, so
 * rendering a page costs one array lookup instead of a query.
 */
import pg from "pg";
import { CITY_PROVINCE, PROVINCE_BY_SLUG, PROVINCE_HUB_PREFIX } from "../data/wilayah";

export interface LinkTarget {
	slug: string;
	title: string;
}

export interface ProvinceRef {
	slug: string;
	name: string;
}

export interface RelatedLinks {
	/** Detected family prefix (e.g. "jasa-cetak-buku"), null when the page stands alone. */
	family: string | null;
	/** Family root used for anchor text ("jasa-cetak-buku-aceh" -> "jasa-cetak-buku"). */
	anchorFamily: string | null;
	/** Upward link: the nearest pillar page of this family (province hub when it exists). */
	hub: LinkTarget | null;
	/** Ancestors above `hub` (province hub -> national pillar), so hierarchy stays explicit. */
	parents: LinkTarget[];
	/** Province this page belongs to, when it is a city hub. */
	province: ProvinceRef | null;
	/** Lateral links: sibling pages, ring-ordered around the current page. */
	lateral: LinkTarget[];
	/** Cross-pillar links: same topic in another family, or a fallback pillar. */
	cross: LinkTarget[];
	/** Hub pages only: directory of child pages (cities of a province, or all provinces). */
	directory: LinkTarget[];
	/** Heading for the directory block. */
	directoryLabel: string;
	/** Heading for the lateral block ("Layanan serupa di Jawa Timur" / "Provinsi lain"). */
	lateralLabel: string;
}

const CACHE_TTL_MS = 5 * 60 * 1000;
const MIN_FAMILY_SIZE = 3;
const MAX_PREFIX_TOKENS = 6;
const LATERAL_COUNT = 6;
const CROSS_COUNT = 2;
const DIRECTORY_LIMIT = 48;

/** Pages that must never render the related-links band. */
const SKIP_SLUGS = new Set([
	"",
	"home",
	"index",
	"index-old",
	"about",
	"contact",
	"blog",
	"blocks",
	"all-blocks",
	"ai-statement",
	"404",
	"search",
	"pricing",
	"layanan",
	"projects",
	"template",
	"index-old",
	"all-blocks",
]);

/**
 * Families whose pillar page cannot be derived from the slug alone.
 * Anything missing here falls back to a page whose slug equals the family
 * prefix, then to the first path segment, then to the generic pillar rotation.
 */
const FAMILY_HUBS: Record<string, string> = {
	"jasa-cetak-buku": "percetakan/cetak-buku",
	"jasa-cetak-al-quran": "percetakan/cetak-al-quran",
	"jasa-cetak-brosur": "percetakan/cetak-brosur",
	"jasa-cetak-banner-spanduk": "percetakan/cetak-banner-spanduk",
	"jasa-cetak-company-profile": "percetakan/cetak-company-profile",
	"jasa-cetak-album-pernikahan": "percetakan/cetak-album-pernikahan",
	"jasa-cetak-buku-kenangan-sekolah": "percetakan/cetak-buku-kenangan-sekolah",
	"jasa-install": "services",
	"jasa-instal": "services",
	"jasa-servis": "services",
	"jasa-service": "services",
	"jasa-upgrade": "services",
	"jasa-rakit": "services",
	"rakit-pc": "services",
	"jasa-pasang": "services",
	"rekomendasi-jual-game-pc": "products",
	"terbaik-jual-game-pc": "products",
	"no-1-jual-game-pc": "products",
	"jual-game-pc": "products",
	"jual-dvd": "products",
	"jasa-pembuatan-website": "pembuatan-website",
	"pembuatan-website": "pembuatan-website",
};

/** Last-resort cross links when a page has no topical partner. */
const PILLAR_FALLBACKS = [
	"percetakan/cetak-buku",
	"percetakan/cetak-al-quran",
	"percetakan/cetak-buku-kenangan-sekolah",
	"pembuatan-website",
	"pembuatan-website/harga",
	"sistem-pos",
	"software",
	"services",
	"products",
];

interface Graph {
	pages: Map<string, LinkTarget>;
	byFamily: Map<string, LinkTarget[]>;
	byTail: Map<string, Array<{ family: string; page: LinkTarget }>>;
	byToken: Map<string, LinkTarget[]>;
	tokensOf: Map<string, string[]>;
	familyOf: Map<string, string | null>;
	rootFamilyOf: Map<string, string | null>;
	hubsOf: Map<string, string[]>;
	provinceOf: Map<string, string>;
	byProvince: Map<string, LinkTarget[]>;
	provinceHubs: LinkTarget[];
}

let pagesCache: { at: number; pages: LinkTarget[] } | null = null;
let graphCache: { at: number; graph: Graph } | null = null;
let pool: pg.Pool | null = null;

function poolConfig(): pg.PoolConfig | null {
	const url = process.env.DATABASE_URL;
	if (url && !url.includes("***") && url.startsWith("postgres")) {
		return { connectionString: url, max: 2 };
	}
	if (!process.env.PGHOST) return null;
	return {
		host: process.env.PGHOST,
		port: Number(process.env.PGPORT || 5432),
		database: process.env.PGDATABASE || "emdash",
		user: process.env.PGUSER || "dokploy",
		password: process.env.PGPASSWORD,
		max: 2,
	};
}

function getPool(): pg.Pool | null {
	if (pool) return pool;
	const config = poolConfig();
	if (!config) return null;
	pool = new pg.Pool(config);
	// Never let a background pool error take the render down.
	pool.on("error", () => {});
	return pool;
}

async function loadPublishedPages(): Promise<LinkTarget[]> {
	const now = Date.now();
	if (pagesCache && now - pagesCache.at < CACHE_TTL_MS) return pagesCache.pages;

	const db = getPool();
	if (!db) return pagesCache?.pages ?? [];

	try {
		const { rows } = await db.query<{ slug: string; title: string | null }>(
			`SELECT slug, title
			   FROM ec_pages
			  WHERE status = 'published'
			    AND deleted_at IS NULL
			    AND slug IS NOT NULL
			    AND slug <> ''
			  ORDER BY slug`,
		);
		const pages = rows.map((row) => ({
			slug: String(row.slug),
			title: String(row.title ?? row.slug),
		}));
		pagesCache = { at: now, pages };
		return pages;
	} catch {
		// Database hiccup: keep serving the previous graph, never throw from render.
		return pagesCache?.pages ?? [];
	}
}

/** All prefix candidates of a slug, longest first ("a-b-c", "a-b", "a", ...). */
function candidatePrefixes(slug: string): string[] {
	const parts = slug.split("/").filter(Boolean);
	const tail = parts.pop() ?? "";
	const base = parts.length > 0 ? `${parts.join("/")}/` : "";
	const tokens = tail.split("-").filter(Boolean);

	const out: string[] = [];
	const from = Math.min(tokens.length, MAX_PREFIX_TOKENS);
	for (let k = from; k >= 1; k--) out.push(`${base}${tokens.slice(0, k).join("-")}`);
	if (base) out.push(base.slice(0, -1));
	return out;
}

function tailAfter(slug: string, family: string | null): string {
	if (!family) return "";
	if (slug === family) return "";
	const prefix = `${family}/`;
	if (slug.startsWith(prefix)) return slug.slice(prefix.length);
	const dash = `${family}-`;
	if (slug.startsWith(dash)) return slug.slice(dash.length);
	return slug;
}

// Longest kabupaten name in the dataset: "kepulauan-siau-tagulandang-biaro".
const MAX_CITY_TOKENS = 5;

/**
 * Province of a page, resolved by matching the longest known kabupaten/kota key
 * at the end of its slug: "jasa-cetak-buku-aceh-barat" -> "aceh".
 */
export function provinceOfSlug(slug: string): string | undefined {
	const parts = slug.split("/").filter(Boolean);
	const segment = parts[parts.length - 1] ?? "";
	const tokens = segment.split("-").filter(Boolean);
	for (let size = Math.min(MAX_CITY_TOKENS, tokens.length); size >= 1; size--) {
		const key = tokens.slice(tokens.length - size).join("-");
		if (size === tokens.length) continue; // the whole segment is a service slug, not a city
		const province = CITY_PROVINCE[key];
		if (province) return province;
	}
	return undefined;
}

/** `percetakan/cetak-buku/jawa` — a truncated province slug, not a real page. */
function isPartialProvincePath(path: string): boolean {
	if (!path.startsWith(PROVINCE_HUB_PREFIX)) return false;
	const rest = path.slice(PROVINCE_HUB_PREFIX.length);
	return Boolean(rest) && !rest.includes("/") && !PROVINCE_BY_SLUG[rest];
}

/** Province hub page (e.g. "percetakan/cetak-buku/jawa-timur"), if this slug is one. */
export function provinceHubOfSlug(slug: string): string | undefined {
	if (!slug.startsWith(PROVINCE_HUB_PREFIX)) return undefined;
	const rest = slug.slice(PROVINCE_HUB_PREFIX.length);
	if (!rest || rest.includes("/")) return undefined;
	return PROVINCE_BY_SLUG[rest] ? rest : undefined;
}

function buildGraph(pages: LinkTarget[]): Graph {
	const pageMap = new Map<string, LinkTarget>();
	const prefixCount = new Map<string, number>();
	const prefixMembers = new Map<string, LinkTarget[]>();

	for (const page of pages) {
		pageMap.set(page.slug, page);
		for (const prefix of candidatePrefixes(page.slug)) {
			prefixCount.set(prefix, (prefixCount.get(prefix) ?? 0) + 1);
			const list = prefixMembers.get(prefix);
			if (list) list.push(page);
			else prefixMembers.set(prefix, [page]);
		}
	}

	const familyOf = new Map<string, string | null>();
	for (const page of pages) {
		let family: string | null = null;
		for (const prefix of candidatePrefixes(page.slug)) {
			if (prefix === page.slug) continue;
			// "percetakan/cetak-buku/jawa" is not a family, it is a truncated
			// province slug — keep the real family ("percetakan/cetak-buku").
			if (isPartialProvincePath(prefix)) continue;
			if ((prefixCount.get(prefix) ?? 0) >= MIN_FAMILY_SIZE) {
				family = prefix;
				break;
			}
		}
		familyOf.set(page.slug, family);
	}

	// Root family ("jasa-cetak-buku-bolaang-mongondow" -> "jasa-cetak-buku") keeps
	// nested sub-hubs in the same bucket as their parent service.
	const rootOf = new Map<string, string | null>();
	for (const page of pages) {
		const family = familyOf.get(page.slug) ?? null;
		rootOf.set(page.slug, rootFamilyOf(family) ?? family);
	}

	const byFamily = new Map<string, LinkTarget[]>();
	const byTail = new Map<string, Array<{ family: string; page: LinkTarget }>>();
	const byToken = new Map<string, LinkTarget[]>();
	const tokensOf = new Map<string, string[]>();

	for (const page of pages) {
		const family = familyOf.get(page.slug) ?? null;
		const tail = tailAfter(page.slug, family);

		const tokens = page.slug
			.split(/[/\-]+/)
			.filter((token) => token.length > 3 && !STOP_WORDS.has(token) && token !== tail);
		tokensOf.set(page.slug, tokens);
		for (const token of tokens) {
			const bucket = byToken.get(token);
			if (bucket) bucket.push(page);
			else byToken.set(token, [page]);
		}

		if (!family) continue;

		const members = byFamily.get(family);
		if (members) members.push(page);
		else byFamily.set(family, [page]);

		if (!tail) continue;
		const entry = { family, page };
		const tailBucket = byTail.get(tail);
		if (tailBucket) tailBucket.push(entry);
		else byTail.set(tail, [entry]);
	}

	// Which families consider a given page their hub?
	const hubsOf = new Map<string, string[]>();
	for (const family of byFamily.keys()) {
		const hub = resolveHubSlug(family, pageMap);
		if (!hub) continue;
		const list = hubsOf.get(hub);
		if (list) list.push(family);
		else hubsOf.set(hub, [family]);
	}

	// Province layer: group generated city pages by kabupaten/kota, and collect
	// the province hub pages that exist, so the national pillar can link to them.
	const provinceOf = new Map<string, string>();
	const byProvince = new Map<string, LinkTarget[]>();
	const provinceHubs: LinkTarget[] = [];
	for (const page of pages) {
		if (provinceHubOfSlug(page.slug)) {
			provinceHubs.push(page);
			continue;
		}
		// Only pages whose tail *is* a kabupaten/kota count as city pages, so
		// "jasa-install-windows-11-surabaya" never becomes a "city" page. The root
		// family is used so nested families ("jasa-cetak-buku-bolaang-mongondow")
		// still resolve to their city.
		const rootFamily = rootOf.get(page.slug) ?? null;
		const pageTail = rootFamily ? tailAfter(page.slug, rootFamily) : "";
		const province = pageTail ? CITY_PROVINCE[pageTail] : undefined;
		if (!province) continue;
		provinceOf.set(page.slug, province);
		const bucket = byProvince.get(province);
		if (bucket) bucket.push(page);
		else byProvince.set(province, [page]);
	}
	provinceHubs.sort((a, b) => a.slug.localeCompare(b.slug));

	return { pages: pageMap, byFamily, byTail, byToken, tokensOf, familyOf, rootFamilyOf: rootOf, hubsOf, provinceOf, byProvince, provinceHubs };
}

function resolveHubSlug(family: string, pages: Map<string, LinkTarget>): string | null {
	const configured = FAMILY_HUBS[family];
	if (configured && pages.has(configured)) return configured;
	if (pages.has(family)) return family;

	// Walk up the family (drop trailing tokens / path segments) until a pillar
	// page is found: "jasa-cetak-buku-aceh" -> "jasa-cetak-buku" -> "percetakan/cetak-buku".
	let current = family;
	for (let guard = 0; guard < 8; guard++) {
		const parts = current.split("/");
		const last = parts[parts.length - 1] ?? "";
		const trimmed = last.includes("-") ? last.slice(0, last.lastIndexOf("-")) : "";
		current = trimmed
			? [...parts.slice(0, -1), trimmed].join("/")
			: parts.slice(0, -1).join("/");
		if (!current) return null;

		const ancestorHub = FAMILY_HUBS[current];
		if (ancestorHub && pages.has(ancestorHub)) return ancestorHub;
		if (pages.has(current)) return current;
	}
	return null;
}

/** Root of a family, used as the anchor-text prefix ("jasa-cetak-buku-aceh" -> "jasa-cetak-buku"). */
function rootFamilyOf(family: string | null): string | null {
	if (!family) return null;
	let best: string | null = FAMILY_HUBS[family] ? family : null;

	let current = family;
	for (let guard = 0; guard < 8; guard++) {
		const parts = current.split("/");
		const last = parts[parts.length - 1] ?? "";
		const trimmed = last.includes("-") ? last.slice(0, last.lastIndexOf("-")) : "";
		current = trimmed
			? [...parts.slice(0, -1), trimmed].join("/")
			: parts.slice(0, -1).join("/");
		if (!current) break;
		if (FAMILY_HUBS[current]) best = current;
	}
	return best ?? family;
}

async function getGraph(): Promise<Graph> {
	const now = Date.now();
	if (graphCache && now - graphCache.at < CACHE_TTL_MS) return graphCache.graph;

	const pages = await loadPublishedPages();
	if (pages.length === 0) return graphCache?.graph ?? buildGraph([]);

	const graph = buildGraph(pages);
	graphCache = { at: now, graph };
	return graph;
}

function hash(input: string): number {
	let h = 2166136261;
	for (let i = 0; i < input.length; i++) {
		h ^= input.charCodeAt(i);
		h = Math.imul(h, 16777619);
	}
	return Math.abs(h);
}

const SMALL_WORDS = new Set(["di", "dan", "untuk", "ke", "dari", "yang", "pada", "dengan", "atau", "the", "of", "and", "in"]);

/** Words too generic to signal topical similarity. */
const STOP_WORDS = new Set([
	"jasa",
	"di",
	"dan",
	"untuk",
	"ke",
	"dari",
	"yang",
	"pada",
	"dengan",
	"atau",
	"the",
	"of",
	"and",
	"in",
	"murah",
	"terbaik",
	"online",
	"no",
	"layanan",
	"kami",
	"anda",
	"kota",
	"kabupaten",
	"baru",
	"isi",
	"jual",
]);

function titleCase(input: string): string {
	return input
		.replace(/[/_]+/g, " ")
		.split(/[\s-]+/)
		.filter(Boolean)
		.map((word, index) =>
			index > 0 && SMALL_WORDS.has(word.toLowerCase())
				? word.toLowerCase()
				: word.charAt(0).toUpperCase() + word.slice(1),
		)
		.join(" ");
}

/** Page title trimmed down to a usable anchor: drop brand tails, flatten SHOUTING titles. */
function cleanTitle(value: string): string {
	let title = String(value ?? "")
		.replace(/&amp;/g, "&")
		.replace(/&quot;/g, '"')
		.replace(/&#0?39;|&apos;/g, "'")
		.replace(/&nbsp;/g, " ")
		.replace(/&lt;/g, "<")
		.replace(/&gt;/g, ">")
		.replace(/\s*[|•]\s*.*$/, "")
		.replace(/\s+[-–—]\s+.*$/, "")
		.replace(/\s+/g, " ")
		.trim();

	const letters = title.replace(/[^A-Za-z]/g, "");
	const upper = title.replace(/[^A-Z]/g, "");
	// Nobody wants an anchor in ALL CAPS.
	if (letters.length > 8 && upper.length / letters.length > 0.6) {
		title = title
			.toLowerCase()
			.replace(/(^|[\s\-/(])([a-z])/g, (_match, prefix, char) => `${prefix}${char.toUpperCase()}`);
	}

	return title;
}

function truncate(value: string, max: number): string {
	if (value.length <= max) return value;
	const cut = value.slice(0, max);
	const lastSpace = cut.lastIndexOf(" ");
	return `${(lastSpace > max * 0.5 ? cut.slice(0, lastSpace) : cut).trim()}…`;
}

/**
 * Standalone label for a page (used for hub and cross-pillar links, where a
 * page title is usually too long or too vague to read well as an anchor).
 */
export function pageLabel(target: LinkTarget, max = 72): string {
	const title = cleanTitle(target.title);
	const tokens = target.slug.split(/[/-]+/).filter(Boolean);
	const slugLabel = titleCase(target.slug);

	// Generated titles are sometimes cut mid-word ("...Operasional Bi..."),
	// which reads badly as an anchor: fall back to the keyword-rich slug label.
	const truncatedTitle = /(\.\.\.|…)\s*$/.test(title);

	if (!truncatedTitle && tokens.length === 1 && title) return truncate(title, max);
	if (!truncatedTitle && title.length >= 12 && title.length <= max) return title;
	if (slugLabel.length <= max) return slugLabel;
	return truncate(title || slugLabel, max);
}

/**
 * Short, slug-derived label ("Jasa Cetak Buku Mojokerto" -> "Mojokerto"), used for
 * compact link chips where the full page title would be noise.
 */
export function tailAnchor(target: LinkTarget): string {
	const parts = target.slug.split("/").filter(Boolean);
	const segment = parts[parts.length - 1] ?? "";
	const tokens = segment.split("-").filter(Boolean);

	// City page: "jasa-cetak-buku-bolaang-mongondow-selatan" -> "Bolaang Mongondow Selatan".
	for (let size = Math.min(MAX_CITY_TOKENS, tokens.length); size >= 1; size--) {
		if (size === tokens.length) continue;
		const key = tokens.slice(tokens.length - size).join("-");
		if (CITY_PROVINCE[key]) return truncate(titleCase(key), 44);
	}

	// Province hub: "percetakan/cetak-buku/jawa-timur" -> "Jawa Timur".
	const provinceSlug = provinceHubOfSlug(target.slug);
	if (provinceSlug) return truncate(PROVINCE_BY_SLUG[provinceSlug].name, 44);

	return truncate(titleCase(segment || target.slug), 44);
}

/**
 * Anchor text for a target page.
 * Short geo/niche tails ("aceh-barat") read as city names, longer slugs fall
 * back to their page title, and the variant rotates per page so a single page
 * never repeats the same anchor pattern for all of its links.
 */
export function anchorFor(target: LinkTarget, family: string | null, index: number): string {
	const tail = tailAfter(target.slug, family);
	const tokens = tail.split("-").filter(Boolean);
	const seed = (hash(target.slug) + index) % 3;

	if (tokens.length > 0 && tokens.length <= 4) {
		const tailLabel = titleCase(tail);
		if (seed === 0) return tailLabel;
		if (seed === 1) return `${titleCase(family ?? "")} ${tailLabel}`.trim();
		return `layanan ${tailLabel}`;
	}

	const fromTitle = cleanTitle(target.title);
	if (fromTitle) return truncate(fromTitle, seed === 0 ? 48 : 64);
	return truncate(titleCase(tail || target.slug), 64);
}


/** `count` items from `list`, starting at the first entry after `anchorSlug` (wrapping). */
function ringAround(list: LinkTarget[], anchorSlug: string, count: number): LinkTarget[] {
	if (list.length === 0) return [];
	const found = list.findIndex((page) => page.slug > anchorSlug);
	const start = found === -1 ? 0 : found;
	const out: LinkTarget[] = [];
	for (let step = 0; step < Math.min(count, list.length); step++) {
		out.push(list[(start + step) % list.length]);
	}
	return out;
}

export async function getRelatedLinks(slug: string): Promise<RelatedLinks> {
	const empty: RelatedLinks = {
		family: null,
		anchorFamily: null,
		hub: null,
		parents: [],
		province: null,
		lateral: [],
		cross: [],
		directory: [],
		directoryLabel: "",
		lateralLabel: "",
	};
	const clean = String(slug ?? "").replace(/^\/+|\/+$/g, "");
	if (!clean || SKIP_SLUGS.has(clean)) return empty;

	const graph = await getGraph();
	const current = graph.pages.get(clean);
	if (!current) return empty;

	const family = graph.familyOf.get(clean) ?? null;
	const familyHubSlug = family ? resolveHubSlug(family, graph.pages) : null;

	// Province layer: a page either *is* a province hub or belongs to one.
	const provinceSlug = provinceHubOfSlug(clean) ?? graph.provinceOf.get(clean);
	const provinceData = provinceSlug ? PROVINCE_BY_SLUG[provinceSlug] : undefined;
	const province: ProvinceRef | null = provinceData
		? { slug: provinceData.slug, name: provinceData.name }
		: null;
	const isProvinceHubPage = Boolean(provinceHubOfSlug(clean));

	// --- Upward link: nearest province hub, then the national pillar --------
	let hubSlug = familyHubSlug;
	const provinceHubSlug = provinceSlug ? `${PROVINCE_HUB_PREFIX}${provinceSlug}` : null;
	if (!isProvinceHubPage && provinceHubSlug && graph.pages.has(provinceHubSlug)) {
		hubSlug = provinceHubSlug;
	}
	const hub = hubSlug && hubSlug !== clean ? graph.pages.get(hubSlug) ?? null : null;

	const parents: LinkTarget[] = [];
	if (familyHubSlug && familyHubSlug !== clean && familyHubSlug !== hubSlug) {
		const parent = graph.pages.get(familyHubSlug);
		if (parent) parents.push(parent);
	}

	// --- Lateral links: same province first, then the family ring ----------
	const members = family ? (graph.byFamily.get(family) ?? []).filter((p) => p.slug !== clean) : [];
	const lateral: LinkTarget[] = [];
	const pushLateral = (page: LinkTarget | undefined) => {
		if (!page || lateral.length >= LATERAL_COUNT) return;
		if (page.slug === clean || lateral.some((l) => l.slug === page.slug)) return;
		lateral.push(page);
	};

	if (provinceSlug && members.length > 0) {
		// City pages of the same province are the most useful neighbours.
		const rootFamily = graph.rootFamilyOf.get(clean) ?? family;
		const siblings = (graph.byProvince.get(provinceSlug) ?? [])
			.filter(
				(p) => p.slug !== clean && (!rootFamily || (graph.rootFamilyOf.get(p.slug) ?? null) === rootFamily),
			)
			.sort((a, b) => a.slug.localeCompare(b.slug));
		for (const page of ringAround(siblings, clean, LATERAL_COUNT)) pushLateral(page);
	}

	if (lateral.length < LATERAL_COUNT && members.length > 0) {
		for (const page of ringAround(members, clean, LATERAL_COUNT)) pushLateral(page);

		// A couple of "same leading token" neighbours (e.g. all "aceh-*" pages).
		const tail = tailAfter(clean, family);
		const firstToken = tail.split("-")[0];
		if (firstToken && firstToken.length > 2) {
			const cluster = members.filter(
				(p) => !lateral.some((l) => l.slug === p.slug) && tailAfter(p.slug, family).startsWith(firstToken),
			);
			for (const page of cluster.slice(0, 2)) pushLateral(page);
		}
	}

	// --- Cross-pillar links: same topic/city in another family -------------
	const cross: LinkTarget[] = [];
	const tail = tailAfter(clean, family);
	const seen = new Set<string>([
		clean,
		...lateral.map((p) => p.slug),
		...(hub ? [hub.slug] : []),
		...parents.map((p) => p.slug),
	]);

	const isPillarPage = graph.hubsOf.has(clean);
	const push = (page: LinkTarget | undefined) => {
		if (!page || seen.has(page.slug) || cross.length >= CROSS_COUNT) return;
		// Province hubs are structural, not topical: never offer "Jawa Timur" as a
		// "related service" for a city page just because both end in "timur".
		if (!isPillarPage && provinceHubOfSlug(page.slug)) return;
		seen.add(page.slug);
		cross.push(page);
	};

	if (isProvinceHubPage && familyHubSlug) {
		// A province hub is a geographic page, not a topic page: link sideways to the
		// other pillars of the same parent (cetak buku -> cetak kartu nama, ...)
		// instead of chasing token similarity across the whole site.
		const parentFamily = graph.familyOf.get(familyHubSlug) ?? null;
		for (const page of parentFamily ? graph.byFamily.get(parentFamily) ?? [] : []) push(page);
	}

	if (!isProvinceHubPage && tail) {
		const matches = (graph.byTail.get(tail) ?? [])
			.filter((entry) => entry.family !== family)
			.sort((a, b) => a.page.slug.localeCompare(b.page.slug));
		for (const entry of matches) push(entry.page);
	}

	if (!isProvinceHubPage && cross.length < CROSS_COUNT) {
		// Same topic, different service: score pages sharing distinctive slug
		// tokens with the current one (e.g. "software" -> other software pages).
		const ownTokens = graph.tokensOf.get(clean) ?? [];
		const scored = new Map<string, { page: LinkTarget; score: number }>();
		for (const token of ownTokens) {
			const bucket = graph.byToken.get(token) ?? [];
			if (bucket.length > 150) continue; // too generic to be a signal
			// Rarer tokens are a stronger signal: weight each match by 1/log2(size).
			const weight = 1 / Math.log2(bucket.length + 2);
			for (const page of bucket) {
				if (page.slug === clean) continue;
				const entry = scored.get(page.slug);
				if (entry) entry.score += weight;
				else scored.set(page.slug, { page, score: weight });
			}
		}
		const ranked = [...scored.values()]
			.sort((a, b) => b.score - a.score || (hash(a.page.slug) % 97) - (hash(b.page.slug) % 97))
			.map((entry) => entry.page);
		for (const page of ranked) push(page);
	}

	if (!isProvinceHubPage && cross.length < CROSS_COUNT) {
		const pillarPool = PILLAR_FALLBACKS.map((s) => graph.pages.get(s)).filter(
			(p): p is LinkTarget => Boolean(p),
		);
		if (pillarPool.length > 0) {
			const offset = hash(clean) % pillarPool.length;
			for (let i = 0; i < pillarPool.length && cross.length < CROSS_COUNT; i++) {
				push(pillarPool[(offset + i) % pillarPool.length]);
			}
		}
	}

	// --- Directory ---------------------------------------------------------
	const directory: LinkTarget[] = [];
	let directoryLabel = "";

	if (isProvinceHubPage && provinceSlug) {
		// Only the city pages of the family this province hub fronts (e.g. the
		// "jasa-cetak-buku-*" pages), not every page that happens to end in a city name.
		const childFamilies = new Set<string>(familyHubSlug ? graph.hubsOf.get(familyHubSlug) ?? [] : []);
		const cities = (graph.byProvince.get(provinceSlug) ?? [])
			.filter((p) => !seen.has(p.slug))
			.filter(
				(p) =>
					childFamilies.size === 0 ||
					childFamilies.has((graph.rootFamilyOf.get(p.slug) ?? "") as string),
			)
			.sort((a, b) => a.slug.localeCompare(b.slug));
		directory.push(...cities.slice(0, DIRECTORY_LIMIT));
		if (directory.length > 0) {
			directoryLabel = `Kota & kabupaten di ${province?.name ?? "provinsi ini"}`;
		}
	} else {
		const familiesForHub = graph.hubsOf.get(clean) ?? [];
		if (familiesForHub.length > 0) {
			// A pillar that fronts a province-mapped family lists the provinces
			// first, so the national page points at the regional layer.
			const coversProvinces = familiesForHub.some((hubFamily) =>
				(graph.byFamily.get(hubFamily) ?? []).some((member) => graph.provinceOf.has(member.slug)),
			);
			if (coversProvinces && graph.provinceHubs.length > 0) {
				directory.push(
					...graph.provinceHubs.filter((p) => !seen.has(p.slug)).slice(0, DIRECTORY_LIMIT),
				);
				directoryLabel = "Pilih provinsi Anda";
			} else {
				const children: LinkTarget[] = [];
				for (const hubFamily of familiesForHub) {
					for (const member of graph.byFamily.get(hubFamily) ?? []) {
						if (!seen.has(member.slug)) children.push(member);
					}
				}
				children.sort((a, b) => a.slug.localeCompare(b.slug));
				directory.push(...children.slice(0, DIRECTORY_LIMIT));
				if (directory.length > 0) directoryLabel = "Pilih kota atau wilayah Anda";
			}
		}
	}

	// Only promise a province in the heading when every lateral link is in it.
	const provinceScoped =
		Boolean(provinceSlug) &&
		lateral.length > 0 &&
		lateral.every((page) => graph.provinceOf.get(page.slug) === provinceSlug);
	const lateralLabel = isProvinceHubPage
		? "Provinsi lain"
		: provinceScoped && province
			? `Layanan serupa di ${province.name}`
			: "Layanan serupa";

	return {
		family,
		anchorFamily: rootFamilyOf(family),
		hub,
		parents,
		province,
		lateral,
		cross,
		directory,
		directoryLabel,
		lateralLabel,
	};
}
