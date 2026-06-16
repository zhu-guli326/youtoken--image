---
name: youtoken-image
description: Generate or edit images synchronously through the Youtoken OpenAI-compatible image API at https://token.youzhuapp.com. Use when the user asks to call the configured image generation API, generate UI images, create raster assets, edit images, test the Youtoken image endpoint, or save generated image files locally. The CLI reads YOUTOKEN_IMAGE_API_KEY from the environment or ~/.codex/youtoken-image.env, supports /v1/images/generations and /v1/images/edits, and handles both b64_json and URL image responses.
---

# Youtoken Image

Generate or edit images through `https://token.youzhuapp.com` and save final image files locally before replying.

## Quick Workflow

1. Confirm `YOUTOKEN_IMAGE_API_KEY` is available. The CLI also accepts `OPENROUTER_ICU_API_KEY` for backward compatibility.
2. Use `scripts/youtoken_image.py`; do not write one-off API callers unless the user explicitly asks.
3. Keep API controls out of the visual prompt. The prompt should describe only subject, scene, style, composition, text, and constraints.
4. Prefer non-streaming mode for this endpoint. The CLI defaults to `--no-stream` and can parse both `b64_json` and returned image `url` fields.
5. Run the command in the foreground and wait for it to exit. If a terminal session remains live, poll until it finishes.
6. Verify the output file exists and render or inspect it when useful.

## CLI

Text-to-image:

```bash
python3 /Users/zzhu/.codex/skills/youtoken-image/scripts/youtoken_image.py generate \
  --prompt "A high fidelity 16:9 To Do app UI concept, soft blue background, rounded mobile cards, playful hand-drawn illustration, no watermark" \
  --output outputs/todo-ui.png \
  --size 1536x864 \
  --quality medium \
  --output-format png
```

Image edit or reference-image generation:

```bash
python3 /Users/zzhu/.codex/skills/youtoken-image/scripts/youtoken_image.py edit \
  --image reference.png \
  --prompt "Use the reference as style inspiration and create a polished mobile To Do UI, preserving the pastel rounded-card visual language" \
  --output outputs/todo-ui-from-reference.png \
  --size 1536x864 \
  --quality medium \
  --output-format png
```

Dry run:

```bash
python3 /Users/zzhu/.codex/skills/youtoken-image/scripts/youtoken_image.py generate \
  --prompt "test image" \
  --output outputs/test.png \
  --dry-run
```

## Defaults

- Base URL: `https://token.youzhuapp.com`
- Model: `gpt-image-2`
- Size: `1024x1024`
- Quality: `medium`
- Output format: `png`
- Streaming: disabled by default for compatibility
- Key file: `~/.codex/youtoken-image.env`

## Parameters

- Use `--size WIDTHxHEIGHT`; dimensions must be divisible by 16 and no more than `3840x2160` pixels.
- Use `--quality low|medium|high|auto`.
- Use `--output-format png|jpeg|webp`.
- Use `--n` for multiple variants of the same prompt.
- Use `--base-url` only when the user asks to override the endpoint.
- Use `--stream` only if the endpoint supports SSE for the requested model.

## Errors

- `401`: the key is missing or invalid; ask for a valid key.
- `400`: fix request parameters before retrying.
- `503 No available compatible accounts`: service-side capacity/account issue; local configuration may still be correct.
- URL download failures: retry with non-streaming mode; the CLI already sends browser-like download headers for returned image URLs.

Read `references/api.md` only when you need complete API details or script internals.
