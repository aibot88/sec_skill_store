---
name: competitor-analysis
version: 1.0.0
description: |
  Comprehensive competitor SEO & content analysis tool. Analyzes competitor websites, 
  identifies keywords, content gaps, backlink strategies, and ranking opportunities. 
  Accepts sitemaps for deep analysis. Supports 3 output formats: detailed reports (Opus 4.6+ with adaptive thinking), 
  quick findings (Sonnet 4.6+), and competitive comparisons (any model 4.0+). 
  Use when: analyzing competitor strategy, finding content gaps, identifying keyword opportunities, 
  benchmarking your SEO performance.
allowed-tools:
  - Web search
  - Web fetch
  - Data analysis
compatibility: Works with any Claude 3.5+ model (Opus 4.6 recommended for detailed analysis)
---

# competitor-analysis — Competitor SEO & Content Strategy Tool
## By mhuzaifaariz

Analyze competitor websites in depth. Find keywords they rank for, content gaps you can exploit, backlink strategies, and SEO opportunities. Use sitemap data for comprehensive analysis.

---

## 🚀 Quick Start (3 Steps)

### Step 1: Provide Competitor Info
```
Competitor name: [Company]
Website: [URL]
Sitemap: [Paste URL or content]
Industry: [CCTV, SaaS, Security, etc.]
```

### Step 2: Choose Analysis Type
```
1. Detailed Report (Opus 4.6 + adaptive thinking)
2. Quick Findings (Sonnet 4.6)
3. Competitive Comparison (your site vs theirs)
```

### Step 3: Get Results
- Detailed: 3,000+ word deep analysis + recommendations
- Quick: 1,000 word summary + top insights
- Comparison: Side-by-side metrics + gaps

---

## 📋 What Gets Analyzed

### **1. Keywords & Rankings**
- Keywords they rank for (position 1-20 in search)
- Search volume + difficulty
- Keywords you're NOT ranking for (opportunity gaps)
- Long-tail keyword opportunities
- Seasonal keyword trends

### **2. Content Strategy**
- Blog post topics + structure
- Content types (how-to, case studies, buyer guides, etc.)
- Content frequency (how often they publish)
- Top-performing pages (by traffic signals)
- Content calendar patterns
- Keyword density per page

### **3. Backlink Profile**
- Total referring domains
- Top backlink sources
- Link types (guest posts, directory, citations, etc.)
- Domain authority of backlinks
- Anchor text distribution
- Competitor backlink opportunities (where to pitch)

### **4. Technical SEO**
- Core Web Vitals (if data available)
- Site speed analysis
- Mobile optimization
- URL structure
- Internal linking strategy
- Schema markup usage

### **5. Content Gaps**
- Topics they cover that you don't
- Topics you cover that they don't (your advantage)
- Underutilized keyword opportunities
- Content format gaps (missing video, infographics, etc.)
- FAQ section analysis

### **6. Competitive Positioning**
- Market positioning analysis
- Unique value propositions
- Target audience insights
- Messaging strategy
- Call-to-action patterns

---

## 📊 Input: How to Provide Competitor Data

### **Option A: Sitemap URL**
```
Paste their sitemap.xml URL:
https://example.com/sitemap.xml

System will fetch and analyze all pages listed.
```

### **Option B: Sitemap Content**
```
Paste sitemap XML directly:
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/blog/post-1</loc>
    <lastmod>2024-04-15</lastmod>
  </url>
  ...
</urlset>
```

### **Option C: Demo Data (Default)**
```
If no sitemap provided, system uses demo competitor data:
- Competitor: TechSecure (fictional CCTV monitoring company)
- Website: techsecure.example.com
- 50+ pages analyzed
- Full backlink profile included
- Content strategy breakdown
```

---

## 🎯 Output Format Selection

### **Format 1: Detailed Report** (Opus 4.6 + Adaptive Thinking)
**When to use:** Deep competitive analysis, strategic planning, market entry

**Model requirement:** Claude Opus 4.6 or higher WITH adaptive thinking enabled

**Output includes:**
- Executive summary (2 pages)
- Keywords analysis (top 50 keywords they rank for)
- Content gap analysis (detailed)
- Backlink strategy breakdown
- Technical SEO audit
- Competitive positioning matrix
- Top 10 opportunities + how to exploit
- 3-month action plan
- Benchmark metrics (your site vs theirs)

**Length:** 3,000-5,000 words

**Best for:** Strategic planning, presenting to clients/stakeholders, comprehensive market research

---

### **Format 2: Quick Findings** (Sonnet 4.6+)
**When to use:** Quick insights, content ideation, weekly monitoring

**Model requirement:** Claude Sonnet 4.6 or higher

**Output includes:**
- Top 10 keywords they rank for
- Top 5 content topics
- Top 3 backlink sources
- 5 content gap opportunities (you can create)
- 3 quick wins (easy to execute)
- 2-minute summary of strategy

**Length:** 1,000-1,500 words

