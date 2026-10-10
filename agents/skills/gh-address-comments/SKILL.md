---
name: gh-address-comments
description: Address review or issue comments on the open GitHub PR for the current branch.
metadata:
  short-description: Address comments in a GitHub PR review
---

# PR Comment Handler

Guide to find the open PR for the current branch and address its comments with `oai_gh` when available, otherwise `gh`.

Prereq: ensure the GitHub CLI is installed and authenticated. Prefer `oai_gh auth status` when `oai_gh` exists on `PATH`, otherwise run `gh auth status`. If neither CLI is available or auth is missing, ask the user to install/authenticate before continuing.

## 1) Inspect comments needing attention
- Run scripts/fetch_comments.py which will print out all the comments and review threads on the PR

## 2) Resolve the requested scope
- Summarize actionable comments. Use a subset if the user named one; otherwise a request to address the PR comments covers all actionable comments.
- Ask only about conflicting requirements or a product decision that cannot be resolved from the PR and source.

## 3) Apply and verify
- Apply the scoped fixes and run relevant checks. Report each comment as addressed, not applicable with evidence, or blocked with a reason.
- Send replies or resolve remote discussions only when the user authorizes those actions.

Notes:
- If GitHub auth/rate issues appear mid-run, prompt the user to re-authenticate with `oai_gh auth login` or `gh auth login`, then retry.
