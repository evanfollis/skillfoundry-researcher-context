# Workflow: Bottleneck To Market Candidate

## Goal

Convert a real builder bottleneck into:

1. an internal mechanism or research artifact that sharpens the opportunity, and
2. a product candidate that can later be evaluated for public launch.

## Steps

1. Capture high-signal sources into `artifacts/sources/`.
2. Curate and summarize them into evidence notes.
3. Update `memory/findings/ranked_bottlenecks.md`.
4. Select one bottleneck and decide whether the immediate next artifact is:
   - an internal mechanism brief, or
   - an external product brief.
5. Write or update the relevant brief bundle in `bundles/briefs/`.
6. Draft mechanism-facing or launch-facing artifacts under `artifacts/projections/`.
7. Hand off the brief and projection artifacts to downstream design and build work.

## Quality Bar

- Every canon claim should point back to grounded evidence.
- Internal mechanisms and external products should never be described as the same
  thing.
- The first external product should expose a narrow tool surface.
- Any launch-facing artifact should explain tools, inputs, outputs, example prompts,
  and limits.
- Price and positioning should be deliberate before public publish because post-publish
  changes are constrained.

## Kill Criteria

Kill or re-rank a candidate if:

- the value cannot be explained clearly in one paragraph,
- the server would need too many tools to feel coherent,
- the likely user is outside the chosen ICP,
- or the path to public HTTPS deployment is too heavy for a first launch.
