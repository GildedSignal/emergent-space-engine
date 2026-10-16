#!/bin/sh
# Regen for 20261016-1459-spacex-7fd2: the kick's key-displacement census.
# Applies work/patch.diff, rebuilds, reruns the three bench arms, re-analyzes.
# Total wall on the lab box: ~3 min (build ~50 s + three ~2 s runs + analysis).
set -e
cd "$(dirname "$0")/../../.."   # repo root
RUN=lab/results/20261016-1459-spacex-7fd2

git apply --check "$RUN/work/patch.diff" 2>/dev/null && git apply "$RUN/work/patch.diff" \
  || echo "patch already applied or tree dirty; continuing on current tree"

cargo build --release -p xtask

for sd in 3 7 11; do
  ES_KICK_DUMP="$RUN/work/kicks-s$sd.json" \
    cargo run --release -p xtask -- universe --kick-bench --seed $sd --rtf 100 --seconds 30 \
    > "$RUN/work/bench-s$sd.json"
done

# Pristine-tree digest control (patch neutrality), seed 3 only.
git stash -q
cargo build --release -p xtask
cargo run --release -p xtask -- universe --kick-bench --seed 3 --rtf 100 --seconds 30 \
  > "$RUN/work/bench-pristine-s3.json"
git stash pop -q
cargo build --release -p xtask

cd "$RUN/work"
python3 ../analyze.py kicks-s3.json kicks-s7.json kicks-s11.json
echo "regen done: $RUN/work/census-summary.json + bench-s*.json + bench-pristine-s3.json"
