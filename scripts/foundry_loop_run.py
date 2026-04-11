#!/usr/bin/env python3
"""Run the full foundry loop: harvest → enrich → score → draft outreach → report.

This is the single automated entrypoint for the launch-compliance pipeline.
Run it on a schedule or manually to advance the loop without human intervention.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
REPORT_PATH = ROOT / "memory" / "reports" / "foundry_loop_run_log.md"
ENRICHMENT_REPORT_PATH = ROOT / "memory" / "reports" / "launch_compliance_enrichment_report.md"
TARGET_PROFILES_DIR = ROOT / "memory" / "signals" / "target_profiles"
OUTREACH_QUEUE_PATH = ROOT / "memory" / "signals" / "outreach_queue.md"
OUTREACH_DRAFTS_DIR = ROOT / "memory" / "signals" / "outreach_drafts"

TABLE_SPLIT_RE = __import__("re").compile(r"^\|")

TOUCH_1_TEMPLATE = """I've been looking closely at MCP launches and keep seeing a gap between "server works" and "server is actually ready for public distribution."

{personalization}

I'm testing a narrow review that flags trust, compatibility, and directory-readiness issues for one server package. If that sounds relevant, I can show you the exact shape of the review."""


def run_step(name: str, script: str) -> tuple[bool, str]:
    """Run a pipeline script, return (success, output)."""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / script)],
        capture_output=True, text=True, check=False,
        cwd=str(ROOT),
    )
    if result.returncode != 0:
        return False, result.stderr.strip()
    return True, result.stdout.strip()


