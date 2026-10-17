#!/bin/bash
# Regen for 20261017-1829-second-...-e517 (second author on fd35): rebuilds the
# instrument (fd35's HAZ/PRE/RB/FIRE + e517's RB `out=` sibling-closure field) and
# fd35's race.rs + 01e7's finpol.rs from work/patch.diff, then regenerates every
# dossier number: the firing sweep (positive side, P5), the equality-law churn arms
# and the corrected armed-episode arm (sab x -> None; fd35's regen bug), all
# analysed from the repo root (fd35's relative-path bug). ~4 min on 8 vCPU.
#
# Fires are wall-clock raced (bc0f): each firing seed gets up to 3 attempts; the
# per-seed panic values are stable, only incidence moves with load.
set -u
cd "$(git rev-parse --show-toplevel)"   # repo root; analyze.py is invoked by absolute path below
R=$(cd "$(dirname "$0")" && pwd)

# 1. clean tree, then the print-only instrument + the two example drivers
git checkout -- crates/allocator/src/alloc.rs 2>/dev/null || true
rm -f crates/allocator/examples/race.rs crates/allocator/examples/finpol.rs
git apply "$R/work/patch.diff"
cargo build -p emergent-allocator --release --offline --examples 2>&1 | grep -E '^error' && exit 1
BIN="$CARGO_TARGET_DIR/release/examples"
FIN="$BIN/finpol"; RAC="$BIN/race"

# 2. the firing sweep: 4 seeds that fired 2/2 in the window's sweep (retry x3: raced),
#    2 draws of never-fired seeds (armed survivors), one 1-of-2 seed as-is
S="$R/regen/sweep"; mkdir -p "$S"
for s in 11 13 15 16; do
  for try in 1 2 3; do
    timeout 15 "$FIN" selfchurn frames 120 6 128 600 2 $s > "$S/f_s$s.out" 2> "$S/f_s$s.err"
    [ $? -eq 101 ] && break
  done
done
for s in 12 17 14; do timeout 15 "$FIN" selfchurn frames 120 6 128 600 2 $s > "$S/f_s$s.out" 2> "$S/f_s$s.err"; done

# 3. the state-side arms on the race harness: the corrected armed-episode probe
#    (sab 'x' parses to None — fd35's `sab 0` mapped to Some(1)) and two churn arms
A="$R/regen/racearms"; mkdir -p "$A"
timeout 60 "$RAC" 400 11 1 900 2 16 8 128 60 x 0.3 > "$A/h_nosab.out" 2> "$A/h_nosab.err"
timeout 60 "$RAC" 3000 11 1 2400 4 16 8  64 40 3 1.0 > "$A/m_churn_11.out" 2> "$A/m_churn_11.err"
timeout 60 "$RAC" 3000 15 1 2400 4 16 8  64 40 3 1.0 > "$A/m_churn_15.out" 2> "$A/m_churn_15.err"

# 4. the dossier numbers (from the repo root; $R absolute — no cd into regen/)
python3 "$R/analyze2.py" "$S" | tee "$R/regen/sweep-summary.txt"
python3 - "$A" <<'EOF' | tee "$R/regen/racearms-summary.txt"
import re, sys
from pathlib import Path
for p in sorted(Path(sys.argv[1]).glob('*.err')):
    txt = p.read_text(errors='replace')
    D = [int(m.group(1)) for m in re.finditer(r'D=Some\(\((-?\d+), ', txt)]
    M = [int(m) for m in re.findall(r' m=(-?\d+) out=', txt)]
    A = [int(m) for m in re.findall(r' A=(-?\d+)', txt)]
    out = len(re.findall(r'out=\[\(', txt))
    fires = txt.count('\nFIRE ') + txt.startswith('FIRE ')
    print(f"{p.stem}: clashes={len(D)} minD={min(D) if D else None} maxD={max(D) if D else None} "
          f"rb={len(M)} maxm={max(M) if M else None} out_open={out} fires={fires} "
          f"posA={sum(1 for a in A if a > 0)} maxA={max(A) if A else None}")
EOF
echo "regen done"
