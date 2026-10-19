#!/bin/bash
# Regen: rebuilds the harness, reflies every arm of the dossier, reanalyses.
# Runtime ~4 min on the lab box (build ~1 min, 38 flights ~2.5 min, analysis seconds).
set -eu
cd "$(dirname "$0")/../../.."   # repo root
ROOT=$(pwd)
cd "$ROOT"
cargo build --release --example fleetburst -p emergent-lattice 2>&1 | tail -1
BIN=$(cargo metadata --no-deps --format-version 1 | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/examples/fleetburst
cd "$ROOT/lab/results/20261019-0325-taleb-90b7"
rm -f work/*.tsv work/analysis.json work/table.txt

# 1. main grid: n x {aligned, sigma ladder, thermal} (run_grid.sh, uses $BIN)
BIN=$BIN ./run_grid.sh

# 2. probes: axis decomposition, jitter-only, long horizons
for s in 1 2; do
  $BIN --scene head --n 1600 --sigma 4096  --nojitter --horizon 4096 --seed $s --out work/nj_n1600_sig4096_s${s}.tsv 2>/dev/null &
  $BIN --scene head --n 1600 --sigma 65536 --nojitter --horizon 4096 --seed $s --out work/nj_n1600_sig65536_s${s}.tsv 2>/dev/null &
  $BIN --scene head --n 1600 --sx 4096  --sy 0 --nojitter --horizon 4096 --seed $s --out work/ax_n1600_sx4096_sy0_s${s}.tsv 2>/dev/null &
  $BIN --scene head --n 1600 --sx 0     --sy 4096 --horizon 4096 --seed $s --out work/ax_n1600_sx0_sy4096_s${s}.tsv 2>/dev/null &
  $BIN --scene head --n 1600 --sx 0     --sy 4096 --horizon 4096 --seed $s --out work/ax_n1600_sx0_sy4096_jit_s${s}.tsv 2>/dev/null &
  $BIN --scene head --n 1600 --sx 65536 --sy 0 --nojitter --horizon 4096 --seed $s --out work/ax_n1600_sx65536_sy0_s${s}.tsv 2>/dev/null &
  $BIN --scene head --n 1600 --horizon 4096 --seed $s --out work/jit_n1600_sig0_s${s}.tsv 2>/dev/null &
done
$BIN --scene head --n 1600 --sigma 4096 --horizon 8192 --seed 1 --out work/head_n1600_sig4096_H8192_s1.tsv 2>/dev/null &
$BIN --scene head --n 400  --sigma 4096 --horizon 4096 --seed 1 --out work/head_n400_sig4096_H4096_s1.tsv 2>/dev/null &
$BIN --scene head --n 6400 --sx 4096 --sy 0 --nojitter --horizon 8192 --seed 1 --out work/ax_n6400_sx4096_sy0_s1.tsv 2>/dev/null &
wait

# 3. analysis
python3 analyze.py > work/table.txt
python3 - <<'EOF'
import json, collections
res = json.load(open('work/analysis.json'))
def arm(r):
    if r['scene'] == 'thermal': return 'thermal'
    if r['aligned'] == 'true': return 'aligned (sx=sy=0, no jit)'
    j = 'jit' if r['jitter'] == 'true' else 'col'
    return f"sx={r['sx']:>6},sy={r['sy']:>6},{j}"
g = collections.defaultdict(list)
for r in res: g[(r['n'], arm(r), r['verdict'])].append(r)
print(f"{'n':>5} {'arm':30} {'k':>2} {'maxc/n':>7} {'maxW/ml':>7} {'F64L':>8} {'conc':>5} {'exc/n':>7} {'w/ex':>5}")
for k in sorted(g, key=str):
    rs = g[k]
    print(f"{k[0]:>5} {k[1]:30} {len(rs):>2} {max(r['maxc_per_n'] for r in rs):>7.3f} "
          f"{max(r['maxW_over_meanlate'] for r in rs):>7.2f} {max(r['F64_late'] for r in rs):>8.1f} "
          f"{max(r['concentration'] for r in rs):>5.1f} {max(r['excess_per_n'] for r in rs):>7.2f} "
          f"{max(r['width_over_extent'] or 0 for r in rs):>5.2f}")
EOF
echo REGEN_OK
