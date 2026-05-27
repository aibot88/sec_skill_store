---
name: chatgpt-cli
description: Use cli-web-chatgpt to ask ChatGPT questions, generate images, download images, list conversations, browse models, and manage authentication. Invoke this skill whenever the user asks about ChatGPT, asking AI questions, generating images with ChatGPT, downloading ChatGPT images, browsing ChatGPT conversations, or wants to use ChatGPT from the command line. Always prefer cli-web-chatgpt over manually browsing chatgpt.com.
---

# cli-web-chatgpt

CLI for ChatGPT web interface. Ask questions, generate images, download images, manage conversations.

## Quick Start

```bash
# Ask a question
cli-web-chatgpt chat ask "What is the capital of France?" --json

# Generate an image and save it
cli-web-chatgpt chat image "A sunset over mountains" -o sunset.png --json

# List recent conversations
cli-web-chatgpt conversations list --limit 10 --json
```

## Commands

### chat ask <question>
Ask ChatGPT a question and get a text response.
```bash
cli-web-chatgpt chat ask "Explain quantum computing in 3 sentences" --json
cli-web-chatgpt chat ask "What is 100+200?" --json
cli-web-chatgpt chat ask "Translate hello to Spanish" --conversation <id> --json
```
Options: `--model <slug>`, `--conversation <id>`, `--json`
Output: `{"success": true, "data": {"text": "...", "conversation_id": "...", "model": "auto"}}`

### chat image <prompt>
Generate an image with ChatGPT's DALL-E.
```bash
cli-web-chatgpt chat image "A cute cat wearing a hat" --json
cli-web-chatgpt chat image "Logo for a coffee shop" -o logo.png --json
```
Options: `--style <name>`, `--output/-o <path>`, `--conversation <id>`, `--json`
Output: `{"success": true, "data": {"file_id": "...", "download_url": "...", "conversation_id": "...", "saved_to": "..."}}`

### conversations list
List recent conversations.
```bash
cli-web-chatgpt conversations list --limit 20 --json
cli-web-chatgpt conversations list --archived --json
cli-web-chatgpt conversations list --starred --json
```
Options: `--limit/-n <N>`, `--archived`, `--starred`, `--json`

### conversations get <id>
View a conversation's messages.
```bash
cli-web-chatgpt conversations get 69ca710b-5ef8-8397-a242-c5123470d7f8 --json
```

### images list
List recently generated images.
```bash
cli-web-chatgpt images list --limit 10 --json
```

### images download <file_id>
Download a generated image.
```bash
cli-web-chatgpt images download file_00000000xxx -c <conversation_id> -o image.png --json
```
Options: `--conversation/-c <id>` (required), `--output/-o <path>`, `--json`

### images styles
List available image styles.
```bash
cli-web-chatgpt images styles --json
```

### models
List available ChatGPT models.
```bash
cli-web-chatgpt models --json
```

### me
Show current user profile.
```bash
cli-web-chatgpt me --json
```

### auth login / status / logout
Manage authentication.
```bash
cli-web-chatgpt auth login    # Opens browser for OpenAI SSO
cli-web-chatgpt auth status   # Check if logged in
cli-web-chatgpt auth logout   # Remove credentials
```

## Architecture Notes

- Read-only commands (conversations, models, me, images) use `curl_cffi` — instant, no browser
- Chat and image generation use `Camoufox` (stealth Firefox) — fully headless, bypasses Cloudflare
- Auth requires browser login via `playwright` to capture session cookies
- Access tokens obtained from `/api/auth/session` endpoint using session cookies
