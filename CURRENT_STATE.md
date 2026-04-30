---
name: CURRENT_STATE
description: Front door for the skillfoundry-researcher-context repo — what the researcher owns, what's active, what's stale, where to dig deeper
type: front-door
updated: 2026-04-30
---

# CURRENT_STATE — skillfoundry-researcher-context

**Last updated**: 2026-04-30 — front-door created (harness-check gap)

---

## What this repo owns

The researcher's live context workspace. It holds:
- active research tracks (target lists, signals, outreach queue)
- candidate critical assumptions and draft probes (before promotion to valuation-context)
- findings, ICP definitions, and mechanism briefs
- workflows and plans for the always-on foundry loop

This repo feeds downstream agents (valuation, growth, product) with grounded inputs. It is **not** a truth source for commercial evidence — promoted assumptions and probes live in `skillfoundry-valuation-context`.

---

## Active research tracks

### 1. Launch Compliance Intelligence (LCI) — stalled at outreach

- Target list: `memory/signals/launch_compliance_target_list.md` (~45KB, 2026-04-11)
- Outreach queue: `memory/signals/outreach_queue.md` — 10 drafts, all status `drafted` (not sent)
- Draft messages: `memory/signals/outreach_drafts/` (10 files)
- Assumption: `memory/assumptions/launch-compliance-intelligence.md`
- Probe draft: `memory/probes/drafts/launch-compliance-intelligence-manual-offer.md`
- **Blocker**: Outreach not sent. Sending requires principal decision (Tally form + channel access).
  Escalation on file: `general-skillfoundry-tally-form-needed-2026-04-18.md`

### 2. Launchpad Lint — waiting for first external interaction

- Assumption: implicit via valuation-context (`launchpad-lint-first-external-commitment`)
- Status: listed live on AgenticMarket; 0 external evidence recorded
- No pending researcher-side work — monitoring only

### 3. Candidate assumptions / probe drafts (backlog)

- `memory/assumptions/agent-evaluation-trust-evidence.md`
- `memory/assumptions/tool-surface-compression.md`
- `memory/probes/drafts/agent-evaluation-trust-review.md`
- `memory/probes/drafts/tool-surface-compression-review.md`
- Not promoted; awaiting external evidence signal before elevation

---

## What is stale / degraded

- `memory/reports/foundry_loop_status.md` was generated 2026-04-11. Operator guidance says "run daily" — it is 19 days stale as of this update.
- No new git commits since 2026-04-11 (`aef4c63`).
- `valuation_root` paths in the status report reference `/opt/projects/...` (old path); canonical path is `/opt/workspace/projects/...`.

---

## What the next agent must read first

1. `memory/mission.md` — why this repo exists and what it produces
2. `memory/reports/foundry_loop_status.md` — last known lane / evidence snapshot (stale, verify before acting)
3. `memory/signals/outreach_queue.md` — 10 unsent outreach drafts
4. `skillfoundry-valuation-context/CURRENT_STATE.md` — commercial lane truth source

---

## Where to find deeper material

| What you need | Where |
|---|---|
| Target lists | `memory/signals/launch_compliance_target_list.md`, `memory/signals/target_profiles/` (28 files) |
| Raw signals | `memory/signals/launch_compliance_sources.md` |
| Outreach drafts | `memory/signals/outreach_drafts/` |
| Candidate assumptions | `memory/assumptions/` |
| Findings / ICP | `memory/findings/` |
| Probe drafts | `memory/probes/drafts/` |
| Workflows | `memory/workflows/` |
| Plans | `memory/plans/` |
| Enrichment/harvest reports | `memory/reports/` |
| Mechanism briefs | `artifacts/projections/mechanisms/` |
