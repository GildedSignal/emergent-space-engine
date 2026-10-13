#!/usr/bin/env bash
# Regenerates every number in dossier.md from the patched tree (work/patch.diff is applied
# before this runs). ~8–10 minutes on the lab runner: two builds, the probe in both arms,
# the digest comparison, and the universe suite.
set -euo pipefail
cd "$(dirname "$0")/../../.."

RUN=lab/results/20261013-0037-second-20261012-2257-spacex-5eb6-8b43
mkdir -p "$RUN"
run() { cargo run --release -q -p emergent-universe --example lazy_probe -- "$@"; }

echo "== 1. the starvation case (the run's decisive experiment): budgeted vs settled vs stepped =="
run starve 2>&1 | tee "$RUN/starve-lazy.txt"
ES_EAGER=1 run starve 2>&1 | tee "$RUN/starve-eager.txt"
python3 "$RUN/check_starve.py"

echo "== 2. quiet frames (the zero-event tier), both arms, 428 to 400k bodies =="
run quiet | tee "$RUN/quiet-lazy.json"
ES_EAGER=1 run quiet | tee "$RUN/quiet-legacy.json"

echo "== 3. the plane to a canonical cut, both arms, 15 schedules =="
run fly | tee "$RUN/fly-lazy.json"
ES_EAGER=1 run fly | tee "$RUN/fly-legacy.json"
python3 "$RUN/compare.py"

echo "== 4. adversarial: the tie storm, the fastest bindable player, the replay schedule =="
run storm | tee "$RUN/storm-lazy.json"
ES_EAGER=1 run storm | tee "$RUN/storm-eager.json"
run fast | tee "$RUN/fast-lazy.json"
ES_EAGER=1 run fast | tee "$RUN/fast-eager.json"
run replay 2>/dev/null | tee "$RUN/replay-lazy.json"
ES_EAGER=1 run replay 2>/dev/null | tee "$RUN/replay-eager.json"
python3 "$RUN/check_adversarial.py"

echo "== 5. the universe suite (cross-schedule digest gauntlet) =="
cargo test --release -q -p emergent-universe 2>&1 | grep -E "running [0-9]+ test|test result" | tee "$RUN/suite.txt"
