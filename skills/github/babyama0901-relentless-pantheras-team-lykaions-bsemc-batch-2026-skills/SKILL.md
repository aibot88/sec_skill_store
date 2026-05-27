---
name: digital-college-yearbook
version: 1.0.0
description: >
  Design, build, and refine a web-based digital college yearbook — a
  permanent, interactive, and emotionally resonant record of a graduating
  batch's academic life. Triggers on: "build a digital yearbook", "create
  an online yearbook", "design a batch website", "make an interactive
  yearbook", "college graduation website", "batch memento site",
  "student roster web app", "class of [year] website", or any request to
  produce a scrollable, searchable, shareable yearbook experience on the
  web. Covers all phases: information architecture, visual design, animation
  choreography, student data modeling, photo management, and deployment.
tags: [yearbook, college, batch, graduation, interactive, scroll, GSAP, roster]
license: MIT
---

<!--
  ╔══════════════════════════════════════════════════════════════════════════╗
  ║       DIGITAL COLLEGE YEARBOOK — AGENT SKILL SPECIFICATION              ║
  ║       The complete system for building a batch's permanent record        ║
  ╚══════════════════════════════════════════════════════════════════════════╝

  AGENT BEHAVIOR MANDATE
  ──────────────────────
  A digital yearbook is not a website. It is a time capsule.
  Every decision — color, font, animation timing, section order, photo crop —
  must be made with one question in mind:

      "Will this still feel right when someone opens this ten years from now?"

  The agent must produce work that is:

    ① Timeless    — Design choices that do not date themselves in 2 years
    ② Emotional   — Every scroll triggers memory, pride, or warmth
    ③ Complete    — No section is a placeholder; every feature is implemented
    ④ Performant  — Loads fast even with hundreds of high-res portraits
    ⑤ Preserved   — Static-deployable; no database required; survives decades
    ⑥ Accessible  — Graduates of all abilities can experience it fully

  DO NOT build a generic photo gallery.
  DO NOT produce a portfolio template with student names pasted in.
  BUILD a yearbook — structured like a book, felt like a memory.
-->

---

## 0 — Agent Initialization Protocol

Before generating any code or design output, execute this sequence in order:

```
STEP 1 → CLASSIFY the yearbook scope
         [ ] Single department/program    [ ] Full college/university
         [ ] One graduating batch         [ ] Multi-batch alumni archive

STEP 2 → EXTRACT brief signals
         — Batch name / theme word        (e.g., "Meridian", "Ascendance")
         — Graduation year                (e.g., 2026)
         — School / Department name
         — Estimated student count        (affects data architecture)
         — Existing brand colors / logo   (if none → generate)
         — Primary device of audience     (mobile-first vs. desktop-first)
         — Tone keywords                  (warm, elegant, bold, minimal...)
         — Sections needed                (see § 3 for full menu)
         — Special features requested     (search, audio, print mode...)

STEP 3 → SELECT the Yearbook Aesthetic Archetype (§ 2)

STEP 4 → DESIGN the Information Architecture (§ 3)

STEP 5 → BUILD the Technical Stack (§ 4)

STEP 6 → IMPLEMENT section by section (§ 5–12)

STEP 7 → APPLY the Performance & Refinement pass (§ 13–14)

STEP 8 → OUTPUT the Deployment Checklist (§ 15)
```

If Step 2 signals are incomplete, the agent INFERS from college batch
defaults and logs all assumptions in the Agent Assumptions Log (§ 16).

---

## 1 — What a Digital Yearbook Is (and Is Not)

### 1.1 Definitional Boundaries

```
IS a digital yearbook:                   IS NOT a digital yearbook:
──────────────────────────────────────   ──────────────────────────────────────
A structured, chapter-based narrative    A photo dump / gallery site
A permanent record tied to a year        A general student organization site
An emotionally curated experience        A portfolio or resume site
A searchable student directory           A social media feed
A time-stamped cultural artifact         A CMS-managed blog
Designed to be opened once a year        Designed for daily active use
Static-deployable, link-shareable        Requires login or account
```

### 1.2 The Three Experience Goals

Every feature and design decision must serve at least one of these:

```
GOAL 1 — DISCOVERY
  "I want to find a specific classmate / photo / moment quickly."
  Served by: Search, filtering, alphabetical roster, section nav

GOAL 2 — IMMERSION
  "I want to relive the experience of being in this batch."
  Served by: Scroll animations, music, timeline, quotes, memories

GOAL 3 — PRESERVATION
  "I want this to exist forever and still work in 2040."
  Served by: Static deployment, no auth, progressive enhancement,
             semantic HTML, no proprietary dependencies
```

---

## 2 — Aesthetic Archetype Selection

### 2.1 The Six Yearbook Aesthetics

The agent MUST select exactly ONE primary aesthetic. All design decisions
(color, font, layout, animation style, photo treatment) derive from it.

```
╔══════════════════╦═══════════════════════════════════════════════════════╗
║  ARCHETYPE       ║  FINGERPRINT                                          ║
╠══════════════════╬═══════════════════════════════════════════════════════╣
║                  ║  Clean white space · Serif editorial type             ║
║  EDITORIAL       ║  Large portrait photography · Minimal ornament        ║
║  LUXURY          ║  Gold or copper accent · Think: Vogue meets academia  ║
║                  ║  Best for: medicine, law, architecture batches        ║
╠══════════════════╬═══════════════════════════════════════════════════════╣
║                  ║  Dark background · Glowing accent color               ║
║  CINEMATIC       ║  Full-bleed photography · Dramatic typography         ║
║  DARK            ║  GSAP-heavy scroll · Think: film credits + memorial   ║
║                  ║  Best for: design, arts, engineering batches          ║
╠══════════════════╬═══════════════════════════════════════════════════════╣
║                  ║  Warm paper tones · Serif + handwritten               ║
║  VINTAGE         ║  Sepia-tinted photos · Grain texture overlays         ║
║  NOSTALGIC       ║  Aged borders · Think: analog photography album       ║
║                  ║  Best for: nursing, education, humanities batches     ║
╠══════════════════╬═══════════════════════════════════════════════════════╣
║                  ║  Vivid color blocks · Bold display typography         ║
║  BOLD            ║  Asymmetric layouts · High-energy animations          ║
║  CONTEMPORARY    ║  Grid-breaking design · Think: creative agency annual ║
║                  ║  Best for: marketing, tourism, multimedia batches     ║
╠══════════════════╬═══════════════════════════════════════════════════════╣
║                  ║  Sky blue + warm white · Rounded corners              ║
║  SOFT            ║  Gentle animations · Illustrated accents              ║
║  ACADEMIC        ║  Institutional pride · Think: official commencement   ║
║                  ║  Best for: education, social work, theology batches   ║
╠══════════════════╬═══════════════════════════════════════════════════════╣
║                  ║  Monochrome base + 1 electric accent                  ║
║  MINIMAL         ║  Data-forward type design · Tight grid                ║
║  TYPOGRAPHIC     ║  Photography as pure content · Think: Swiss design    ║
║                  ║  Best for: IT, computer science, mathematics batches  ║
╚══════════════════╩═══════════════════════════════════════════════════════╝
```

### 2.2 Aesthetic → Design Token Quick Map

```
AESTHETIC         PRIMARY BG      TEXT           ACCENT          FONT STYLE
──────────────    ────────────    ───────────    ─────────────   ──────────────────
Editorial Luxury  #FAFAF7         #1A1A18        #B8963E (gold)  Serif display + thin sans
Cinematic Dark    #070810         #F0EFF6        #00E5FF (cyan)  Condensed sans + mono
Vintage Nostalgic #F5EDD8         #2C1F0E        #8B5E3C (sepia) Serif + script accent
Bold Contemporary #F4F2EE         #0D0D0D        #FF3D00 (red)   Black display + clean sans
Soft Academic     #F0F5FF         #1C2B4A        #3B82F6 (blue)  Rounded sans + serif body
Minimal Typo      #FFFFFF         #111111        #6EE7B7 (mint)  Geometric mono + body sans
```

---

## 3 — Information Architecture

### 3.1 The Yearbook Section Menu

Every digital yearbook is assembled from these canonical sections.
The agent marks each as `[REQUIRED]`, `[RECOMMENDED]`, or `[OPTIONAL]`.

```
╔══════════════════════════════════════════════════════════════════════════╗
║  SECTION                     TYPE          PRIORITY    NOTES             ║
╠══════════════════════════════════════════════════════════════════════════╣
║  00 · COVER / LANDING        Full-bleed    REQUIRED    First impression  ║
║  01 · TABLE OF CONTENTS      Interactive   REQUIRED    Chapter nav       ║
║  02 · OPENING MESSAGE        Editorial     REQUIRED    Dean/adviser note ║
║  03 · BATCH THEME & STORY    Narrative     REQUIRED    Year in words     ║
║  04 · STUDENT ROSTER         Interactive   REQUIRED    The core section  ║
║  05 · OFFICERS & LEADERS     Feature       REQUIRED    Org chart style   ║
║  06 · IN MEMORIAM            Editorial     REQUIRED*   If applicable     ║
║  07 · TIMELINE / HIGHLIGHTS  Scroll-story  RECOMMENDED Key events        ║
║  08 · MEMORIES GALLERY       Masonry grid  RECOMMENDED Candid photos     ║
║  09 · SUPERLATIVES           Card grid     RECOMMENDED Batch awards      ║
║  10 · STATISTICS & FACTS     Infographic   RECOMMENDED Batch by numbers  ║
║  11 · FAREWELL MESSAGES      Scrolling     RECOMMENDED Student quotes    ║
║  12 · FACULTY TRIBUTES       Feature cards RECOMMENDED Prof portraits    ║
║  13 · SPONSORS / SUPPORTERS  Logo grid     OPTIONAL    Funding partners  ║
║  14 · CLOSING / COLOPHON     Editorial     REQUIRED    Credits, version  ║
╚══════════════════════════════════════════════════════════════════════════╝

* [REQUIRED] if any deceased classmates. Handle with dignity and care.
```

### 3.2 Narrative Flow — The Emotional Arc

The section order must follow this emotional arc. Do not reorder without reason.

