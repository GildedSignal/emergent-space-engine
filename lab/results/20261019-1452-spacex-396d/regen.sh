#!/usr/bin/env bash
# Regen: rebuild the instrument (work/patch.diff applied by the runner before this runs) and refly both arms + analysis.
# Budget: build ~15 s, flights ~85 s + ~70 s, analysis < 1 s. Total < 4 min.
cd "$(dirname "$0")/../../.."   # repo root (lab/results/<run>/regen.sh -> results -> lab -> root)
RUN=lab/results/20261019-1452-spacex-396d
cargo build --release -p emergent-universe --example seam
BIN="${CARGO_TARGET_DIR:-target}/release/examples/seam"
cd "$RUN"
ES_SEAM_CENSUS=1 ES_SEAM_CAP_S=1500 ES_SEAM_RSS_MB=1400 "$BIN" 10000 burn 700000 100 12 > logs/long-k1e4-burn.out 2> logs/long-k1e4-burn.err
ES_SEAM_CENSUS=1 ES_SEAM_CAP_S=1400 ES_SEAM_RSS_MB=1300 "$BIN" 30000 burn 40000 100 12 > logs/long-k3e4-burn.out 2> logs/long-k3e4-burn.err
# the shipped-path control: census off, one short flight, same digest-class counters (kicks/events) must match the census-on arm's early flight
"$BIN" 10000 burn 25 100 12 > logs/ctl-k1e4-burn.out 2> logs/ctl-k1e4-burn.err
python3 analyze.py long-k1e4-burn
python3 analyze.py long-k3e4-burn
grep -E "frames after|ladder:" logs/long-k1e4-burn.out | head -2
grep -E "frames after|ladder:" logs/long-k3e4-burn.out | head -2
