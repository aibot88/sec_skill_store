---
name: story-bank
description: Personal anecdote and experience storage — save your stories, failures, wins, observations, and quotes with tags for instant retrieval when writing content. Adds authenticity and originality to every piece. The most underrated content differentiator.
---

# Story Bank

Your personal experiences are your unfair advantage — store them and never forget a good story.

## When to Activate

- User says `/story-bank` or `/stories`
- User says `/stories add` to save a new story
- User says `/stories find {topic}` to search
- User asks "I need a personal example for {topic}"
- Auto-referenced by content-writer for relevant anecdotes

## Prerequisites

- None (works standalone, enhanced with profile.json)

## Data: story-bank.json

Location: `~/.content-autopilot/story-bank.json`

```json
{
  "version": "1.0",
  "stories": [
    {
      "id": "story-001",
      "added_at": "2026-03-21",
      "title": "The time I automated my entire morning routine with AI",
      "type": "win",
      "story": "Last month, I spent 3 hours setting up...",
      "lesson": "Small automation investments compound over time",
      "emotion": "surprise",
      "tags": ["AI", "automation", "productivity", "personal"],
      "usable_as": ["hook", "example", "case_study", "closing"],
      "used_in": [],
      "detail_level": "full"
    }
  ]
}
```

## Story Types

| Type | Description | Best For |
|------|------------|----------|
| win | Success story, achievement | Social proof, inspiration |
| failure | Mistake, lesson learned | Relatability, trust |
| observation | Something you noticed | Insight, unique perspective |
| conversation | Dialogue or exchange | Engagement, story hooks |
| data | Personal experiment/result | Credibility, evidence |
| turning_point | Moment that changed your thinking | Transformation narratives |
| daily | Everyday moment with deeper meaning | Relatability |

## Commands

### `/stories` — Browse all stories
### `/stories add` — Add a new story (interactive)
### `/stories quick "{one-liner}"` — Quick-add a brief anecdote
### `/stories find {topic}` — Find stories matching a topic
### `/stories find {type}` — Find stories by type (win/failure/observation)
### `/stories suggest {topic}` — Get story prompts to help you remember experiences
### `/stories stats` — Show story bank statistics

## Workflow: Add Story

### Interactive (`/stories add`):

```
Let's save a story! Answer these questions:

1. Give it a short title:
   (e.g., "The time my AI script deleted the wrong files")

2. What type of story is this?
   win / failure / observation / conversation / data / turning_point / daily

3. Tell the story (as much detail as you want):
   (The more detail, the more ways we can use it later)

4. What's the lesson or takeaway?
   (One sentence)

5. What emotion does this story evoke?
   surprise / humor / empathy / inspiration / caution / curiosity

6. Tags (topics this story relates to):
   (e.g., AI, automation, business, personal)
```

### Quick Add (`/stories quick`):

```
/stories quick "Tried to automate my email — ended up sending 500 duplicate replies. Lesson: always test with dry-run first."

Saved! Auto-categorized:
  Type: failure
  Tags: automation, email
  Emotion: humor
  Lesson: Always test with dry-run first

Edit details later with /stories edit story-{id}
```

### Story Prompts (`/stories suggest {topic}`):

Help users remember experiences they haven't recorded:

```
Story prompts for "{topic}":

Think about...
  1. The first time you {topic-related action} — what happened?
  2. Your biggest mistake with {topic} — what went wrong?
  3. A conversation where someone changed your mind about {topic}
  4. A surprising result when you tried {topic-related experiment}
  5. The moment you realized {topic} was important
  6. Something about {topic} that most people get wrong (and how you know)
  7. A time when {topic} saved you time/money/stress

Which prompt triggers a memory? Tell me the story.
```

## Workflow: Find Stories

`/stories find AI`:

```
Stories matching "AI" ({count} results):

1. [win] "Automated my morning routine with AI" (2026-03-21)
   Lesson: Small automation investments compound
   Usable as: hook, example
   Used {N} times in content

2. [failure] "AI script deleted the wrong files" (2026-03-15)
   Lesson: Always test with dry-run first
   Usable as: hook, cautionary tale
   Used {N} times

3. [observation] "Client's face when they saw AI demo" (2026-03-10)
   Lesson: People need to see AI in action, not hear about it
   Usable as: conversation opener, example

Select a story number to see full details, or type a number to use it.
```

## Integration with Other Skills

- **content-writer**: When generating content, checks story-bank for relevant anecdotes:
  ```
  Found relevant story: "Automated my morning routine with AI"
  Include in this article? (yes / no / different story)
  ```
- **hook-library**: Stories generate "story" type hooks automatically
- **newsletter-generator**: "Behind the Scenes" section pulls from story-bank
- **persona-switcher**: Same story told differently for each persona
- **content-dna**: Tracks which story types resonate most

## Story Freshness

Track usage to avoid overusing stories:
- Stories used 3+ times in 30 days → flagged as "heavily used"
- Suggest alternative stories or prompt for new ones
- `used_in` array tracks which content pieces used each story

## Quality Gate

- [ ] Stories are stored with enough detail to be useful later
- [ ] Tags enable accurate search
- [ ] Story types are correctly categorized
- [ ] Lesson/takeaway is captured for each story
- [ ] Usage tracking prevents overuse
- [ ] Story prompts help users dig into memory
