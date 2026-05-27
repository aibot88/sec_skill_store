---
name: int-youtube
description: "Query YouTube Data API v3 — channel stats, recent videos, top videos, comments. Supports multi-account (OAuth or API Key). Use when user asks about YouTube metrics, YouTube channel, subscribers, views, videos, engagement, or any reference to YouTube analytics."
---

# YouTube Data API v3

YouTube integration to monitor Evolution channels and others. Supports multiple accounts via OAuth (Social Auth App) or API Key.

## Setup

Accounts configured via `make social-auth` (OAuth login) or manually in `.env`:
```env
SOCIAL_YOUTUBE_1_LABEL=Evolution API
SOCIAL_YOUTUBE_1_ACCESS_TOKEN=ya29...
SOCIAL_YOUTUBE_1_CHANNEL_ID=UC9kZHm3TnEt41ztGOLyQO9g
SOCIAL_YOUTUBE_1_REFRESH_TOKEN=1//0h...
```

## API Client

```bash
python3 {project-root}/.claude/skills/int-youtube/scripts/youtube_client.py <command> [args]
```

### Commands

```bash
# List configured accounts
youtube_client.py accounts

# Channel stats (subscribers, views, total videos)
youtube_client.py channel_stats [account_label_or_index]

# Last N videos with metrics (via playlistItems — 3 units)
youtube_client.py recent_videos [account] [N]

# Top N videos by views
youtube_client.py top_videos [account] [N]

# Stats for specific videos
youtube_client.py video_stats VIDEO_ID [VIDEO_ID...]

# Comments on a video
youtube_client.py comments VIDEO_ID [N]

# Summary of all accounts
youtube_client.py summary
```

### Output JSON exemplo
```json
{
  "account": "Evolution API",
  "channel_id": "UC9kZHm3TnEt41ztGOLyQO9g",
  "subscribers": 7450,
  "total_views": 132462,
  "video_count": 27,
  "videos": [
    {
      "id": "abc",
      "title": "...",
      "published": "2026-...",
      "views": 7180,
      "likes": 500,
      "comments": 164,
      "engagement_rate": 9.25,
      "url": "https://youtube.com/watch?v=abc"
    }
  ]
}
```

## Key metrics
- Subscribers (daily/weekly/monthly delta)
- Total views and per video
- Engagement rate: (likes + comments) / views
- Best video of the period
- Publishing frequency
- Recent comments (sentiment)

## Quota
- 10,000 units/day (resets at midnight Pacific Time)
- `playlistItems`: 1 unit (used instead of `search` which costs 100)
- `channels`, `videos`, `commentThreads`: 1 unit each
- Each pagination is charged again
