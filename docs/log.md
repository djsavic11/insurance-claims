# Log

Use this file only when an agent starts or completes a real task.
Do not use it for repo setup notes or documentation cleanup.

## Format

- Task: short task name
- Done: what changed
- Next: what should happen next
- Blocker: any issue or decision needed

## Entries

### 2026-05-15

- Task: convert extraction prompt to Markdown
- Done: replaced the split Bedrock prompt text files with a single Markdown prompt file containing front matter plus `## System` and `## User` sections, extended the prompt manager to parse that format, and wired Bedrock extraction to use prompt metadata for inference settings
- Next: keep future prompt changes in Markdown prompt files under `prompts/`
- Blocker: none

- Task: add local prompt template manager
- Done: added a dependency-free prompt template manager under `src/lib/`, moved the Bedrock extraction system and user prompts into `prompts/bedrock/`, and wired Bedrock extraction to render those templates before calling Converse
- Next: none in `Now`/`Next`; continue with `Later` tasks only when approved
- Blocker: none

### 2026-05-10

- Task: fix visible evaluation PDFs
- Done: regenerated `data/evaluation/input/claim-eval-001.pdf`, `claim-eval-002.pdf`, and `claim-eval-003.pdf` as valid visible PDF documents while preserving the expected evaluation claim content
- Next: keep evaluation PDF fixtures viewer-readable and extractor-readable
- Blocker: none

### 2026-05-08

- Task: update agentic workflow references
- Done: replaced the GitHub Copilot reference in `docs/README.md` with official OpenAI Codex references for AGENTS.md, harness engineering, and PLANS.md execution planning
- Next: keep references focused on sources that directly support the documented Codex workflow
- Blocker: none

- Task: simplify developer prompt examples
- Done: shortened `docs/README.md` prompt examples so they express developer intent instead of repeating repository rules already covered by `AGENTS.md`
- Next: keep prompts concise and avoid duplicating agent instructions
- Blocker: none

- Task: clarify AGENTS.md prompt usage
- Done: updated `docs/README.md` so developer prompt examples no longer ask Codex to read `AGENTS.md` manually, because Codex and compatible agents load it as repository-level instructions
- Next: keep developer prompts focused on task intent and source-of-truth project docs
- Blocker: none

- Task: remove supporting project docs section from agentic workflow guide
- Done: removed the `Supporting Project Docs` section from `docs/README.md` so the guide stays focused only on the Codex workflow files
- Next: keep evaluation documentation discoverable through the root README
- Blocker: none

- Task: move evaluation documentation to root
- Done: moved `docs/evaluation.md` to `EVALUATION.md` and updated README, docs guide, and task references so evaluation reads as project documentation rather than core agentic workflow state
- Next: keep `docs/` focused on Codex workflow, plan, spec, task state, and execution log
- Blocker: none

- Task: clarify evaluation docs relationship to agentic workflow
- Done: updated `docs/README.md` so evaluation documentation is described as supporting project documentation linked from the root README, not as part of the core Codex workflow
- Next: keep workflow docs focused on agent instructions, plan, spec, task state, and execution log
- Blocker: none

- Task: add agentic workflow terminology and references
- Done: updated `docs/README.md` to name the approach as a spec-driven agentic development workflow and link it to AGENTS.md, docs-as-code, spec-driven development, context engineering, and repository custom instruction practices
- Next: keep external references limited to concepts that directly explain this repository workflow
- Blocker: none

- Task: refine docs README agentic workflow guide
- Done: rewrote `docs/README.md` so it opens with a clear agentic workflow summary, removes repeated purpose/maintenance/review sections, and keeps detailed workflow, ownership, prompts, and examples in separate sections
- Next: keep future workflow changes in this guide concise and example-driven
- Blocker: none

- Task: document Codex agentic workflow examples
- Done: expanded `docs/README.md` with the Codex workflow, developer prompt examples, example task flows, file update ownership, and human decision responsibilities
- Next: use these prompt patterns when starting future Codex task runs
- Blocker: none

