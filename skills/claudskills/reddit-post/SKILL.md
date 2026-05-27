---
name: reddit-post
description: "Research a subreddit topic, draft a post in authentic Reddit tone, and submit via real Chrome browser. Use when the user wants to post on Reddit — asking a question, sharing experience, or starting a discussion."
allowed-tools: Bash(agent-browser:*), Bash(pkill:*), Bash(sleep:*), WebSearch, Read, Write, Glob, Grep, Agent
---

# Reddit Post Skill

Create and submit Reddit posts with research-backed content and authentic tone.

## Workflow

### Step 1: Research the subreddit

Before writing anything, understand the conversation landscape:

1. Launch /real-browser (follow its skill.md exactly — Chrome Beta + agent-browser --session)
2. Navigate to the target subreddit's search page
3. Search for 2-3 keyword variations related to the topic
4. Extract post URLs using JS eval (don't rely on snapshot links for navigation):
   ```bash
   agent-browser --session reddit eval --stdin <<'EVALEOF'
   JSON.stringify(
     Array.from(document.querySelectorAll('a[href*="/comments/"]'))
       .map(a => ({ title: a.textContent.trim(), href: a.href }))
       .filter(a => a.title.length > 10)
       .filter((v, i, a) => a.findIndex(x => x.href === v.href) === i)
   )
   EVALEOF
   ```
5. Open the top 3-5 most relevant posts in new tabs and extract content:
   ```bash
   agent-browser --session reddit tab new "<url>"
   agent-browser --session reddit wait 5000
   agent-browser --session reddit eval --stdin <<'EVALEOF'
   const post = document.querySelector('shreddit-post');
   const title = post ? post.getAttribute('post-title') : '';
   const body = document.querySelector('[slot="text-body"]');
   const comments = Array.from(document.querySelectorAll('shreddit-comment')).map(c => {
     const author = c.getAttribute('author');
     const thing = c.querySelector('[slot="comment"]');
     return author + ': ' + (thing ? thing.textContent.trim().substring(0, 600) : '');
   });
   JSON.stringify({ title, body: body ? body.textContent.trim().substring(0, 2000) : '', comments: comments.slice(0, 15) });
   EVALEOF
   ```
6. Summarize key findings to the user before drafting

### Step 2: Draft the post

Write the post following Reddit tone guidelines:

**Title:**
- Short, specific, genuine — not clickbait
- Ask a real question or state a clear topic
- Under 100 characters preferred

**Body tone — sound like a real person, not AI:**
- Write in first person, casual but not sloppy
- Use contractions (I'm, can't, doesn't, it's)
- Be specific about your experience — mention real tools, real error messages, real frustrations
- Mild profanity is fine if it fits (damn, hell) — Reddit is casual
- DON'T use: "I'd love to hear", "Thanks in advance", "Happy to", "Pretty solid", "Curious to hear"
- DON'T use bullet-heavy corporate formatting — mix paragraphs and lists naturally
- DON'T hedge everything — have opinions, state what worked and what didn't
- Reference what you found in the sub ("I saw some people recommending X, but...")
- End with 1-2 focused questions, not a numbered list of 5

**Body structure:**
- Open with your situation in 1-2 sentences
- Describe the problem concretely (what happens, not what "might" happen)
- Say what you've tried and why it didn't work
- Reference existing discussions you found
- Ask your actual question(s)

**Run /de-ai on the draft** if it sounds too polished or AI-generated.

### Step 3: Show draft to user

Present the title and body to the user for review. Wait for approval or edits before proceeding.

### Step 4: Submit via browser

1. Navigate to the subreddit's submit page:
   ```bash
   agent-browser --session reddit eval "window.location.href='https://www.reddit.com/r/<subreddit>/submit'"
   agent-browser --session reddit wait --load networkidle
   agent-browser --session reddit wait 3000
   ```
2. Snapshot to find form fields:
   ```bash
   agent-browser --session reddit snapshot -i
   ```
3. Fill title and body using refs from snapshot (typically @e18 for title, @e20 for body — but always verify via snapshot)
4. Add flair if required (check for "Add flair" button)
5. Screenshot the draft for user confirmation:
   ```bash
   agent-browser --session reddit screenshot /tmp/reddit-post-draft.png --full
   ```
6. Show screenshot to user and ask: "Ready to post?"
7. Only click Post after explicit user confirmation

## Important notes

- ALWAYS use `--session reddit` for all agent-browser commands
- Follow /real-browser skill for Chrome Beta launch (never use bare `agent-browser open`)
- Reddit's new UI uses shadow DOM — standard CSS selectors often fail, use the JS eval patterns above
- After any navigation, wait 3-5s before interacting (Reddit is slow to hydrate)
- If the subreddit requires flair, the Post button stays disabled until flair is set

## Arguments

Usage: `/reddit-post <subreddit> <topic description>`

Example: `/reddit-post ClaudeCode Looking for reliable browser automation setups — my current agent-browser setup fails 50% of the time`
