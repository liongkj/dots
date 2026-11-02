#!/usr/bin/env bash
# Install or update cursor/plugins pstack for OpenCode. Re-run after upstream changes.
set -euo pipefail

REPO="$HOME/.local/share/cursor-plugins"
SRC="$REPO/pstack"
SKILLS="$HOME/.config/opencode/skills"
AGENTS="$HOME/.config/opencode/agents"

if [ -d "$REPO/.git" ]; then
  git -C "$REPO" pull -q --ff-only
else
  git clone -q --depth 1 --filter=blob:none --sparse https://github.com/cursor/plugins.git "$REPO"
  git -C "$REPO" sparse-checkout set pstack
fi

mkdir -p "$SKILLS" "$AGENTS"

# Drop links to skills that upstream removed.
for link in "$SKILLS"/*; do
  [ -L "$link" ] || continue
  case "$(readlink "$link")" in "$SRC"/skills/*) [ -e "$link" ] || rm "$link" ;; esac
done

for dir in "$SRC"/skills/*/; do
  name="$(basename "$dir")"
  # OpenCode also reads ~/.agents/skills and drops a name found in both.
  if [ -e "$HOME/.agents/skills/$name" ]; then
    [ -L "$SKILLS/$name" ] && rm "$SKILLS/$name"
    continue
  fi
  ln -sfn "${dir%/}" "$SKILLS/$name"
done

for file in "$SRC"/agents/*.md; do
  name="$(basename "$file")"
  awk -v skill="$SRC/skills/poteto-mode/SKILL.md" '
    NR == 1 && $0 == "---" { print; infm = 1; next }
    infm && $0 == "---" { print "mode: subagent"; print; infm = 0; next }
    infm && /^(name|is_background):/ { next }
    { gsub(/search `~\/\.cursor\/plugins\/` for a file whose path ends in `skills\/poteto-mode\/SKILL.md`/, "read `" skill "`") }
    { print }
  ' "$file" > "$AGENTS/$name"
done

version="$(sed -n 's/.*"version": *"\([^"]*\)".*/\1/p' "$SRC/plugin.json" | head -1)"
echo "pstack $version: $(ls -d "$SRC"/skills/*/ | wc -l | tr -d ' ') skills, $(ls "$SRC"/agents/*.md | wc -l | tr -d ' ') agents"
