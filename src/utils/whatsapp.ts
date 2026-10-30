import { getEmDashCollection } from "emdash";

export interface WhatsAppSetting {
	title?: string;
	whatsapp_number?: string;
	callout_text?: string;
	default_message?: string;
	enabled?: boolean | number;
	append_source_url?: boolean | number;
	include_page_title?: boolean | number;
	source_label?: string;
	product_cta_label?: string;
	post_cta_label?: string;
	product_message_template?: string;
	post_message_template?: string;
}

export type WhatsAppContext =
	| "general"
	| "floating"
	| "product"
	| "post"
	| "page"
	| "block";

export interface WhatsAppBuildOptions {
	pageUrl?: string;
	pageTitle?: string;
	context?: WhatsAppContext;
	customMessage?: string;
	customLabel?: string;
}

let cachedSetting: WhatsAppSetting | null = null;
let lastFetchTime = 0;

export async function getWhatsAppSettings(): Promise<WhatsAppSetting | null> {
	const now = Date.now();
	if (cachedSetting && now - lastFetchTime < 10000) {
		return cachedSetting;
	}

	try {
		const res = await getEmDashCollection("whatsapp_settings", { limit: 1 });
		if (res && res.entries && res.entries.length > 0) {
			cachedSetting = res.entries[0].data as WhatsAppSetting;
			lastFetchTime = now;
			return cachedSetting;
		}
	} catch (e) {
		// Fallback
	}

	return cachedSetting;
}

export function sanitizePhoneNumber(input?: string | null): string {
	return (input || "").replace(/[^0-9]/g, "");
}

export function buildWhatsAppMessage(
	setting: WhatsAppSetting | null,
	opts: WhatsAppBuildOptions = {},
): string {
	const context = opts.context || "general";
	const pageTitle = opts.pageTitle || "";
	const pageUrl = opts.pageUrl || "";

	if (opts.customMessage) {
		return opts.customMessage
			.replace(/\{title\}/g, pageTitle)
			.replace(/\{url\}/g, pageUrl);
	}

	let baseMessage = setting?.default_message?.trim() || "Halo, saya ingin konsultasi layanan Anda.";

	if (context === "product") {
		baseMessage =
			setting?.product_message_template?.trim() ||
			"Halo, saya tertarik dengan produk *{title}*. Apakah masih tersedia?";
	} else if (context === "post") {
		baseMessage =
			setting?.post_message_template?.trim() ||
			"Halo Kotacom, saya membaca artikel *{title}* dan ingin konsultasi kebutuhan cetak atau digital untuk bisnis saya.";
	}

	baseMessage = baseMessage.replace(/\{title\}/g, pageTitle).replace(/\{url\}/g, pageUrl);

	const parts: string[] = [baseMessage];

	const includeTitle =
		setting?.include_page_title === true ||
		setting?.include_page_title === 1 ||
		setting?.include_page_title === "1";

	if (includeTitle && pageTitle && !baseMessage.includes(pageTitle)) {
		parts.push(`*Halaman:* ${pageTitle}`);
	}

	const appendSource =
		setting?.append_source_url === true ||
		setting?.append_source_url === 1 ||
		setting?.append_source_url === "1" ||
		true; // default enabled for conversion tracking

	if (appendSource && pageUrl) {
		const label = setting?.source_label?.trim() || "Sumber";
		parts.push(`${label}: ${pageUrl}`);
	}

	return parts.join("\n\n");
}

export function buildWhatsAppHref(
	setting: WhatsAppSetting | null,
	opts: WhatsAppBuildOptions = {},
): string {
	const rawNumber = setting?.whatsapp_number?.trim() || "6285799520350";
	const cleanNumber = sanitizePhoneNumber(rawNumber);
	if (!cleanNumber) return "#";

	const message = buildWhatsAppMessage(setting, opts);
	return `https://wa.me/${cleanNumber}?text=${encodeURIComponent(message)}`;
}
