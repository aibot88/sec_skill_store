---
name: presentation-master
description: "Create beautiful HTML presentations from topic + authors. Generates slides + speaker notes. No dependencies, works offline."
aliases:
  - presentation
  - create presentation
  - make presentation
---

# Presentation Master — Workflow Guide

## Quick Reference

**Input:** Topic + Author names  
**Output:** 2 HTML files (slides + speech notes)  
**Style:** Study `examples/` folder for quality reference  
**Language:** Match user's language

---

## Essential Requirements

### 1. Layout Rules

```css
/* CRITICAL: No scrolling on slides */
.slide {
    overflow: hidden;
    padding: 40px 60px 80px 60px; /* bottom padding for nav */
}
```

**Why 80px bottom padding?** Navigation buttons sit at bottom — content must not overlap them.

### 2. Navigation Pattern

```
┌─────────────────────────────────────┐
│                                     │
│           SLIDE CONTENT             │
│                                     │
│                                     │
├─────────────────────────────────────┤
│  [1/15]                    [◄] [►]  │  ← Nav area (~60px)
└─────────────────────────────────────┘
   ↑ Counter                  ↑ Buttons
   bottom-left               bottom-right
```

**Key:** Counter on left, buttons on right. Both fixed position, ~24-30px from edges.

### 3. Content Density

Since slides can't scroll, content must be **compact**:

| Element | Recommended Size |
|---------|------------------|
| h1 (title) | 2.5-3.5rem |
| h2 (slide heading) | 1.75-2rem |
| h3 (card heading) | 1-1.2rem |
| Body text | 0.85-0.95rem |
| Card padding | 1-1.5rem |
| Grid gaps | 0.75-1.25rem |

**Tip:** Use grids (2-4 columns) to fit more content horizontally.

---

## Slide Structure

### Recommended: 14-22 slides

```
Slide 1:  Title (topic + authors)
Slide 2:  Overview/Agenda
Slides 3-N: Content (mix of types)
Slide N-1: Summary/Key Takeaways  
Slide N:  Thank You
```

### Slide Types to Mix

| Type | Use For | Layout |
|------|---------|--------|
| Title | Opening, section dividers | Centered, gradient bg |
| Content | Main ideas | Heading + bullets/cards |
| Grid | Multiple concepts | 2-4 column card grid |
| Comparison | Pros/cons, before/after | 2-column layout |
| Stats | Key numbers | Large numbers + labels |
| Quote | Expert opinion | Blockquote style |
| Timeline | History, process | Vertical/horizontal steps |

---

## Visual Design

### Default Style

Study `examples/` — they show the quality bar:
- **Dark backgrounds** with colored accents
- **Glass/gradient cards** with subtle borders
- **Smooth animations** (fade, slide)
- **Icon usage** for visual interest

### Key Visual Elements

Every content slide should include:
- Cards or containers (not bare lists)
- Color accents or icons
- Clear visual hierarchy
- Adequate spacing

### Animation Classes

```css
.animate-in {
    opacity: 0;
    transform: translateY(20px);
}

.slide.active .animate-in {
    animation: fadeUp 0.5s ease forwards;
}

.delay-1 { animation-delay: 0.1s; }
.delay-2 { animation-delay: 0.2s; }
.delay-3 { animation-delay: 0.3s; }
```

---

## Technical Implementation

### HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{Topic}</title>
    <style>
        /* All CSS inline */
    </style>
</head>
<body>
    <!-- Background effects (optional) -->
    <div class="bg-effects">...</div>
    
    <!-- Progress bar -->
    <div class="progress-bar" id="progress"></div>
    
    <!-- Slides -->
    <div class="slides-container">
        <div class="slide active" data-slide="1">...</div>
        <div class="slide" data-slide="2">...</div>
        <!-- ... more slides ... -->
    </div>
    
    <!-- Navigation: counter left, buttons right -->
    <div class="slide-counter">
        <span id="currentSlide">1</span> / <span id="totalSlides">N</span>
    </div>
    
    <nav class="nav-container">
        <button class="nav-btn" onclick="prevSlide()">◄</button>
        <button class="nav-btn" onclick="nextSlide()">►</button>
    </nav>
    
    <script>
        /* Navigation logic */
    </script>
