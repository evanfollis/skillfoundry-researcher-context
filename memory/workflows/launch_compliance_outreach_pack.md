# Launch Compliance Outreach Pack

This pack supports the live Stage 1 lane:

- assumption: `launch-compliance-intelligence-first-paid-review`
- probe: `launch-compliance-intelligence-manual-offer`

Canonical valuation references:

- [launch-compliance-intelligence-first-paid-review.md](/opt/projects/skillfoundry/skillfoundry-valuation-context/memory/venture/assumptions/launch-compliance-intelligence-first-paid-review.md)
- [launch-compliance-intelligence-manual-offer.md](/opt/projects/skillfoundry/skillfoundry-valuation-context/memory/venture/probes/launch-compliance-intelligence-manual-offer.md)

## Goal

Get the first admissible external evidence for the live launch-compliance lane.

This pack is not for broad marketing. It is for direct, evidence-seeking outreach.

## Target Profile

Best first targets:

- solo builders with a live or near-live MCP server
- small automation agencies packaging a public server
- builders visibly preparing listings, launch docs, or trust surfaces

Good signs:

- public repo plus server docs but weak packaging
- listing copy that looks unclear, incomplete, or generic
- signs of launch friction, directory questions, or trust/approval uncertainty
- active discussion about launch prep, compatibility, or submission issues

Weak signs:

- no public launch intent at all
- obvious hobby projects with no commercial intent
- mature teams with clear internal launch/compliance ownership

## Offer

Offer a narrow review of one MCP server package focused on:

- trust and compatibility checklist
- directory-readiness gaps
- submission-risk notes
- prioritized fixes

The offer should remain narrow. Do not sell generic go-to-market consulting.

## Outreach Sequence

### Touch 1: direct pain hypothesis

Goal:

- test whether the builder recognizes launch compliance and readiness as a separate pain

Template:

> I’ve been looking closely at MCP launches and keep seeing a gap between “server works” and “server is actually ready for public distribution.”  
>  
> Your server looks close to launchable, but I suspect there may be hidden trust, compatibility, or directory-readiness issues that are different from just polishing copy.  
>  
> I’m testing a narrow review that flags those issues for one server package. If that sounds relevant, I can show you the exact shape of the review.

### Touch 2: concrete review shape

Goal:

- move from abstract interest to concrete engagement

Template:

> The review is intentionally narrow: trust/compatibility checklist, directory-readiness gaps, submission-risk notes, and a short prioritized fix list.  
>  
> I’m not trying to sell broad launch strategy here. I’m trying to see whether builders actually want this specific preflight layer before they push harder on distribution.  
>  
> If useful, send the current repo/docs/listing materials and I’ll tell you whether the framing is off.

### Touch 3: commitment ask

Goal:

- convert interest into admissible evidence

Template:

> I’m trying to distinguish curiosity from real pain. If this is useful enough to engage with, the clean next step is for you to send the current package or ask for terms on the review.  
>  
> If it feels like this is just “better copy help,” that’s also useful to know and I’d rather learn that quickly.

## What Counts As Evidence

Counts:

- the builder distinguishes compliance/readiness pain from generic copy help
- the builder sends materials for review
- the builder asks for terms, timing, or scope
- the builder describes a concrete launch risk this would reduce

Does not count:

- polite agreement with no follow-up
- generic “interesting” responses
- vague praise without pain specificity
- internal discussion only

## Logging Rules

After every meaningful contact:

1. create or update a target row in the target list
2. write a typed evidence record in valuation canon
3. update the next action

Refresh the queue with:

```bash
python3 skillfoundry-researcher-context/scripts/launch_compliance_target_harvest.py
```

Generated source and harvest artifacts:

- [launch_compliance_sources.md](../signals/launch_compliance_sources.md)
- [launch_compliance_target_list.md](../signals/launch_compliance_target_list.md)
- [launch_compliance_harvest_report.md](../reports/launch_compliance_harvest_report.md)

Target enrichment:

```bash
python3 skillfoundry-researcher-context/scripts/launch_compliance_target_enrich.py
```

- [launch_compliance_enrichment_report.md](../reports/launch_compliance_enrichment_report.md)
- [target_profiles/README.md](../signals/target_profiles/README.md)

Use the valuation evidence template:

- [TEMPLATE_external_conversation.md](/opt/projects/skillfoundry/skillfoundry-valuation-context/memory/venture/evidence/TEMPLATE_external_conversation.md)

## Decision Boundary

Continue the lane only if conversations reveal real willingness to engage with this
specific review shape.

If the market keeps translating the offer into generic launch copy help, do not widen
the lane by hand-waving. Record that as falsification pressure.
