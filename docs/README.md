# Agentic Workflow Guide

This folder contains the working documentation Codex uses to plan, execute, and record small, reviewable project changes.

The root [README.md](../README.md) explains the project for readers and reviewers.
This guide explains the agentic workflow: how Codex uses the plan, spec, task queue, and log to decide what to do next, keep scope stable, and record what changed.

This approach can be described as a **spec-driven agentic development workflow**.
It combines repository-level agent instructions, docs-as-code, spec-driven development, and context engineering:

- **Repository-level agent instructions:** [AGENTS.md](../AGENTS.md) gives Codex project-specific working rules, similar to the open [AGENTS.md](https://agents.md/) convention and repository custom instruction patterns used by AI coding tools.
- **Spec-driven development:** [spec.md](spec.md) defines the behavior and stable contracts before or alongside code changes.
- **Docs-as-code:** planning, specs, tasks, and logs live in Git with the implementation, so documentation changes can be reviewed like code.
- **Context engineering:** the workflow gives Codex the right project context on each run instead of relying only on chat history.

In short:

1. [AGENTS.md](../AGENTS.md) defines how Codex should work in this repository.
2. [plan.md](plan.md) explains the current build approach and phase order.
3. [spec.md](spec.md) defines required system behavior and stable contracts.
4. [tasks.md](tasks.md) shows what work is active, next, deferred, blocked, or done.
5. [log.md](log.md) records what happened during real task execution.

Codex should rely on these files instead of chat history alone.
This is not a separate framework or tool requirement; it is a lightweight repository convention for keeping human decisions, agent work, implementation state, and project scope aligned.

## Workflow

For normal implementation work, Codex follows this sequence:

1. Use [AGENTS.md](../AGENTS.md) as the repository-level instruction file loaded by Codex and compatible agents.
2. Read [plan.md](plan.md) to understand the current implementation phase.
3. Read [spec.md](spec.md) to understand required behavior, inputs, outputs, validation rules, and constraints.
4. Check [tasks.md](tasks.md) for the current task state.
5. Make one focused code or documentation change.
6. Update [tasks.md](tasks.md) if task state changes.
7. Update [log.md](log.md) when a real task is executed, completed, or blocked.

If the requested change alters behavior, inputs, outputs, validation, constraints, implementation sequencing, AWS services, or model choices, Codex should update the relevant source-of-truth docs before or alongside code changes.

## File Ownership

| File | Purpose | Updated By | Update When |
| --- | --- | --- | --- |
| [AGENTS.md](../AGENTS.md) | Agent working rules and coordination model | Human/developer, sometimes Codex with approval | Repository workflow rules change |
| [plan.md](plan.md) | Build phases, execution order, tooling, and implementation approach | Human/developer or Codex | Phase, sequencing, tooling, or approach changes |
| [spec.md](spec.md) | Required behavior, inputs, outputs, validation rules, and constraints | Human/developer or Codex | System behavior or contracts change |
| [tasks.md](tasks.md) | Live work queue | Codex during execution; human/developer for priorities | Work moves between `Now`, `Next`, `Later`, `Blocked`, and `Done` |
| [log.md](log.md) | Execution history for real task runs | Codex | A task starts, completes, or is blocked |

Humans and developers own product direction.
They should update the docs directly, or ask Codex to update them, when decisions affect scope, AWS service choices, model choices, evaluation expectations, demo priorities, or what the PoC is meant to prove.

## Developer Prompts

Use prompts to state the developer intent.
Repository rules and update behavior are defined in [AGENTS.md](../AGENTS.md) and the workflow docs, so they do not need to be repeated in every prompt.

Start the next task:

```text
Pick the next appropriate task from docs/tasks.md and implement it.
```

Review the queue without changing files:

```text
Review docs/tasks.md against docs/plan.md and docs/spec.md.
Tell me what should be worked on next.
Do not change files yet.
```

Implement the current task:

```text
Implement the current task in docs/tasks.md.
```

Change behavior or output shape:

```text
We need to change the expected output schema.
Review docs/spec.md and docs/plan.md first, explain the impact, then update the relevant docs and tasks before changing code.
```

Review implementation against the docs:

```text
Review the implementation against docs/spec.md and docs/plan.md.
Report gaps, risks, and suggested next tasks.
Do not change files yet.
```

## Example Flows

### Adding A Validation Rule

1. A developer asks Codex to implement the next task from [tasks.md](tasks.md).
2. Codex checks [spec.md](spec.md) for the expected output structure and validation rules.
3. Codex updates the validation code.
4. Codex runs a focused local check when possible.
5. Codex moves the task to `Done` or marks it `Blocked` in [tasks.md](tasks.md).
6. Codex adds a short execution entry to [log.md](log.md).

### Changing Scope

1. A developer decides the PoC should support a new output field.
2. The developer asks Codex to review the impact before coding.
3. Codex updates [spec.md](spec.md) because the output contract changed.
4. Codex updates [plan.md](plan.md) if the implementation sequence or phase scope changes.
5. Codex adds or adjusts tasks in [tasks.md](tasks.md).
6. Codex implements code only after the intended behavior is documented.

## Related Concepts

- [AGENTS.md](https://agents.md/): a shared convention for giving AI coding agents repository-specific instructions.
- [GitHub Copilot repository custom instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions): repository-level guidance that helps AI coding tools understand how to build, test, and validate changes.
- [Docs-as-code](https://www.doctave.com/docs-as-code): managing documentation through the same source-control and review workflow as code.
- [Context engineering](https://www.ibm.com/think/topics/context-engineering): deliberately structuring the information an AI model or agent receives so its work is more relevant and reliable.
- [Spec-based development for AI coding agents](https://specthis.ai/): using a written specification as the source of truth before an agent writes code.
