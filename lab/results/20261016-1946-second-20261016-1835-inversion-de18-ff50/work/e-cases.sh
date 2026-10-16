#!/usr/bin/env bash
# The checker's E-cases: interleaved damage (three concurrent pristine publishes
# damage the page), then the patched publisher must never write a marker line
# back — with or without a heal in between. v1 contrast included.
# Usage: e-cases.sh <pristine-wiki.py> <v1-wiki.py> <v2-wiki.py>
set -uo pipefail
R=$(cd "$(dirname "$0")" && pwd)
PRIS=$(readlink -f "$1"); V1=$(readlink -f "$2"); V2=$(readlink -f "$3")
PY=python3; export PYTHONDONTWRITEBYTECODE=1
INST="$PY $R/inst.py"

S=$R/scratch-e; rm -rf "$S"; mkdir -p "$S/lab/wiki"; cd "$S"
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

mkrun() { # id best line
  local id=$1 best=$2 line=$3
  mkdir -p results/$id/wiki
  $PY - "$id" "$best" "$line" <<'PY'
import sys, pathlib
run, best, line = sys.argv[1:4]
t = pathlib.Path("base-page.md").read_text()
t = t.replace("**Best A.", best)
t = t.replace("- 20261016-0000-a (gold): first", f"- 20261016-0000-a (gold): first\n{line}")
pathlib.Path(f"results/{run}/wiki/topic.md").write_text(t)
PY
  printf 'Grade: gold' > results/$id/DONE; echo "$C0" > results/$id/base
}

# damage: three concurrent pristine publishes (A, B, C from the same base)
for id in A B C; do mkrun run$id "**Best A plus run$id." "- 20261016-0100-run$id (gold): run$id"; done
$PY "$PRIS" apply results "$C0" >/dev/null
cp lab/wiki/topic.md damaged.md
echo "damaged page (pristine, 3 concurrent publishes): $($INST count damaged.md) maxdepth=$($INST maxdepth damaged.md)"

echo "== E1: patched apply (runD) straight on the damaged page =="
mkrun runD "**Best A plus runD." "- 20261016-0200-runD (gold): rund"
rm -rf e1; mkdir -p e1/lab/wiki; cp lab/wiki/*.md e1/lab/wiki/
(cd e1 && cp -r "$S"/results ./results && LAB_WIKI=lab/wiki $PY "$V2" apply results "$C0" >/dev/null)
echo "  v2 on damaged -> e1: $($INST count e1/lab/wiki/topic.md)  content: $($INST subseq damaged.md e1/lab/wiki/topic.md)"
rm -rf e1v1; mkdir -p e1v1/lab/wiki; cp lab/wiki/*.md e1v1/lab/wiki/
(cd e1v1 && cp -r "$S"/results ./results && LAB_WIKI=lab/wiki $PY "$V1" apply results "$C0" >/dev/null)
echo "  v1 contrast -> e1v1: $($INST count e1v1/lab/wiki/topic.md) (the checker found 2 marker lines back)"

echo "== E2: heal first, then patched apply (runD) =="
rm -rf e2; mkdir -p e2/lab/wiki; cp lab/wiki/*.md e2/lab/wiki/
(cd e2 && LAB_WIKI=lab/wiki $PY "$V2" heal >/dev/null && cp -r "$S"/results ./results && LAB_WIKI=lab/wiki $PY "$V2" apply results "$C0" >/dev/null)
echo "  healed then apply -> e2: $($INST count e2/lab/wiki/topic.md)  content: $($INST subseq damaged.md e2/lab/wiki/topic.md)"

echo "== E3: apply on damaged, heal, apply again (runE too) =="
mkrun runE "**Best A plus runE." "- 20261016-0300-runE (gold): rune"
rm -rf e3; mkdir -p e3/lab/wiki; cp lab/wiki/*.md e3/lab/wiki/
(cd e3 && cp -r "$S"/results ./results && LAB_WIKI=lab/wiki $PY "$V2" apply results "$C0" >/dev/null \
  && LAB_WIKI=lab/wiki $PY "$V2" heal >/dev/null \
  && LAB_WIKI=lab/wiki $PY "$V2" apply results "$C0" >/dev/null)
echo "  apply->heal->apply -> e3: $($INST count e3/lab/wiki/topic.md)  content: $($INST subseq damaged.md e3/lab/wiki/topic.md)"
echo "  all five sides present in e3: $(for x in A B C D E; do printf '%s=%s ' $x $(grep -c "plus run$x" e3/lab/wiki/topic.md); done)"
echo "  runs union in e3: $(grep -c '^- 2026' e3/lab/wiki/topic.md) run lines"
