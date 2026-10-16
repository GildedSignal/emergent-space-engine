#!/usr/bin/env bash
# P2-P5 regression (the original run's crafted replay) plus the checker's
# six-publish adversarial count, with all-three-marker counting, and the
# content cross-check pristine-final vs patched-final.
# Usage: replay.sh <pristine-wiki.py> <patched-wiki.py>
set -uo pipefail
R=$(cd "$(dirname "$0")" && pwd)
PRIS=$(readlink -f "$1"); PATCH=$(readlink -f "$2")
PY=python3; export PYTHONDONTWRITEBYTECODE=1
INST="$PY $R/inst.py"

runcase() { # <wiki.py> <label> <npublishes>
  local W=$(readlink -f "$1") L=$2 N=$3
  local S=$R/scratch-replay-$L; rm -rf "$S"; mkdir -p "$S/lab/wiki"; cd "$S"
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
  git add -A; git commit -qm C0; local C0=$(git rev-parse HEAD)
  git show "$C0":lab/wiki/topic.md > base-page.md
  local ids=(A B C D E F)
  for i in $(seq 0 $((N-1))); do
    local id=${ids[$i]}
    mkdir -p results/run$id/wiki
    $PY - "run$id" "**Best A plus run$id." "- 20261016-0${i}00-run$id (gold): run$id" <<'PY'
import sys, pathlib
run, best, line = sys.argv[1:4]
t = pathlib.Path("base-page.md").read_text()
t = t.replace("**Best A.", best)
t = t.replace("- 20261016-0000-a (gold): first", f"- 20261016-0000-a (gold): first\n{line}")
pathlib.Path(f"results/{run}/wiki/topic.md").write_text(t)
PY
    printf 'Grade: gold' > results/run$id/DONE; echo "$C0" > results/run$id/base
    $PY "$W" apply results "$C0" >/dev/null
    echo "[$L] publish $((i+1)) ($id): $($INST count lab/wiki/topic.md) maxdepth=$($INST maxdepth lab/wiki/topic.md)"
  done
  $PY "$W" index >/dev/null
  echo "[$L] index row: $(grep '| \[topic\]' lab/wiki/index.md | cut -c1-140)"
  echo "[$L] summary() returns: $($PY -c "import importlib.util as u; s=u.spec_from_file_location('w','$W'); w=u.module_from_spec(s); s.loader.exec_module(w); print(repr(w.summary(open('lab/wiki/topic.md').read())))")"
  echo "[$L] runs-union kept: $(grep -c '^- 2026' lab/wiki/topic.md) run lines"
  echo "[$L] sides present: $(for x in A B C D E F; do [ $x != F ] && printf '%s=%s ' $x $(grep -c "plus run$x" lab/wiki/topic.md); done)"
}

echo "== P2-P4: pristine apply, four concurrent publishes (regression) =="
runcase "$PRIS" PRISTINE 4
echo "== P5: patched v2 apply, same four publishes (regression) =="
runcase "$PATCH" PATCHED 4
echo "== P5+: patched v2 apply, six concurrent publishes (the checker's adversarial count) =="
runcase "$PATCH" PATCHED6 6
echo "== P5x: pristine at six (contrast) =="
runcase "$PRIS" PRISTINE6 6
echo "  $($INST subseq $R/scratch-replay-PRISTINE/lab/wiki/topic.md $R/scratch-replay-PATCHED/lab/wiki/topic.md)"
