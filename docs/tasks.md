# Tasks

## Now

- None

## Next

- None

## Later

- Add PII checks and guardrails
- Add policy enrichment from Amazon Knowledge Bases
- Compare 2 models max for demo purposes
- Add a simple UI only if it materially improves the demo

## Blocked

- None

## Done

- Initialize Git repository
- Create `setup-project` branch
- Commit initial repository files
- Create `docs/plan.md`
- Create `AGENTS.md`
- Organize working docs under `docs/`
- Decide the implementation runtime for the PoC
- Create the minimal folder structure
- Scaffold the CDK stack
- Implement the first Lambda handler path
- Enable local testing for the Lambda handler
- Define the first extraction output schema
- Add a sample input document for the demo
- Define validation rules for the extraction output schema
- Add a sample event payload for local handler runs
- Implement the first Lambda handler path with Bedrock invocation
- Scaffold the first S3-triggered infrastructure resources in CDK
- Implement a local CLI upload script using `boto3` to upload `data/input/claim-001.pdf` to the S3 input bucket
- Refactor the CDK stack to use one S3 bucket with `claims/` for inputs and `processed/` for outputs
