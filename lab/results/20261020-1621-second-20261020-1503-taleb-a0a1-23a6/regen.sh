#!/usr/bin/env bash
# Regenerates every dossier number from shipped code + work/patch.diff (applied by the runner
# before this runs). Flights: 3 wall (~45 s each, W3 up to ~70 s and 5.9 GB — see dossier), the
# 1e5 digest pair + determinism control (3 flights, the OFF arms pay an ~18 s settle), the 3e5
# digest pair, and the verify control. Total ~10 min + build (~10 s incremental).
set -eu
RUN_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$RUN_DIR/../.." && pwd)"
cd "$REPO"
cargo build --release -p emergent-universe --example nladder
BIN=${CARGO_TARGET_DIR:-target}/release/examples/nladder
cd "$RUN_DIR/work"

# Wall arms (anatomy, wall-mode burn at frame 60 as shipped): W1 OFF / W2 ON at 1e5, W3 ON at 3e5.
ES_ANSWER_ANATOMY=1 timeout 100 "$BIN" 100000 burn 45 1300 12 1 > w1_1e5_off.out 2> w1_1e5_off.err || true
ES_ANSWER_ANATOMY=1 ES_CARRY_BOUND=1 timeout 100 "$BIN" 100000 burn 45 1300 12 1 > w2_1e5_on.out 2> w2_1e5_on.err || true
ES_ANSWER_ANATOMY=1 ES_CARRY_BOUND=1 timeout 110 "$BIN" 300000 burn 45 1300 12 1 > w3_3e5_on.out 2> w3_3e5_on.err || true

# Digest identity at a canonical cut (cut mode schedules the burn at one fixed tick: a wall-mode
# input at `now` ties the digest to the frames' pacing — the run's harness finding). No TTL fence
# (wall-time, breaks the cut). E1/E2 = OFF twice (determinism control), E3 = ON at 1e5 cut 30k gs;
# E4/E5 = OFF/ON at 3e5 cut 19.5k gs (pre-ALL era there, disclosed).
timeout 160 "$BIN" 100000 burn 25 1300 12 1 30000 > e1_off.out 2> e1_off.err || true
timeout 160 "$BIN" 100000 burn 25 1300 12 1 30000 > e2_off.out 2> e2_off.err || true
ES_ANSWER_ANATOMY=1 ES_CARRY_BOUND=1 timeout 160 "$BIN" 100000 burn 25 1300 12 1 30000 > e3_1e5_on.out 2> e3_1e5_on.err || true
ES_ANSWER_ANATOMY=1 timeout 160 "$BIN" 300000 burn 17 1300 12 1 19500 > e4_3e5_off.out 2> e4_3e5_off.err || true
ES_ANSWER_ANATOMY=1 ES_CARRY_BOUND=1 timeout 160 "$BIN" 300000 burn 17 1300 12 1 19500 > e5_3e5_on.out 2> e5_3e5_on.err || true
# The verify control: every body the bound skips is read exactly and asserted not-hit (45 s wall).
ES_ANSWER_ANATOMY=1 ES_CARRY_BOUND=1 ES_BOUND_VERIFY=1 timeout 100 "$BIN" 3000 burn 45 1300 12 1 > d5_3e3_verify.out 2> d5_3e3_verify.err || true

echo "== walks and channel =="
./analyze.sh w1_1e5_off 100028
./analyze.sh w2_1e5_on 100028
./analyze.sh w3_3e5_on 300076
echo "== digest identity (P1): determinism control then the pairs =="
for A in e1_off e2_off e3_1e5_on; do echo -n "$A: "; grep -o 'digest: [0-9a-f]*' $A.out; done
for A in e4_3e5_off e5_3e5_on; do echo -n "$A: "; grep -o 'digest: [0-9a-f]*' $A.out; done
grep -h "^cut" e1_off.out e3_1e5_on.out e4_3e5_off.out e5_3e5_on.out
echo "== the answer walk's collapse (E3 belt-wide answers, settle answers every held scan) =="
grep '^ANS' e3_1e5_on.err | sed 's/ANS t=//; s/ ns=/ /; s/ read_ns=/ /; s/ cand=/ /; s/ tests=/ /; s/ skip_dom=/ /; s/ skip_bnd=/ /; s/ enc=/ /' | awk '$4 >= 50000 {n++; tot+=$2; c+=$4; sb+=$7; us=$2/$4/1000; if (us>3) cold++; else {wn++; wu+=us; if (us>wmax) wmax=us}} END {printf "1e5 belt-wide: n=%d cold=%d; warm n=%d mean %.4f worst %.4f us/body; mean skip %.2f%%\n", n, cold+0, wn+0, wu/wn, wmax, 100*sb/c}'
echo "-- 3e5 (E4 vs E5, same windows, cand>10000):"
for A in e4_3e5_off e5_3e5_on; do echo -n "  $A: "; grep '^ANS' $A.err | awk '{for(i=1;i<=NF;i++){if($i~/^cand=/)c=substr($i,6); if($i~/^ns=/)n=substr($i,4)}; if(c+0>10000){k++; s+=n/c} } END {printf "%d answers >10k cand, mean %.3f us/body\n", k, s/k/1000}'; done
echo "== verify control (D5): panics =="
grep -c "panicked" d5_3e3_verify.err || echo "0 (clean)"
echo "regen done"
