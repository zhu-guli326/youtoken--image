# Youtoken Image API

## Endpoints

- Generate: `POST https://token.kynexis.cc/v1/images/generations`
- Edit: `POST https://token.kynexis.cc/v1/images/edits`

`--base-url` accepts either `https://token.kynexis.cc` or `https://token.kynexis.cc/v1`.

## Authentication

Preferred:

```bash
export YOUTOKEN_IMAGE_API_KEY="..."
```

Local file fallback:

```text
~/.codex/youtoken-image.env
YOUTOKEN_IMAGE_API_KEY="..."
```

The CLI also reads `OPENROUTER_ICU_API_KEY` for backward compatibility.

## Request Payload

Common JSON fields:

```json
{
  "model": "gpt-image-2",
  "prompt": "visual prompt only",
  "size": "1024x1024",
  "quality": "medium",
  "n": 1,
  "output_format": "png",
  "stream": false
}
```

For local image edits, the CLI uses multipart `image[]` uploads. For remote references, it can send JSON `images` entries from `--file-id` or `--image-url`.

## Response Handling

The endpoint may return either:

```json
{"data":[{"b64_json":"..."}]}
```

or:

```json
{"data":[{"url":"https://.../image.png"}]}
```

`scripts/youtoken_image.py` handles both. For URL results it downloads the image with browser-like headers and writes the requested output path.

## Useful Commands

Generate:

```bash
python3 scripts/youtoken_image.py generate \
  --prompt "A polished mobile app UI mockup, soft pastel background, no watermark" \
  --output output/youtoken-image/app-ui.png \
  --size 1536x864 \
  --quality medium \
  --output-format png
```

Edit:

```bash
python3 scripts/youtoken_image.py edit \
  --image reference.png \
  --prompt "Use this reference style to create a new To Do app UI mockup" \
  --output output/youtoken-image/edit.png \
  --size 1536x864 \
  --quality medium \
  --output-format png
```

Dry run:

```bash
python3 scripts/youtoken_image.py generate \
  --prompt "test" \
  --output output/youtoken-image/test.png \
  --dry-run
```

## Notes

- Keep API parameters out of the prompt.
- Use non-streaming mode unless explicitly testing SSE.
- For 16:9, use `1536x864`, `2048x1152`, or `3840x2160`.
- Treat `503 No available compatible accounts` as a service-side availability issue.
