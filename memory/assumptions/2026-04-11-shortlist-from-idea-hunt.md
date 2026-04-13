# 2026-04-11 Shortlist From IDEA_HUNT

This note converts the first scouting pass in [IDEA_HUNT.md](../findings/IDEA_HUNT.md)
into concrete Stage 1 candidate assumptions.

Selection rule for this pass:

- choose paths that look commercially reachable soon
- prefer pains that can be tested with a cheap external probe
- avoid paths that depend on frontier autonomy being "already solved"
- keep at least one candidate adjacent to the live `launchpad-lint` lane

## Shortlist

### 1. MCP launch compliance and directory-readiness intelligence

- reason for selection:
  - strongest adjacency to existing Skillfoundry work
  - policy and compatibility constraints are getting sharper
  - likely to produce immediate builder pain around trust, packaging, and approval surfaces
- candidate assumption:
  - [launch-compliance-intelligence.md](./launch-compliance-intelligence.md)

### 2. Tool-surface compression and allowed-tools governance

- reason for selection:
  - official docs now warn that too many tools create cost, latency, and selection problems
  - this looks like a repeated design/ops bottleneck rather than a one-off launch issue
- candidate assumption:
  - [tool-surface-compression.md](./tool-surface-compression.md)

### 3. Agent evaluation and trust evidence for real deployments

- reason for selection:
  - recent papers argue current capability narratives are too optimistic
  - trust and evaluation may be easier wedges than building full autonomous systems
- candidate assumption:
  - [agent-evaluation-trust-evidence.md](./agent-evaluation-trust-evidence.md)

## Not Shortlisted Yet

### Agent memory products

- reason:
  - likely real pain, but too easy to drift into infra-for-infra's-sake
  - needs a more concrete buyer and workflow before it becomes a strong Stage 1 candidate

### Voice and real-time agent operations

- reason:
  - plausibly valuable, but farther from current Skillfoundry channel access and current edge

### Generic interruption-compression products

- reason:
  - trend signal is strong, but the category is broad and crowded
  - needs a much tighter workflow slice before entering the next shortlist

## Next Step

Turn these three candidates into:

- one likely probe draft each
- one target evidence class each
- one first external contact or distribution path each
