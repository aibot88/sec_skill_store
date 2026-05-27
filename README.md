# Sec Skills Store

Static catalog and corpus for cybersecurity-related Codex, Claude Code, and OpenClaw skills.

## Layout

- `scripts/collect_sec_skills.py` crawls Skillstore, ClaudSkills, OpenClawDir, and GitHub fallback search results.
- `scripts/validate_catalog.py` checks the generated catalog and site assets.
- `data/skills.json` is the canonical normalized index.
- `data/sources.json` records source counts and crawl timestamps.
- `skills/` contains downloaded raw skill files grouped by source.
- `site/` is a pure static website for GitHub Pages.

The current site is served from `/site/` when GitHub Pages is configured to publish the repository root.

## Collect

Run a source reachability pass:

```bash
python3 scripts/collect_sec_skills.py --dry-run
```

Run the full resumable collection:

```bash
python3 scripts/collect_sec_skills.py
```

Run validation:

```bash
python3 scripts/validate_catalog.py
```

Serve locally:

```bash
python3 -m http.server 8080
```

Then open `http://127.0.0.1:8080/site/`.

## GitHub Pages

This repository is intended to be public at `aibot88/sec_skill_store` and published with GitHub Pages from the `main` branch root. The root `index.html` redirects to the static site in `site/`.

