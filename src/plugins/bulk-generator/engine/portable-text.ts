/**
 * Generate a random short key for Portable Text blocks
 */
function randomKey(): string {
  return Math.random().toString(36).substring(2, 10) + Math.random().toString(36).substring(2, 6);
}

export interface PortableTextMarkDef {
  _key: string;
  _type: "link";
  href: string;
}
export interface PortableTextBlock {
  _type: "block";
  _key: string;
  style: "normal" | "h1" | "h2" | "h3" | "h4" | "blockquote";
  listItem?: "bullet" | "number";
  level?: number;
  children: Array<{
    _type: "span";
    _key: string;
    text: string;
    marks?: string[];
  }>;
  markDefs?: PortableTextMarkDef[];
}

/**
 * Parse inline markdown (links `[label](url)` and bold `**text**`) into
 * Portable Text spans + markDefs. Everything else stays a plain span.
 */
function inlineSpans(text: string): {
  children: PortableTextBlock["children"];
  markDefs: PortableTextMarkDef[];
} {
  const children: PortableTextBlock["children"] = [];
  const markDefs: PortableTextMarkDef[] = [];
  // Alternation: [label](url)  |  **bold**
  const re = /\[([^\]]+)\]\(([^)\s]+)\)|\*\*([^*]+)\*\*/g;
  let last = 0;
  let m: RegExpExecArray | null;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) {
      const plain = text.slice(last, m.index);
      if (plain) children.push({ _type: "span", _key: randomKey(), text: plain, marks: [] });
    }
    if (m[1] !== undefined && m[2] !== undefined) {
      // link
      const key = "lnk" + randomKey();
      markDefs.push({ _key: key, _type: "link", href: m[2].trim() });
      children.push({ _type: "span", _key: randomKey(), text: m[1], marks: [key] });
    } else if (m[3] !== undefined) {
      // bold
      children.push({ _type: "span", _key: randomKey(), text: m[3], marks: ["strong"] });
    }
    last = re.lastIndex;
  }
  if (last < text.length) {
    const tail = text.slice(last);
    if (tail) children.push({ _type: "span", _key: randomKey(), text: tail, marks: [] });
  }
  if (children.length === 0) {
    children.push({ _type: "span", _key: randomKey(), text: "", marks: [] });
  }
  return { children, markDefs };
}

function block(style: PortableTextBlock["style"], text: string, listItem?: "bullet" | "number"): PortableTextBlock {
  const { children, markDefs } = inlineSpans(text);
  const b: PortableTextBlock = { _type: "block", _key: randomKey(), style, children, markDefs };
  if (listItem) {
    b.listItem = listItem;
    b.level = 1;
  }
  return b;
}

/**
 * Converts markdown text into Portable Text JSON blocks.
 * Supports: h1–h4, blockquote, bullet & numbered lists, inline links and bold.
 */
export function markdownToPortableText(markdown: string): PortableTextBlock[] {
  if (!markdown || !markdown.trim()) {
    return [block("normal", "")];
  }

  const lines = markdown.split(/\r?\n/);
  const blocks: PortableTextBlock[] = [];

  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line) continue;

    if (line.startsWith("#### ")) {
      blocks.push(block("h4", line.replace(/^####\s+/, "")));
    } else if (line.startsWith("### ")) {
      blocks.push(block("h3", line.replace(/^###\s+/, "")));
    } else if (line.startsWith("## ")) {
      blocks.push(block("h2", line.replace(/^##\s+/, "")));
    } else if (line.startsWith("# ")) {
      blocks.push(block("h1", line.replace(/^#\s+/, "")));
    } else if (line.startsWith("> ")) {
      blocks.push(block("blockquote", line.replace(/^>\s+/, "")));
    } else if (/^[-*]\s+/.test(line)) {
      blocks.push(block("normal", line.replace(/^[-*]\s+/, ""), "bullet"));
    } else if (/^\d+[.)]\s+/.test(line)) {
      blocks.push(block("normal", line.replace(/^\d+[.)]\s+/, ""), "number"));
    } else {
      blocks.push(block("normal", line));
    }
  }

  return blocks;
}
