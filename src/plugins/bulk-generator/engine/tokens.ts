/**
 * Slugify string helper.
 *
 * Mirrors EmDash's own slugify (@emdash-cms/admin/slugify) so the slug we
 * expect matches the one EmDash auto-generates from an entry's title. The
 * plugin content API cannot set a slug directly, so an exact match here keeps
 * skip_existing / update_existing from silently creating duplicates.
 */
export function slugify(text: string): string {
  return text
    .toString()
    .normalize("NFKC")
    .toLowerCase()
    .replace(/[\s_]+/gu, "-")
    .replace(/[^\p{Letter}\p{Number}\p{Mark}-]+/gu, "")
    .replace(/-+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80)
    .replace(/-+$/g, "");
}

/**
 * Replace spintax patterns: {opsi A|opsi B|opsi C}
 * Only matches if pipe '|' exists to avoid interfering with single {bracket} tokens
 */
export function resolveSpintax(text: string): string {
  if (!text) return "";
  let result = text;
  const spintaxRegex = /\{([^{}|]+\|[^{}]+)\}/g;
  while (spintaxRegex.test(result)) {
    result = result.replace(spintaxRegex, (_, choices) => {
      const parts = choices.split("|");
      return parts[Math.floor(Math.random() * parts.length)].trim();
    });
  }
  return result;
}

/**
 * Replace {{token}} or {{token | filter}} in a template string
 * Filters supported:
 * - slug: converts to URL slug
 * - lower: to lowercase
 * - upper: to uppercase
 * - title: Title Case
 */
export function substituteTokens(template: string, row: Record<string, string>): string {
  if (!template) return "";

  let res = template.replace(/\{\{\s*([a-zA-Z0-9_\-]+)(?:\s*\|\s*([a-zA-Z0-9_\-]+))?\s*\}\}/g, (_, key, filter) => {
    let val = row[key] ?? row[key.trim()] ?? "";

    if (filter) {
      const f = filter.trim().toLowerCase();
      if (f === "slug") val = slugify(val);
      else if (f === "lower") val = val.toLowerCase();
      else if (f === "upper") val = val.toUpperCase();
      else if (f === "title") val = val.replace(/\w\S*/g, (txt) => txt.charAt(0).toUpperCase() + txt.slice(1).toLowerCase());
    }

    return val;
  });

  return resolveSpintax(res);
}

/**
 * Sync version for templates without AI tokens
 */
export function deepSubstituteTokens<T>(input: T, row: Record<string, string>): T {
  if (typeof input === "string") {
    return substituteTokens(input, row) as unknown as T;
  }
  if (Array.isArray(input)) {
    return input.map((item) => deepSubstituteTokens(item, row)) as unknown as T;
  }
  if (input !== null && typeof input === "object") {
    const result: Record<string, unknown> = {};
    for (const [key, val] of Object.entries(input)) {
      if (key === "_key") {
        result[key] = Math.random().toString(36).substring(2, 10);
      } else {
        result[key] = deepSubstituteTokens(val, row);
      }
    }
    return result as unknown as T;
  }
  return input;
}
export interface AiConfig {
  endpoint?: string;
  apiKey?: string;
  model?: string;
}

/**
 * Call local or remote OpenAI-compatible chat completion endpoint
 */
export async function callAiCompletion(prompt: string, config?: AiConfig): Promise<string> {
  const endpoint = config?.endpoint?.trim() || "http://172.18.0.1:20128/v1/chat/completions";
  const model = config?.model?.trim() || "daily";
  const apiKey = config?.apiKey?.trim() || "sk-e1c...b74e";

  try {
    const res = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model,
        messages: [
          {
            role: "system",
            content:
              "Anda adalah asisten penulis konten SEO profesional Bahasa Indonesia. Tulis konten berkualitas tinggi, natural, mengalir, tanpa basa-basi pembuka, langsung ke substansi inti.",
          },
          { role: "user", content: prompt },
        ],
        stream: false,
        temperature: 0.7,
        max_tokens: 1000,
      }),
    });

    if (!res.ok) {
      console.warn(`[AI Completion] HTTP error: ${res.status}`);
      return "";
    }

  const resText = await res.text();
  let data: any;
  try {
    data = JSON.parse(resText);
  } catch (e) {
    // If SSE streaming chunk
    const lines = resText.split("\n");
    let full = "";
    for (const line of lines) {
      if (line.startsWith("data: ") && line.trim() !== "data: [DONE]") {
        try {
          const chunk = JSON.parse(line.replace("data: ", ""));
          full += chunk?.choices?.[0]?.delta?.content || "";
        } catch {}
      }
    }
    return full.trim();
  }
  const text = data?.choices?.[0]?.message?.content?.trim() || "";
  return text;
  } catch (err: any) {
    console.warn(`[AI Completion] Failed to call AI endpoint: ${err?.message}`);
    return "";
  }
}

/**
 * Async token substitution including {{ai:...}} prompts
 */
export async function substituteTokensAsync(
  template: string,
  row: Record<string, string>,
  aiConfig?: AiConfig
): Promise<string> {
  if (!template) return "";

  // 1. Extract and replace {{ai:...}} patterns
  // Using custom matching to handle nested {{...}} inside the AI tag
  let text = template;
  const aiTagStart = "{{ai:";
  let startIndex = text.indexOf(aiTagStart);

  while (startIndex !== -1) {
    let depth = 0;
    let endIndex = -1;
    for (let i = startIndex; i < text.length - 1; i++) {
      if (text[i] === "{" && text[i + 1] === "{") {
        depth++;
        i++;
      } else if (text[i] === "}" && text[i + 1] === "}") {
        depth--;
        if (depth === 0) {
          endIndex = i + 2;
          break;
        }
        i++;
      }
    }

    if (endIndex === -1) break;

    const fullMatch = text.slice(startIndex, endIndex);
    const promptRaw = fullMatch.slice(aiTagStart.length, -2).trim();
    const promptSubstituted = substituteTokens(promptRaw, row).trim();

    let replacement = "";
    if (promptSubstituted) {
      let generated = await callAiCompletion(promptSubstituted, aiConfig);
      if (generated) {
        replacement = substituteTokens(generated, row);
      }
    }

    text = text.slice(0, startIndex) + replacement + text.slice(endIndex);
    startIndex = text.indexOf(aiTagStart);
  }

  // 2. Finally resolve regular tokens and spintax for the whole text
  return substituteTokens(text, row);
}

/**
 * Deep async token substitution
 */
export async function deepSubstituteTokensAsync<T>(
  input: T,
  row: Record<string, string>,
  aiConfig?: AiConfig
): Promise<T> {
  if (typeof input === "string") {
    return (await substituteTokensAsync(input, row, aiConfig)) as unknown as T;
  }
  if (Array.isArray(input)) {
    const arr: any[] = [];
    for (const item of input) {
      arr.push(await deepSubstituteTokensAsync(item, row, aiConfig));
    }
    return arr as unknown as T;
  }
  if (input !== null && typeof input === "object") {
    const result: Record<string, unknown> = {};
    for (const [key, val] of Object.entries(input)) {
      if (key === "_key") {
        result[key] = Math.random().toString(36).substring(2, 10);
      } else {
        result[key] = await deepSubstituteTokensAsync(val, row, aiConfig);
      }
    }
    return result as unknown as T;
  }
  return input;
}
