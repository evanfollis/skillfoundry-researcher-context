#!/usr/bin/env python3
"""Refresh the launch-compliance target ledger from configured public sources."""

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
SOURCE_LIST_PATH = ROOT / "memory" / "signals" / "launch_compliance_sources.md"
REPORT_PATH = ROOT / "memory" / "reports" / "launch_compliance_harvest_report.md"

TABLE_SPLIT_RE = re.compile(r"^\|")
CARD_RE = re.compile(
    r'href="(?P<href>/([^"/]+)/([^"/]+))".*?<h3[^>]*>(?P<title>[^<]+)</h3>.*?<p[^>]*>(?P<description>[^<]+)</p>',
    re.DOTALL,
)
LOC_RE = re.compile(r"<loc>(?P<loc>[^<]+)</loc>")


@dataclass
class Source:
    source_id: str
    url: str
    source_type: str
    status: str
    notes: str


@dataclass
class Target:
    target_id: str
    name: str
    url: str
    surface_type: str
    why_they_fit: str
    launch_stage: str
    last_contact_at: str
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


def fetch_text(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "skillfoundry-harvest/0.1 (+https://agenticmarket.dev)"
        },
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_sources() -> list[Source]:
    _, rows = parse_markdown_table(SOURCE_LIST_PATH)
    sources = []
    for row in rows:
        if row.get("status") != "active":
            continue
        sources.append(
            Source(
                source_id=row["source_id"],
                url=row["url"],
                source_type=row["source_type"],
                status=row["status"],
                notes=row.get("notes", ""),
            )
        )
    return sources


def parse_existing_targets() -> dict[str, Target]:
    _, rows = parse_markdown_table(TARGET_LIST_PATH)
    targets: dict[str, Target] = {}
    for row in rows:
        if not row.get("target_id"):
            continue
        target = Target(
            target_id=row["target_id"],
            name=row.get("name", ""),
            url=row.get("url", ""),
            surface_type=row.get("surface_type", ""),
            why_they_fit=row.get("why_they_fit", ""),
            launch_stage=row.get("launch_stage", ""),
            last_contact_at=row.get("last_contact_at", ""),
            contact_status=row.get("contact_status", ""),
            next_action=row.get("next_action", ""),
            notes=row.get("notes", ""),
        )
        targets[target.target_id] = target
    return targets


def harvest_agenticmarket_servers(source: Source) -> list[Target]:
    text = fetch_text(source.url)
    found: dict[str, Target] = {}
    for match in CARD_RE.finditer(text):
        href = match.group("href")
        creator_slug = href.strip("/").split("/")[0]
        server_slug = href.strip("/").split("/")[1]
        if creator_slug in {"servers", "dashboard", "explore", "strange_loop"}:
            continue

        title = html.unescape(match.group("title")).strip()
        description = html.unescape(re.sub(r"\s+", " ", match.group("description"))).strip()
        target_id = f"agenticmarket-{creator_slug}-{server_slug}"
        found[target_id] = Target(
            target_id=target_id,
            name=f"{title} by @{creator_slug}",
            url=f"https://agenticmarket.dev{href}",
            surface_type="agenticmarket_listing",
            why_they_fit="live MCP listing with a visible public packaging surface and directory-readiness implications",
            launch_stage="live_listing",
            last_contact_at="",
            contact_status="not_contacted",
            next_action="inspect listing and find direct contact path",
            notes=f"harvested from {source.source_id}; description: {description}",
        )
    return list(found.values())


def harvest_agenticmarket_sitemap(source: Source) -> list[Target]:
    text = fetch_text(source.url)
    found: dict[str, Target] = {}
    reserved_first_segments = {
        "servers",
        "docs",
        "blog",
        "learn",
        "explore",
        "pricing",
        "earn",
        "about",
        "contact",
        "terms",
        "privacy",
        "cookies",
        "faq",
        "roadmap",
        "login",
        "signup",
        "dashboard",
    }
    for match in LOC_RE.finditer(text):
        loc = match.group("loc").strip()
        parsed = urlparse(loc)
        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) != 2:
            continue
        creator_slug, server_slug = parts
        if creator_slug in reserved_first_segments or creator_slug == "strange_loop":
            continue
        target_id = f"agenticmarket-{creator_slug}-{server_slug}"
        is_platform_owned = creator_slug == "agenticmarket"
        found[target_id] = Target(
            target_id=target_id,
            name=f"{server_slug.replace('-', ' ')} by @{creator_slug}",
            url=loc,
            surface_type="agenticmarket_listing",
            why_they_fit=(
                "public MCP listing discovered in the AgenticMarket sitemap; likely owner has active packaging and launch-readiness concerns"
                if not is_platform_owned
                else "public MCP listing on the platform's own creator account; useful for packaging pattern study but weaker as first outreach target"
            ),
            launch_stage="live_listing",
            last_contact_at="",
            contact_status="not_contacted" if not is_platform_owned else "cold",
            next_action=(
                "inspect listing and find direct contact path"
                if not is_platform_owned
                else "use as packaging reference unless a strong direct contact path appears"
            ),
            notes=(
                f"harvested from {source.source_id}"
                if not is_platform_owned
                else f"harvested from {source.source_id}; platform-owned listing, likely lower buyer priority"
            ),
        )
    return list(found.values())


