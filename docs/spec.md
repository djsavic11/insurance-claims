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

- If a field cannot be extracted, set it to `null`
- The system must always produce output and must not fail silently

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
