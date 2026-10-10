---
name: gh-commit
description: Organize local Git changes into clear, semantic commits when the user asks to commit.
---

# GH Commit

## Goal

Turn the current working tree into a small set of clean commits without mixing unrelated changes.

## Workflow

1. Verify git context.
- Run `git rev-parse --show-toplevel` and `git status -sb`.
- Read the branch with `git branch --show-current`.
- If on the default branch, create a task branch under the repository worktree rules unless the user explicitly asked to commit on that branch. Preserve the requested changes and unrelated state.

2. Inspect all changes before staging anything.
- Run `git diff --stat` and `git diff --cached --stat`.
- List untracked files with `git ls-files --others --exclude-standard`.
- Read actual hunks with `git diff` and `git diff --cached`.
- Include untracked files in the review (read them if needed) so commit grouping decisions cover the full diff.

3. Propose semantic commit groups.
- Group by intent, not just file type (for example: bug fix, refactor, tests, docs).
- Keep user-authored unrelated work separate.
- Call out any files that need partial staging because they contain mixed concerns.

4. Create each commit group.
- Stage only the files or hunks for that group (`git add <paths>` or `git add -p`).
- Verify exactly what is staged with `git diff --cached --stat` and `git diff --cached`.
- Commit with a concise imperative message.
- Prefer `type(scope): summary` when the change has an obvious type/scope; otherwise use a clear plain-English summary.

5. Repeat until done.
- After each commit, re-check `git status -sb`.
- Continue until all intended changes are committed or intentionally left uncommitted.

6. Report the result.
- List the commit SHAs and messages in order.
- Note any remaining staged/unstaged/untracked files.

## Safety Rules

- Stage explicit paths or hunks. Never use `git add .` or `git add -A`.
- Use partial staging when a file mixes multiple concerns.
- Do not rewrite or discard user changes unless explicitly asked.
- If grouping is ambiguous, ask before committing.
