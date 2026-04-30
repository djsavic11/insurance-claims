# Insurance Claims Processing (PoC)

## Overview

This repository contains a Proof-of-Concept (PoC) for an AI-powered insurance claims processing pipeline built on AWS.
This project uses agent-driven development to keep implementation iterative, focused, and easy to parallelize.

The system processes unstructured claim documents and transforms them into structured, actionable outputs by combining:

- LLM-based information extraction
- Automated claim summarization
- Optional enrichment using policy knowledge (RAG)

The architecture emphasizes:

- Clear separation between data storage, processing logic, and AI inference
- Reusable components (prompt management, model invocation, validation)
- Lightweight model evaluation (latency, output quality, consistency)

This PoC demonstrates how foundation models can be integrated into enterprise workflows for intelligent document processing (IDP) to reduce manual effort and improve consistency.

---

## Demo Flow

The smallest end-to-end flow demonstrated by this PoC:

1. Upload a claim document to Amazon S3
2. Trigger an AWS Lambda function
3. Process the document using Amazon Bedrock
4. Extract structured claim data
5. Generate a concise claim summary
6. Save results back to Amazon S3

Additional capabilities (policy enrichment, validation, evaluation, UI) are added incrementally.

---

## PoC Constraints

- Focus on a single document type (for consistency)
- Minimal infrastructure and configuration
- No production-level hardening
- Prioritize clarity and end-to-end flow over completeness

---

## Capabilities (Incremental)

As the PoC evolves, it may include:

- Retrieval-Augmented Generation (RAG) using policy knowledge
- Basic PII handling and guardrails
- Simple validation of extracted data
- Lightweight model comparison (latency, quality, cost)
- Minimal UI for demo visualization

---

## Architecture Approach

The system is designed around a simple, modular pipeline:

- **Ingestion layer** → document upload and storage (S3)
- **Processing layer** → event-driven compute (Lambda)
- **AI layer** → model inference via Amazon Bedrock
- **Output layer** → structured results and summaries

Each layer is loosely coupled to allow iterative improvements without large refactoring.

![Architecture](architecture.png)

---

## Documentation

This repository keeps documentation intentionally small so humans and agents can move quickly.

- [AGENTS.md](AGENTS.md): agent working rules and doc map
- [docs/plan.md](docs/plan.md): execution plan, phases, and workstreams
- [docs/spec.md](docs/spec.md): PoC scope, inputs, outputs, and done criteria
- [docs/tasks.md](docs/tasks.md): active task list (current iteration only)
- [docs/log.md](docs/log.md): task execution log (decisions, outcomes, blockers)
