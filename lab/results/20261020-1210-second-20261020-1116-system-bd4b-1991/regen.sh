#!/bin/sh
# Regen for 20261020-1210-second-20261020-1116-system-bd4b-1991 (second author on bd4b).
# Assumes work/patch.diff is applied (the base census + the span-coverage census; print-only).
# Rebuilds the patched xtask and reruns the measured arms, then prints the dossier's numbers.
set -e
cd "$(dirname "$0")/../../.."   # repo root
BIN="${CARGO_TARGET_DIR:-target}/release/xtask"
OUT="lab/results/20261020-1210-second-20261020-1116-system-bd4b-1991"
cargo build --release -p xtask -p emergent-universe --example nladder
"$BIN" universe --kick-bench --seconds 10                > "$OUT/span_default_seed1.json"
"$BIN" universe --kick-bench --members 400 --seconds 30 --seed 1 > "$OUT/span_m400_seed1.json"
"$BIN" universe --kick-bench --members 400 --seconds 30 --seed 2 > "$OUT/span_m400_seed2.json"
"$BIN" universe --kick-bench --members 400 --seconds 30 --seed 3 > "$OUT/span_m400_seed3.json"
python3 - "$OUT" <<'EOF'
import json, sys
out = sys.argv[1]
# Controls: the print-only census must regenerate the shipped record bit for bit (seed 1).
stored = {"span_default_seed1.json": ("b42da477294f7619", "a693ac68cbc7fb46"),
          "span_m400_seed1.json":     ("8c242b023e8b79e4", "0de3a82c1926a83d")}
for f, (d, r) in stored.items():
    j = json.load(open(f"{out}/{f}"))
    ok = j["digest"].startswith(d) and j["replay_digest"].startswith(r) and j["refused"] == 0
    print(f"[control] {f}: digest {j['digest'][:16]} replay {j['replay_digest'][:16]} refused {j['refused']} -> {'PASS' if ok else 'FAIL'}")
for f in ("span_m400_seed1.json", "span_m400_seed2.json", "span_m400_seed3.json"):
    j = json.load(open(f"{out}/{f}")); sp = j["span"]
    print(f"\n[{f}] seed {j['seed']} samples {j['samples']} digest {j['digest'][:16]} refused {j['refused']}")
    print("  plan_control ok/bad", sp["plan_control_ok"], sp["plan_control_bad"], "unopened", sp["span_rows_unopened"])
    for k in ("made_cycle", "member_cycle", "member_passage"):
        s = sp[k]
        if s["n"] == 0:
            print(f"  {k}: n=0"); continue
        print(f"  {k}: n {s['n']} t1_est {s['t1_estimated']} knots_med {s['knots_med']} "
              f"coverage p25/med {s['coverage_p25']:.6f}/{s['coverage_med']:.5f} max {s['coverage_max']:.4f} "
              f"never_read med {s['never_read_med']} share_total {s['never_read_share_total']:.3f} "
              f"release_capped {s['release_capped']} overhang_med {s['release_overhang_med']:.5f}")
    print("  tail rows:", [(t["pop"], t["kind"], t["knots"], t["never_read"], f"{t['coverage']:.2e}") for t in sp["tail_rows"][:3]])
j = json.load(open(f"{out}/span_m400_seed1.json"))
m = j["mint_leavers"]
print(f"\noriginal census fields regenerate: mints {m['mints']} kinds {m['kinds_cycle_passage_plunge']} heap/mint {m['heap_bytes_total']//m['mints']} B")
EOF