```
ACT I — ARRIVAL (Sections 00–03)
  Purpose: Orient, establish identity, set the emotional tone.
  Feeling: "I'm home. This is us."
  Pacing: Slow, deliberate, cinematic reveals.

ACT II — THE PEOPLE (Sections 04–06)
  Purpose: Center the humans. This is the most-visited section.
  Feeling: Recognition, pride, belonging.
  Pacing: Interactive, browsable, searchable.

ACT III — THE STORY (Sections 07–11)
  Purpose: Narrate the journey. Trigger memories.
  Feeling: Nostalgia, laughter, collective identity.
  Pacing: Varied — timeline is slow; gallery is fast-browsable.

ACT IV — GRATITUDE (Sections 12–13)
  Purpose: Acknowledge those who shaped the journey.
  Feeling: Warmth, respect, closure.
  Pacing: Calm, unhurried.

ACT V — CLOSE (Section 14)
  Purpose: A quiet, final page. The book closes.
  Feeling: Bittersweet completeness.
  Pacing: Very slow, minimal.
```

### 3.3 URL / Route Architecture

```
/                   → Cover / Landing (§ 5)
/toc                → Table of Contents
/message            → Opening Message (§ 6)
/theme              → Batch Theme & Story (§ 7)
/roster             → Student Roster index (§ 8)
/roster/[slug]      → Individual student profile
/officers           → Officers & Leaders (§ 9)
/timeline           → Timeline / Highlights (§ 10)
/gallery            → Memories Gallery (§ 11)
/superlatives       → Superlatives (§ 12)
/stats              → Statistics & Facts (§ 13)
/messages           → Farewell Messages (§ 14)
/faculty            → Faculty Tributes (§ 15)
/colophon           → Closing / Credits

ROUTING STRATEGY:
  Static site (preferred): Hash-based SPA or flat HTML pages
  Dynamic: Next.js with SSG (getStaticPaths per student)
  
  Prefer static generation. A yearbook must work offline, on slow
  connections, and without a server — forever.
```

### 3.4 Student Data Schema

```json
{
  "students": [
    {
      "id": "2026-001",
      "slug": "maria-santos",
      "name": {
        "first": "Maria Celeste",
        "last": "Santos",
        "nickname": "Cel",
        "honorific": null
      },
      "photo": {
        "portrait": "photos/portraits/maria-santos.webp",
        "portrait_2x": "photos/portraits/maria-santos@2x.webp",
        "candid": ["photos/candid/santos-01.webp", "photos/candid/santos-02.webp"]
      },
      "academic": {
        "program": "BS Computer Science",
        "track": "Software Engineering",
        "student_number": "2022-00123",
        "latin_honor": "Cum Laude",
        "awards": ["Best Thesis", "Dean's Lister"]
      },
      "personal": {
        "quote": "The best is yet to come.",
        "quote_source": "F. Scott Fitzgerald",
        "ambition": "Build technology that matters.",
        "favorite_memory": "Late nights at the CS lab",
        "message_to_batch": "Thank you for making every hard day worth it."
      },
      "roles": ["President, ACM Student Chapter", "Lead Developer, Thesis 2026"],
      "socials": {
        "linkedin": "https://linkedin.com/in/mariasantos",
        "github": "https://github.com/celdev"
      },
      "superlatives": ["Most Likely to Become a CTO", "Best Coder"],
      "section": "CS-4A",
      "group_number": 1
    }
  ]
}
```

### 3.5 Site Configuration Schema

```json
{
  "yearbook": {
    "title": "Meridian",
    "subtitle": "Class of 2026",
    "institution": "University of the Philippines Visayas",
    "department": "College of Management",
    "graduation_date": "2026-06-15",
    "theme_statement": "We crossed the meridian together.",
    "color_primary": "#0F3460",
    "color_accent": "#C8A951",
    "font_display": "Cormorant Garamond",
    "font_body": "DM Sans",
    "cover_video": "assets/cover-reel.mp4",
    "cover_image": "assets/cover-still.webp",
    "logo": "assets/batch-logo.svg",
    "school_logo": "assets/school-logo.svg",
    "total_graduates": 187,
    "sections_enabled": [
      "cover", "toc", "message", "theme", "roster",
      "officers", "timeline", "gallery", "superlatives",
      "stats", "messages", "faculty", "colophon"
    ],
    "features": {
      "search": true,
      "audio_ambient": false,
      "print_mode": true,
      "dark_mode_toggle": true,
      "share_card_generation": true
    }
  }
}
```

---

## 4 — Technical Stack Architecture

### 4.1 Stack Decision Tree

```
Is the student count > 300?
  YES → Use a build-time static generator (Next.js SSG, Astro, Eleventy)
  NO  → Can use a single-page vanilla HTML/JS application

Is a CMS / admin panel needed for content updates?
  YES → Headless CMS (Contentful, Sanity) + static generator frontend
  NO  → JSON-file-driven static build (preferred for permanence)

Will the yearbook be self-hosted (shared hosting)?
  YES → Must be pure static output (HTML + CSS + JS only)
  NO  → Can use Vercel / Netlify with serverless functions if needed

Is the development team one person?
  YES → Vanilla HTML + CSS + JS + GSAP (no build step required)
  NO  → Vite + vanilla JS modules OR Next.js static export
```

### 4.2 Recommended Stack (Greenfield, 50–300 students)

```
LAYER           TECHNOLOGY              RATIONALE
─────────────   ──────────────────────  ──────────────────────────────────────
Structure       Semantic HTML5          Permanent, browser-agnostic
Styling         Vanilla CSS + Tokens    No dependency, fully portable
Animation       GSAP 3 + ScrollTrigger  Industry standard; CDN-available
Data            JSON flat files         No database; editable by non-devs
Build           None (or Vite)          Zero build = zero future breakage
Fonts           Google Fonts (self-host preferred)
Images          WebP with JPEG fallback + native lazy loading
Icons           Phosphor Icons (CDN) or SVG inline
Hosting         GitHub Pages / Netlify  Free forever; git-versioned
Search          Fuse.js (fuzzy search)  Lightweight, no server needed
```

### 4.3 CDN Dependencies (Pin Versions — Critical for Longevity)

```html
<!-- In <head> — load order matters -->

<!-- Fonts: Self-host if possible, else preconnect -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@400;500;600&display=swap">

<!-- GSAP Core (ALWAYS pin to specific version) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"
        integrity="sha512-[SRI_HASH]" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"
        integrity="sha512-[SRI_HASH]" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollToPlugin.min.js"
        crossorigin="anonymous"></script>

<!-- Fuse.js for search (pin version) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/fuse.js/7.0.0/fuse.min.js"
        crossorigin="anonymous"></script>

<!-- CRITICAL: Always include local fallback copies in /vendor/ -->
<!-- If CDN fails in 2040, local copies still work -->
```

### 4.4 Project File Structure

```
/yearbook-[batch-name]-[year]/
│
├── index.html                      ← Cover / Landing
├── toc.html                        ← Table of Contents
├── message.html                    ← Opening Message
├── theme.html                      ← Batch Theme
├── roster.html                     ← Roster Index
├── roster/
│   └── [slug].html                 ← Individual profile pages (generated)
├── officers.html
├── timeline.html
├── gallery.html
├── superlatives.html
├── stats.html
├── messages.html
├── faculty.html
├── colophon.html
│
├── assets/
│   ├── css/
│   │   ├── tokens.css              ← Design tokens (variables only)
│   │   ├── reset.css               ← CSS reset
│   │   ├── base.css                ← Typography, body, global elements
│   │   ├── layout.css              ← Grid, containers, responsive
│   │   ├── components.css          ← Cards, nav, modals, badges
│   │   ├── animations.css          ← CSS-only animation declarations
│   │   └── print.css               ← @media print overrides
│   │
│   ├── js/
│   │   ├── main.js                 ← Init, nav, global interactions
│   │   ├── roster.js               ← Roster scroll + search logic
│   │   ├── gallery.js              ← Gallery lightbox + masonry
│   │   ├── timeline.js             ← Timeline scroll narrative
│   │   ├── superlatives.js         ← Superlatives card interactions
│   │   ├── stats.js                ← Animated counters + charts
│   │   ├── search.js               ← Fuse.js search implementation
│   │   └── utils.js                ← Shared helpers (debounce, etc.)
│   │
│   ├── fonts/                      ← Self-hosted font files (.woff2)
│   │
│   ├── icons/                      ← SVG icon sprites
│   │
│   └── vendor/                     ← Local copies of all CDN libraries
│                                     (critical for long-term preservation)
│
├── data/
│   ├── students.json               ← Master student data
│   ├── officers.json               ← Leadership roster
│   ├── faculty.json                ← Faculty profiles
│   ├── timeline.json               ← Events & milestones
│   ├── gallery.json                ← Photo metadata
│   ├── superlatives.json           ← Awards data
│   ├── messages.json               ← Farewell messages
│   └── config.json                 ← Site-wide configuration
│
└── photos/
    ├── portraits/                  ← [slug].webp + [slug]@2x.webp
    ├── candid/                     ← candid-[n].webp
    ├── events/                     ← [event-slug]-[n].webp
    ├── cover/                      ← cover.webp, cover-mobile.webp
    └── faculty/                    ← [slug].webp
```

---

## 5 — Section 00: Cover / Landing Page

### 5.1 Design Specification

```
PURPOSE:       The emotional hook. Sets the entire yearbook's tone.
               Must stop the viewer within 3 seconds.

LAYOUT:        Full-bleed. No scrollbar visible on load.
               Content is vertically and horizontally centered.

LAYERS (back to front):
  Layer 1:  Cover image or video (full viewport, object-fit: cover)
  Layer 2:  Gradient overlay (darkens image without losing texture)
  Layer 3:  Batch theme word (hero typography — the largest type on the site)
  Layer 4:  Subtitle (graduation year + institution)
  Layer 5:  Scroll indicator (animated arrow or "Scroll to begin")
  Layer 6:  Navigation (minimal top bar, fades in after 1.5s delay)

COVER IMAGE REQUIREMENTS:
  — Group photo preferred (batch identity, not individual)
  — Must work with text overlay (avoid bright, flat images)
  — Mobile crop: center-focused (heads must be visible at 390px wide)
  — WebP, 1920×1080px (desktop), 828×1792px (mobile portrait)
  — Use <picture> for art-direction responsive serving
```

### 5.2 HTML Structure

