// Ad-hoc sanity check for the internal link graph. Run:
//   PGHOST=10.0.1.195 PGPASSWORD=... node scripts/check-internal-links.mjs
import { getRelatedLinks, anchorFor } from "../src/lib/internal-links.ts";

const samples = process.argv.slice(2);
const slugs = samples.length
	? samples
	: [
			"jasa-cetak-buku-aceh-barat",
			"jasa-cetak-buku-sanggau",
			"rekomendasi-jual-game-pc-bandung-barat",
			"pembuatan-website/bandung",
			"jasa-install-autocad",
			"percetakan/cetak-buku",
			"software",
			"about",
		];

for (const slug of slugs) {
	const res = await getRelatedLinks(slug);
	console.log(`\n=== ${slug}`);
	console.log(`family: ${res.family} | anchorFamily: ${res.anchorFamily}`);
	console.log(`province: ${res.province ? `${res.province.name} (${res.province.slug})` : "-"}`);
	console.log(`hub: ${res.hub ? res.hub.slug : "-"}`);
	console.log(`parents: ${res.parents.map((p) => p.slug).join(" | ") || "-"}`);
	console.log(`lateral: ${res.lateral.map((p, i) => `${p.slug} [${anchorFor(p, res.anchorFamily, i)}]`).join(" | ") || "-"}`);
	console.log(`cross: ${res.cross.map((p) => p.slug).join(" | ") || "-"}`);
	console.log(`directory: ${res.directory.length} entries "${res.directoryLabel}"${res.directory.length ? ` (${res.directory.slice(0, 5).map((p) => p.slug).join(", ")}…)` : ""}`);
}

// Link-graph coverage: how many published pages receive at least one inbound link?
const { readFile } = await import("node:fs/promises");
const visited = new Map();
const all = JSON.parse(await readFile(new URL("./_slugs.json", import.meta.url), "utf8"));
for (const slug of all) {
	const res = await getRelatedLinks(slug);
	for (const target of [res.hub, ...res.parents, ...res.lateral, ...res.cross, ...res.directory].filter(Boolean)) {
		visited.set(target.slug, (visited.get(target.slug) ?? 0) + 1);
	}
}
const orphans = all.filter((slug) => !visited.has(slug));
console.log(`\nTotal pages: ${all.length} | with inbound related link: ${all.length - orphans.length} | without: ${orphans.length}`);
if (orphans.length) console.log("No inbound:", orphans.slice(0, 25).join(", "));
