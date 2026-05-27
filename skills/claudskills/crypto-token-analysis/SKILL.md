---
name: crypto-token-analysis
description: Deep-dive framework for analyzing crypto tokens — market data, liquidity health, tokenomics, unlock schedules, and risk assessment. Combines on-chain data, API queries, and multi-source validation to generate actionable investment verdicts.
tags: [crypto, token-analysis, defi, research, trading, airdrop, risk-assessment]
origin: unknown
source_license: see upstream
language: en
---

# Crypto Token Deep Analysis Framework

Systematic approach for analyzing crypto tokens with focus on **profit opportunities** and **risk avoidance**. Used when user requests token analysis, investment research, or airdrop evaluation.

## When to Use

- User asks to analyze a specific token (e.g., "$HPL analysis")
- Requests for "deep dive", "fundamental analysis", or "is X token good?"
- **Airdrop opportunity evaluation** (token OR project-level)
- Risk assessment before investment
- Comparing tokens in an ecosystem
- **Analyzing crypto projects/protocols for airdrop potential** (AI agents, DeFi protocols, infrastructure)
- **Evaluating X/Twitter announcements** for alpha/farming opportunities
- **DePIN project analysis** (Decentralized Physical Infrastructure Networks — Helium, IoTeX, Peaq, Render, etc.)
- **Stock market dividend analysis** (IDX/Indonesian stocks) — see `references/idx-dividend-analysis.md` for workflow when APIs fail
- **NFT collection analysis** (OpenSea, Blur, etc.) — floor price, volume, holder distribution, project status

## Analysis Types

### Type A: Token Analysis (existing token with market data)
Use when: Token already listed on CoinGecko/CMC, has trading volume, circulating supply.

### Type B: Project/Protocol Analysis (pre-token or early-stage)
Use when: Analyzing for **airdrop potential**, product is live but no token yet, or token just launched with minimal data.

**Key difference:** Type B focuses on **product reality**, **user onboarding**, **VC backing**, and **airdrop signals** rather than liquidity metrics.

### Type C: DePIN Project Analysis (hardware-based infrastructure)
Use when: Analyzing **Decentralized Physical Infrastructure Networks** — projects requiring hardware (IoT devices, sensors, nodes, GPUs, wireless hotspots).

**Key difference:** Type C evaluates **hardware requirements**, **operator economics**, **network effects**, and **adoption barriers** unique to physical infrastructure.

### Type D: NFT Collection Analysis (floor price, volume, holders)
Use when: Analyzing **NFT collections** on OpenSea, Blur, or other marketplaces — evaluating floor price trends, trading volume, holder distribution, and project status.

**Key difference:** Type D focuses on **floor price trends**, **volume/holder ratio**, **chart patterns** (pump & dump, death spiral), and **project abandonment signals** rather than tokenomics.

---

## Core Analysis Framework (Type A: Token Analysis)

### 1. Market Data (CoinGecko API)

**Primary endpoint:**
```bash
curl -s "https://api.coingecko.com/api/v3/coins/{token_id}"
```

**Key metrics to extract:**
- Market cap & FDV (Fully Diluted Valuation)
- 24h volume
- Circulating vs total supply
- Price performance (24h, 7d, 30d)
- ATH/ATL with dates
- Contract addresses

**Critical calculation:**
```python
vol_mcap_ratio = (volume_24h / market_cap) * 100

# Benchmarks:
# Healthy: >10%
# Acceptable: 3-10%
# Weak: 1-3%
# Dead: <1%
```

### 2. Liquidity Health Assessment

**Volume/MCap ratio is THE critical metric for exit risk.**

If ratio < 1%, token is **illiquid** regardless of other fundamentals.

**Slippage estimation (rough):**
- <0.1% ratio: Expect 10-30% slippage on $5K trade
- 0.1-1%: Expect 3-10% slippage on $5K trade
- 1-5%: Expect 1-3% slippage on $5K trade
- >5%: Liquid, <1% slippage

### 3. Tokenomics & Unlock Risk

**Supply breakdown:**
```python
circulating_pct = (circulating_supply / total_supply) * 100
locked_pct = 100 - circulating_pct

# Risk levels:
# <20% locked: Low risk
# 20-50% locked: Medium risk
# 50-70% locked: High risk
# >70% locked: Extreme risk (avoid)
```

**Unlock schedule:**
- Check project docs, GitHub, or token vesting contracts
- If not disclosed = RED FLAG
- Calculate potential sell pressure per unlock event

### 4. Protocol Fundamentals (for DeFi tokens)

**For lending/DEX/yield protocols:**

```python
# Revenue efficiency
revenue_tvl_ratio = (annual_revenue / tvl) * 100

# Benchmarks (lending protocols):
# Excellent: >2%
# Good: 1-2%
# Acceptable: 0.5-1%
# Poor: <0.5%

# Utilization rate
utilization = (total_borrowed / total_supplied) * 100

# Healthy range: 40-80%
# Too low (<30%): Dead capital
# Too high (>90%): Liquidity risk
```

**TVL quality check:**
- Look for "dead capital" (high TVL, low utilization)
- Check if TVL is real or wash farming
- Compare TVL to actual user count

### 5. Ecosystem & Narrative

**Context matters:**
- Is the base chain/ecosystem growing or dying?
- Compare token performance to ecosystem native token
- Check if token is listed on major trackers (CMC, CoinGecko)

**Example comparison:**
```python
# If analyzing token on Hyperliquid:
hype_vol_mcap = 1.2%  # Native token
target_vol_mcap = 0.02%  # Your token

relative_health = target_vol_mcap / hype_vol_mcap
# If <0.1 (10x worse), token is dying relative to ecosystem
```

### 6. Sentiment & Catalyst Check

**Use delegation for:**
- Recent X/Twitter mentions (sentiment, KOL coverage)
- Upcoming events (CEX listings, partnerships, protocol upgrades)
- Community activity (Discord, Telegram, Reddit)

**Red flags:**
- No social media presence
- Last announcement >1 month ago
- Community size << TVL (fake TVL indicator)

---

## Type B: Project/Protocol Airdrop Analysis Framework

**Use when:** Analyzing projects for airdrop potential (no token yet, or token just launched with minimal market data).

### 1. Context Extraction (from X/Twitter or announcement)

**What to extract:**
- Tweet content (product update? funding? campaign? teaser?)
- Account type (official project? founder? influencer?)
- Engagement metrics (likes, RTs, replies)
- Media attached (video, images, links)

**Tools:**
```bash
# Get tweet data
curl -s "https://api.fxtwitter.com/{handle}/status/{tweet_id}" | jq -r '.tweet | {text, author, likes, retweets, replies, media}'

# Get account info
curl -s "https://api.fxtwitter.com/{handle}" | jq -r '.user | {name, description, followers, website}'
```

### 2. Project Identification

