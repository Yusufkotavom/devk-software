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
  /** How many times to retry a 429/5xx/network failure (default from env or 4). */
  maxRetries?: number;
  /** First backoff delay in ms; doubles each attempt (default 1500). */
  baseDelayMs?: number;
  /** Upper bound for a single backoff wait in ms (default 30000). */
  maxDelayMs?: number;
  /** Per-request timeout in ms (default 60000). */
  timeoutMs?: number;
  /** Max tokens for the completion (default from env or 2000). */
  maxTokens?: number;
}

const DEFAULT_MAX_TOKENS = 2000;

/**
 * System prompt sent with every generation request. Kept as a named constant
 * so brand voice / SEO rules live in one place and are easy to tune.
 */
export const SYSTEM_PROMPT = [
  "Anda adalah penulis konten SEO senior untuk Kotacom, usaha percetakan buku dan solusi IT yang berbasis di Surabaya–Sidoarjo, Jawa Timur.",
  "Layanan Kotacom: cetak buku satuan (print-on-demand) maupun grosir/offset, pilihan kertas bookpaper, opsi jilid, pengurusan ISBN, dan proofing sebelum cetak; serta layanan IT.",
  "",
  "Tugas: menulis PERSIS bagian konten yang diminta pada pesan pengguna, mengikuti format, panjang, dan bahasa yang diminta.",
  "Aturan wajib:",
  "- Bahasa Indonesia natural, jelas, profesional, langsung ke inti; tanpa pembuka basa-basi ('di era digital', 'tentu saja') dan tanpa penutup klise.",
  "- SELALU relevan dengan topik yang diminta (cetak buku / percetakan / layanan Kotacom). JANGAN menulis tentang topik lain (mis. hosting, domain, software) kecuali diminta eksplisit.",
  "- Sebut Kotacom dan area layanan Surabaya/Sidoarjo secara wajar bila relevan.",
  "- JANGAN mengarang fakta, angka, harga pasti, alamat, nomor telepon, atau klaim sertifikasi. Untuk harga, gunakan rentang/kualitatif tanpa angka palsu; untuk kontak, arahkan ke WhatsApp Kotacom.",
  "- Jika diminta meta description atau judul, patuhi batas panjangnya (meta 150–158 karakter).",
  "- Bila membantu, gunakan subjudul markdown (##), daftar bernomor/bullet, dan tautan internal format markdown [teks](/path). Jangan menambah markdown lain bila tidak diminta.",
].join("\n");

const sleep = (ms: number): Promise<void> => new Promise((r) => setTimeout(r, ms));

/** HTTP statuses worth retrying. 4xx (other than 429) are caller errors. */
function isRetryableStatus(status: number): boolean {
  return status === 429 || status === 500 || status === 502 || status === 503 || status === 504;
}

/**
 * Call local or remote OpenAI-compatible chat completion endpoint
 */
export async function callAiCompletion(prompt: string, config?: AiConfig): Promise<string> {
  const endpoint = config?.endpoint?.trim() || process.env.EMDASH_AI_ENDPOINT?.trim() || "http://172.18.0.1:20128/v1/chat/completions";
  const model = config?.model?.trim() || "daily";
  const apiKey = config?.apiKey?.trim() || process.env.EMDASH_AI_API_KEY?.trim() || "";
  const maxRetries = Math.max(0, config?.maxRetries ?? (Number.parseInt(process.env.EMDASH_AI_MAX_RETRIES || "", 10) || 4));
  const baseDelayMs = config?.baseDelayMs ?? (Number.parseInt(process.env.EMDASH_AI_RETRY_BASE_MS || "", 10) || 1500);
  const maxDelayMs = config?.maxDelayMs ?? 30000;
  const timeoutMs = config?.timeoutMs ?? (Number.parseInt(process.env.EMDASH_AI_TIMEOUT_MS || "", 10) || 60000);

  const requestBody = JSON.stringify({
    model,
    messages: [
      { role: "system", content: SYSTEM_PROMPT },
      { role: "user", content: prompt },
    ],
    stream: false,
    temperature: 0.7,
    max_tokens: config?.maxTokens ?? (Number.parseInt(process.env.EMDASH_AI_MAX_TOKENS || "", 10) || DEFAULT_MAX_TOKENS),
  });

  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (apiKey) headers.Authorization = `Bearer ${apiKey}`;

  for (let attempt = 0; ; attempt++) {
    let res: Response;
    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), timeoutMs);
      try {
        res = await fetch(endpoint, { method: "POST", headers, body: requestBody, signal: controller.signal });
      } finally {
        clearTimeout(timer);
      }
    } catch (err: any) {
      if (attempt < maxRetries) {
        const wait = Math.min(maxDelayMs, baseDelayMs * 2 ** attempt) + Math.floor(Math.random() * 250);
        console.warn(`[AI Completion] network error (${err?.message || err}); retry ${attempt + 1}/${maxRetries} in ${wait}ms`);
        await sleep(wait);
        continue;
      }
      console.warn(`[AI Completion] network error after ${attempt} retries: ${err?.message || err}`);
      return "";
    }

    if (isRetryableStatus(res.status) && attempt < maxRetries) {
      const retryAfter = Number.parseFloat(res.headers.get("retry-after") || "");
      let wait = Number.isNaN(retryAfter) ? baseDelayMs * 2 ** attempt : retryAfter * 1000;
      wait = Math.min(maxDelayMs, wait) + Math.floor(Math.random() * 250);
      console.warn(`[AI Completion] HTTP ${res.status}; retry ${attempt + 1}/${maxRetries} in ${wait}ms`);
      try { await res.text(); } catch { /* drain body before retry */ }
      await sleep(wait);
      continue;
    }

    if (!res.ok) {
      console.warn(`[AI Completion] HTTP error: ${res.status} (not retried)`);
      return "";
    }

    const resText = await res.text();
    let text = "";
    try {
      const data = JSON.parse(resText);
      text = data?.choices?.[0]?.message?.content ?? "";
    } catch {
      // SSE streaming chunks
      for (const line of resText.split("\n")) {
        if (line.startsWith("data: ") && line.trim() !== "data: [DONE]") {
          try {
            const chunk = JSON.parse(line.replace("data: ", ""));
            text += chunk?.choices?.[0]?.delta?.content || "";
          } catch {}
        }
      }
    }
    text = text.trim();
    if (!text) {
      // Empty completion (some models return 200 with no content) — treat it
      // as a transient failure and retry so sections never render blank.
      if (attempt < maxRetries) {
        const wait = Math.min(maxDelayMs, baseDelayMs * 2 ** attempt) + Math.floor(Math.random() * 250);
        console.warn(`[AI Completion] empty response; retry ${attempt + 1}/${maxRetries} in ${wait}ms (model=${model})`);
        await sleep(wait);
        continue;
      }
      console.warn(`[AI Completion] empty response after ${attempt} retries (model=${model})`);
      return "";
    }
    return text;
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
