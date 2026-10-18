#!/bin/bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff (applied by the runner
# before this runs). Wall ~2-3 min on the lab box (build cached: ~10 s; flights: ~90 s total).
set -e
cd "$(dirname "$0")/../../.."   # repo root
R="lab/results/20261018-1717-inversion-d839/raw"
mkdir -p "$R"
cargo build --release -p emergent-universe --example nladder --example belt_first
run() { LADDER_CAP_S=280 cargo run --release -p emergent-universe --example nladder -- "$@"; }
# The wave map (first planned items), then the flights: control, one step, one step + second kick wave.
cargo run --release -p emergent-universe --example belt_first -- 30000 | tee "$R/belt_first_30000.txt"
run 0      coast 360 100 | tee "$R/n0_coast_360s.log"
run 30000  coast 360 100 | tee "$R/n30000_coast_360s.log"
run 30000  coast 456 100 | tee "$R/n30000_coast_456s.log"
run 100000 coast 360 100 | tee "$R/n100000_coast_360s.log"
run 100000 coast 456 100 | tee "$R/n100000_coast_456s.log"
# Determinism arm: the counters must reproduce exactly.
run 30000  coast 456 100 | tee "$R/n30000_coast_456s_rerun.log"
# The analysis table the dossier quotes.
python3 - <<'EOF'
import re, glob
base = "lab/results/20261018-1717-inversion-d839/raw"
for name in ["n0_coast_360s.log","n30000_coast_360s.log","n30000_coast_456s.log",
             "n100000_coast_360s.log","n100000_coast_456s.log","n30000_coast_456s_rerun.log"]:
    rows=[]
    for line in open(f"{base}/{name}"):
        m=re.match(r"probe: f=(\d+) gs=(\S+) rss_mb=(\S+) hwm_mb=(\S+) bpb=(\d+) cat=(\d+) held=(\d+) kicks=(\d+) events=(\d+)",line)
        if m: rows.append((float(m[2]),float(m[3]),int(m[5]),int(m[6]),int(m[7]),int(m[8]),int(m[9])))
    waves=[]; prev=None
    for r in rows:
        if prev and r[5]-prev[5]>4000: waves.append((prev[0],r[0],r[5]-prev[5]))
        prev=r
    lad=[l for l in open(f"{base}/{name}") if l.startswith("ladder:")][0]
    g=[l for l in open(f"{base}/{name}") if l.startswith("game ")][0]
    kv=dict(re.findall(r"(\w+)=(\S+)",lad))
    ks=re.search(r"kicks (\d+)",g).group(1); bd=re.search(r"boundaries (\d+)",g).group(1)
    print(f"{name}: gs={rows[-1][0]:.0f} rss_end={kv['foot_end_mb']}MB over={kv['over']} max={kv['max_ms']}ms "
          f"kicks={ks} boundaries={bd} cat_end={rows[-1][3]} bpb_end={rows[-1][2]} waves={waves}")
EOF
