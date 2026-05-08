# AI-Powered Insurance Claims Processing on AWS

Proof of Concept demonstrating a production-minded Generative AI document-processing workflow for insurance claims using Amazon Bedrock, AWS Lambda, and Amazon S3.

## Goals

This PoC was designed to demonstrate:

- practical GenAI architecture patterns on AWS
- AI-powered document-processing workflows
- foundation model integration with Amazon Bedrock
- document understanding and structured information extraction
- insurance claim summary generation
- evaluation and observability foundations
- production-minded system design considerations
- infrastructure-as-code deployment with AWS CDK

## Overview

This repository is an example of a real-world AI system for insurance claims processing on AWS.
It shows how Generative AI can be introduced into an enterprise document workflow with clear architecture, event-driven processing, structured outputs, and measurable evaluation.

The implementation demonstrates how an uploaded claim document can move through an AWS pipeline, be processed by Amazon Bedrock, and produce a stable JSON result that can be reviewed, stored, evaluated, or consumed by downstream systems.

The scope is intentionally narrow: deliver a focused end-to-end workflow with architecture diagrams, runnable code, deployment steps, sample data, and evaluation artifacts rather than a full production insurance platform.

## Architecture Patterns

This example focuses on concrete patterns used in AI document-processing systems:

- **S3 prefix-based workflow:** claim PDFs are uploaded under `claims/`, while generated JSON outputs are stored under `processed/`.
- **Event-driven Lambda processing:** an S3 object-created event invokes the claims processor without requiring a polling service.
- **Bedrock Converse integration:** the processor uses Amazon Bedrock through `boto3` for structured extraction and claim summarization.
- **Schema-first extraction:** model output is normalized into a fixed claim schema and validated before storage.
- **Configurable model runtime:** CDK context controls the deployed Bedrock model, and `BEDROCK_MODEL_ID` controls local Bedrock runs.
- **Offline development path:** a local fallback extractor allows the handler and evaluation runner to work without live model calls.
- **Invocation observability:** CDK configures Bedrock invocation logging to Amazon S3 and Amazon CloudWatch Logs.
- **Evaluation artifact flow:** the local runner scores structured fields, records latency, and prepares Bedrock Evaluation JSONL/job references.

## System Architecture

The current architecture uses a simple event-driven pipeline:

The current implementation focuses on a narrow but realistic end-to-end workflow intended for portfolio demonstration, architecture discussions, and GenAI experimentation.

1. A synthetic claim PDF is uploaded to Amazon S3 under the `claims/` prefix.
2. An S3 object-created event triggers an AWS Lambda function.
3. Lambda loads the PDF, extracts readable text, and invokes Amazon Bedrock when configured.
4. The processor returns normalized claim fields and a generated summary.
5. The JSON output is saved back to the same S3 bucket under the `processed/` prefix.

![Architecture](architecture.png)

## Tech Stack

- **AWS services:** Amazon S3, AWS Lambda, Amazon Bedrock, Amazon CloudWatch Logs, IAM
- **Infrastructure:** AWS CDK with Python
- **Runtime:** Python 3.12
- **SDKs and tools:** `boto3`, `venv`, `pip`
- **Evaluation:** local deterministic extraction scoring plus optional managed Amazon Bedrock Evaluation jobs

## Core Features

- S3-triggered claims-processing Lambda
- single-bucket storage layout with `claims/` input and `processed/` output prefixes
- Amazon Bedrock model invocation from the processing path
- local fallback extraction for offline development
- stable claim JSON schema and validation rules
- sample synthetic claim PDFs and S3 event payloads
- CDK-managed Bedrock invocation logging prerequisites
- CDK-managed Bedrock Evaluation input/output locations and IAM role
- local evaluation runner for extraction accuracy, latency, and Bedrock Evaluation dataset generation

## GenAI Workflow

The processing pipeline uses Amazon Bedrock to:

- analyze uploaded insurance claim documents
- extract structured claim information
- normalize model responses into a stable schema
- generate claim summaries
- support downstream evaluation workflows

The implementation intentionally focuses on deterministic outputs, schema normalization, and observable processing behavior instead of purely prompt-driven experimentation.

## Future Improvements

- basic PII checks and guardrail touchpoints
- policy enrichment with Retrieval-Augmented Generation
- minimal UI for demo visualization, only if it improves the portfolio presentation

## Example Workflow

