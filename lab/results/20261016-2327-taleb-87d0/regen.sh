#!/usr/bin/env bash
# Regen for run 20261016-2327-taleb-87d0. Everything is deterministic text work
# on lab/wiki.py + git; runs in well under a minute. The runner applies
# work/patch.diff first; if not, this applies it (idempotently guarded).
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
RUN=lab/results/20261016-2327-taleb-87d0

grep -q "def defuse" lab/wiki.py || git apply "$RUN/work/patch.diff"
grep -q "def defuse" lab/wiki.py || { echo "patch not applied"; exit 1; }

# the pristine control is always regenerated from git (never trusted from work/)
git show HEAD:lab/wiki.py > "$RUN/work/wiki-pristine.py"
grep -q "def defuse" "$RUN/work/wiki-pristine.py" && { echo "control is not pristine"; exit 1; }

python3 "$RUN/work/sims.py" 2>&1 | tee "$RUN/work/sims-out.txt"

echo "== regen complete; verdicts above (S3/S4/S5 each OK, S2 control deepened, S6 skip vs no-skip)"
