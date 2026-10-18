#!/bin/sh
# Regen: every dossier number, from shipped code + this run's instruments.
# work/patch.diff (applied by the runner first) adds crates/universe/examples/rigidring.rs;
# this script builds and flies it, then runs the corrected replica tier2.py, then asserts
# the DETERMINISTIC counts only (no wall-clock gates: timings print as information).
# Path-independent: resolves its own folder, works from any starting cwd.
set -e
RUN_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$(git -C "$RUN_DIR" rev-parse --show-toplevel)"
echo "== flight: the shipped capture+answer path on rigid keys rings =="
cargo run --release -p emergent-universe --example rigidring -- 10000 1.0 1 1 536870912 2>&1 | grep -E "ring K|scan|t\+" | tee "$RUN_DIR/flight-regen.log" || true
cargo run --release -p emergent-universe --example rigidring -- 100000 0.1 1 0 536870912 2>&1 | grep -E "ring K|scan" | tee -a "$RUN_DIR/flight-regen.log" || true
echo "== replica: exact law::hit branch structure, soundness sweep + store costs =="
cd "$RUN_DIR"
python3 tier2.py > /dev/null
python3 - <<'EOF'
import json, re
r = json.load(open("tier2.json"))
A, B, C = r["A_soundness"], r["B_rigid_ring"], r["C_store"]
misses = sum(v["selector_misses"] for v in A.values())
assert misses == 0, f"selector misses {misses}: the widened window is unsound"
assert len(A) == 48, "sweep shape changed"
uw = max(v["unwidened_miss_rate_among_hits"] for v in A.values())
assert uw > 0.5, "the unwidened 1D curve must miss most hits (approaching window)"
rk = [v["reads"] / v["hits"] for k, v in A.items() if k.endswith("sa=0_h=P/10")]
assert max(rk) < 7, "keys-class reads stay a few x hits (window both sides vs approaching subset)"
f = open("flight-regen.log").read()
# flown, deterministic (fixed construction, no rng): the counts the dossier quotes
assert "near_set(read list)=32 in_window=32" in f, "K=1e4 rho=1e-5 window must be 32"
assert "ANSWERS=15 (ring 15, contacts 0)" in f, "flown answers at t (interval 2)"
assert "t+536870912: ANSWERS=31" in f and "t+1073741824: ANSWERS=12" in f, "noise swing"
assert "candidates=100009 (ring 99999)" in f, "1.00*K candidates at K=1e5"
assert "near_set(read list)=32 in_window=32" in f, "K=1e5 rho=1e-6 window must be 32"
assert B["h=0.628319"]["near_set"] == 316 and B["h=9"]["near_set"] == 316, "replica near set"
assert B["h=0.628319"]["answers_after_1e12_perturbation"] == 316, "noise-decided answers"
assert 1.0 < C["searchsorted_window_lookup_us"] < 50.0, "lookup must be O(log K) class"
print(f"regen OK: 0 selector misses over 48 cells; max unwidened miss {uw:.1%}; "
      f"lookup {C['searchsorted_window_lookup_us']:.1f} us; "
      f"tier scan {C['tier_scan_s_at_1e6_rho1e-6_uniform']*1e3:.2f} ms vs shipped "
      f"{C['shipped_scan_s_at_1e6_flown_rate']:.1f} s (flown rate)")
EOF
