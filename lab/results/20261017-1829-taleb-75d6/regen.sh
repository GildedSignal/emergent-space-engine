#!/usr/bin/env bash
# Regen (20261017-1829-taleb-75d6): every dossier number, from the patched tree (work/patch.diff
# applied by the runner before this runs: ES_STAGGER hunk in crates/universe/src/step.rs + the
# probe crates/universe/examples/stagger_legality.rs + this folder's scripts). ~6 min single-box.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261017-1829-taleb-75d6
RUN() { echo "+ $*" >&2; "$@"; }

RUN cargo build --release -p emergent-universe --example stagger_legality
RUN cargo build --release -p emergent-universe --example frame_digest

# The six arms (CSVs; stderr keeps the settle/digest progress). The ref s1 run is ~80 s (2x kicks
# to two belt orbits): the one command over the 60-s norm, disclosed in the dossier.
RUN env timeout 60 cargo run --release -p emergent-universe --example stagger_legality -- off 1 128 1,2 > "$R/off_s1.csv" 2> "$R/off_s1.err"
RUN env ES_STAGGER=1 timeout 60 cargo run --release -p emergent-universe --example stagger_legality -- on 1 128 1,2 > "$R/on_s1.csv" 2> "$R/on_s1.err"
RUN env timeout 60 cargo run --release -p emergent-universe --example stagger_legality -- off 2 128 2 > "$R/off_s2.csv" 2> "$R/off_s2.err"
RUN env ES_STAGGER=1 timeout 60 cargo run --release -p emergent-universe --example stagger_legality -- on 2 128 2 > "$R/on_s2.csv" 2> "$R/on_s2.err"
RUN env timeout 100 cargo run --release -p emergent-universe --example stagger_legality -- ref 1 128 1,2 > "$R/ref_s1.csv" 2> "$R/ref_s1.err"
RUN env timeout 70 cargo run --release -p emergent-universe --example stagger_legality -- ref 2 128 1 > "$R/ref_s2.csv" 2> "$R/ref_s2.err"

# C3: the off arm on the patched build is bit-identical to pristine (frame_digest; the timing
# annotations differ, the digests must not). Restore the patch afterwards.
cp crates/universe/src/step.rs /tmp/step_patched.rs.$$
git checkout -- crates/universe/src/step.rs
trap 'cp /tmp/step_patched.rs.$$ crates/universe/src/step.rs' EXIT
RUN env timeout 100 cargo run --release -p emergent-universe --example frame_digest -- 3 2>/dev/null | sed 's/ \[[0-9.]* s\]//' > "$R/fd_pristine.txt"
cp /tmp/step_patched.rs.$$ crates/universe/src/step.rs
RUN env timeout 100 cargo run --release -p emergent-universe --example frame_digest -- 3 2>/dev/null | sed 's/ \[[0-9.]* s\]//' > "$R/fd_patched.txt"
if diff -q "$R/fd_pristine.txt" "$R/fd_patched.txt" >/dev/null; then echo "C3: PRISTINE == PATCHED-OFF (digests identical)" | tee "$R/c3.txt"; else echo "C3: MISMATCH" | tee "$R/c3.txt"; fi

RUN python3 "$R/analyze.py" > "$R/analysis.json"
echo "regen done: $R/analysis.json"