- Task: remove meta instructions from docs README
- Done: revised `docs/README.md` so it reads as human-facing documentation guidance rather than exposing agent-specific instruction framing
- Next: keep the docs guide concise and aligned with the working docs
- Blocker: none

- Task: rewrite docs README for agentic workflow
- Done: replaced the generic `docs/README.md` with an explanation of how the docs folder supports human review and agent-assisted task coordination according to `AGENTS.md`
- Next: keep `docs/README.md` aligned with `AGENTS.md` if workflow rules change
- Blocker: none

- Task: align README patterns with implementation
- Done: rewrote the README engineering section as `Implemented Patterns` with concrete repository features including S3 prefixes, Lambda triggers, Bedrock Converse integration, schema validation, model configuration, local fallback extraction, invocation logging, and evaluation artifacts
- Next: run evaluation and populate the README results table
- Blocker: none

- Task: professionalize README engineering section
- Done: reframed the README skills section as `Engineering Focus` and rewrote the bullets around implementation qualities instead of personal skill demonstration
- Next: run evaluation and populate the README results table
- Blocker: none

- Task: refine README project positioning
- Done: reframed the README overview from a portfolio PoC to an example real-world AI system, emphasizing architecture, workflow, structured outputs, deployment, sample data, and evaluation artifacts
- Next: run evaluation and populate the README results table
- Blocker: none

- Task: address README review comments
- Done: removed the explicit certification reference from the README, expanded the skills demonstrated section with model selection, evaluation, logging, and orchestration details, moved detailed documentation guidance into `docs/README.md`, and replaced the simple limitations section with production readiness notes
- Next: run evaluation and populate the README results table
- Blocker: none

- Task: update README for portfolio demo
- Done: rewrote `README.md` to emphasize the portfolio context, implemented AWS/Bedrock capabilities, demo flow, sample output, prerequisites, evaluation workflow, and placeholder result table for future evaluation data
- Next: run local and Bedrock evaluation, then replace the placeholder table values with measured results
- Blocker: none

### 2026-05-07

- Task: update claim output validation schema and processor response building
- Done: updated `src/lib/claim_output.py` to validate the richer claim output schema and updated `src/handlers/claims_processor.py` to build responses with the new fields while preserving temporary compatibility with the old `amount` extractor output
- Next: update the Bedrock extraction prompt and response parser to return the richer claim output schema
- Blocker: none

- Task: update Bedrock extraction prompt and response parser
- Done: updated `src/lib/bedrock_extraction.py` so the Bedrock prompt requests the richer schema fields and the parser returns the richer output shape, including temporary compatibility mapping from legacy `amount` to `claim_amount`
- Next: update the local fallback extractor to return the richer claim output schema for offline runs
- Blocker: none

- Task: execute remaining evaluation implementation queue
- Done: updated local fallback extraction to richer schema, created 3 synthetic evaluation PDF samples and matching expected-answer files, added evaluation folder structure, updated sample processed output shape, added `scripts/evaluate_claims.py` for local deterministic scoring and optional Bedrock evaluation job submission, added CDK Bedrock evaluation prerequisites (S3 paths, role, permissions, conditional CORS), and added evaluation/readme documentation updates
- Next: none in `Now`/`Next`; continue with `Later` tasks only when approved
- Blocker: none

- Task: address evaluation review findings
- Done: updated Bedrock Evaluation BYOI JSONL output to use `modelResponses`, changed managed evaluation submission to create one job per model identifier, and fixed CDK context parsing for the optional console CORS flag
- Next: none in `Now`/`Next`; continue with `Later` tasks only when approved
- Blocker: none

### 2026-05-06

- Task: align plan and task queue with richer claim output schema
- Done: updated `docs/plan.md` to reference the stable claim schema from `docs/spec.md` and added the processor/schema implementation task to `docs/tasks.md`
- Next: update processor code, prompt behavior, validation schema, local fallback extraction, and sample output to produce the richer claim output structure
- Blocker: none

