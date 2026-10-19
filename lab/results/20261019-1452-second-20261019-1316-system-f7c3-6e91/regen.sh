#!/bin/sh
# Regen: every dossier number, from shipped code + work/patch.diff (runner applies it first;
# this re-applies only if missing). ~12 min on the 8-vCPU lab box.
set -e
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261019-1452-second-20261019-1316-system-f7c3-6e91
if [ ! -f crates/universe/examples/beltcensus.rs ]; then
  git apply --check $R/work/patch.diff && git apply $R/work/patch.diff
fi
echo "loadavg at start: $(cut -d' ' -f1-3 /proc/loadavg)"
cargo build --release -p emergent-universe --example beltcensus --example servetime -p xtask 2>/dev/null

echo "=== controls: memo.rs (guard 0.85) OFF / ON, qmemo ==="
cargo test --release -p emergent-universe --test memo 2>&1 | grep -E "test result|distinct"
ES_QMEMO=1 cargo test --release -p emergent-universe --test memo 2>&1 | grep -E "test result|distinct"
cargo test --release -p emergent-universe --test qmemo 2>&1 | grep "test result"

echo "=== belt stream, 10^4 and 10^5, exact vs served ==="
cd crates/universe
for arm in "10000 1 50 1800" "100000 1 50 1800"; do
  echo "--- $arm exact ---"
  timeout 70 env ES_CENSUS=1 cargo run --release -q -p emergent-universe --example beltcensus -- $arm 2>/dev/null | grep -E "^census:|^stream:|^stream_split:|^served:"
  echo "--- $arm served ---"
  timeout 70 env ES_CENSUS=1 ES_QMEMO=1 cargo run --release -q -p emergent-universe --example beltcensus -- $arm 2>/dev/null | grep -E "^census:|^stream:|^stream_split:|^served:"
done

echo "=== belt-key constants (microbench, 99,699 keys) ==="
timeout 90 cargo run --release -q -p emergent-universe --example servetime -- 100000 1 2>/dev/null | grep belt_keys
timeout 90 env ES_QMEMO=1 cargo run --release -q -p emergent-universe --example servetime -- 100000 1 2>/dev/null | grep belt_keys
cd ../../

echo "=== gates: B13 exact vs served (the decisive pair) ==="
cargo run --release -q -p xtask -- behave --law plane --gates B13 2>/dev/null | grep -E "^B13"
ES_QMEMO=1 cargo run --release -q -p xtask -- behave --law plane --gates B13 2>/dev/null | grep -E "^B13"
echo "=== gates: strong-branch guard (ES_QWEAK=1) does not rescue ==="
ES_QMEMO=1 ES_QWEAK=1 cargo run --release -q -p xtask -- behave --law plane --gates B13 2>/dev/null | grep -E "^B13"
echo "=== B13 per-draw, served (the failing draws) ==="
ES_QMEMO=1 timeout 120 cargo test --release -q -p xtask b13_by_draw -- --ignored --nocapture 2>/dev/null | grep -E "^step|^draw" | sed -n '1,6p;20,24p'

echo "=== gates: B12 (broken instrument here: fails for the exact law) and B17 (60 s limit) ==="
cargo run --release -q -p xtask -- behave --law plane --gates B12 2>/dev/null | grep -E "^B12" | cut -c1-140
ES_QMEMO=1 cargo run --release -q -p xtask -- behave --law plane --gates B12 2>/dev/null | grep -E "^B12" | cut -c1-140
timeout 100 cargo run --release -q -p xtask -- behave --law plane --gates B17 2>/dev/null | grep -E "^B17" || echo "B17 (exact): timeout over the 60 s limit"
timeout 100 env ES_QMEMO=1 cargo run --release -q -p xtask -- behave --law plane --gates B17 2>/dev/null | grep -E "^B17" || echo "B17 (served): timeout over the 60 s limit"

echo "=== clean-tree control: B13 on the pristine shipped law ==="
git stash push -q -m lab-clean-control crates/space crates/universe
cargo run --release -q -p xtask -- behave --law plane --gates B13 2>/dev/null | grep -E "^B13"
git stash pop -q
git status --short | grep -v '^??' | head -6
echo "regen done"
