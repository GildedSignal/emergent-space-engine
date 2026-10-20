#!/bin/sh
# Regen for 20261020-1116-system-bd4b. Assumes work/patch.diff is applied.
# Rebuilds the patched xtask (print-only census) and reruns the measured arms.
set -e
cd "$(dirname "$0")/../../.."   # repo root
BIN="${CARGO_TARGET_DIR:-target}/release/xtask"
OUT="lab/results/20261020-1116-system-bd4b"
cargo build --release -p xtask -p emergent-universe --example nladder
"$BIN" universe --kick-bench --seconds 10 > "$OUT/kick_census_default.json"
"$BIN" universe --kick-bench --members 400 --seconds 30 > "$OUT/kick_census_m400.json"
"$BIN" universe --kick-bench --members 400 --seconds 30 > "$OUT/kick_census_m400_run2.json"
python3 - <<'EOF'
import json
o = "lab/results/20261020-1116-system-bd4b"
a = json.load(open(f"{o}/kick_census_m400.json")); b = json.load(open(f"{o}/kick_census_m400_run2.json"))
d = json.load(open(f"{o}/kick_census_default.json"))
print("control digests identical:", a["digest"] == b["digest"] and a["replay_digest"] == b["replay_digest"])
for name, j in (("default", d), ("m400", a)):
    print(f"[{name}] digest {j['digest'][:16]} replay {j['replay_digest'][:16]} refused {j['refused']} samples {j['samples']}")
    for k in ("mint_made", "mint_leavers"):
        m = j[k]
        keep = ("mints","kinds_cycle_passage_plunge","knots_min","knots_med","knots_p75","knots_max",
                "knots_share_of_heap","spearman_us_knots","heap_bytes_total")
        print(" ", k, {x: m[x] for x in keep})
        print("   terciles", m["median_us_by_knot_tercile"])
        if m["mints"]:
            print("   heap/mint = %.0f B" % (m["heap_bytes_total"]/m["mints"]))
EOF