**Best for:** Quick decisions, content planning, weekly competitive monitoring

---

### **Format 3: Competitive Comparison** (Any model 4.0+)
**When to use:** Benchmarking, understanding position, presentation to team

**Model requirement:** Any Claude 3.5+ model (4.0 or higher)

**Output includes:**
- Side-by-side comparison table:
  - Keywords you rank for but they don't
  - Keywords they rank for but you don't
  - Shared keywords (compare positions)
  - Content quantity comparison
  - Backlink count comparison
  - Domain authority comparison
- Strengths vs weaknesses matrix
- Quick wins for you
- Threats to watch

**Length:** 1,500-2,000 words

**Best for:** Team presentations, quick board updates, understanding competitive position

---

## 📈 Analysis Process

### **Step 1: Data Collection**
- Fetch sitemap (or use provided data)
- Extract all URLs
- Categorize by topic/content type
- Identify page structure

### **Step 2: Keyword Research**
- Search for competitor's top pages
- Extract ranking keywords
- Get search volume data
- Identify ranking positions
- Find keyword gaps (your site missing)

### **Step 3: Content Analysis**
- Analyze page structure (H1, H2, word count)
- Identify content types used
- Review topic clusters
- Assess content freshness
- Map content calendar patterns

### **Step 4: Backlink Analysis**
- Identify backlink sources
- Categorize link types
- Assess domain authority
- Review anchor text patterns
- Find backlink opportunities

### **Step 5: Gap Analysis**
- Compare your keywords vs theirs
- Identify missing content topics
- Find underutilized opportunities
- Spot format gaps (video, infographics, etc.)
- Recommend quick wins

### **Step 6: Recommendations**
- Top 10 keywords to target
- Content to create
- Backlink opportunities
- Technical improvements
- Positioning strategy

---

## 💡 Demo Data Example

**Default competitor (if no sitemap provided):**

```
Competitor: TechSecure CCTV Monitoring
Website: techsecure.example.com
Industry: CCTV & Video Surveillance

Top Keywords (Demo):
1. CCTV monitoring services (25K searches, position 3)
2. Remote CCTV monitoring (18K searches, position 5)
3. 24/7 live CCTV monitoring (12K searches, position 2)
4. CCTV system installation (8K searches, position 7)
5. Cybersecurity for CCTV (6K searches, position 4)

Top Content Topics:
- CCTV system setup guides (5 posts)
- Security best practices (8 posts)
- Case studies (3)
- Buyer guides (2)
- FAQ pages (4)

Backlinks:
- Total referring domains: 342
- Top sources:
  - SecurityBlog.com (28 links)
  - TechNews.io (21 links)
  - IndustryDirectory.org (15 links)
- Average DA: 42

Content Gaps (You could create):
- "CCTV vs NVR: Complete Comparison"
- "CCTV Cybersecurity Checklist"
- "Remote monitoring from mobile apps"
- "GDPR compliance for CCTV systems"
```

---

## 🔧 How to Use

### **Workflow: Analyze a Competitor**

```
User: /competitor-analysis

System:
1. Ask for competitor website URL
2. Ask if they have sitemap (optional)
3. Ask which output format:
   - Detailed (Opus 4.6 + adaptive)
   - Quick (Sonnet 4.6)
   - Comparison (any 4.0+)
4. Collect data
5. Run analysis
6. Generate report in selected format
```

### **Workflow: Compare Multiple Competitors**

```
User: /competitor-analysis batch

System:
1. Ask for 2-3 competitor URLs
2. Ask for output format
3. Analyze each competitor
4. Create comparison matrix
5. Identify which competitor is strongest
6. Provide consolidated recommendations
```

### **Workflow: Find Content Gaps**

```
User: /competitor-analysis gaps

System:
1. Ask for competitor URL
2. Ask for your website URL (optional)
3. Analyze competitor content
4. Compare with your content (if provided)
5. List all content gaps
6. Prioritize by opportunity (search volume + difficulty)
```

---

## 📊 Report Sections (Detailed Format)

### **1. Executive Summary**
- Competitor overview
- Top 3 threats
- Top 3 opportunities
- Recommended focus areas

