---
name: popiskill-image-img2img-basic-v1
description: Transform one existing image into a new image through the PopiArt runtime baseline. Use this when the user already has a source image and wants the most direct image-to-image path for redraws, style transfer, or pipeline validation.
tags:
  - official
  - runtime
  - image
  - img2img
  - basic
version: v1
model_type: image
estimated_duration_s: 150
default_profile: true
profile_description: Official PopiArt runtime baseline for single-image image-to-image generation.
---

# PopiArt Image To Image Basic

This is an official PopiArt runtime catalog skill.

- `Popiart_skillhub` owns the public skill definition.
- `popiartServer` owns source resolution, execution, jobs, artifacts, and stable media URLs.
- `PopiNewAPI` owns provider routing and upstream model access.
- `popiartcli` owns source upload ergonomics, `run`, `jobs`, and `artifacts`.

Use it when the goal is to:

- take one existing image and restyle or redraw it
- validate that image-conditioned generation works
- make one lightweight variation from a PopiArt artifact or a stable image URL

Do not use it for:

- text-only generation
- mask-heavy multi-step retouch pipelines
- video generation

## Required input

- `prompt`: the transformation intent
- one image source:
  - `source_artifact_id`, or
  - `image_url`, or
  - `reference_image_url`

## Optional input

- `strength`
- `style`
- `size`
- `aspect_ratio`
- `seed`
- `notes`

## Workflow

1. Prefer `source_artifact_id` when the source image already comes from PopiArt.
2. Use `image_url` or `reference_image_url` only when the source already lives at a stable URL.
3. Build the smallest valid JSON payload.
4. Run the skill through `popiart`.
5. Wait for completion and pull the output artifact if needed.

## Command pattern

```sh
popiart run popiskill-image-img2img-basic-v1 --input @params.json --wait
```

Inline example:

```sh
popiart run popiskill-image-img2img-basic-v1 --input '{"prompt":"convert this into a watercolor illustration","source_artifact_id":"art_123","strength":0.6}' --wait
```

## Payload template

```json
{
  "prompt": "convert this into a watercolor illustration",
  "source_artifact_id": "art_123",
  "strength": 0.6,
  "style": "soft pastel",
  "aspect_ratio": "1:1",
  "seed": 42
}
```

## Output handling

After the job finishes:

- read `job_id`
- inspect `artifact_ids`
- inspect `url` or `media_id` when a stable media URL is returned
- use `popiart artifacts pull <artifact-id>` to save the result locally

## Operating guidance

- For local source files, upload first with `popiart artifacts upload ./source.png --role source`.
- `reference_image_url` is a compatibility alias for `image_url`.
- If no source image exists yet, switch to `popiskill-image-text2image-basic-v1`.
- If the user wants motion from the result, switch to `popiskill-video-image2video-basic-v1`.
