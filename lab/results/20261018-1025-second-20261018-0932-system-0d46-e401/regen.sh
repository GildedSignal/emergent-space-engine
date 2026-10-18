#!/usr/bin/env bash
# Regen: every dossier number, from shipped code + work/patch.diff (applied by the runner before
# this runs). Linux/x86 shared box: orders of magnitude only. ~4 min.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
B="${CARGO_TARGET_DIR:-/home/glmlab/lab-target-3}/release/xtask"
E="${CARGO_TARGET_DIR:-/home/glmlab/lab-target-3}/release/examples/phasegather"
R="lab/results/20261018-1025-second-20261018-0932-system-0d46-e401/work"
mkdir -p "$R"
cargo build --release -p xtask
cargo build --release -p emergent-universe --example phasegather

echo "== arm A: the shipped bench crowd (400 members, 428 bodies; 0d46's scene) =="
"$B" universe --bench --seed 1 --rtf 100 --seconds 30 --members 400 --threads 1 > "$R/arm400.log" 2>&1 || true
echo "== control: --members 4 (32 bodies) =="
"$B" universe --bench --seed 1 --rtf 100 --seconds 10 --members 4 --threads 1 > "$R/ctl4.log" 2>&1 || true
echo "== arm B: the formation (one shared compiled key, K=4000, e=2^-48) =="
"$E" 4000 240 100 > "$R/ring4000.log" 2>&1 || true
echo "== arm B2: the same, smaller (K=1000) =="
"$E" 1000 240 100 > "$R/ring1000.log" 2>&1 || true

python3 - "$R" <<'EOF'
import re, sys, statistics as st
R = sys.argv[1]
def rows(name):
    out = []
    for line in open(f"{R}/{name}.log", errors="ignore"):
        if "TIERPROBE" in line:
            out.append(dict(re.findall(r"(\w+)=(\S+)", line)))
    return out
def num(d, k, f=float):
    return f(d[k]) if k in d else 0
for name in ("arm400", "ctl4", "ring4000", "ring1000"):
    rs = rows(name)
    if not rs:
        print(f"{name}: NO PROBE OUTPUT"); continue
    bodies = num(rs[-1], "bodies", int)
    # steady windows: skip the first (the pre-step regime) for the in-flight law
    steady = rs[1:]
    def med(k, sel=None):
        v = [num(r, k) for r in (sel if sel is not None else rs)]
        return st.median(v) if v else 0.0
    cross = med("cross_ms"); row = med("row_ms"); loop = med("loop_ms")
    ship_us = (cross + row) * 1e3 / max(bodies, 1)
    tier_us = med("tier_ms") * 1e3 / max(bodies, 1)
    solve_us = med("solve_ms") * 1e3 / max(bodies, 1)
    trow_us = med("trow_ms") * 1e3 / max(bodies, 1)
    g = lambda k: sum(num(r, k, int) for r in rs)
    # the te histogram prints as one token te=0:N/1:N/2+:N
    te0 = te1 = te2 = 0
    for r in rs:
        m = re.match(r"0:(\d+)/1:(\d+)/2\+:(\d+)", r.get("te", ""))
        if m:
            te0, te1, te2 = te0 + int(m.group(1)), te1 + int(m.group(2)), te2 + int(m.group(3))
    n = len(rs) * 60
    print(f"{name}: windows={len(rs)} bodies={bodies} | ship us/body={ship_us:.2f} (cross {cross:.2f} ms, row {row:.2f} ms, share {cross/max(loop,1e-9):.2f}) | tier us/body={tier_us:.3f} (solve {solve_us:.3f}, row {trow_us:.3f}) -> walk x{ship_us/max(tier_us,1e-12):.0f} | census us/body={med('census_ms')*1e3/max(bodies,1):.2f} | groups/gather={g('groups')/max(n,1):.1f} gmax={max(num(r,'gmax',int) for r in rs)} eligible/gather={g('eligible')/max(n,1):.0f} tiered/gather={g('tiered')/max(n,1):.0f} kick_inel/gather={g('kick_inel')/max(n,1):.0f} rebound/gather={g('rebound')/max(n,1):.0f} solve_fail/gather={g('solve_fail')/max(n,1):.0f}")
    print(f"    audit(all windows): audited={g('audited')} px_viol={g('px_viol')} panel_viol={g('panel_viol')} te0={te0} te1={te1} te2={te2} max_dth_px={max(num(r,'max_dth_px') for r in rs):.3f} max_dls_tol={max(num(r,'max_dls_tol') for r in rs):.2e} max_dshift_tol={max(num(r,'max_dshift_tol') for r in rs):.2e} max_dclosing_tol={max(num(r,'max_dclosing_tol') for r in rs):.2e} exact_keys_last={num(rs[-1],'exact_keys',int)}")
EOF
echo "== the bench crowd's key spread at coarser quantization (the domain probe) =="
for q in 8 5 3; do
  PHASE_QBITS=$q "$B" universe --bench --seed 1 --rtf 100 --seconds 6 --members 400 --threads 1 2>/dev/null | grep TIERPROBE | tail -1 | grep -oE "groups=[0-9]+ gmax=[0-9]+ eligible=[0-9]+" | sed "s/^/QBITS=$q /" | tee -a "$R/qbits.log"
done
grep -E '"view_gather"|"bodies"' "$R/arm400.log" | tail -2 || true
