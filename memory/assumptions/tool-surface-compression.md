# Candidate CriticalAssumption: tool-surface-compression

- `assumption_id`: `candidate-tool-surface-compression`
- `status`: `candidate`
- `created_at`: `2026-04-11`
- `owner`: `skillfoundry`
- `source_note`: [IDEA_HUNT.md](../findings/IDEA_HUNT.md)

## Title

Technical teams shipping agentic products will pay for help deciding the minimum safe
and useful tool surface to expose because excessive tool surfaces create cost, latency,
confusion, and trust problems.

## Why This Made The Shortlist

- multiple official docs now explicitly warn about tool overload and tool filtering
- narrow enough to test with a design-review or governance-style offer
- closer to repeated operational pain than broad "agent platform" claims

## Buyer

- primary buyer role: technical founder, staff engineer, or product engineer exposing tools to an agent framework
- likely economic buyer: engineering lead or founder responsible for reliability, cost, and product clarity

## Problem Claim

Teams can build and expose tools quickly, but they struggle to decide:

- which tools should be exposed at all
- which tools should require approval
- which tools should stay hidden behind a narrower interface

## Economic Claim

Bad tool-surface decisions increase latency, token spend, failure modes, and user
confusion enough that teams may pay for a fast governance and compression review.

## Channel Claim

The best first surface is likely direct founder or builder outreach, using technical
teams already experimenting with MCP or hosted agent workflows.

## First Likely Probe

- likely probe type: `manual_offer`
- artifact shape: "tool-surface review" or "allowed-tools audit" for one existing agent workflow
- possible follow-on probe: docs-to-tool-surface or allowed-tools recommendation assistant

## Target Evidence

- target evidence class: `external_conversation`
- minimum evidence quality: `moderate`
- preferred stronger evidence: `external_commitment`

## What Would Count As Support

- teams say tool selection and tool exposure are active pain points rather than a solved configuration task
- buyers distinguish this from generic prompt engineering
- at least one external team asks for a review, sends docs, or requests a proposal

## What Would Falsify It

- teams see this as a one-time setup task with little economic importance
- buyers collapse the problem into broader architecture consulting with no narrow wedge
- the real pain is elsewhere, such as retrieval quality or output quality, not tool-surface design

## Search Trail

- source path that led here:
  - OpenAI remote MCP docs
  - Anthropic programmatic tool calling docs
  - Vercel AI SDK 5 release
- method quality: `high`
- reason:
  - official platform docs are explicitly naming the failure mode, which is a strong scouting signal
