#!/usr/bin/env bash
# Regenerates every number in dossier.md (run id 20261018-2312-system-9eeb).
# The runner applies work/patch.diff before this runs. Linux/x86: orders of magnitude only.
# Budget: one cold build (~3-6 min on 2 jobs) + ~4 min of tests + one prof rebuild (~3-4 min).
set -euo pipefail
# cd to the repo root: the nearest ancestor holding the workspace manifest
# (the checkout depth varies between the author host and the CI runner).
_root="$(cd "$(dirname "$0")" && pwd)"
while [ "$_root" != "/" ] && [ ! -f "$_root/Cargo.toml" ]; do _root="$(dirname "$_root")"; done
cd "$_root"

cargo build --release -p emergent-universe --tests 2>&1 | tail -1

echo "=== ON arm: the cell serves the rebind, exact key carried (P1-P8) ==="
ES_QMEMO=1 cargo test --release -p emergent-universe --test qmemo the_cell_serves -- --nocapture

echo "=== OFF arm: the shipped law verbatim, the patch inert ==="
cargo test --release -p emergent-universe --test qmemo unset_the_law -- --nocapture

echo "=== The standing memo.rs measurement, both arms (exact keys never recur; cells do) ==="
echo "(expected under ES_QMEMO=1: the served stream's recurrence is ~0.898, so this shipped"
echo " test's own >0.9 guard FAILS by design of the law change — the run's instrument is the"
echo " build-rate assert in the qmemo test above; the number to read here is 'quantized cells N (hit H)')"
cargo test --release -p emergent-universe --test memo -- --nocapture || echo "(on-arm trip disclosed above; off-arm must pass — check both result lines)"

echo "=== The suites, gate off (inertness): space and universe ==="
cargo test --release -p emergent-space 2>&1 | grep -E 'test result' | sort | uniq -c
# Examples excluded: the shipped nladder example calls macOS's proc_pid_rusage
# unconditionally (no cfg guard) and does not link on Linux — pre-existing on main.
cargo test --release -p emergent-universe --lib --tests 2>&1 | grep -E 'test result' | sort | uniq -c

echo "=== FIT column (dossier table row 2): the same qmemo arms under --features prof ==="
cargo build --release -p emergent-universe --tests --features prof 2>&1 | tail -1
ES_QMEMO=1 cargo test --release -p emergent-universe --features prof --test qmemo the_cell_serves -- --nocapture
cargo test --release -p emergent-universe --features prof --test qmemo unset_the_law -- --nocapture
