#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff.
# Total wall: ~4 min (build ~25 s + three flights ~90 s + arithmetic).
set -euo pipefail
cd "$(dirname "$0")/../../.."
RUN=lab/results/20261021-1443-fermi-d709
OUT=$RUN/out
# Idempotent: apply only when the tree does not already carry the instrument.
if ! grep -q "ship_boundary_ns" crates/universe/src/universe.rs; then
  git apply "$RUN/work/patch.diff"
fi
cargo build --release -p emergent-universe --example brow
BROW=${CARGO_TARGET_DIR:-target}/release/examples/brow
# The three flights of the record (each ≤ 60 s): 3e4 s1, 1e5 s1, 1e5 s2 (held-out seed).
for spec in "30000 7000 12 1" "100000 7000 12 1" "100000 7000 12 2"; do
  set -- $spec
  echo "== brow $1 $2 $3 $4"
  "$BROW" "$1" "$2" "$3" "$4" | tee "$OUT/brow-n$1-s$4.txt"
done
# Steady-window composition (era-clean, chunks 4..12): the dossier's belt-law rows.
python3 - "$OUT" <<'EOF'
import sys, re
out = sys.argv[1]
print("steady window (gs 33k..89k, two full clock periods), per rung:")
for f in ["brow-n30000-s1.txt", "brow-n100000-s1.txt", "brow-n100000-s2.txt"]:
    ks, bs = [], []
    k4 = b4 = kn = bn = None
    for line in open(f"{out}/{f}"):
        m = re.search(r"chunk\s+(\d+):.*kicks\s+(\d+) .*boundaries\s+(\d+) ", line)
        if m:
            c, k, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
            if c == 4: k4, b4 = k, b
            kn, bn = k, b
    gs, bodies = 56000.0, {"n30000": 30028, "n100000": 100028}[f.split("-")[1]]
    rk, rb = (kn - k4) / bodies / gs, (bn - b4) / bodies / gs
    row = lambda r, u: r * 1e9 * 100 * u * 1e-6
    # costs from the totals line of the same flight
    t = open(f"{out}/{f}").read()
    uk = float(re.search(r"us_kick ([\d.]+)", t).group(1))
    ub = float(re.search(r"us_boundary ([\d.]+)", t).group(1))
    print(f"{f}: rate_k {rk:.3e} rate_b {rb:.3e} b/k {rb/rk:.3f} | kick {row(rk, uk):.1f} + boundary {row(rb, ub):.1f} = {row(rk, uk)+row(rb, ub):.1f} cores @1e9 rtf100 | split8 {row(rk, uk)/4.92:.1f}+{row(rb, ub)/4.92:.1f}={row(rk,uk)/4.92+row(rb,ub)/4.92:.1f} (M1 x0.58: {row(rk,uk)*0.58/4.92:.1f}+{row(rb,ub)*0.58/4.92:.1f}={row(rk,uk)*0.58/4.92+row(rb,ub)*0.58/4.92:.1f})")
    print(f"  boundary share: today {ub*rb/(ub*rb+uk*rk):.3f} | at the 4.9us kick bar {ub/(ub+4.92):.3f} | bar halves to {4.92/2:.2f} us/event if the comb is kept")
EOF