def parse_markdown_table(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
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
    return rows


def score_targets() -> list[dict[str, object]]:
    """Score enriched targets by outreach readiness."""
    scored: list[dict[str, object]] = []
    if not TARGET_PROFILES_DIR.exists():
        return scored

    for profile_path in sorted(TARGET_PROFILES_DIR.glob("*.md")):
        if profile_path.name == "README.md":
            continue
        text = profile_path.read_text(encoding="utf-8")
        target_id = ""
        name = ""
        url = ""
        contactability = ""
        contact_paths: list[str] = []
        description = ""
        surface_type = ""
        stars = 0

        in_contact = False
        in_description = False
        for line in text.splitlines():
            if line.startswith("- `target_id`:"):
                target_id = line.split("`")[3] if "`" in line else ""
            elif line.startswith("- `name`:"):
                name = line.split("`")[3] if "`" in line else ""
            elif line.startswith("- `url`:"):
                url = line.split("`")[3] if "`" in line else ""
            elif line.startswith("- `contactability`:"):
                contactability = line.split("`")[3] if "`" in line else ""
            elif line.startswith("- `surface_type`:"):
                surface_type = line.split("`")[3] if "`" in line else ""
            elif line.startswith("- `stars`:"):
                try:
                    stars = int(line.split("`")[3])
                except (IndexError, ValueError):
                    pass
            elif line.startswith("## Contact Paths"):
                in_contact = True
                in_description = False
            elif line.startswith("## Description"):
                in_description = True
                in_contact = False
            elif line.startswith("## "):
                in_contact = False
                in_description = False
            elif in_contact and line.startswith("- ") and "none" not in line.lower():
                contact_paths.append(line[2:].strip())
            elif in_description and line.strip():
                description = line.strip()

        if not target_id:
            continue

        # Scoring: higher = better outreach candidate
        score = 0
        if contactability == "public_contact_path_found":
            score += 30
        elif contactability == "github_only":
            score += 10
        if any("email:" in p for p in contact_paths):
            score += 20
        if any("twitter:" in p for p in contact_paths):
            score += 10
        if stars > 0:
            score += min(stars, 20)  # Cap star bonus at 20
        if surface_type == "github_repo":
            score += 5  # GitHub repos have richer contact paths

        scored.append({
            "target_id": target_id,
            "name": name,
            "url": url,
            "contactability": contactability,
            "contact_paths": contact_paths,
            "description": description,
            "surface_type": surface_type,
            "stars": stars,
            "score": score,
        })

    scored.sort(key=lambda t: -t["score"])
    return scored


def draft_outreach(scored_targets: list[dict[str, object]], max_drafts: int = 10) -> list[dict[str, str]]:
    """Generate personalized Touch 1 outreach drafts for top targets."""
    OUTREACH_DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    drafts: list[dict[str, str]] = []

    for target in scored_targets[:max_drafts]:
        target_id = target["target_id"]
        name = target["name"]
        description = target["description"]
        contact_paths = target["contact_paths"]
        url = target["url"]

        if not contact_paths:
            continue

        # Build personalization based on what we know
        if description:
            personalization = f"Your project ({name}) looks close to launchable — {description[:150].rstrip('.')}. But I suspect there may be hidden trust, compatibility, or directory-readiness issues that are different from just polishing copy."
        else:
            personalization = f"Your server ({name}) looks close to launchable, but I suspect there may be hidden trust, compatibility, or directory-readiness issues that are different from just polishing copy."

        message = TOUCH_1_TEMPLATE.format(personalization=personalization)

        # Determine best contact channel
        best_channel = "unknown"
        best_address = ""
        for path in contact_paths:
            if path.startswith("email:"):
                best_channel = "email"
                best_address = path.split("email:", 1)[1].strip()
                break
            elif path.startswith("twitter:"):
                best_channel = "twitter_dm"
                best_address = path.split("twitter:", 1)[1].strip()
            elif path.startswith("github:") and best_channel not in {"email", "twitter_dm"}:
                best_channel = "github_discussion"
                best_address = path.split("github:", 1)[1].strip()

        draft = {
            "target_id": target_id,
            "name": name,
            "url": url,
            "channel": best_channel,
            "address": best_address,
            "message": message,
            "status": "drafted",
        }
        drafts.append(draft)

        # Write individual draft file
        draft_lines = [
            f"# Outreach Draft: {target_id}",
            "",
            f"- `target_id`: `{target_id}`",
            f"- `name`: `{name}`",
            f"- `url`: `{url}`",
            f"- `channel`: `{best_channel}`",
            f"- `address`: `{best_address}`",
            f"- `status`: `drafted`",
            f"- `drafted_at`: `{datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')}`",
            "",
            "## Message",
            "",
            message,
            "",
            "## Contact Paths Available",
            "",
        ]
        for path in contact_paths:
            draft_lines.append(f"- {path}")
        draft_lines.extend(["", ""])
        (OUTREACH_DRAFTS_DIR / f"{target_id}.md").write_text(
            "\n".join(draft_lines), encoding="utf-8"
        )

    return drafts


def write_outreach_queue(drafts: list[dict[str, str]]) -> None:
    """Write the outreach queue summary."""
    lines = [
        "# Outreach Queue",
        "",
        f"- `generated_at`: `{datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')}`",
        f"- `total_drafts`: `{len(drafts)}`",
        "",
        "## Queue",
        "",
        "| target_id | name | channel | address | status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for draft in drafts:
        lines.append(
            f"| {draft['target_id']} | {draft['name']} | {draft['channel']} | {draft['address']} | {draft['status']} |"
        )
    lines.extend([
        "",
        "## Rules",
        "",
        "- A draft moves to `sent` when the message is delivered.",
        "- A `sent` target moves to `responded` or `no_response` after 7 days.",
        "- Any response gets logged as typed evidence in valuation canon.",
        "- Do not batch-send. Send 3-5 per cycle, wait, learn, adjust.",
        "",
    ])
    OUTREACH_QUEUE_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_run_log(
    generated_at: datetime,
    steps: list[tuple[str, bool, str]],
    scored_count: int,
    draft_count: int,
) -> None:
    lines = [
        "# Foundry Loop Run Log",
        "",
        f"- `generated_at`: `{generated_at.strftime('%Y-%m-%dT%H:%M:%SZ')}`",
        "",
        "## Pipeline Steps",
        "",
    ]
    for name, success, detail in steps:
        status = "OK" if success else "FAIL"
        lines.append(f"- `{name}`: `{status}` {detail[:200] if detail else ''}")
    lines.extend([
        "",
        f"## Scoring: `{scored_count}` targets scored",
        f"## Outreach: `{draft_count}` drafts generated",
        "",
    ])
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_at = datetime.now(UTC)
    steps: list[tuple[str, bool, str]] = []

    # Step 1: Harvest
    ok, output = run_step("harvest", "launch_compliance_target_harvest.py")
    steps.append(("harvest", ok, output))
    if not ok:
        print(f"FAIL harvest: {output}", file=sys.stderr)

    # Step 2: Enrich
    ok, output = run_step("enrich", "launch_compliance_target_enrich.py")
    steps.append(("enrich", ok, output))
    if not ok:
        print(f"FAIL enrich: {output}", file=sys.stderr)

    # Step 3: Score
    scored = score_targets()
    steps.append(("score", True, f"{len(scored)} targets scored"))

    # Step 4: Draft outreach
    drafts = draft_outreach(scored)
    steps.append(("draft_outreach", True, f"{len(drafts)} drafts generated"))
    write_outreach_queue(drafts)

    # Step 5: Status report
    ok, output = run_step("status_report", "foundry_loop_report.py")
    steps.append(("status_report", ok, output))

    # Write run log
    write_run_log(generated_at, steps, len(scored), len(drafts))

    # Print summary
    print(f"Foundry loop complete at {generated_at.strftime('%Y-%m-%dT%H:%M:%SZ')}")
    for name, success, detail in steps:
        print(f"  {'OK' if success else 'FAIL'} {name}")
    print(f"  {len(scored)} targets scored, {len(drafts)} outreach drafts ready")

    if drafts:
        print("\nTop outreach candidates:")
        for d in drafts[:5]:
            print(f"  {d['target_id']} via {d['channel']} ({d['address']})")


if __name__ == "__main__":
    main()
