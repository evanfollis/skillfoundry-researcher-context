#!/usr/bin/env python3
"""Enrich launch-compliance targets with metadata and contactability from multiple surfaces."""

from __future__ import annotations

import html
import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
TARGET_LIST_PATH = ROOT / "memory" / "signals" / "launch_compliance_target_list.md"
DOSSIER_DIR = ROOT / "memory" / "signals" / "target_profiles"
REPORT_PATH = ROOT / "memory" / "reports" / "launch_compliance_enrichment_report.md"

TABLE_SPLIT_RE = re.compile(r"^\|")
TITLE_RE = re.compile(r"<title>(?P<title>[^<]+)</title>", re.IGNORECASE)
EXTERNAL_LINK_RE = re.compile(r'href="(?P<href>https://[^"]+)"')
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


@dataclass
class Target:
    target_id: str
    name: str
    url: str
    surface_type: str
    contact_status: str
    next_action: str
    notes: str


def parse_markdown_table(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    header: list[str] = []
    rows: list[dict[str, str]] = []
    in_table = False
    for line in lines:
        if not TABLE_SPLIT_RE.match(line):
            if in_table:
                break
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if not header:
            header = parts
            in_table = True
            continue
        if all(part.startswith("-") for part in parts):
            continue
        if len(parts) != len(header):
            continue
        rows.append(dict(zip(header, parts)))
    return header, rows


def fetch_text(url: str, accept: str = "text/html") -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "skillfoundry-enrich/0.1",
            "Accept": accept,
        },
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_targets() -> list[Target]:
    _, rows = parse_markdown_table(TARGET_LIST_PATH)
    return [
        Target(
            target_id=row["target_id"],
            name=row["name"],
            url=row["url"],
            surface_type=row.get("surface_type", ""),
            contact_status=row["contact_status"],
            next_action=row["next_action"],
            notes=row["notes"],
        )
        for row in rows
        if row.get("target_id")
    ]


def clean_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


# --- GitHub enrichment ---

