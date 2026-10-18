#!/bin/sh
# Regen: every dossier number, from shipped code + work/patch.diff (this run's wiring:
# the original --extra knob + 2df1's gather_rows + the row-set policy wired into
# Session::step behind --rows), in ~6 min.
set -e
cd "$(dirname "$0")/../../.." || exit 1
R=lab/results/20261018-1433-second-20261018-1237-system-4875-4143
W="$R/work"

# 1. The patch (idempotent: skip what the tree already carries).
if ! git diff -- xtask | grep -q -- '--rows-audit'; then
  git apply "$W/extra.patch"
  git apply --exclude=crates/universe/examples/flyframe2.rs "$W/gather-rows.patch"
  git apply "$W/rowset-wiring.patch"
fi

# 2. Build.
if ! cargo build --release -p xtask 2>&1 | grep -qE "^error"; then :; else exit 1; fi
X=/home/glmlab/lab-target-0/release/xtask
[ -x "$X" ] || X=target/release/xtask

# 3. The flights. Baselines (rows off) reproduce the first author's arms; --rows arms
#    fly the same matrix with the deletion wired in; a* arms add the audit; r10000s2
#    is the held-out seed; r30000 the held-out decade.
"$X" universe --bench --unpaced --seconds 10 --rtf 100 --extra 0     > "$W/b0.json"
"$X" universe --bench --unpaced --seconds 10 --rtf 100 --extra 1000  > "$W/b1000.json"
"$X" universe --bench --unpaced --seconds 6  --rtf 100 --extra 10000 > "$W/b10000.json"
"$X" universe --bench --unpaced --seconds 10 --rtf 100 --extra 0     --rows > "$W/r0.json"
"$X" universe --bench --unpaced --seconds 10 --rtf 100 --extra 1000  --rows > "$W/r1000.json"
"$X" universe --bench --unpaced --seconds 6  --rtf 100 --extra 10000 --rows > "$W/r10000.json"
"$X" universe --bench --unpaced --seconds 3  --rtf 100 --extra 30000 --rows > "$W/r30000.json"
"$X" universe --bench --unpaced --seconds 3  --rtf 100 --extra 10000 --rows --seed 2 > "$W/r10000s2.json"
"$X" universe --bench --unpaced --seconds 6  --rtf 100 --extra 1000  --rows --rows-audit 10 > "$W/a1000.json"
"$X" universe --bench --unpaced --seconds 6  --rtf 100 --extra 10000 --rows --rows-audit 30 > "$W/a10000.json"

# 4. The table.
python3 - "$W" <<'EOF'
import json, sys
w = sys.argv[1]
def load(n): return json.load(open(f"{w}/{n}.json"))
rows = [("b0","b0.json",0),("b1000","b1000.json",0),("b10000","b10000.json",0),
        ("r0","r0.json",1),("r1000","r1000.json",1),("r10000","r10000.json",1),
        ("r30000","r30000.json",1),("r10000s2","r10000s2.json",1)]
print(f"{'arm':<10}{'bodies':>7}{'frame p50':>10}{'p99':>8}{'over16.7':>9}{'eng p50/p99':>14}{'gather':>8}{'json':>7}{'wire':>7}  vw share   served  readouts  wireKB  fill_ms")
for name, f, is_rows in rows:
    d = load(name); t = d["where_the_time_goes_ms"]
    vw = t["view_gather"]["share"] + t["view_json"]["share"] + t["wire"]["share"]
    rs = d.get("rowset") or {}
    over = sum(d["hitch_counts"][:1]) if isinstance(d["hitch_counts"], list) else "?"
    print(f"{name:<10}{d['bodies']:>7}{d['frame_ms']['p50']:>10.2f}{d['frame_ms']['p99']:>8.2f}{str(over):>9}"
          f"{t['engine']['p50']:>8.2f}/{t['engine']['p99']:<5.2f}{t['view_gather']['p50']:>8.2f}{t['view_json']['p50']:>7.2f}{t['wire']['p50']:>7.2f}  {vw:.3f}"
          f"  {rs.get('served_per_frame',0):>6.0f}  {rs.get('readouts_per_frame',0):>8.0f}  {rs.get('wire_kb_median',0):>6.1f}  {rs.get('fill_ms',0):>6.1f}")
for name in ["a1000", "a10000"]:
    d = load(name); a = d["rowset"]["audit"]
    print(f"{name}: audit frames {a['frames']}, drawn {a['drawn_rows']}, viol px/miss/ghost/panel {a['viol_px']}/{a['viol_miss']}/{a['viol_ghost']}/{a['viol_panel']}"
          f" -> {a['viol_share']*100:.2f}% of drawn rows; frame p50 {d['frame_ms']['p50']:.2f} ms")
d1, d2 = load("b1000"), load("r1000")
print(f"\ncollapse at 1e3: {d1['frame_ms']['p50']:.1f} -> {d2['frame_ms']['p50']:.2f} ms ({d1['frame_ms']['p50']/d2['frame_ms']['p50']:.0f}x)")
d1, d2 = load("b10000"), load("r10000")
print(f"collapse at 1e4: {d1['frame_ms']['p50']:.1f} -> {d2['frame_ms']['p50']:.2f} ms ({d1['frame_ms']['p50']/d2['frame_ms']['p50']:.0f}x)")
b, r = load("b10000"), load("r10000")
print(f"engine digest at equal cut: baseline {b['digest'][:16]} rows {r['digest'][:16]} identical={b['digest']==r['digest']}")
EOF
