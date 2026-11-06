/**
 * Reusable Section placement resolver.
 *
 * A reusable_sections entry can be displayed in four ways (display_type):
 *   - inline     : embedded manually via a `/Section` block (existing behavior)
 *   - slot       : auto-injected into a named slot of a page template
 *   - popup      : modal overlay triggered by scroll / timer / exit-intent / click
 *   - sticky_bar : persistent floating banner pinned to the viewport
 *
 * Targeting is per entry:
 *   - target_collections : ["all"] or a list of collection slugs
 *   - target_categories  : comma-separated category slugs (empty = every category)
 */
import { getEmDashCollection } from "emdash";

export type SlotName = "after_title" | "middle_content" | "bottom_content" | "footer";
export type DisplayType = "inline" | "slot" | "popup" | "sticky_bar";
export type PopupTrigger = "scroll" | "timer" | "exit_intent" | "click";

export interface SectionPlacement {
	slug: string;
	title: string;
	displayType: DisplayType;
	slotPosition: SlotName | null;
	targetCollections: string[];
	targetCategories: string[];
	popupTrigger: PopupTrigger;
	popupThreshold: number;
	frequencyDays: number;
	isActive: boolean;
	blocks: unknown[];
}

interface RawEntry {
	id?: string;
	slug?: string;
	data?: Record<string, unknown>;
}

function asStringList(value: unknown): string[] {
	if (Array.isArray(value)) {
		return value.map((v) => String(v).trim().toLowerCase()).filter(Boolean);
	}
	if (typeof value === "string") {
		return value
			.split(",")
			.map((v) => v.trim().toLowerCase())
			.filter(Boolean);
	}
	return [];
}

function normalize(entry: RawEntry): SectionPlacement | null {
	const data = (entry.data ?? {}) as Record<string, unknown>;
	const slug = String(entry.slug ?? data.title ?? "");
	if (!slug) return null;

	const blocks = Array.isArray(data.blocks) ? (data.blocks as unknown[]) : [];
	if (blocks.length === 0) return null;

	const rawType = String(data.display_type ?? "inline");
	const displayType: DisplayType =
		rawType === "slot" || rawType === "popup" || rawType === "sticky_bar" ? rawType : "inline";

	const rawTrigger = String(data.popup_trigger ?? "scroll");
	const popupTrigger: PopupTrigger =
		rawTrigger === "timer" || rawTrigger === "exit_intent" || rawTrigger === "click"
			? rawTrigger
			: "scroll";

	const slotRaw = data.slot_position ? String(data.slot_position) : "";
	const slotPosition: SlotName | null =
		slotRaw === "after_title" ||
		slotRaw === "middle_content" ||
		slotRaw === "bottom_content" ||
		slotRaw === "footer"
			? slotRaw
			: null;

	return {
		slug,
		title: String(data.title ?? slug),
		displayType,
		slotPosition,
		targetCollections: asStringList(data.target_collections),
		targetCategories: asStringList(data.target_categories),
		popupTrigger,
		popupThreshold: Number(data.popup_threshold ?? 50) || 50,
		frequencyDays: Number(data.frequency_days ?? 7) || 7,
		isActive: data.is_active === undefined ? true : Boolean(data.is_active),
		blocks,
	};
}

/** Load every active placement. Small collection — one query per request is fine. */
export async function loadPlacements(): Promise<SectionPlacement[]> {
	try {
		const { entries } = await getEmDashCollection("reusable_sections", { limit: 100 });
		return (entries as unknown as RawEntry[])
			.map(normalize)
			.filter((p): p is SectionPlacement => p !== null && p.isActive);
	} catch {
		return [];
	}
}

function matchesTarget(
	placement: SectionPlacement,
	collection: string,
	categories: string[],
): boolean {
	const byCollection =
		placement.targetCollections.length === 0 ||
		placement.targetCollections.includes("all") ||
		placement.targetCollections.includes(collection.toLowerCase());
	if (!byCollection) return false;

	if (placement.targetCategories.length === 0) return true;
	if (categories.length === 0) return false;
	return placement.targetCategories.some((c) => categories.includes(c));
}

/** Sections to render inside a page slot. */
export async function getSectionsForSlot(
	slot: SlotName,
	collection: string,
	categories: string[] = [],
): Promise<SectionPlacement[]> {
	const placements = await loadPlacements();
	return placements.filter(
		(p) =>
			p.displayType === "slot" &&
			p.slotPosition === slot &&
			matchesTarget(p, collection, categories),
	);
}

/** Popup sections applicable to the current page. */
export async function getPopupsFor(
	collection: string,
	categories: string[] = [],
): Promise<SectionPlacement[]> {
	const placements = await loadPlacements();
	return placements.filter(
		(p) => p.displayType === "popup" && matchesTarget(p, collection, categories),
	);
}

/** Sticky bar sections applicable to the current page. */
export async function getStickyBarsFor(
	collection: string,
	categories: string[] = [],
): Promise<SectionPlacement[]> {
	const placements = await loadPlacements();
	return placements.filter(
		(p) => p.displayType === "sticky_bar" && matchesTarget(p, collection, categories),
	);
}
