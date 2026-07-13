---
name: CURRENT_STATE
description: Front door for the skillfoundry-researcher-context repo — what the researcher owns, what's active, what's stale, where to dig deeper
type: front-door
updated: 2026-07-13
---

# CURRENT_STATE — skillfoundry-researcher-context

**Last updated**: 2026-07-13T02:23Z — reflection pass. LCI lane park fully enforced (code guard in `foundry_loop_run.py`). No new external evidence. Data/API sleeve still has no researcher artifact (5th cycle).

---

## What this repo owns

The researcher's live context workspace. It holds:
- active research tracks (target lists, signals, outreach queue)
- candidate critical assumptions and draft probes (before promotion to valuation-context)
- findings, ICP definitions, and mechanism briefs
- workflows and plans for the always-on foundry loop

This repo feeds downstream agents (valuation, growth, product) with grounded inputs. It is **not** a truth source for commercial evidence — promoted assumptions and probes live in `skillfoundry-valuation-context`.

## Portfolio framing note (ADR-0033, 2026-05-21)

Research outputs now support three sleeve types, not one: agent/developer tooling (existing focus), data/API products (structured feeds derived from the research pipeline itself — marketplace diffs, launch-readiness metadata, compliance feeds, landscape signals), and research/content licensing (machine-readable research surfaces). AgenticMarket is **one channel for one sleeve**, not the business. See `memory/mission.md` for the updated mission framing and `../skillfoundry-harness/docs/passive-income-candidates/` for concrete data/API candidate proposals.

---

## Active research tracks

### 1. Launchpad Lint — waiting for first external interaction

- Assumption: implicit via valuation-context (`launchpad-lint-first-external-commitment`)
- Status: listed live on AgenticMarket; 0 external evidence recorded
- No pending researcher-side work — monitoring only

### 2. Candidate assumptions / probe drafts (backlog)

- `memory/assumptions/agent-evaluation-trust-evidence.md`
- `memory/assumptions/tool-surface-compression.md`
- `memory/probes/drafts/agent-evaluation-trust-review.md`
- `memory/probes/drafts/tool-surface-compression-review.md`
- Not promoted; awaiting external evidence signal before elevation

---

## Parked lanes (dormant — not blockers, not work items)

### Launch Compliance Intelligence (LCI) — PARKED 2026-07-12

Parked on **explicit principal instruction** per Decision
`2026-07-12-park-launch-compliance-intelligence-lane`
(`skillfoundry-valuation-context/memory/venture/decisions/`). `decision_type:
pause` — **reversible; the assumption is preserved, not falsified.**

The probe ran 79 days past its own `stale_close_date` (2026-04-24) at `status:
active` with all 10 drafts unsent and zero external contact ever made. The
`falsification_rule` was never exercised. What failed was the **channel** —
direct outreach requires principal-initiated contact, which this workspace does
not do — not the problem thesis.

**This is no longer an open principal blocker.** The decision the reflection loop
was escalating for since 2026-05-02 has now been made. Reflection cycles must
stop reporting "10 unsent drafts" as a pending blocker; the disposition exists.

Preserved (dormant, nothing deleted):

- Target list: `memory/signals/launch_compliance_target_list.md` (~45KB, 2026-04-11)
- Outreach queue: `memory/signals/outreach_queue.md` — **DORMANT, not a send queue**
- Draft messages: `memory/signals/outreach_drafts/` (10 files, 0 sent)
- Assumption: `memory/assumptions/launch-compliance-intelligence.md`
- Probe draft: `memory/probes/drafts/launch-compliance-intelligence-manual-offer.md`
- Harvest/enrich reports + scripts: `memory/reports/`, `scripts/`

**The park is enforced in code, not just declared.** `scripts/foundry_loop_run.py`
regenerates `outreach_queue.md` from scratch on every run — a single run would
have erased the dormant marker and rebuilt a live `drafted` send queue holding 10
real people's contact addresses. A banner in a file that a script overwrites is
not a park. The loop now hard-stops on `LANE_PARKED` (no-op, exit 0 — a parked
lane is designed behavior, not a failure), and `write_outreach_queue()` raises if
called directly. Verified: running the loop leaves the queue byte-identical.

There is **no send capability anywhere in skillfoundry** — no SMTP, no mail
client, no Twitter/GitHub API writer. The queue cannot auto-send even if
regenerated. Audited 2026-07-12.

**Resume only on a positive signal**: an inbound request, fresh buyer-demand
evidence, a materially better zero-touch channel, or explicit principal
reprioritization. The continued existence of the drafts is not a reason to
resume. On resume, re-verify every target — the list is ~3 months stale — write a
successor Decision, and flip `LANE_PARKED` **last**, not first.

---

## What is stale / degraded

