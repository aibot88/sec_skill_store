---
name: "google-labs-extension"
description: "Access Google's experimental AI tools (Stitch, Whisk, Flow, MusicFX, ImageFX) with OAuth authentication and browser automation. Use for visual storytelling, image remixing, animation, and compound workflows that combine multiple tools."
version: "1.0.0"
author: "@aegntic"
tags: ["google", "ai-tools", "creative", "browser-automation", "oauth"]
trigger_patterns:
  - "google labs"
  - "stitch"
  - "whisk"
  - "flow"
  - "musicfx"
  - "imagefx"
  - "visual storytelling"
  - "image remix"
  - "ai animation"
  - "creative workflow"
allowed_tools: ["Bash", "Read", "Write", "Edit"]
---

# Google Suite Labs Extension

## Overview

Access Google's cutting-edge AI experiments: **Stitch**, **Whisk**, **Flow**, **MusicFX**, **ImageFX**, and more. This extension provides OAuth authentication, browser automation, and compound workflows.

## 🚀 Featured Tools

### **🧵 Stitch** - Visual Storytelling
Transform ideas into visual narratives with AI-generated imagery.
- **Input**: Text prompts, concept descriptions
- **Output**: Visual storyboards, image sequences
- **Compound Use**: Feed Stitch output into Whisk for refinement

### **🎨 Whisk** - Creative Remix
Blend, remix, and transform images with AI-powered creativity.
- **Input**: Images, style references, creative directions
- **Output**: Remixes, variations, style transfers
- **Compound Use**: Use Whisk outputs as Flow inputs for animation

### **🌊 Flow** - Motion & Animation
Bring static visuals to life with AI-generated motion and animation.
- **Input**: Images, visual concepts, style preferences
- **Output**: Animated sequences, motion graphics
- **Compound Use**: Animate Stitch/Whisk outputs for complete stories

## Authentication

```bash
# One-time OAuth setup
glabs auth
```

## Usage

### Individual Tools
```bash
# Stitch
glabs stitch "A cyberpunk city at sunset"

# Whisk
glabs whisk ./my-image.jpg --style "vaporwave"

# Flow
glabs flow ./my-image.jpg --duration 5s
```

### Compound Workflows
```bash
# Full pipeline
glabs pipeline -i "floating garden" -t stitch,whisk,flow

# Batch processing
glabs batch -i ./images/ -w "stitch→whisk→flow"
```

### Interactive Mode
```bash
glabs interactive
```

## Workflow Examples

**Visual Story Pipeline:**
```
Idea → Stitch → Whisk → Flow
```

**Creative Campaign:**
```
Brief → Text → Visuals → Variations → Motion
```

---

**NPM**: @aegntic/google-labs-extension