**Core questions:**
- What problem does it solve?
- Category: AI / Infra / DeFi / Identity / L2 / Gaming / etc.
- Unique edge vs competitors?
- Target users (devs? traders? consumers?)

**Research sources:**
- Project bio on X
- Website (if accessible)
- GitHub org/repos
- Documentation

### 3. Product Reality Check

**Critical validation:**
```bash
# Check GitHub
curl -s "https://api.github.com/orgs/{project}/repos" | jq -r '.[] | {name, description, stars, updated_at}'

# Check specific repo
curl -s "https://api.github.com/repos/{org}/{repo}" | jq -r '{stars, forks, created_at, updated_at, language}'

# Recent commits (activity check)
curl -s "https://api.github.com/repos/{org}/{repo}/commits?per_page=5" | jq -r '.[] | {date: .commit.author.date, message: .commit.message}'

# Check npm package (if CLI tool)
curl -s "https://registry.npmjs.org/{package}" | jq -r '{name, version, description, "dist-tags": ."dist-tags"}'
```

**Maturity indicators:**
- ✅ Live product (not just whitepaper)
- ✅ Active GitHub (commits in last 30 days)
- ✅ Documentation exists
- ✅ Testnet or mainnet deployed
- ❌ Vaporware (no code, only marketing)

### 4. Ecosystem & Backing

**VC/Funding signals:**
- Check project bio for "Backed by X"
- Search Crunchbase, Twitter for funding announcements
- Look for partner logos on website

**Ecosystem positioning:**
- Which chain(s)? (Ethereum, Solana, Cosmos, etc.)
- Part of larger narrative? (AI agents, DeFi 2.0, RWA, etc.)
- Integrations with major protocols?

**Legitimacy check:**
```bash
# Search for funding news
curl -s "https://api.duckduckgo.com/?q={project}+funding+backed&format=json" | jq -r '.AbstractText'
```

### 5. Airdrop Signal Scoring (0-10)

**Positive signals (+):**
- ✅ No token yet (or just launched)
- ✅ User onboarding flow (login, wallet connect, testnet)
- ✅ Referral system exists
- ✅ Keywords: "early", "points", "rewards", "campaign", "waitlist"
- ✅ Active community growth
- ✅ Similar to past successful airdrops (Rabby, Zapper, etc.)
- ✅ VC backing (incentive to distribute tokens)
- ✅ Freemium model (free tier + premium = points system likely)

**Negative signals (-):**
- ❌ Token already exists with full circulation
- ❌ No user onboarding (just marketing site)
- ❌ Paid-only product (no free tier)
- ❌ Explicit "no token" statement
- ❌ Revenue model is pure SaaS (subscription-only)

**Scoring formula:**
```python
score = 5  # baseline

# Product stage
if no_token_yet: score += 2
if user_onboarding: score += 1
if referral_system: score += 1

# Signals
if "points" in announcement: score += 1
if "early" in announcement: score += 0.5
if freemium_model: score += 1

# Backing
if vc_backed: score += 1
if major_vc: score += 0.5  # Circle, a16z, Paradigm, etc.

# Red flags
if paid_only: score -= 2
if explicit_no_token: score -= 5

return min(10, max(0, score))
```

**Probability estimate:**
- Score 8-10: 80-90% airdrop likely
- Score 6-7.5: 60-75% likely
- Score 4-5.5: 40-55% (speculative)
- Score <4: <40% (unlikely)

### 6. User Action Requirements

**What can users do NOW?**
- Install/signup (email, wallet, social auth)
- Complete onboarding (KYC, testnet tasks)
- Make transactions (swaps, deposits, trades)
- Referrals (invite friends)
- Social tasks (follow, retweet, Discord)

**Effort assessment:**
- LOW: Just signup/follow
- MEDIUM: Testnet transactions, small deposits
- HIGH: Mainnet activity with real funds

### 7. Momentum Analysis

**Engagement check:**
- Tweet engagement (likes/followers ratio)
- Follower growth rate
- GitHub stars growth
- Community size (Discord, Telegram)

**Stage detection:**
- Pre-early: <1K followers, no product
- Early: 1K-50K followers, MVP live
- Mid: 50K-200K followers, product mature
- Late: >200K followers, token likely soon

### 8. Red Flag Detection

**Scam/farming trap signals:**
- ❌ Hype without product
- ❌ Anonymous team
- ❌ Unrealistic promises ("10000x guaranteed")
- ❌ Requires upfront payment for "airdrop"
- ❌ Asks for private keys/seed phrases
- ❌ Fake partnerships (check official partner accounts)
- ❌ Copied code (check GitHub for forks of scam projects)

### 9. Hidden Alpha (Strategic Insights)

**Non-obvious opportunities:**
- Infrastructure play (if AI agents go mainstream, this becomes critical)
- First-mover in new category
- Potential acquisition target
- Ecosystem positioning (official tool for major protocol)
- Developer-first = sticky users (high retention)
- Cross-protocol exposure (using Project A might qualify for Project B airdrop)

**Comparison to past successes:**
- Rabby Wallet: Product-first, airdrop later → successful
- Zapper: Freemium, eventual token → successful
- LayerZero: Testnet farming → successful (but controversial)
- Arbitrum: Mainnet usage → successful

### 10. Final Verdict

**Verdict options:**
- **FARM**: High confidence, clear action path, good ROI potential
- **WATCH**: Promising but wait for explicit announcement
- **SKIP**: Low probability or too much effort for expected return
- **AVOID**: Red flags detected, likely scam/waste of time

**Output format:**
```markdown
## VERDICT: [FARM / WATCH / SKIP / AVOID]

**Score:** X/10
**Airdrop Probability:** X%
**Stage:** [Pre-early / Early / Mid / Late]

**Reasoning:**
[2-3 sentences with key data points]

**If FARM, action steps:**
1. [Specific action with command/link]
2. [Next action]
3. [Monitoring trigger]

**If WATCH, entry conditions:**
- ✅ [Condition 1]
- ✅ [Condition 2]

**Time commitment:** [LOW / MEDIUM / HIGH]
**Expected ROI (if airdrop):** $X-Y
**Risk:** [Financial / Time / Opportunity cost]
```

### 11. Strategy & Action Plan

**For FARM verdict:**
```markdown
**Immediate actions (next 24h):**
1. [Setup step with exact command]
2. [Onboarding step]
3. [First transaction/activity]

**Ongoing (weekly/monthly):**
- [Maintenance activity]
- [Monitoring what to watch]

**Exit triggers:**
- ❌ [Condition that invalidates thesis]
- ✅ [Condition to farm harder]

**Time commitment:** X hours/month
**Capital required:** $X-Y
**Risk level:** [LOW / MEDIUM / HIGH]
```

---

## Type C: DePIN Project Analysis Framework

**Use when:** Analyzing Decentralized Physical Infrastructure Networks (Helium, Peaq, IoTeX, Render, Hivemapper, etc.)

