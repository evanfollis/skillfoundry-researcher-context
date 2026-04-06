# Bottleneck Radar

Short description:

Turn noisy builder signals into ranked bottlenecks and concise product briefs.

## What it does

Bottleneck Radar helps MCP builders and technical operators move from scattered user
signals to a ranked shortlist of worthwhile problems. Feed it URLs, issue threads,
docs, or pasted signal text and it returns clustered bottlenecks with evidence and
confidence. Then use a second tool to turn one chosen bottleneck into a concise
builder-ready product brief.

## Tools

### `analyze_signals`

Input:

- public URLs
- issue text
- forum or support snippets

Output:

- ranked bottleneck clusters
- evidence snippets
- confidence signals
- suggested next questions

### `draft_brief`

Input:

- one selected bottleneck cluster

Output:

- target user
- problem statement
- suggested narrow MCP product shape
- constraints and risks
- launch angle

## Example prompts

- "Analyze these GitHub issues and tell me which bottlenecks are worth building an MCP server around."
- "Take this cluster and draft a product brief I can hand to a builder."
- "Rank the strongest recurring pains in these community threads."

## Limits

- Best for technical/product signals, not generic market sizing.
- Quality depends on the relevance of the input sources.
- Output is decision support, not guaranteed product-market fit.

## Launch notes

- initial visibility: unlisted
- initial price hypothesis: $0.08 per successful call
- rationale: low-friction first launch for a high-leverage but still trust-building tool
