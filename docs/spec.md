# Spec

## Purpose

Define the minimum functional scope for the Insurance Claims Processing PoC.

## Goal

Build a proof of concept for an AI-powered insurance claims processing pipeline on AWS.

## Core Slice

1. Upload one claim document to Amazon S3
2. Trigger an AWS Lambda handler
3. Invoke Amazon Bedrock from Lambda
4. Extract structured claim data from the document
5. Save the result back to Amazon S3

## Extensions Later

- PII checks and guardrails
- Policy enrichment from Amazon Knowledge Bases
- Model comparison
- Simple UI for demo display

## Input

- One simple document type only
- Example target format: single-page PDF

## Output

- One stable structured output format
- Saved to Amazon S3
- Able to support downstream validation and demo display

## Constraints

- Keep the PoC intentionally small
- Prefer end-to-end clarity over completeness
- Avoid production-level architecture
- Do not broaden document support early

## Done Criteria For Phase 1

- A document upload triggers processing automatically
- Lambda calls Bedrock successfully
- Structured output is produced
- Output is saved to Amazon S3

