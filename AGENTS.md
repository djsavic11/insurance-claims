# AGENTS.md

## Purpose

This file gives agents the minimum context needed to work safely in this repository.
Keep it short and keep it current.

## Project

- Project: Insurance Claims Processing PoC on AWS
- Goal: build a small demo of document upload, processing with Bedrock, structured extraction, and saving results
- Priority: deliver the smallest working end-to-end slice first

## Source Of Truth

- Start with [docs/plan.md](docs/plan.md)
- Use [README.md](README.md) for high-level project context
- Use [docs/spec.md](docs/spec.md) for the current PoC scope
- Use [docs/tasks.md](docs/tasks.md) for active work
- Use [docs/log.md](docs/log.md) only for active task execution updates
- Use this file for agent working rules and lightweight coordination

## Working Rules

- Keep the solution simple
- Work on one small task at a time
- Do not expand scope beyond the current phase
- Prefer the core slice over optional features
- Keep output structures stable once defined
- Update docs if scope, assumptions, or state changes

## Task Handling

- Pick a task from [docs/tasks.md](docs/tasks.md)
- Make focused changes
- Record progress in [docs/log.md](docs/log.md) only for real task execution
- If blocked, write the blocker clearly before moving on

## When To Ask For Guidance

Ask for guidance only if:

- a decision changes scope
- there are multiple valid directions with different tradeoffs
- a required AWS or model choice is unclear
- the current task is blocked by a missing product decision
