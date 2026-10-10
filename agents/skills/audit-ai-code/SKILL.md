---
name: audit-ai-code
description: Audit or clean up AI-shaped backend or general code for real defects and maintainability issues.
---

# Code Audit

Review the requested diff or files for concrete correctness, safety, and maintainability problems. Read adjacent code to establish local conventions. AI-like style is a clue to inspect, not evidence of authorship or a defect by itself.

Focus on:

- Duplicate helpers, shadow APIs, invented imports, and abstractions without real callers.
- Fixture-specific branches, weakened tests, swallowed failures, and fallbacks that hide invalid state.
- Unclear ownership, broad parameter bags, and control flow that obscures behavior.
- Security and runtime failures supported by the affected code path.

Prefer existing utilities and narrow interfaces. Extract shared behavior only when it removes meaningful duplication; preserve intended behavior and public contracts unless the task calls for a change.

For a review, report only actionable findings with severity, file/line, trigger, impact, and the smallest fix. Group repeated symptoms and state uncertainty. An empty finding list is valid.

For authorized cleanup, apply focused changes, run relevant checks, and inspect the final diff for behavior changes. Summarize the result and verification limits.

Consult [sources.md](references/sources.md) when the rationale for a review criterion needs support.
