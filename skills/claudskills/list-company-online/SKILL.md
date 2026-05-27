---
name: list-company-online
description: Submit company profiles to 50+ online directories, business listings, and platforms for maximum visibility, off-page SEO boost, and brand authority. Use when the user wants to list a company online, submit business profiles, boost off-page SEO, or mentions "list company", "business directory", "company listing", "off-page SEO", "business visibility", "list business online".
user-invocable: true
argument-hint: "[--config listing-config.yaml] [--dry-run] [--platforms crunchbase,f6s,betalist,...]"
---

# List Company Online

Automated company profile submission to 50+ directories ranked by SEO authority and brand visibility impact.

## Trigger
- User says "list company online", "submit company to directories", "off-page SEO", "business listing"
- User invokes `/list-company-online`
- User mentions company directory submissions, business profiles, brand visibility, off-page SEO

## Execution Protocol

### Phase 1: Prep
1. Collect company details: name, website, description, industry, team size, founding year, locations, social links
2. Create tracker: `output/company-listings-tracker-{date}.md` — columns: Platform | DA | Status | Profile URL | Notes
3. Status values: PENDING / SUBMITTING / SUBMITTED / LIVE / FAILED / SKIPPED / MANUAL

### Phase 2: Submission (per directory)
1. Navigate to submit/signup/add page
2. Form type: direct form → fill+submit | OAuth → Google (mryadavgulshan@gmail.com) | CAPTCHA → **MANUAL** | paid → **SKIPPED** | down → **FAILED**
3. Fill completely: name, website, description, industry, location, team size, founding year, social links; submit; verify profile live; update tracker

### Phase 3: Parallelization
- **Max 4 browser-based parallel agents** — more causes tab conflicts
- CLI/API-based (GitHub Org, npm, etc.) run sequentially first
- Print full MANUAL list at end

## Priority Company Directories (Top 15)

| # | Directory | Submit URL | DA | Focus |
|---|-----------|-----------|-----|-------|
| 1 | Google Business Profile | business.google.com | 100 | Local + global |
| 2 | LinkedIn Company Page | linkedin.com/company/setup | 99 | B2B visibility |
| 3 | CrunchBase | crunchbase.com/add | 91 | Startups / tech |
| 4 | AngelList / Wellfound | wellfound.com/company/new | 88 | Hiring + investors |
| 5 | Bing Places | bingplaces.com | 93 | Search visibility |
| 6 | Apple Maps Connect | mapsconnect.apple.com | 100 | iOS users |
| 7 | Yelp | biz.yelp.com/signup | 93 | Local business |
| 8 | Product Hunt | producthunt.com/posts/new | 88 | Tech company launches |
| 9 | TrustPilot | business.trustpilot.com/signup | 93 | Consumer trust |
| 10 | G2 | g2.com/products/new | 89 | SaaS reviews |
| 11 | Capterra | capterra.com/vendors/sign-up | 88 | Software vendors |
| 12 | SourceForge | sourceforge.net/software/vendors/new | 88 | Tech companies |
| 13 | F6S | f6s.com/company/new | 75 | Startup ecosystem |
| 14 | HackerNews (Show HN) | news.ycombinator.com/submit | 89 | Tech launches |
| 15 | StartupBlink | startupblink.com/submit | 58 | Startup ecosystems |

## Error Recovery

| Error | Action |
|-------|--------|
| "Company already exists" | Claim existing profile instead |
| Required field missing | Re-read form snapshot, fill |
| CAPTCHA / reCAPTCHA | Mark **MANUAL** (not FAILED) |
| Google OAuth popup | Use redirect-based OAuth only |
| 403 / 429 rate limit | Wait 30s, retry once |
| Paid only | Mark **SKIPPED** (note price) |
| Site down | Mark **FAILED** (down) |

## Contact / Form Defaults

```
Company: Misar AI | Website: misar.io | Industry: AI / SaaS / Developer Tools
Founded: 2024 | Location: India | Team size: 1-10
LinkedIn: linkedin.com/company/misar-ai | Twitter: @mrgulshanyadav
```

## Automation Script

```bash
python ~/.claude/scripts/list_company_auto.py --config listing-config.yaml
python ~/.claude/scripts/list_company_auto.py --config listing-config.yaml --dry-run
python ~/.claude/scripts/list_company_auto.py --config listing-config.yaml --platforms "crunchbase,f6s,wellfound"
```

Full 50-directory database with per-platform submission steps lives in the tracker file generated each run.
