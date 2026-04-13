# Always-On Foundry Loop

This note describes how Skillfoundry should evolve from occasional bursts into a more
automated, constantly running loop.

The objective is not to automate everything immediately. It is to automate the right
surfaces in the right order while preserving evidence discipline.

## Loop Layers

### Layer 1: signal intake

Purpose:

- keep fresh signals arriving continuously

Outputs:

- raw notes in `memory/signals/`
- updates to [IDEA_HUNT.md](../findings/IDEA_HUNT.md)

Automation target:

- recurring sweeps of official docs, policy pages, marketplace surfaces, and selected research feeds
- generated loop status reports in `memory/reports/`

Human role:

- decide which signals are noise versus actual bottlenecks

### Layer 2: assumption synthesis

Purpose:

- convert signals into candidate `CriticalAssumption` records

Outputs:

- candidate notes in `memory/assumptions/`

Automation target:

- clustering, de-duplication, and pre-formatting

Human role:

- sharpen the buyer, problem, economic claim, and falsification rule

### Layer 3: probe queueing

Purpose:

- decide which assumptions deserve scarce live Stage 1 capacity

Outputs:

- shortlist notes
- draft probes
- promotion into valuation-side active assumptions

Automation target:

- ranking suggestions, stale-lane detection, queue summaries

Human role:

- capacity-aware selection and explicit kill/continue judgments

### Layer 4: live evidence capture

Purpose:

- keep active lanes honest

Outputs:

- typed evidence records in valuation canon
- explicit decisions

Automation target:

- reminder generation
- target ledger updates
- telemetry-to-evidence handoff suggestions

Human role:

- classify evidence quality correctly
- decide what it means

### Layer 5: primitive extraction

Purpose:

- turn repeated internal wins into sellable external primitives

Outputs:

- updated product candidates
- new internal mechanisms
- stronger hunt heuristics

Automation target:

- pattern summaries across lanes
- recurring objection extraction
- repeated-fix detection

Human role:

- decide whether the pattern is truly externalizable or merely internally useful

## Cadence

### Daily

- add fresh signals
- update the active target ledger
- record new evidence and next actions

### Weekly

- re-rank candidate assumptions
- choose which probes stay active
- kill or pause weak lanes explicitly
- update `IDEA_HUNT.md` with search-method performance

### Monthly

- review repeated internal bottlenecks
- ask which primitives are becoming externalizable
- update the sequencing logic in [COMPOUNDING_PRIMITIVES.md](../findings/COMPOUNDING_PRIMITIVES.md)

## Automation Priorities

Automate first:

- source sweeps
- note scaffolding
- stale queue detection
- basic ledger maintenance
- telemetry summarization
- active lane status reporting
- target harvest and queue refresh for live probes
- target enrichment and contact-path extraction

Automate later:

- candidate clustering
- ranking suggestions
- objection pattern extraction

Do not automate prematurely:

- final evidence interpretation
- promotion decisions
- productization decisions

## Invariants

- every active lane must have one next action
- every live probe must have a target evidence class
- every meaningful external interaction should become a typed evidence note
- every week should produce at least one explicit keep, tighten, pause, or kill judgment

## Immediate Operational Use

For the current phase, use this loop to keep two systems moving at once:

1. `launchpad-lint` stays live and gathers real external signal
2. `launch-compliance-intelligence` runs as the next manual offer probe

That is enough to start compounding without pretending the whole foundry is already autonomous.

## First Automation Surface

The first actual operator aid is the generated report:

- [foundry_loop_status.md](../reports/foundry_loop_status.md)

Run it with:

```bash
python3 skillfoundry-researcher-context/scripts/foundry_loop_report.py
```

Use the report to find:

- active lanes with only internal evidence
- missing next actions
- backlog pressure versus live Stage 1 capacity
