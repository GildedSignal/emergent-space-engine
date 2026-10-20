#!/bin/sh
# Regen: every dossier number from shipped code + work/patch.diff.
# Total ~6 min (two release builds dominate). Never touches git.
cd "$(dirname "$0")/../../.."   # repo root
RUN=lab/results/20261020-1210-spacex-624a
X=/home/glmlab/lab-target-1/release/xtask

# 1. Apply the census patch if not already applied.
git diff --quiet -- crates/space/src/orbit.rs || git apply --check "$RUN/work/patch.diff" 2>/dev/null || true
if git diff --quiet -- crates/space/src/orbit.rs; then git apply "$RUN/work/patch.diff"; fi

# 2. Instrument controls.
cargo test --release -p emergent-space mint_census 2>&1 | grep "test result"

# 3. Pristine references (digest neutrality): save patched binary, restore tree.
cp "$X" /tmp/xtask-patched
git checkout -- crates xtask
cargo build --release -p xtask
for a in "default:--seconds 30" "fleet:--members 400 --rtf 100 --seconds 30" "seed3:--seed 3 --rtf 100 --seconds 30"; do
  name=${a%%:*}; args=${a#*:}
  $X universe --kick-bench $args > "$RUN/work/ref-$name.json"
done

# 4. Patched arms (digest must equal pristine; census is print-only).
git apply "$RUN/work/patch.diff"
cargo build --release -p xtask
for a in "default:--seconds 30" "fleet:--members 400 --rtf 100 --seconds 30" "seed3:--seed 3 --rtf 100 --seconds 30"; do
  name=${a%%:*}; args=${a#*:}
  $X universe --kick-bench $args > "$RUN/work/cen-$name.json"
done

# 5. The numbers.
python3 "$RUN/summarize.py"
