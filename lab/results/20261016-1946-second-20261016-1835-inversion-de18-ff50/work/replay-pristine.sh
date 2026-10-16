#!/usr/bin/env bash
# Replay the production publish sequence through a lab/wiki.py apply() in a
# throwaway git repo: three gold runs (A, B, C) starting from the same commit,
# each rewriting ## Current best from the SAME start page (concurrent windows).
# Usage: replay-pristine.sh <path-to-wiki.py> <output-label>
set -euo pipefail
WIKI_PY=$(readlink -f "$1"); LABEL=$2
S=$(mktemp -d); trap 'rm -rf "$S"' EXIT
mkdir -p "$S/lab/wiki"
cd "$S"
git init -q .; git config user.email t@t; git config user.name t
cat > lab/wiki/topic.md <<'EOF'
topic: topic
status: open
closed-by:
valid-while:
updated: 20261016-0000-a

# T

## Current best

**Best A.**

## Refuted

- none

## Runs
- 20261016-0000-a (gold): first
EOF
git add -A; git commit -qm C0; C0=$(git rev-parse HEAD)
git show "$C0":lab/wiki/topic.md > base-page.md

mkrun() { # id  new-best-text  runs-line
  local id=$1 best=$2 line=$3
  mkdir -p "results/$id/wiki"
  python3 - "$id" "$best" "$line" <<'PY'
import sys, pathlib
run, best, line = sys.argv[1:4]
t = pathlib.Path("base-page.md").read_text()
t = t.replace("**Best A.", best)
t = t.replace("- 20261016-0000-a (gold): first", f"- 20261016-0000-a (gold): first\n{line}")
pathlib.Path(f"results/{run}/wiki/topic.md").write_text(t)
PY
  printf 'Grade: gold' > "results/$id/DONE"
  echo "$C0" > "results/$id/base"
}

mkrun runA "**Best A plus runA." "- 20261016-0100-runA (gold): second"
python3 "$WIKI_PY" apply results "$C0"
echo "[$LABEL] after A: markers=$(grep -c '^<<<<<<< ' lab/wiki/topic.md || true)"

mkrun runB "**Best A plus runB." "- 20261016-0200-runB (gold): third"
python3 "$WIKI_PY" apply results "$C0"
echo "[$LABEL] after B: markers=$(grep -c '^<<<<<<< ' lab/wiki/topic.md || true)"

mkrun runC "**Best A plus runC." "- 20261016-0300-runC (gold): fourth"
python3 "$WIKI_PY" apply results "$C0"
D=$(awk '/^<<<<<<< /{d++; if(d>m)m=d} /^>>>>>>> /{d--} END{print m+0}' lab/wiki/topic.md)
echo "[$LABEL] after C: markers=$(grep -c '^<<<<<<< ' lab/wiki/topic.md || true) maxdepth=$D"

mkrun runD "**Best A plus runD." "- 20261016-0400-runD (gold): fifth"
python3 "$WIKI_PY" apply results "$C0"
D=$(awk '/^<<<<<<< /{d++; if(d>m)m=d} /^>>>>>>> /{d--} END{print m+0}' lab/wiki/topic.md)
echo "[$LABEL] after D: markers=$(grep -c '^<<<<<<< ' lab/wiki/topic.md || true) maxdepth=$D"

python3 "$WIKI_PY" index
echo "[$LABEL] index row: $(grep '| \[topic\]' lab/wiki/index.md)"
echo "[$LABEL] summary() returns: $(python3 -c "
import importlib.util
spec = importlib.util.spec_from_file_location('w', '$WIKI_PY'); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
print(repr(w.summary(open('lab/wiki/topic.md').read())))")"
echo "[$LABEL] runs-union kept: $(grep -c '^- 2026' lab/wiki/topic.md) run lines"
echo "[$LABEL] sides preserved: A=$(grep -c 'plus runA' lab/wiki/topic.md) B=$(grep -c 'plus runB' lab/wiki/topic.md) C=$(grep -c 'plus runC' lab/wiki/topic.md) D=$(grep -c 'plus runD' lab/wiki/topic.md)"
