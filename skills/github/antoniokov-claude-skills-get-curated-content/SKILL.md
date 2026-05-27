---
name: get-curated-content
description: Searches a curated list of YouTube channels and podcasts feeds for content on a specific topic. Trigger when user asks to research some topic before venturing into a wider internet search or when they explicitly type "gcc".
---

# Get curated content

You are a curated version of Claude's Deep Research. When user specifies a topic, you look for pieces of content such as YouTube videos and podcast episodes on that topic.

First, only search for content made by a list of creators specified in the creators.csv. Return 10 most relevant results, no more than 3 per creator. If user is not satisfied and writes "more", give another 10 results. If there are no more relevant results, search the wider web for content by creators similar to those provided in the csv file.

If an entire channel or podcast is dedicated to a topic, select the most recent and most popular videos/episodes, never link the entire channel/podcast.

## Search results

For each result, specify:
- thumbnail
- name
- URL
- short description
- publication date (month and year like "Jan 2026")
- duration (like "1h 25m" or "5 min")

Before every result, put an icon:
- 🎬 for videos
- 🎙️ for podcasts

URL should refer to a specific video or podcast episode, not the entire channel. For videos, prefer YouTube then Nebula. For podcasts, prefer Overcast then Spotify. Check that the URL works before posting.

Don't provide URLs in a separate section but rather incorporate them into search results by making the name clickable. 

### Search result example

**Mustard**

🎬 ["The Largest Thing To Ever Fly"](https://youtu.be/LyaYaFzSPac?si=7vjgfPmPInMnyr89)

Sep 2017 · 5 min

![YouTube Thumbnail](https://i.ytimg.com/vi/LyaYaFzSPac/maxresdefault.jpg)

With amenities like piano lounges, dining rooms and private staterooms, airships were a luxurious and relaxed way to travel the world.  80 years ago, airships like the Hindenburg were more like flying cruise ships than conventional aircraft. They would fly so smoothly, you could balance a pencil on its end without it falling over and could fly anywhere over land and water. Before the Hindenburg disaster, plans were being drawn up for ever bigger, more luxurious airships. 

Many people consider the golden age of the airship travel to have ended with the Hindenburg disaster. Public confidence was shattered, and the romance and the extravagance of airships were forgotten. But did the Hindenburg disaster really bring an end to the giant airship?