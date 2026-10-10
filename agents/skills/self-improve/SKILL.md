---
name: self-improve
description: Improve Codex behavior or project instructions from evidence in prior sessions and feedback.
---

# Self Improve

## Overview

Use this Codex-specific skill to inspect prior Codex threads and generate evidence-backed improvement proposals for three targets: skills, project-local `AGENTS.md`, and global `~/.codex/AGENTS.md`.

This skill depends on Codex's local session system (`~/.codex/state_5.sqlite` plus rollout JSONL files under `~/.codex/sessions` and `~/.codex/archived_sessions`). It is not intended to work unchanged in non-Codex agent runtimes.

## Workflow

1. Run the session browser to identify candidate threads:

   ```bash
   python3 scripts/self_improve.py list --limit 25 --archived all
   ```

2. Render specific sessions as readable transcripts when you need direct evidence:

   ```bash
   python3 scripts/self_improve.py show <thread-id>
   ```

3. Run a dream pass to mine repeated user corrections and workflow preferences:

   ```bash
   python3 scripts/self_improve.py dream --limit 250 --days 365 --min-support 2 --min-confidence 0.6 --emit-patch
   ```

4. Run a skill audit when you want per-skill `SKILL.md` improvements instead of global/project instruction updates:

   ```bash
   python3 scripts/self_improve.py skill-audit --limit 500 --days 365 --min-support 1 --min-confidence 0.6 --emit-patch
   ```

   The script includes personal skill roots and the nearest `.agents/skills` root above the current directory. Add other project libraries with repeatable `--skill-root <path>` options.

5. Read the proposal buckets and decide what to patch:
   - `Skills`: tighten existing `SKILL.md`, add scripts/references, or create a new skill.
   - `Project AGENTS.md`: update the nearest repo/vault instruction file for a project-specific preference.
   - `Global AGENTS.md`: add durable defaults that should apply across all repos.

6. When the user asks about frustration or persistence, inspect cited examples with `show` and specifically look for repeated `continue`, `keep going`, `don't stop`, `Come on`, and “can't you just...” messages before proposing global behavior rules.

## Source Of Truth

- Treat `~/.codex/state_5.sqlite` as the authoritative session index.
- Use each row's `threads.rollout_path` to load full rollout JSONL transcripts from `~/.codex/sessions/...` or `~/.codex/archived_sessions/...`.
- Read direct user text from both legacy `event_msg.user_message` records and current `response_item.message` records. For current records, accept `user.text` and exclude injected skill, plugin, environment, and instruction items.
- When ambient browser state, response annotations, referenced conversations, app context, or file context wraps a `## My request:` section, mine only that request. Do not treat wrapper instructions or quoted context as user preferences.
- Treat `~/.codex/session_index.jsonl` as an incomplete convenience index, not the source of truth.
- Use `~/.codex/memories/MEMORY.md` and `~/.codex/memories/memory_summary.md` as supporting context only. Do not write them by default.

## Proposal Rules

- Default to propose-first. Do not patch `SKILL.md`, project `AGENTS.md`, or global `~/.codex/AGENTS.md` until the user explicitly approves the proposed edits.
- Separate facts from inference. Every proposal must cite one or more concrete thread IDs plus timestamps and rollout paths.
- Do not overfit one-off phrasing. Prefer repeated corrections, repeated style/tooling requests, and instructions that are likely to recur.
- Treat `Support` as deduped thread clusters, not raw thread IDs, so same-day retries of one task do not inflate one proposal.
- Use `Confidence` to suppress one-off task noise. If a proposal still reads like a transient implementation ask, inspect its cited sessions with `show` before patching.
- Keep proposal buckets disjoint. If a preference belongs in a project `AGENTS.md`, do not also copy the same rule into global `~/.codex/AGENTS.md` unless it clearly applies across repos.
- For project proposals, infer the nearest target `AGENTS.md` from the session `cwd`. Resolve deleted worktrees to a current repository with the same repository name when possible. Never propose a new instruction file inside a stale or deleted task directory.
- For skill proposals, map edits to an existing skill folder under the configured skill roots when the transcript or cwd makes that unambiguous; otherwise propose a new skill path under `~/.codex/skills/<name>/SKILL.md`.
- Use `skill-audit` when the question is “which existing skills should be improved?” because it suppresses suggestions already present in each target `SKILL.md` and emits only uncovered rules per skill.

### scripts/

- `scripts/self_improve.py` provides `list`, `show`, `dream`, and `skill-audit` subcommands.
