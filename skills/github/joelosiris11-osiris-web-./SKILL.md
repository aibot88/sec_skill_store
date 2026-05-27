---
name: osiris-web
description: Build cinematic scroll-driven portfolio sites with Apple-style frame-sequence canvas scrubbing. Triggers when the user asks for "a website like Osiris", "cinematic portfolio with video transitions", "scroll-driven storytelling site", or "Apple-AirPods-style page". Uses Vite + Three.js (optional) + GSAP ScrollTrigger + Lenis + a frame-sequence canvas instead of `<video>` to guarantee frame-perfect scrubbing across all browsers.
---

# OSIRIS Web Skill — Cinematic Scroll Portfolio

A reusable recipe for building **scroll-driven cinematic websites** where the hero animation is a scroll-scrubbed sequence of pre-rendered frames (no `<video>` tag, no jitter). Includes auto-scroll with narrative stop points, custom cursor, smooth Lenis scroll, and progressive content reveals.

Reference implementation: <https://github.com/joelosiris11/osiris-web>

---

## 1. When to use this skill

Use this skill when the user wants:

- A portfolio / personal site with a **cinematic intro** that responds to scroll
- A page like **CityPunks**, **Apple AirPods Pro**, or **Lusion / Activetheory** style
- A site with **frame-by-frame scroll scrubbing** of a short video as you go down
- Multiple "acts" that crossfade through tagline UIs (NO RULES → WALK THE EDGE → content)

Do **NOT** use this skill if the user only wants a static portfolio, a CMS-driven site, or has no transition videos to scrub.

---

## 2. Questions to ask the user (BEFORE coding)

Ask these in order with `AskUserQuestion` (or equivalent). Don't guess.

### 2.1 Brand
1. **Brand / logo text** — short word that goes in the top-left (e.g. `OSIRIS`).
2. **Logo mark** — optional single character or kanji (e.g. `機`, `O`, an SVG path).
3. **Person name** — full name for the byline (e.g. `Joel O. Pena`).
4. **Role / overline** — short label for the yellow accent line (e.g. `FULL-STACK ENGINEER · DOMINICAN REPUBLIC · 2026`).
5. **Hero tagline** — 2 lines, big display type (e.g. `NO RULES.` / `NO LIMITS.`).
6. **Hero sub-paragraph** — 1–2 sentences describing what the person builds.
7. **Bridge tagline** — 2 lines for the mid-cinematic moment (e.g. `WALK THE` / `EDGE.`).
8. **Bridge sub-paragraph** — 1–2 sentences for the bridge moment.

### 2.2 Assets the user must provide

For the cinematic to work, the user **must** deliver:

| Asset | Format | Resolution | Notes |
|---|---|---|---|
| Hero/static "act 1" image | PNG/JPG | ≥1920×1080 | The "before scroll" pose. Often = first frame of video 1. |
| Bridge static "act 2" image | PNG/JPG | ≥1920×1080 | The mid-state pose (only used in About portrait, optional) |
| Empty background | PNG/JPG | ≥1920×1080 | The "after cinematic" scene. Used as fixed bg behind content. Often = last frame of video 2. |
| Video 1 (intro→bridge transition) | MP4 (H.264) | ≥1280×720, ≤6 sec | Scrubbed during first half of pin |
| Video 2 (bridge→empty transition) | MP4 (H.264) | ≥1280×720, ≤6 sec | Scrubbed during second half of pin |

Both videos should be **continuous in framing** with the static images: the first frame of video 1 ≈ act 1 image, last frame of video 1 ≈ first frame of video 2 ≈ act 2 image, last frame of video 2 ≈ empty background.

Ask the user:
9. **Where are the assets?** Path on disk (e.g. `~/Desktop/osiris/`).
10. **Watermark to crop?** Most AI video gens (Kling, Sora, Runway) add a bottom-right badge. Ask whether to crop bottom 40–60px.

### 2.3 Sections
11. **Which sections after the cinematic?** (multi-select)
    - About (bio, stats, portrait)
    - Projects (grid of cards)
    - Skills / Stack (columns of tech)
    - Contact (CTA + social links)
    - Custom (user describes)

12. **Project list** — for each project: name, tag/subtitle, description, tech stack, accent color.
13. **Skill columns** — categorized lists (e.g. Backend / Frontend / AI / DevOps).
14. **Contact info** — email, GitHub, social URLs.

