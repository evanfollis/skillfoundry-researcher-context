# Probe Draft: agent-evaluation-trust-review

- `probe_id`: `draft-agent-evaluation-trust-review`
- `assumption_id`: `candidate-agent-evaluation-trust-evidence`
- `status`: `draft`
- `probe_type`: `manual_offer`
- `artifact_class`: `service_probe`

## Shape

Offer a narrow evaluation and trust review for one real agent workflow.

Deliverable shape:

- workflow risk map
- reliability blind spots
- what current tests miss
- recommendation on whether the workflow is safe to broaden, needs tightening, or should stay internal

## Why This Probe First

- evaluation pain is likely real, but buyer willingness is less certain than in the other shortlisted paths
- manual review is the cheapest way to find out if teams want trust evidence enough to pay for it

## Target Evidence

- target evidence class: `external_conversation`
- minimum evidence quality: `moderate`
- preferred stronger evidence: `external_commitment`

## Continue Rule

Continue if operators say trust and evaluation are blocking rollout and at least one
team asks for a scoped review, pilot, or concrete next step.

## Kill Rule

Kill or pause if the real urgent pain turns out to be integration plumbing, model cost,
or missing capability rather than trust evidence.