1. A claim PDF is uploaded to Amazon S3.
2. An S3 event triggers the claims-processing Lambda.
3. The processor extracts text and invokes Amazon Bedrock.
4. Structured claim fields are extracted and validated.
5. A generated summary is produced.
6. Final JSON results are written back to S3.
7. Evaluation artifacts and logs can be used for analysis and benchmarking.

## Sample Output

The processor produces a stable JSON object:

```json
{
  "claim_id": "claim-001",
  "claimant_name": "Jane Doe",
  "policy_number": "POL-123456",
  "incident_date": "2026-04-18",
  "claim_amount": 2450.75,
  "incident_description": "Water damage reported after a burst pipe in the kitchen.",
  "summary": "Jane Doe filed a claim for kitchen water damage related to policy POL-123456."
}
```

If a field cannot be extracted, the processor returns `null` for that field while preserving the same top-level structure.

## Evaluation & Observability

Evaluation is local-first and split into two complementary parts:

The PoC includes several evaluation-oriented and observable-system patterns:

- structured extraction scoring
- latency measurement
- Bedrock invocation logging
- CloudWatch log integration
- evaluation dataset generation
- repeatable local benchmarking

- deterministic structured extraction checks for `claim_id`, claimant, policy, date, amount, and incident details
- managed Amazon Bedrock summary-quality evaluation for generated summaries

Run the local fallback evaluation:

```bash
python3 scripts/evaluate_claims.py --models local-fallback
```

Compare up to two Bedrock models:

```bash
python3 scripts/evaluate_claims.py \
  --models <model-id-1> <model-id-2> \
  --bedrock-region <aws-region>
```

Start managed Bedrock Evaluation jobs after deployment:

```bash
python3 scripts/evaluate_claims.py \
  --models <model-id-1> <model-id-2> \
  --bedrock-region <aws-region> \
  --bedrock-eval-s3-input-uri s3://<bucket>/evaluation/bedrock/input/ \
  --bedrock-eval-s3-output-uri s3://<bucket>/evaluation/bedrock/output/ \
  --bedrock-eval-role-arn <bedrock-evaluation-role-arn> \
  --bedrock-eval-evaluator-model <judge-model-id> \
  --start-bedrock-eval-job
```

Evaluation artifacts are written to:

- `data/evaluation/results/` for local extraction accuracy and latency results
- `data/evaluation/bedrock-evaluation/` for Bedrock Evaluation datasets, references, and job metadata

### Results Placeholder

Populate this table after running evaluation:

| Model            | Structured Field Accuracy | Summary Quality (Bedrock) | Avg Processing Time (ms) | Notes                      |
| ---------------- | ------------------------: | ------------------------: | -----------------------: | -------------------------- |
| `local-fallback` |                      TODO |                       N/A |                     TODO | Baseline offline extractor |
| `<model-id-1>`   |                      TODO |                      TODO |                     TODO | Populate after Bedrock run |
| `<model-id-2>`   |                      TODO |                      TODO |                     TODO | Optional second model      |

See [EVALUATION.md](EVALUATION.md) for methodology, metrics, limitations, and the combined findings format.

## Architecture Decisions & Tradeoffs

- **Event-driven processing:** S3 and Lambda keep the demo small while matching a realistic document-ingestion pattern.
- **Stable output schema:** every run produces the same top-level fields so local runs, Lambda runs, and evaluation runs stay comparable.
- **Local fallback:** offline extraction keeps development fast even without active Bedrock credentials.
- **Split evaluation:** deterministic checks measure structured field extraction, while Bedrock Evaluation measures generated summary quality.
- **Single S3 bucket:** `claims/`, `processed/`, and evaluation prefixes keep the infrastructure minimal for the PoC.

## Security & Production Considerations

Even though this repository is intentionally scoped as a PoC, the implementation includes several production-oriented foundations:

- IAM-scoped Lambda permissions
- Bedrock invocation logging
- schema validation before persistence
- infrastructure-as-code deployment
- deterministic processing flow
- isolated S3 prefixes for claims and processed outputs

Additional hardening for a production implementation would include:

- PII detection and redaction
- KMS encryption
- audit workflows
- retry/replay pipelines
- human-review processes
- stronger monitoring and alerting
- cost governance and model controls

## AWS Prerequisites

- AWS credentials configured locally
- AWS CDK CLI installed
- target AWS account bootstrapped for CDK
- Amazon Bedrock model access enabled in the target Region
- permissions to create S3, Lambda, IAM, CloudWatch Logs, and Bedrock logging/evaluation resources