### 2.4 Stack / build target
15. **Stack preference** — recommend `Vite + GSAP + Lenis + Three.js (optional)`. Alternatives: Next.js + R3F, plain HTML.
16. **Deploy target** — local only / Cloudflare Pages / Vercel / GitHub Pages.

---

## 3. Asset processing pipeline

### 3.1 Inspect the videos first

```bash
ffprobe -v error -select_streams v -show_entries stream=r_frame_rate,nb_frames,duration,width,height -of default=noprint_wrappers=1 input.mp4
```

Record: **fps**, **frame count**, **duration**, **dimensions**.

### 3.2 Extract frames as JPG sequence

This is the core technique — replace `<video>` with a sequence of preloaded `<img>` frames drawn to `<canvas>`.

```bash
mkdir -p public/assets/frames-1 public/assets/frames-2

# Crop bottom 50px (removes Kling/Sora watermark) + scale to 1280 wide + JPG q=4
ffmpeg -i video1.mp4 \
  -vf "crop=in_w:in_h-50:0:0,scale=1280:-2" \
  -q:v 4 -start_number 1 \
  public/assets/frames-1/f_%03d.jpg -y

ffmpeg -i video2.mp4 \
  -vf "crop=in_w:in_h-50:0:0,scale=1280:-2" \
  -q:v 4 -start_number 1 \
  public/assets/frames-2/f_%03d.jpg -y
```

**Padding** (`%03d`): 3 digits supports up to 999 frames. Adjust if videos are longer (`%04d` for 4 digits).

### 3.3 Sizing math

| Frames per video | Pin scroll length | Frames per viewport scroll | Feel |
|---|---|---|---|
| 60–90 | `+=500%` | ~12–18 frames/vh | Smooth, cinematic |
| 120+ | `+=700%` | ~17 frames/vh | More tactile, longer scroll |
| 30 | `+=300%` | ~10 frames/vh | Snappy, less narrative |

Total memory budget after decode: ~50–100MB for 150 frames at 1280×720 JPG q=4. Acceptable on desktop, marginal on mobile (consider 640×360 fallback).

### 3.4 Static images

Compress with `sips` (macOS) or `cwebp`:
```bash
sips -s format jpeg -s formatOptions 85 fondo.png --out fondo.jpg
# or for high-quality WebP
cwebp -q 85 fondo.png -o fondo.webp
```

---

## 4. Architecture

```
project/
├── public/assets/
│   ├── frames-1/f_001.jpg … f_NNN.jpg   ← extracted from video 1
│   ├── frames-2/f_001.jpg … f_NNN.jpg   ← extracted from video 2
│   ├── osirisA.png   ← hero static (also used for About portrait)
│   ├── osirisB.png   ← bridge static (optional)
│   └── fondo.png     ← empty bg (rarely used; canvas takes over)
├── src/
│   ├── main.js              ← Lenis + boot + scroll-restoration
│   ├── ui/
│   │   ├── cursor.js        ← custom circle cursor (mix-blend-mode: difference)
│   │   └── loader.js        ← preloads ALL frames before unlocking scroll
│   ├── scene/
│   │   └── frames.js        ← SEQUENCES export with HTMLImageElement arrays
│   ├── animations/
│   │   └── scroll.js        ← cinematic pin + UI overlays + auto-scroll
│   └── styles/
│       └── main.css         ← tokens + sections
└── index.html
```

### 4.1 Layered rendering

```
z-index   element                          position
────────  ───────────────────────────────  ─────────
   0      .bg-canvas (fixed, full-screen)  fixed   ← persistent canvas
   1      .bg-overlay (subtle gradient)    fixed
   5      .cinematic, .stage, sections     normal flow
  10      cinematic UI overlays            absolute
  50      [reserved for portals]           —
 100      .nav                             fixed
 500      .loader                          fixed
1000      .cursor                          fixed
```

The **bg-canvas is fixed at root level**, NOT inside the cinematic section. This is critical: it ensures the last frame stays visible behind content sections (no visual seam when pin releases).

---

## 5. Critical code patterns

### 5.1 Frame loader (with progress + decode)

```js
function preloadFrame(src) {
  return new Promise((resolve) => {
    const img = new Image();
    img.decoding = 'async';
    img.onload = () => {
      // decode forces actual pixel decode so first drawImage is instant
      if (typeof img.decode === 'function') {
        img.decode().then(() => resolve(img)).catch(() => resolve(img));
      } else resolve(img);
    };
    img.onerror = () => resolve(img);
    img.src = src;
  });
}
```

