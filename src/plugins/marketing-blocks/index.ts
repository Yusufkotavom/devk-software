/**
 * Marketing blocks plugin (inline, template-local).
 *
 * Registers the marketing block types so editors can insert and edit them
 * in the admin's Portable Text editor. Block Kit `fields` describe the form
 * shown when inserting or editing a block.
 *
 * Constraints worth knowing:
 *
 * - Block Kit has no "object group" element, so nested object shapes (e.g. a
 *   CTA's { label, url }) are flattened to sibling fields like ctaLabel and
 *   ctaUrl. The site-side renderer reads the flat keys.
 * - Repeater sub-fields are scalar only: text_input, number_input, select,
 *   toggle. Nested repeaters are not allowed -- list-of-strings becomes a
 *   single multiline text field, split on newline at render time (see
 *   Pricing.astro for the pattern).
	 * - There is no media picker element in the editor's plugin-block modal yet,
	 *   so image fields are URL strings entered by hand.
 *
 * Site-side rendering is wired via componentsEntry and MarketingBlocks.astro.
 */

import { definePlugin } from "emdash";
import type { PluginDefinition } from "emdash";

const ICON_OPTIONS = [
	{ label: "Lightning", value: "zap" },
	{ label: "Shield", value: "shield" },
	{ label: "Users", value: "users" },
	{ label: "Chart", value: "chart" },
	{ label: "Code", value: "code" },
	{ label: "Globe", value: "globe" },
	{ label: "Heart", value: "heart" },
	{ label: "Star", value: "star" },
	{ label: "Check", value: "check" },
	{ label: "Lock", value: "lock" },
	{ label: "Clock", value: "clock" },
	{ label: "Cloud", value: "cloud" },
	{ label: "Storefront / Kasir", value: "storefront" },
	{ label: "Shopping Cart", value: "cart" },
	{ label: "Desktop / PC", value: "desktop" },
	{ label: "Database", value: "database" },
	{ label: "CPU / Chip", value: "cpu" },
	{ label: "Wrench / Install", value: "wrench" },
	{ label: "Gear / Settings", value: "gear" },
	{ label: "Rocket", value: "rocket" },
];

const CONTACT_ICON_OPTIONS = [
	{ label: "Email", value: "email" },
	{ label: "Support", value: "support" },
	{ label: "Sales", value: "sales" },
	{ label: "Phone", value: "phone" },
	{ label: "Chat", value: "chat" },
	{ label: "Location", value: "location" },
];

const COLUMN_OPTIONS = [
	{ label: "2 columns", value: "2" },
	{ label: "3 columns", value: "3" },
	{ label: "4 columns", value: "4" },
];

const PANEL_OPTIONS = [
	{ label: "None (blend with page)", value: "none" },
	{ label: "Soft panel", value: "sunken" },
	{ label: "Dark panel", value: "ink" },
];

const POSITION_OPTIONS = [
	{ label: "Image after text", value: "end" },
	{ label: "Image before text", value: "start" },
	{ label: "Image above text", value: "top" },
	{ label: "Image as background", value: "background" },
];

const FEED_SOURCE_OPTIONS = [
	{ label: "Posts (blog)", value: "posts" },
	{ label: "Products", value: "products" },
	{ label: "Pages", value: "pages" },
];

const FEED_MODE_OPTIONS = [
	{ label: "Latest", value: "latest" },
	{ label: "By category", value: "category" },
	{ label: "By tag", value: "tag" },
	{ label: "Random", value: "random" },
];

const FEED_LAYOUT_OPTIONS = [
	{ label: "Grid", value: "grid" },
	{ label: "List", value: "list" },
	{ label: "Slider", value: "slide" },
];

/**
 * Header text for a new Capabilities block. The admin pre-fills the fields with
 * it, and Capabilities.astro falls back to it when a field is absent.
 */
export const capabilitiesDefaults = {
	headline: "Build your next blog or microsite today",
	subheadline: "EmDash combines with Astro to create one end-to-end TypeScript CMS and frontend.",
};

