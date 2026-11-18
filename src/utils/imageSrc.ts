// Best-effort WebP resolver for static /images/* assets.
// Uses a build-time manifest (webp-manifest.json) instead of fs.existsSync so it
// behaves identically during SSG and inside the Docker build stage.
// Falls back to the original path when no WebP sibling is listed.
import manifest from "./webp-manifest.json";

const webpSet = new Set<string>(manifest as string[]);

/** Rewrite "/images/foo.png" -> "/images/foo.webp" when that WebP is in the manifest. */
export function webpSrc(src: unknown): unknown {
	if (typeof src !== "string") return src;
	if (!src.startsWith("/images/") || !/\.(png|jpe?g)$/i.test(src)) return src;
	const candidate = src.replace(/\.(png|jpe?g)$/i, ".webp");
	return webpSet.has(candidate) ? candidate : src;
}