</body>
</html>
```

### Navigation JavaScript

```javascript
let currentSlide = 1;
const totalSlides = N; // Set actual count
const slides = document.querySelectorAll('.slide');

function showSlide(n) {
    if (n < 1) n = 1;
    if (n > totalSlides) n = totalSlides;
    
    slides.forEach(slide => slide.classList.remove('active'));
    slides[n - 1].classList.add('active');
    currentSlide = n;
    
    document.getElementById('currentSlide').textContent = currentSlide;
    document.getElementById('prevBtn').disabled = currentSlide === 1;
    document.getElementById('nextBtn').disabled = currentSlide === totalSlides;
    document.getElementById('progress').style.width = 
        ((currentSlide / totalSlides) * 100) + '%';
}

function nextSlide() { showSlide(currentSlide + 1); }
function prevSlide() { showSlide(currentSlide - 1); }

// Keyboard support
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ') { 
        e.preventDefault(); 
        nextSlide(); 
    }
    if (e.key === 'ArrowLeft') { 
        e.preventDefault(); 
        prevSlide(); 
    }
});

// Touch/swipe support
let touchStartX = 0;
document.addEventListener('touchstart', (e) => { 
    touchStartX = e.touches[0].clientX; 
});
document.addEventListener('touchend', (e) => {
    const diff = touchStartX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 50) { 
        diff > 0 ? nextSlide() : prevSlide(); 
    }
});

showSlide(1);
```

---

## Speaker Notes Format

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Speech Notes — {Topic}</title>
    <style>
        body {
            font-family: system-ui, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px;
            line-height: 1.7;
        }
        .slide-notes {
            margin-bottom: 2rem;
            padding: 1.5rem;
            border-left: 4px solid #3b82f6;
            background: #f8fafc;
        }
        .slide-number {
            font-weight: bold;
            color: #3b82f6;
        }
        .slide-title {
            font-size: 1.2rem;
            font-weight: 600;
            margin: 0.5rem 0;
        }
        .duration {
            font-size: 0.85rem;
            color: #64748b;
        }
    </style>
</head>
<body>
    <h1>Speech Notes</h1>
    <p class="subtitle">{Topic}</p>
    
    <div class="slide-notes">
        <span class="slide-number">Slide 1</span>
        <span class="duration">~30 sec</span>
        <div class="slide-title">Title Slide</div>
        <p>Opening remarks...</p>
        <p>Introduction to topic...</p>
    </div>
    
    <!-- Repeat for each slide -->
    
    <div class="total-time">
        Total: ~15-20 min
    </div>
</body>
</html>
```

---

## Content Guidelines

### Do's
- ✓ One main idea per slide
- ✓ Concrete examples (not abstract statements)
- ✓ Visual structure (cards, grids, icons)
- ✓ Logical flow between slides
- ✓ Natural speaker notes (conversational)

### Don'ts
- ✗ Scrolling content
- ✗ Walls of text
- ✗ Generic filler ("This is important...")
- ✗ Made-up statistics
- ✗ External dependencies

---

## Reference: Study Examples

The `examples/` folder contains production-quality presentations:

| File | Style | Learn From |
|------|-------|-----------|
| Artificial Intelligence.html | Dark glass | Animations, grids, timeline |
| Climate Change.html | Light professional | Cards, stats, clean layout |
| Cybersecurity.html | Neon/gaming | Particles, threat meters, glow |

**Best practice:** Open examples in browser, study their CSS patterns, adapt to your topic.

---

## Checklist Before Completion

- [ ] Content fits without scrolling
- [ ] Navigation visible and doesn't overlap content
- [ ] All slides have visual structure (not plain text)
- [ ] Facts are accurate
- [ ] Speech notes cover every slide
- [ ] Works offline (no external deps)
- [ ] Keyboard navigation works
- [ ] Touch/swipe works

---

**Remember:** The examples/ folder is your quality reference. Be creative, but maintain that level of polish.
