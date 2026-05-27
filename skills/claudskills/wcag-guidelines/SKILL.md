---
name: ux-developer-wcag-guidelines
description: "WCAG 2.2 accessibility guidelines reference for web development. WCAG 2.2無障礙指南速查：POUR四原則、A/AA/AAA準則、代碼示例。 Use when: accessibility audit, new feature design, pre-launch compliance check."
disable-model-invocation: true
---

# WCAG 2.2 Guidelines Reference

構建包容性網絡體驗之無障礙指南。

## WCAG Principles: POUR

### Perceivable
信息須以用戶可感知之方式呈現。

### Operable
界面組件須可操作。

### Understandable
信息與UI操作須可理解。

### Robust
內容須足夠健壯，適配各類用戶代理與輔助技術。

---

## Level A (Minimum)

### 1.1 Text Alternatives

**1.1.1 Non-text Content**
非文本內容須有文本替代。

```html
<!-- Images -->
<img src="chart.png" alt="Sales increased 25% in Q4 2024">

<!-- Decorative images -->
<img src="divider.png" alt="" role="presentation">

<!-- Complex images -->
<figure>
  <img src="diagram.png" alt="System architecture overview">
  <figcaption>Detailed description of the architecture...</figcaption>
</figure>

<!-- Icons with meaning -->
<button>
  <svg aria-hidden="true">...</svg>
  <span class="sr-only">Delete item</span>
</button>
```

### 1.3 Adaptable

**1.3.1 Info and Relationships**
呈現所傳達之結構，可程序化獲取。

```html
<!-- Use semantic HTML -->
<nav aria-label="Main navigation">...</nav>
<main>...</main>
<aside>...</aside>

<!-- Proper heading hierarchy -->
<h1>Page Title</h1>
  <h2>Section</h2>
    <h3>Subsection</h3>

<!-- Data tables -->
<table>
  <caption>Monthly Sales</caption>
  <thead>
    <tr><th scope="col">Month</th><th scope="col">Sales</th></tr>
  </thead>
  <tbody>...</tbody>
</table>
```

**1.3.2 Meaningful Sequence**
閱讀順序合乎邏輯。

**1.3.3 Sensory Characteristics**
指示不唯賴形狀、大小、位置或聲音。

```html
<!-- Bad -->
<p>Click the round button on the right</p>

<!-- Good -->
<p>Click the "Submit" button to continue</p>
```

### 1.4 Distinguishable

**1.4.1 Use of Color**
顏色非傳達信息之唯一手段。

```html
<!-- Bad: color only -->
<span style="color: red">Error</span>

<!-- Good: color + icon + text -->
<span class="error">
  <svg aria-hidden="true">...</svg>
  Error: Please enter a valid email
</span>
```

### 2.1 Keyboard Accessible

**2.1.1 Keyboard**
所有功能可由鍵盤操作。

```html
<!-- Ensure custom controls are focusable and operable -->
<div role="button" tabindex="0"
     onkeydown="handleKeyDown(event)"
     onclick="handleClick()">
  Custom Button
</div>
```

**2.1.2 No Keyboard Trap**
焦點可由鍵盤移離任何組件。

### 2.4 Navigable

**2.4.1 Bypass Blocks**
跳過重複內容塊。

```html
<a href="#main-content" class="skip-link">Skip to main content</a>
```

**2.4.2 Page Titled**
頁面有描述性標題。

```html
<title>Product Details - My Store</title>
```

**2.4.3 Focus Order**
焦點順序保持意義與可操作性。

**2.4.4 Link Purpose (In Context)**
鏈接目的可由鏈接文字或上下文判定。

```html
<!-- Bad -->
<a href="/article">Read more</a>

<!-- Good -->
<a href="/article">Read more about accessibility guidelines</a>
```

### 3.1 Readable

**3.1.1 Language of Page**
頁面默認語言可程序化判定。

```html
<html lang="en">
```

### 4.1 Compatible

**4.1.2 Name, Role, Value**
自定義UI組件暴露名稱、角色與狀態。

```html
<button aria-expanded="false" aria-controls="menu">
  Menu
</button>
<ul id="menu" hidden>...</ul>
```

---

## Level AA (Target for Most Sites)

### 1.4 Distinguishable

**1.4.3 Contrast (Minimum)**
- Text: 4.5:1 contrast ratio
- Large text (18pt+): 3:1 contrast ratio

**1.4.4 Resize Text**
文字可縮放至200%而不失功能。

**1.4.5 Images of Text**
用真實文字，勿用文字圖片。

**1.4.10 Reflow**
內容在320px寬度下重排，無需水平滾動。

**1.4.11 Non-text Contrast**
UI組件與圖形具3:1對比度。

**1.4.12 Text Spacing**
調整文字間距後不失內容。

**1.4.13 Content on Hover or Focus**
懸停/焦點出現之附加內容可關閉、可懸停、持久存在。

### 2.4 Navigable

**2.4.5 Multiple Ways**
提供多種方式定位站點內頁面。

**2.4.6 Headings and Labels**
標題與標籤描述主題或目的。

**2.4.7 Focus Visible**
鍵盤焦點指示器可見。

```css
:focus {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

/* Never do this without replacement */
/* :focus { outline: none; } */
```

### 2.5 Input Modalities

**2.5.3 Label in Name**
可訪問名稱含可見標籤文字。

```html
<!-- Visible label: "Search" -->
<!-- Accessible name must include "Search" -->
<input type="search" aria-label="Search products">
```

### 3.2 Predictable

**3.2.3 Consistent Navigation**
導航在頁面間保持一致。

**3.2.4 Consistent Identification**
相同功能組件一致標識。

### 3.3 Input Assistance

**3.3.1 Error Identification**
錯誤以文字識別並描述。

**3.3.2 Labels or Instructions**
用戶輸入提供標籤或指示。

**3.3.3 Error Suggestion**
已知時建議修正方法。

**3.3.4 Error Prevention (Legal, Financial, Data)**
提交可撤銷、核查或確認。

---

## Level AAA (Enhanced)

值得關注之AAA準則：

**1.4.6 Contrast (Enhanced)**: 文字7:1，大文字4.5:1

**2.4.9 Link Purpose (Link Only)**: 鏈接目的可由鏈接文字單獨判定

**3.1.5 Reading Level**: 內容可供初中教育水平閱讀

---

## Quick Reference Checklist

### Before Development
- [ ] Design reviewed for color contrast
- [ ] Semantic HTML structure planned
- [ ] Keyboard interaction patterns defined
- [ ] Error states designed accessibly

### During Development
- [ ] Semantic HTML used correctly
- [ ] ARIA only when HTML insufficient
- [ ] Focus management implemented
- [ ] Form labels properly associated
- [ ] Alt text for all meaningful images
- [ ] Skip links implemented
- [ ] Language attribute set

### Before Launch
- [ ] Automated accessibility audit passes
- [ ] Keyboard-only navigation tested
- [ ] Screen reader tested (NVDA/VoiceOver)
- [ ] Zoom to 200% tested
- [ ] Color contrast verified
- [ ] Form error handling tested

---

## Testing Tools

**Automated**:
- axe DevTools (browser extension)
- Lighthouse Accessibility
- WAVE (webaim.org/wave)
- pa11y (CLI)

**Manual**:
- Keyboard navigation testing
- Screen reader testing (NVDA, VoiceOver, JAWS)
- Browser zoom testing
- Color contrast analyzers

**agnt Integration**:
```javascript
// Run accessibility audit via agnt proxy
__devtool.auditAccessibility()
```