def enrich_github(target: Target) -> dict[str, object]:
    """Enrich a GitHub repo target via the API."""
    parsed = urlparse(target.url)
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 2:
        return _empty_enrichment(target)

    owner, repo = parts[0], parts[1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    user_url = f"https://api.github.com/users/{owner}"

    repo_data = json.loads(fetch_text(api_url, accept="application/vnd.github+json"))
    user_data = json.loads(fetch_text(user_url, accept="application/vnd.github+json"))

    description = repo_data.get("description", "") or ""
    homepage = repo_data.get("homepage", "") or ""
    stars = repo_data.get("stargazers_count", 0)
    topics = repo_data.get("topics", [])
    license_info = repo_data.get("license", {}) or {}
    license_name = license_info.get("spdx_id", "none")
    created_at = repo_data.get("created_at", "")
    pushed_at = repo_data.get("pushed_at", "")

    email = user_data.get("email", "") or ""
    blog = user_data.get("blog", "") or ""
    bio = user_data.get("bio", "") or ""
    twitter = user_data.get("twitter_username", "") or ""
    user_name = user_data.get("name", "") or owner

    contact_paths: list[str] = []
    if email:
        contact_paths.append(f"email: {email}")
    if twitter:
        contact_paths.append(f"twitter: @{twitter}")
    if blog:
        contact_paths.append(f"blog/site: {blog}")
    # GitHub profile itself is always a contact path via issues
    contact_paths.append(f"github: https://github.com/{owner}")

    # Try to fetch README for launch intent signals
    readme_signals: list[str] = []
    try:
        readme_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{repo_data.get('default_branch', 'main')}/README.md"
        readme_text = fetch_text(readme_url)[:3000].lower()
        signal_terms = {
            "mcp": "mentions MCP",
            "install": "has install instructions",
            "deploy": "mentions deployment",
            "docker": "mentions Docker",
            "npm publish": "mentions npm publishing",
            "pypi": "mentions PyPI",
            "release": "mentions releases",
            "getting started": "has getting started section",
        }
        for term, label in signal_terms.items():
            if term in readme_text:
                readme_signals.append(label)
    except urllib.error.URLError:
        pass

    return {
        "page_title": f"{repo} by {user_name}",
        "description": description,
        "stars": stars,
        "topics": topics,
        "license": license_name,
        "created_at": created_at,
        "pushed_at": pushed_at,
        "homepage": homepage,
        "owner_name": user_name,
        "owner_bio": bio,
        "contact_paths": contact_paths,
        "contactability": "public_contact_path_found" if (email or twitter or blog) else "github_only",
        "readme_signals": readme_signals,
        "surface_type": "github_repo",
    }


# --- Smithery enrichment ---

def enrich_smithery(target: Target) -> dict[str, object]:
    """Enrich a Smithery listing target."""
    # Extract qualified name from target_id: smithery-owner-slug -> owner/slug
    parts = target.target_id.removeprefix("smithery-").split("-", 1)
    if len(parts) < 2:
        return _empty_enrichment(target)

    # Try the homepage URL first (often a GitHub link)
    contact_paths: list[str] = []
    homepage = target.url
    github_owner = ""
    description = ""

    if "github.com" in homepage:
        # Extract owner from GitHub URL and enrich via GitHub
        parsed = urlparse(homepage)
        gh_parts = [p for p in parsed.path.split("/") if p]
        if len(gh_parts) >= 2:
            github_owner = gh_parts[0]
            try:
                user_data = json.loads(fetch_text(
                    f"https://api.github.com/users/{github_owner}",
                    accept="application/vnd.github+json",
                ))
                email = user_data.get("email", "") or ""
                blog = user_data.get("blog", "") or ""
                twitter = user_data.get("twitter_username", "") or ""
                if email:
                    contact_paths.append(f"email: {email}")
                if twitter:
                    contact_paths.append(f"twitter: @{twitter}")
                if blog:
                    contact_paths.append(f"blog/site: {blog}")
                contact_paths.append(f"github: https://github.com/{github_owner}")
            except urllib.error.URLError:
                contact_paths.append(f"github: https://github.com/{github_owner}")

            # Try to get repo description
            try:
                repo_data = json.loads(fetch_text(
                    f"https://api.github.com/repos/{gh_parts[0]}/{gh_parts[1]}",
                    accept="application/vnd.github+json",
                ))
                description = repo_data.get("description", "") or ""
            except urllib.error.URLError:
                pass
    elif "smithery.ai" in homepage:
        contact_paths.append(f"smithery: {homepage}")
    else:
        contact_paths.append(f"homepage: {homepage}")

    return {
        "page_title": target.name,
        "description": description or f"Smithery listing: {target.name}",
        "contact_paths": contact_paths,
        "contactability": "public_contact_path_found" if any(
            p.startswith(("email:", "twitter:", "blog/site:")) for p in contact_paths
        ) else "github_only" if github_owner else "no_public_contact_path_found",
        "homepage": homepage,
        "surface_type": "smithery_listing",
    }


# --- AgenticMarket enrichment ---

PARA_RE = re.compile(
    r'<p class="text-\[17px\][^"]*"[^>]*>(?P<text>.*?)</p>', re.DOTALL
)
ACCESS_TIER_RE = re.compile(
    r"<span class=\"text-\[#666\]\">Access Tier</span><span class=\"text-white\">(?P<access>[^<]+)</span>"
)
CATEGORY_RE = re.compile(
    r"<span class=\"text-\[#666\] font-mono uppercase tracking-widest\">Category</span>.*?"
    r"<div class=\"flex items-center text-sm font-mono text-\[#AAA\][^>]*>(?P<category>.*?)</div>",
    re.DOTALL,
)
KNOWN_PLATFORM_LINK_MARKERS = (
    "agenticmarket.dev",
    "github.com/agenticmarket/",
    "github.com/nyxhora/agenticmarket-cli",
    "x.com/agenticmktdev",
    "marketplace.visualstudio.com/items?itemName=agenticmarket.",
    "discord.gg/m22mxGSW5w",
)


def enrich_agenticmarket(target: Target) -> dict[str, object]:
    """Enrich an AgenticMarket listing target by scraping listing and creator pages."""
    listing_html = fetch_text(target.url)

    parsed = urlparse(target.url)
    parts = [p for p in parsed.path.split("/") if p]
    creator_page = f"{parsed.scheme}://{parsed.netloc}/{parts[0]}" if parts else target.url

    try:
        creator_html = fetch_text(creator_page)
    except urllib.error.URLError:
        creator_html = ""

    title_match = TITLE_RE.search(listing_html)
    access_match = ACCESS_TIER_RE.search(listing_html)
    category_match = CATEGORY_RE.search(listing_html)
    paragraphs = [clean_html(m.group("text")) for m in PARA_RE.finditer(listing_html)]

    external_links = sorted({
        href for href in EXTERNAL_LINK_RE.findall(creator_html + "\n" + listing_html)
        if "agenticmarket.dev" not in href and "cloud.umami.is" not in href
    })
    contact_links = [
        href for href in external_links
        if not any(marker in href for marker in KNOWN_PLATFORM_LINK_MARKERS)
    ]

    contact_paths = [f"link: {link}" for link in contact_links]

    return {
        "page_title": title_match.group("title").strip() if title_match else target.name,
        "description": "; ".join(paragraphs[:3]) if paragraphs else "",
        "access_tier": access_match.group("access").strip() if access_match else "unknown",
        "category": clean_html(category_match.group("category")) if category_match else "unknown",
        "contact_paths": contact_paths,
        "contactability": "public_contact_path_found" if contact_links else "no_public_contact_path_found",
        "homepage": target.url,
        "surface_type": "agenticmarket_listing",
    }


# --- Shared ---

def _empty_enrichment(target: Target) -> dict[str, object]:
    return {
        "page_title": target.name,
        "description": "",
        "contact_paths": [],
        "contactability": "no_public_contact_path_found",
        "homepage": target.url,
        "surface_type": target.surface_type,
    }


def enrich_target(target: Target) -> dict[str, object]:
    """Route to the right enrichment function based on surface type."""
    if target.surface_type == "github_repo" or "github.com" in target.url:
        return enrich_github(target)
    elif target.surface_type == "smithery_listing":
        return enrich_smithery(target)
    elif target.surface_type == "agenticmarket_listing":
        return enrich_agenticmarket(target)
    else:
        return _empty_enrichment(target)


def write_dossier(target: Target, enriched: dict[str, object]) -> None:
    DOSSIER_DIR.mkdir(parents=True, exist_ok=True)
    contact_paths = enriched.get("contact_paths", [])
    lines = [
        f"# Target Profile: {target.target_id}",
        "",
        f"- `target_id`: `{target.target_id}`",
        f"- `name`: `{target.name}`",
        f"- `url`: `{target.url}`",
        f"- `surface_type`: `{enriched.get('surface_type', target.surface_type)}`",
        f"- `contact_status`: `{target.contact_status}`",
        f"- `contactability`: `{enriched['contactability']}`",
    ]

    # Surface-specific metadata
    if "stars" in enriched:
        lines.append(f"- `stars`: `{enriched['stars']}`")
    if "topics" in enriched and enriched["topics"]:
        lines.append(f"- `topics`: `{', '.join(enriched['topics'])}`")
    if "license" in enriched:
        lines.append(f"- `license`: `{enriched['license']}`")
    if "access_tier" in enriched:
        lines.append(f"- `access_tier`: `{enriched['access_tier']}`")
    if "category" in enriched:
        lines.append(f"- `category`: `{enriched['category']}`")

    lines.extend(["", "## Description", ""])
    lines.append(enriched.get("description", "") or "(no description)")

    if enriched.get("readme_signals"):
        lines.extend(["", "## Launch Readiness Signals", ""])
        for signal in enriched["readme_signals"]:
            lines.append(f"- {signal}")

    lines.extend(["", "## Contact Paths", ""])
    if contact_paths:
        for path in contact_paths:
            lines.append(f"- {path}")
    else:
        lines.append("- none found")

    lines.extend([
        "",
        "## Operational Read",
        "",
        f"- current queue note: {target.notes}",
        f"- current next action: {target.next_action}",
        "",
    ])
    (DOSSIER_DIR / f"{target.target_id}.md").write_text("\n".join(lines), encoding="utf-8")


def write_report(
    generated_at: datetime,
    processed: list[tuple[Target, dict[str, object]]],
    errors: list[str],
) -> None:
    lines = [
        "# Launch Compliance Enrichment Report",
        "",
        f"- `generated_at`: `{generated_at.strftime('%Y-%m-%dT%H:%M:%SZ')}`",
        f"- `processed_targets`: `{len(processed)}`",
        f"- `errors`: `{len(errors)}`",
        "",
        "## Contactability Summary",
        "",
    ]
    found = [t for t, e in processed if e["contactability"] == "public_contact_path_found"]
    github_only = [t for t, e in processed if e["contactability"] == "github_only"]
    missing = [t for t, e in processed if e["contactability"] == "no_public_contact_path_found"]
    lines.append(f"- public contact path (email/twitter/blog): `{len(found)}`")
    lines.append(f"- github profile only: `{len(github_only)}`")
    lines.append(f"- no public contact path: `{len(missing)}`")

    # Top outreach candidates — those with direct contact paths
    lines.extend(["", "## Top Outreach Candidates", ""])
    candidates = [(t, e) for t, e in processed if e["contactability"] == "public_contact_path_found"]
    if candidates:
        for target, enriched in candidates[:20]:
            paths = "; ".join(enriched.get("contact_paths", [])[:2])
            lines.append(f"- `{target.target_id}` — {paths}")
    else:
        lines.append("- none with direct contact paths in this batch")

    # GitHub-contactable (via issues or profile)
    lines.extend(["", "## GitHub-Contactable", ""])
    gh_targets = [(t, e) for t, e in processed if e["contactability"] == "github_only"]
    if gh_targets:
        for target, enriched in gh_targets[:20]:
            paths = "; ".join(enriched.get("contact_paths", [])[:1])
            lines.append(f"- `{target.target_id}` — {paths}")
    else:
        lines.append("- none")

    lines.extend(["", "## Errors", ""])
    if errors:
        for error in errors:
            lines.append(f"- {error}")
    else:
        lines.append("- none")

    lines.extend([
        "",
        "## Notes",
        "",
        "- Enrichment is discovery support, not evidence.",
        "- Targets with direct contact paths are highest priority for outreach.",
        "- GitHub-only targets can be contacted via issues or discussions.",
        "",
    ])
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    targets = [
        target
        for target in parse_targets()
        if target.contact_status in {"not_contacted", "contacted"}
    ]
    processed: list[tuple[Target, dict[str, object]]] = []
    errors: list[str] = []
    for target in targets:
        try:
            enriched = enrich_target(target)
            write_dossier(target, enriched)
            processed.append((target, enriched))
        except (urllib.error.URLError, json.JSONDecodeError, KeyError) as exc:
            errors.append(f"{target.target_id}: {exc}")
    write_report(datetime.now(UTC), processed, errors)


if __name__ == "__main__":
    main()