### 5.2 Cover-fit canvas drawImage

```js
function render(idx, canvas, ctx, frames) {
  const img = frames[Math.max(0, Math.min(frames.length - 1, idx))];
  if (!img || !img.complete) return;
  const cw = canvas.width, ch = canvas.height;
  const iw = img.naturalWidth, ih = img.naturalHeight;
  const scale = Math.max(cw / iw, ch / ih);
  const dw = iw * scale, dh = ih * scale;
  ctx.fillStyle = '#0a0203';
  ctx.fillRect(0, 0, cw, ch);
  ctx.drawImage(img, (cw - dw) / 2, (ch - dh) / 2, dw, dh);
}

function setSize(canvas) {
  const rect = canvas.getBoundingClientRect();
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  canvas.width  = Math.round(rect.width  * dpr);
  canvas.height = Math.round(rect.height * dpr);
}
```

### 5.3 Pin + scrub + UI overlays

```js
const state = { frame: 0 };
const trigger = ScrollTrigger.create({
  trigger: '#cinematic',
  start: 'top top',
  end: '+=500%',          // ← adjust based on frame count
  pin: true,
  pinSpacing: true,
  scrub: 0.4,             // small scrub buffer for smoothness
  anticipatePin: 1,
  invalidateOnRefresh: true,
  onUpdate: (self) => {
    const p = self.progress;
    const idx = Math.round(p * (totalFrames - 1));
    if (idx !== state.frame) { state.frame = idx; render(idx); }

    // UI overlay opacity windows (calibrate to match your stop points)
    openingUI.style.opacity = fadeWindow(p, 0,    0,    0.08, 0.18);
    bridgeUI.style.opacity  = fadeWindow(p, 0.42, 0.52, 0.60, 0.70);
    scrollhint.style.opacity= fadeWindow(p, 0,    0,    0.005,0.03);
  },
});

function fadeWindow(p, fadeIn0, fadeIn1, fadeOut0, fadeOut1) {
  if (p < fadeIn0) return 0;
  if (p < fadeIn1) return (p - fadeIn0) / Math.max(1e-6, fadeIn1 - fadeIn0);
  if (p < fadeOut0) return 1;
  if (p < fadeOut1) return 1 - (p - fadeOut0) / Math.max(1e-6, fadeOut1 - fadeOut0);
  return 0;
}
```

### 5.4 Auto-scroll with narrative stop points

```js
function setupAutoScroll(lenis, trigger) {
  const IDLE_MS = 1200;
  const STOP_POINTS = [0.56, 1.0]; // bridge moment, then end
  let idleTimer = null, autoActive = false, hasInteracted = false;

  const inRange = () => {
    const p = trigger.progress;
    return p > 0.02 && p < 0.96;
  };

  function getNextStop() {
    const p = trigger.progress;
    for (const s of STOP_POINTS) if (s > p + 0.04) return s;
    return null;
  }

  function triggerAuto() {
    if (!hasInteracted || !inRange()) return;
    const target = getNextStop();
    if (target === null) return;
    autoActive = true;
    const remaining = target - trigger.progress;
    const duration = Math.max(1.6, remaining * 3.5);

    let targetY;
    if (target >= 0.99) {
      // Land on the first content title for a satisfying finish
      const t = document.querySelector('#about .section-title');
      if (t) {
        const r = t.getBoundingClientRect();
        targetY = r.top + window.scrollY - window.innerHeight * 0.22;
      } else {
        targetY = trigger.end + 240;
      }
    } else {
      targetY = trigger.start + (trigger.end - trigger.start) * target;
    }

    lenis.scrollTo(targetY, {
      duration,
      easing: (t) => 1 - Math.pow(1 - t, 2.5),
      onComplete: () => { autoActive = false; },
    });
  }

  function bumpIdle() {
    hasInteracted = true;
    clearTimeout(idleTimer);
    if (autoActive) autoActive = false;
    if (inRange()) idleTimer = setTimeout(triggerAuto, IDLE_MS);
  }

  ['wheel', 'touchmove', 'touchstart'].forEach((e) =>
    window.addEventListener(e, bumpIdle, { passive: true }));
  window.addEventListener('keydown', (e) => {
    const keys = ['PageUp','PageDown','ArrowUp','ArrowDown','Home','End',' ','Spacebar'];
    if (keys.includes(e.key)) bumpIdle();
  });
}
```

