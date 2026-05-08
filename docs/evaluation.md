# Evaluation

## Purpose

Document how local structured extraction evaluation and managed Amazon Bedrock summary evaluation are run and combined for final findings.

## Scope

- Evaluate at most 2 generator models per run
- Use local deterministic checks for structured extraction accuracy
- Use Amazon Bedrock Evaluation for generated summary quality
- Keep processing latency directional and local-first

## Inputs

- Input documents: `data/evaluation/input/*.pdf`
- Expected answers: `data/evaluation/expected/*.json`

Each expected-answer file uses the matching filename stem and includes:

- `claim_id`
- `claimant_name`
- `policy_number`
- `incident_date`
- `claim_amount`
- `incident_description`

## Local Runner

Use:

```bash
python3 scripts/evaluate_claims.py --models local-fallback
```

Or compare two Bedrock models:

```bash
python3 scripts/evaluate_claims.py \
  --models <model-id-1> <model-id-2> \
  --bedrock-region <aws-region>
```

The runner writes:

- Local results: `data/evaluation/results/`
- Bedrock evaluation artifacts and references: `data/evaluation/bedrock-evaluation/`

## Structured Extraction Metrics

Deterministic checks:

- `claim_id`
- normalized `claimant_name`
- `policy_number`
- normalized `incident_date` (`YYYY-MM-DD`)
- numeric `claim_amount` with tolerance
- `incident_description` when expected value exists

Output includes:

- field-level results
- `structured_field_accuracy`
- schema validation result
- processing timing (`parse`, `extract`, `validate`, `total_processing`)

## Bedrock Summary Quality

The local runner exports a JSONL prompt dataset from local records and can optionally start managed Bedrock evaluation jobs.
When comparing two models, the local runner creates one Bedrock Evaluation job per model because model-as-judge BYOI jobs accept one unique `modelIdentifier` per dataset.

Example:

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

## Combined Findings

Final findings must combine:

- local deterministic extraction results
- managed Bedrock summary-quality results

These are complementary signals and should not be treated as competing evaluators.

Use this structure for final reporting:

| Model | Structured Field Accuracy | Summary Quality (Bedrock) | Avg Processing Time (ms) | Notes |
|---|---:|---:|---:|---|
| model-1 | 0.00 | pending | 0.00 | fill after run |
| model-2 | 0.00 | pending | 0.00 | fill after run |

## Code Organization And Reusability Notes

Capture implementation notes in each run review:

- shared extraction/validation path reused by handler and evaluation runner
- deterministic checks isolated in evaluation scoring helpers
- Bedrock job request and response references persisted for traceability
- local artifacts separated from S3 output prefixes

## Limitations

- Local latency values are directional, not production benchmarks
- Bedrock evaluation job requirements depend on AWS account model access and IAM permissions
- Prompt dataset format for managed jobs may evolve with AWS API changes