### 1. Infrastructure Type Classification

**Categories:**
- **Wireless:** Helium (5G/LoRaWAN), XNET (WiFi)
- **Compute:** Render (GPU), Akash (cloud compute), Gensyn (ML training)
- **Storage:** Filecoin, Arweave, Storj
- **Sensors/IoT:** Peaq (machine economy), IoTeX (smart devices)
- **Mapping:** Hivemapper (dashcam mapping), DIMO (vehicle data)
- **Energy:** Powerledger (grid), Arkreen (solar)

### 2. Hardware Requirements Assessment

**Critical questions:**
- What hardware is needed? (hotspot, GPU, sensor, vehicle, etc.)
- Upfront cost? ($100-$500 = accessible, $1K-$5K = medium, >$5K = high barrier)
- Technical complexity? (plug-and-play vs requires networking knowledge)
- Ongoing costs? (electricity, bandwidth, maintenance)

**Barrier entry scoring:**
```python
barrier_score = 10  # start at 10 (lowest barrier)

# Hardware cost penalty
if hardware_cost > 5000: barrier_score -= 4
elif hardware_cost > 1000: barrier_score -= 2
elif hardware_cost > 500: barrier_score -= 1

# Technical complexity penalty
if requires_networking_knowledge: barrier_score -= 2
if requires_custom_setup: barrier_score -= 1

# Ongoing costs penalty
if monthly_cost > 50: barrier_score -= 2
elif monthly_cost > 20: barrier_score -= 1

# Accessibility bonus
if plug_and_play: barrier_score += 1
if no_hardware_needed: barrier_score += 3  # software-only

return max(0, min(10, barrier_score))
```

**Verdict:**
- Score 8-10: **LOW BARRIER** (accessible to retail)
- Score 5-7: **MEDIUM BARRIER** (enthusiasts only)
- Score 0-4: **HIGH BARRIER** (avoid unless institutional)

### 3. Operator Economics (ROI Analysis)

**Key metrics:**
```python
# Monthly revenue per device
monthly_revenue = token_rewards_per_month * token_price

# Payback period
payback_months = hardware_cost / monthly_revenue

# Annual ROI
annual_roi = ((monthly_revenue * 12) / hardware_cost) * 100

# Benchmarks:
# Excellent: <6 months payback, >200% ROI
# Good: 6-12 months payback, 100-200% ROI
# Acceptable: 12-24 months payback, 50-100% ROI
# Poor: >24 months payback, <50% ROI
```

**Token price risk:**
- DePIN rewards are in native token
- If token drops 50%, ROI halves
- Check token volatility (ATH vs current price)

**Example calculation:**
```
Helium 5G hotspot:
- Hardware: $500
- Monthly rewards: 50 MOBILE tokens
- Token price: $0.001
- Monthly revenue: $0.05
- Payback: 10,000 months (DEAD)

Peaq machine node:
- Hardware: $0 (software-only)
- Monthly rewards: 100 PEAQ
- Token price: $0.018
- Monthly revenue: $1.80
- Payback: N/A (no hardware cost)
- But token down -97.6% from ATH (HIGH RISK)
```

### 4. Network Effects & Adoption

**Critical mass indicators:**
- How many devices/nodes currently active?
- Growth rate (MoM, YoY)?
- Geographic coverage?
- Actual usage vs speculative deployment?

**Benchmarks:**
```python
# Device count
if devices < 1000: stage = "Pre-early"
elif devices < 10000: stage = "Early"
elif devices < 100000: stage = "Growth"
else: stage = "Mature"

# Usage vs deployment
usage_ratio = (active_users / total_devices) * 100

# Healthy: >50% (real demand)
# Speculative: 10-50% (mostly farming)
# Dead: <10% (ghost network)
```

**Example:**
- Helium (peak): 1M+ hotspots, but <5% actual usage → **FARMING TRAP**
- Render: 10K+ GPUs, 80%+ utilization → **REAL DEMAND**

### 5. Tokenomics for DePIN

**Emission schedule:**
- How many tokens minted per day/month?
- What % goes to operators vs team/treasury?
- Is emission rate sustainable?

**Sell pressure calculation:**
```python
# Daily operator sell pressure
daily_operator_rewards = devices * avg_reward_per_device
daily_sell_pressure_usd = daily_operator_rewards * token_price

# Compare to daily volume
sell_pressure_ratio = (daily_sell_pressure_usd / daily_volume) * 100

# Sustainable: <10%
# Concerning: 10-30%
# Unsustainable: >30% (token will dump)
```

**Burn mechanisms:**
- Does protocol burn tokens? (usage fees, transaction fees)
- Burn rate vs emission rate?
- Net inflation or deflation?

### 6. Product Reality for DePIN

**Validation checklist:**
- ✅ Hardware available for purchase? (or waitlist?)
- ✅ Onboarding docs exist?
- ✅ Active operator community? (Discord, Telegram)
- ✅ Network map/explorer showing live devices?
- ✅ Actual customers using the service? (not just operators)

