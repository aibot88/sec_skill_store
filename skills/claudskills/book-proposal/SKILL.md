---
name: book-proposal
description: Generate a publisher-ready book proposal from your content archive — title, chapter outline, market analysis, author platform, sample chapter, and competitive analysis. Prove that your content is already a book waiting to be organized.
---

# Book Proposal Generator

Your content archive is a manuscript draft. This skill turns it into a publisher-ready proposal.

## When to Activate

- User says `/book-proposal` or `/book`
- User asks "could I write a book from my content?"
- User wants to approach a publisher

## Commands

### `/book` — Analyze archive and generate proposal
### `/book {topic}` — Proposal for specific topic
### `/book sample-chapter {N}` — Generate a sample chapter

## Workflow

### Step 1: Archive-to-Book Analysis

```
Book Potential: Your content maps to {N} possible books

Top candidate: "{Book Title}"
  Source articles: {N} articles covering this theme
  Estimated manuscript: ~{N} chars (~{pages} pages)
  Gaps to fill: {N} chapters need new content
  Unique angle: "{what makes YOUR book different}"
```

### Step 2: Generate Proposal

```markdown
# Book Proposal: "{Title}"

## Overview
{2-3 paragraph pitch — what the book is about and why now}

## Target Reader
{Specific reader profile — who buys this book}

## Market Analysis
{Market size, comparable titles, positioning}
  Comp 1: "{title}" by {author} — {how yours differs}
  Comp 2: "{title}" by {author} — {differentiation}
  Comp 3: "{title}" by {author} — {gap you fill}

## Author Platform
  note followers: {N}
  X followers: {N}
  Monthly content reach: {N}
  Email subscribers: {N}
  Published articles: {N}
  Expertise: {credentials from profile}

## Chapter Outline
  Ch 1: "{title}" — {summary} [based on: {article}]
  Ch 2: "{title}" — {summary} [based on: {articles}]
  ...
  Ch 10: "{title}" — {summary} [NEW — to be written]

## Sample Chapter
{Full chapter generated from best-performing article cluster}

## Timeline
  Manuscript completion: {estimate based on gap analysis}

## Marketing Plan
  {How you'll promote using your existing platforms}
```

## Quality Gate

- [ ] Proposal follows industry-standard format
- [ ] Market analysis based on real competitive research
- [ ] Author platform numbers are accurate
- [ ] Chapter outline is coherent (not just article list)
- [ ] Sample chapter is polished book-quality writing
