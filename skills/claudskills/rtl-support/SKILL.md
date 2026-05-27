---
name: rtl-support
description: >-
  Add right-to-left (RTL) text support to web projects for Hebrew, Arabic, and Farsi.
  Use when the user asks about RTL layout, Hebrew/Arabic text direction, bidirectional
  text, CSS direction, unicode-bidi, or wants to make a web app support RTL languages.
  Provides automatic direction detection, CSS injection, and JavaScript utilities.
license: MIT
compatibility: Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex.
metadata:
  author: skills-il
  version: 1.0.0
  category: localization
  tags:
    he:
    - RTL
    - עברית
    - ערבית
    - כיוון-טקסט
    - לוקליזציה
    - נגישות
    en:
    - rtl
    - hebrew
    - arabic
    - text-direction
    - localization
    - bidi
    - unicode
  display_name:
    he: תמיכה ב-RTL
    en: RTL Support
  display_description:
    he: >-
      הוספת תמיכה בכתיבה מימין לשמאל לפרויקטי ווב עבור עברית, ערבית ופרסית.
      כולל זיהוי כיוון אוטומטי, הזרקת CSS ועזרי JavaScript.
    en: >-
      Add right-to-left text support to web projects for Hebrew, Arabic, and Farsi.
      Includes automatic direction detection, CSS injection, and JavaScript utilities.
  supported_agents:
  - claude-code
  - cursor
  - github-copilot
  - windsurf
  - opencode
  - codex
---

# RTL Support

RTL (Right-to-Left) support enables correct rendering of Hebrew (עברית), Arabic (العربية), and Farsi (فارسی) text in web applications. The key is automatic direction detection per element while preserving LTR for code blocks.

## Unicode RTL Ranges

| Script | Range | Example |
|--------|-------|---------|
| Hebrew | U+0590–U+05FF | עברית |
| Arabic | U+0600–U+06FF | العربية |
| Arabic Supplement | U+0750–U+077F | ݐ |
| Arabic Extended-A | U+08A0–U+08FF | ࢠ |

## Core JavaScript Detection

```javascript
function isRTL(c) {
  var code = c.charCodeAt(0);
  return (code >= 0x0590 && code <= 0x05FF) ||
         (code >= 0x0600 && code <= 0x06FF) ||
         (code >= 0x0750 && code <= 0x077F) ||
         (code >= 0x08A0 && code <= 0x08FF);
}

function hasRTL(text) {
  if (!text) return false;
  for (var i = 0; i < text.length; i++) {
    if (isRTL(text[i])) return true;
  }
  return false;
}

function firstStrong(text) {
  if (!text) return null;
  for (var i = 0; i < text.length; i++) {
    if (isRTL(text[i])) return 'rtl';
    if (/[a-zA-Z]/.test(text[i])) return 'ltr';
  }
  return null;
}

function detectTextDir(text) {
  if (!text || !text.trim()) return null;
  var d = firstStrong(text);
  if (d === 'rtl') return 'rtl';
  if (!hasRTL(text)) return 'ltr';
  // Strip leading LTR characters and re-check
  var stripped = text.replace(/^[^א-תa-zA-Z\u0600-\u06FF]*/, '');
  return firstStrong(stripped) === 'rtl' ? 'rtl' : 'ltr';
}
```

## CSS Injection

```javascript
function injectRTLStyles() {
  if (document.getElementById('rtl-styles')) return;
  var s = document.createElement('style');
  s.id = 'rtl-styles';
  s.textContent = [
    // Auto-bidi for text elements
    'p:not([dir]),li:not([dir]),h1:not([dir]),h2:not([dir]),h3:not([dir]),' +
    'h4:not([dir]),h5:not([dir]),h6:not([dir]),blockquote:not([dir]),' +
    'td:not([dir]),th:not([dir]),label:not([dir]),' +
    'dt:not([dir]),dd:not([dir])' +
    '{unicode-bidi:plaintext!important;text-align:start!important}',

    // Force code blocks to LTR
    'pre,code,.code-block' +
    '{unicode-bidi:embed!important;direction:ltr!important;text-align:left!important}',

    // Honour explicit dir attributes
    '[dir]{text-align:start!important}' +
    '[dir="rtl"]{direction:rtl!important}' +
    '[dir="ltr"]{direction:ltr!important}',
  ].join('');
  document.head.appendChild(s);
}
```

## Auto-Detection Observer

