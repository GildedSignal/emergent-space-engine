#!/usr/bin/env bash
# Regenenerates every number in dossier.md from shipped code + this run's patch (work/patch.diff,
# applied by the runner before this runs). Linux/x86: orders of magnitude only.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
B="${CARGO_TARGET_DIR:-/home/glmlab/lab-target-3}/release/xtask"
R="lab/results/20261018-0932-system-0d46/work"
mkdir -p "$R"
cargo build --release -p xtask
# The crowd arm (28 locals + a 400-member fleet, the shipped CLI's crowd clamp) and the control.
"$B" universe --bench --seed 1 --rtf 100 --seconds 30 --members 400 --threads 1 > "$R/arm400.log" 2>&1
"$B" universe --bench --seed 1 --rtf 100 --seconds 30 --members 4   --threads 1 > "$R/ctl4.log" 2>&1
# The dossier's derived table.
python3 - <<'EOF'
import re, statistics as st
for name in ("arm400", "ctl4"):
    rows = []
    per = []
    for line in open(f"lab/results/20261018-0932-system-0d46/work/{name}.log"):
        if "WALKPROBE" in line:
            d = dict(re.findall(r"(\w+)=(\d+)", line))
            rows.append({k: int(v) for k, v in d.items()})
    g = [r["ok_ns"]/60/1e3 for r in rows]           # gather ms per frame
    b = rows[-1]["bodies"] if rows else 0
    caps = sum(r["captures"] for r in rows); cands = sum(r["cands"] for r in rows)
    cap = sum(r["cap_ns"] for r in rows); anss = sum(r["answers"] for r in rows)
    ac = sum(r["ans_cands"] for r in rows); ans = sum(r["ans_ns"] for r in rows)
    print(f"{name}: probe_windows={len(rows)} bodies={b} gather_ms_per_frame "
          f"p50={st.median(g):.2f} max={max(g):.2f} | us_per_body={st.median(g)*1e3/max(b,1):.2f} | "
          f"captures={caps} cands_per_capture={cands/max(caps,1):.0f} cap_us_per_cand={cap/max(cands,1)/1e3:.2f} | "
          f"answers={anss} ans_cands_per_answer={ac/max(anss,1):.0f} ans_us_per_cand={ans/max(ac,1)/1e3:.2f}")
EOF
grep -E '"view_gather"|"engine"' "$R/arm400.log" | tail -1
