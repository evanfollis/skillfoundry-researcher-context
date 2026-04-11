#!/usr/bin/env python3
"""Generate a markdown status report for the Skillfoundry always-on loop."""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
VALUATION_ROOT = ROOT.parent / "skillfoundry-valuation-context"
REPORT_PATH = ROOT / "memory" / "reports" / "foundry_loop_status.md"


FIELD_RE = re.compile(r"^- `([^`]+)`: ?(?:`(.*)`)?$")

EVIDENCE_CLASS_RANK = {
    "internal_operational": 0,
    "external_conversation": 1,
    "external_commitment": 2,
    "external_transaction": 3,
}

EVIDENCE_QUALITY_RANK = {
    "weak": 0,
    "moderate": 1,
    "strong": 2,
}


@dataclass
class Note:
    path: Path
    title: str
    fields: dict[str, object]
    body: str


def slug_title(path: Path) -> str:
    return path.stem.replace("-", " ")


def parse_note(path: Path) -> Note:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = lines[0].lstrip("# ").strip() if lines else slug_title(path)
    fields: dict[str, object] = {}
    current_list_key: str | None = None

    for line in lines[1:]:
        match = FIELD_RE.match(line)
        if match:
            key, value = match.groups()
            if value is None:
                fields[key] = []
                current_list_key = key
            else:
                fields[key] = value
                current_list_key = None
            continue

        if current_list_key and line.startswith("  - "):
            cast = fields.get(current_list_key)
            if isinstance(cast, list):
                cast.append(line[4:].strip().strip("`"))
            continue

        if line and not line.startswith("  "):
            current_list_key = None

    return Note(path=path, title=title, fields=fields, body=text)


def list_markdown_notes(directory: Path, required_field: str | None = None) -> list[Note]:
    if not directory.exists():
        return []
    notes = []
    for path in sorted(directory.glob("*.md")):
        if path.name == "README.md":
            continue
        note = parse_note(path)
        if required_field and required_field not in note.fields:
            continue
        notes.append(note)
    return notes


def parse_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    if value in {"", "(open)"}:
        return None
    try:
        if value.endswith("Z"):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def fmt_date(dt: datetime | None) -> str:
    if dt is None:
        return "n/a"
    return dt.astimezone(UTC).strftime("%Y-%m-%d")


def bucket_external_status(evidence_notes: Iterable[Note]) -> str:
    best_class = -1
    best_quality = -1
    for note in evidence_notes:
        evidence_class = str(note.fields.get("evidence_class", ""))
        quality = str(note.fields.get("evidence_quality", ""))
        best_class = max(best_class, EVIDENCE_CLASS_RANK.get(evidence_class, -1))
        best_quality = max(best_quality, EVIDENCE_QUALITY_RANK.get(quality, -1))

    if best_class >= EVIDENCE_CLASS_RANK["external_transaction"]:
        return "external_transaction"
    if best_class >= EVIDENCE_CLASS_RANK["external_commitment"]:
        return "external_commitment"
    if best_class >= EVIDENCE_CLASS_RANK["external_conversation"]:
        return "external_conversation"
    if best_class >= EVIDENCE_CLASS_RANK["internal_operational"]:
        return "internal_only"
    return "none"


def latest_by_key(notes: Iterable[Note], key: str) -> dict[str, Note]:
    latest: dict[str, Note] = {}
    for note in notes:
        field_value = note.fields.get(key)
        if not isinstance(field_value, str):
            continue
        current = latest.get(field_value)
        note_time = parse_timestamp(note.fields.get("timestamp") or note.fields.get("observed_at"))
        current_time = None
        if current is not None:
            current_time = parse_timestamp(
                current.fields.get("timestamp") or current.fields.get("observed_at")
            )
        if current is None or (note_time and (current_time is None or note_time > current_time)):
            latest[field_value] = note
    return latest


def render_table(rows: list[list[str]]) -> str:
    if not rows:
        return "_None_\n"
    widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]
    rendered = []
    rendered.append(
        "| " + " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(rows[0])) + " |"
    )
    rendered.append(
        "| " + " | ".join("-" * widths[i] for i in range(len(rows[0]))) + " |"
    )
    for row in rows[1:]:
        rendered.append(
            "| " + " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)) + " |"
        )
    return "\n".join(rendered) + "\n"


