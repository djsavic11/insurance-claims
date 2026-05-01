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

- Task: enable local testing for the Lambda handler
- Done: added a standalone local entrypoint so the claims processor can be run directly with a built-in sample S3 event or a JSON event file
- Next: define the first extraction output schema
- Blocker: none

- Task: define the first extraction output schema
- Done: added a shared claim output schema module and updated the handler to build responses through that contract
- Next: add a sample input document for the demo
- Blocker: none

- Task: add a sample input document for the demo
- Done: added `data/input/claim-001.pdf` as a small single-page sample claim document for local development and demo work
- Next: define validation rules for the extraction output schema
- Blocker: none

- Task: define validation rules for the extraction output schema
- Done: tightened the shared schema contract so `claim_id` and `summary` must be non-empty strings, `amount` must be non-negative or `null`, and unsupported top-level fields are rejected
- Next: add a sample event payload for local handler runs
- Blocker: none

- Task: add a sample event payload for local handler runs
- Done: added `data/events/s3-put-claim-001.json` so the handler can be exercised locally with a checked-in S3 event payload
- Next: implement the first Lambda handler path with Bedrock invocation
- Blocker: none

- Task: implement the first Lambda handler path with Bedrock invocation
- Done: updated the claims processor to load the uploaded PDF, extract readable text, call Amazon Bedrock when `BEDROCK_MODEL_ID` is configured, fall back to a local regex extractor for offline runs, and persist the structured output to S3 or the local output folder
- Next: scaffold the first S3-triggered infrastructure resources in CDK
- Blocker: none

- Task: scaffold the first S3-triggered infrastructure resources in CDK
- Done: added dedicated input and output S3 buckets, a Python 3.12 Lambda function, an S3 object-created trigger on the `claims/` prefix, Bedrock invoke permissions, and CloudFormation outputs for the generated resource names
- Next: implement a local CLI upload script using `boto3` to upload `data/input/claim-001.pdf` to the S3 input bucket
- Blocker: none

- Task: implement a local CLI upload script using `boto3` to upload `data/input/claim-001.pdf` to the S3 input bucket
- Done: added `scripts/upload_claim.py` so the sample PDF can be uploaded to the deployed input bucket with a small `boto3` CLI helper
- Next: none
- Blocker: none
