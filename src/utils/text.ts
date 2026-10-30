const PARAGRAPH_BREAK = /\n\s*\n/;

/** Splits plain text into paragraphs at blank lines, dropping empty ones. */
export function toParagraphs(text: string | null | undefined): string[] {
	return (text ?? "")
		.split(PARAGRAPH_BREAK)
		.map((paragraph) => paragraph.trim())
		.filter(Boolean);
}

/** Formats text by turning {word} into gradient text and *word* into a highlight marker */
export function formatAccentWords(text: string | null | undefined): string {
	if (!text) return "";
	return text
		.replace(/\{([^}]+)\}/g, '<span class="text-accent-gradient">$1</span>')
		.replace(/\*([^*]+)\*/g, '<span class="highlight-marker">$1</span>');
}