The CDK stack defaults to `anthropic.claude-3-haiku-20240307-v1:0` unless `bedrockModelId` is provided as CDK context.

## Local Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r infra/cdk/requirements.txt
```

## Run Locally

Run the handler with local input and output folders:

```bash
python -m src.handlers.claims_processor
```

Run with the checked-in S3 event payload:

```bash
python -m src.handlers.claims_processor --event data/events/s3-put-claim-001.json
```

To call Amazon Bedrock locally instead of using the regex fallback, set `BEDROCK_MODEL_ID` and make sure AWS credentials are available.

## Deploy To AWS

Run CDK commands from `infra/cdk/`.

Bootstrap the target account:

```bash
cd infra/cdk
cdk bootstrap
```

Synthesize the stack:

```bash
cdk synth
```

Review changes:

```bash
cdk diff
```

Deploy:

```bash
cdk deploy
```

Deploy with a specific Bedrock model:

```bash
cdk deploy -c bedrockModelId=<model-id>
```

If you plan to create Bedrock Evaluation jobs from the AWS console, deploy with the optional CORS flag:

```bash
cdk deploy -c enableBedrockEvaluationConsoleCors=true
```

## Run The Demo

Upload the sample PDF to the deployed claims bucket:

```bash
python scripts/upload_claim.py --bucket <claims-bucket-name>
```

Optional arguments:

- `--file` uploads a different PDF
- `--key` changes the S3 object key
- `--region` overrides the S3 client Region

Processed JSON results are written back to the same bucket under the `processed/` prefix.
The CDK stack outputs the generated bucket name and Bedrock Evaluation S3 locations after deployment.

## Project Structure

- `infra/cdk/`: CDK app and stack definitions
- `scripts/`: local upload and evaluation helpers
- `src/handlers/`: Lambda handler entrypoints
- `src/lib/`: shared parsing, extraction, validation, and S3-event helpers
- `prompts/`: prompt assets
- `data/events/`: sample event payloads for local handler runs
- `data/input/`: sample input documents for the main demo
- `data/output/`: local processed outputs
- `data/evaluation/input/`: synthetic evaluation PDFs
- `data/evaluation/expected/`: expected-answer files for deterministic scoring
- `data/evaluation/results/`: local evaluation run outputs
- `data/evaluation/bedrock-evaluation/`: Bedrock Evaluation datasets and job references

## Documentation

- [docs/README.md](docs/README.md) explains how Codex uses the plan, spec, task queue, and execution log to support agent-assisted development.
- [EVALUATION.md](EVALUATION.md) expands on the evaluation methodology, metrics, limitations, and reporting format.

## Production Readiness Notes

This PoC includes some production-aligned foundations:

- infrastructure is defined with AWS CDK
- claim documents and processed outputs use separate S3 prefixes
- Bedrock invocation logging is configured for S3 and CloudWatch Logs
- Lambda uses IAM permissions for S3 access and Bedrock model invocation
- extraction output is normalized through a stable schema
- evaluation artifacts are stored separately from normal processed outputs

The following would be added or hardened for a production version:

- CloudWatch metrics, dashboards, alarms, and alert routing for Lambda failures, latency, throttling, and Bedrock errors
- retry strategy, dead-letter queue, and replay process for failed document processing
- stronger S3 security controls, including KMS encryption, lifecycle policies, access logging, and stricter bucket policies
- PII redaction, guardrails, audit requirements, and human-review workflows for sensitive claims
- document classification/OCR strategy for multiple layouts, scanned PDFs, and low-quality files
- CI/CD, environment separation, automated tests, and deployment approvals
- cost controls, model governance, prompt/version tracking, and production evaluation thresholds

Current limitations:

- supports one simple synthetic claim document type for the core demo
- local fallback extraction is a development convenience, not a model-quality benchmark
- evaluation latency is directional and should not be treated as production performance data
- policy enrichment and UI are intentionally deferred until the core slice is stable

This project intentionally focuses on a small but realistic vertical slice instead of a fully production-ready insurance platform.

The goal is to demonstrate practical GenAI engineering patterns, architecture decisions, evaluation workflows, and AWS integration approaches.

## Key Learnings

This project highlighted several practical challenges common in real-world GenAI systems:

- maintaining stable structured outputs
- balancing latency and model quality
- designing observable AI workflows
- separating deterministic logic from model behavior
- preparing evaluation-ready datasets and pipelines
- building reproducible local development workflows

## Disclaimer

This repository is a Proof of Concept created for learning, experimentation, architecture exploration, and portfolio demonstration purposes.