### **2. Keyword Analysis**
- Top 50 keywords they rank for
- Your gaps (keywords they rank for, you don't)
- Their gaps (keywords you rank for, they don't)
- Opportunity scoring

### **3. Content Strategy**
- Content types breakdown (% by type)
- Top-performing topics
- Publishing frequency
- Content gaps
- Recommended content to create

### **4. Backlink Profile**
- Total referring domains
- Top 20 backlink sources
- Link type distribution
- Anchor text analysis
- Backlink opportunities (where to pitch)

### **5. Technical SEO**
- Core Web Vitals (if available)
- Site structure analysis
- Mobile optimization
- URL structure review
- Internal linking patterns

### **6. Competitive Positioning**
- Market positioning
- Messaging strategy
- Target audience analysis
- Unique selling points
- Positioning gaps (your advantage)

### **7. Opportunity Matrix**
- Ranked by:
  - Search volume
  - Difficulty
  - Relevance to your business
  - Quick-win potential

### **8. Action Plan**
- 30-day priorities
- 90-day roadmap
- Resource requirements
- Success metrics

---

## 🎨 Output Examples

### **Example 1: Keyword Gap Finding**
```
COMPETITIVE KEYWORD ANALYSIS

Their Top Keywords (You Don't Rank For):
1. "CCTV monitoring services" (25K searches, DA 45, Rank #3)
   → Opportunity: High search volume, moderate difficulty
   → Action: Create buyer guide + optimize for this keyword

2. "24/7 live CCTV monitoring" (12K searches, DA 38, Rank #2)
   → Opportunity: Exact match to your service offering
   → Action: Create dedicated landing page

Your Top Keywords (They Don't Rank For):
1. "Remote CCTV monitoring setup" (8K searches)
   → Your advantage: Leverage this gap
   → Action: Keep producing content on this topic

Shared Keywords (Compare Positions):
1. "CCTV system installation"
   → They rank: Position 7
   → You rank: Position 12
   → Gap: 5 positions behind
   → Action: Improve content, get backlinks to catch up
```

### **Example 2: Content Gap**
```
CONTENT GAP ANALYSIS

They Have (You Don't):
- "CCTV Cybersecurity Best Practices" (8,500 monthly views estimated)
- "GDPR Compliance for Video Surveillance" (4,200 views)
- "CCTV vs NVR Comparison Guide" (5,100 views)

Quick Wins (Create These First):
1. CCTV Cybersecurity Checklist (estimated 6,000 views/month)
2. GDPR Compliance Guide for CCTV (estimated 3,500 views/month)
3. CCTV vs NVR: Complete Comparison (estimated 4,500 views/month)

Content Type Gap:
- They have: 3 case studies, 2 webinars, 8 blog posts
- You have: 12 blog posts, 0 case studies, 0 webinars
- Action: Create 2-3 case studies + 1 webinar to diversify
```

### **Example 3: Backlink Strategy**
```
BACKLINK OPPORTUNITY ANALYSIS

Where They Get Links:
1. SecurityBlog.com (28 links, DA 58)
   → Strategy: Submit guest post about CCTV security
   → Angle: "How to Secure Your CCTV System"

2. TechNews.io (21 links, DA 51)
   → Strategy: Pitch news story about new monitoring features
   → Angle: "New approach to remote CCTV monitoring"

3. IndustryDirectory.org (15 links, DA 44)
   → Strategy: Get listed in directory (free/paid)
   → Action: Submit your site + description

Your Opportunity:
- Pitch same websites with different angles
- Create content these sites would link to
- Target 10+ links in first quarter
```

---

## 🎯 Commands Quick Reference

```
/competitor-analysis                      → Interactive (ask questions)
/competitor-analysis [URL]                → Analyze with demo format
/competitor-analysis [URL] detailed       → Detailed report (Opus 4.6+)
/competitor-analysis [URL] quick          → Quick findings (Sonnet 4.6+)
/competitor-analysis [URL] comparison     → Comparison to your site
/competitor-analysis batch [URL1] [URL2]  → Compare multiple competitors
/competitor-analysis gaps [URL]           → Content gaps only
/competitor-analysis keywords [URL]       → Keywords only
/competitor-analysis backlinks [URL]      → Backlinks only
/competitor-analysis demo                 → Show demo analysis (TechSecure)
```

---

## ⚙️ Model Selection Guide

| Format | Model | Why |
|--------|-------|-----|
| **Detailed Report** | Opus 4.6+ with adaptive thinking | Deep reasoning, complex analysis, strategic insights |
| **Quick Findings** | Sonnet 4.6+ | Fast processing, sufficient depth, cost-effective |
| **Comparison** | Any Claude 4.0+ | Simple comparison, tables, structured data |

---

## 📌 Best Practices

1. **Update quarterly** — Competitors change, re-analyze every 3 months
2. **Batch analyze** — Compare 2-3 competitors, not just one
3. **Combine formats** — Use Quick for ideas, Detailed for strategy
4. **Act on findings** — Top 3 content gaps should be created within 30 days
5. **Monitor changes** — Track when competitors publish new content
6. **Validate data** — Cross-check findings with your own rank tracking

---

## 🔐 Data Privacy

- No competitor data is stored
- Analysis is real-time, not saved
- Sitemaps are processed, then discarded
- Reports are generated on-demand
- All analysis is for competitive intelligence only (ethical use)

---

## 📚 Resources

- **SEMrush API** (optional, for advanced backlink data)
- **Ahrefs** (optional, for more detailed backlink analysis)
- **Google Search Console** (your own rankings)
- **Screaming Frog** (optional, crawl competitor site)

---

**Built by mhuzaifaariz** — Competitive intelligence for SEO professionals.

*Last updated: April 2026*
