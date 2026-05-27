---
name: collab-planner
description: Collaboration planning tool — analyze content overlap between you and potential collaborators, propose win-win collaboration formats (cross-posts, interviews, co-authored content, joint series). Leverages competitor-scout data and profile analysis.
---

# Collaboration Planner

Find and plan content collaborations that benefit both you and your partner.

## When to Activate

- User says `/collab` or `/collab {handle}`
- User asks "who should I collaborate with?"
- User asks "plan a collab with {name}"
- User wants to grow audience through partnerships

## Prerequisites

- `~/.content-autopilot/profile.json` must exist
- Optional: `competitor-analysis.json` (for overlap analysis)
- Optional: `content-history.json` (for topic matching)

## Commands

### `/collab {handle}` — Analyze and plan collaboration with a specific creator
### `/collab suggest` — Suggest potential collaborators based on your niche
### `/collab formats` — Show all available collaboration formats

## Collaboration Formats

| Format | Effort | Reach Boost | Best For |
|--------|--------|-------------|----------|
| Cross-mention | Low | 1.2x | Quick visibility boost |
| Quote + Comment | Low | 1.5x | Building relationship |
| Joint X Thread | Medium | 2x | Shared audience exposure |
| Interview (note) | Medium | 2.5x | Authority building |
| Co-authored Article | High | 3x | Deep expertise showcase |
| Joint Series | High | 4x | Long-term audience growth |
| Challenge/Campaign | Medium | 3x | Community engagement |

## Workflow: Analyze Collaborator (`/collab {handle}`)

### Step 1: Research the Collaborator

Use WebSearch to gather information:
```
Search: "{handle} note" OR "site:note.com/{handle}"
Search: "{handle} X" OR "from:{handle}" (Twitter)
Search: "{handle} profile" "{handle} about"
```

Extract:
- Content topics and niche
- Audience size (approximate)
- Content style and frequency
- Platform presence (note, X, Instagram)

### Step 2: Overlap Analysis

Compare your profile with the collaborator:

```
============================================
  Collaboration Analysis
  You × {collaborator_name}
============================================

--- Topic Overlap ---
Shared interests:
  - {topic A} (you: {count} posts, them: {count} posts)
  - {topic B} (you: {count} posts, them: {count} posts)

Your unique topics: {topic C}, {topic D}
Their unique topics: {topic E}, {topic F}

Overlap score: {percentage}%
  (20-40% = ideal — enough common ground, enough differentiation)
  (>60% = too much overlap — may feel competitive)
  (<20% = too little overlap — hard to find common audience)

--- Audience Comparison ---
Your audience: {audience_description}
Their audience: {audience_description}
Overlap estimate: {low/medium/high}
New audience potential: {estimate}

--- Style Compatibility ---
Your style: {style.tone}
Their style: {observed_style}
Compatibility: {high/medium/low}
```

### Step 3: Propose Collaboration Ideas

Based on the overlap analysis, suggest 3-5 collaboration ideas:

```
--- Collaboration Proposals ---

1. [Quick Win] Cross-Mention Thread
   You tweet about {shared_topic}, mention {handle}'s perspective
   They quote-tweet with their take
   Effort: Low | Expected reach: +{estimate}% impressions
   Draft tweet: "{draft_tweet_mentioning_them}"

2. [Medium] Interview on note
   You interview {handle} about {their_unique_topic}
   Publish on your note → they share with their audience
   Effort: Medium | Expected reach: +{estimate}% new note followers
   Topic: "{interview_topic_suggestion}"
   5 interview questions:
     Q1: {question}
     Q2: {question}
     Q3: {question}
     Q4: {question}
     Q5: {question}

3. [Ambitious] Joint 5-Day Series
   Alternate publishing: Day 1 (you) → Day 2 (them) → ...
   Topic: "{joint_series_topic}"
   Your angle: {your_perspective}
   Their angle: {their_perspective}
   Effort: High | Expected reach: +{estimate}% for both

4. [Community] "{topic}" Challenge
   7-day challenge where both audiences participate
   Daily prompt published alternately by you and them
   Effort: Medium | Expected reach: +{estimate}% engagement
   Challenge outline: {brief_outline}

Which format interests you? (1-4 / or describe your own idea)
```

### Step 4: Generate Outreach Message

After the user selects a format, draft an outreach message:

```
--- Outreach Message Draft ---

Platform: {X DM / note comment / email}

Subject: {collab_format}のご提案 — {your_name}

{collaborator_name}さん、はじめまして。
{your_name}と申します。{theme.main}について{platform}で発信しています。

{handle}さんの「{specific_content_reference}」の記事、とても参考になりました。
特に{specific_point}の視点は、私の読者にも響く内容だと思います。

ぜひ{collab_format_description}で一緒にコンテンツを作れないかと思い、
ご連絡しました。

{specific_proposal_details}

お互いの読者に新しい価値を届けられると思いますが、いかがでしょうか？

{your_name}
{your_platforms}

---
Customize this message before sending.
```

### Step 5: Plan Execution

If the user proceeds, create an execution plan:

```
--- Collaboration Execution Plan ---

Format: {selected_format}
Partner: {collaborator_name}
Timeline: {proposed_dates}

Pre-collaboration:
  [ ] Send outreach message
  [ ] Agree on format, topic, and timeline
  [ ] Share profile.json style notes (so content feels cohesive)

During:
  [ ] {step_1}
  [ ] {step_2}
  [ ] {step_3}

Post-collaboration:
  [ ] Cross-promote final content
  [ ] Thank publicly on each platform
  [ ] Measure reach/engagement increase
  [ ] Record in content-history.json
```

## Suggest Collaborators (`/collab suggest`)

If competitor-analysis.json exists, suggest from:
1. Competitors with complementary (not identical) content
2. Creators in adjacent niches found during research
3. Active commenters/engagers from content-history

```
Potential Collaborators:

1. {name} — {niche}
   Overlap: {percentage}% | Audience: ~{size}
   Why: {reason this would be a good collab}

2. {name} — {niche}
   Overlap: {percentage}% | Audience: ~{size}
   Why: {reason}

3. {name} — {niche}
   Overlap: {percentage}% | Audience: ~{size}
   Why: {reason}

Analyze: /collab {handle} for detailed planning
```

## Quality Gate

Before delivering:
- [ ] Collaborator research is based on public information only
- [ ] Overlap analysis is accurate and data-backed
- [ ] Proposals are genuinely win-win (not one-sided)
- [ ] Outreach message is respectful and personalized
- [ ] Execution plan is realistic and actionable
- [ ] Selected format matches both parties' audience and content style
