# Candidate CriticalAssumption: launch-compliance-intelligence

- `assumption_id`: `candidate-launch-compliance-intelligence`
- `status`: `candidate`
- `created_at`: `2026-04-11`
- `owner`: `skillfoundry`
- `source_note`: [IDEA_HUNT.md](../findings/IDEA_HUNT.md)

## Title

Builders launching MCP servers will pay for a narrow tool that tells them whether
their server is directory-ready, policy-safe, and trust-legible before they submit it
or broaden distribution.

## Why This Made The Shortlist

- directly adjacent to `launchpad-lint`, so it reuses current understanding and channel access
- official policy surfaces are now explicit enough to create repeated failure modes
- strong candidate for a narrow product with clear before/after usefulness

## Buyer

- primary buyer role: solo MCP builder or small automation agency preparing a public launch
- likely economic buyer: the same operator, especially when launch mistakes would delay visibility or trust

## Problem Claim

Builders do not just need "better copy." They need help translating technical servers
into assets that are compatible with marketplace, directory, and trust requirements.

## Economic Claim

The cost of a bad launch is high enough in time, confusion, and lost early trust that
builders will pay for a focused preflight check if it is fast and concrete.

## Channel Claim

The best first surface is the current launch and listing ecosystem: AgenticMarket,
Anthropic directory requirements, and other public MCP submission surfaces.

## First Likely Probe

- likely probe type: `manual_offer`
- artifact shape: launch compliance review sold as a narrow preflight service or guided audit
- possible follow-on probe: MCP tool that maps one server package against known directory and policy constraints

## Target Evidence

- target evidence class: `external_conversation`
- minimum evidence quality: `moderate`
- preferred stronger evidence: `external_commitment`

## What Would Count As Support

- external builders say they are confused about policy, trust, or readiness rather than only marketing copy
- a builder asks for a review, requests terms, or gives concrete repeat-intent
- builders distinguish this from a generic copywriting or marketing service

## What Would Falsify It

- repeated conversations show builders only want better promotional copy, not compliance/readiness help
- builders see policy or directory work as too occasional or too low-value to pay for
- the pain is real but is already solved by simple checklists with no willingness to pay for guided support

## Search Trail

- source path that led here:
  - official MCP directory/policy docs
  - current `launchpad-lint` lane
  - marketplace-surface checks
- method quality: `high`
- reason:
  - this path emerged from practical constraints rather than trend speculation
