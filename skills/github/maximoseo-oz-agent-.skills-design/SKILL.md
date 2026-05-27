# UI/UX Design System Generation

AI-powered design intelligence for generating complete, tailored design systems. Analyzes project requirements and outputs pattern, style, colors, typography, effects, and anti-patterns.

**Source:** https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

## When to Use

- Starting a new UI project — generate a full design system before coding
- Choosing styles, colors, and fonts for a specific industry/product type
- Landing page design with conversion-focused patterns
- Ensuring accessibility (WCAG AA) and responsive design

## Design System Generation Process

1. **Analyze project requirements** — product type, target audience, industry
2. **Multi-domain search** — match across patterns (24), styles (67), colors (161), fonts (57)
3. **Reasoning engine** — apply industry-specific rules, filter anti-patterns
4. **Output complete system** — pattern + style + colors + typography + effects + checklist

## Style Categories (67 Total)

### General Styles
- **Minimalism & Swiss Style** — Enterprise, dashboards, documentation
- **Glassmorphism** — Modern SaaS, financial dashboards
- **Brutalism** — Design portfolios, artistic projects
- **Neumorphism** — Health/wellness, meditation apps
- **Claymorphism** — Educational, children's apps, SaaS
- **Aurora UI** — Modern SaaS, creative agencies
- **Dark Mode (OLED)** — Night-mode apps, coding platforms
- **Motion-Driven** — Portfolio sites, storytelling
- **Bento Grid** — Dashboards, feature showcases
- **Liquid Glass** — Premium SaaS, high-end e-commerce

### Industry-Specific Rules (161 Categories)
- **Tech & SaaS:** Developer tools, AI platforms, cybersecurity
- **Finance:** Fintech, banking, insurance — conservative palettes, trust signals
- **Healthcare:** Medical, dental, mental health — calming, accessible
- **E-commerce:** Luxury, marketplace, subscription — conversion-focused
- **Services:** Beauty/spa, restaurants, hotels — emotion-driven
- **Creative:** Portfolio, agency, photography — expressive, bold
- **Lifestyle:** Habit tracker, recipes, meditation — warm, organic

Each rule includes: recommended pattern, style priority, color mood, typography mood, key effects, anti-patterns to avoid.

## Font Pairings (57 Combinations)

Match typography mood to product type:
- **Elegant/Sophisticated:** Cormorant Garamond / Montserrat
- **Modern/Clean:** Plus Jakarta Sans / Inter
- **Bold/Impactful:** Space Grotesk / DM Sans
- **Playful/Friendly:** Fredoka / Nunito
- **Professional/Corporate:** IBM Plex Sans / Source Sans Pro

## Landing Page Patterns (24)

- **Hero-Centric + Social Proof** — Emotion-driven with trust elements
- **Problem-Solution** — Pain point → transformation
- **Feature Grid** — Multiple features with visual hierarchy
- **Story-Driven** — Narrative scroll with progressive disclosure
- **Pricing-First** — Direct comparison with clear CTAs

## Pre-Delivery Checklist

- No emojis as icons (use SVG: Heroicons/Lucide)
- `cursor-pointer` on all clickable elements
- Hover states with smooth transitions (150-300ms)
- Text contrast 4.5:1 minimum (WCAG AA)
- Focus states visible for keyboard navigation
- `prefers-reduced-motion` respected
- Responsive breakpoints: 375px, 768px, 1024px, 1440px

## Tech Stack Support

React, Next.js, Astro, Vue, Nuxt, Svelte, SwiftUI, React Native, Flutter, HTML+Tailwind, shadcn/ui, Angular, Laravel

## Anti-Patterns to Always Avoid

- AI purple/pink gradients (overused, generic)
- Same design across different projects
- Emojis instead of proper SVG icons
- Missing hover/focus states
- Ignoring accessibility standards
