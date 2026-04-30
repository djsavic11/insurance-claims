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

- Task: create the minimal folder structure
- Done: added placeholder directories for infrastructure, Lambda handlers, shared Python code, prompts, and sample input/output data, and added a minimal `.gitignore`
- Next: scaffold the CDK stack
- Blocker: none

- Task: scaffold the CDK stack
- Done: added a minimal Python CDK app, dependency file, and placeholder stack class under `infra/cdk/`
- Next: implement the first Lambda handler path
- Blocker: none

- Task: implement the first Lambda handler path
- Done: added a minimal Lambda entrypoint that parses the first S3 record, derives a fallback claim identifier from the object key, and returns the required extraction-shaped payload
- Next: define the first extraction output schema
- Blocker: none
