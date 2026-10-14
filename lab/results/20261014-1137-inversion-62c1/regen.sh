#!/bin/sh
# Regen: every number in dossier.md, from the shipped tree + work/patch.diff (this run's probe).
# The probe (crates/universe/examples/flyframe.rs) flies the page's own frame (engine 5 ms budget ->
# gather_cached -> view_json replica -> serde_json::to_vec, xtask/src/universe/session.rs Session::step)
# on the N ladder's scenes (scenario::plane_extra, the gate N1 population), and counts what the page
cd "$(dirname "$0")/../../.."
# Total: four runs, ~4 minutes on a quiet 8-core box (10^5 dominates: ~2.5 s/frame x 48 frames).
set -e
[ -f lab/results/20261014-1137-inversion-62c1/work/patch.diff ] && git apply lab/results/20261014-1137-inversion-62c1/work/patch.diff || true
cargo run --release -p emergent-universe --example flyframe -- 0 240 100
cargo run --release -p emergent-universe --example flyframe -- 1000 480 100
cargo run --release -p emergent-universe --example flyframe -- 10000 240 100
cargo run --release -p emergent-universe --example flyframe -- 100000 48 100
