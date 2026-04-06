# AgenticMarket Launch Loop

## Current Goal

Get one narrow hosted MCP server from research brief to live AgenticMarket listing with
clear activation and pricing hypotheses.

## Chosen First Product

`bottleneck-radar`

Given URLs, issue trackers, docs, or pasted signal text, return ranked bottleneck
clusters with evidence and a builder-oriented opportunity brief.

## Product Shape

- tool 1: `analyze_signals`
  Input: URLs and/or pasted issue text
  Output: ranked bottleneck clusters with evidence snippets and confidence
- tool 2: `draft_brief`
  Input: one selected bottleneck cluster
  Output: a concise product brief with user, problem, constraints, and launch angle

## Initial Launch Strategy

- Deploy as a hosted HTTPS MCP server.
- Start unlisted on AgenticMarket to validate end-to-end install and usage.
- Use the marketplace long description as the canonical public README for the listing.
- Keep the first call price conservative because post-publish price changes require a
  new listing.

## Initial Pricing Hypothesis

- launch hypothesis: $0.08 per successful call
- rationale: low enough to reduce install hesitation, high enough to price actual
  research leverage above generic utility calls

## Validation Targets

- install to first successful call within one session
- at least one returned bottleneck cluster that feels decision-relevant to the user
- users can understand the server from the listing without external explanation

## Immediate Next Deliverables

- final product brief bundle for `bottleneck-radar`
- AgenticMarket listing draft
- builder handoff with tool contract and deployment checklist