**Calibrating stop points:**
- `STOP_POINTS = [bridgeUI midpoint, 1.0]`
- Bridge midpoint = midpoint of bridge UI's full-visibility window. For windows `[0.42, 0.52, 0.60, 0.70]`, midpoint = `(0.52 + 0.60) / 2 = 0.56`.
- For a third stop (e.g. a third tagline), insert before 1.0.

### 5.5 Lenis + ScrollTrigger setup (mandatory)

```js
const lenis = new Lenis({
  duration: 1.1,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
});
lenis.stop(); // start locked, .start() after loader

lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((time) => lenis.raf(time * 1000));
gsap.ticker.lagSmoothing(0);

// Force fresh scroll on every load (prevents browser restoration mid-cinematic)
if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
window.scrollTo(0, 0);
```

### 5.6 Loader with hard scroll lock

```html
<style>
  body.is-locked { overflow: hidden; height: 100vh; }
</style>
```

```js
document.body.classList.add('is-locked');
await initLoader(); // preloads frames + decodes them
document.body.classList.remove('is-locked');
lenis.start();
ScrollTrigger.refresh();
```

---

## 6. Pitfalls (do NOT repeat these mistakes)

### 6.1 Don't use `<video>.currentTime` for scrub
- Browsers throttle `currentTime` updates
- Safari shows black flashes between keyframes
- iOS requires user-gesture unlock that often fails silently
- **Always extract frames** and use canvas drawImage instead

### 6.2 Don't put the canvas inside the cinematic section
- When pin releases, the canvas scrolls away with its parent
- Creates a visible seam where the last frame ends and content bg begins
- **Solution:** put the canvas at root `<body>` level with `position: fixed`. It persists and shows the last frame behind all subsequent sections.

### 6.3 Don't override the user's source backgrounds with synthetic CSS gradients
- If the user provides a hero PNG with red atmospheric bg, **use it directly** as `background-image` or `<img class="act-bg">` with `object-fit: cover`
- Don't paint your own radial gradients on top with `mix-blend-mode: multiply` — it desaturates the source
- Only add a SUBTLE corner-gradient overlay for text legibility (max 50% opacity)

### 6.4 Don't auto-scroll without a hard `hasInteracted` gate
- Browser scroll restoration, Lenis init, or ScrollTrigger refresh can fire fake scroll events on load
- Without a guard, the page starts auto-scrolling before the user touches anything
- **Fix:** track `hasInteracted` and only allow auto-scroll after a real wheel/touch/key event

### 6.5 Don't chain auto-scrolls between stops
- Auto-scroll should fire ONCE per user input, then wait for the next input
- Chaining (auto → dwell → auto → dwell) feels like a hijack
- The user wants to read each UI moment, not be carried through

### 6.6 Don't preload only `loadedmetadata` on videos
- That gives you `duration` but not decoded frame data
- For frame sequences: use `img.decode()` to force decode before the first paint

### 6.7 Don't forget `pointer-events: none` on cursor + overlays
- The custom cursor must NOT block clicks
- The bg overlay must NOT capture mouse events meant for content

---

## 7. Build sequence (recommended order)

1. **Setup** — `pnpm create vite` + `pnpm add three gsap lenis`
2. **Inspect videos** — `ffprobe` to record fps/frames
3. **Extract frames** — ffmpeg to public/assets/frames-{1,2}/
4. **Strip metadata files** — remove `vite.svg`, default counter.js, default style.css
5. **Tokens + reset CSS** — design tokens, fonts via Google Fonts CDN
6. **Loader** — preload frames + 1 static image (fondo)
7. **Persistent canvas** — `<canvas class="bg-canvas">` at root with fixed positioning
8. **Cinematic section** — empty pinned section with UI overlays only
9. **Render function** — cover-fit drawImage based on frame index
10. **Pin + scrub trigger** — `+=500%`, scrub 0.4
11. **UI fade windows** — calibrate fadeWindow() params
12. **Hero entrance timeline** — animate opening UI in on load
13. **Bridge entrance** — fire once when progress crosses bridge threshold
14. **Auto-scroll** — stop points + idle timer + hasInteracted gate
15. **Content sections** — About → Projects → Skills → Contact, all transparent bg
16. **Section reveals** — gsap.fromTo on viewport enter
17. **Counters, project tilt, title word-reveal** — secondary polish
18. **Custom cursor** — circle + difference blend mode
19. **Responsive breakpoints** — mobile fallbacks (lower DPR, fewer frames)
20. **Reduced motion** — bypass timelines, keep static images visible
21. **Test** — local dev server, hard refresh, scroll all the way through