def main() -> None:
    assumptions = list_markdown_notes(
        VALUATION_ROOT / "memory" / "venture" / "assumptions", required_field="assumption_id"
    )
    probes = list_markdown_notes(
        VALUATION_ROOT / "memory" / "venture" / "probes", required_field="probe_id"
    )
    evidence = list_markdown_notes(
        VALUATION_ROOT / "memory" / "venture" / "evidence", required_field="evidence_id"
    )
    decisions = list_markdown_notes(
        VALUATION_ROOT / "memory" / "venture" / "decisions", required_field="decision_id"
    )

    candidate_assumptions = list_markdown_notes(
        ROOT / "memory" / "assumptions", required_field="assumption_id"
    )
    draft_probes = list_markdown_notes(
        ROOT / "memory" / "probes" / "drafts", required_field="probe_id"
    )
    signals = list_markdown_notes(ROOT / "memory" / "signals")

    evidence_by_assumption: dict[str, list[Note]] = defaultdict(list)
    for note in evidence:
        assumption_id = note.fields.get("assumption_id")
        if isinstance(assumption_id, str):
            evidence_by_assumption[assumption_id].append(note)

    latest_decision = latest_by_key(decisions, "assumption_id")

    active_assumptions = [
        note for note in assumptions if note.fields.get("status") == "active"
    ]
    active_probe_by_assumption = {
        note.fields.get("assumption_id"): note
        for note in probes
        if note.fields.get("status") == "active"
    }

    now = datetime.now(UTC)
    report: list[str] = []
    report.append("# Foundry Loop Status")
    report.append("")
    report.append(f"- `generated_at`: `{now.strftime('%Y-%m-%dT%H:%M:%SZ')}`")
    report.append(f"- `valuation_root`: `{VALUATION_ROOT}`")
    report.append(f"- `researcher_root`: `{ROOT}`")
    report.append("")
    report.append("## Snapshot")
    report.append("")
    report.append(f"- active Stage 1 assumptions: `{len(active_assumptions)}`")
    report.append(f"- active Stage 1 probes: `{sum(1 for note in probes if note.fields.get('status') == 'active')}`")
    report.append(f"- evidence notes: `{len(evidence)}`")
    report.append(f"- decision notes: `{len(decisions)}`")
    report.append(f"- candidate assumptions: `{len(candidate_assumptions)}`")
    report.append(f"- draft probes: `{len(draft_probes)}`")
    report.append(f"- signal notes: `{len(signals)}`")
    report.append("")
    report.append("## Active Lanes")
    report.append("")

    lane_rows = [[
        "assumption_id",
        "probe_id",
        "external_status",
        "latest_decision",
        "next_action",
    ]]
    attention: list[str] = []
    recent_evidence_rows = [["evidence_id", "assumption_id", "class", "quality", "observed_at"]]

    for assumption in active_assumptions:
        assumption_id = str(assumption.fields.get("assumption_id", assumption.path.stem))
        probe = active_probe_by_assumption.get(assumption_id)
        decision = latest_decision.get(assumption_id)
        lane_evidence = evidence_by_assumption.get(assumption_id, [])
        external_status = bucket_external_status(lane_evidence)
        decision_type = str(decision.fields.get("decision_type", "none")) if decision else "none"
        next_action = str(decision.fields.get("next_action", "missing")) if decision else "missing"
        probe_id = str(probe.fields.get("probe_id", "missing")) if isinstance(probe, Note) else "missing"

        lane_rows.append([assumption_id, probe_id, external_status, decision_type, next_action])

        if external_status in {"none", "internal_only"}:
            attention.append(
                f"`{assumption_id}` has no admissible external evidence yet; current status is `{external_status}`."
            )
        if next_action == "missing":
            attention.append(f"`{assumption_id}` is missing a current `next_action` in the latest decision note.")
        if probe_id == "missing":
            attention.append(f"`{assumption_id}` has no active probe note linked from valuation canon.")

        for note in sorted(
            lane_evidence,
            key=lambda item: parse_timestamp(item.fields.get("observed_at")) or datetime.min.replace(tzinfo=UTC),
            reverse=True,
        )[:2]:
            recent_evidence_rows.append([
                str(note.fields.get("evidence_id", note.path.stem)),
                assumption_id,
                str(note.fields.get("evidence_class", "unknown")),
                str(note.fields.get("evidence_quality", "unknown")),
                fmt_date(parse_timestamp(note.fields.get("observed_at"))),
            ])

    report.append(render_table(lane_rows))
    report.append("## Attention Queue")
    report.append("")
    if attention:
        for item in attention:
            report.append(f"- {item}")
    else:
        report.append("- No immediate structural gaps detected.")
    report.append("")
    report.append("## Recent Evidence")
    report.append("")
    report.append(render_table(recent_evidence_rows))
    report.append("## Research Backlog")
    report.append("")

    backlog_rows = [["category", "count", "notes"]]
    backlog_rows.append(["candidate_assumptions", str(len(candidate_assumptions)), "research-side critical assumptions not yet promoted"])
    backlog_rows.append(["draft_probes", str(len(draft_probes)), "probe drafts awaiting live Stage 1 selection"])
    backlog_rows.append(["signal_notes", str(len(signals)), "raw or semi-structured hunt and target notes"])
    report.append(render_table(backlog_rows))

    report.append("## Operator Guidance")
    report.append("")
    report.append("- Run this report at least daily while any Stage 1 lane is active.")
    report.append("- Treat `internal_only` as operational proof, not commercial proof.")
    report.append("- Promote nothing without typed external evidence recorded in valuation canon.")
    report.append("- Update the latest decision note whenever a lane changes state, not just when a new product artifact ships.")
    report.append("")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report), encoding="utf-8")


if __name__ == "__main__":
    main()
