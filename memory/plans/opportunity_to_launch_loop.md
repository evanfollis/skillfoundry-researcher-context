# Opportunity To Launch Loop

## Current Goal

Use internal mechanisms to sharpen real opportunity selection, then promote one narrow
external MCP product candidate into the AgenticMarket launch lane with clear
activation and pricing hypotheses.

## Chosen First Mechanism

`bottleneck-radar`

Given URLs, issue trackers, docs, or pasted signal text, return ranked bottleneck
clusters with evidence and a builder-oriented opportunity brief. This is an internal
factory mechanism, not the first monetized product.

## Mechanism Shape

- tool 1: `analyze_signals`
  Input: URLs and/or pasted issue text
  Output: ranked bottleneck clusters with evidence snippets and confidence
- tool 2: `draft_brief`
  Input: one selected bottleneck cluster
  Output: a concise opportunity brief with user, problem, constraints, and likely
  launch angle

## External Launch Strategy

The first public distribution surface remains AgenticMarket, but the public launch
candidate has not been selected yet. `bottleneck-radar` exists to improve that
selection and produce better external product briefs.

## Current Selection Rule

- use `bottleneck-radar` to rank opportunities and draft briefs
- choose one external product candidate with a narrow, legible value proposition
- only then create listing-facing and pricing-facing launch artifacts

## Validation Targets

- at least one returned bottleneck cluster feels decision-relevant to the operator
- the generated brief is good enough to hand to design and builder work
- the mechanism helps reduce uncertainty about what external product should launch next

## Immediate Next Deliverables

- final mechanism brief bundle for `bottleneck-radar`
- operator note for mechanism usage and deployment
- builder handoff for the internal mechanism implementation
- first downstream external product candidate brief
