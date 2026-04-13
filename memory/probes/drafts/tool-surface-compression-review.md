# Probe Draft: tool-surface-compression-review

- `probe_id`: `draft-tool-surface-compression-review`
- `assumption_id`: `candidate-tool-surface-compression`
- `status`: `draft`
- `probe_type`: `manual_offer`
- `artifact_class`: `service_probe`

## Shape

Offer a narrow review of one live or near-live agent workflow to recommend:

- which tools should stay exposed
- which tools should be hidden or combined
- which tools should require approval
- where the current surface creates unnecessary token, latency, or trust cost

## Why This Probe First

- manual review is faster than building a recommender prematurely
- gives direct access to the buyer's current tool sprawl and language
- can reveal whether this is a recurring paid pain or just an interesting technical issue

## Target Evidence

- target evidence class: `external_conversation`
- minimum evidence quality: `moderate`
- preferred stronger evidence: `external_commitment`

## Continue Rule

Continue if technical teams describe tool-surface choice as an active operational pain
and at least one team requests a review or proposal.

## Kill Rule

Kill or pause if teams treat this as a trivial settings issue or if the pain always
collapses into broader architecture consulting with no narrow wedge.
