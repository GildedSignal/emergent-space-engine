#!/usr/bin/env bash
# Regen for 20261020-0229-fermi-476d: rebuilds every dossier number from shipped code + work/patch.diff.
# ~4 min: build (~10 s warm) + 6 flights (1e5 s17 ~26 s, s10 ~20 s; 2e5 s10 ~36 s, s17 ~50-90 s or killed past ~28k gs; 3e5 s10 ~47 s, s17 ~60-90 s or killed) + analysis.
set -u
cd "$(dirname "$0")/../../.." || exit 1  # repo root
RUN=lab/results/20261020-0229-fermi-476d
D=$RUN/work/flights
mkdir -p "$D"
git apply "$RUN/work/patch.diff" 2>/dev/null || echo "patch already applied"
cargo build --release -p emergent-universe --example nladder || exit 1
BIN=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-2}/release/examples/nladder
# arms: reproduction (full window), matched 600-frame, held-out 3e5, long windows for the wave-2 channel
for spec in "100000 17" "100000 10" "200000 10" "200000 17" "300000 10"; do
  set -- $spec
  k=$1; s=$2
  if [ ! -s "$D/k${k}_s${s}.out" ]; then
    "$BIN" "$k" burn "$s" 2000 12 2>"$D/k${k}_s${s}.csv.err" >"$D/k${k}_s${s}.out" \
      || echo "arm k=$k s=$s exited nonzero (memory kill past the crest is expected on the s17 arms; the csv keeps the frames)"
  fi
done
python3 "$RUN/work/wave_analysis.py"
python3 "$RUN/work/compose.py"