const definition: PluginDefinition = {
	id: "marketing-blocks",
	version: "0.1.0",

	admin: {
		portableTextBlocks: [
			{
				type: "marketing.hero",
				label: "Hero",
				description: "Headline with optional links or agent actions",
				fields: [
					{ type: "text_input", action_id: "headline", label: "Headline" },
					{
						type: "text_input",
						action_id: "subheadline",
						label: "Subheadline",
						multiline: true,
					},
					{ type: "text_input", action_id: "primaryCtaLabel", label: "Primary CTA label" },
					{ type: "text_input", action_id: "primaryCtaUrl", label: "Primary CTA URL" },
					{ type: "text_input", action_id: "secondaryCtaLabel", label: "Secondary CTA label" },
					{ type: "text_input", action_id: "secondaryCtaUrl", label: "Secondary CTA URL" },
					{ type: "toggle", action_id: "showAgentActions", label: "Show agent actions instead of secondary CTA" },
					{
						type: "text_input",
						action_id: "agentPrompt",
						label: "Agent starter prompt (optional)",
						multiline: true,
					},
					{ type: "toggle", action_id: "centered", label: "Center the layout" },
					{ type: "text_input", action_id: "imageUrl", label: "Image URL (optional)" },
					{ type: "text_input", action_id: "imageCaption", label: "Image caption (optional)" },
					{
						type: "select",
						action_id: "imageFit",
						label: "Ukuran / Tampilan Gambar",
						options: [
							{ label: "Cover (16:9 Wide)", value: "cover" },
							{ label: "Full (1:1 / Utuh Tanpa Terpotong)", value: "full" },
						],
						initial_value: "cover",
					},
					{
						type: "select",
						action_id: "imageSide",
						label: "Posisi Visual",
						options: [
							{ label: "Kanan (teks kiri)", value: "right" },
							{ label: "Kiri (teks kanan)", value: "left" },
						],
						initial_value: "right",
					},
				],
			},

			{
				type: "marketing.capabilities",
				label: "Capabilities (Bento Grid)",
				description: "Feature bento modern dengan kartu dinamis yang dapat diedit bebas",
				fields: [
					{ type: "text_input", action_id: "eyebrow", label: "Eyebrow", initial_value: "KEMAMPUAN PLATFORM" },
					{ type: "text_input", action_id: "headline", label: "Headline", initial_value: "Solusi Lengkap & Terintegrasi" },
					{
						type: "text_input",
						action_id: "subheadline",
						label: "Subheadline / Introduction",
						multiline: true,
						initial_value: "Kombinasi performa cepat, integrasi fleksibel, dan kemudahan manajemen konten.",
					},
					{
						type: "repeater",
						action_id: "items",
						label: "Cards",
						item_label: "Card",
						min_items: 1,
						max_items: 12,
						fields: [
							{ type: "text_input", action_id: "title", label: "Judul Card", initial_value: "Performa Tinggi" },
							{ type: "text_input", action_id: "description", label: "Deskripsi", multiline: true, initial_value: "Rendering server native dengan waktu respon sub-100ms." },
							{ type: "text_input", action_id: "tag", label: "Category Tag (misal: SPEED)", initial_value: "PERFORMANCE" },
							{ type: "text_input", action_id: "icon", label: "Nama Icon (ph:rocket, ph:shield, dll)", initial_value: "rocket" },
							{
								type: "select",
								action_id: "col_span",
								label: "Lebar Kolom (1, 2, atau 3)",
								options: [
									{ label: "1 Kolom", value: "1" },
									{ label: "2 Kolom", value: "2" },
									{ label: "3 Kolom", value: "3" },
								],
								initial_value: "1",
							},
							{ type: "text_input", action_id: "link_url", label: "URL Tujuan (opsional)" },
						],
					},
					{ type: "text_input", action_id: "anchor_id", label: "Section ID (optional)" },
				],
			},

			{
				type: "marketing.features",
				label: "Features",
				description: "Grid of feature cards with icons",
				fields: [
					{ type: "text_input", action_id: "headline", label: "Headline" },
					{
						type: "text_input",
						action_id: "subheadline",
						label: "Subheadline",
						multiline: true,
					},
					{
						type: "select",
						action_id: "columns",
						label: "Columns",
						options: COLUMN_OPTIONS,
						initial_value: "3",
					},
					{
						type: "select",
						action_id: "panel",
						label: "Panel background",
						options: PANEL_OPTIONS,
						initial_value: "none",
					},
					{
						type: "repeater",
						action_id: "features",
						label: "Features",
						item_label: "Feature",
						min_items: 1,
						max_items: 12,
						fields: [
							{
								type: "select",
								action_id: "icon",
								label: "Icon",
								options: ICON_OPTIONS,
							},
							{
								type: "text_input",
								action_id: "imageUrl",
								label: "Image URL (opsional, ganti icon dengan gambar)",
							},
							{ type: "text_input", action_id: "title", label: "Title" },
							{
								type: "text_input",
								action_id: "description",
								label: "Description",
								multiline: true,
							},
							{ type: "text_input", action_id: "linkLabel", label: "Link label (optional)" },
							{ type: "text_input", action_id: "linkUrl", label: "Link URL (optional)" },
						],
					},
				],
			},

			{
				type: "marketing.testimonials",
				label: "Testimonials",
				description: "Customer testimonial cards",
				fields: [
					{ type: "text_input", action_id: "headline", label: "Headline" },
					{
						type: "repeater",
						action_id: "testimonials",
						label: "Testimonials",
						item_label: "Testimonial",
						min_items: 1,
						fields: [
							{ type: "text_input", action_id: "quote", label: "Quote", multiline: true },
							{ type: "text_input", action_id: "author", label: "Author name" },
							{ type: "text_input", action_id: "role", label: "Role / title" },
							{ type: "text_input", action_id: "company", label: "Company" },
							{ type: "text_input", action_id: "imageUrl", label: "Avatar image URL (optional)" },
						],
					},
				],
			},

			{
				type: "marketing.pricing",
				label: "Pricing",
				description: "Pricing plan comparison cards",
				fields: [
					{ type: "text_input", action_id: "headline", label: "Headline" },
					{
						type: "repeater",
						action_id: "plans",
						label: "Plans",
						item_label: "Plan",
						min_items: 1,
						max_items: 6,
						fields: [
							{ type: "text_input", action_id: "name", label: "Plan name" },
							{
								type: "text_input",
								action_id: "price",
								label: "Price",
								placeholder: "$29 or Custom",
							},
							{
								type: "text_input",
								action_id: "period",
								label: "Period",
								placeholder: "/month",
							},
							{
								type: "text_input",
								action_id: "description",
								label: "Description",
								multiline: true,
							},
							{
								type: "text_input",
								action_id: "features",
								label: "Features (one per line)",
								multiline: true,
								placeholder: "Unlimited projects\nPriority support\nSSO",
							},
							{ type: "text_input", action_id: "ctaLabel", label: "CTA label" },
							{ type: "text_input", action_id: "ctaUrl", label: "CTA URL" },
							{ type: "toggle", action_id: "highlighted", label: "Highlight this plan" },
						],
					},
				],
			},

			{
				type: "marketing.faq",
				label: "FAQ",
				description: "Frequently asked questions",
				fields: [
					{ type: "text_input", action_id: "headline", label: "Headline" },
					{
						type: "repeater",
						action_id: "items",
						label: "Questions",
						item_label: "Question",
						min_items: 1,
						fields: [
							{ type: "text_input", action_id: "question", label: "Question" },
							{
								type: "text_input",
								action_id: "answer",
								label: "Answer",
								multiline: true,
							},
						],
					},
				],
			},
			{
				type: "marketing.cta",
				label: "Call to Action",
				description: "Call to action banner",
				fields: [
					{ type: "text_input", action_id: "headline", label: "Headline" },
					{ type: "text_input", action_id: "body", label: "Body text", multiline: true },
					{ type: "text_input", action_id: "primaryCtaLabel", label: "Primary CTA label" },
					{ type: "text_input", action_id: "primaryCtaUrl", label: "Primary CTA URL" },
					{ type: "text_input", action_id: "secondaryCtaLabel", label: "Secondary CTA label" },
					{ type: "text_input", action_id: "secondaryCtaUrl", label: "Secondary CTA URL" },
					{ type: "text_input", action_id: "imageUrl", label: "Background image URL (optional)" },
				],
			},
			{
				type: "marketing.logos",
				label: "Logos",
				description: "Logo marquee track",
				fields: [
					{ type: "text_input", action_id: "headline", label: "Headline" },
					{
						type: "repeater",
						action_id: "logos",
						label: "Logos",
						item_label: "Logo",
						min_items: 1,
						fields: [
							{ type: "text_input", action_id: "name", label: "Brand name (used as alt text for images)" },
							{ type: "text_input", action_id: "imageUrl", label: "Logo image URL (optional — shows an image instead of the name)" },
						],
					},
				],
			},
			{
				type: "marketing.split",
				label: "Split Content",
				description: "Two-column feature with highlights and CTA",
				fields: [
					{ type: "text_input", action_id: "eyebrow", label: "Eyebrow" },
					{ type: "text_input", action_id: "headline", label: "Headline" },
					{ type: "text_input", action_id: "body", label: "Body text", multiline: true },
					{
						type: "text_input",
						action_id: "points",
						label: "Bullet points (one per line)",
						multiline: true,
					},
					{ type: "text_input", action_id: "ctaLabel", label: "CTA label" },
					{ type: "text_input", action_id: "ctaUrl", label: "CTA URL" },
					{ type: "text_input", action_id: "imageUrl", label: "Image URL (optional)" },
					{ type: "text_input", action_id: "imageCaption", label: "Image caption (optional)" },
					{
						type: "select",
						action_id: "imageFit",
						label: "Ukuran / Tampilan Gambar",
						options: [
							{ label: "Cover (16:9 Wide)", value: "cover" },
							{ label: "Full (1:1 / Utuh Tanpa Terpotong)", value: "full" },
						],
						initial_value: "cover",
					},
					{ type: "toggle", action_id: "imageFirst", label: "Show media first" },
				],
			},
			{
				type: "marketing.stats",
				label: "Stats",
				description: "Key metrics and statistics",
				fields: [
					{ type: "text_input", action_id: "headline", label: "Headline" },
					{ type: "text_input", action_id: "subheadline", label: "Subheadline" },
					{ type: "select", action_id: "panel", label: "Panel background", options: PANEL_OPTIONS, initial_value: "none" },
					{
						type: "repeater",
						action_id: "stats",
						label: "Statistics",
						item_label: "Stat",
						min_items: 1,
						fields: [
							{ type: "text_input", action_id: "label", label: "Label" },
							{ type: "text_input", action_id: "value", label: "Value (e.g. 99.9% or 10M+)" },
							{ type: "text_input", action_id: "description", label: "Caption (optional)", multiline: true },
						],
					},
				],
			},
			{
				type: "marketing.contact",
				label: "Contact",
				description: "Contact channels and options",
				fields: [
					{ type: "text_input", action_id: "eyebrow", label: "Eyebrow" },
					{ type: "text_input", action_id: "headline", label: "Headline" },
					{ type: "text_input", action_id: "subheadline", label: "Subheadline", multiline: true },
					{
						type: "repeater",
						action_id: "options",
						label: "Contact options",
						item_label: "Option",
						min_items: 1,
						fields: [
							{
								type: "select",
								action_id: "icon",
								label: "Icon",
								options: CONTACT_ICON_OPTIONS,
							},
							{ type: "text_input", action_id: "title", label: "Title" },
							{ type: "text_input", action_id: "description", label: "Description", multiline: true },
							{ type: "text_input", action_id: "linkLabel", label: "Link label" },
							{ type: "text_input", action_id: "linkUrl", label: "Link URL" },
						],
					},
				],
			},
			{
				type: "marketing.richtext",
				label: "Rich Text",
				description: "Long-form rich text section",
				fields: [
					{ type: "text_input", action_id: "headline", label: "Headline" },
					{ type: "text_input", action_id: "body", label: "Body text", multiline: true },
				],
			},
			{
				type: "marketing.feature_section",
				label: "Feature Section",
				description: "Headline, copy, media (or auto card) and buttons",
				fields: [
					{ type: "text_input", action_id: "eyebrow", label: "Eyebrow" },
					{ type: "text_input", action_id: "headline", label: "Headline" },
					{ type: "text_input", action_id: "body", label: "Body text", multiline: true },
					{
						type: "text_input",
						action_id: "points",
						label: "Bullet points (one per line)",
						multiline: true,
					},
					{ type: "text_input", action_id: "primaryCtaLabel", label: "Primary button label" },
					{ type: "text_input", action_id: "primaryCtaUrl", label: "Primary button URL" },
					{ type: "text_input", action_id: "secondaryCtaLabel", label: "Secondary button label" },
					{ type: "text_input", action_id: "secondaryCtaUrl", label: "Secondary button URL" },
					{ type: "text_input", action_id: "imageUrl", label: "Image URL (optional — leave empty for an auto-generated card)" },
					{ type: "text_input", action_id: "imageCaption", label: "Image caption (optional)" },
					{ type: "select", action_id: "position", label: "Media position", options: POSITION_OPTIONS, initial_value: "end" },
					{ type: "select", action_id: "panel", label: "Panel background", options: PANEL_OPTIONS, initial_value: "none" },
				],
			},
			{
				type: "marketing.slider",
				label: "Slider",
				description: "Horizontal slides of images and cards",
				fields: [
					{ type: "text_input", action_id: "eyebrow", label: "Eyebrow" },
					{ type: "text_input", action_id: "headline", label: "Headline" },
					{
						type: "text_input",
						action_id: "subheadline",
						label: "Subheadline",
						multiline: true,
					},
					{
						type: "select",
						action_id: "layout",
						label: "Slide style",
						options: [
							{ label: "Card", value: "card" },
							{ label: "Wide (image + text)", value: "wide" },
						],
						initial_value: "card",
					},
					{
						type: "select",
						action_id: "panel",
						label: "Panel background",
						options: PANEL_OPTIONS,
						initial_value: "none",
					},
					{
						type: "repeater",
						action_id: "slides",
						label: "Slides",
						item_label: "Slide",
						min_items: 1,
						max_items: 12,
						fields: [
							{ type: "text_input", action_id: "imageUrl", label: "Image URL (optional)" },
							{ type: "text_input", action_id: "title", label: "Title" },
							{ type: "text_input", action_id: "description", label: "Description", multiline: true },
							{ type: "text_input", action_id: "linkLabel", label: "Link label (optional)" },
							{ type: "text_input", action_id: "linkUrl", label: "Link URL (optional)" },
						],
					},
				],
			},
			{
				type: "marketing.feed",
				label: "Content Feed",
				description: "List posts, products or pages by tag, category or latest",
				fields: [
					{ type: "text_input", action_id: "eyebrow", label: "Eyebrow" },
					{ type: "text_input", action_id: "headline", label: "Headline" },
					{
						type: "text_input",
						action_id: "subheadline",
						label: "Subheadline",
						multiline: true,
					},
					{ type: "select", action_id: "source", label: "Content type", options: FEED_SOURCE_OPTIONS, initial_value: "posts" },
					{ type: "select", action_id: "mode", label: "Mode", options: FEED_MODE_OPTIONS, initial_value: "latest" },
					{ type: "text_input", action_id: "term", label: "Category / tag slug (for the modes above)" },
					{ type: "number_input", action_id: "limit", label: "How many items", initial_value: 6 },
					{ type: "select", action_id: "layout", label: "Layout", options: FEED_LAYOUT_OPTIONS, initial_value: "grid" },
					{ type: "text_input", action_id: "ctaLabel", label: "\"View all\" label (optional)" },
					{ type: "text_input", action_id: "ctaUrl", label: "\"View all\" URL (optional)" },
				],
			},
			{
				type: "marketing.steps",
				label: "Steps / How It Works",
				description: "Numbered workflow sequence explaining a process or methodology",
				fields: [
					{ type: "text_input", action_id: "eyebrow", label: "Eyebrow", initial_value: "CARA KERJA" },
					{ type: "text_input", action_id: "headline", label: "Headline", initial_value: "3 Langkah Mudah Menuju Hasil Maksimal" },
					{
						type: "text_input",
						action_id: "subheadline",
						label: "Subheadline",
						multiline: true,
						initial_value: "Proses terstruktur dan transparan untuk memastikan proyek Anda selesai tepat waktu.",
					},
					{
						type: "repeater",
						action_id: "steps",
						label: "Steps",
						item_label: "Step",
						min_items: 1,
						max_items: 10,
						fields: [
							{ type: "text_input", action_id: "step_number", label: "Nomor Step (01, 02)", initial_value: "01" },
							{ type: "text_input", action_id: "title", label: "Judul Step", initial_value: "Konsultasi & Discovery" },
							{ type: "text_input", action_id: "description", label: "Deskripsi", multiline: true, initial_value: "Kami membedah kebutuhan, tantangan, dan tujuan spesifik bisnis Anda." },
						],
					},
					{ type: "text_input", action_id: "anchor_id", label: "Section ID (optional)" },
				],
			},
			{
				type: "marketing.tabs",
				label: "Tabs Showcase",
				description: "Tab interaktif untuk menampilkan modul, spesifikasi, atau use cases",
				fields: [
					{ type: "text_input", action_id: "eyebrow", label: "Eyebrow", initial_value: "KAPABILITAS" },
					{ type: "text_input", action_id: "headline", label: "Headline", initial_value: "Solusi Lengkap dalam Satu Ekosistem" },
					{
						type: "text_input",
						action_id: "subheadline",
						label: "Subheadline",
						multiline: true,
						initial_value: "Pilih tab di bawah untuk melihat detail kapabilitas yang kami sediakan.",
					},
					{
						type: "repeater",
						action_id: "tabs",
						label: "Tabs",
						item_label: "Tab",
						min_items: 1,
						max_items: 10,
						fields: [
							{ type: "text_input", action_id: "tab_id", label: "Tab ID (unik)", initial_value: "tab-1" },
							{ type: "text_input", action_id: "tab_label", label: "Label Tab", initial_value: "Overview" },
							{ type: "text_input", action_id: "title", label: "Judul Konten", initial_value: "Performa Tinggi & Andal" },
							{ type: "text_input", action_id: "description", label: "Deskripsi", multiline: true, initial_value: "Arsitektur modern yang menjamin kecepatan akses dan kestabilan sistem." },
							{ type: "text_input", action_id: "image_url", label: "URL Gambar (opsional)" },
						],
					},
					{ type: "text_input", action_id: "anchor_id", label: "Section ID (optional)" },
				],
			},
			{
				type: "marketing.whatsapp_cta",
				label: "WhatsApp CTA",
				description: "Banner atau kartu ajakan diskusi / order via WhatsApp",
				fields: [
					{ type: "text_input", action_id: "headline", label: "Headline", initial_value: "Siap Mewujudkan Proyek Anda?" },
					{
						type: "text_input",
						action_id: "subheadline",
						label: "Subheadline",
						multiline: true,
						initial_value: "Konsultasikan kebutuhan teknis Anda bersama kami secara langsung melalui WhatsApp.",
					},
					{ type: "text_input", action_id: "button_text", label: "Teks Tombol", initial_value: "Chat WhatsApp Sekarang" },
					{ type: "text_input", action_id: "custom_message", label: "Pesan WhatsApp Custom" },
					{
						type: "select",
						action_id: "variant",
						label: "Style Tampilan",
						options: [
							{ label: "Banner", value: "banner" },
							{ label: "Card", value: "card" },
						],
						initial_value: "banner",
					},
					{ type: "text_input", action_id: "anchor_id", label: "Section ID (optional)" },
				],
			},
			{
				type: "marketing.bento_grid",
				label: "Bento Grid Showcase",
				description: "Grid modern asimetris ala Vercel/Linear untuk fitur, visual, dan code snippet",
				fields: [
					{ type: "text_input", action_id: "eyebrow", label: "Eyebrow", initial_value: "TEKNOLOGI MODERN" },
					{ type: "text_input", action_id: "headline", label: "Headline", initial_value: "Dirancang untuk Efisiensi & Skalabilitas" },
					{
						type: "text_input",
						action_id: "subheadline",
						label: "Subheadline",
						multiline: true,
						initial_value: "Kombinasi arsitektur headless modern, integrasi cerdas, dan performa tanpa kompromi.",
					},
					{
						type: "repeater",
						action_id: "cards",
						label: "Cards",
						item_label: "Card",
						min_items: 1,
						max_items: 12,
						fields: [
							{ type: "text_input", action_id: "title", label: "Judul Card", initial_value: "Infrastruktur Cepat & Aman" },
							{ type: "text_input", action_id: "description", label: "Deskripsi", multiline: true, initial_value: "Deployment terisolasi dengan Docker Swarm dan proteksi edge network." },
							{ type: "text_input", action_id: "tag", label: "Category Tag (misal: SPEED)", initial_value: "PERFORMANCE" },
							{ type: "text_input", action_id: "icon", label: "Nama Icon", initial_value: "rocket" },
							{
								type: "select",
								action_id: "col_span",
								label: "Lebar Kolom (1, 2, atau 3)",
								options: [
									{ label: "1 Kolom", value: "1" },
									{ label: "2 Kolom", value: "2" },
									{ label: "3 Kolom", value: "3" },
								],
								initial_value: "1",
							},
							{ type: "text_input", action_id: "link_url", label: "URL Tujuan (opsional)" },
						],
					},
					{ type: "text_input", action_id: "anchor_id", label: "Section ID (optional)" },
				],
			},
			{
				type: "marketing.comparison_table",
				label: "Comparison Table",
				description: "Matriks perbandingan fitur ala SaaS: Kita vs Solusi Lain",
				fields: [
					{ type: "text_input", action_id: "eyebrow", label: "Eyebrow", initial_value: "PERBANDINGAN" },
					{ type: "text_input", action_id: "headline", label: "Headline", initial_value: "Mengapa Memilih Devk Software?" },
					{
						type: "text_input",
						action_id: "subheadline",
						label: "Subheadline",
						multiline: true,
						initial_value: "Lihat perbedaan nyata dalam kecepatan, fleksibilitas, dan keandalan sistem.",
					},
					{ type: "text_input", action_id: "our_label", label: "Nama Solusi Kita", initial_value: "Devk Platform" },
					{ type: "text_input", action_id: "competitor_label", label: "Nama Solusi Lain", initial_value: "Solusi Konvensional" },
					{
						type: "repeater",
						action_id: "rows",
						label: "Daftar Perbandingan",
						item_label: "Baris",
						min_items: 1,
						max_items: 20,
						fields: [
							{ type: "text_input", action_id: "feature_name", label: "Nama Fitur", initial_value: "Setup & Deployment Cepat" },
							{ type: "text_input", action_id: "our_value", label: "Nilai Kita ('yes' / teks)", initial_value: "yes" },
							{ type: "text_input", action_id: "competitor_value", label: "Nilai Kompetitor ('no' / teks)", initial_value: "no" },
						],
					},
					{ type: "text_input", action_id: "cta_label", label: "Label Tombol CTA", initial_value: "Mulai Sekarang" },
					{ type: "text_input", action_id: "cta_url", label: "URL Tombol CTA", initial_value: "#contact" },
					{ type: "text_input", action_id: "anchor_id", label: "Section ID (optional)" },
				],
			},
			{
				type: "marketing.marquee_logos",
				label: "Logo Marquee (Infinite Scroll)",
				description: "Slider logo berjalan halus otomatis tanpa jeda untuk social proof",
				fields: [
					{ type: "text_input", action_id: "headline", label: "Headline Teks", initial_value: "Dipercaya oleh berbagai bisnis dan developer" },
					{
						type: "repeater",
						action_id: "logos",
						label: "Daftar Logo",
						item_label: "Logo",
						min_items: 1,
						max_items: 20,
						fields: [
							{ type: "text_input", action_id: "name", label: "Nama Brand", initial_value: "Brand Partner" },
							{ type: "text_input", action_id: "logo_url", label: "URL File Logo", initial_value: "/images/placeholder-logo.svg" },
							{ type: "text_input", action_id: "link_url", label: "Link Target (opsional)" },
						],
					},
					{ type: "text_input", action_id: "anchor_id", label: "Section ID (optional)" },
				],
			},
		],
	},
};

/** The registered blocks, in slash-menu order. The capabilities illustration lists them. */
export const portableTextBlocks = definition.admin?.portableTextBlocks ?? [];

export function createPlugin() {
	return definePlugin(definition);
}

export default createPlugin;