def harvest_smithery_registry(source: Source) -> list[Target]:
    text = fetch_text(source.url)
    data = json.loads(text)
    found: dict[str, Target] = {}
    platform_namespaces = {
        "instagram", "reddit", "googlesheets", "gmail", "slack",
        "github", "notion", "linear", "jira", "trello", "asana",
        "hubspot", "salesforce", "stripe", "twilio", "discord",
    }
    for server in data.get("servers", []):
        qname = server.get("qualifiedName", "")
        if "/" not in qname:
            # Single-segment names are typically platform integrations
            if qname.lower() in platform_namespaces:
                continue
        namespace = server.get("namespace", "")
        slug = server.get("slug", "") or qname
        display = server.get("displayName", slug)
        homepage = server.get("homepage", "")
        verified = server.get("verified", False)
        # Skip verified platform integrations (Composio-managed)
        if verified and "/" not in qname:
            continue
        target_id = f"smithery-{qname.replace('/', '-').lower()}"
        found[target_id] = Target(
            target_id=target_id,
            name=f"{display} by @{namespace}",
            url=homepage or f"https://smithery.ai/servers/{qname}",
            surface_type="smithery_listing",
            why_they_fit="published MCP server on Smithery directory; builder has active packaging and distribution concerns",
            launch_stage="live_listing",
            last_contact_at="",
            contact_status="not_contacted",
            next_action="inspect listing homepage and find direct contact path",
            notes=f"harvested from {source.source_id}; smithery use_count: {server.get('useCount', '?')}",
        )
    return list(found.values())


