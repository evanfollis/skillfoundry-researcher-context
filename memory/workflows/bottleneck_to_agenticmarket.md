# Workflow: Bottleneck To AgenticMarket

## Goal

Convert a real builder bottleneck into a listing-ready hosted MCP server concept that
can be implemented and submitted to AgenticMarket quickly.

## Steps

1. Capture high-signal sources into `artifacts/sources/`.
2. Curate and summarize them into evidence notes.
3. Update `memory/findings/ranked_bottlenecks.md`.
4. Select one bottleneck and write or update a product brief bundle in `bundles/briefs/`.
5. Draft marketplace-facing artifacts under `artifacts/projections/agenticmarket/`.
6. Hand off the brief and projection artifacts to downstream design and build work.

## Quality Bar

- Every canon claim should point back to grounded evidence.
- The first product should expose a narrow tool surface.
- The draft listing should explain tools, inputs, outputs, example prompts, and limits.
- Price and positioning should be deliberate before public publish because post-publish
  changes are constrained.

## Kill Criteria

Kill or re-rank a candidate if:

- the value cannot be explained clearly in one paragraph,
- the server would need too many tools to feel coherent,
- the likely user is outside the chosen ICP,
- or the path to public HTTPS deployment is too heavy for a first launch.
