# Repository Guidelines

## Project Structure & Module Organization
This repository contains a Hugo static site plus utility scripts.

- `content/`: Markdown content pages (for example `content/ai-agent-methodology.md`).
- `layouts/`: Hugo templates (`_default/` for shared page types, `index.html` for home).
- `static/`: Static assets served as-is (for example `static/css/site.css`).
- `scripts/`: Utility scripts, currently `scripts/fetch_subtitles.py`.
- `subtitles/`: Generated `.srt` files used as source material.
- `.github/workflows/`: CI/CD workflows (GitHub Pages deploy via `hugo.yml`).

Keep changes scoped to the correct directory boundary (content vs. layout vs. script).

## Build, Test, and Development Commands
- `hugo server -D`: Run local dev server with drafts.
- `hugo --minify`: Build production output into `public/`.
- `uv run scripts/fetch_subtitles.py "<youtube-url-or-id>"`: Fetch subtitles and write `.srt`.
- `uv run scripts/fetch_subtitles.py <id> --out-dir subtitles --languages zh-TW zh-Hant zh en`: Use explicit language priority and output path.

If `hugo` is not installed locally, install it before running site commands.

## Coding Style & Naming Conventions
- Markdown content should be concise, sectioned, and use clear headings.
- Python should follow existing script style: type hints, small focused functions, and explicit error messages.
- Use descriptive filenames (`ai-agent-methodology.md`, `fetch_subtitles.py`).
- Prefer kebab-case for content file names and lowercase paths.

## Testing Guidelines
There is no formal automated test suite yet.

- For site changes: run `hugo --minify` and verify pages render without template errors.
- For subtitle script changes: run the script with a known video ID and confirm output naming and file creation.
- Treat build/runtime checks as required before claiming completion.

## Commit & Pull Request Guidelines
Follow the current commit style in history: short, imperative, and scoped (for example `Add ...`, `Move ...`, `Force ...`, `Scaffold ...`).

PRs should include:
- What changed and why.
- Affected paths (for example `layouts/_default/single.html`).
- Verification performed (commands and outcomes).
- Screenshots for visible UI/layout changes when relevant.
