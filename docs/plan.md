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

### Extensions Later

- PII checks and guardrails
- Policy enrichment from Amazon Knowledge Bases
- Model comparison
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
- Add optional Amazon Knowledge Bases integration point

### 3. Document Processing Flow

- Implement document ingestion from S3 event
- Implement document parsing and prompt preparation
- Implement extraction for the stable claim schema, including claimant, policy, incident, amount, description, and summary fields
- Save outputs in the structured format defined in `docs/spec.md`

### 4. Safety And Validation

- Add basic PII handling checks
- Add guardrail touchpoints
- Add validation rules for the stable claim output schema

### 5. Evaluation

- Compare 2 models max for demo purposes
- Use structured fields for deterministic information extraction accuracy checks
- Track simple metrics such as field accuracy, summary quality, and processing latency
- Store evaluation outputs for demo review

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

Add enrichment and lightweight model evaluation.

### Phase 4

Add a minimal UI only if it improves the demo materially.

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

## First Recommended Tasks

1. Create the minimal folder structure
2. Scaffold the CDK stack
3. Implement the first Lambda handler path
4. Define the first extraction output schema
5. Add a sample input document for the demo
