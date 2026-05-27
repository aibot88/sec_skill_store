#!/usr/bin/env python3
"""Validate the generated sec skills catalog."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FIELDS = {
    "name",
    "slug",
    "source",
    "source_url",
    "download_url",
    "local_path",
    "license",
    "description",
    "cwe",
    "owasp",
    "security_domains",
    "business_domains",
    "confidence",
    "download_status",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    skills_path = ROOT / "data" / "skills.json"
    sources_path = ROOT / "data" / "sources.json"
    site_files = [
        ROOT / "site" / "index.html",
        ROOT / "site" / "styles.css",
        ROOT / "site" / "app.js",
    ]

    if not skills_path.exists():
        fail("data/skills.json is missing")
    if not sources_path.exists():
        fail("data/sources.json is missing")
    for path in site_files:
        if not path.exists():
            fail(f"{path.relative_to(ROOT)} is missing")

    payload = json.loads(skills_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        fail("data/skills.json must be a JSON array")
    if not payload:
        fail("data/skills.json is empty")

    seen = set()
    missing_local = []
    for index, item in enumerate(payload):
        missing = REQUIRED_FIELDS - set(item)
        if missing:
            fail(f"entry {index} is missing fields: {sorted(missing)}")

        key = (item["source"], item["slug"])
        if key in seen:
            fail(f"duplicate source/slug entry: {key}")
        seen.add(key)

        status = item["download_status"]
        local_path = item.get("local_path") or ""
        if status in {"downloaded", "partial"} and not local_path:
            missing_local.append(item["slug"])
        if local_path:
            local_file = ROOT / local_path
            if not local_file.exists():
                missing_local.append(f"{item['slug']} -> {local_path}")

    if missing_local:
        fail("entries refer to missing local files: " + ", ".join(missing_local[:10]))

    source_payload = json.loads(sources_path.read_text(encoding="utf-8"))
    if "sources" not in source_payload:
        fail("data/sources.json must contain a sources object")

    print(f"OK: {len(payload)} skills, {len(source_payload['sources'])} sources")


if __name__ == "__main__":
    main()