**Red flags:**
- ❌ Hardware "coming soon" for >6 months
- ❌ No network explorer (can't verify device count)
- ❌ Operator community larger than user community (farming trap)
- ❌ No proof of actual service usage

### 7. Competitive Moat

**DePIN-specific moats:**
- **Network density:** More devices = better coverage = more users (Helium's original thesis)
- **Hardware lock-in:** Proprietary hardware = switching cost (weak moat)
- **Data quality:** Better sensors/coverage = better data (Hivemapper vs Google Maps)
- **First-mover:** Established network hard to displace (but not impossible)

**Threat assessment:**
- Can Web2 incumbents do this better? (Google, AWS, Verizon)
- Can another DePIN project fork and improve?
- Is the "decentralization" actually valuable or just marketing?

### 8. DePIN-Specific Red Flags

**Ponzi indicators:**
- ❌ Rewards come from new operator deposits (not service revenue)
- ❌ No actual customers, only operators
- ❌ Emission rate >> service revenue (unsustainable)
- ❌ Token price required to stay high for ROI (circular dependency)

**Overhype indicators:**
- ❌ "Revolutionary" claims without proof
- ❌ Comparing to trillion-dollar industries (e.g., "We'll replace AWS")
- ❌ Roadmap with no delivered milestones
- ❌ Anonymous team or team with no relevant experience

### 9. DePIN Verdict Framework

**Scoring matrix:**

| Factor | Weight | Score (0-10) | Weighted |
|--------|--------|--------------|----------|
| Barrier to entry | 20% | X | X * 0.2 |
| Operator ROI | 25% | X | X * 0.25 |
| Network adoption | 20% | X | X * 0.2 |
| Tokenomics | 15% | X | X * 0.15 |
| Competitive moat | 10% | X | X * 0.1 |
| Product reality | 10% | X | X * 0.1 |

**Total score → Verdict:**
- 8-10: **FARM** (strong fundamentals, good ROI)
- 6-7.5: **WATCH** (promising but wait for better entry)
- 4-5.5: **SKIP** (too risky or poor ROI)
- 0-3.5: **AVOID** (likely farming trap or scam)

### 10. DePIN Action Plan Template

**For FARM verdict:**
```markdown
## HARDWARE SETUP
1. Purchase: [Device name] from [vendor] (~$X)
2. Setup time: X hours
3. Technical requirements: [List]

## OPERATOR ECONOMICS
- Monthly revenue: $X (at current token price)
- Payback period: X months
- Annual ROI: X%
- Risk: Token price volatility (currently -X% from ATH)

## ONGOING MAINTENANCE
- Electricity: $X/month
- Bandwidth: X GB/month
- Monitoring: [Tools/dashboards]
- Troubleshooting: [Discord/docs links]

## EXIT STRATEGY
- Sell hardware if ROI < X%
- Dump tokens if price drops below $X
- Monitor network growth (if devices drop X%, exit)
```

**For WATCH verdict:**
```markdown
## ENTRY CONDITIONS
- ✅ Token price recovers to $X (X% from current)
- ✅ Network reaches X devices (proof of adoption)
- ✅ Hardware cost drops below $X
- ✅ Operator ROI improves to >X%/year

## MONITORING
- Check monthly: [Metrics to track]
- Set alerts: [Price/network thresholds]
```

---

## Type D: NFT Collection Analysis Framework

**Use when:** Analyzing NFT collections on OpenSea, Blur, or other marketplaces (e.g., "Is Numismatis NFT worth buying?")

### 1. Current Metrics Extraction

**Primary data sources:**
- OpenSea API (if accessible)
- OpenSea web UI (via Browser Use Cloud if Cloudflare blocks)
- Blur API
- NFTScan API

**Key metrics to extract:**
```
Floor Price:     X ETH (~$Y USD)
Total Volume:    X ETH (all-time)
Total Sales:     X sales
Holders:         X unique owners
Supply:          X NFTs
Market Cap:      X ETH (floor * supply)

Trading Activity:
├─ 24h:  X ETH (Y sales) → Avg: Z ETH/sale
├─ 7d:   X ETH (Y sales) → Avg: Z ETH/sale
└─ 30d:  X ETH (Y sales) → Avg: Z ETH/sale
```

**Critical calculations:**
```python
# Volume per holder (liquidity indicator)
vol_per_holder = volume_24h / holders

# Holder concentration
holder_concentration = holders / supply  # Lower = more concentrated

# Average sale price trends
avg_sale_24h = volume_24h / sales_24h
avg_sale_7d = volume_7d / sales_7d
avg_sale_30d = volume_30d / sales_30d

# Declining avg sale = death spiral
if avg_sale_24h < avg_sale_7d < avg_sale_30d:
    trend = "DEATH_SPIRAL"
```

### 2. Historical Price Analysis

**Chart pattern recognition:**

**A. Pump & Dump Pattern** 🔴
```
Characteristics:
- Slow accumulation (0.1 → 0.2 ETH over weeks)
- Flat distribution phase (consolidation)
- Sharp pump (2-5x in days/weeks)
- Immediate crash (50-100% drop)
- Dead cat bounce (brief recovery)
- Final death spiral (continuous decline)

Example timeline:
Oct: 0.1 ETH (launch)
Dec: 0.2 ETH (accumulation)
Jan: 0.2 ETH (distribution)
Feb: 0.5 ETH (PUMP - 2.5x)
Mar: 0.0 ETH (CRASH - rug pull)
Apr: 0.4 ETH (dead cat bounce)
May: 0.003 ETH (death spiral)

Verdict: RUG PULL / ABANDONED
```

**B. Death Spiral Pattern** 🔴
```
Characteristics:
- Continuous decline with no support levels
- No consolidation zones
- No buying pressure
- Accelerating decline (e.g., -94% in 7 days)
- High sale count but tiny values (panic selling)

Indicators:
- Floor price -90%+ from peak
- No horizontal support lines on chart
- Volume declining but sale count high
- Avg sale price dropping faster than floor

Verdict: PROJECT DEAD
```

**C. Healthy Correction Pattern** ✅
```
Characteristics:
- Gradual uptrend with consolidation
- Multiple horizontal support levels
- Higher lows, higher highs
- Volume steady or increasing
- Community active during dips

Indicators:
- Floor price -20-40% from peak (normal correction)
- Clear support levels (price bounces)
- Volume/holder ratio stable
- Social media active

Verdict: HEALTHY PROJECT
```

**Price decline severity:**
```python
decline_from_peak = ((ath_price - current_price) / ath_price) * 100

# Classification:
if decline > 95: severity = "TERMINAL"      # Project dead
elif decline > 80: severity = "CRITICAL"    # Likely abandoned
elif decline > 60: severity = "SEVERE"      # Major issues
elif decline > 40: severity = "MODERATE"    # Normal bear market
else: severity = "HEALTHY"                  # Normal volatility
```

### 3. Project Fundamentals Assessment

**Basic info checklist:**
```
Name:       [Collection name]
Concept:    [What is it? Art? Utility? PFP?]
Contract:   [Ethereum address]
Launched:   [Date] (X months ago)
Website:    [URL] ✅/❌
Twitter:    [@handle] (X followers) ✅/❌
Discord:    [Link] (X members) ✅/❌
Telegram:   [Link] ✅/❌
Status:     OpenSea Verified ✅/❌
```

**Team & development:**
```
Team:       ✅ Doxxed / ❌ Anonymous
Roadmap:    ✅ Exists / ❌ None
Updates:    ✅ Regular / ⚠️ Sporadic / ❌ None
Social:     ✅ Active / ⚠️ Declining / ❌ Dead
Community:  ✅ Engaged / ⚠️ Quiet / ❌ Ghost town
```

**Utility assessment:**
```
Staking:        ✅/❌
Rewards:        ✅/❌
Ecosystem:      ✅/❌ (DAO, token, metaverse, etc.)
Partnerships:   ✅/❌
Real Benefits:  ✅/❌ (IRL utility, access, etc.)
Use Case:       [Description or "None"]

Verdict: [STRONG UTILITY / WEAK UTILITY / ZERO UTILITY]
```

### 4. Red Flag Detection (NFT-Specific)

**10 Major Warning Signs:**

**1. Catastrophic Floor Price** 🔴
```
Floor < $10 = Dead project territory
Floor < $50 = Severe distress
Floor < $100 = Concerning (depends on mint price)

Context matters: If mint was $100 and floor is $5 = -95% = DEAD
```

**2. Abandoned Community** 🔴
```
Twitter followers < 1K after 6+ months = DEAD
No Discord/Telegram = ABANDONED
Last tweet > 1 month ago = INACTIVE
Discord last message > 1 week ago = GHOST TOWN
```

**3. Zero Market Cap** 🔴
```
If OpenSea reports 0.0 ETH market cap = NO VALUE
```

**4. No Development** 🔴
```
No roadmap updates = ABANDONED
No new features/utilities = STAGNANT
No team communication = RUG PULL
```

**5. Suspicious Volume** 🔴
```
High sale count but low total volume = WASH TRADING or PANIC SELLING

Example:
- 129 sales/day but only 1.1 ETH total
- Avg: 0.0085 ETH/sale ($20)
- Pattern: Desperate holders dumping at any price
```

**6. Poor Holder Distribution** 🔴
```
Holders / Supply < 60% = High concentration risk

Example:
- 285 holders / 547 supply = 52%
- Many holders own multiple NFTs
- Whales can dump and crash floor
```

**7. No Utility** 🔴
```
Just collectible, no use case = WEAK VALUE PROP
No staking, rewards, or benefits = NO REASON TO HOLD
```

**8. Declining Momentum** 🔴
```
All metrics trending DOWN:
├─ Price: -X% from 30d avg
├─ Volume: Declining
├─ Holders: Decreasing
└─ Community: Shrinking

Trend: DEATH SPIRAL
```

**9. Fast Death** 🔴
```
Launched < 12 months ago but already dead = EXTREMELY FAST FAILURE

Example:
- Launched: Aug 2025
- Dead by: May 2026 (9 months)
- Speed: RED FLAG (most projects take 18-24 months to die)
```

**10. No Recovery Catalysts** 🔴
```
No team announcements = NO HOPE
No roadmap updates = NO FUTURE
No partnerships = NO GROWTH
No utility additions = NO VALUE
No community growth = NO BUYERS

Recovery Chance: ~5% (near zero)
```

### 5. Positive Signals (Rare in Dying Projects)

**What to look for:**
```
✅ OpenSea Verified (but doesn't save dying project)
✅ Website still online (but check last update)
✅ Unique concept (but execution matters more)
✅ Very cheap entry (but cheap for a reason)
✅ Complete collection minted (but doesn't mean success)
✅ Active Discord (>100 messages/day)
✅ Regular team updates (weekly or more)
✅ Partnerships announced (with proof)
✅ Utility roadmap (with delivered milestones)
✅ Community events (spaces, AMAs, giveaways)
```

**Note:** In dying projects, positives are usually MEANINGLESS compared to negatives.

### 6. Risk Assessment Framework

**Risk Level Calculation:**
```python
risk_score = 0  # Start at 0 (lowest risk)

# Price risk
if floor_decline > 95: risk_score += 4
elif floor_decline > 80: risk_score += 3
elif floor_decline > 60: risk_score += 2
elif floor_decline > 40: risk_score += 1

# Liquidity risk
if volume_24h < 1: risk_score += 3  # <1 ETH/day = CRITICAL
elif volume_24h < 5: risk_score += 2
elif volume_24h < 10: risk_score += 1

# Community risk
if no_discord_telegram: risk_score += 2
if twitter_followers < 1000: risk_score += 1
if last_update > 30_days: risk_score += 2

# Development risk
if no_roadmap: risk_score += 1
if no_utility: risk_score += 1

# Total risk (0-10 scale)
risk_level = min(10, risk_score)

# Classification:
if risk_level >= 8: return "EXTREME"
elif risk_level >= 6: return "HIGH"
elif risk_level >= 4: return "MEDIUM"
else: return "LOW"
```

**Scenario Probability Estimation:**
```python
# Best case (recovery)
if risk_level >= 8:
    best_case_prob = 5  # 5% chance
    best_case_gain = "3-5x"
elif risk_level >= 6:
    best_case_prob = 15
    best_case_gain = "2-3x"
else:
    best_case_prob = 30
    best_case_gain = "1.5-2x"

# Most likely (continued decline)
most_likely_prob = 100 - best_case_prob - 15  # Reserve 15% for worst case
most_likely_outcome = "50-90% more loss"

# Worst case (complete death)
worst_case_prob = 15
worst_case_outcome = "100% loss"
```

### 7. NFT Verdict Framework

**Verdict options:**
- **BUY (SEROK)**: Strong fundamentals, healthy chart, active community, clear utility
- **HOLD**: Already own, project still has potential, wait for recovery
- **AVOID (JANGAN SEROK)**: Death spiral, abandoned project, no recovery chance
- **WATCH**: Interesting but wait for better entry or more data

**Decision matrix:**

| Floor Decline | Volume | Community | Utility | Verdict |
|---------------|--------|-----------|---------|---------|
| <40% | >10 ETH/day | Active | Strong | BUY |
| 40-60% | 5-10 ETH/day | Moderate | Weak | WATCH |
| 60-80% | 1-5 ETH/day | Declining | None | AVOID |
| >80% | <1 ETH/day | Dead | None | AVOID |

**Special case: Death spiral pattern detected**
```
If chart shows:
- Pump & dump pattern (Feb peak → Mar crash)
- -90%+ decline in <3 months
- No support levels
- Volume declining but sale count high

→ VERDICT: AVOID (regardless of other factors)
→ REASON: "Ini bukan dip, ini project mati"
```

### 8. Output Format (Indonesian Style)

**User prefers:**
- Direct verdict upfront (JANGAN SEROK / SEROK)
- Concise explanations (no fluff)
- Data-driven reasoning
- Clear risk assessment
- Specific numbers (not ranges)

**Template:**
```markdown
# 🔴 [COLLECTION NAME] — ANALISA MENDALAM

## 🎯 JAWABAN SINGKAT

### **"Lagi dump, apakah kita serok?"**

# ❌ **JANGAN SEROK!**

**Ini bukan dip, ini project MATI!** 💀

---

## 📊 CURRENT METRICS (Date)

```
Floor Price:    X ETH (~$Y USD)
Total Volume:   X ETH (all-time)
Total Sales:    X sales
Holders:        X unique owners
Supply:         X NFTs
Market Cap:     X ETH

Trading Activity:
├─ 24h:  X ETH (Y sales) → Avg: Z ETH/sale
├─ 7d:   X ETH (Y sales) → Avg: Z ETH/sale
└─ 30d:  X ETH (Y sales) → Avg: Z ETH/sale
```

---

## 📉 HISTORICAL ANALYSIS

**Price Trends:**
```
Current Floor:     X ETH ($Y)
30-day Average:    X ETH ($Y)
Decline:           -X% ⚠️⚠️⚠️

Status: [DEATH SPIRAL / HEALTHY CORRECTION / etc.]
```

**Chart Pattern:** [Pump & Dump / Death Spiral / Healthy]

**Timeline:**
```
[Month] [Year]:  ~X ETH    ([Stage])
[Month] [Year]:  ~X ETH    ([Stage])
...
[Month] [Year]:  X ETH     ← NOW

Trend: [↓↓↓ CONTINUOUS DECLINE / ↑ RECOVERY / etc.]
```

---

## 🏢 PROJECT FUNDAMENTALS

**Basic Info:**
```
Name:       [Name]
Concept:    [Description]
Contract:   [Address]
Launched:   [Date] (X months ago)
Website:    [URL] ✅/❌
Twitter:    [@handle] (X followers) ✅/❌
Discord:    [Link] ✅/❌
Status:     OpenSea Verified ✅/❌
```

**Team & Development:**
```
Team:       ✅/❌
Roadmap:    ✅/❌
Updates:    ✅/❌
Social:     ✅/⚠️/❌
Community:  ✅/⚠️/❌
```

**Utility:**
```
[List of utilities or "ZERO UTILITY"]
```

---

## 🚩 RED FLAGS (X MAJOR WARNINGS)

### **1. [Red Flag Name]** 🔴
```
[Description with data]
```

[Repeat for each red flag]

---

## ✅ POSITIVE SIGNALS (Minimal/None)

```
[List positives or "NONE"]
```

**Note:** [Context on why positives don't matter]

---

## ⚖️ RISK ASSESSMENT

**Risk Level: 🔴 [EXTREME / HIGH / MEDIUM / LOW] (X/10)**

**Scenarios:**

**1. Best Case (X% probability):**
```
[Description]
Gain: Xx from current price
Likelihood: [VERY LOW / LOW / MODERATE / HIGH]
```

**2. Most Likely (X% probability):**
```
[Description]
Loss: -X% more from current
Status: [Description]
Likelihood: [VERY HIGH / HIGH / MODERATE]
```

**3. Worst Case (X% probability):**
```
[Description]
Loss: -100% of investment
Status: [Description]
Likelihood: [HIGH / MODERATE / LOW]
```

**Risk Factors:**
```
Liquidity:          🔴 [CRITICAL / HIGH / MEDIUM / LOW]
Abandonment:        🔴 [HIGH / MEDIUM / LOW]
Price Decline:      🔴 [CRITICAL / SEVERE / MODERATE]
Recovery Potential: 🔴 [NEAR ZERO / LOW / MEDIUM / HIGH]
Community:          🔴 [DEAD / DECLINING / ACTIVE]
Utility:            🔴 [NONE / WEAK / STRONG]
Development:        🔴 [ABANDONED / SLOW / ACTIVE]
```

**Overall Risk:** 🔴 **[VERDICT]**

---

## 🎯 FINAL RECOMMENDATION

# ❌ **[AVOID / BUY / HOLD / WATCH] — [REASON]**

**WHY NOT TO BUY:** (if AVOID)

**1. [Reason 1]**
```
[Explanation with data]
```

[Repeat for each reason]

**WHAT TO DO:**

**If you HOLD [Collection]:**
```
❌ [Action 1]
❌ [Action 2]
✅ [Recommended action]
```

**If you're CONSIDERING buying:**
```
❌ [What not to do]
✅ [What to do instead]
```

**Better alternatives:**
```
[List of better NFT projects or strategies]
```

---

## 📝 CONCLUSION

**[Collection Name] = [VERDICT]**

**Signs of [Status]:**
- ✅ [Sign 1]
- ✅ [Sign 2]
- ✅ [Sign 3]

---

# 🇮🇩 FINAL ANSWER:

## ❌ **[VERDICT IN INDONESIAN]**

**[Concise explanation in Indonesian]**

**[Collection] = 💀 [STATUS]**

**Recovery chance: X%**  
**Loss risk: X%**

**Verdict: [FINAL VERDICT]** 🔴

---

**Disclaimer:** Not financial advice. DYOR.

**Analysis Date:** [Date]  
**Data Sources:** [OpenSea, Twitter, etc.]
```

### 9. Data Gathering for NFTs

**Primary method: Browser Use Cloud API**

**Why Browser Use over Scrapling:**
- ✅ Zero disk usage (cloud-based)
- ✅ Zero RAM usage (no local browser)
- ✅ Bypasses Cloudflare automatically
- ✅ Stealth browser (forked Chromium)
- ✅ Residential proxies built-in
- ❌ Pay per use (but worth it for VPS with limited resources)

**Scrapling comparison:**
- ❌ 650-900 MB disk
- ❌ 200-400 MB RAM per browser session
- ❌ Too heavy for 2GB RAM VPS
- ✅ Free (self-hosted)

**Verdict:** Use Browser Use Cloud for NFT scraping on resource-constrained VPS.

**API endpoint:**
```bash
# Create session
curl -X POST "https://api.browser-use.com/v3/sessions" \
  -H "X-Browser-Use-API-Key: bu_..." \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://opensea.io/collection/{slug}/analytics",
    "task": "Extract floor price, volume (24h/7d/30d), holders, supply, recent sales",
    "model": "gpt-4o-mini",
    "max_steps": 15
  }'

# Poll for result
curl -X GET "https://api.browser-use.com/v3/sessions/{session_id}" \
  -H "X-Browser-Use-API-Key: bu_..."
```

**Fallback if Browser Use unavailable:**
- OpenSea API (if accessible)
- Blur API
- NFTScan API
- Manual user screenshot (ask user to provide data)

**See:** `references/browser-use-cloud.md` for full API documentation and self-registration flow.

**Polymarket bot ecosystem:** See `references/polymarket-bots-ecosystem.md` for comprehensive analysis of 20+ trading bot repositories, strategies, and tech stacks.

### 10. Common Pitfalls (NFT-Specific)

**Pitfall 1: "Cheap = Good Deal" Fallacy**

**Problem:** Low floor price doesn't mean undervalued

**Solution:** Check WHY it's cheap:
- Project abandoned? (team gone, no updates)
- No utility? (just art, no use case)
- No community? (Discord dead, Twitter inactive)
- Death spiral? (continuous decline, no support)

**Example:**
- Floor $5 but project dead = NOT A DEAL
- Floor $500 but active community + utility = POTENTIALLY GOOD

**Pitfall 2: "High Volume = Healthy" Fallacy**

**Problem:** High sale count doesn't mean healthy project

**Solution:** Check average sale price:
```python
avg_sale = volume / sale_count

if avg_sale < floor_price * 0.5:
    # People selling below floor = PANIC
    status = "DEATH_SPIRAL"
```

**Example:**
- 129 sales/day, 1.1 ETH volume = Avg $20/sale
- Floor is $8 = People dumping at any price
- Status: PANIC SELLING, not healthy volume

**Pitfall 3: "OpenSea Verified = Safe" Fallacy**

**Problem:** Verification doesn't prevent rug pulls

**Solution:** Verify badge only confirms identity, not quality:
- Check team activity (Twitter, Discord)
- Check development (roadmap progress)
- Check community (engagement, not just size)

**Pitfall 4: Ignoring Chart Patterns**

**Problem:** Focusing only on current price, not trend

**Solution:** Always check historical chart:
- Pump & dump pattern = RUG PULL
- Death spiral = ABANDONED
- Healthy correction = TEMPORARY DIP

**User provided chart showing pump & dump:**
- Feb peak (0.5 ETH) → Mar crash (0.0 ETH) → Apr bounce (0.4 ETH) → May death (0.003 ETH)
- Pattern: TEXTBOOK RUG PULL
- Verdict: AVOID (not a dip, project dead)

**Pitfall 5: "High Risk = High Reward" Fallacy**

**Problem:** Assuming dying project = opportunity

**Solution:** Calculate expected value:
```python
expected_value = (prob_gain * gain) + (prob_loss * loss)

# Example (dying NFT):
# 5% chance of 3x = +0.15
# 95% chance of -90% = -0.855
# Expected value = -0.705 (NEGATIVE!)

if expected_value < 0:
    verdict = "AVOID"  # You WILL lose money on average
```

**Pitfall 6: Resource Constraints (VPS-Specific)**

**Problem:** User rejected Scrapling immediately: "gede banget makan emori dan ram"

**Lesson:** On 2GB RAM VPS, user has ZERO tolerance for heavy tools:
- 650-900 MB disk = INSTANT REJECTION
- 200-400 MB RAM = INSTANT REJECTION
- "gede banget" = STOP, don't try to convince

**Solution:** Always check resource impact BEFORE recommending tools:
- Disk: <100 MB = OK, >500 MB = ASK FIRST
- RAM: <50 MB = OK, >100 MB = ASK FIRST
- If user says "gede banget" = IMMEDIATELY pivot to lightweight alternative

**Alternative for NFT scraping:**
- Browser Use Cloud (0 MB disk, 0 MB RAM) ✅
- OpenSea API (0 MB disk, 0 MB RAM) ✅
- Ask user for screenshot (0 MB disk, 0 MB RAM) ✅

---

## Real-Time Data Gathering (X/Twitter)

---

## Real-Time Data Gathering Techniques

### X/Twitter Data (fxtwitter API)

**Primary tool: fxtwitter API** (no auth required, works from terminal)

**Get Tweet Data:**
```bash
# Single tweet
curl -s "https://api.fxtwitter.com/{handle}/status/{tweet_id}" | jq -r '.tweet | {text, created_at, likes, retweets, replies, author: .author.name}'

# With media check
curl -s "https://api.fxtwitter.com/{handle}/status/{tweet_id}" | jq -r '.tweet | {text, likes, retweets, has_media: (.media != null), media_count: (.media | length)}'
```

**Note:** Use `.author.name` not `.author.screen_name` for display name.

**Get Account Info:**
```bash
curl -s "https://api.fxtwitter.com/{handle}" | jq -r '.user | {name, description, followers, following, tweets, verified}'
```

**Engagement Analysis:**
```python
# Calculate engagement rate
engagement_rate = ((likes + retweets + replies) / followers) * 100

# Benchmarks:
# Excellent: >5%
# Good: 2-5%
# Normal: 1-2%
# Weak: 0.5-1%
# Dead: <0.5%
```

**Fallback if fxtwitter blocked:**
- Try vxtwitter.com (same API structure)
- Try fixupx.com
- Use web search: `curl -s "https://duckduckgo.com/html/?q=site:twitter.com+{query}"`

### GitHub Data

**Organization repos:**
```bash
curl -s "https://api.github.com/orgs/{project}/repos" | jq -r '.[0:5] | .[] | {name, description, stars: .stargazers_count, updated: .updated_at}'
```

**Specific repo details:**
```bash
curl -s "https://api.github.com/repos/{org}/{repo}" | jq -r '{name, stars: .stargazers_count, forks, created_at, updated_at, language}'
```

**Recent activity check:**
```bash
curl -s "https://api.github.com/repos/{org}/{repo}/commits?per_page=5" | jq -r '.[] | {date: .commit.author.date, message: .commit.message}'
```

### CoinGecko Data

**Step 1: Search for token ID**

```bash
# Search by name/symbol
curl -s "https://api.coingecko.com/api/v3/search?query={token_name}" | jq -r '.coins[] | select(.name | test("Token"; "i")) | {id, symbol, name, market_cap_rank}'
```

**Step 2: Get comprehensive market data**

```bash
# Full market data (single call)
curl -s "https://api.coingecko.com/api/v3/coins/{token_id}?localization=false&tickers=false&market_data=true&community_data=true&developer_data=true" | jq '{
  price: .market_data.current_price.usd,
  mcap: .market_data.market_cap.usd,
  fdv: .market_data.fully_diluted_valuation.usd,
  volume_24h: .market_data.total_volume.usd,
  circulating: .market_data.circulating_supply,
  total: .market_data.total_supply,
  max: .market_data.max_supply,
  ath: .market_data.ath.usd,
  ath_date: .market_data.ath_date.usd,
  atl: .market_data.atl.usd,
  atl_date: .market_data.atl_date.usd,
  price_change_24h: .market_data.price_change_percentage_24h,
  price_change_7d: .market_data.price_change_percentage_7d,
  price_change_30d: .market_data.price_change_percentage_30d,
  twitter: .community_data.twitter_followers,
  github_stars: .developer_data.stars,
  github_forks: .developer_data.forks,
  commits_4w: .developer_data.commit_count_4_weeks
}'
```

**Step 3: Get exchange liquidity data**

```bash
# Top exchanges with spread data
curl -s "https://api.coingecko.com/api/v3/coins/{token_id}/tickers?depth=true" | jq '[.tickers[] | {exchange: .market.name, pair: (.base + "-" + .target), volume_usd: .converted_volume.usd, spread: .bid_ask_spread_percentage}] | .[0:5]'
```

**Step 4: Get project links**

```bash
curl -s "https://api.coingecko.com/api/v3/coins/{token_id}" | jq -r '.links | {homepage: .homepage[0], twitter: .twitter_screen_name, telegram: .telegram_channel_identifier, github: .repos_url.github[0]}'
```

**Step 5: Get project description**

```bash
curl -s "https://api.coingecko.com/api/v3/coins/{token_id}" | jq -r '.description.en' | head -c 800
```

**Calculate Vol/MCap ratio:**

```bash
echo "Volume/MCap ratio: $(echo "scale=4; {volume_24h} / {market_cap}" | bc)"
```

### Step 2: Protocol Data (if DeFi)

**Check DeFiLlama (if accessible):**
```bash
curl -s "https://api.llama.fi/protocol/{protocol_name}"
```

**Or scrape from protocol's own app/API:**
- Navigate to app with browser tools
- Extract TVL, volume, utilization from UI
- Cross-reference with on-chain data if possible

### Step 3: Delegate Social/Catalyst Research

```python
delegate_task(
    goal="Check X/Twitter for recent mentions of {token}, upcoming catalysts, and sentiment. Also check if there are any CEX listing announcements or major partnerships in the last 7 days.",
    toolsets=["web", "browser"]
)
```

## Output Format

**Always structure output as:**

**For English analysis:**

```markdown
# TOKEN ANALYSIS: ${SYMBOL}

## SKOR: X/10

## STATUS: [GEM / SPECULATIVE / TRAP / AVOID]

---

## DATA KRITIS

**Market Cap vs Volume:** [SEHAT / LEMAH / DEAD]
- MCap: $X
- Volume: $X/day
- Ratio: X%

**Unlock:** [% LOCKED] (X tokens)
- Risk: [LOW / MEDIUM / HIGH / EXTREME]

**TVL Quality:** [REAL / FAKE / MIXED]
- Total: $X
- Real productive: $X
- Dead capital: $X

---

## 3 INSIGHT PALING PENTING

1. [Most critical finding with data]
2. [Second most important insight]
3. [Third key point]

---

## RED FLAG UTAMA

❌ [Flag 1]
❌ [Flag 2]
❌ [Flag 3]

---

## VERDICT: [GAS / WAIT / SKIP / AVOID]

**Reasoning:**
[2-3 sentences explaining the verdict with data]

**If WAIT, conditions to enter:**
- ✅ [Condition 1]
- ✅ [Condition 2]
- ✅ [Condition 3]
```

## Common Pitfalls & Solutions

### Pitfall 0: Browser Tool Fails in WSL2

**Problem:** Chrome/Playwright fails with sandbox errors in WSL2/containers

**Error message:**
```
FATAL:zygote_host_impl_linux.cc:128] No usable sandbox!
```

**Solution:** Skip browser tools entirely for crypto analysis. Use API-first approach:
- Twitter: fxtwitter API (no auth)
- CoinGecko: REST API (no auth for basic queries)
- GitHub: REST API (no auth for public repos)
- DeFiLlama: REST API

**Only use browser if:**
- Need to interact with dApp UI
- Scraping data not available via API
- In that case, add `--args "--no-sandbox"` to browser launch

### Pitfall 0.1: Stock Market Data (IDX/Indonesian Stocks)

**Problem:** Yahoo Finance rate limits aggressively (429 errors), Google Finance blocks scraping, IDX.co.id behind Cloudflare, Stockbit API requires auth

**Current limitation:** No reliable free API for real-time Indonesian stock prices

**DO NOT guess or use outdated data.** If all APIs fail:
1. **Admit limitation immediately**: "Gua gak bisa akses data real-time karena API kena rate limit"
2. **Ask user for screenshot from their broker** (Stockbit, IPOT, etc.) — this is the FASTEST path to real data
3. **Ask user for context**: "Lu bisa kasih context: IHSG level berapa? Bank lain turun berapa persen?"
4. **Use user-provided data**: If user says "BBCA @ Rp 5.900", treat that as ground truth and analyze from there
5. **Never fabricate price ranges** — saying "BBCA Rp 9.000-10.000" when it's actually Rp 5.900 destroys credibility

**Fallback strategy (in order):**
1. Try Yahoo Finance API with rate limit handling (sleep between calls, max 3-5 tickers)
2. Try Google Finance scraping (often blocked)
3. **STOP and ask user for broker screenshot** — don't waste time trying 5+ blocked sources
4. If user provides current price, use it and analyze implications (e.g., "BBCA @ Rp 5.900 = crash ~40% from normal range, ini bukan koreksi biasa")
5. Use curated fallback data from public financial reports ONLY if user explicitly asks for analysis without real-time data, and clearly label it as "estimasi, bukan real-time"

**Key lesson:** Better to admit "gua gak bisa akses data" and ask for user's broker screenshot than give wrong analysis based on guesses. User's broker app (Stockbit, IPOT, etc.) is the most reliable source.

### Pitfall 1: Bot Detection on Major Sites

**Problem:** DeFiLlama, CoinGecko web UI blocked by Cloudflare

**Solution:** Use APIs directly with curl
- CoinGecko API: No auth needed for basic queries
- DeFiLlama API: `api.llama.fi` endpoints
- Fallback: Scrape protocol's own app

### Pitfall 2: "Cheap" vs "Undervalued" Confusion

**Problem:** Low price ≠ good investment

**Solution:** Always check:
1. Volume/MCap ratio (liquidity)
2. Unlock schedule (sell pressure)
3. Momentum (ATH distance, trend)

**Example:**
- Token A: $0.01, vol/mcap 0.02%, 60% locked = TRAP
- Token B: $10, vol/mcap 5%, 10% locked = Potentially good

### Pitfall 3: Bear Market Excuse

**Problem:** "It's just bear market" can mask fundamental issues

**Solution:** Compare to ecosystem native token
```python
if token_vol_mcap < (ecosystem_token_vol_mcap * 0.1):
    # Token is 10x worse than ecosystem average
    # This is NOT just bear market
    verdict = "DYING"
```

### Pitfall 4: TVL Misleading

**Problem:** High TVL doesn't mean good token

**Solution:** Check utilization
```python
if tvl > 100M and utilization < 30%:
    # Dead capital, likely farming residue
    tvl_quality = "FAKE"
```

## Decision Matrix

| Vol/MCap | Unlock | Momentum | Catalyst | Verdict |
|----------|--------|----------|----------|---------|
| >5% | <30% | Up | Yes | GAS |
| 1-5% | 30-50% | Flat | Maybe | WAIT |
| 0.1-1% | 50-70% | Down | No | SKIP |
| <0.1% | >70% | Down | No | AVOID |

## Risk Scoring

```python
def calculate_risk_score(vol_mcap, locked_pct, momentum, catalyst):
    score = 10
    
    # Liquidity penalty
    if vol_mcap < 0.1:
        score -= 5
    elif vol_mcap < 1:
        score -= 3
    elif vol_mcap < 5:
        score -= 1
    
    # Unlock penalty
    if locked_pct > 70:
        score -= 3
    elif locked_pct > 50:
        score -= 2
    elif locked_pct > 30:
        score -= 1
    
    # Momentum penalty
    if momentum < -30:  # >30% down from ATH
        score -= 1
    
    # Catalyst bonus
    if catalyst:
        score += 1
    
    return max(0, min(10, score))
```

## Memory Protocol

**After analysis, save to memory:**
```
Token: ${SYMBOL}
Date: ${DATE}
Price: $X
MCap: $X
Vol/MCap: X%
Locked: X%
Status: [VERDICT]
Key insight: [1 sentence]
```

**Update if analyzing same token again:**
- Compare old vs new data
- Note trend changes
- Update verdict if conditions changed

## Example: Full Analysis

See conversation history for complete example of $HPL (Hyperlend) analysis demonstrating:
- CoinGecko API usage
- Volume/MCap calculation
- Unlock risk assessment
- Protocol fundamental analysis
- Ecosystem comparison
- Verdict with reasoning
- Re-analysis after user pushback (important: be willing to revise if new context provided)