```html
<!DOCTYPE html>
<html lang="en" data-theme="dark" data-aesthetic="cinematic">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="[Batch Name] — [Year] · [Institution]">

  <!-- Open Graph (for link sharing — every graduate will share this) -->
  <meta property="og:title"       content="[Batch Name] — Class of [Year]">
  <meta property="og:description" content="[Theme Statement]">
  <meta property="og:image"       content="photos/cover/og-cover.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height"content="630">
  <meta property="og:type"        content="website">
  <meta name="twitter:card"       content="summary_large_image">

  <title>[Batch Name] · Class of [Year] · [Institution]</title>
  <link rel="icon" href="assets/icons/favicon.ico">
  <link rel="apple-touch-icon" href="assets/icons/apple-touch-icon.png">
  <link rel="stylesheet" href="assets/css/tokens.css">
  <link rel="stylesheet" href="assets/css/reset.css">
  <link rel="stylesheet" href="assets/css/base.css">
  <link rel="stylesheet" href="assets/css/layout.css">
  <link rel="stylesheet" href="assets/css/components.css">
  <link rel="stylesheet" href="assets/css/animations.css">
</head>
<body class="page-cover">

  <!-- ── Navigation ─────────────────────────────── -->
  <nav class="site-nav site-nav--transparent" aria-label="Main navigation"
       id="site-nav">
    <a href="/" class="site-nav__logo" aria-label="Home">
      <img src="assets/batch-logo.svg" alt="[Batch Name] Logo" width="40" height="40">
    </a>
    <button class="site-nav__menu-btn" aria-label="Open navigation menu"
            aria-expanded="false" aria-controls="nav-drawer">
      <span class="sr-only">Menu</span>
      <span class="hamburger-line"></span>
      <span class="hamburger-line"></span>
    </button>
  </nav>

  <!-- ── Full-screen Drawer Nav ─────────────────── -->
  <div class="nav-drawer" id="nav-drawer" role="dialog" aria-modal="true"
       aria-label="Navigation menu" hidden>
    <button class="nav-drawer__close" aria-label="Close menu">×</button>
    <nav aria-label="Site chapters">
      <ol class="nav-drawer__list" role="list">
        <li><a href="toc.html"          class="nav-drawer__link">Table of Contents</a></li>
        <li><a href="message.html"      class="nav-drawer__link">Opening Message</a></li>
        <li><a href="theme.html"        class="nav-drawer__link">Batch Theme</a></li>
        <li><a href="roster.html"       class="nav-drawer__link">Student Roster</a></li>
        <li><a href="officers.html"     class="nav-drawer__link">Officers</a></li>
        <li><a href="timeline.html"     class="nav-drawer__link">Timeline</a></li>
        <li><a href="gallery.html"      class="nav-drawer__link">Gallery</a></li>
        <li><a href="superlatives.html" class="nav-drawer__link">Superlatives</a></li>
        <li><a href="messages.html"     class="nav-drawer__link">Messages</a></li>
        <li><a href="faculty.html"      class="nav-drawer__link">Faculty</a></li>
      </ol>
    </nav>
  </div>
  <div class="nav-drawer__backdrop" aria-hidden="true"></div>

  <!-- ── Cover Hero ─────────────────────────────── -->
  <main class="cover-hero" id="main-content">

    <!-- Background: video with image fallback -->
    <div class="cover-hero__media" aria-hidden="true">
      <picture>
        <source media="(max-width: 768px)"
                srcset="photos/cover/cover-mobile.webp" type="image/webp">
        <source srcset="photos/cover/cover.webp" type="image/webp">
        <img src="photos/cover/cover.jpg"
             alt="" role="presentation"
             width="1920" height="1080"
             loading="eager" fetchpriority="high">
      </picture>
      <!-- Optional: loop video for ambience -->
      <!-- <video autoplay loop muted playsinline poster="photos/cover/cover.jpg">
             <source src="assets/cover-reel.mp4" type="video/mp4">
           </video> -->
    </div>

    <!-- Overlay gradient -->
    <div class="cover-hero__overlay" aria-hidden="true"></div>

    <!-- Content -->
    <div class="cover-hero__content">
      <p class="cover-hero__eyebrow" data-animate="fade-up" data-delay="0.2">
        <span>[Institution]</span>
        <span class="separator" aria-hidden="true">·</span>
        <span>[Department]</span>
      </p>

      <h1 class="cover-hero__title" data-animate="split-reveal" data-delay="0.5">
        [BATCH THEME WORD]
      </h1>

      <p class="cover-hero__subtitle" data-animate="fade-up" data-delay="0.9">
        Class of [Year]
      </p>

      <p class="cover-hero__theme" data-animate="fade-up" data-delay="1.1">
        "[Theme Statement]"
      </p>
    </div>

    <!-- Scroll indicator -->
    <div class="cover-hero__scroll-cue" aria-hidden="true">
      <span class="scroll-cue__label">Scroll to begin</span>
      <div class="scroll-cue__line"></div>
    </div>

  </main>

  <script src="assets/vendor/gsap.min.js"></script>
  <script src="assets/vendor/ScrollTrigger.min.js"></script>
  <script src="assets/js/main.js" type="module"></script>
</body>
</html>
```

### 5.3 Cover CSS

```css
/* ── Cover Hero Layout ───────────────────────── */
.cover-hero {
  position: relative;
  width: 100%;
  height: 100dvh;           /* dvh = accounts for mobile address bar */
  min-height: 600px;
  display: grid;
  place-items: center;
  overflow: hidden;
}

/* ── Media Layer ─────────────────────────────── */
.cover-hero__media {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.cover-hero__media img,
.cover-hero__media video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 30%;  /* Prioritize faces */
}

/* ── Gradient Overlay ────────────────────────── */
.cover-hero__overlay {
  position: absolute;
  inset: 0;
  z-index: 1;
  background:
    linear-gradient(
      to bottom,
      rgba(0,0,0,0.1) 0%,
      rgba(0,0,0,0.3) 40%,
      rgba(0,0,0,0.7) 75%,
      rgba(0,0,0,0.9) 100%
    );
}

/* ── Content Layer ───────────────────────────── */
.cover-hero__content {
  position: relative;
  z-index: 2;
  text-align: center;
  padding: 0 var(--space-6);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-4);
}

.cover-hero__eyebrow {
  font-family: var(--font-accent);
  font-size: var(--text-xs);
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.6);
  display: flex;
  gap: var(--space-3);
  align-items: center;
  opacity: 0;  /* GSAP will animate in */
}

.cover-hero__title {
  font-family: var(--font-display);
  font-size: clamp(4rem, 15vw, 10rem);
  font-weight: 600;
  line-height: 0.9;
  letter-spacing: -0.03em;
  color: var(--clr-text-primary);
  opacity: 0;  /* GSAP will animate in */
}

.cover-hero__subtitle {
  font-family: var(--font-body);
  font-size: var(--text-lg);
  font-weight: 400;
  color: rgba(255,255,255,0.8);
  opacity: 0;
}

.cover-hero__theme {
  font-family: var(--font-display);
  font-style: italic;
  font-size: var(--text-base);
  color: var(--clr-accent);
  opacity: 0;
}

/* ── Scroll Cue ──────────────────────────────── */
.cover-hero__scroll-cue {
  position: absolute;
  bottom: var(--space-8);
  left: 50%;
  transform: translateX(-50%);
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
}

.scroll-cue__label {
  font-family: var(--font-accent);
  font-size: var(--text-xs);
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.4);
}

.scroll-cue__line {
  width: 1px;
  height: 48px;
  background: linear-gradient(to bottom, var(--clr-accent), transparent);
  animation: scroll-cue-pulse 2s ease-in-out infinite;
}

@keyframes scroll-cue-pulse {
  0%, 100% { opacity: 0.3; transform: scaleY(1); }
  50%       { opacity: 1;   transform: scaleY(1.15); }
}
```

### 5.4 Cover Animation (GSAP)

```js
// cover-animation.js
import { gsap } from 'gsap';

export function initCoverAnimation() {
  // Respect reduced motion preference
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (prefersReduced) {
    // Simple instant reveal
    document.querySelectorAll('[data-animate]').forEach(el => {
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
    return;
  }

  const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });

  // Phase 1: Image scale up (Ken Burns on load)
  tl.from('.cover-hero__media img', {
    scale: 1.08,
    duration: 2.5,
    ease: 'power2.out',
  }, 0);

  // Phase 2: Eyebrow
  tl.to('.cover-hero__eyebrow', {
    opacity: 1,
    y: 0,
    duration: 0.7,
  }, 0.3);

  // Phase 3: Title — character-by-character reveal
  const titleEl = document.querySelector('.cover-hero__title');
  if (titleEl) {
    // Split into characters manually (no SplitText plugin needed)
    const text = titleEl.textContent.trim();
    titleEl.innerHTML = text
      .split('')
      .map(ch => ch === ' '
        ? '<span class="char char--space"> </span>'
        : `<span class="char" aria-hidden="true">${ch}</span>`)
      .join('');
    titleEl.setAttribute('aria-label', text); // screen reader gets the full word

    tl.from('.cover-hero__title .char', {
      opacity: 0,
      y: 40,
      rotateX: -60,
      transformOrigin: 'top center',
      duration: 0.6,
      stagger: 0.04,
    }, 0.6);

    tl.to('.cover-hero__title', { opacity: 1, duration: 0 }, 0.6);
  }

  // Phase 4: Subtitle + theme
  tl.to(['.cover-hero__subtitle', '.cover-hero__theme'], {
    opacity: 1,
    y: 0,
    duration: 0.6,
    stagger: 0.15,
  }, 1.2);

  // Phase 5: Scroll cue (delayed entrance)
  tl.from('.cover-hero__scroll-cue', {
    opacity: 0,
    y: 10,
    duration: 0.8,
  }, 2.0);

  // Nav fades in independently
  gsap.to('.site-nav', {
    opacity: 1,
    duration: 0.6,
    delay: 1.5,
  });
}
```

---

## 6 — Section 04: Student Roster (Core Section)

### 6.1 Roster Architecture

The roster is the most critical and most-visited section. It must support:

