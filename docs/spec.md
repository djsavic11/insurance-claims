# Spec

## Purpose

Define the minimum functional scope for the Insurance Claims Processing PoC.

## Goal

Build a proof of concept for an AI-powered insurance claims processing pipeline on AWS.

## Scope Reference

This specification describes the required system behavior for the core slice defined in [plan.md](plan.md).

## Input

- One simple document type only
- Example target format: single-page PDF
- The document must enter the system through an upload to Amazon S3
- For the PoC, uploaded claim documents should be stored under the `claims/` prefix

## Output

The system must produce a JSON object with this stable structure:

```json
{
  "claim_id": "string",
  "claimant_name": "string or null",
  "policy_number": "string or null",
  "incident_date": "YYYY-MM-DD or null",
  "claim_amount": 123.45,
  "incident_description": "string or null",
  "summary": "string"
}
```

- `claim_id`: string
- `claimant_name`: string or `null`
- `policy_number`: string or `null`
- `incident_date`: ISO 8601 date string in `YYYY-MM-DD` format, or `null`
- `claim_amount`: number or `null`
- `incident_description`: string or `null`
- `summary`: string
- The JSON output must be saved to Amazon S3 under the `processed/` prefix

## Behavior Rules

- The system must react to a document uploaded to Amazon S3
- The processing trigger must apply to documents uploaded under the `claims/` prefix only
- If a field cannot be extracted, set it to `null`
- The system must always produce output and must not fail silently
- The summary must be generated from the document content and extracted claim details
- The output structure must remain stable across local runs, Lambda runs, and evaluation runs
- Prompt templates must be kept separate from processing code and must preserve the stable output structure

## Validation Rules

- `claim_id` must be a non-empty string
- If the extracted `claim_id` is empty, fall back to the uploaded document filename stem
- `claimant_name` must be a non-empty string or `null`
- `policy_number` must be a non-empty string or `null`
- `incident_date` must be a valid `YYYY-MM-DD` date string or `null`
- `claim_amount` must be a number greater than or equal to `0`, or `null`
- `incident_description` must be a non-empty string or `null`
- `summary` must be a non-empty string
- The output must not contain additional top-level fields outside `claim_id`, `claimant_name`, `policy_number`, `incident_date`, `claim_amount`, `incident_description`, and `summary`

## Evaluation

The PoC must support a local-first evaluation flow for demo and learning purposes.

### Evaluation Inputs

- Evaluation should run against at least 3 testable claim PDF samples stored under `data/evaluation/input/`
- The samples should use different claim form layouts, but remain within the PDF claim-document scope
- Each sample PDF should contain claimant name, policy number, incident date, claim amount, and incident description
- Each sample should use realistic but synthetic claim data only
- Each evaluation sample should have an expected-answer file under `data/evaluation/expected/` for deterministic structured field checks
- Expected-answer files should include ground truth for `claim_id`, `claimant_name`, `policy_number`, `incident_date`, `claim_amount`, and `incident_description` when those values are present in the source document
- Expected-answer filenames should match the input document stem, for example `claim-001.pdf` and `claim-001.json`

### Evaluation Outputs

Evaluation results should be saved separately from normal processed claim outputs under `data/evaluation/results/`.
Amazon Bedrock Evaluation input and output references should be tracked under `data/evaluation/bedrock-evaluation/`.

Each evaluation result should include:

- document name
- model identifier
- schema validation result
- field-level extraction comparison results
- overall structured field accuracy
- generated summary
- summary quality result or reference to the Amazon Bedrock Evaluation result
- processing time measurements
- code organization and reusability notes for the evaluation implementation

The final evaluation report should combine deterministic structured extraction results from the local runner with managed Amazon Bedrock Evaluation summary-quality results.
These two result types should not be treated as competing evaluators because they measure different parts of the workflow.

### Evaluation Rules

- Compare 2 generator models max for demo purposes
- Use deterministic checks for structured extraction accuracy
- Match `claim_id`, `policy_number`, and normalized `claimant_name` as strings
- Match `incident_date` after normalizing to `YYYY-MM-DD`
- Match `claim_amount` numerically with a small tolerance for formatting differences
- Evaluate `incident_description` as part of structured field accuracy only when an expected value is provided
- Use Amazon Bedrock Evaluation for generated summary quality
- Do not add a custom LLM-as-judge summary evaluator unless Amazon Bedrock Evaluation is explicitly blocked
- Generate Bedrock Evaluation JSONL input from local evaluation records
- Reference Bedrock Evaluation job/report results from the local evaluation artifacts
- Keep local processor latency separate from Bedrock Evaluation overhead
- Treat latency results as directional demo metrics, not production benchmarks
- Treat code organization and reusability as documented engineering findings, not automated scores
- Do not require deployed Lambda or S3 event processing for evaluation runs

## Constraints

- Keep the PoC intentionally small
- Prefer end-to-end clarity over completeness
- Avoid production-level architecture
- Do not broaden document support early
- Keep the output structure stable once defined, even if extraction improves

## Done Criteria For Phase 1

- A document upload triggers processing automatically
- Lambda calls Bedrock successfully
- Structured output is produced
- Output is saved to Amazon S3
