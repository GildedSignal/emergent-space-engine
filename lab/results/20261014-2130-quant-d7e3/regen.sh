#!/bin/bash
# Regenerates every number in the dossier from shipped code + this run's patch.
# Patch = 38bf's ES_PULL_CAP re-derivation (the pending wave fix, default-unset) + this run's
# plane_extra_belt_player scene and wave_band bench (progress lines: game-s, RSS, held-scans).
# ~14 min. The in-band arms at N >= 5e4 are EXPECTED to be OOM-killed (exit 137): that is the
# result; /usr/bin/time -v still reports the peak RSS and the progress lines the trajectory.
set -u
cd "$(dirname "$0")/../../.."  # repo root
R=$(dirname "$0")

git apply "$R/work/patch.diff"
trap 'git apply -R "$R/work/patch.diff" || true' EXIT

cargo build --release -p emergent-universe --example wave_band --example wave_input 2>&1 | tail -1
BIN=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-1}/release/examples
mkdir -p "$R/out"

run () { local name=$1; shift; echo "=== $name $(date +%H:%M:%S)"; /usr/bin/time -v "$@" > "$R/out/$name.txt" 2>&1; echo "exit $? ($(date +%H:%M:%S))"; grep -E "Maximum resident" "$R/out/$name.txt"; grep -E "^wave" "$R/out/$name.txt" | tail -1; }

# validity controls (out-of-band, fast): ctl-capped digest must equal 38bf's c2b834bb… record
run ctl-uncapped env -u ES_PULL_CAP $BIN/wave_input 200000 plain 175 100 12
run ctl-capped   env ES_PULL_CAP=64 $BIN/wave_input 200000 plain 175 100 12
# the decisive pair: the player in the belt band at 2.5 AU (root doll), seed 1
run band-uncapped env -u ES_PULL_CAP $BIN/wave_band 200000 1 2.5 175 100 12
run band-capped   env ES_PULL_CAP=64 $BIN/wave_band 200000 1 2.5 175 100 12
# the accumulation watched: 5e4 pair (identical trajectories expected) and 1e5 capped
run band50-uncapped env -u ES_PULL_CAP $BIN/wave_band 50000 1 2.5 155 100 12
run band50-capped   env ES_PULL_CAP=64 $BIN/wave_band 50000 1 2.5 155 100 12
run band100-capped  env ES_PULL_CAP=64 $BIN/wave_band 100000 1 2.5 175 100 12
# the small-N clean arm (completes; digest ad8a0e78…)
run band1k-uncapped env -u ES_PULL_CAP $BIN/wave_band 1000 1 2.5 15 100 12

echo; echo "== digests (controls identical; in-band 2e5/1e5/5e4 die before the cut)"
grep -H "^digest " "$R"/out/ctl-uncapped.txt "$R"/out/ctl-capped.txt "$R"/out/band1k-uncapped.txt
echo "== summary lines"
grep -h "^waveband\|^waveinput" "$R"/out/*.txt
echo "== the accumulation (band50 pair, progress tails)"
tail -3 "$R"/out/band50-uncapped.txt | grep progress; tail -3 "$R"/out/band50-capped.txt | grep progress
echo "== peaks"
grep -H "Maximum resident" "$R"/out/*.txt
