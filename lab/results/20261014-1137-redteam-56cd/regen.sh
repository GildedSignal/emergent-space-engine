#!/bin/sh
# 20261014-1137-redteam-56cd — regenerates every number in dossier.md.
# The runner applies work/patch.diff (Battle::burn, Battle::last_anchor_refusal,
# examples/rt_fleet_thrust.rs) before this runs. Wall time ~25 s.
set -e
cd "$(dirname "$0")/../../.."
cargo build --release -p emergent-engine --example rt_fleet_thrust 2>&1 | tail -2
timeout 300 cargo run --release -p emergent-engine --example rt_fleet_thrust \
  | tee lab/results/20261014-1137-redteam-56cd/fleet-thrust.txt
echo "--- controls ---"
# A0 must sit in the shipped class (max_shape < 1%: the reanchor test's own bar) and
# A2's refusal reason must name the unbound orbit. Both checked by eye from the log above.
grep -q "ARM A0" lab/results/20261014-1137-redteam-56cd/fleet-thrust.txt
grep -q "not on a bound orbit" lab/results/20261014-1137-redteam-56cd/fleet-thrust.txt && echo "refusal reason present"
