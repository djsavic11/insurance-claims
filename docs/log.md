# Log

Use this file only when an agent starts or completes a real task.
Do not use it for repo setup notes or documentation cleanup.

## Format

- Task: short task name
- Done: what changed
- Next: what should happen next
- Blocker: any issue or decision needed

## Entries

### 2026-05-01

- Task: decide implementation runtime for the PoC
- Done: selected Python 3.12 as the shared runtime for Lambda, CLI tooling, and AWS CDK, with simple `venv` + `pip` packaging for phase 1
- Next: create the minimal folder structure
- Blocker: none
