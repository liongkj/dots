## Python
- Use `uv` instead of `pip` when possible.
- Use `uv run` instead of `python`.

## Testing
- Do not mock tests just to make them pass.
- When in plan mode, always include writing tests.

## Git workflow
- Never use `git add .`; select files one at a time.
- Commit often in logical groups.
- Do not work on `main` unless given permission.

## Writing and content
- Do not use emojis in pull requests.
- Do not make up fake case studies or numbers.
- Sacrifice grammar for the sake of concision.
- List any unresolved questions at the end, if any.

## Autonomy
- Default to action; only ask when a decision is truly blocking.
- If details are missing, pick a reasonable default and state the assumption.
- Keep work moving with small, incremental steps and quick checks.

## Corrections
- Repeated mistake corrected: fix the instance, then remove its cause at the highest level that works: (1) architecture or data structure that makes it impossible, (2) type, lint, or test that fails CI and names the fix, (3) skill or AGENTS rule, judgment calls only. Human review is not a fix.
- Fix outside task scope: propose it with its level instead. Whole class of mistakes: use the `correct` skill.
