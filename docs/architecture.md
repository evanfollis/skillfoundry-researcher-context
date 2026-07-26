# Architecture

This `context` repository is the researcher agent’s durable Git-backed
lineage. `skillfoundry.toml` declares identity, front-door pins, and promotion
policy. `memory/` contains findings, workflows, signals, assumptions, and
plans; `bundles/` contains promoted inputs. Operator scripts report and advance
specific foundry loops but do not change epistemic status by themselves.

`runs/` and raw artifacts are non-canonical execution surfaces. The parked LCI
lane guard in `scripts/foundry_loop_run.py` is a load-bearing decision
enforcement point, not generic runtime behavior.

## July 2026 transition exceptions

The new instruction front door and existing mission/profile prompts lack a
fresh ADR-0039 baseline. Owner: Skillfoundry researcher context; milestone:
create a production-grounded eval loop before central conformance advances
from `migrating`. `runs/` still contains a tracked placeholder and is not yet
declared as an ignored runtime path. Host containment gaps remain
supervisor-owned under ADR-0050.
