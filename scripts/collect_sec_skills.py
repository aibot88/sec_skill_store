#!/usr/bin/env python3
"""Collect cybersecurity-related AI skills into a static catalog.

The collector intentionally uses only Python's standard library so the
repository remains easy to run on a fresh machine and on GitHub Actions.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SKILLS_DIR = ROOT / "skills"
USER_AGENT = "sec-skill-store/1.0 (+https://github.com/aibot88/sec_skill_store)"

SECURITY_TERMS = [
    "security",
    "cyber security",
    "cybersecurity",
    "code security",
    "secure coding",
    "安全",
    "vulnerability",
    "vulnerabilities",
    "cwe",
    "owasp",
    "cve",
    "sast",
    "secret",
    "secrets",
    "appsec",
    "auth",
    "authorization",
    "authentication",
    "xss",
    "sql injection",
    "sqli",
    "injection",
    "csrf",
    "ssrf",
    "crypto",
    "threat",
    "pentest",
    "red team",
    "privacy",
    "compliance",
    "malware",
    "reverse engineering",
    "binary",
]

STRONG_TERMS = [
    "cwe",
    "owasp",
    "cve",
    "sast",
    "xss",
    "sql injection",
    "sqli",
    "csrf",
    "ssrf",
    "secrets",
    "hardcoded",
    "vulnerability",
    "pentest",
    "red team",
    "static analysis",
    "threat model",
    "security audit",
]

CWE_RULES = [
    (r"\bsql injection\b|\bsqli\b", "CWE-89"),
    (r"\bxss\b|cross[- ]site scripting", "CWE-79"),
    (r"command injection|os command", "CWE-78"),
    (r"path traversal|directory traversal", "CWE-22"),
    (r"deseriali[sz]ation", "CWE-502"),
    (r"csrf|cross[- ]site request forgery", "CWE-352"),
    (r"ssrf|server[- ]side request forgery", "CWE-918"),
    (r"xxe|external entity", "CWE-611"),
    (r"open redirect", "CWE-601"),
    (r"hardcoded|secret|api key|credential", "CWE-798"),
    (r"weak crypto|insecure crypto|cryptograph", "CWE-327"),
    (r"tls|certificate validation", "CWE-295"),
    (r"authenti", "CWE-287"),
    (r"authori[sz]|access control|idor", "CWE-862"),
    (r"file upload|unrestricted upload", "CWE-434"),
    (r"dependency|third[- ]party|supply chain|known vulnerab", "CWE-1104"),
    (r"logging|sensitive data exposure|pii", "CWE-532"),
    (r"cors", "CWE-942"),
    (r"rate limit|brute force", "CWE-307"),
]

OWASP_RULES = [
    (r"access control|authori[sz]|idor|privilege", "A01: Broken Access Control"),
    (r"crypto|cryptograph|secret|password|tls", "A02: Cryptographic Failures"),
    (r"injection|sql|xss|command injection|ssrf|xxe", "A03: Injection"),
    (r"insecure design|threat model|architecture", "A04: Insecure Design"),
    (r"misconfig|headers|cors|cloud|kubernetes|terraform|iac", "A05: Security Misconfiguration"),
    (r"dependency|cve|vulnerable component|supply chain", "A06: Vulnerable and Outdated Components"),
    (r"authenti|session|login|identity", "A07: Identification and Authentication Failures"),
    (r"integrity|supply chain|ci/cd|artifact|provenance", "A08: Software and Data Integrity Failures"),
    (r"logging|monitoring|incident|alert", "A09: Security Logging and Monitoring Failures"),
    (r"ssrf", "A10: Server-Side Request Forgery"),
]

SECURITY_DOMAIN_RULES = [
    (r"cwe|owasp|vulnerab|sast|static analysis|code review|xss|sql injection|injection", "Application Security"),
    (r"dependency|cve|supply chain|sbom|package|npm|pypi|maven", "Supply Chain"),
    (r"secret|credential|api key|token|password", "Secrets Management"),
    (r"authenti|authori[sz]|access control|identity|iam|acl|rbac", "Identity and Access"),
    (r"cloud|aws|azure|gcp|kubernetes|terraform|docker|iac|container", "Cloud and IaC"),
    (r"ai security|agent security|skill security|prompt injection|llm|model security|mcp|clawhub", "AI and Agent Security"),
    (r"privacy|pii|gdpr|hipaa|anonymi[sz]ation|redact", "Privacy and Data Protection"),
    (r"binary|reverse engineering|malware|forensic", "Reverse Engineering and Malware"),
    (r"pentest|red team|exploit|attack path", "Offensive Security"),
    (r"incident|monitoring|detection|siem|threat", "Detection and Response"),
    (r"compliance|soc2|pci|nist|iso", "Compliance"),
    (r"crypto|encryption|certificate|tls", "Cryptography"),
]

BUSINESS_DOMAIN_RULES = [
    (r"security audit|audit|review|code review|sast|scan", "Code Audit"),
    (r"secure coding|fix|remediation|hardening|best practices", "Secure Coding"),
    (r"dependency|cve|supply chain|sbom", "Dependency Scanning"),
    (r"compliance|soc2|pci|nist|gdpr|hipaa|iso", "Compliance"),
    (r"incident|monitoring|alert|detection|response", "Incident Response"),
    (r"pentest|red team|exploit|attack path", "Pentest and Red Team"),
    (r"binary|reverse engineering|malware", "Binary and RE"),
    (r"agent security|skill security|prompt injection|llm|model security|mcp|skill guard|clawhub", "Skill and Agent Security"),
    (r"privacy|pii|redact|anonymi[sz]e", "Privacy Operations"),
    (r"cloud|kubernetes|terraform|docker|iac", "Cloud Security"),
    (r"threat model|requirements|design", "Security Architecture"),
]


@dataclass
class Candidate:
    source: str
    slug: str
    name: str
    description: str = ""
    category: str = ""
    license: str = ""
    source_url: str = ""
    download_url: str = ""
    external_source_url: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def request(url: str, *, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def request_text(url: str, *, timeout: int = 30) -> str:
    return request(url, timeout=timeout).decode("utf-8", errors="replace")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def safe_slug(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value[:140] or "unnamed"


def text_matches(text: str) -> bool:
    lower = text.lower()
    return any(term.lower() in lower for term in SECURITY_TERMS)


def extract_cwe(text: str) -> list[str]:
    found = {m.upper().replace("CWE ", "CWE-") for m in re.findall(r"CWE[- ]?\d{1,5}", text, flags=re.I)}
    lower = text.lower()
    for pattern, cwe in CWE_RULES:
        if re.search(pattern, lower, flags=re.I):
            found.add(cwe)
    return sorted(found, key=lambda item: int(re.search(r"\d+", item).group(0)))


def classify_by_rules(text: str, rules: list[tuple[str, str]]) -> list[str]:
    lower = text.lower()
    return sorted({label for pattern, label in rules if re.search(pattern, lower, flags=re.I)})


def confidence(candidate: Candidate, content: str) -> float:
    text = " ".join([
        candidate.name,
        candidate.slug,
        candidate.description,
        candidate.category,
        candidate.source,
        content[:20000],
    ]).lower()
    score = 0.18
    if "security" in candidate.category.lower():
        score += 0.22
    if any(term in candidate.slug.lower() or term in candidate.name.lower() for term in ["security", "sec", "cve", "cwe", "owasp", "sast", "pentest"]):
        score += 0.2
    strong_hits = sum(1 for term in STRONG_TERMS if term in text)
    score += min(0.3, strong_hits * 0.045)
    if extract_cwe(text):
        score += 0.1
    if classify_by_rules(text, OWASP_RULES):
        score += 0.08
    return min(1.0, round(score, 2))


def html_unescape(value: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", value)).strip()


def unique_candidates(candidates: Iterable[Candidate]) -> list[Candidate]:
    seen: dict[tuple[str, str], Candidate] = {}
    for candidate in candidates:
        key = (candidate.source, candidate.slug)
        if key not in seen:
            seen[key] = candidate
        else:
            existing = seen[key]
            for attr in ["description", "license", "source_url", "download_url", "external_source_url", "category"]:
                if not getattr(existing, attr) and getattr(candidate, attr):
                    setattr(existing, attr, getattr(candidate, attr))
            existing.metadata.update(candidate.metadata)
    return list(seen.values())


def parse_skillstore_list(html_text: str) -> list[str]:
    slugs = set()
    for match in re.finditer(r'href="(?:/[^"]*)?/skills/([A-Za-z0-9_.-]+)"', html_text):
        slugs.add(match.group(1))
    for match in re.finditer(r"slug:&quot;([A-Za-z0-9_.-]+)&quot;|slug:\"([A-Za-z0-9_.-]+)\"", html_text):
        slugs.add(match.group(1) or match.group(2))
    return sorted(slugs)


def parse_ld_json_blocks(html_text: str) -> list[dict[str, Any]]:
    blocks = []
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html_text, flags=re.S):
        try:
            value = json.loads(html.unescape(raw))
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            blocks.append(value)
    return blocks


def github_raw_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc != "github.com":
        return url
    parts = parsed.path.strip("/").split("/")
    if len(parts) >= 5 and parts[2] == "blob":
        owner, repo, _, branch = parts[:4]
        rest = "/".join(parts[4:])
        return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{rest}"
    return url


def parse_github_tree(url: str) -> tuple[str, str, str, str] | None:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc != "github.com":
        return None
    parts = parsed.path.strip("/").split("/")
    if len(parts) < 5 or parts[2] != "tree":
        return None
    owner, repo, _, branch = parts[:4]
    path = "/".join(parts[4:])
    return owner, repo, branch, path


def parse_github_blob(url: str) -> tuple[str, str, str, str] | None:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc != "github.com":
        return None
    parts = parsed.path.strip("/").split("/")
    if len(parts) < 5 or parts[2] != "blob":
        return None
    owner, repo, _, branch = parts[:4]
    path = "/".join(parts[4:])
    return owner, repo, branch, path


def github_api_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if not token and shutil.which("gh"):
        try:
            token = subprocess.check_output(["gh", "auth", "token"], text=True, timeout=10).strip()
        except (subprocess.SubprocessError, OSError):
            token = ""
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def request_json(url: str, headers: dict[str, str] | None = None) -> Any:
    all_headers = {"User-Agent": USER_AGENT}
    if headers:
        all_headers.update(headers)
    req = urllib.request.Request(url, headers=all_headers)
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download_github_directory(tree_url: str, dest_dir: Path) -> tuple[str, str]:
    parsed = parse_github_tree(tree_url)
    if not parsed:
        return "failed", "not a GitHub tree URL"
    owner, repo, branch, path = parsed
    api_path = urllib.parse.quote(path, safe="/")
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{api_path}?ref={urllib.parse.quote(branch)}"
    headers = github_api_headers()
    dest_dir.mkdir(parents=True, exist_ok=True)
    downloaded = 0

    def walk(contents_url: str, relative_base: Path) -> None:
        nonlocal downloaded
        items = request_json(contents_url, headers)
        if isinstance(items, dict):
            items = [items]
        for item in items:
            item_type = item.get("type")
            name = item.get("name", "")
            if item_type == "dir":
                walk(item["url"], relative_base / name)
            elif item_type == "file":
                target = dest_dir / relative_base / name
                if target.exists() and target.stat().st_size > 0:
                    downloaded += 1
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                download_url = item.get("download_url")
                if not download_url:
                    continue
                target.write_bytes(request(download_url))
                downloaded += 1

    walk(url, Path())
    return ("downloaded" if downloaded else "partial"), f"{downloaded} files"


def download_single_file(url: str, target: Path) -> tuple[str, str]:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.stat().st_size > 0:
        return "downloaded", "cached"
    try:
        target.write_bytes(request(github_raw_url(url)))
    except Exception as exc:  # noqa: BLE001
        return "failed", str(exc)
    return "downloaded", "1 file"


def collect_claudskills() -> tuple[list[Candidate], dict[str, Any]]:
    url = "https://claudskills.com/data/skills.json"
    payload = request_json(url)
    all_skills = payload.get("skills", [])
    candidates = []
    for item in all_skills:
        haystack = " ".join([
            item.get("slug", ""),
            item.get("name", ""),
            item.get("description", ""),
            item.get("category", ""),
            item.get("subcategory", ""),
            " ".join(item.get("tags", []) or []),
        ])
        if not text_matches(haystack):
            continue
        slug = item.get("slug") or safe_slug(item.get("name", "claudskill"))
        candidates.append(
            Candidate(
                source="claudskills",
                slug=safe_slug(slug),
                name=item.get("name") or slug,
                description=item.get("description", ""),
                category=item.get("category", ""),
                license=item.get("license", ""),
                source_url=f"https://claudskills.com/skills/{slug}/",
                download_url=f"https://claudskills.com/skills/{slug}/SKILL.md",
                metadata={"subcategory": item.get("subcategory", ""), "featured": item.get("featured", False)},
            )
        )
    return candidates, {"url": url, "total": len(all_skills), "candidates": len(candidates)}


def collect_openclaw() -> tuple[list[Candidate], dict[str, Any]]:
    candidates = []
    seen_hrefs = set()
    pages = []
    for page in range(1, 20):
        url = f"https://openclawdir.com/skills?category=Security&sort=popular&page={page}"
        text = request_text(url)
        pages.append(url)
        matches = list(
            re.finditer(
                r'<a href="(/skills/[^"]+)" class="card[\s\S]*?<div class="card-title">([\s\S]*?)</div>[\s\S]*?<div class="card-desc">([\s\S]*?)</div>[\s\S]*?<span class="card-tag">([\s\S]*?)</span>',
                text,
            )
        )
        new_count = 0
        for match in matches:
            href, title, desc, category = match.groups()
            if href in seen_hrefs:
                continue
            seen_hrefs.add(href)
            new_count += 1
            slug = href.rstrip("/").split("/")[-1]
            candidates.append(
                Candidate(
                    source="openclawdir",
                    slug=safe_slug(slug),
                    name=html_unescape(title),
                    description=html_unescape(desc),
                    category=html_unescape(category),
                    source_url=f"https://openclawdir.com{href}",
                    metadata={"listing_page": url},
                )
            )
        if not matches or new_count == 0:
            break
    return candidates, {"urls": pages, "candidates": len(candidates)}


def enrich_openclaw(candidate: Candidate) -> Candidate:
    try:
        text = request_text(candidate.source_url)
    except Exception as exc:  # noqa: BLE001
        candidate.metadata["detail_error"] = str(exc)
        return candidate
    githubs = re.findall(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+[^\"'<>\s]*", text)
    githubs = [html.unescape(url) for url in githubs]
    skill_links = [url for url in githubs if "SKILL.md" in url or "/tree/" in url]
    if skill_links:
        candidate.external_source_url = skill_links[0]
        candidate.download_url = skill_links[0]
    return candidate


def collect_skillstore() -> tuple[list[Candidate], dict[str, Any]]:
    base_urls = [
        "https://skillstore.io/skills?category=security&tools=codex",
        "https://skillstore.io/zh-hans/skills?category=security&tools=codex",
    ]
    for term in ["security", "cybersecurity", "code security", "cwe", "owasp", "sast", "vulnerability"]:
        query = urllib.parse.urlencode({"search": term, "tools": "codex"})
        base_urls.append(f"https://skillstore.io/skills?{query}")

    slugs = set()
    fetched = []
    for base in base_urls:
        for page in range(1, 8):
            sep = "&" if "?" in base else "?"
            url = f"{base}{sep}page={page}"
            try:
                text = request_text(url)
            except Exception:
                continue
            fetched.append(url)
            before = len(slugs)
            slugs.update(parse_skillstore_list(text))
            if page > 1 and len(slugs) == before:
                break

    def build_candidate(slug: str) -> Candidate | None:
        page_url = f"https://skillstore.io/skills/{slug}"
        name = slug
        description = ""
        license_value = ""
        metadata: dict[str, Any] = {}
        try:
            detail = request_text(page_url)
            for block in parse_ld_json_blocks(detail):
                if block.get("@type") == "SoftwareApplication":
                    name = block.get("name") or name
                    description = block.get("description") or description
                    license_value = block.get("license") or license_value
                    metadata["application_category"] = block.get("applicationCategory")
            githubs = re.findall(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+[^\"'<>\s]*", detail)
            githubs = [html.unescape(url) for url in githubs]
            skill_links = [url for url in githubs if "SKILL.md" in url or "/tree/" in url]
            if skill_links:
                metadata["github_source"] = skill_links[0]
        except Exception as exc:  # noqa: BLE001
            metadata["detail_error"] = str(exc)

        combined = " ".join([slug, name, description])
        if not text_matches(combined):
            return None
        return Candidate(
            source="skillstore",
            slug=safe_slug(slug),
            name=name,
            description=description,
            category="Security",
            license=license_value,
            source_url=page_url,
            download_url=metadata.get("github_source", ""),
            external_source_url=metadata.get("github_source", ""),
            metadata=metadata,
        )

    candidates = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        for candidate in pool.map(build_candidate, sorted(slugs)):
            if candidate:
                candidates.append(candidate)
    return candidates, {"urls": fetched, "candidates": len(candidates)}


def github_search_candidates(limit_per_query: int) -> tuple[list[Candidate], dict[str, Any]]:
    if limit_per_query <= 0:
        return [], {"enabled": False, "reason": "limit is zero"}
    headers = github_api_headers()
    if "Authorization" not in headers:
        return [], {"enabled": False, "reason": "missing GitHub token"}

    queries = [
        'filename:SKILL.md "security"',
        'filename:SKILL.md "OWASP"',
        'filename:SKILL.md "CWE"',
        'filename:SKILL.md "CVE"',
        'filename:SKILL.md "SAST"',
        'filename:SKILL.md "vulnerability"',
        'filename:SKILL.md "cybersecurity"',
        'filename:SKILL.md "安全"',
    ]
    candidates: list[Candidate] = []
    raw_items = 0
    for query in queries:
        per_page = min(100, limit_per_query)
        url = "https://api.github.com/search/code?" + urllib.parse.urlencode(
            {"q": query, "per_page": per_page}
        )
        try:
            payload = request_json(url, headers)
        except urllib.error.HTTPError as exc:
            continue
        items = payload.get("items", [])[:limit_per_query]
        raw_items += len(items)
        for item in items:
            repo = item.get("repository", {})
            repo_full = repo.get("full_name", "unknown/repo")
            path = item.get("path", "SKILL.md")
            html_url = item.get("html_url", "")
            slug = safe_slug(repo_full.replace("/", "-") + "-" + str(Path(path).parent).replace("/", "-"))
            name = Path(path).parent.name if Path(path).parent.name != "." else repo.get("name", slug)
            candidates.append(
                Candidate(
                    source="github",
                    slug=slug,
                    name=name,
                    description=repo.get("description") or "",
                    category="GitHub Search",
                    license=(repo.get("license") or {}).get("spdx_id", ""),
                    source_url=html_url or repo.get("html_url", ""),
                    download_url=html_url,
                    external_source_url=html_url,
                    metadata={"repo": repo_full, "path": path, "query": query},
                )
            )
        time.sleep(1)
    return unique_candidates(candidates), {"enabled": True, "queries": queries, "raw_items": raw_items, "candidates": len(candidates)}


def download_candidate(candidate: Candidate) -> dict[str, Any]:
    dest_dir = SKILLS_DIR / candidate.source / candidate.slug
    meta_path = dest_dir / "source.json"
    status = "failed"
    note = ""
    local_path = ""
    content = ""

    try:
        if candidate.source == "claudskills":
            target = dest_dir / "SKILL.md"
            status, note = download_single_file(candidate.download_url, target)
            local_path = str(target.relative_to(ROOT))
            content = target.read_text(encoding="utf-8", errors="replace") if target.exists() else ""
        elif candidate.download_url and parse_github_tree(candidate.download_url):
            status, note = download_github_directory(candidate.download_url, dest_dir)
            skill_file = next(dest_dir.rglob("SKILL.md"), None)
            local_path = str((skill_file or dest_dir).relative_to(ROOT))
            if skill_file:
                content = skill_file.read_text(encoding="utf-8", errors="replace")
        elif candidate.download_url and parse_github_blob(candidate.download_url):
            target = dest_dir / "SKILL.md"
            status, note = download_single_file(candidate.download_url, target)
            local_path = str(target.relative_to(ROOT))
            content = target.read_text(encoding="utf-8", errors="replace") if target.exists() else ""
        elif candidate.download_url:
            target = dest_dir / "SKILL.md"
            status, note = download_single_file(candidate.download_url, target)
            local_path = str(target.relative_to(ROOT))
            content = target.read_text(encoding="utf-8", errors="replace") if target.exists() else ""
        else:
            dest_dir.mkdir(parents=True, exist_ok=True)
            status = "partial"
            note = "metadata only; no downloadable source URL found"
            local_path = str(meta_path.relative_to(ROOT))
    except Exception as exc:  # noqa: BLE001
        dest_dir.mkdir(parents=True, exist_ok=True)
        status = "failed"
        note = str(exc)
        local_path = str(meta_path.relative_to(ROOT))

    if status == "failed":
        local_path = str(meta_path.relative_to(ROOT))

    meta = {
        "name": candidate.name,
        "slug": candidate.slug,
        "source": candidate.source,
        "source_url": candidate.source_url,
        "download_url": candidate.download_url,
        "external_source_url": candidate.external_source_url,
        "license": candidate.license,
        "description": candidate.description,
        "category": candidate.category,
        "download_status": status,
        "download_note": note,
        "metadata": candidate.metadata,
        "collected_at": now_iso(),
    }
    write_json(meta_path, meta)

    text = " ".join([
        candidate.name,
        candidate.slug,
        candidate.description,
        candidate.category,
        candidate.license,
        candidate.source_url,
        candidate.download_url,
        content[:30000],
    ])
    return {
        "name": candidate.name,
        "slug": candidate.slug,
        "source": candidate.source,
        "source_url": candidate.source_url,
        "download_url": candidate.download_url,
        "local_path": local_path,
        "license": candidate.license,
        "description": candidate.description,
        "cwe": extract_cwe(text),
        "owasp": classify_by_rules(text, OWASP_RULES),
        "security_domains": classify_by_rules(text, SECURITY_DOMAIN_RULES),
        "business_domains": classify_by_rules(text, BUSINESS_DOMAIN_RULES),
        "confidence": confidence(candidate, content),
        "download_status": status,
        "download_note": note,
        "category": candidate.category,
        "external_source_url": candidate.external_source_url,
        "collected_at": now_iso(),
    }


def dry_run(args: argparse.Namespace) -> int:
    collectors = [
        ("claudskills", collect_claudskills),
        ("openclawdir", collect_openclaw),
        ("skillstore", collect_skillstore),
    ]
    source_info = {}
    total = 0
    for name, collector in collectors:
        try:
            candidates, info = collector()
        except Exception as exc:  # noqa: BLE001
            print(f"{name}: ERROR {exc}")
            source_info[name] = {"error": str(exc)}
            continue
        print(f"{name}: {len(candidates)} candidates")
        source_info[name] = info
        total += len(candidates)
    gh_candidates, gh_info = github_search_candidates(args.github_limit)
    print(f"github: {len(gh_candidates)} candidates ({gh_info})")
    total += len(gh_candidates)
    print(f"total candidates before de-duplication: {total}")
    return 0


def collect(args: argparse.Namespace) -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    all_candidates: list[Candidate] = []
    sources: dict[str, Any] = {}

    for source_name, collector in [
        ("claudskills", collect_claudskills),
        ("openclawdir", collect_openclaw),
        ("skillstore", collect_skillstore),
    ]:
        print(f"Collecting {source_name} candidates...")
        candidates, info = collector()
        if source_name == "openclawdir":
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
                candidates = list(pool.map(enrich_openclaw, candidates))
        all_candidates.extend(candidates)
        sources[source_name] = {**info, "collected_at": now_iso()}
        print(f"  {len(candidates)} candidates")

    print("Collecting GitHub fallback candidates...")
    gh_candidates, gh_info = github_search_candidates(args.github_limit)
    all_candidates.extend(gh_candidates)
    sources["github"] = {**gh_info, "collected_at": now_iso()}
    print(f"  {len(gh_candidates)} candidates")

    candidates = unique_candidates(all_candidates)
    if args.limit:
        candidates = candidates[: args.limit]
    print(f"Downloading {len(candidates)} unique candidates...")

    entries: list[dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(download_candidate, candidate): candidate for candidate in candidates}
        for index, future in enumerate(concurrent.futures.as_completed(futures), 1):
            candidate = futures[future]
            try:
                entry = future.result()
            except Exception as exc:  # noqa: BLE001
                entry = {
                    "name": candidate.name,
                    "slug": candidate.slug,
                    "source": candidate.source,
                    "source_url": candidate.source_url,
                    "download_url": candidate.download_url,
                    "local_path": "",
                    "license": candidate.license,
                    "description": candidate.description,
                    "cwe": [],
                    "owasp": [],
                    "security_domains": [],
                    "business_domains": [],
                    "confidence": 0,
                    "download_status": "failed",
                    "download_note": str(exc),
                    "category": candidate.category,
                    "external_source_url": candidate.external_source_url,
                    "collected_at": now_iso(),
                }
            entries.append(entry)
            if index % 100 == 0 or index == len(candidates):
                print(f"  {index}/{len(candidates)}")

    entries.sort(key=lambda item: (-item["confidence"], item["source"], item["slug"]))
    write_json(DATA_DIR / "skills.json", entries)
    write_json(
        DATA_DIR / "sources.json",
        {
            "generated_at": now_iso(),
            "candidate_count": len(candidates),
            "entry_count": len(entries),
            "sources": sources,
            "classification_axes": {
                "cwe": "CWE identifiers extracted from text plus keyword inference",
                "owasp": "OWASP Top 10 2021 categories inferred from security keywords",
                "security_domains": [label for _, label in SECURITY_DOMAIN_RULES],
                "business_domains": [label for _, label in BUSINESS_DOMAIN_RULES],
            },
        },
    )
    print(f"Wrote {DATA_DIR / 'skills.json'}")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="collect candidate counts without downloading skill files")
    parser.add_argument("--workers", type=int, default=12, help="parallel download workers")
    parser.add_argument("--limit", type=int, default=0, help="optional maximum unique candidates for test runs")
    parser.add_argument("--github-limit", type=int, default=50, help="maximum GitHub fallback results per query")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.dry_run:
        return dry_run(args)
    return collect(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