```
FEATURE                  IMPLEMENTATION
──────────────────────   ──────────────────────────────────────────────
Split-text scroll reveal GSAP ScrollTrigger (horizontal split, desktop)
                         Vertical stack (mobile — NO horizontal split)
Background crossfade     A/B layer swap with GSAP opacity tween
Portrait expansion       CSS width/height transition from 0 to full
Fuzzy search             Fuse.js on name, nickname, program, section
Filter by program        JavaScript array filter, instant re-render
Filter by section        Same filter mechanism
Alphabetical sort        Default; secondary sort by program
Individual profile page  Static HTML per student OR JS modal
Virtual scroll           Required for batches > 100 students
Keyboard navigation      Arrow keys cycle through students
```

### 6.2 Roster Layout Variants

```
VARIANT A — CINEMATIC SCROLL (Default for ≤ 200 students)
  One student fills the full viewport at a time.
  Scrolling triggers the next student's reveal.
  Background crossfades to blurred portrait.
  Name splits left/right. Portrait expands in center gap.
  [See full implementation: § 6.3–6.5]

VARIANT B — MAGAZINE GRID (For > 200 students or "browse" preference)
  4-column desktop / 2-column mobile photo grid.
  On hover: portrait lifts, name overlays.
  On click: student profile modal or page.
  Filter/search bar at top, sticky.

VARIANT C — HYBRID
  Cinematic scroll for officers/honor students.
  Magazine grid for the full class.
  Toggle between views with animated transition.
```

### 6.3 Roster HTML

```html
<section class="roster-section" id="roster" aria-label="Student Roster">

  <!-- Search & Filter Bar (sticky) -->
  <div class="roster-controls" role="search" aria-label="Search students">
    <div class="search-field">
      <label for="roster-search" class="sr-only">Search students</label>
      <input type="search" id="roster-search"
             placeholder="Search by name, nickname, program..."
             autocomplete="off" spellcheck="false"
             aria-controls="roster-results"
             aria-describedby="search-hint">
      <span id="search-hint" class="sr-only">
        Results update as you type
      </span>
    </div>
    <div class="filter-group" role="group" aria-label="Filter by program">
      <button class="filter-btn is-active" data-filter="all">All</button>
      <!-- Generated dynamically from data -->
    </div>
    <p class="roster-count" aria-live="polite" aria-atomic="true">
      Showing <span id="visible-count">187</span> graduates
    </p>
  </div>

  <!-- Roster Wrapper (creates scroll height) -->
  <div class="roster-wrapper" id="roster-wrapper"
       aria-label="Student roster, scroll to browse">

    <!-- Background crossfade layers -->
    <div class="bg-layer bg-layer--a is-active" aria-hidden="true"
         role="presentation"></div>
    <div class="bg-layer bg-layer--b" aria-hidden="true"
         role="presentation"></div>

    <!-- Progress indicator -->
    <div class="roster-progress" aria-hidden="true">
      <div class="roster-progress__bar"></div>
      <span class="roster-progress__counter">
        <span id="current-student">1</span> / <span id="total-students">187</span>
      </span>
    </div>

    <!-- Sticky viewport -->
    <div class="roster-sticky" id="roster-sticky">
      <div class="roster-list" id="roster-list"
           role="list" aria-label="Graduate profiles">
        <!-- Populated by roster.js from students.json -->
      </div>
    </div>

  </div>

  <!-- Keyboard navigation hint -->
  <div class="keyboard-hint" aria-hidden="true">
    <kbd>↑</kbd><kbd>↓</kbd> to navigate
  </div>

</section>
```

### 6.4 Roster CSS

```css
/* ── Controls ────────────────────────────────── */
.roster-controls {
  position: sticky;
  top: var(--nav-height);
  z-index: 50;
  background: rgba(var(--clr-bg-rgb), 0.92);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: var(--space-4) var(--space-6);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-3);
  border-bottom: 1px solid var(--clr-border);
}

.search-field {
  flex: 1;
  min-width: 200px;
  position: relative;
}

.search-field input {
  width: 100%;
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-full);
  padding: var(--space-2) var(--space-4);
  color: var(--clr-text-primary);
  font-size: var(--text-sm);
  transition: border-color var(--duration-fast);
}

.search-field input:focus {
  outline: none;
  border-color: var(--clr-accent);
}

/* ── Roster Wrapper (scroll container) ────────── */
.roster-wrapper {
  position: relative;
  /* Height set by JS: students.length × window.innerHeight */
}

/* ── Sticky Viewport ─────────────────────────── */
.roster-sticky {
  position: sticky;
  top: calc(var(--nav-height) + var(--controls-height, 72px));
  height: calc(100dvh - var(--nav-height) - var(--controls-height, 72px));
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ── Individual Student Item ─────────────────── */
.roster-item {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(var(--space-6), 4vw, var(--space-16));
  padding: 0 clamp(var(--space-6), 6vw, var(--space-24));
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.5s var(--ease-out-quart);
}

.roster-item.is-active {
  opacity: 1;
  pointer-events: auto;
}

/* ── Student Name ────────────────────────────── */
.roster-item__name {
  font-family: var(--font-display);
  font-size: clamp(2rem, 8vw, 7rem);
  font-weight: 600;
  line-height: 1;
  letter-spacing: -0.025em;
  color: var(--clr-text-primary);
  transition: transform 0.6s var(--ease-out-quart),
              opacity 0.4s ease;
  white-space: nowrap;
  flex: 1;
}

.roster-item__name--first {
  text-align: right;
  transform: translateX(0);
}

.roster-item__name--last {
  text-align: left;
  transform: translateX(0);
}

/* Active state: names split apart */
@media (min-width: 769px) {
  .roster-item.is-active .roster-item__name--first {
    transform: translateX(clamp(-2rem, -3vw, -4rem));
  }
  .roster-item.is-active .roster-item__name--last {
    transform: translateX(clamp(2rem, 3vw, 4rem));
  }
}

/* ── Portrait Container ──────────────────────── */
.roster-item__portrait-wrap {
  flex-shrink: 0;
  overflow: hidden;
  border-radius: var(--radius-lg);
  width: 0;
  height: 0;
  transition: width 0.6s var(--ease-out-quart),
              height 0.6s var(--ease-out-quart);
  position: relative;
}

.roster-item.is-active .roster-item__portrait-wrap {
  width:  clamp(100px, 16vw, 240px);
  height: clamp(130px, 20vw, 300px);
}

.roster-item__portrait-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top; /* Prioritize faces */
  display: block;
}

/* ── Info Overlay on Portrait ────────────────── */
.roster-item__info-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: var(--space-3);
  background: linear-gradient(transparent, rgba(0,0,0,0.8));
  color: white;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.roster-item.is-active:hover .roster-item__info-overlay,
.roster-item.is-active:focus-within .roster-item__info-overlay {
  opacity: 1;
}

.roster-item__program {
  font-size: var(--text-xs);
  font-family: var(--font-accent);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  opacity: 0.7;
}

.roster-item__honor {
  font-size: var(--text-xs);
  color: var(--clr-accent);
  font-weight: 600;
}

/* ── Background Layers ───────────────────────── */
.bg-layer {
  position: fixed;
  inset: 0;
  background-size: cover;
  background-position: center top;
  filter: blur(28px) brightness(0.3) saturate(1.4);
  transform: scale(1.12);   /* Prevents blur edge artifacts */
  opacity: 0;
  z-index: -1;
  transition: opacity 0.9s var(--ease-out-quart);
  will-change: opacity;
}
.bg-layer.is-active { opacity: 1; }

/* ── Progress Indicator ──────────────────────── */
.roster-progress {
  position: fixed;
  right: var(--space-6);
  top: 50%;
  transform: translateY(-50%);
  z-index: 30;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
}

.roster-progress__bar {
  width: 2px;
  height: 120px;
  background: var(--clr-border);
  border-radius: var(--radius-full);
  position: relative;
  overflow: hidden;
}

.roster-progress__bar::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  background: var(--clr-accent);
  border-radius: inherit;
  height: var(--progress, 0%);
  transition: height 0.3s ease;
}

.roster-progress__counter {
  font-family: var(--font-accent);
  font-size: 0.6rem;
  letter-spacing: 0.1em;
  color: var(--clr-text-secondary);
  writing-mode: vertical-rl;
}

/* ── MOBILE OVERRIDE — Vertical stack ────────── */
@media (max-width: 768px) {
  .roster-item {
    flex-direction: column;
    text-align: center;
    padding: var(--space-6);
    gap: var(--space-3);
    overflow: hidden;  /* NO horizontal overflow ever */
  }

  .roster-item__name {
    white-space: normal;     /* Allow wrapping on small screens */
    word-break: break-word;
    flex: unset;
    width: 100%;
    font-size: clamp(2rem, 10vw, 3.5rem);
  }

  /* Hard override: no horizontal transform on mobile */
  .roster-item.is-active .roster-item__name--first,
  .roster-item.is-active .roster-item__name--last {
    transform: none !important;
    text-align: center !important;
  }

  /* Vertical order: First Name → Portrait → Last Name */
  .roster-item__name--first    { order: 1; }
  .roster-item__portrait-wrap  { order: 2; }
  .roster-item__name--last     { order: 3; }

  .roster-item.is-active .roster-item__portrait-wrap {
    width:  clamp(90px, 35vw, 150px);
    height: clamp(110px, 44vw, 190px);
  }

  /* Hide progress indicator on mobile */
  .roster-progress { display: none; }
}
```

### 6.5 Roster JavaScript

