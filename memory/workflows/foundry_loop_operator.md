# Foundry Loop Operator

This workflow explains how to run the always-on loop as a repeatable operating
system instead of an intermittent research burst.

## Primary Command

From the Skillfoundry root:

```bash
python3 skillfoundry-researcher-context/scripts/foundry_loop_report.py
```

This generates or refreshes:

- [foundry_loop_status.md](../reports/foundry_loop_status.md)

## What The Report Is Allowed To Do

The report may:

- summarize active Stage 1 lanes
- count backlog notes
- flag missing next actions
- flag lanes with only internal evidence
- show recent evidence and decisions

The report may not:

- promote a lane
- kill a lane
- reinterpret evidence quality automatically
- replace valuation canon

## Daily Operator Routine

1. Run the report.
2. Read the attention queue.
3. For each active lane, confirm there is one concrete next action.
4. If a new external interaction happened, write a typed evidence note in valuation canon.
5. If a lane meaningfully changed, add or update the decision note.

## Weekly Operator Routine

1. Run the report.
2. Review whether active lanes have produced admissible external evidence.
3. Pause or kill lanes that have gone stale.
4. Promote at most one additional candidate into live Stage 1 if capacity exists.
5. Update [IDEA_HUNT.md](../findings/IDEA_HUNT.md) with search-method performance notes.

## Scheduling Guidance

The report generator is cheap and deterministic enough to run on a schedule.

Good first automation options:

- cron job on the workstation or server
- systemd timer that executes the Python script
- tmux session hook or shell alias that runs before daily review

Do not add stateful automation first. Start by automating visibility.

## Current Use

Right now this operator workflow exists to keep these lanes honest:

- `launchpad-lint-first-external-commitment`
- `launch-compliance-intelligence-first-paid-review`

## Input Refresh Command

For the launch-compliance lane, refresh the target queue with:

```bash
python3 skillfoundry-researcher-context/scripts/launch_compliance_target_harvest.py
```

This updates:

- [launch_compliance_target_list.md](../signals/launch_compliance_target_list.md)
- [launch_compliance_harvest_report.md](../reports/launch_compliance_harvest_report.md)

Then enrich the first-pass targets with:

```bash
python3 skillfoundry-researcher-context/scripts/launch_compliance_target_enrich.py
```

This updates:

- [launch_compliance_enrichment_report.md](../reports/launch_compliance_enrichment_report.md)
- `memory/signals/target_profiles/`