- Task: address schema planning review comments
- Done: removed Bedrock Evaluation wording from the schema-change plan section and expanded the active implementation task to include new testable sample claim files
- Next: update processor code, prompt behavior, validation schema, local fallback extraction, sample output, and sample claim files for the richer output structure
- Blocker: none

- Task: define evaluation phase and split implementation tasks
- Done: updated `docs/plan.md` to make Evaluation a dedicated phase before policy enrichment, updated `docs/spec.md` with evaluation inputs, outputs, and rules, and split `docs/tasks.md` into smaller schema, sample, evaluation, and documentation tasks
- Next: start with the claim output validation schema and processor response-building update
- Blocker: none

- Task: tighten evaluation planning after review
- Done: moved policy enrichment out of the execution phases and into backlog, added concrete evaluation artifact paths and scoring rules to `docs/spec.md`, and made the evaluation tasks more explicit
- Next: start with the claim output validation schema and processor response-building update
- Blocker: none

- Task: add Bedrock Evaluation CDK prerequisite planning
- Done: updated `docs/plan.md` and `docs/tasks.md` with the S3, IAM service role, model invocation, and optional CORS prerequisites needed before running Amazon Bedrock Evaluation jobs
- Next: start with the claim output validation schema and processor response-building update
- Blocker: none

- Task: review evaluation planning completeness
- Done: clarified that historical starter tasks are not the active queue and added code organization/reusability as documented evaluation findings in the plan, spec, and task list
- Next: start with the claim output validation schema and processor response-building update
- Blocker: none

- Task: document combined evaluation reporting flow
- Done: clarified that local structured extraction results and Amazon Bedrock Evaluation summary-quality results should be combined in the final findings rather than compared as competing evaluators
- Next: start with the claim output validation schema and processor response-building update
- Blocker: none

- Task: specify evaluation sample document requirements
- Done: updated `docs/spec.md` and `docs/tasks.md` to require at least 3 synthetic claim PDF samples with different layouts and all richer schema fields present
- Next: start with the claim output validation schema and processor response-building update
- Blocker: none

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

### 2026-05-02

- Task: document single-bucket S3 storage decision
- Done: updated the live task queue, plan, and spec to use one S3 bucket with `claims/` for input documents and `processed/` for generated outputs
- Next: refactor the CDK stack to match the documented single-bucket storage layout
- Blocker: none

- Task: refactor the CDK stack to use one S3 bucket with `claims/` for inputs and `processed/` for outputs
- Done: replaced the separate input and output buckets with one claims bucket, updated the Lambda environment and permissions to read and write the same bucket, refreshed the sample event and upload helper wording, and updated the README to describe outputs under the `processed/` prefix
- Next: add CDK support for Amazon Bedrock model invocation logging with S3 and CloudWatch Logs
- Blocker: none

- Task: add CDK support for Amazon Bedrock model invocation logging with S3 and CloudWatch Logs
- Done: added CDK-managed Bedrock invocation logging configuration through an AWS custom resource so the stack now enables account-and-Region Bedrock logging to Amazon S3 and CloudWatch Logs during deployment
- Next: configure Bedrock invocation log delivery in CDK to use a log prefix in the existing claims S3 bucket
- Blocker: none

- Task: configure Bedrock invocation log delivery in CDK to use a log prefix in the existing claims S3 bucket
- Done: reused the existing claims bucket for Bedrock invocation logs under the `bedrock-invocation-logs/` prefix, added the required bucket policy for the Bedrock service principal, and exposed the log prefix as a stack output
- Next: configure the required CloudWatch Logs log group and IAM service role in CDK for Bedrock invocation logging
- Blocker: none

- Task: configure the required CloudWatch Logs log group and IAM service role in CDK for Bedrock invocation logging
- Done: added a dedicated CloudWatch Logs log group and Bedrock service role with the required trust and `logs:CreateLogStream` and `logs:PutLogEvents` permissions, and wired both into the deployed invocation logging configuration
- Next: none
- Blocker: none