```js
// roster.js — Complete implementation
import { gsap } from '../vendor/gsap.min.js';
import { ScrollTrigger } from '../vendor/ScrollTrigger.min.js';

gsap.registerPlugin(ScrollTrigger);

// ── Configuration ─────────────────────────────────────────────────────
const SCROLL_PER_STUDENT = window.innerHeight;
const VIRTUAL_BUFFER     = 5;   // render this many students before/after visible

// ── State ─────────────────────────────────────────────────────────────
let students        = [];        // Loaded from students.json
let filteredStudents = [];       // Current filtered/searched set
let activeIndex     = 0;
let renderedItems   = new Map(); // index → DOM element
let bgActive        = 'a';

// ── DOM References ────────────────────────────────────────────────────
const wrapper      = document.getElementById('roster-wrapper');
const stickyPane   = document.getElementById('roster-sticky');
const list         = document.getElementById('roster-list');
const bgA          = document.querySelector('.bg-layer--a');
const bgB          = document.querySelector('.bg-layer--b');
const searchInput  = document.getElementById('roster-search');
const countEl      = document.getElementById('visible-count');
const currentEl    = document.getElementById('current-student');
const totalEl      = document.getElementById('total-students');
const progressBar  = document.querySelector('.roster-progress__bar');

// ── Data Loading ──────────────────────────────────────────────────────
async function loadStudents() {
  const res = await fetch('/data/students.json');
  const data = await res.json();
  students = data.students.sort((a, b) =>
    a.name.last.localeCompare(b.name.last)
  );
  filteredStudents = [...students];
  return students;
}

// ── DOM Builder ───────────────────────────────────────────────────────
function buildItem(student, index) {
  const item = document.createElement('article');
  item.className    = 'roster-item';
  item.dataset.index = index;
  item.setAttribute('role', 'listitem');
  item.setAttribute('aria-label',
    `${student.name.first} ${student.name.last}, ${student.academic.program}`);

  item.innerHTML = `
    <span class="roster-item__name roster-item__name--first"
          aria-hidden="true">${student.name.first}</span>

    <div class="roster-item__portrait-wrap">
      <img
        src="${student.photo.portrait}"
        srcset="${student.photo.portrait} 1x, ${student.photo.portrait_2x} 2x"
        alt="${student.name.first} ${student.name.last}"
        width="240" height="300"
        loading="${index <= 2 ? 'eager' : 'lazy'}"
        decoding="async"
      >
      <div class="roster-item__info-overlay">
        <p class="roster-item__program">${student.academic.program}</p>
        ${student.academic.latin_honor
          ? `<p class="roster-item__honor">${student.academic.latin_honor}</p>`
          : ''}
      </div>
    </div>

    <span class="roster-item__name roster-item__name--last"
          aria-hidden="true">${student.name.last}</span>
  `;

  // Profile link — click portrait to view full profile
  item.querySelector('.roster-item__portrait-wrap').addEventListener('click', () => {
    window.location.href = `/roster/${student.slug}.html`;
  });

  return item;
}

// ── Virtual Render ────────────────────────────────────────────────────
function renderVisible(centerIndex) {
  const start = Math.max(0, centerIndex - VIRTUAL_BUFFER);
  const end   = Math.min(filteredStudents.length - 1, centerIndex + VIRTUAL_BUFFER);

  // Remove items outside buffer
  for (const [idx, el] of renderedItems) {
    if (idx < start || idx > end) {
      el.remove();
      renderedItems.delete(idx);
    }
  }

  // Add items inside buffer
  for (let i = start; i <= end; i++) {
    if (!renderedItems.has(i)) {
      const el = buildItem(filteredStudents[i], i);
      list.appendChild(el);
      renderedItems.set(i, el);
    }
  }
}

// ── Background Crossfade ──────────────────────────────────────────────
function crossfadeTo(imageUrl) {
  const next    = bgActive === 'a' ? bgB : bgA;
  const current = bgActive === 'a' ? bgA : bgB;
  next.style.backgroundImage = `url(${imageUrl})`;

  gsap.to(current, { opacity: 0, duration: 0.9, ease: 'power2.inOut' });
  gsap.to(next,    { opacity: 1, duration: 0.9, ease: 'power2.inOut' });

  current.classList.remove('is-active');
  next.classList.add('is-active');
  bgActive = bgActive === 'a' ? 'b' : 'a';
}

// ── Activate Student ──────────────────────────────────────────────────
function activateStudent(index) {
  if (index === activeIndex && renderedItems.has(index)) return;

  // Deactivate current
  const currentEl = renderedItems.get(activeIndex);
  if (currentEl) currentEl.classList.remove('is-active');

  activeIndex = index;
  renderVisible(index);

  // Activate new
  const newEl = renderedItems.get(index);
  if (newEl) newEl.classList.add('is-active');

  // Crossfade background
  const student = filteredStudents[index];
  if (student) crossfadeTo(student.photo.portrait);

  // Update progress UI
  updateProgress(index);
}

function updateProgress(index) {
  const total    = filteredStudents.length;
  const progress = total > 1 ? (index / (total - 1)) * 100 : 0;

  if (progressBar) {
    progressBar.style.setProperty('--progress', `${progress}%`);
  }
  if (currentEl) currentEl.textContent = index + 1;
}

// ── Scroll Trigger ────────────────────────────────────────────────────
let scrollTriggerInstance = null;

function initScrollTrigger() {
  if (scrollTriggerInstance) {
    scrollTriggerInstance.kill();
  }

  wrapper.style.height =
    `${filteredStudents.length * SCROLL_PER_STUDENT + window.innerHeight}px`;

  scrollTriggerInstance = ScrollTrigger.create({
    trigger: wrapper,
    start:   'top top',
    end:     'bottom bottom',
    onUpdate: self => {
      const index = Math.min(
        filteredStudents.length - 1,
        Math.max(0, Math.floor(self.progress * filteredStudents.length))
      );
      activateStudent(index);
    },
    onEnter: () => activateStudent(0),
  });

  activateStudent(0);
}

// ── Search ────────────────────────────────────────────────────────────
function initSearch() {
  const fuse = new Fuse(students, {
    keys: ['name.first', 'name.last', 'name.nickname',
           'academic.program', 'academic.section'],
    threshold: 0.35,
    includeScore: true,
  });

  searchInput?.addEventListener('input', debounce(e => {
    const query = e.target.value.trim();

    if (!query) {
      filteredStudents = [...students];
    } else {
      filteredStudents = fuse.search(query).map(r => r.item);
    }

    if (countEl)  countEl.textContent  = filteredStudents.length;
    if (totalEl)  totalEl.textContent  = filteredStudents.length;

    renderedItems.forEach(el => el.remove());
    renderedItems.clear();
    initScrollTrigger();
    window.scrollTo({ top: wrapper.offsetTop, behavior: 'smooth' });
  }, 300));
}

// ── Keyboard Navigation ───────────────────────────────────────────────
function initKeyboardNav() {
  document.addEventListener('keydown', e => {
    // Only when roster is in viewport
    const rect = wrapper.getBoundingClientRect();
    const inView = rect.top < window.innerHeight && rect.bottom > 0;
    if (!inView) return;

    if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
      e.preventDefault();
      const nextIndex = Math.min(filteredStudents.length - 1, activeIndex + 1);
      const targetScroll = wrapper.offsetTop + nextIndex * SCROLL_PER_STUDENT;
      window.scrollTo({ top: targetScroll, behavior: 'smooth' });
    }

    if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
      e.preventDefault();
      const prevIndex = Math.max(0, activeIndex - 1);
      const targetScroll = wrapper.offsetTop + prevIndex * SCROLL_PER_STUDENT;
      window.scrollTo({ top: targetScroll, behavior: 'smooth' });
    }
  });
}

// ── Utility ───────────────────────────────────────────────────────────
function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

// ── Init ──────────────────────────────────────────────────────────────
export async function initRoster() {
  await loadStudents();
  if (totalEl) totalEl.textContent = students.length;
  if (countEl) countEl.textContent = students.length;
  initScrollTrigger();
  initSearch();
  initKeyboardNav();
  window.addEventListener('resize', debounce(() => {
    ScrollTrigger.refresh();
  }, 250));
}
```

---

## 7 — Section 07: Timeline / Highlights

### 7.1 Design Specification

```
PURPOSE:   A chronological narrative of the batch's journey,
           from orientation week to graduation day.

LAYOUT:    Vertical scroll timeline.
           Alternating left/right cards (desktop).
           Single-column stacked (mobile).
           Center spine line with animated progress.

ENTRIES:   Each timeline entry contains:
           — Date (month + year, not specific day)
           — Event title
           — Short description (2–3 sentences max)
           — Optional: 1–3 photos
           — Optional: quote from a student about that event

ANIMATION: Entries reveal as user scrolls into them (fade-up + slide-in
           from the correct side). Spine line draws progressively.
```

### 7.2 Timeline Data Schema

```json
{
  "timeline": [
    {
      "id": "orientation-2022",
      "date": "August 2022",
      "title": "First Day. 187 Strangers.",
      "description": "None of us knew what we were walking into. The College of Management was bigger than it looked online. We found our classrooms by following whoever looked the most confident.",
      "photos": ["events/orientation-01.webp", "events/orientation-02.webp"],
      "quote": {
        "text": "I sat in the wrong room for twenty minutes.",
        "author": "Jose Reyes"
      },
      "category": "milestone",
      "side": "left"
    }
  ]
}
```

### 7.3 Timeline CSS (Core)

```css
.timeline {
  position: relative;
  padding: var(--space-16) 0;
}

/* Center spine */
.timeline::before {
  content: '';
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--clr-border);
  transform: translateX(-50%);
}

/* Animated progress overlay on spine */
.timeline__progress-line {
  position: absolute;
  left: 50%;
  top: 0;
  width: 2px;
  background: var(--clr-accent);
  transform: translateX(-50%);
  transform-origin: top;
  height: 0;  /* GSAP scrolls this to 100% */
  box-shadow: 0 0 8px var(--clr-accent);
}

/* Entry */
.timeline-entry {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: var(--space-6);
  align-items: start;
  margin-bottom: var(--space-16);
  opacity: 0;
  transform: translateY(40px);
}

.timeline-entry.is-visible {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 0.7s var(--ease-out-quart),
              transform 0.7s var(--ease-out-quart);
}

/* Content card — left or right */
.timeline-entry__card {
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  position: relative;
}

/* Dot on spine */
.timeline-entry__dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--clr-accent);
  border: 3px solid var(--clr-bg);
  margin-top: var(--space-6);
  flex-shrink: 0;
  box-shadow: 0 0 0 4px rgba(var(--clr-accent-rgb), 0.2);
}

/* Entries: alternating sides */
.timeline-entry:nth-child(odd)  .timeline-entry__card { grid-column: 1; }
.timeline-entry:nth-child(odd)  .timeline-entry__dot  { grid-column: 2; }
.timeline-entry:nth-child(odd)  .timeline-entry__empty { grid-column: 3; }

.timeline-entry:nth-child(even) .timeline-entry__empty { grid-column: 1; }
.timeline-entry:nth-child(even) .timeline-entry__dot   { grid-column: 2; }
.timeline-entry:nth-child(even) .timeline-entry__card  { grid-column: 3; }

/* Mobile: single column */
@media (max-width: 768px) {
  .timeline::before,
  .timeline__progress-line { left: var(--space-4); }

  .timeline-entry {
    grid-template-columns: auto 1fr;
  }

  .timeline-entry__dot   { grid-column: 1; grid-row: 1; }
  .timeline-entry__card  { grid-column: 2; grid-row: 1; }
  .timeline-entry__empty { display: none; }

  /* Override even/odd on mobile */
  .timeline-entry:nth-child(even) .timeline-entry__empty { display: none; }
  .timeline-entry:nth-child(even) .timeline-entry__dot   { grid-column: 1; }
  .timeline-entry:nth-child(even) .timeline-entry__card  { grid-column: 2; }
}
```

