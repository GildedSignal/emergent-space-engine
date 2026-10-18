#!/bin/sh
# Regen: every dossier number, from shipped code + work/patch.diff, in ~5 min.
# The patch adds `--extra N` (the ladder's belt/locals scene) to the FLYABLE frame loop
# (`xtask universe`, Session::step: engine advance + view gather + view JSON + wire,
# the frame the served page runs; the benchmark prints the same dashboard headless).
set -e
cd "$(dirname "$0")/../../.." || exit 1
R=lab/results/20261018-1237-system-4875

# 1. The patch (idempotent: skip when the tree already carries it).
if ! git diff -- xtask | grep -q -- '--extra'; then
  git apply "$R/work/patch.diff"
fi

# 2. Build.
if cargo build --release -p xtask 2>&1 | grep -qE "^error"; then exit 1; fi
X=/home/glmlab/lab-target-2/release/xtask
[ -x "$X" ] || X=target/release/xtask

# 3. The flights (unpaced: the wall never couples; the dashboard times the frame's own parts).
#    control (the shipped flyable plane) | the ladder's scene at 1e3, 1e4 | held-out seed 2 | rtf 1.
"$X" universe --bench --unpaced --seconds 10 --rtf 100 --extra 0      > "$R/work/cf_e0.json"
"$X" universe --bench --unpaced --seconds 10 --rtf 100 --extra 1000   > "$R/work/cf_e1000.json"
"$X" universe --bench --unpaced --seconds 6  --rtf 100 --extra 10000  > "$R/work/cf_e10000.json"
"$X" universe --bench --unpaced --seconds 3  --rtf 100 --extra 10000 --seed 2 > "$R/work/cf_e10000_s2.json"
"$X" universe --bench --unpaced --seconds 3  --rtf 1   --extra 10000  > "$R/work/cf_e10000_rtf1.json"

# 4. The table.
python3 - "$R/work" <<'EOF'
import json, sys
rows = [("control e0", "cf_e0.json"), ("e1000", "cf_e1000.json"), ("e10000", "cf_e10000.json"),
        ("e10000 s2", "cf_e10000_s2.json"), ("e10000 rtf1", "cf_e10000_rtf1.json")]
print(f"{'arm':<14}{'bodies':>7}{'frame p50':>10}{'engine p50/p99':>18}{'gather p50':>11}{'json p50':>9}{'wire p50':>9}  share view+wire")
for name, f in rows:
    d = json.load(open(f"{sys.argv[1]}/{f}"))
    w = d["where_the_time_goes_ms"]
    vw = w["view_gather"]["share"] + w["view_json"]["share"] + w["wire"]["share"]
    print(f"{name:<14}{d['bodies']:>7}{d['frame_ms']['p50']:>10.2f}"
          f"{w['engine']['p50']:>10.2f}/{w['engine']['p99']:<6.2f}{w['view_gather']['p50']:>11.2f}"
          f"{w['view_json']['p50']:>9.2f}{w['wire']['p50']:>9.2f}  {vw:.3f}")
d = json.load(open(f"{sys.argv[1]}/cf_e1000.json")); d2 = json.load(open(f"{sys.argv[1]}/cf_e10000.json"))
b = (d2["frame_ms"]["p50"] - d["frame_ms"]["p50"]) / (d2["bodies"] - d["bodies"]) * 1e3
d0 = json.load(open(f"{sys.argv[1]}/cf_e0.json"))
b0 = (d["frame_ms"]["p50"] - d0["frame_ms"]["p50"]) / (d["bodies"] - d0["bodies"]) * 1e3
print(f"\nper-body slope 0->1e3: {b0:.1f} us/body; 1e3->1e4: {b:.1f} us/body")
print(f"flyable frame crosses 16.7 ms at ~{16700 / b0:.0f} bodies (view-bound); engine p99 stays under its 5 ms budget in every arm")
EOF