```javascript
function applyDirToElement(el) {
  // Skip code blocks
  if (el.matches('pre,code,.code-block')) return;
  var text = el.textContent || '';
  if (!text.trim()) return;
  var dir = detectTextDir(text);
  if (dir) el.setAttribute('dir', dir);
}

function observeDOM(rootSelector) {
  injectRTLStyles();
  var root = document.querySelector(rootSelector) || document.body;

  // Apply to existing elements
  root.querySelectorAll('p,li,h1,h2,h3,h4,h5,h6,td,th,label,blockquote')
      .forEach(applyDirToElement);

  // Watch for new content
  var observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(m) {
      m.addedNodes.forEach(function(node) {
        if (node.nodeType !== 1) return;
        applyDirToElement(node);
        node.querySelectorAll('p,li,h1,h2,h3,h4,h5,h6,td,th,label,blockquote')
            .forEach(applyDirToElement);
      });
    });
  });
  observer.observe(root, { childList: true, subtree: true });
  return observer;
}
```

## React Hook

```tsx
import { useEffect } from 'react';

function useRTLDirection(ref: React.RefObject<HTMLElement>) {
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const text = el.textContent || '';
    const hasHebrew = /[\u0590-\u05FF]/.test(text);
    const hasArabic = /[\u0600-\u06FF]/.test(text);
    if (hasHebrew || hasArabic) {
      el.setAttribute('dir', 'rtl');
      el.style.textAlign = 'right';
    } else {
      el.setAttribute('dir', 'ltr');
      el.style.textAlign = 'left';
    }
  }, [ref]);
}
```

## CSS-Only Approach (Modern Browsers)

```css
/* Use unicode-bidi: plaintext on content containers */
.content {
  unicode-bidi: plaintext;
  text-align: start;
}

/* Force code blocks LTR */
pre, code {
  direction: ltr;
  unicode-bidi: embed;
  text-align: left;
}
```

## HTML Best Practices

```html
<!-- Page-level RTL (for fully RTL pages) -->
<html lang="he" dir="rtl">

<!-- Mixed content — let browser detect per paragraph -->
<p style="unicode-bidi: plaintext; text-align: start;">
  שלום! Hello!
</p>

<!-- Explicit override -->
<p dir="rtl">טקסט בעברית</p>
<p dir="ltr">English text</p>
```

## Framework Integration

### Next.js / React

```tsx
// app/layout.tsx — detect locale and set dir
export default function RootLayout({ children, params: { locale } }) {
  const dir = ['he', 'ar', 'fa'].includes(locale) ? 'rtl' : 'ltr';
  return (
    <html lang={locale} dir={dir}>
      <body>{children}</body>
    </html>
  );
}
```

### Vue 3

```vue
<template>
  <div :dir="textDir">{{ content }}</div>
</template>

<script setup>
import { computed } from 'vue';
const props = defineProps({ content: String });
const textDir = computed(() =>
  /[\u0590-\u05FF\u0600-\u06FF]/.test(props.content) ? 'rtl' : 'ltr'
);
</script>
```

## Examples

### Example 1: Add RTL to an existing web page
User says: "My Hebrew text is showing left-aligned, fix it"
Actions:
1. Add `dir="rtl"` to the `<html>` tag if the whole page is Hebrew
2. Or inject the CSS + observer script for mixed content
3. Wrap code blocks with explicit `dir="ltr"`
Result: Hebrew text aligns right, code stays left-aligned

### Example 2: React app with Hebrew and English mixed content
User says: "My chat app needs to support both Hebrew and English messages"
Actions:
1. Apply `useRTLDirection` hook to each message bubble component
2. Add CSS: `unicode-bidi: plaintext; text-align: start` on message elements
3. Force `.code-block { direction: ltr }`
Result: Each message auto-detects its direction independently

## Troubleshooting

### Hebrew text appears LTR
Cause: Missing `dir` attribute or `direction: ltr` override higher in the DOM
Solution: Add `unicode-bidi: plaintext` and ensure no ancestor has `direction: ltr` without `unicode-bidi: isolate`

### Punctuation appears on wrong side
Cause: Unicode Bidirectional Algorithm misidentifying neutral characters
Solution: Wrap text in `<bdi>` tags or add explicit `dir` attribute

### Code blocks showing RTL
Cause: RTL direction inherited from parent
Solution: Add `direction: ltr; unicode-bidi: embed` explicitly to `pre` and `code` elements
