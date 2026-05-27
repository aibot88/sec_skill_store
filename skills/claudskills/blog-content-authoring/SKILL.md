---
name: blog-content-authoring
description: Create/update Markdown blog posts and topic metadata for this Next.js static-export blog (multi-language en/tr). Use when adding/editing files under content/posts/**, updating post/topic indexes, choosing valid topic colors, and creating 1200x630 WebP thumbnails under public/images.
---

# Blog Content Authoring (en/tr)

This repo generates content via **static export**. List pages are driven by **JSON index** files, while the post detail page is driven by the **Markdown** file. Therefore, when adding a new post you must update Markdown + post index JSON + thumbnail + (if needed) topics/category index JSON together.

## File/Folder Map

- Posts (Markdown): `content/posts/<locale>/<slug>.md` (`<locale>`: `en` or `tr`)
- Post list index: `public/data/posts.<locale>.json`
- Topic list: `public/data/topics.<locale>.json`
- Category list: `public/data/categories.<locale>.json`
- Thumbnails: `public/images/*.webp` (referenced as `/images/<file>.webp` in Markdown/JSON)

## Non-Negotiable Rules (Summary)

1. **Slug/ID**: kebab-case (`my-new-post`). Use the same slug for both `en` and `tr`.
2. **Post index JSON is the source of truth**: list pages / RSS / sitemap use `public/data/posts.<locale>.json`. Markdown is read for the detail page content + frontmatter metadata.
3. **Sorting**: post index JSON should be kept in **publishedDate DESC** order (newest first).
4. **Images**: keep post images under `/images/` and prefer `webp` for consistency/performance.
5. **Thumbnail**: `1200x630` (OG size), `webp`, under `public/images/` (recommended name: `<slug>-thumbnail.webp`).
6. **Topic consistency**: topic `id`s must exist in topic index JSON in both locales; `name` is translated per locale; `color` must be one of the allowed values.
7. **Category consistency**: every post must have a `category` object (`id`, `name`) in Markdown frontmatter and post index JSON; category values come from `public/data/categories.<locale>.json`.
8. **Category/Topic separation**: do not duplicate the post category as a topic (e.g. `programming` belongs to `category`, not `topics[]`).
9. **Icon standards**: tab icons use the `[icon=...]` format and must be from the allowed set; step headings must use the standardized emoji + label format (see below).

## 2024+ Editorial Rule Set (Mandatory)

Use this rule set to keep every article at a modern, professional developer-blog quality bar (Vercel/Cloudflare/Stripe/GitHub Engineering style patterns).

### A) Structural contract (all posts)

1. `title` is specific and searchable; `summary` clearly states outcome and stays concise.
2. After frontmatter, include a short opening paragraph (2-4 sentences) that frames problem + value.
3. First main section is always `## 🌟 ...` and explains either:
   - what the reader will learn, or
   - why this approach matters.
4. `## 📋 Prerequisites` / `## 📋 Gereksinimler` must exist and be explicit.
5. Tutorial / implementation posts use sequential step headings (`## 🛠️/🧪/▶️ Step N` or `Adım N`).
6. `gaming` category posts do not use `Step N` / `Adım N` in headings. Use short editorial section titles instead (for example `## 🛠️ Official Facts`, `## 🛠️ Gameplay Pitch`, `## 🎬 Media`).
7. Each `##` section must contain real content (no empty headings).
8. End with a single `## 🏁 Conclusion` / `## 🏁 Sonuç`:
   - one concise synthesis paragraph,
   - one practical next step for production hardening.

### B) Readability & prose quality

1. No visual spacer hacks in markdown (remove `<span style="display:block; height:1rem;"></span>`).
2. No language-mixing in headings (`Adım ...: Add Dependencies` is invalid).
3. Keep heading hierarchy clean: main sections `##`, subsections `###`, avoid deeper nesting.
4. Keep prose direct and concrete; prefer short paragraphs and scannable bullets.
5. Avoid duplicate/redundant wording (e.g., repeated “Spring Boot” phrases in conclusions).

### C) Professional editing checks

1. Headings must reflect the section content; remove vague or dead headings.
2. Keep terminology consistent across the post (same concept, same naming).
3. Validation/testing instructions should include expected behavior (not just commands).
4. Conclusion should not be generic filler; it must summarize the delivered architecture/pattern.

### Batch standardization flow

```bash
# 1) Headings + typo/language cleanup + spacer cleanup
node .agents/skills/blog-content-authoring/scripts/standardize-posts.mjs --dry-run
node .agents/skills/blog-content-authoring/scripts/standardize-posts.mjs

# 2) Professional, non-generic conclusions (rewrite mode)
node .agents/skills/blog-content-authoring/scripts/standardize-conclusions.mjs --rewrite
```

## Image Standards

## Iram City Art Direction (Thumbnails & Inline Images)

Goal: make all **post visuals** (thumbnails + optional inline images) feel like they belong to the same world:

- Iram of the Pillars (Irem Şehri), ancient Arab myth-inspired lost city
- endless columns, monumental palaces, sacred timeless atmosphere
- terraced nature, clear water channels, reflective pools
- golden-hour / “golden light” beams, volumetric light, cinematic haze
- **no people**, no modern elements, no readable text/logos/watermarks
- style: fantastical realism, epic cinematic, wide angle, high detail

### Generate base Iram prompts for all posts

The helper script outputs one JSONL line per post with a single, topic-independent Iram prompt.

```bash
node .agents/skills/blog-content-authoring/scripts/generate-thumbnail-prompts.mjs > /tmp/irem-prompts.jsonl
```

### Prompt template (copy/paste)

Use this as-is in your image generator (SDXL / Midjourney / etc.):

**Base prompt**

- “Iram of the Pillars (Irem Şehri), ancient Arab myth-inspired lost city, majestic and mysterious sacred place, timeless, uninhabited (no people), endless columns and towering palaces, monumental architecture, terraced gardens integrated with nature, clear water channels, reflective pools, golden hour light beams, volumetric light, atmospheric haze, epic cinematic mood, fantastical realism, ultra-detailed, wide-angle, HDR”

**Negative prompt**

- “people, faces, crowds, text, logos, watermark, lowres, blurry, noise, oversaturated, cartoon, anime”

### Batch prompt generation for all existing posts

Generate one JSONL line per post (includes EN/TR prompts + negative prompt + suggested thumbnail path):

```bash
node .agents/skills/blog-content-authoring/scripts/generate-thumbnail-prompts.mjs > /tmp/irem-prompts.jsonl
```

Workflow suggestion:

1. Pick a post from `/tmp/irem-prompts.jsonl`
2. Generate an image at 1200x630 (or generate larger, then crop)
3. Convert/crop to blog thumbnail:

```bash
node .agents/skills/blog-content-authoring/scripts/make-thumbnail.mjs --in /path/to/generated.png --out public/images/<slug>-thumbnail.webp
```

### 1) Post thumbnail (required)

- **Purpose**: post list card + RSS/sitemap image + OG-like share image
- **Format**: `webp`
- **Dimensions**: `1200x630`
- **Location**: `public/images/`
- **Path in Markdown/post index JSON**: `/images/<slug>-thumbnail.webp`

#### Thumbnail quality checklist (must pass)

- No readable text (no UI text, no captions, no logos, no watermarks)
- Composition centered, with strong leading lines (columns/arches/perspective)
- 1200x630 output (crop if needed; avoid distorted aspect ratios)
- `webp` only
- Target file size: **< 350KB** (optimize/crop if larger)

Generate:

```bash
node .agents/skills/blog-content-authoring/scripts/make-thumbnail.mjs \
  --in /path/to/source.png \
  --out public/images/<slug>-thumbnail.webp
```

If `sharp` is not available locally, use the Cloudinary fallback helper (upload -> transformed URL -> local `webp`):

```bash
# Signed upload (recommended when unsigned preset is not enabled)
CLOUDINARY_CLOUD_NAME=<cloud_name> \
CLOUDINARY_API_KEY=<api_key> \
CLOUDINARY_API_SECRET=<api_secret> \
CLOUDINARY_UPLOAD_PRESET=<upload_preset> \
node .agents/skills/blog-content-authoring/scripts/make-thumbnail-cloudinary.mjs \
  --in /path/to/source.png \
  --out public/images/<slug>-thumbnail.webp
```

Remote image URL input is also supported:

```bash
node .agents/skills/blog-content-authoring/scripts/make-thumbnail-cloudinary.mjs \
  --in "https://example.com/source.jpg" \
  --out public/images/<slug>-thumbnail.webp \
  --cloud-name <cloud_name> \
  --upload-preset <unsigned_or_signed_preset> \
  --api-key <api_key> \
  --api-secret <api_secret>
```

Notes:

- Defaults to `w_1200,h_630,c_fill,f_webp,q_auto`
- Prints both the uploaded asset URL and the transformed delivery URL
- If `--public-id` is not provided, the script derives it from `--out` (e.g. `public/images/my-post-thumbnail.webp` -> `my-post-thumbnail`)
- If using only `--upload-preset`, the preset must allow unsigned uploads
- Do not commit Cloudinary secrets to the repo; use environment variables

### 2) Inline post images (optional)

If you add images inside the post body (Markdown/HTML):

- **Format**: prefer `webp`
- **Location**: `public/images/posts/<slug>/`
- **Reference path**: `/images/posts/<slug>/<name>.webp`

#### Gaming gallery standard (mandatory for `category.id: gaming`)

- If a gaming post includes a visual gallery, gallery cards use a consistent landscape ratio
- **Required output**: `1200x630`
- **Format**: `webp`
- **Use the same rendered dimensions in markdown**: `width="1200"` and `height="630"`
- Keep all gallery cards in the same post on the same ratio; do not mix square and landscape assets
- Trailer cards can stay feature-sized, but regular gallery cards should all follow the same `1200x630` standard

Generate (keeps aspect ratio, resizes to a max width):

```bash
node .agents/skills/blog-content-authoring/scripts/make-post-image.mjs \
  --in /path/to/source.png \
  --out public/images/posts/<slug>/<name>.webp \
  --maxWidth 1200
```

Recommended markup (for better layout stability):

```html
<figure>
  <img
    src="/images/posts/<slug>/<name>.webp"
    alt="Describe the image"
    width="1200"
    height="675"
    loading="lazy"
    decoding="async"
  />
  <figcaption>Optional caption</figcaption>
</figure>
```

Tip: use the generated file’s real `width`/`height` (the script prints it) to avoid layout shift.

## Icon & Heading Standards

### Tab icons (`:::tabs` + `@tab`)

Format:

```md
:::tabs
@tab Java [icon=java]
...
:::
```

Allowed tab icons:

- Languages: `java`, `kotlin`, `go`, `javascript`, `typescript`
- Build tools: `maven`, `gradle`

### Heading emojis (recommended)

Keep headings consistent across posts:

- **Overview / Why**
  - EN: `## 🌟 ...`
  - TR: `## 🌟 ...`
- **Prerequisites**
  - EN: `## 📋 Prerequisites`
  - TR: `## 📋 Gereksinimler`
- **Steps**
  - Build/implementation step:
    - EN: `## 🛠️ Step N: ...`
    - TR: `## 🛠️ Adım N: ...`
  - Testing/verification step: `## 🧪 Step N: ...` / `## 🧪 Adım N: ...`
  - Run/start step: `## ▶️ Step N: ...` / `## ▶️ Adım N: ...`
- **Gaming posts (`category.id: gaming`)**
  - Do not use numbered `Step N` / `Adım N` headings
  - Use short editorial `##` headings instead
    - EN: `## 🛠️ Official Facts`, `## 🛠️ Gameplay Pitch`, `## 🎬 Media`
    - TR: `## 🛠️ Resmi Bilgiler`, `## 🛠️ Oynanış Yaklaşımı`, `## 🎬 Medya`

Note: Avoid “random” emojis in headings. Prefer the small set above so posts feel consistent.

### Heading hierarchy & text style (repo standard)

Apply these rules for all EN/TR post markdown files:

- TOC is main-section oriented: keep **main sections as `##` only**.
- Use `###` for sub-sections (examples, controller snippets, notes).
- Every `###` heading must be followed by a short editorial lead-in (1-2 sentences) that explains intent/value before code/list blocks.
- Do not use `####` and deeper levels; collapse them to `###`.
- If a section title is plain (non-step/non-standard emoji), prefer making it a sub-section (`###`) rather than a new `##`.
- Keep body/list text plain; avoid bold emphasis markers (`**text**`, `__text__`) in prose.
- Keep technical tokens in inline code (`` `@ConfigurationProperties` ``, `` `application.yml` ``), not bold.

Goal: visual rhythm and hierarchy stay consistent across all posts without noisy emphasis.

## Conclusion Standard (Required)

All posts should end with a short, consistent conclusion section:

- EN: `## 🏁 Conclusion`
- TR: `## 🏁 Sonuç`

Template (EN):

- “This setup delivers a robust, production-ready … by combining …”

Template (TR):

- “Bu kurulum, … için sağlam ve üretim‑hazır bir yaklaşım sunar; …”

You can batch-apply this standard to all posts with:

```bash
node .agents/skills/blog-content-authoring/scripts/standardize-conclusions.mjs
```

## Add a New Post (Step-by-Step)

## Random Post Generation (Constrained Topics)

If you want to generate a **random new post idea** that still fits this blog’s content constraints, use the helper script below.

Constraints (topic pool):

- Java (`java`)
- Kotlin (`kotlin`)
- Spring Boot (`spring-boot`)
- Kubernetes (`kubernetes`)
- Go / Golang (`go`)

Generate a random post idea (deterministic with a seed):

```bash
node .agents/skills/blog-content-authoring/scripts/suggest-random-post.mjs --seed=2026-02-04
```

It prints:

- suggested `slug` + `publishedDate`
- EN/TR `title` + `summary`
- topic entries (id/name/color) for both locales
- a minimal outline that already follows the standard heading emojis and the single Conclusion rule

After picking an idea:

1. Create `content/posts/en/<slug>.md` and `content/posts/tr/<slug>.md`
2. Add the post to `public/data/posts.en.json` and `public/data/posts.tr.json`
3. Ensure the post `category` exists in `public/data/categories.en.json` and `public/data/categories.tr.json`
4. Create `public/images/<slug>-thumbnail.webp` (1200x630) using the Iram art direction
5. Run the checker: `node .agents/skills/blog-content-authoring/scripts/check-content.mjs`

## Documentation Source (Context7 MCP Required)

When writing technical posts (Java/Kotlin/Spring Boot/Kubernetes/Go), always pull **current** API guidance from **Context7** before finalizing code/config snippets.

Workflow:

1. Resolve the library id:
   - `mcp__context7__resolve-library-id` (example inputs: “spring boot”, “kubernetes”, “go”)
2. Query for the exact topic you’re writing about:
   - `mcp__context7__query-docs` (ask for the _specific feature_, version caveats, and example snippets)
3. Adapt examples to this repo’s constraints:
   - Blog markdown conventions (headings/steps/conclusion)
   - Keep code snippets minimal and production-safe

### 1) Choose the slug/ID

- Use only lowercase letters + digits + hyphens: `spring-boot-ai`
- The file name and the post index `id` must match.

### 2) Create the thumbnail (WebP, 1200x630)

This skill includes a helper script:

```bash
node .agents/skills/blog-content-authoring/scripts/make-thumbnail.mjs \
  --in /path/to/source.png \
  --out public/images/<slug>-thumbnail.webp
```

- Put the output **exactly** under `public/images/...`.
- Reference it in Markdown/post index JSON as: `"/images/<slug>-thumbnail.webp"`.

### 3) Pick topics / add a new topic if needed

- To see existing topics:
  - `public/data/topics.en.json`
  - `public/data/topics.tr.json`
- To see existing categories (post `category` source-of-truth):
  - `public/data/categories.en.json`
  - `public/data/categories.tr.json`
- If you need a new topic, follow “Add a New Topic” below, then use it in the post.
- If you need a new category, add it to both category files first, then use it in the post.

## Add a New Category (Step-by-Step)

When you introduce a new category, it must be added to **both** locale files and then referenced by posts via the `category` field.

1. Pick a stable category `id` (kebab-case), e.g. `gaming`
2. Add it to `public/data/categories.en.json`:
   - `id`: the same id
   - `name`: English display name (e.g. `Gaming`)
   - `color`: pick a UI color variant (same family used by topics/category links)
3. Add it to `public/data/categories.tr.json`:
   - `id`: the same id
   - `name`: Turkish display name (localized or project-preferred label)
   - `color`: **must match** the EN color
4. Use it in both Markdown frontmatter and post index JSON as `category: { id, name }`
5. Keep categories and topics separate (do not also add the category as a topic).

## Add a New Topic (Step-by-Step)

When you introduce a new topic (e.g. `redis`, `kafka`), it must be added to **both** locale files and then used consistently.

1. Pick a stable topic `id` (kebab-case), e.g. `spring-ai`
2. Add it to `public/data/topics.en.json`:
   - `id`: the same id
   - `name`: English display name (e.g. `Spring AI`)
   - `color`: pick from the allowed set (see checker’s `ALLOWED_TOPIC_COLORS`)
3. Add it to `public/data/topics.tr.json`:
   - `id`: the same id
   - `name`: Turkish display name (e.g. `Spring AI` or a localized equivalent)
   - `color`: **must match** the EN color
4. Use the topic in both `public/data/posts.en.json` and `public/data/posts.tr.json` entries (topic object must include `id/name/color`)
   - Do **not** use a category id (e.g. `programming`) as a topic.
5. Re-run the checker:
   - `node .agents/skills/blog-content-authoring/scripts/check-content.mjs`

### 4) Create Markdown files (en + tr)

Create two files:

- `content/posts/en/<slug>.md`
- `content/posts/tr/<slug>.md`

Frontmatter template (example):

```md
---
title: '...'
publishedDate: 'YYYY-MM-DD'
category:
  id: programming
  name: Programming
updatedDate: 'YYYY-MM-DD'
summary: '...'
thumbnail: '/images/<slug>-thumbnail.webp'
readingTime: '3 min read' # Note: computed in the app; optional/ignored as a source of truth
topics:
  - id: 'java'
    name: 'Java'
    color: 'red'
---
```

Notes:

- Keep `summary` short and scannable:
  - Recommended: **140–180 characters**
  - Hard limit: **≤ 200 characters**
- Keep `title` clean and SEO-friendly:
  - Avoid parentheses in titles (e.g. do **not** use “(Type-Safe Config + Profiles)”)
- `publishedDate` format: `YYYY-MM-DD` (e.g. `2026-02-03`)
- `updatedDate` format: `YYYY-MM-DD` and should be on/after `publishedDate`.
- `category` is required and must be an **object** with `id/name` (do not use a plain string category).
- `category.id`/`category.name` must match `public/data/categories.<locale>.json` for the current locale.
- `topics` entries must be **objects** (`id/name/color`). The `id` must exist in topic index JSON.
- Do not include the category as a topic (example: do **not** add `programming` under `topics` when `category.id = programming`).
- `readingTime` is computed automatically; you may keep it for consistency, but it is not a reliable source of truth.
- Content supports GitHub Flavored Markdown (tables/lists/code blocks).
- If you want tabbed blocks:

````md
:::tabs
@tab Maven [icon=maven]

```xml
...
```

@tab Gradle [icon=gradle]

```kts
...
```

:::
````

Constraint:

- The `@tab` title is parsed via a regex; avoid emojis/special characters. Use **letters/numbers/spaces**.

Link rule:

- Write internal links as `/posts/<id>` or `/topics/<id>`; the renderer will add the locale prefix automatically.

### 5) Update post index JSON (en + tr)

Add the new entry (same `id`) to both files:

- `public/data/posts.en.json`
- `public/data/posts.tr.json`

Entry template:

```json
{
  "id": "<slug>",
  "title": "...",
  "publishedDate": "YYYY-MM-DD",
  "updatedDate": "YYYY-MM-DD",
  "category": { "id": "programming", "name": "Programming" },
  "summary": "...",
  "thumbnail": "/images/<slug>-thumbnail.webp",
  "topics": [{ "id": "java", "name": "Java", "color": "red" }],
  "readingTimeMin": 3,
  "searchText": "normalized searchable text",
  "source": "blog"
}
```

Notes:

- `title/summary/topic.name` must be translated per locale (`en` vs `tr`).
- `category.name` must be translated per locale (`en` vs `tr`); `category.id` must remain stable across locales.
- `topics[].id` and `topics[].color` must remain the same across locales.
- Keep `category` separate from `topics`; do not duplicate the category in `topics[]`.
- Sorting is done at runtime by `publishedDate`; still, keeping JSON roughly **newest to oldest** is practical.
- `updatedDate` is used for SEO/RSS/Sitemap freshness (`dateModified`, `lastmod`, `atom:updated`).

### 6) Quick validation

This skill includes a content check script:

```bash
node .agents/skills/blog-content-authoring/scripts/check-content.mjs
```

To see a quick inventory of images referenced by posts:

```bash
node .agents/skills/blog-content-authoring/scripts/report-images.mjs
```

To standardize existing posts (headings/steps/prerequisites), run:

```bash
node .agents/skills/blog-content-authoring/scripts/standardize-posts.mjs --dry-run
node .agents/skills/blog-content-authoring/scripts/standardize-posts.mjs
```

To sync computed metadata (`readingTimeMin`, `searchText`, `updatedDate`) into post index JSON, run:

```bash
pnpm run sync:post-metadata
```

Then run the repo quality gates:

```bash
pnpm test
pnpm run lint
pnpm build
```

## Add a New Topic (Step-by-Step)

1. Choose a new topic `id` (kebab-case): `spring-ai`
2. Add it to both locale files:
   - `public/data/topics.en.json`
   - `public/data/topics.tr.json`
3. Template:

```json
{ "id": "spring-ai", "name": "Spring AI", "color": "orange" }
```

4. `color` must be one of:

`primary, secondary, success, info, warning, danger, light, dark, red, green, blue, orange, yellow, purple, gray, brown, pink, cyan`

5. Then add the same `id/name/color` to:
   - the Markdown frontmatter `topics` list
   - the post index JSON `topics` list
     for the relevant posts.
   - Keep category separate; do not duplicate the post category in `topics`.

## Common Mistakes

- Adding only the Markdown file but not updating post index JSON (the post won’t appear in list/RSS/sitemap).
- Mismatched `id` vs filename (post index `id` != `<slug>.md`).
- Putting the thumbnail outside `public/images/` or referencing it with a path not starting with `/images/...`.
- Adding a topic in only one locale (topic pages/build become inconsistent).
- Adding the post category (e.g. `programming`) into `topics[]` as well (category and topics are separate fields).
- Using emojis/special characters in `@tab` titles (tab parsing may break).
