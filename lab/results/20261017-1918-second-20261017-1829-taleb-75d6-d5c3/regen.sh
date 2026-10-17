#!/usr/bin/env bash
# Regen (20261017-1918-second-20261017-1829-taleb-75d6-d5c3): every dossier number, from the patched
# tree (work/patch.diff applied by the runner before this runs: ES_STAGGER + ES_STAGGER_SYM hunks in
# crates/universe/src/step.rs, the instrument v2 crates/universe/examples/stagger_legality.rs, and
# this folder's scripts). ~13 min single box; every arm of a seed reads at the SAME absolute ticks.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261017-1918-second-20261017-1829-taleb-75d6-d5c3
RUN() { echo "+ $*" >&2; "$@"; }

RUN cargo build --release -p emergent-universe --example stagger_legality
RUN cargo build --release -p emergent-universe --example frame_digest

# The common readout ticks, from each seed's OFF arm base (setup: no criteria data in them).
BASE=$(env -u ES_STAGGER -u ES_STAGGER_SYM cargo run --release -q -p emergent-universe --example stagger_legality -- base 1 128 2>/dev/null | grep '# BASE')
TW1=$(echo "$BASE" | sed 's/.*t_wave_end=\([0-9]*\).*/\1/')
PM1=$(echo "$BASE" | sed 's/.*p_min=\([0-9.e+-]*\).*/\1/')
BASE2=$(env -u ES_STAGGER -u ES_STAGGER_SYM cargo run --release -q -p emergent-universe --example stagger_legality -- base 2 128 2>/dev/null | grep '# BASE')
TW2=$(echo "$BASE2" | sed 's/.*t_wave_end=\([0-9]*\).*/\1/')
PM2=$(echo "$BASE2" | sed 's/.*p_min=\([0-9.e+-]*\).*/\1/')
read -r T1 T2 <<EOF
$(python3 -c "import math; t=$TW1; p=float('$PM1'); print(int(t+1.0*p), int(t+2.0*p))")
EOF
T1S2=$(python3 -c "import math; print(int($TW2+1.0*float('$PM2')))")
echo "common ticks: s1 T1=$T1 T2=$T2 ; s2 T1=$T1S2" >&2
echo "$BASE / $BASE2 / s1: T1=$T1 T2=$T2 ; s2: T1=$T1S2" > "$R/ticks.txt"

# The decisive matrix (CSVs; stderr keeps the settle/digest progress). The two ref9 commands and
# ref8 s1 run past the 60-s norm (~100-240 s: 4x/2x the kicks to two belt orbits) - disclosed.
RUN env -u ES_STAGGER -u ES_STAGGER_SYM timeout 120 cargo run --release -q -p emergent-universe --example stagger_legality -- off 1 128 at:$T1,$T2 > "$R/off_s1.csv" 2> "$R/off_s1.err"
RUN env ES_STAGGER=1 timeout 120 cargo run --release -q -p emergent-universe --example stagger_legality -- on 1 128 at:$T1,$T2 > "$R/on_s1.csv" 2> "$R/on_s1.err"
RUN env ES_STAGGER_SYM=1 timeout 120 cargo run --release -q -p emergent-universe --example stagger_legality -- sym 1 128 at:$T1,$T2 > "$R/sym_s1.csv" 2> "$R/sym_s1.err"
RUN env -u ES_STAGGER -u ES_STAGGER_SYM timeout 200 cargo run --release -q -p emergent-universe --example stagger_legality -- ref8 1 128 at:$T1,$T2 > "$R/ref8_s1.csv" 2> "$R/ref8_s1.err"
RUN env -u ES_STAGGER -u ES_STAGGER_SYM timeout 320 cargo run --release -q -p emergent-universe --example stagger_legality -- ref9 1 128 at:$T1,$T2 > "$R/ref9_s1.csv" 2> "$R/ref9_s1.err"
RUN env -u ES_STAGGER -u ES_STAGGER_SYM timeout 120 cargo run --release -q -p emergent-universe --example stagger_legality -- off 2 128 at:$T1S2 > "$R/off_s2.csv" 2> "$R/off_s2.err"
RUN env ES_STAGGER=1 timeout 120 cargo run --release -q -p emergent-universe --example stagger_legality -- on 2 128 at:$T1S2 > "$R/on_s2.csv" 2> "$R/on_s2.err"
RUN env ES_STAGGER_SYM=1 timeout 120 cargo run --release -q -p emergent-universe --example stagger_legality -- sym 2 128 at:$T1S2 > "$R/sym_s2.csv" 2> "$R/sym_s2.err"
RUN env -u ES_STAGGER -u ES_STAGGER_SYM timeout 320 cargo run --release -q -p emergent-universe --example stagger_legality -- ref9 2 128 at:$T1S2 > "$R/ref9_s2.csv" 2> "$R/ref9_s2.err"

# C4 (mechanics): the first-rebind lead, just past each arm's wave. off/sym must read lead = half
# (a symmetric first step; sym's half is re-derived at t+off), on must read lead = half + off.
RUN env -u ES_STAGGER -u ES_STAGGER_SYM timeout 60 cargo run --release -q -p emergent-universe --example stagger_legality -- off 1 128 at:2937920643 > "$R/mech_off.csv" 2>/dev/null
RUN env ES_STAGGER=1 timeout 60 cargo run --release -q -p emergent-universe --example stagger_legality -- on 1 128 at:8508023861 > "$R/mech_on.csv" 2>/dev/null
RUN env ES_STAGGER_SYM=1 timeout 60 cargo run --release -q -p emergent-universe --example stagger_legality -- sym 1 128 at:8508023861 > "$R/mech_sym.csv" 2>/dev/null

# C3: the patched build with BOTH gates unset is bit-identical to pristine (frame_digest; the timing
# annotations differ, the digests must not). Restore the patch afterwards.
cp crates/universe/src/step.rs /tmp/step_patched.rs.$$
git checkout -- crates/universe/src/step.rs
trap 'cp /tmp/step_patched.rs.$$ crates/universe/src/step.rs' EXIT
RUN env timeout 100 cargo run --release -q -p emergent-universe --example frame_digest -- 3 2>/dev/null | sed 's/ \[[0-9.]* s\]//' > "$R/fd_pristine.txt"
cp /tmp/step_patched.rs.$$ crates/universe/src/step.rs
RUN env -u ES_STAGGER -u ES_STAGGER_SYM timeout 100 cargo run --release -q -p emergent-universe --example frame_digest -- 3 2>/dev/null | sed 's/ \[[0-9.]* s\]//' > "$R/fd_patched.txt"
if diff -q "$R/fd_pristine.txt" "$R/fd_patched.txt" >/dev/null; then echo "C3: PRISTINE == PATCHED-OFF (digests identical)" | tee "$R/c3.txt"; else echo "C3: MISMATCH" | tee "$R/c3.txt"; fi

RUN python3 "$R/analyze.py" > "$R/analysis.json"
echo "regen done: $R/analysis.json"