---

## 8 — Section 08: Memories Gallery

### 8.1 Design Specification

```
PURPOSE:    Candid photos. The unposed, real moments.
            This is the section that triggers actual laughter and tears.

LAYOUT:     Masonry grid (column-based, not row-based).
            Photos of varying aspect ratios arranged without white space.
            Lightbox on click: full-screen view with keyboard navigation.

LOADING:    Lazy load all images below the fold.
            Thumbnail (400px wide WebP) loads first.
            Full resolution (1200px wide WebP) loads on lightbox open.

FILTERING:  By event category (Orientation, Intramurals, Retreat, etc.)
            By year (1st year, 2nd year, 3rd year, 4th year)

MOBILE:     2-column masonry (reduce to 1 column below 400px).
```

### 8.2 Masonry CSS (No JS Required for Layout)

```css
.gallery-grid {
  columns: 4 240px;       /* Auto-fills columns, min 240px each */
  column-gap: var(--space-3);
  padding: 0 var(--space-6);
}

.gallery-item {
  break-inside: avoid;     /* Critical: prevents photo from splitting across columns */
  margin-bottom: var(--space-3);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  border-radius: var(--radius-md);
}

.gallery-item img {
  width: 100%;
  height: auto;
  display: block;
  transition: transform 0.5s var(--ease-out-quart),
              filter 0.3s ease;
  will-change: transform;
}

.gallery-item:hover img {
  transform: scale(1.04);
  filter: brightness(0.85);
}

/* Caption overlay */
.gallery-item__caption {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: var(--space-3) var(--space-4);
  background: linear-gradient(transparent, rgba(0,0,0,0.75));
  color: white;
  font-size: var(--text-xs);
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.gallery-item:hover .gallery-item__caption {
  opacity: 1;
  transform: translateY(0);
}

@media (max-width: 768px) {
  .gallery-grid { columns: 2 160px; }
}
@media (max-width: 400px) {
  .gallery-grid { columns: 1; }
}
```

### 8.3 Lightbox Implementation

```js
// gallery.js — Lightweight lightbox (no dependencies)
export function initLightbox() {
  const items   = document.querySelectorAll('.gallery-item');
  const images  = Array.from(items).map(item => ({
    src:     item.dataset.fullSrc,
    alt:     item.querySelector('img').alt,
    caption: item.dataset.caption,
  }));

  let currentIndex = 0;

  // Create lightbox DOM
  const lb = document.createElement('div');
  lb.className = 'lightbox';
  lb.setAttribute('role', 'dialog');
  lb.setAttribute('aria-modal', 'true');
  lb.setAttribute('aria-label', 'Photo viewer');
  lb.hidden = true;
  lb.innerHTML = `
    <div class="lightbox__backdrop"></div>
    <button class="lightbox__close" aria-label="Close photo viewer">×</button>
    <button class="lightbox__prev" aria-label="Previous photo">‹</button>
    <button class="lightbox__next" aria-label="Next photo">›</button>
    <figure class="lightbox__figure">
      <img class="lightbox__img" src="" alt="" loading="eager">
      <figcaption class="lightbox__caption"></figcaption>
    </figure>
    <div class="lightbox__counter" aria-live="polite"></div>
  `;
  document.body.appendChild(lb);

  const lbImg     = lb.querySelector('.lightbox__img');
  const lbCaption = lb.querySelector('.lightbox__caption');
  const lbCounter = lb.querySelector('.lightbox__counter');

  function open(index) {
    currentIndex = index;
    const photo = images[index];
    lbImg.src          = photo.src;
    lbImg.alt          = photo.alt;
    lbCaption.textContent = photo.caption || '';
    lbCounter.textContent = `${index + 1} / ${images.length}`;
    lb.hidden = false;
    document.body.style.overflow = 'hidden';
    lb.querySelector('.lightbox__close').focus();
  }

  function close() {
    lb.hidden = true;
    document.body.style.overflow = '';
    // Return focus to the triggering element
    items[currentIndex]?.querySelector('img').closest('button, a, [tabindex]')?.focus();
  }

  function navigate(direction) {
    currentIndex = (currentIndex + direction + images.length) % images.length;
    open(currentIndex);
  }

  // Event binding
  items.forEach((item, i) => {
    item.setAttribute('tabindex', '0');
    item.setAttribute('role', 'button');
    item.setAttribute('aria-label', `View photo ${i + 1}`);
    item.addEventListener('click', () => open(i));
    item.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(i); }
    });
  });

  lb.querySelector('.lightbox__close').addEventListener('click', close);
  lb.querySelector('.lightbox__prev').addEventListener('click', () => navigate(-1));
  lb.querySelector('.lightbox__next').addEventListener('click', () => navigate(1));
  lb.querySelector('.lightbox__backdrop').addEventListener('click', close);

  document.addEventListener('keydown', e => {
    if (lb.hidden) return;
    if (e.key === 'Escape')     close();
    if (e.key === 'ArrowLeft')  navigate(-1);
    if (e.key === 'ArrowRight') navigate(1);
  });
}
```

---

## 9 — Section 09: Superlatives

### 9.1 Design Specification

```
PURPOSE:   Batch-voted awards that capture personality and memory.
           Humorous + sincere in equal measure.

LAYOUT:    Card grid. Each card: Award name + two recipient portraits
           side-by-side (male + female, or simply two awardees).

ANIMATION: Cards flip on hover to reveal back side with a quote
           from each awardee.

CATEGORIES (Standard):
  ─ Most Likely to Be Famous
  ─ Most Likely to Become a CEO
  ─ Most Likely to Change the World
  ─ Best Couple (Batch Sweethearts)
  ─ Best Dressed
  ─ Most Organized
  ─ Most Hardworking
  ─ Class Clown
  ─ Most Photogenic
  ─ Best Leader
  ─ [Custom batch-specific awards]
```

### 9.2 Superlative Card CSS (3D Flip)

```css
.superlatives-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(280px, 100%), 1fr));
  gap: var(--space-6);
  padding: var(--space-8) var(--space-6);
}

.superlative-card {
  perspective: 1000px;
  height: 360px;
  cursor: pointer;
}

.superlative-card__inner {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  transition: transform 0.65s cubic-bezier(0.4, 0, 0.2, 1);
}

.superlative-card:hover .superlative-card__inner,
.superlative-card:focus-within .superlative-card__inner {
  transform: rotateY(180deg);
}

.superlative-card__front,
.superlative-card__back {
  position: absolute;
  inset: 0;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  border-radius: var(--radius-lg);
  overflow: hidden;
}

/* ── Front ────────────────────────────────────── */
.superlative-card__front {
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.superlative-card__award {
  padding: var(--space-4) var(--space-6);
  font-family: var(--font-accent);
  font-size: var(--text-xs);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--clr-accent);
  text-align: center;
  border-bottom: 1px solid var(--clr-border);
  width: 100%;
}

.superlative-card__photos {
  display: flex;
  flex: 1;
  width: 100%;
}

.superlative-card__photos img {
  width: 50%;
  height: 100%;
  object-fit: cover;
  object-position: center top;
}

.superlative-card__names {
  padding: var(--space-3);
  display: flex;
  justify-content: space-around;
  width: 100%;
  font-size: var(--text-sm);
  font-weight: 500;
  border-top: 1px solid var(--clr-border);
}

/* ── Back ─────────────────────────────────────── */
.superlative-card__back {
  background: var(--clr-accent);
  transform: rotateY(180deg);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-8);
  gap: var(--space-4);
}

.superlative-card__quote {
  font-family: var(--font-display);
  font-style: italic;
  font-size: var(--text-lg);
  color: var(--clr-bg);
  text-align: center;
  line-height: 1.4;
}

.superlative-card__quote-author {
  font-family: var(--font-accent);
  font-size: var(--text-xs);
  color: rgba(var(--clr-bg-rgb), 0.6);
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

/* Reduce motion: no flip, use fade instead */
@media (prefers-reduced-motion: reduce) {
  .superlative-card__inner {
    transition: none;
  }
  .superlative-card:hover .superlative-card__back {
    opacity: 1;
  }
}
```

---

## 10 — Section 10: Statistics & Facts

### 10.1 Design Specification

```
PURPOSE:   Give the batch a quantitative identity.
           "We are more than people — we are a story told in numbers."

DATA TYPES:
  — Total graduates (by gender, program, section)
  — Latin honors breakdown
  — Cities/provinces represented
  — Thesis topics word cloud (if applicable)
  — Most common: names, birthdays, favorite quotes
  — Average GPA range
  — Number of org memberships, awards, leadership roles
  — "If we were all in the same room" fun facts

ANIMATION: Number counters animate from 0 to final value when scrolled
           into view. Pie/bar charts draw progressively.
           Word cloud fades in word by word.
```

### 10.2 Animated Counter

```js
// stats.js
export function initCounters() {
  const counters = document.querySelectorAll('[data-count-to]');
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      observer.unobserve(entry.target);

      const el       = entry.target;
      const target   = parseInt(el.dataset.countTo, 10);
      const duration = parseInt(el.dataset.duration, 10) || 1500;
      const suffix   = el.dataset.suffix || '';

      if (prefersReduced) {
        el.textContent = target.toLocaleString() + suffix;
        return;
      }

      const start = performance.now();
      function tick(now) {
        const elapsed  = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased    = 1 - Math.pow(1 - progress, 3); // ease-out-cubic
        const current  = Math.round(eased * target);
        el.textContent = current.toLocaleString() + suffix;
        if (progress < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    });
  }, { threshold: 0.5 });

  counters.forEach(el => observer.observe(el));
}
```

