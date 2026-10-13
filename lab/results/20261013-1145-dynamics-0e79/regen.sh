#!/bin/sh
# Regenerates every number in dossier.md: rebuilds the probe (added by work/patch.diff,
# or restored from this folder) and reruns the full grid at the same horizon, 2^35.
# Wall ~6 min on the shared 8-vCPU runner; every physics column is deterministic
# (settle-based flights, fixed 2^24 check quantum, seed 1), so a rerun reproduces
# grid.txt's rows bit for bit apart from the [..s wall] field.
set -e
cd "$(dirname "$0")/../../.."
[ -f crates/universe/examples/pump_probe.rs ] || cp lab/results/20261013-1145-dynamics-0e79/pump_probe.rs crates/universe/examples/pump_probe.rs
cargo build --release -p emergent-universe --example pump_probe
R=lab/results/20261013-1145-dynamics-0e79
"${CARGO_TARGET_DIR:-target}/release/examples/pump_probe" 35 | tee "$R/grid-regen.txt" 2> "$R/traces-regen.txt"
echo "--- diff against the run's grid (wall fields must differ, physics columns must not):"
# strip the wall-time bracket for the comparison
sed 's/ \[[0-9.]*s wall.*\]$//' "$R/grid-regen.txt" > /tmp/a.$$; sed 's/ \[[0-9.]*s wall.*\]$//' "$R/grid.txt" > /tmp/b.$$
diff /tmp/b.$$ /tmp/a.$$ && echo "IDENTICAL (physics columns)" || echo "DIFFERS — inspect above"
rm -f /tmp/a.$$ /tmp/b.$$
