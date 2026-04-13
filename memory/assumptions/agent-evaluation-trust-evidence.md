# Candidate CriticalAssumption: agent-evaluation-trust-evidence

- `assumption_id`: `candidate-agent-evaluation-trust-evidence`
- `status`: `candidate`
- `created_at`: `2026-04-11`
- `owner`: `skillfoundry`
- `source_note`: [IDEA_HUNT.md](../findings/IDEA_HUNT.md)

## Title

Teams deploying real agentic workflows will pay for narrow evaluation and trust
evidence products before they pay for more autonomy, because current capability
claims overstate real-world reliability.

## Why This Made The Shortlist

- recent papers consistently suggest that long-horizon and web-agent capability is less mature than the hype implies
- this creates a gap between demos and operational confidence
- trust/evaluation support is more likely to be immediately valuable than selling "more autonomy"

## Buyer

- primary buyer role: technical team lead or operator responsible for a live or near-live agent workflow
- likely economic buyer: engineering or product owner who needs evidence before broader rollout

## Problem Claim

Teams are being told agents are ready for complex real-world tasks, but they lack a
clear way to evaluate whether their specific workflow is reliable enough to trust.

## Economic Claim

The cost of hidden failures, false confidence, and rollout mistakes is high enough
that a narrow evaluation and trust-evidence product could justify paid demand.

## Channel Claim

The best first channel is likely direct outreach to teams already operating internal
or external agent workflows, not broad public marketplace distribution.

## First Likely Probe

- likely probe type: `manual_offer`
- artifact shape: narrow workflow evaluation review with a trust-risk writeup
- possible follow-on probe: benchmark-backed evaluator for one workflow class such as launch, browsing, or multi-tool approval flows

## Target Evidence

- target evidence class: `external_conversation`
- minimum evidence quality: `moderate`
- preferred stronger evidence: `external_commitment`

## What Would Count As Support

- operators say they do not trust current evaluation practices
- buyers ask for help proving whether a workflow is reliable enough to ship
- at least one external team requests a scoped evaluation or risk review

## What Would Falsify It

- teams say their main pain is not trust but raw capability or integration plumbing
- evaluation is acknowledged as important but not urgent enough to pay for
- the demand collapses into generic QA or consulting with no narrow, repeatable wedge

## Search Trail

- source path that led here:
  - recent benchmarking papers on web agents, long-horizon agents, and memory
  - official ecosystem shifts indicating more teams will attempt production agent workflows
- method quality: `medium-high`
- reason:
  - strong structural signal, but buyer-path clarity is weaker than the first two candidates