---

## 11 — Section 11: Farewell Messages

### 11.1 Design Specification

```
PURPOSE:   Each student's final words to their batch.
           This is the most intimate, personal section.

LAYOUT:    Scrolling marquee (horizontal) of short quotes at top.
           Below: card grid where each card shows name + message.
           Card expand on click to reveal full message.

CONSIDERATIONS:
  — Messages may be long. Truncate to 3 lines, expand on click.
  — Sort options: alphabetical, random (use seeded random for consistency)
  — Allow reading without clicking: keyboard expandable
  — Handle empty messages gracefully: "Maria chose to let her smile
    speak for her." (auto-generated fallback)
```

---

## 12 — Section 14: Closing / Colophon

### 12.1 Design Specification

```
PURPOSE:   The last page of the book. Quiet. Final. Memorable.

CONTENT:
  — Final batch portrait (the most formal group photo)
  — Theme statement, large
  — "Made with love by [Yearbook Committee], [Year]"
  — Credits: photography, design, development, data
  — Version number (for archiving: "Edition 1.0, June 2026")
  — Copyright notice
  — Preservation note: "This yearbook is permanently archived at [URL]"

ANIMATION: After scrolling to the very bottom, the page "closes" —
           a soft fade to the batch color, then a final message appears.
           Then: silence. The book is done.
```

---

## 13 — Design Token System

### 13.1 Complete Token File

```css
/* tokens.css — The single source of truth for all design decisions */
:root {

  /* ══ Color Architecture ════════════════════════════════════════════ */

  /* Primary — large surfaces, backgrounds */
  --clr-primary: #070810;
  --clr-primary-rgb: 7, 8, 16;

  /* Surface — cards, panels */
  --clr-surface:     rgba(255,255,255,0.04);
  --clr-surface-alt: rgba(255,255,255,0.07);

  /* Borders */
  --clr-border:      rgba(255,255,255,0.08);
  --clr-border-strong: rgba(255,255,255,0.16);

  /* Accent — the batch's signature color */
  --clr-accent:      #C8A951;   /* Gold — override per batch */
  --clr-accent-rgb:  200, 169, 81;
  --clr-accent-dim:  rgba(200,169,81,0.15);
  --clr-accent-glow: 0 0 24px rgba(200,169,81,0.3);

  /* Text */
  --clr-text-primary:   #F0EFF6;
  --clr-text-secondary: rgba(240,239,246,0.5);
  --clr-text-muted:     rgba(240,239,246,0.3);

  /* Status */
  --clr-success: #39D98A;
  --clr-warning: #FFBE0B;
  --clr-error:   #FF4D6D;

  /* Background alias */
  --clr-bg:     var(--clr-primary);
  --clr-bg-rgb: var(--clr-primary-rgb);


  /* ══ Typography ════════════════════════════════════════════════════ */

  --font-display: 'Cormorant Garamond', Georgia, serif;
  --font-body:    'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-accent:  'JetBrains Mono', 'Courier New', monospace;

  /* Type scale: fluid with clamp() */
  --text-micro: clamp(0.6rem,  1.2vw, 0.65rem);
  --text-xs:    clamp(0.7rem,  1.5vw, 0.75rem);
  --text-sm:    clamp(0.8rem,  2vw,   0.875rem);
  --text-base:  clamp(0.9rem,  2.5vw, 1rem);
  --text-lg:    clamp(1rem,    3vw,   1.2rem);
  --text-xl:    clamp(1.2rem,  4vw,   1.5rem);
  --text-2xl:   clamp(1.5rem,  5vw,   2rem);
  --text-3xl:   clamp(2rem,    7vw,   3rem);
  --text-4xl:   clamp(2.5rem,  9vw,   4.5rem);
  --text-hero:  clamp(4rem,    15vw,  10rem);


  /* ══ Spacing (8pt system) ══════════════════════════════════════════ */
  --space-1:   0.25rem;  /*  4px */
  --space-2:   0.5rem;   /*  8px */
  --space-3:   0.75rem;  /* 12px */
  --space-4:   1rem;     /* 16px */
  --space-5:   1.25rem;  /* 20px */
  --space-6:   1.5rem;   /* 24px */
  --space-8:   2rem;     /* 32px */
  --space-10:  2.5rem;   /* 40px */
  --space-12:  3rem;     /* 48px */
  --space-16:  4rem;     /* 64px */
  --space-20:  5rem;     /* 80px */
  --space-24:  6rem;     /* 96px */
  --space-32:  8rem;     /* 128px */


  /* ══ Border Radii ══════════════════════════════════════════════════ */
  --radius-xs:   2px;
  --radius-sm:   4px;
  --radius-md:   8px;
  --radius-lg:   16px;
  --radius-xl:   24px;
  --radius-2xl:  32px;
  --radius-full: 9999px;


  /* ══ Shadows ═══════════════════════════════════════════════════════ */
  --shadow-sm:    0 1px 3px rgba(0,0,0,0.35);
  --shadow-md:    0 4px 16px rgba(0,0,0,0.45);
  --shadow-lg:    0 12px 40px rgba(0,0,0,0.55);
  --shadow-glow:  var(--clr-accent-glow);


  /* ══ Animation ═════════════════════════════════════════════════════ */
  --ease-out-quart:    cubic-bezier(0.25, 1, 0.5, 1);
  --ease-in-out-expo:  cubic-bezier(0.87, 0, 0.13, 1);
  --ease-spring:       cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-smooth:       cubic-bezier(0.4, 0, 0.2, 1);

  --duration-instant: 100ms;
  --duration-fast:    200ms;
  --duration-base:    350ms;
  --duration-slow:    600ms;
  --duration-xslow:   1000ms;
  --duration-cinematic: 1500ms;


  /* ══ Layout ════════════════════════════════════════════════════════ */
  --max-width:        1280px;
  --max-width-narrow: 720px;
  --max-width-wide:   1536px;
  --nav-height:       64px;
  --controls-height:  72px;
  --section-padding:  clamp(var(--space-12), 8vw, var(--space-24));
}


/* ── Light Theme Override ───────────────────── */
[data-theme="light"] {
  --clr-primary:        #FAFAF7;
  --clr-primary-rgb:    250, 250, 247;
  --clr-surface:        rgba(0,0,0,0.03);
  --clr-surface-alt:    rgba(0,0,0,0.06);
  --clr-border:         rgba(0,0,0,0.08);
  --clr-border-strong:  rgba(0,0,0,0.14);
  --clr-text-primary:   #1A1A18;
  --clr-text-secondary: rgba(26,26,24,0.55);
  --clr-text-muted:     rgba(26,26,24,0.35);
}
```

---

## 14 — Performance Engineering

### 14.1 Image Optimization Pipeline

```
STEP 1 — SOURCE REQUIREMENTS
  Portrait originals: minimum 600×750px, JPG or PNG
  Candid originals:   minimum 1200px wide on longest edge
  Cover original:     minimum 2400×1600px

STEP 2 — CONVERSION TO WEBP
  Tool: squoosh.app (web), sharp (Node.js), or cwebp (CLI)
  
  CLI batch conversion:
    for f in photos/originals/*.jpg; do
      cwebp -q 80 "$f" -o "photos/portraits/${f%.jpg}.webp"
    done

STEP 3 — GENERATE @2x (RETINA)
  Portraits:   300×375px (@1x)  →  600×750px (@2x)
  Thumbnails:  200px wide (@1x) →  400px wide (@2x)
  Cover:       1920×1080px      →  3840×2160px (only if file size ≤ 400KB)

STEP 4 — JPEG FALLBACK (for older browsers, email)
  Keep compressed JPG alongside WebP.
  Use <picture> element for format negotiation.

STEP 5 — GENERATE OG IMAGE (for social sharing)
  Size: 1200×630px, JPEG, ≤ 150KB
  Content: Cover photo + batch name + year overlay
```

### 14.2 Loading Strategy by Section

```
SECTION              STRATEGY                      IMAGE PRIORITY
──────────────────   ────────────────────────────  ──────────────
Cover                Eager + fetchpriority="high"  CRITICAL PATH
Table of Contents    No images                     N/A
Opening Message      1 portrait, lazy              LOW
Batch Theme          Background only, lazy         MEDIUM
Student Roster       Virtualized, lazy after [2]   MEDIUM
Officers             Eager (above fold)            HIGH
Timeline             Lazy, progressive reveal      LOW
Gallery              Lazy, thumbnail first         LOW
Superlatives         Lazy, 2 portraits per card    LOW
Stats                No real images                N/A
Messages             Avatar thumbnails, lazy       LOW
Faculty              Lazy                          LOW
Colophon             1 group photo, lazy           LOW
```

### 14.3 Performance Budget

```
METRIC                   BUDGET          HOW TO ACHIEVE
──────────────────────   ─────────────   ─────────────────────────────────────
Largest Contentful Paint ≤ 2.5s          Eager cover image, preload font
First Input Delay        ≤ 100ms         Defer all JS; no render-blocking CSS
Cumulative Layout Shift  ≤ 0.1           width+height on all images
Total Page Weight (cover)≤ 800KB         WebP, compressed video, subsetting fonts
Time to Interactive      ≤ 3.5s          Defer JS; inline critical CSS
Lighthouse Score         ≥ 90 all        Run audit before deployment
```

### 14.4 Font Subsetting

```bash
# Subset fonts to only the characters needed (saves 60–80% font size)
# Tool: pyftsubset (pip install fonttools)

pyftsubset "CormorantGaramond-Regular.ttf" \
  --output-file="CormorantGaramond-Regular.subset.woff2" \
  --flavor=woff2 \
  --unicodes="U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,\
              U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,\
              U+2212,U+2215,U+FEFF,U+FFFD"
```

### 14.5 Critical CSS Strategy

```html
<!-- Inline only what's needed for above-the-fold render -->
<style>
  /* Paste inlined critical CSS here — tokens + reset + cover hero only */
  /* Everything else loads via <link> */
</style>

<!-- Defer non-critical CSS -->
<link rel="stylesheet" href="assets/css/components.css"
      media="print" onload="this.media='all'">
<noscript>
  <link rel="stylesheet" href="assets/css/components.css">
</noscript>
```