def harvest_github_mcp_search(source: Source) -> list[Target]:
    request = urllib.request.Request(
        source.url,
        headers={
            "User-Agent": "skillfoundry-harvest/0.1",
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        text = response.read().decode("utf-8", errors="replace")
    data = json.loads(text)
    found: dict[str, Target] = {}
    for repo in data.get("items", []):
        owner = repo.get("owner", {}).get("login", "")
        name = repo.get("name", "")
        full_name = repo.get("full_name", f"{owner}/{name}")
        description = repo.get("description", "") or ""
        html_url = repo.get("html_url", "")
        stars = repo.get("stargazers_count", 0)
        # Skip very popular repos (likely frameworks, not individual builders)
        if stars > 500:
            continue
        target_id = f"github-{full_name.replace('/', '-').lower()}"
        found[target_id] = Target(
            target_id=target_id,
            name=f"{name} by @{owner}",
            url=html_url,
            surface_type="github_repo",
            why_they_fit="actively maintained MCP server repo; builder likely has launch-readiness and distribution concerns",
            launch_stage="pre_launch" if stars < 10 else "live_listing",
            last_contact_at="",
            contact_status="not_contacted",
            next_action="check GitHub profile for contact email and inspect repo README for distribution intent",
            notes=f"harvested from {source.source_id}; stars: {stars}; {description[:100]}",
        )
    return list(found.values())


def merge_targets(existing: dict[str, Target], harvested: list[Target]) -> list[Target]:
    merged: dict[str, Target] = {
        key: value
        for key, value in existing.items()
        if not (harvested and key.startswith("target-template-"))
    }
    for target in harvested:
        prior = merged.get(target.target_id)
        if prior:
            untouched_auto_row = (
                prior.contact_status in {"", "not_contacted"}
                and not prior.last_contact_at
                and prior.notes.startswith("harvested from ")
            )
            if not untouched_auto_row:
                target.last_contact_at = prior.last_contact_at
                target.contact_status = prior.contact_status
                target.next_action = prior.next_action or target.next_action
                target.notes = prior.notes or target.notes
        merged[target.target_id] = target
    return sorted(
        normalize_targets(merged.values()),
        key=lambda item: (
            is_platform_owned_target(item),
            item.contact_status not in {"not_contacted", "contacted"},
            item.target_id,
        ),
    )


def is_platform_owned_target(target: Target) -> bool:
    parts = [part for part in urlparse(target.url).path.split("/") if part]
    return len(parts) >= 2 and parts[0] == "agenticmarket"


def normalize_targets(targets) -> list[Target]:
    normalized: list[Target] = []
    for target in targets:
        if is_platform_owned_target(target) and not target.last_contact_at and target.contact_status in {"", "not_contacted"}:
            target.contact_status = "cold"
            target.next_action = "use as packaging reference unless a strong direct contact path appears"
            if "platform-owned listing" not in target.notes:
                suffix = "; " if target.notes else ""
                target.notes = f"{target.notes}{suffix}platform-owned listing, likely lower buyer priority"
        normalized.append(target)
    return normalized


def write_target_list(targets: list[Target]) -> None:
    rows = [
        "| target_id | name | url | surface_type | why_they_fit | launch_stage | last_contact_at | contact_status | next_action | notes |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for target in targets:
        values = [
            target.target_id,
            target.name,
            target.url,
            target.surface_type,
            target.why_they_fit,
            target.launch_stage,
            target.last_contact_at,
            target.contact_status,
            target.next_action,
            target.notes,
        ]
        escaped = [value.replace("|", "\\|") for value in values]
        rows.append("| " + " | ".join(escaped) + " |")

    body = f"""# Launch Compliance Target List

This is the working target ledger for the live probe:

- assumption: `launch-compliance-intelligence-first-paid-review`
- probe: `launch-compliance-intelligence-manual-offer`

Use this as a simple operational queue. Keep it ugly but current.

## Fields

- `target_id`
- `name`
- `url`
- `surface_type`
- `why_they_fit`
- `launch_stage`
- `last_contact_at`
- `contact_status`
- `next_action`
- `notes`

## Current Rows

{chr(10).join(rows)}

## Status Values

- `not_contacted`
- `contacted`
- `responded`
- `materials_sent`
- `asked_for_terms`
- `cold`
- `ruled_out`

## Rules

- do not keep dead targets in your head; mark them explicitly
- do not count a target as evidence until a valuation-side evidence note exists
- prefer a smaller, live queue over a giant stale spreadsheet
- if the harvester refreshes a row, preserve the contact state unless the human changes it
"""
    TARGET_LIST_PATH.write_text(body, encoding="utf-8")


def write_report(
    generated_at: datetime,
    sources: list[Source],
    harvested: list[Target],
    merged: list[Target],
    errors: list[str],
) -> None:
    creator_counts: dict[str, int] = {}
    recommended: list[Target] = []
    for target in merged:
        creator = target.url.rstrip("/").split("/")[-2]
        creator_counts[creator] = creator_counts.get(creator, 0) + 1
        if (
            not is_platform_owned_target(target)
            and target.contact_status in {"not_contacted", "contacted"}
        ):
            recommended.append(target)

    lines = [
        "# Launch Compliance Harvest Report",
        "",
        f"- `generated_at`: `{generated_at.strftime('%Y-%m-%dT%H:%M:%SZ')}`",
        f"- `source_count`: `{len(sources)}`",
        f"- `harvested_targets`: `{len(harvested)}`",
        f"- `merged_targets`: `{len(merged)}`",
        "",
        "## Sources",
        "",
    ]
    for source in sources:
        lines.append(f"- `{source.source_id}` `{source.source_type}` {source.url}")
    lines.extend(["", "## Errors", ""])
    if errors:
        for error in errors:
            lines.append(f"- {error}")
    else:
        lines.append("- none")
    lines.extend(["", "## Creator Concentration", ""])
    for creator, count in sorted(creator_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- `{creator}`: `{count}` targets")
    lines.extend(["", "## Recommended First-Pass Targets", ""])
    if recommended:
        for target in recommended[:5]:
            lines.append(f"- `{target.target_id}` {target.url}")
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- This harvest is an input queue refresh, not evidence.",
            "- Every harvested target still needs human triage and a concrete contact path.",
            "- Promotion happens only through valuation-side evidence and decisions.",
            "- If one creator dominates the queue, treat the source as structurally weak for outreach and add more discovery surfaces.",
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    sources = parse_sources()
    existing = parse_existing_targets()
    harvested: list[Target] = []
    errors: list[str] = []

    for source in sources:
        try:
            if source.source_type == "agenticmarket_servers":
                harvested.extend(harvest_agenticmarket_servers(source))
            elif source.source_type == "agenticmarket_sitemap":
                harvested.extend(harvest_agenticmarket_sitemap(source))
            elif source.source_type == "smithery_registry":
                harvested.extend(harvest_smithery_registry(source))
            elif source.source_type == "github_mcp_search":
                harvested.extend(harvest_github_mcp_search(source))
            else:
                errors.append(f"{source.source_id}: unsupported source_type `{source.source_type}`")
        except urllib.error.URLError as exc:
            errors.append(f"{source.source_id}: fetch failed: {exc}")

    merged = merge_targets(existing, harvested)
    write_target_list(merged)
    write_report(datetime.now(UTC), sources, harvested, merged, errors)


if __name__ == "__main__":
    main()