- `memory/reports/foundry_loop_status.md` generated 2026-04-11 — **93 days stale**. Path references inside (`valuation_root`, `researcher_root`) point to `/opt/projects/...` (old path); canonical is `/opt/workspace/projects/...`. Loop broken by path drift independent of the LCI park.
- No automated workflow has run since 2026-04-11 (93+ days). The harvest→enrich→score→draft loop (`19281a7`) emits no structured telemetry — cannot distinguish "ran and found nothing" from "never ran."
- No user-directed feature commits since 2026-04-11. The session that committed `1b6a4f3` and `a5bac8a` (2026-07-12) was the first attended session in ~71 days, run via claude.ai rather than local Claude Code.
- No external evidence on any assumption. (The LCI outreach queue is no longer counted here — the lane was **parked 2026-07-12**; see "Parked lanes" above. Its drafts are dormant by decision, not stalled by neglect.)

---

## Known broken or degraded

- **Foundry loop paths stale**: `foundry_loop_status.md:3-4` and likely `foundry_loop_run.py` constants block reference `/opt/projects/` paths. Fix before any future lane activation or the loop will fail silently on first run.
- **No telemetry**: researcher workflows emit nothing; loop health is invisible to reflection and meta-scan. `foundry_loop_run.py` exits parked-lane state with a `print()`, not a structured `eventType: "throttled"` event.
- **reflect.sh auto-commit has never produced a commit in this repo**: The fix proposal (`proposal-fix-reflect-sh-argument-ordering-2026-05-24T03-29-01Z.md`) is no longer in INBOX; the current `reflect.sh:245-249` has correct argument ordering. But no `reflect: auto-update` commit appears in this repo's history. All CURRENT_STATE.md updates have required attended sessions. Status uncertain — the auto-commit gate may work now, or there may be a different failure mode (Write tool blocked in reflection-spawned sessions). Next reflection should verify.
- **Data/API sleeve has no researcher artifact**: ADR-0033 framing landed in mission.md 2026-05-21; `c6071bb` in skillfoundry-harness wrote a monetization preflight for this sleeve. Researcher-context has no corresponding assumption, probe draft, or signal file. 53 days without a researcher artifact for the second declared portfolio sleeve.
- **Adversarial review gate dead**: No `/review` invocation in 19+ consecutive cycles across related skillfoundry sessions. The 2026-07-12 code change to `foundry_loop_run.py` was a meaningful behavioral enforcement that should have triggered review.

---

## What bit the last session

- The 2026-07-12 attended session (via claude.ai, Claude Opus 4.8) correctly caught that commit `1b6a4f3` alone was insufficient — marking the outreach queue file DORMANT is reversed by a single loop run. The code guard in `a5bac8a` was the right response.
- The 14:17 UTC July 12 reflection pass (`d588b88d`) hit a session usage limit immediately and produced no output — no reflection file exists for that window. This is the first observed truncation. reflect.sh likely did not emit a failure telemetry event.
- All meaningful decisions continue to be made by the principal directly via claude.ai, not by local sessions or automated loops. The loop produces diagnosis; execution still requires direct principal engagement.

---

## Recent decisions

- 2026-04-30: Created `CURRENT_STATE.md` front door to close harness-check gap. Grounded in real state; honest about stale status and blockers.
- 2026-05-01 (c9faf97): Reflection pass (02:32) removed false escalation reference. Committed via attended session because reflect.sh auto-commit did not fire.
- 2026-05-02: Reflection pass surfaced 3-cycle URGENT threshold crossing for LCI blocker. CANNOT self-execute URGENT handoff; escalated to general session / principal via reflection file.
- 2026-05-21 (67b2ed6): ADR-0033 portfolio broadening applied to mission.md — three research sleeve types now explicit.
- 2026-05-22 through 2026-05-26: Ten consecutive reflection-only windows. LCI escalation carried forward each cycle. reflect.sh auto-commit failure confirmed recurring. Root cause diagnosed at 2026-05-24T14:27Z; fix proposal entered INBOX.
- **2026-07-12T21:45Z — LCI lane PARKED** (attended session via claude.ai, explicit principal instruction). Decision `2026-07-12-park-launch-compliance-intelligence-lane` (`decision_type: pause`, reversible). Two commits: `1b6a4f3` documented the park; `a5bac8a` enforced it in code. Closes a ~71-day escalation loop. Nothing sent externally; assumption parked not falsified.
- **2026-07-13T02:23Z — reflection pass**: Verified park enforcement. Updated Known Broken (reflect.sh count was stale; auto-commit status uncertain). Flagged: data/API sleeve at 53 days without researcher artifact (5th cycle); session-limit truncation on 14:17 pass; foundry loop paths still broken; no telemetry on parked-lane exit.

---

## What the next agent must read first

1. `memory/mission.md` — three-sleeve mission framing (updated 2026-05-21)
2. **LCI lane decision: MADE — parked 2026-07-12.** Read `skillfoundry-valuation-context/memory/venture/decisions/2026-07-12-park-launch-compliance-intelligence-lane.md`. Do **not** re-open as an escalation; the disposition exists. The outreach queue is dormant.
3. `skillfoundry-valuation-context/CURRENT_STATE.md` — commercial lane truth source
4. `runtime/.meta/skillfoundry-researcher-reflection-2026-07-13T02-23-02Z.md` — latest reflection (this pass: 5 proposals, 3 questions)
5. `memory/reports/foundry_loop_status.md` — **stale and path-broken**; verify before acting on any loop reference

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