---

## 15 — Print Mode

### 15.1 Print CSS

```css
/* print.css — Loaded always; only active on @media print */
@media print {

  /* Remove interactive elements */
  .site-nav,
  .roster-controls,
  .cover-hero__scroll-cue,
  .nav-drawer,
  .lightbox,
  .keyboard-hint,
  .roster-progress {
    display: none !important;
  }

  /* Reset scroll-based layout to static */
  .roster-wrapper { height: auto !important; }
  .roster-sticky  { position: static !important; }
  .roster-item    { position: static !important; opacity: 1 !important; }

  /* Each student on their own row */
  .roster-item {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 1cm;
    page-break-inside: avoid;
    padding: 0.5cm 0;
    border-bottom: 0.5pt solid #ccc;
  }

  .roster-item__name--last { display: inline; }
  .roster-item__portrait-wrap {
    width: 3cm !important;
    height: 3.75cm !important;
  }

  /* Page setup */
  @page {
    size: A4;
    margin: 2cm 2.5cm;
  }

  /* Section page breaks */
  .yearbook-section { page-break-before: always; }
  .yearbook-section:first-child { page-break-before: auto; }

  /* Ensure URLs print */
  a[href]::after {
    content: " (" attr(href) ")";
    font-size: 8pt;
    color: #666;
  }

  /* Preserve cover photo */
  .cover-hero__media img { max-height: 10cm; }
}
```

---

## 16 — Accessibility Standards

### 16.1 Yearbook-Specific A11y Requirements

```
REQUIREMENT                     IMPLEMENTATION
──────────────────────────────  ────────────────────────────────────────────
Screen reader roster access     All student names in aria-label, not just
                                split-text spans (which are aria-hidden)
Photo alt text                  "[Name]'s graduation portrait" — never empty
Gallery navigation              Full keyboard nav in lightbox (arrow keys)
Animation opt-out               prefers-reduced-motion respected everywhere
Color contrast                  Text on portrait overlays ≥ 4.5:1
Focus management in modals      Focus trapped inside open lightbox/drawer
Skip link                       "Skip to main content" as first element
Section landmarks               All sections wrapped in <section> + aria-label
Live regions                    Search result count in aria-live="polite"
Closed captions                 Any video on cover has muted default + no
                                required audio content
Latin honor display             Never rely on color alone; show text labels
```

### 16.2 Skip Link

```html
<!-- Must be the absolute first focusable element in <body> -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<style>
.skip-link {
  position: absolute;
  top: -100%;
  left: var(--space-4);
  background: var(--clr-accent);
  color: var(--clr-bg);
  padding: var(--space-2) var(--space-4);
  border-radius: 0 0 var(--radius-md) var(--radius-md);
  font-weight: 600;
  font-size: var(--text-sm);
  z-index: 9999;
  text-decoration: none;
  transition: top 0.2s;
}
.skip-link:focus { top: 0; }
</style>
```

---

## 17 — Deployment & Preservation

### 17.1 Deployment Checklist

```
PRE-DEPLOYMENT
  [ ] All student photos uploaded and correctly named ([slug].webp)
  [ ] students.json validated — no missing required fields
  [ ] All internal links tested (no 404s)
  [ ] Open Graph image generated (og-cover.jpg, 1200×630px)
  [ ] Favicon set: favicon.ico + apple-touch-icon.png
  [ ] robots.txt present (allow all crawlers — yearbooks should be indexed)
  [ ] sitemap.xml generated
  [ ] Print mode tested (File → Print in Chrome)
  [ ] All pages tested at 320px, 768px, 1024px, 1440px
  [ ] Keyboard navigation tested (Tab, Enter, Escape, Arrow keys)
  [ ] Screen reader tested (NVDA + Chrome, or VoiceOver + Safari)
  [ ] Lighthouse scores ≥ 90 for Performance, Accessibility, Best Practices
  [ ] All CDN scripts have local /vendor/ fallbacks
  [ ] HTTPS enabled on deployment host

DEPLOYMENT PLATFORMS (in order of preference for longevity)
  1. GitHub Pages — Free, git-versioned, survives company changes
  2. Netlify       — Free tier, global CDN, form support if needed
  3. Vercel        — Free tier, excellent performance
  4. Cloudflare Pages — Free, fast globally
  5. Shared hosting  — cPanel upload (for non-technical committees)

POST-DEPLOYMENT
  [ ] Custom domain configured (e.g., batch2026.college.edu.ph)
  [ ] Domain renewal set for 10 years minimum
  [ ] DNS TTL documented for future maintainers
  [ ] Repository archived (GitHub → Settings → Archive)
  [ ] ZIP of entire /dist/ folder backed up to 3 locations
  [ ] Wayback Machine submission: https://web.archive.org/save/[URL]
  [ ] Share URL sent to all graduates via email/chat
```

### 17.2 Long-Term Preservation Protocol

```
YEAR 1:    Normal maintenance. Fix any broken links.
YEAR 3:    Audit external links (CDN versions). Update vendor/ if needed.
YEAR 5:    Test on current browsers. Ensure no deprecation issues.
YEAR 10:   Major review. Consider static snapshot if hosting changes.
           Archive full site as single HTML file using:
           wget --mirror --convert-links --adjust-extension
                --page-requisites --no-parent [URL]

ASSET BACKUP RULE:
  The yearbook must exist in at least THREE places at all times:
  ① Live website (primary)
  ② GitHub repository (version control)
  ③ Offline ZIP (USB drive held by batch president or faculty adviser)

VENDOR LOCK-IN AVOIDANCE:
  — No proprietary database (JSON files only)
  — No authentication system
  — No third-party comment/interaction system
  — No dynamic server (pure static output)
  — Google Fonts: always download and self-host in /assets/fonts/
```

---

## 18 — Output Protocol

### FORMAT A — FULL YEARBOOK BUILD

*Trigger: "build the complete yearbook" / "create the full site"*

```
Produce: All section HTML files + complete CSS + JS modules
         Full data schema with example entries
         All animation implementations
         Deployment-ready file structure
Complete in: Multiple responses (section by section, clearly marked)
Start with: Cover + Roster (highest priority sections)
```

### FORMAT B — SINGLE SECTION BUILD

*Trigger: "build the roster section" / "create the gallery"*

```
Produce: Complete HTML + CSS + JS for that section only
         Self-contained (can drop into existing project)
         Include relevant data schema for that section
         Include responsive behavior description
```

### FORMAT C — DESIGN-ONLY SPRINT

*Trigger: "design the yearbook" / "give me the visual direction"*

```
Produce: Aesthetic archetype selection + rationale
         Full color token set (all 6 roles with hex)
         Font pairing (3 roles with Google Fonts links)
         Section-by-section layout description
         Animation choreography notes
         NO CODE — design specification only
```

### FORMAT D — REFINEMENT / AUDIT

*Trigger: "improve my yearbook" / "audit this code" / "what's wrong with this"*

```
Produce: Gap analysis against this skill's standards
         Ranked list of issues (Critical → High → Medium → Low)
         Specific code fixes for each issue
         Performance improvements with measurable impact
```

---

## Appendix A — Agent Assumptions Log Template

```
When brief signals are absent, the agent records every creative decision here.

FORMAT:
  [ASSUMED] [SECTION § __] → Decision → Reason → Override instruction

EXAMPLE:
  [ASSUMED] § 2 Aesthetic → Cinematic Dark selected → "engineering batch"
             implies technical/bold preference + no existing brand colors
             provided. Override: specify "Editorial Luxury" or any other
             archetype name to change the entire visual system.

  [ASSUMED] § 4 Stack → Vanilla HTML/CSS/JS chosen → No framework preference
             stated; vanilla maximizes longevity and portability.
             Override: specify "Next.js" or "Astro" for build-step workflow.

  [ASSUMED] § 5 Cover → Video disabled → No video file referenced in brief.
             Override: provide cover-reel.mp4 path to enable video background.
```

---

## Appendix B — Content Collection Checklist

```
DATA TO COLLECT FROM EACH STUDENT:
  [ ] Legal full name (for official record)
  [ ] Preferred display name / nickname
  [ ] Course / program + section
  [ ] Student number
  [ ] Portrait photo (specifications: § 14.1)
  [ ] 1–3 candid photo submissions
  [ ] Senior quote (text + optional attribution)
  [ ] Personal ambition / life goal
  [ ] Favorite batch memory (1–2 sentences)
  [ ] Message to the batch (for farewell section)
  [ ] LinkedIn / portfolio URL (optional)
  [ ] Awards, honors, organization roles

DATA TO COLLECT FROM BATCH LEADERSHIP:
  [ ] Batch theme word and full theme statement
  [ ] Batch logo (SVG preferred)
  [ ] Batch color palette
  [ ] Timeline of key events (date + title + description)
  [ ] Superlatives winners (by award name + two awardees)
  [ ] Officers list (position + name + portrait)
  [ ] Dean's / adviser's message (text or letter scan)
  [ ] Faculty tributes list (name + department + portrait)
  [ ] Sponsors / supporters (name + logo)
  [ ] Yearbook committee credits
```

---

## Appendix C — Accessibility Testing Protocol

```
TOOL                    TEST                              PASS THRESHOLD
─────────────────────   ────────────────────────────────  ────────────────
Chrome DevTools         Lighthouse → Accessibility         Score ≥ 90
axe DevTools extension  Full page scan                     0 Critical errors
NVDA + Chrome           Navigate roster by keyboard        All names readable
iOS VoiceOver           Swipe through gallery              Captions announced
Keyboard only (no mouse)Complete yearbook navigation       No trapped focus
Color Contrast Analyzer Text on all backgrounds            ≥ 4.5:1 (AA)
Zoom to 200%            No horizontal overflow at 200%     No scroll at 320px×2
```

<!--
  ╔══════════════════════════════════════════════════════════════════════════╗
  ║  END OF SKILL — digital-college-yearbook v1.0.0                        ║
  ║                                                                         ║
  ║  This skill produces a time capsule, not a website.                    ║
  ║  Build it like it needs to work in 2040.                               ║
  ║  Design it like someone will cry looking at it in 2035.                ║
  ║  Code it like the person maintaining it is a stranger.                 ║
  ╚══════════════════════════════════════════════════════════════════════════╝
-->
