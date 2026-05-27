---
name: 21st-dev-builder-v2
description: Build websites and web apps using 21st.dev — the largest marketplace of shadcn/ui-based React Tailwind components with 1400+ components. Use when user mentions "21st.dev", "21st", "ใช้ 21st", "จาก 21st", "build with 21st", "21st component", "21st magic MCP", or references the 21st.dev component registry in any language. Covers building complete sites (landing pages, dashboards, portfolios, e-commerce storefronts, auth pages), browsing and installing individual 21st.dev components into existing projects, and setting up the 21st.dev MCP server. Also trigger when user wants premium UI components specifically from the 21st.dev registry. Do NOT trigger for general web development, standard shadcn/ui, plain Tailwind CSS, React Native, API development, testing, deployment, or any task that doesn't explicitly reference 21st or 21st.dev.
---

# 21st.dev Web Builder v2

Build production-ready websites using [21st.dev](https://21st.dev) — the largest open-source registry of React UI components. You are an expert at discovering, analyzing, selecting, and integrating 21st.dev components to create polished, cohesive web applications.

This skill makes you exceptionally good at:
- **Live discovery** — Always fetching the latest components from 21st.dev before building
- **Smart analysis** — Evaluating which components best fit the user's needs
- **Design coherence** — Maintaining visual consistency across components from different authors
- **Full-stack composition** — Building complete multi-page applications, not just isolated pages

## Core Knowledge

### What is 21st.dev?
An open-source community registry (the "npm for design engineers") with 1400+ React components. Unlike npm packages, components are installed as full source code you own and can customize. Built on shadcn/ui philosophy.

### Tech Stack
- **Framework**: React 18+ / Next.js (App Router preferred)
- **Styling**: Tailwind CSS 4+
- **Primitives**: Radix UI
- **Language**: TypeScript
- **Install**: `npx shadcn@latest add "https://21st.dev/r/{author}/{component}"`

### URL Patterns
| Purpose | URL Pattern |
|---------|-------------|
| Browse category | `https://21st.dev/s/{slug}` |
| Component detail | `https://21st.dev/r/{author}/{component}` |
| Author profile | `https://21st.dev/{author}` |
| Community search | `https://21st.dev/community/components/search` |

## Workflow

### Phase 1: Project Setup

Check if the project is ready. Look for `package.json`, `tailwind.config.*`, and `components.json`.

**New project:**
```bash
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
cd my-app
npx shadcn@latest init -d
```

**Existing project missing shadcn:**
```bash
npx shadcn@latest init
```

**Check MCP availability:** If `21st_magic_component_builder` tool is available, use it as the primary component generation method. Otherwise, use WebSearch + WebFetch + npx install (works perfectly well).

### Phase 2: Requirement Analysis

Break down the user's request into a component plan:

1. **Identify the application type** — What kind of app or page is being built?
2. **List required sections/features** — What does each page need?
3. **Map to component categories** — Use the Component Map below
4. **Identify shared components** — Which components appear across multiple pages?

#### Component Map

| Building... | Search these categories on 21st.dev |
|-------------|-------------------------------------|
| Landing page | `hero`, `features`, `pricing`, `testimonials`, `cta`, `footers`, `navbars`, `backgrounds`, `announcements`, `clients` |
| Dashboard | `sidebar`, `cards`, `tables`, `tabs`, `buttons`, `menus`, `badges`, `numbers` |
| Auth pages | `sign-ins`, `sign-ups`, `forms`, `inputs`, `buttons` |
| Blog / Content | `cards`, `texts`, `images`, `paginations`, `scroll-areas` |
| E-commerce | `cards`, `carousels`, `badges`, `buttons`, `dialogs`, `inputs`, `tabs`, `selects` |
| Form-heavy app | `inputs`, `selects`, `checkboxes`, `radio-groups`, `date-pickers`, `forms`, `text-areas`, `toggles` |
| AI / Chat app | `ai-chats`, `inputs`, `buttons`, `cards`, `spinner-loaders` |
| Settings page | `forms`, `inputs`, `toggles`, `tabs`, `selects`, `checkboxes`, `accordions` |
| Portfolio | `hero`, `cards`, `images`, `texts`, `scroll-areas`, `backgrounds`, `navigation-menus` |
| SaaS product | `hero`, `pricing`, `features`, `testimonials`, `navbars`, `footers`, `cta`, `comparisons` |

### Phase 3: Live Component Discovery

**Every build session must include live discovery.** 21st.dev adds new components constantly — never rely on memory alone.

#### Discovery Strategy

For each component category you need, follow this search sequence:

**Step 1: Browse the category page**
```
WebFetch: https://21st.dev/s/{category-slug}
```
This shows all available components in that category with names, authors, and popularity.

**Step 2: Deep-dive on promising components**
```
WebFetch: https://21st.dev/r/{author}/{component}
```
View the component's demo, code, dependencies, and installation command.

**Step 3: Search for specific styles (if category browsing isn't enough)**
```
WebSearch: "site:21st.dev {specific style or feature}"
```
Example: `site:21st.dev animated gradient hero` or `site:21st.dev glassmorphism card`

#### Category Slugs Reference

Read `references/component-catalog.md` for the full catalog of categories with slugs, counts, and top authors. Here are the most-used ones:

**Landing Sections:** `hero`, `features`, `pricing`, `testimonials`, `cta`, `footers`, `navbars`, `backgrounds`, `announcements`, `clients`, `comparisons`, `docks`, `shaders`

**UI Components:** `buttons`, `inputs`, `cards`, `selects`, `sliders`, `accordions`, `tabs`, `dialogs`, `calendars`, `ai-chats`, `tables`, `badges`, `dropdowns`, `alerts`, `forms`, `popovers`, `text-areas`, `radio-groups`, `spinner-loaders`, `paginations`, `checkboxes`, `menus`, `numbers`, `avatars`, `carousels`, `links`, `toggles`, `date-pickers`, `tooltips`, `toasts`, `sidebar`, `sign-ins`, `sign-ups`, `file-uploads`, `file-trees`, `icons`, `tags`, `notifications`, `empty-states`

### Phase 4: Component Analysis & Selection

This is where expertise matters most. For each component slot, evaluate candidates on these dimensions:

#### Selection Criteria (in priority order)

1. **Functional fit** — Does it actually do what's needed? Check props, interactivity, responsiveness.
2. **Visual quality** — Is it polished, modern, and well-designed? Check the live preview.
3. **Design coherence** — Will it look consistent with other selected components? Prefer:
   - Same author for related components (e.g., all navbar + footer from one author)
   - Similar design language (rounded vs. sharp corners, shadow style, spacing)
   - Consistent color system (CSS variable-based components work best together)
4. **Completeness** — Does it support dark mode? Is it responsive? Accessible?
5. **Popularity** — Higher likes/downloads usually mean better quality and fewer bugs.
6. **Recency** — Recently updated components often use newer patterns and APIs.
7. **Dependencies** — Fewer external dependencies = easier integration.

#### Decision Framework

```
For each component slot:
  1. Find 2-3 candidates from category browsing
  2. Score each on the criteria above (mentally)
  3. If user is involved → present top 2 with preview links + your recommendation
  4. If user says "you decide" → pick the best-scoring one
  5. Document your choice with reasoning
```

#### Author Consistency Strategy

When building a full page or site, try to use components from a small set of authors. This dramatically improves visual coherence. Notable authors with broad component ranges:

- **shadcn** — The foundation. Clean, minimal, highly composable.
- **bundui** — Animated, modern components.
- **magicui** — Motion-rich, creative components.
- Other prolific authors can be discovered during live browsing.

### Phase 4.5: Build vs Install Decision

Not every section needs a 21st.dev component. For each section, decide:

**INSTALL from 21st.dev when:**
- The section needs complex interactivity (navbar with dropdowns, pricing toggle, carousel)
- The section needs polished animations you don't want to write (animated hero, testimonial slider)
- A 21st.dev component fits the need almost perfectly

**WRITE CUSTOM when:**
- The section is simple (feature grid, stats row, basic CTA)
- No good 21st.dev component exists for this exact need
- You need very specific layout that would require heavy modification anyway
- Mixing too many authors would break design coherence

A typical landing page might install 2-3 complex components (hero, navbar, footer) and write 2-3 simple sections (features grid, stats, CTA) custom. This is faster and produces better results than forcing every section through 21st.dev.

### Phase 5: Installation & Integration

#### Install components:
```bash
npx shadcn@latest add "https://21st.dev/r/{author}/{component-name}"
```

What this does:
- Copies component source code to your project (usually `components/ui/` or `components/blocks/`)
- Installs required npm dependencies
- Updates Tailwind config if needed
- Resolves internal component dependencies

#### Installation order matters:
1. Install base/primitive components first (buttons, inputs)
2. Then composite components that may depend on them (forms, dialogs)
3. Finally section-level components (hero, pricing)

#### Post-Install Compatibility Fixes (CRITICAL)

After installing each component, **immediately check for these common issues** before moving on:

**1. `render` prop vs `asChild` conflict:**
Many newer 21st.dev components use `render` prop from `@base-ui/react`, but your project may use standard shadcn `asChild`. If you see TypeScript errors about `render` prop:
```tsx
// BROKEN: Component uses render prop
<Button render={<a href="/signup" />}>Sign Up</Button>

// FIX: Convert to asChild pattern
<Button asChild><a href="/signup">Sign Up</a></Button>
```
Check `Button`, `SheetTrigger`, `SelectTrigger` in every installed component.

**2. Container width mismatch:**
Components may assume different max-widths. After installing, verify each component uses a consistent container:
```tsx
// If component uses its own container, it may conflict with your layout
// Wrap all sections in a consistent container OR
// Remove the component's internal container and use your own
<section className="py-20">
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    {/* component content here */}
  </div>
</section>
```

**3. Missing CSS variables:**
If a component looks invisible or wrong, check that your `globals.css` defines all required CSS variables. Common missing ones: `--border`, `--ring`, `--muted`, `--muted-foreground`, `--accent`, `--accent-foreground`.

**4. framer-motion typing issues:**
Some components use `ease` arrays that TypeScript rejects. Fix by casting:
```tsx
// BROKEN
ease: [0.16, 1, 0.3, 1]
// FIX
ease: [0.16, 1, 0.3, 1] as const
```

**5. Faint/invisible card backgrounds:**
Many 21st.dev testimonial and feature cards use extremely subtle gradients (`from-muted/50 to-muted/10` or `border-t` only) that appear invisible on white backgrounds, especially in marquees where edge fades add further transparency. Fix by giving cards visible styling:
```tsx
// BROKEN: Nearly invisible
"rounded-lg border-t bg-gradient-to-b from-muted/50 to-muted/10"

// FIX: Clearly visible with depth
"rounded-xl border border-border/60 bg-card shadow-sm"
```

**6. Edge fade gradients too aggressive on marquees:**
Marquee components often have `w-1/3` fade gradients on each side, covering 2/3 of the content area. Reduce to `w-1/6` so cards remain visible:
```tsx
// BROKEN: Covers too much
"absolute inset-y-0 left-0 w-1/3 bg-gradient-to-r from-background"

// FIX: Subtle fade
"absolute inset-y-0 left-0 w-1/6 bg-gradient-to-r from-background"
```

**7. Gradient colors with oklch():**
Tailwind v4 uses `oklch()` for color values, but oklch is poorly rendered in `radial-gradient()` and some gradient contexts. Use `rgba()` or hex values for custom gradients:
```tsx
// BROKEN: oklch in gradients renders poorly
"bg-[radial-gradient(ellipse_at_center,_oklch(0.55_0.28_285_/_0.18)_0%,_transparent_65%)]"

// FIX: Use rgba for reliable gradient rendering
"bg-[radial-gradient(ellipse_at_center,_rgba(139,92,246,0.18)_0%,_transparent_65%)]"
```

**8. Gradient backgrounds behind parent backgrounds (z-index trap):**
Don't put gradient decorative elements with `-z-10` behind a parent that has its own `bg-background`. The parent's opaque background covers the gradient. Instead, apply the gradient directly on the section:
```tsx
// BROKEN: Gradient div behind parent bg-background
<section className="bg-background">
  <div className="-z-10 bg-gradient-to-b ..."> {/* invisible! */}

// FIX: Apply gradient directly on the section
<section className="bg-gradient-to-b from-[#ede9fe] via-[#f5f3ff] to-white">
```

#### If installation fails:
1. Check error message — usually a missing peer dependency
2. Try `npm install {missing-dep}` then retry
3. If component URL is wrong, search 21st.dev for the correct path
4. Last resort: fetch the component code via WebFetch and create files manually

### Phase 6: Page Composition

#### Layout Normalization (DO THIS FIRST)

Before composing, normalize the layout of all installed components so they play well together. 21st.dev components from different authors often have conflicting container widths, padding, and alignment. Fix this upfront:

1. **Pick one container width** for the entire page: `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`
2. **Open each installed component file** and check if it has its own container/max-width
3. **Either**: remove the component's internal container and wrap it externally, **or** ensure it matches your chosen width
4. **Check text alignment**: some components center-align content, others left-align. Normalize.
5. **Check hero height**: hero components often use `min-h-screen` which may be too tall. Adjust to `min-h-[80vh]` or less if needed.

#### Composition Patterns

**Landing Page:**
```tsx
<Navbar />                          {/* sticky top-0 z-50 */}
<main>
  <Hero />                          {/* min-h-[80vh] — NOT min-h-screen */}
  <Features />                      {/* py-20 bg-muted/50 */}
  <SocialProof />                   {/* py-16 */}
  <Pricing />                       {/* py-20 bg-muted/50 */}
  <Testimonials />                  {/* py-16 */}
  <CTA />                           {/* py-20 bg-primary text-primary-foreground */}
</main>
<Footer />
```

**Dashboard:**
```tsx
<SidebarProvider>
  <Sidebar>{/* navigation items */}</Sidebar>
  <main className="flex-1">
    <header>{/* toolbar, breadcrumbs */}</header>
    <div className="p-6">
      <div className="grid gap-4 md:grid-cols-3">{/* stat cards */}</div>
      <div className="mt-6">{/* data table or content */}</div>
    </div>
  </main>
</SidebarProvider>
```

**Auth Flow:**
```tsx
<div className="min-h-screen flex items-center justify-center bg-muted/30">
  <div className="w-full max-w-md">
    <SignInCard />  {/* or SignUpCard */}
  </div>
</div>
```

**Multi-page App Layout:**
```tsx
// app/layout.tsx
<html>
  <body>
    <Navbar />
    {children}
    <Footer />
  </body>
</html>
```

#### Spacing & Layout Rules
- Sections: `py-16 md:py-20 lg:py-24` (responsive vertical padding)
- Content width: `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`
- Card grids: `grid gap-4 sm:grid-cols-2 lg:grid-cols-3`
- Alternating section backgrounds: use `bg-background` and `bg-muted/50`

#### Dark Mode Setup
21st.dev components use CSS variables with `dark:` prefixes. Ensure:
```tsx
// In layout.tsx or providers
import { ThemeProvider } from "next-themes"

<ThemeProvider attribute="class" defaultTheme="system" enableSystem>
  {children}
</ThemeProvider>
```

Install next-themes: `npm install next-themes`

#### Font Setup
```tsx
import { Geist, Geist_Mono } from "next/font/google";
const geist = Geist({ variable: "--font-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-mono", subsets: ["latin"] });

<body className={`${geist.variable} ${geistMono.variable} font-sans antialiased`}>
```

### Phase 7: Customization & Refinement

After installing components, customize them to fit the project:

1. **Content** — Replace placeholder text, images, and links with real content
2. **Colors** — Choose brand color intentionally (see Color Selection below)
3. **Typography** — Ensure consistent font sizes and weights
4. **Spacing** — Align padding/margin with the rest of the page
5. **Animations** — Add or tune transitions using Tailwind or framer-motion
6. **Responsiveness** — Test at mobile, tablet, and desktop breakpoints

#### Color Selection (CRITICAL — Avoid AI Purple Bias)

AI models have a strong bias toward purple/violet as the default brand color. This is because purple dominates tech/AI branding (Figma, Notion AI, Copilot) and shadcn/ui examples. Using purple every time is an obvious AI fingerprint — like using the Sparkles icon.

**Rule: NEVER default to purple.** Choose colors based on the product type and industry:

| Product / Industry | Recommended Primary | Avoid |
|---|---|---|
| Finance / Banking | Deep blue (`oklch(0.45 0.15 250)`), Navy, Teal | Purple, Neon |
| Health / Wellness | Green (`oklch(0.55 0.18 155)`), Teal, Soft blue | Red, Purple |
| E-commerce / Retail | Orange (`oklch(0.65 0.2 50)`), Coral, Amber | Muted grays |
| Developer tools | Emerald (`oklch(0.55 0.17 160)`), Cyan, Slate | Purple (overused) |
| Creative / Design | Rose (`oklch(0.6 0.18 10)`), Amber, Indigo | Plain blue |
| Education | Blue (`oklch(0.5 0.16 250)`), Teal, Green | Neon, Dark themes |
| Food / Restaurant | Warm red (`oklch(0.55 0.22 25)`), Orange, Olive | Cold blues |
| AI / Writing tools | Teal (`oklch(0.55 0.12 195)`), Blue-green, Slate | Purple (cliché!) |
| Enterprise / B2B | Slate blue (`oklch(0.5 0.1 255)`), Navy, Steel | Bright neons |
| Social / Community | Coral (`oklch(0.6 0.17 25)`), Sky blue, Warm pink | Dull grays |

**If the user specifies a brand color, use it.** If not, pick from the table above — but NEVER purple unless the user explicitly asks for it.

**How to apply the chosen color:**
```css
/* globals.css — example with teal for an AI writing tool */
:root {
  --brand: oklch(0.55 0.12 195);  /* Teal, NOT purple */
}
```
Then use `bg-brand`, `text-brand`, `border-brand/30` etc. throughout the site. Update hero gradients, CTA buttons, icon backgrounds, and accent colors to match.

#### Hero Visual Quality Checklist

Hero sections make or break the first impression. After installing a hero component, ensure:

- **Heading contrast**: On colored/gradient backgrounds, use solid `text-foreground` instead of gradient-text effects (`bg-clip-text text-transparent`) which can be too faint
- **Background gradients**: Apply gradients directly on the section element (`bg-gradient-to-b from-[color] via-[color] to-white`) — don't layer decorative gradient divs behind opaque parents
- **Product mockups**: For SaaS sites, build a realistic inline mockup (editor, dashboard, chat) instead of using a placehold.co image. Include window chrome (red/yellow/green dots), sidebar, content area, and status indicators. This dramatically improves perceived quality.
- **CTA styling**: Use `rounded-xl`, visible shadows (`shadow-lg`), and brand colors. Add hover effects (`hover:-translate-y-0.5 transition-transform`)
- **Radial glow accents**: Add subtle radial gradients using `rgba()` colors (not oklch) for depth behind hero content
- **Avoid AI-cliché icons**: NEVER use Sparkles/Stars/Wand icons — they instantly signal "AI-generated." Use minimal alternatives: a pulsing dot indicator, a small "NEW" badge, or just well-styled text. The goal is to look like a senior human designer made it, not an AI.
- **Avoid AI-cliché colors**: NEVER default to purple/violet. Choose colors from the Color Selection table based on the product type. Purple is the #1 AI color bias.

#### CSS Variable Theming
```css
/* globals.css */
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 0 0% 3.9%;
    --primary: 0 0% 9%;
    --primary-foreground: 0 0% 98%;
    /* ... customize these to match brand */
  }
  .dark {
    --background: 0 0% 3.9%;
    --foreground: 0 0% 98%;
    /* ... dark variants */
  }
}
```

### Phase 8: Verification (THOROUGH)

This phase catches the bugs that ruin the user's first impression. Do not skip any step.

#### Step 1: Build passes
```bash
npm run build
```
Fix any TypeScript or build errors before proceeding.

#### Step 2: Visual inspection (MOST IMPORTANT)
Run `npm run dev` and **actually look at every section** of the page:

1. **Take a screenshot** or use preview_screenshot — look at the full page from top to bottom
2. Check for these common problems:
   - **Blank/white sections** — content exists in DOM but invisible? Check CSS variables, text color matches background
   - **Content overflow** — text or elements going off-screen to the right? Check container width, remove `text-center` or adjust `max-w`
   - **Giant blank spaces** — hero taking up too much vertical space? Reduce `min-h-screen` to `min-h-[80vh]`
   - **Misaligned sections** — some sections centered, others left-aligned? Normalize container classes
   - **Broken images** — placeholder URLs not loading? Replace with real images or remove

3. **Scroll through the entire page** — every section must be visible and properly styled

#### Step 3: Responsiveness
Test at 3 breakpoints using preview_resize or browser devtools:
- Mobile (375px): single column, readable text, no horizontal overflow
- Tablet (768px): proper grid transition
- Desktop (1280px): full layout as designed

#### Step 4: Interactions
- Click every button and link
- Test navbar dropdown/mobile menu
- Test any toggles or tabs

#### Step 5: Console check
No errors in browser console. Warnings about missing images or unused vars are acceptable.

**If any visual issue is found in Steps 2-3, fix it immediately before presenting to the user.** The most common fixes are: adjusting container width, fixing CSS variable colors, and reducing hero height.

## Advanced Patterns

### Component Dependency Chain
Some 21st.dev components depend on other components. The npx installer handles this automatically, but be aware:
- A `Dialog` component may install `Button` as a dependency
- If you've already customized `Button`, the dialog install might overwrite it
- Install from leaf components up, and keep track of what's been customized

### Mixing Authors Safely
When combining components from different authors:
1. Check that all use the same CSS variable naming (most shadcn-based ones do)
2. Normalize border-radius: pick one style and apply globally via CSS variables
3. Ensure animation timing is consistent (ease-in-out, duration-200)
4. Watch for conflicting Tailwind config extensions

### Building Component Variations
If 21st.dev doesn't have exactly what you need:
1. Find the closest match
2. Install it
3. Modify the source code directly (you own it!)
4. The component file is in your project — edit freely

## Updating Component Knowledge

**At the start of every build session**, refresh your knowledge of available components by browsing the relevant category pages on 21st.dev. The platform adds new components daily, so what was the best option last week might be surpassed by something better today.

This means: if you last browsed `https://21st.dev/s/hero` an hour ago, browse it again if you're starting a new build. Fresh data leads to better component choices.

## Error Recovery

| Problem | Solution |
|---------|----------|
| Component not found | Try alternative spellings, browse the parent category, or search with WebSearch |
| npx install fails | Check for missing peer deps, verify URL format, try `npm install` for deps first |
| Component looks wrong | Check if Tailwind config was updated, verify CSS variables are defined |
| Dark mode broken | Ensure ThemeProvider wraps the app, check CSS variable definitions |
| TypeScript errors | Check component's expected props, install missing @types packages |
| Styling conflicts | Check for conflicting Tailwind classes, CSS variable naming collisions |
| 21st.dev unreachable | Use WebSearch to find component names, construct install URLs from cached knowledge |
| Component too complex | Simplify by removing unused features from the source code |
| `render` prop errors | Component uses @base-ui/react pattern — convert to `asChild` pattern |
| Giant blank space | Hero/section using `min-h-screen` — reduce to `min-h-[80vh]` or remove |
| Content off-screen right | Container width mismatch — add `max-w-7xl mx-auto` wrapper |
| Invisible text | CSS variables undefined — check `globals.css` has all required color tokens |
| Faint/invisible cards | Background gradient too subtle — use `bg-card border border-border/60 shadow-sm` |
| Marquee cards hidden | Edge fade `w-1/3` too wide — reduce to `w-1/6` |
| Gradient not showing | Using `-z-10` behind parent `bg-background` — apply gradient directly on section |
| oklch gradient broken | oklch renders poorly in `radial-gradient()` — use `rgba()` hex values instead |
| Heading invisible on gradient | `bg-clip-text text-transparent` too faint — use solid `text-foreground` |

## MCP Setup (Optional)

For AI-powered component generation, set up the Magic MCP:

```bash
npx @21st-dev/cli@latest install claude --api-key <YOUR_API_KEY>
```

Get API key: https://21st.dev/settings/api-keys

Manual config in `.claude/settings.json`:
```json
{
  "mcpServers": {
    "@21st-dev/magic": {
      "command": "npx",
      "args": ["-y", "@21st-dev/magic@latest"],
      "env": { "API_KEY": "your-api-key" }
    }
  }
}
```

MCP provides these tools:
- `21st_magic_component_builder` — Generate components from descriptions
- `21st_magic_component_inspiration` — Browse component ideas
- `logo_search` — Find company logos (via SVGL)
