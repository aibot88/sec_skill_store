---
name: aso-visuals
description: >
  Visual asset analysis for app store listings. Screenshots, app icon, preview
  videos. Evaluates composition, narrative flow, text readability, platform
  compliance, and conversion impact.
  Triggers on: "screenshots", "icon", "preview video", "visual assets".
user-invokable: true
argument-hint: "<app-id> [--platform ios|android]"
---

# ASO Visuals — Visual Asset Analysis

## Capabilities
1. Screenshot count and device coverage assessment
2. First-3-screenshot impact analysis (iOS critical zone)
3. Text overlay and caption readability check
4. App icon evaluation (distinctiveness, small-size readability)
5. Preview video presence and spec compliance
6. Narrative flow across screenshot sequence
7. Feature graphic analysis (Android only)

## Process

1. Fetch listing data and extract screenshot URLs
2. Analyze screenshots via `scripts/screenshot_analyzer.py`
3. Evaluate against platform specs from `references/visual-asset-specs.md`
4. Score each visual asset category

## Scoring (0-100)

| Factor | Weight | What to check |
|--------|--------|--------------|
| Screenshot count | 20% | iOS: 10 max, Android: 8 max. At least 5 recommended. |
| First 3 screenshots | 25% | Clear value prop, hook, core features (iOS: visible in search) |
| Narrative flow | 15% | Screenshots tell a coherent story |
| Text/captions | 15% | Readable at thumbnail size, localized, keyword-bearing (iOS OCR) |
| Icon quality | 15% | Recognizable at 29x29, strong silhouette, no text |
| Video presence | 10% | Preview video exists and meets specs |

## Screenshot Narrative Analysis

Evaluate the sequence:
1. **Position 1 (Hook)**: Does it immediately communicate core value?
2. **Position 2-3 (Core)**: Do they show primary features/use cases?
3. **Position 4-6 (Support)**: Secondary features, differentiators?
4. **Position 7+ (Proof)**: Social proof, awards, additional features?

## Platform-Specific Checks

### iOS
- Screenshot dimensions match required device sizes
- At least iPhone 6.7" or 6.9" screenshots present
- iPad screenshots present (if universal app)
- App preview video: 15-30s, actual app footage, correct resolution
- Caption text: keep it readable, benefit-led, and localized

### Android
- Screenshots meet 320px min, 3840px max
- Feature graphic present (1024x500)
- Promotional video: YouTube URL provided
- Minimum 2 screenshots (Google Play requirement)

## Output Format

```markdown
# Visual Asset Report: [App Name]

## Score: XX/100

## Screenshots (X/10 or X/8)
[Per-screenshot analysis with position recommendations]

## App Icon
[Distinctiveness, small-size readability assessment]

## Preview Video
[Present/absent, spec compliance, content quality]

## Feature Graphic (Android)
[Present/absent, design quality]

## Recommendations
[Prioritized list of visual improvements]
```

## Available Tools
Read, Bash, Write, Glob, Grep