---

## 8. Default visual language (Osiris reference)

Token values that work well together. Override per brand.

```css
:root {
  --bg-deep:        #0a0203;
  --text-primary:   #f4ede4;
  --text-secondary: rgba(244, 237, 228, 0.66);
  --text-muted:     rgba(244, 237, 228, 0.42);
  --red-accent:     #ff3344;
  --accent-yellow:  #f5c518;
  --line:           rgba(244, 237, 228, 0.12);
  --line-strong:    rgba(244, 237, 228, 0.28);

  --font-display: 'Anton', 'Bebas Neue', Impact, sans-serif;
  --font-mono:    'JetBrains Mono', 'SF Mono', Menlo, monospace;
  --font-body:    'Inter', -apple-system, sans-serif;

  --container: min(1480px, 92vw);
  --gutter:    clamp(20px, 4vw, 48px);
}
```

**Backgrounds** — the Osiris reference uses a single red atmospheric `Fondo.png` (1672×941, dark crimson with floor reflection and floating debris) as the empty-state. The cinematic frames inherit this exact framing because they were generated from the same prompt — that's why the seamless transition works.

When asking the user for backgrounds, recommend they use the **last frame of video 2 as the empty bg**. That guarantees pixel-perfect continuity.

---

## 9. Testing checklist

- [ ] Page loads → frame 0 visible immediately (not black)
- [ ] No scroll until loader at 100%
- [ ] First scroll → frames advance smoothly (no jitter, no black flashes)
- [ ] Pin engages — visually section stays put while frames change
- [ ] Bridge UI appears at correct moment (calibrated fade window)
- [ ] Auto-scroll fires only after real user input
- [ ] Auto-scroll stops at bridge UI (doesn't skip to end)
- [ ] Manual scroll during auto cancels it cleanly
- [ ] Pin releases → content section shows fondo bg with no seam
- [ ] About title animation plays when it enters viewport
- [ ] Project cards tilt on hover (desktop only)
- [ ] Custom cursor follows mouse, grows on links
- [ ] Mobile: cursor hidden, tilts disabled, particles minimal
- [ ] `prefers-reduced-motion`: no scrubs, no auto-scroll, static images visible

---

## 10. Quick math reference

For a video of duration **D** seconds at **F** fps:
- Total frames: `N = ceil(D × F)`
- Recommended pin length: `+=(N × 6)%` (e.g. 73 frames → ~440%, round to 500%)
- Frames per viewport scroll: `N / (pin% / 100)` — target 12–18 for cinematic feel
- Memory at 1280×720 q4 JPG: `N × 80KB ≈ ~6MB on disk`, `N × 4MB ≈ ~290MB decoded` (browser optimizes to ~30-50MB in practice)

For two chained sequences (Osiris pattern, 73 + 73 frames):
- Combined N = 146
- Pin length: `+=500%`
- Frames per viewport: ~29 — buttery smooth
- Stop points: bridge moment ~0.56, final 1.0

---

## 11. Deployment notes

**Local only:** `pnpm dev` serves on `:5173`. Build with `pnpm build`, preview with `pnpm preview`.

**Cloudflare Pages:** point at the repo, build command `pnpm build`, output dir `dist`.

**GitHub Pages:** add `base: '/repo-name/'` to `vite.config.js`.

**Performance budget for production:**
- Total page weight (first paint): < 600KB without frames
- Frames: ~6MB total (split across 146 individual JPG requests — HTTP/2 makes this fine)
- Lazy-load anything below the fold

---

## 12. Variations (extending the skill)

- **Three videos (3 acts):** add a third sequence + third stop point. Pin length grows to 700%.
- **Three.js particles overlay:** spawn debris particles in a Three.js scene above the canvas. Be careful — the user may not want them (they often feel like "AI slop").
- **Audio:** sync ambient track to scroll progress with `audio.currentTime = progress * duration`. Same caveats as video — better as a poster + short clip on user gesture.
- **Multi-language:** factor copy into a JSON dictionary, swap on `navigator.language`.
- **CMS-driven:** read project list from a static JSON or a headless CMS. Keep the cinematic hardcoded.
