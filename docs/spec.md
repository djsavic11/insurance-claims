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

## Output

The system must produce a JSON object with this stable structure:

```json
{
  "claim_id": "string",
  "amount": 123.45,
  "summary": "string"
}
```

- `claim_id`: string
- `amount`: number or `null`
- `summary`: string
- The JSON output must be saved to Amazon S3

## Behavior Rules

- The system must react to a document uploaded to Amazon S3
- If a field cannot be extracted, set it to `null`
- The system must always produce output and must not fail silently

## Validation Rules

- `claim_id` must be a non-empty string
- If the extracted `claim_id` is empty, fall back to the uploaded document filename stem
- `amount` must be a number greater than or equal to `0`, or `null`
- `summary` must be a non-empty string
- The output must not contain additional top-level fields outside `claim_id`, `amount`, and `summary`

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
