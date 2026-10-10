---
name: "gh-fix-ci"
description: Diagnose or fix failing GitHub Actions checks on the current pull request.
---


# GH Fix CI

## Overview

Use `oai_gh` when available, otherwise `gh`, to locate failing PR checks, fetch GitHub Actions logs for actionable failures, summarize the failure snippet, then implement a scoped fix when requested.
- For diagnosis or plan-only requests, report the cause and proposed fix. For a fix request, proceed with reversible changes under existing authorization.

Prereq: authenticate with the GitHub CLI once, then confirm auth with `oai_gh auth status` when available or `gh auth status` otherwise (repo + workflow scopes are typically required).

## Inputs

- `repo`: path inside the repo (default `.`)
- `pr`: PR number or URL (optional; defaults to current branch PR)
- `oai_gh` or `gh` authentication for the repo host

## Quick start

- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"`
- Add `--json` if you want machine-friendly output for summarization.

## Workflow

1. Verify gh authentication.
   - Prefer `oai_gh auth status` in the repo when `oai_gh` exists; otherwise run `gh auth status`.
   - If unauthenticated or neither CLI exists, ask the user to install/authenticate (`oai_gh auth login` or `gh auth login`) before proceeding.
2. Resolve the PR.
   - Prefer the current branch PR: `gh pr view --json number,url`.
   - If the user provides a PR number or URL, use that directly.
3. Inspect failing checks (GitHub Actions only).
   - Preferred: run the bundled script (handles gh field drift and job-log fallbacks):
     - `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"`
     - Add `--json` for machine-friendly output.
   - Manual fallback:
     - `gh pr checks <pr> --json name,state,bucket,link,startedAt,completedAt,workflow`
       - If a field is rejected, rerun with the available fields reported by `gh`.
     - For each failing check, extract the run id from `detailsUrl` and run:
       - `gh run view <run_id> --json name,workflowName,conclusion,status,url,event,headBranch,headSha`
       - `gh run view <run_id> --log`
     - If the run log says it is still in progress, fetch job logs directly:
       - `gh api "/repos/<owner>/<repo>/actions/jobs/<job_id>/logs" > "<path>"`
4. Scope non-GitHub Actions checks.
   - If `detailsUrl` is not a GitHub Actions run, label it as external and only report the URL.
   - Do not attempt Buildkite or other providers; keep the workflow lean.
5. Summarize failures for the user.
   - Provide the failing check name, run URL (if any), and a concise log snippet.
   - Call out missing logs explicitly.
6. Choose the smallest fix supported by the logs and source.
   - Ask only when a product or architecture choice cannot be resolved from the request.
7. Implement the requested fix.
   - Preserve unrelated work. Publish or open a PR when the request authorizes it.
8. Verify the changed behavior with relevant checks.
   - Report checks run and any limits. Local success does not establish CI success; report CI separately when it has run on the changed commit.

## Bundled Resources

### scripts/inspect_pr_checks.py

Fetch failing PR checks, pull GitHub Actions logs, and extract a failure snippet. Exits non-zero when failures remain so it can be used in automation.

Usage examples:
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "123"`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "https://github.com/org/repo/pull/123" --json`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --max-lines 200 --context 40`
