#!/bin/sh
# 1b3f: regenerate every dossier number. Assumes work/patch.diff is applied (the runner applies
# it before this runs): the per-reader `oldest` (env-gated, off = shipped bit for bit) plus
# 4a71's probe verbatim (the Linux /proc footprint, ES_WALL_CAP_S / ES_PROBE_EVERY_GS, the
# census/gap probe lines) in crates/universe/examples/nladder.rs and crates/universe/src/universe.rs.
# ~11 min cold, sequential.
set -e
cd "$(dirname "$0")/../../.."   # repo root
HERE=lab/results/20261019-0435-second-20261019-0325-library-9147-1b3f

# A private target dir: the family default (lab-target-2) is shared with the window's other
# runs and its binaries get clobbered mid-flight (this run lost its first grid to that).
export CARGO_TARGET_DIR=${CARGO_TARGET_DIR:-$HOME/lab-target-1b3f}
cargo build --release --offline -p emergent-universe --example nladder --example ladder_digest
BIN=$CARGO_TARGET_DIR/release/examples/nladder

sh "$HERE/flights.sh"

python3 "$HERE/analyze.py" | tee "$HERE/work/analyze_out.txt"

# The soundness gate: the frozen 13-case ladder_digest suite, flag off vs on, timings stripped —
# the two outputs must be byte-identical.
DG=$CARGO_TARGET_DIR/release/examples/ladder_digest
"$DG" 2>&1 | sed 's/ *\[[0-9.]* s\]//' > "$HERE/work/digest-off.txt"
ES_READER_OLDEST=1 "$DG" 2>&1 | sed 's/ *\[[0-9.]* s\]//' > "$HERE/work/digest-on.txt"
if diff -q "$HERE/work/digest-off.txt" "$HERE/work/digest-on.txt" >/dev/null; then
    echo "digest: 13 cases x 4 schedules BIT-IDENTICAL with ES_READER_OLDEST on"
else
    echo "digest: MOVED (see work/digest-*.txt)"
    diff "$HERE/work/digest-off.txt" "$HERE/work/digest-on.txt" | head -20
fi
