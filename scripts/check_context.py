#!/usr/bin/env python3
"""Validate the shared declarative context-repository contract."""

from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]
required = ("README.md", "repo.toml", "Makefile", "AGENTS.md", "CLAUDE.md",
            "CURRENT_STATE.md", "docs/architecture.md", "skillfoundry.toml",
            "memory", "bundles", "artifacts", "runs")
missing = [path for path in required if not (ROOT / path).exists()]
if missing:
    raise SystemExit(f"missing required paths: {', '.join(missing)}")
repo = tomllib.loads((ROOT / "repo.toml").read_text(encoding="utf-8"))
context = tomllib.loads((ROOT / "skillfoundry.toml").read_text(encoding="utf-8"))
if repo.get("schema_version") != 1 or repo.get("shape") != "context":
    raise SystemExit("repo.toml must declare schema_version=1 and shape=context")
if context.get("repository", {}).get("schema_version") != "1":
    raise SystemExit("skillfoundry.toml repository schema_version must be '1'")
for path in context.get("frontdoor", {}).get("pinned_paths", []):
    if not (ROOT / path).is_file():
        raise SystemExit(f"missing pinned front-door path: {path}")
print("OK context declaration and pinned front door")
