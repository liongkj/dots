---
name: audit-ai-frontend
description: Audit AI-shaped frontend code or design diffs for design-system, responsiveness, and accessibility issues.
---

# Frontend Audit

Review the requested UI or diff against its product behavior and existing design system. Inspect components, tokens, copy, and state ownership; use a running browser when available. Separate observed defects from screenshot or code-only inferences.

Prioritize broken interaction, keyboard access, labels, contrast, touch targets, overflow, and loading/empty/error states. Then inspect fixture-shaped data, duplicate markup, brittle component interfaces, and token drift. Judge visual choices in product context rather than treating a common font, palette, or card as a defect.

Preserve the product's content, information structure, and established primitives unless a redesign is requested. Componentize when it supports real reuse or states.

For reviews, report actionable findings with severity, location, evidence, user impact, and a focused fix. For authorized fixes, implement and recheck the affected states and viewports. State what browser behavior remains unverified.

Read only the reference needed:

- [patterns.md](references/patterns.md): repair patterns and code smells; visual cues are heuristics.
- [rubric.md](references/rubric.md): broader UX and accessibility review.
- [workflows.md](references/workflows.md): browser QA or reference-driven design.
- [sources.md](references/sources.md): research basis.
