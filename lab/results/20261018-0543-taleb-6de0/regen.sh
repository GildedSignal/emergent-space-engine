#!/bin/sh
# Regenerates every number in dossier.md (run 20261018-0543-taleb-6de0) from the patched
# tree (work/patch.diff applied by the runner), in ~9 minutes on 8 vCPUs.
set -e
cd "$(dirname "$0")"
ROOT=../../..
cargo build --release -p emergent-universe --bin tail --manifest-path "$ROOT/Cargo.toml"
BIN=$(ls /home/glmlab/lab-target-2/release/tail 2>/dev/null || echo "$ROOT/target/release/tail")
export TAILBIN="$BIN"
sed "s|BIN=.*|BIN=$BIN|" screen.sh > work/screen-run.sh
sh work/screen-run.sh 0.01 4 100000 work/screen-m2 >/dev/null
sh work/screen-run.sh 0.01 16 100000 work/screen-m2-16 >/dev/null
sh work/screen-run.sh 0.001 64 100000 work/screen-m3 >/dev/null
mkdir -p work/trace
for args in "1.5 169.1 a" "-0.682 81.8 b" "0.409 114.5 c"; do
  set -- $args
  KICK_TRACE=work/trace/k$3.txt KICK_TRACE_EVERY=16 "$BIN" 0.01 $1 $2 16 1500000 > work/trace/summary-$3.json 2>&1 &
done
wait
KICK_TRACE=work/trace/ka2.txt KICK_TRACE_EVERY=16 "$BIN" 0.01 1.5 169.1 16 600000 > work/trace/summary-a2.json 2>&1 &
for args in "-0.682 103.6 d" "-0.409 114.5 e" "1.227 60.0 f" "0.136 136.4 g" "-1.227 169.1 h"; do
  set -- $args
  echo "KICK_TRACE=work/trace/k$3.txt KICK_TRACE_EVERY=64 $BIN 0.01 $1 $2 16 160000 > work/trace/summary-$3.json 2>&1"
done | xargs -P 5 -I{} sh -c '{}'
wait
python3 analyze.py
