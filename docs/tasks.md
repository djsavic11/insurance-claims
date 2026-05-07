# Tasks

## Now

- Update the Bedrock extraction prompt and response parser to return the richer claim output schema

## Next

- Update the local fallback extractor to return the richer claim output schema for offline runs
- Generate at least 3 testable synthetic claim PDF files under `data/evaluation/input/` with different layouts and with claimant name, policy number, incident date, claim amount, and incident description present
- Update the sample processed output JSON to match the richer claim output schema
- Add `data/evaluation/input/`, `data/evaluation/expected/`, `data/evaluation/results/`, and `data/evaluation/bedrock-evaluation/`
- Add expected-answer JSON files for each evaluation sample document, using filenames that match the input document stems
- Add a local evaluation runner for schema validation, deterministic structured field accuracy, 2-model comparison, and processing time measurement
- Add CDK prerequisites for Amazon Bedrock Evaluation: S3 evaluation input/output locations and an IAM service role that Bedrock can assume
- Grant the Bedrock Evaluation service role permissions to read evaluation input, write evaluation output, and invoke selected generator and evaluator models
- Add S3 CORS configuration for evaluation storage only if console-created Bedrock Evaluation jobs are used
- Add Amazon Bedrock Evaluation job support for generated summary quality and store the job input/output references under `data/evaluation/bedrock-evaluation/`
- Combine local structured extraction results and Bedrock Evaluation summary-quality results in the final evaluation findings
- Add `docs/evaluation.md` with evaluation methodology, metrics, code organization/reusability notes, limitations, and combined findings
- Update README with a short evaluation summary and link to `docs/evaluation.md`
- Update README with basic AWS CDK commands for synth, diff, deploy, and bootstrap

## Later

- Add PII checks and guardrails
- Add policy enrichment from Amazon Knowledge Bases
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
- Add CDK support for Amazon Bedrock model invocation logging with S3 and CloudWatch Logs
- Configure Bedrock invocation log delivery in CDK to use a log prefix in the existing claims S3 bucket
- Configure the required CloudWatch Logs log group and IAM service role in CDK for Bedrock invocation logging
- Update the claim output validation schema and processor response building to match the richer claim output schema in `docs/spec.md`
