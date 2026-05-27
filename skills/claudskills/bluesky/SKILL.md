---
name: bluesky
description: >
  Interact with Bluesky social media from the command line. Use this skill whenever the user
  wants to read or write Bluesky posts, search content or users on Bluesky, manage their
  Interact with Bluesky social media from the command line. Use this skill whenever the user
  wants to read or write Bluesky posts, search content or users on Bluesky, manage their
  Bluesky authentication, like or unlike posts, follow or unfollow users, list followers or
  following, view user profiles, create or delete posts, or automate any Bluesky workflow via
  CLI. Triggers on: "post to Bluesky", "search Bluesky", "read my Bluesky feed", "reply to a
  Bluesky post", "like a post", "follow a user", "view a profile", "list followers",
  "list following", "who follows me", "who do I follow", "who is @handle on Bluesky",
  "who posted about X on Bluesky", "check my Bluesky status", or any reference to bsky_client
  commands.
---

# bsky_client Skill

A CLI for interacting with [Bluesky](https://bsky.app) via the ATProto API.
Built with TypeScript, Commander.js, and [@atproto/api](https://github.com/bluesky-social/atproto).

All commands use `--json` for structured output — this skill is designed for program-to-program communication.

---

## Quick Reference

| Goal                        | Command                                                          |
|-----------------------------|------------------------------------------------------------------|
| Log in                      | `npx bsky_client --json login -u <handle> -p <apppassword>`                |
| Check auth status           | `npx bsky_client --json status`                                     |
| Create a post               | `npx bsky_client --json posts create "<text>"`                      |
| List your posts             | `npx bsky_client --json posts list`                                 |
| Get posts from a user       | `npx bsky_client --json posts from <handle>`                        |
| View a single post          | `npx bsky_client --json posts view <uri>`                           |
| Delete a post               | `npx bsky_client --json posts delete <uri>`                         |
| Reply to a post             | `npx bsky_client --json reply <uri> "<text>"`                       |
| Like a post                 | `npx bsky_client --json like <uri>`                                 |
| Unlike a post               | `npx bsky_client --json unlike <uri>`                               |
| View a user's profile       | `npx bsky_client --json profile [handle]`                           |
| Follow a user               | `npx bsky_client --json follow <handle>`                            |
| Unfollow a user             | `npx bsky_client --json unfollow <handle>`                          |
| List followers              | `npx bsky_client --json followers [handle]`                         |
| List following              | `npx bsky_client --json following [handle]`                         |
| List your saved feeds       | `npx bsky_client --json feed saved`                                 |
| View a custom feed          | `npx bsky_client --json feed view <uri>`                            |
| View your home timeline     | `npx bsky_client --json feed timeline`                              |
| Search posts                | `npx bsky_client --json search posts "<query>"`                     |
| Search users                | `npx bsky_client --json search users "<query>"`                     |
| Advanced search             | `npx bsky_client --json search advanced "<query>" [filters]`        |
| Log out                     | `npx bsky_client --json logout`                                            |

---

## Setup

```bash
# From the package root
cd packages/bsky_client
npm install
npm run build        # compiles TypeScript → dist/

# Run via npm script (dev, no build needed)
npm run dev -- <command>

# Or use the compiled binary
node dist/cli.js <command>
```

---

## Authentication

Bluesky requires an **App Password** (not your main account password).
Generate one at: **Settings → Privacy and Security → App Passwords**.

```bash
# Non-interactive login
npx bsky_client --json login -u jerome-etienne.bsky.social -p xxxx-xxxx-xxxx-xxxx

# Verify session
npx bsky_client --json status

# Clear session
npx bsky_client --json logout
```

Sessions are persisted to `~/.bsky_client/session.json`.
All commands except `logout` require a valid session.

---

## Post Commands

```bash
# Create a new post
npx bsky_client --json posts create "Hello Bluesky!"

# List your own recent posts (default: 10)
npx bsky_client --json posts list
npx bsky_client --json posts list --limit 25
npx bsky_client --json posts list --limit 10 --offset 20

# Get posts from any user
npx bsky_client --json posts from nytimes.com
npx bsky_client --json posts from jerome-etienne.bsky.social --limit 5
npx bsky_client --json posts from jerome-etienne.bsky.social --limit 10 --offset 10

# View a single post by AT-URI
npx bsky_client --json posts view at://did:plc:xyz.../app.bsky.feed.post/abc123

# Delete one of your own posts
npx bsky_client --json posts delete at://did:plc:xyz.../app.bsky.feed.post/abc123
```

---

## Reply

```bash
npx bsky_client --json reply at://did:plc:xyz.../app.bsky.feed.post/abc123 "Great post!"
```

The reply is threaded correctly using the post's CID and root reference.

---

## Like / Unlike

```bash
npx bsky_client --json like at://did:plc:xyz.../app.bsky.feed.post/abc123
npx bsky_client --json unlike at://did:plc:xyz.../app.bsky.feed.post/abc123
```

`unlike` automatically looks up whether you have liked the post and removes it.
Errors if the post is not already liked.

---

## Profile

```bash
# View your own profile (no handle needed)
npx bsky_client --json profile

# View another user's profile
npx bsky_client --json profile jerome-etienne.bsky.social
npx bsky_client --json profile nytimes.com
```

Returns the user's DID, handle, display name, bio, follower/following/post counts, and your relationship with them (following, followed by, muted, blocked).
Defaults to the logged-in user when no handle is given.

---

## Follow / Unfollow

```bash
npx bsky_client --json follow jerome-etienne.bsky.social
npx bsky_client --json unfollow jerome-etienne.bsky.social
```

`unfollow` errors if you are not currently following the user.

## Followers / Following

```bash
# List your followers (default: 10)
npx bsky_client --json followers
npx bsky_client --json followers --limit 25
npx bsky_client --json followers --limit 10 --offset 20

# List another user's followers
npx bsky_client --json followers nytimes.com

# List who you follow
npx bsky_client --json following
npx bsky_client --json following --limit 5

# List who another user follows
npx bsky_client --json following jerome-etienne.bsky.social
```

Both commands default to the authenticated user when no handle is given. Use `--limit` and `--offset` for pagination.

---

## Search Commands

### Posts

```bash
npx bsky_client --json search posts "TypeScript"
npx bsky_client --json search posts "AI" --limit 20
npx bsky_client --json search posts "AI" --limit 10 --offset 20
npx bsky_client --json search posts "open source" --sort top
```

### Users

```bash
npx bsky_client --json search users "jerome"
npx bsky_client --json search users "typescript developer" --limit 5
npx bsky_client --json search users "typescript developer" --limit 10 --offset 5
```

### Advanced Search

```bash
npx bsky_client --json search advanced "AI safety" --author eliezer.bsky.social
npx bsky_client --json search advanced "TypeScript" --since 2024-01-01 --until 2024-06-30
npx bsky_client --json search advanced "news" --type replies --language en
npx bsky_client --json search advanced "atproto" --limit 30 --author bluesky.com --language en
```

**Advanced flags:**

| Flag               | Description                                         |
|--------------------|-----------------------------------------------------|
| `-l, --limit`      | Max results (default: 10)                           |
| `-o, --offset`     | Number of results to skip (default: 0)              |
| `-a, --author`     | Filter by author handle                             |
| `--since`          | Results after date (YYYY-MM-DD)                     |
| `--until`          | Results before date (YYYY-MM-DD)                    |
| `-t, --type`       | Content type: `posts`, `replies`, `reposts`         |
| `--language`       | Language code: `en`, `fr`, `es`, `de`, etc.         |

---

## Feed Commands

```bash
# List your saved/pinned feeds (shows display names and AT-URIs)
npx bsky_client --json feed saved

# View posts from a specific feed (URI from feed saved or feed discover)
npx bsky_client --json feed view at://did:plc:xxx/app.bsky.feed.generator/build-in-public
npx bsky_client --json feed view <uri> --limit 20

# View your home timeline (posts from people you follow)
npx bsky_client --json feed timeline
npx bsky_client --json feed timeline --limit 25

# Browse algorithmically suggested feeds
npx bsky_client --json feed discover
npx bsky_client --json feed discover --limit 20
```

**Typical workflow to read a subscribed feed:**
1. `feed saved` — find the AT-URI of "-Build in public" (or any saved feed)
2. `feed view <uri>` — read its posts

---

## Install

```bash
# Install the bsky_client skill into the current agent folder
npx bsky_client --json install --skills
```

Copies the `skills/bsky-cli/` directory into the current working directory so it can be used by a skillmd_runner agent folder.
