# PLAN

## Goal

Proof of concept for an AI-powered insurance claims processing pipeline built on AWS.

## Delivery Style

- Primary: CLI
- Optional: simple UI for demo display

## Guiding Principle

Keep the PoC intentionally small.
Prefer a clear end-to-end demo over complete architecture or production-level quality.

## Smallest End-to-End Demo

### Core Slice

1. Upload a claim document to Amazon S3
2. Trigger an AWS Lambda handler
3. Invoke Amazon Bedrock from Lambda
4. Extract the stable structured claim schema defined in `docs/spec.md`
5. Save results back to Amazon S3 under a separate output prefix

### Backlog / Optional Later

- PII checks and guardrails
- Policy enrichment from Amazon Knowledge Bases
- Simple UI for demo display

## Execution Order

1. Project Setup
2. AWS Infrastructure
3. Core Document Processing Flow
4. Safety and Validation
5. Evaluation
6. Optional UI

## Workstreams

### 1. Project Setup

- Create the minimal repo structure
- Use Python 3.12 across Lambda, CLI tooling, and CDK to keep the repo single-language
- Use simple `venv` + `pip` packaging for phase 1
- Add placeholder folders for data, prompts, and outputs

### 2. AWS Infrastructure

- Use AWS CDK for infrastructure definition
- Define the minimal CDK stack
- Create one S3 bucket with separate prefixes for documents and outputs
- Create Lambda function and event trigger
- Add Bedrock access configuration
- Configure account-level Bedrock invocation logging through CDK using the claims bucket and CloudWatch Logs
- Do not add Amazon Knowledge Bases infrastructure in the current phase

### 3. Document Processing Flow

- Implement document ingestion from S3 event
- Implement document parsing and prompt preparation
- Keep prompt templates separated from processing code
- Implement extraction for the stable claim schema, including claimant, policy, incident, amount, description, and summary fields
- Save outputs in the structured format defined in `docs/spec.md`

### 4. Safety And Validation

- Add basic PII handling checks
- Add guardrail touchpoints
- Add validation rules for the stable claim output schema

### 5. Evaluation

- Compare 2 models max for demo purposes
- Use structured fields for deterministic information extraction accuracy checks
- Use Amazon Bedrock Evaluation for generated summary quality
- Provision Bedrock Evaluation prerequisites in CDK before running managed evaluation jobs
- Generate Bedrock Evaluation JSONL input from local evaluation records
- Combine local structured extraction results with Bedrock Evaluation summary-quality results in the final evaluation findings
- Track simple metrics such as field accuracy, summary quality, and processing latency
- Document code organization and reusability as engineering findings, not as an automated metric
- Store evaluation outputs for demo review

#### Bedrock Evaluation Prerequisites

- Use S3 locations for Bedrock Evaluation input datasets and output reports
- Add an IAM service role that Amazon Bedrock can assume for evaluation jobs
- Allow the evaluation service role to read evaluation input, write evaluation output, and invoke selected generator and evaluator models
- Configure S3 CORS only if Bedrock Evaluation jobs are created through the AWS console
- Keep CDK responsible for prerequisites; create or start evaluation jobs from the local evaluation runner or manually in the console

### 6. Optional UI

- Show uploaded document
- Show extracted fields and summary
- Keep UI minimal and demo-focused

## Thinking Layer

### Phase 1

Define the smallest runnable slice:
S3 upload under `claims/` -> Lambda -> Bedrock -> structured output under `processed/`

### Phase 2

Add safety, validations, and cleaner extraction behavior.

### Phase 3

Add a local-first evaluation flow for model comparison, structured extraction accuracy, generated summary quality, and processing latency.

### Phase 4

Add a minimal UI only if it improves the demo materially.

### Backlog

Add policy enrichment from Amazon Knowledge Bases only after the core processing and evaluation phases are stable.
Keep enrichment separate from baseline extraction accuracy so evaluation results stay easy to explain.

## Out Of Scope

- Complex components or complex architecture
- Deep production hardening
- User management
- Production application concerns
- Unit tests
- End-to-end tests

## Agent Instructions

- Pick one task at a time
- Keep changes small and easy to review
- Do not expand scope beyond the current phase
- Update docs when assumptions or scope change
- Use [tasks.md](tasks.md) for task state
- Use [log.md](log.md) only when executing a real task
- Prefer progress on the end-to-end demo path over side improvements

## Historical First Recommended Tasks

These starter tasks are historical context only.
Use [tasks.md](tasks.md) for the current active queue.

1. Create the minimal folder structure
2. Scaffold the CDK stack
3. Implement the first Lambda handler path
4. Define the first extraction output schema
5. Add a sample input document for the demo
