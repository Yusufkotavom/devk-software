/**
 * Block shapes for the site's marketing blocks.
 *
 * `emdash-env.d.ts` is generated from the `page_templates` collection, so it
 * only knows 11 block shapes — and it names the rich-text block
 * `marketing_text`, while the plugin registers `marketing_richtext`. The plugin
 * in `src/plugins/marketing-blocks/index.ts` registers 20 block types, so
 * importing the generated union directly breaks for slider, feed, richtext,
 * steps, tabs, whatsapp_cta, bento_grid, comparison_table, marquee_logos,
 * capabilities and feature_section.
 *
 * This module is the single import site for block prop types. It re-exports the
 * generated members and widens them with a permissive shape for the rest, so
 * `Extract<PageContentBlock, { _type: "…" }>` still discriminates precisely on
 * `_type` and the components survive `emdash-env.d.ts` regeneration.
 */
import type { PageTemplateContentBlock } from "../../emdash-env";

export type { PageTemplateContentBlock };

/**
 * A block registered by the plugin but absent from the generated env union.
 * `_version` and `_key` are required by EmDash's `BlockValue` constraint; the
 * index signature lets components read fields without a generated shape.
 */
type PluginOnlyBlock<T extends string> = {
	_type: T;
	_version: number;
	_key: string;
	[key: string]: unknown;
};

export type MarketingRichtextBlock = PluginOnlyBlock<"marketing_richtext">;
export type MarketingStepsBlock = PluginOnlyBlock<"marketing_steps">;
export type MarketingTabsBlock = PluginOnlyBlock<"marketing_tabs">;
export type MarketingWhatsappCtaBlock = PluginOnlyBlock<"marketing_whatsapp_cta">;
export type MarketingBentoGridBlock = PluginOnlyBlock<"marketing_bento_grid">;
export type MarketingComparisonTableBlock = PluginOnlyBlock<"marketing_comparison_table">;
export type MarketingMarqueeLogosBlock = PluginOnlyBlock<"marketing_marquee_logos">;
export type MarketingCapabilitiesBlock = PluginOnlyBlock<"marketing_capabilities">;
export type MarketingSliderBlock = PluginOnlyBlock<"marketing_slider">;
export type MarketingFeedBlock = PluginOnlyBlock<"marketing_feed">;
export type MarketingFeatureSectionBlock = PluginOnlyBlock<"marketing_feature_section">;

export type PageContentBlock =
	| PageTemplateContentBlock
	| MarketingRichtextBlock
	| MarketingStepsBlock
	| MarketingTabsBlock
	| MarketingWhatsappCtaBlock
	| MarketingBentoGridBlock
	| MarketingComparisonTableBlock
	| MarketingMarqueeLogosBlock
	| MarketingCapabilitiesBlock
	| MarketingSliderBlock
	| MarketingFeedBlock
	| MarketingFeatureSectionBlock;
