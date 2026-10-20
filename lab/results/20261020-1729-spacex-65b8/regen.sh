#!/usr/bin/env bash
# Regen for 20261020-1729-spacex-65b8. The runner applies work/patch.diff before this runs.
# Flow: (1) rebuild PRISTINE (patch reversed) and re-verify the two shipped rtf-1 digests,
# (2) re-apply the patch, rebuild, (3) run the four census arms, (4) print the summary table.
# Total ~6 min of builds + <30 s of benches on the lab's 8-core box. Each bench <= 60 s.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
R=${R:-lab/results/20261020-1729-spacex-65b8}
X=$CARGO_TARGET_DIR/release/xtask

echo "== 1. pristine control (digest neutrality against the shipped records) =="
# The frozen patch is expected to be applied (the runner applies it). Reverse it for the
# pristine control; if that fails the tree is already pristine and we simply verify.
git apply -R "$R/work/patch.diff" 2>/dev/null || echo "(tree already pristine)"
cargo build --release -p xtask 2>&1 | tail -1
for arm in "--seconds 10:b42da477294f7619" "--members 400 --seconds 30:8c242b023e8b79e4"; do
  flags=${arm%%:*}; want=${arm##*:}
  got=$($X universe --kick-bench $flags 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['digest'])")
  [ "${got:0:16}" = "$want" ] && echo "pristine $flags -> $got (matches shipped)" || { echo "MISMATCH $flags: ${got:0:16} != $want"; exit 1; }
done
git apply "$R/work/patch.diff"

echo "== 2. patched build =="
cargo build --release -p xtask 2>&1 | tail -1

echo "== 3. census arms =="
cd "$R"
mkdir -p out
CENSUS_CSV=out/default-s1.csv       $X universe --kick-bench --seconds 10 > out/default-s1.json 2>/dev/null
CENSUS_CSV=out/m400-s1-rtf1.csv     $X universe --kick-bench --members 400 --seconds 30 > out/m400-s1-rtf1.json 2>/dev/null
CENSUS_CSV=out/m400-s1-rtf100.csv   $X universe --kick-bench --members 400 --rtf 100 --seconds 30 > out/m400-s1-rtf100.json 2>/dev/null
CENSUS_CSV=out/m400-s3-rtf100.csv   $X universe --kick-bench --members 400 --rtf 100 --seconds 30 --seed 3 > out/m400-s3-rtf100.json 2>/dev/null
# determinism: rerun the decisive arm and compare
$X universe --kick-bench --members 400 --rtf 100 --seconds 30 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['digest'])" > out/rtf100-rerun-digest
python3 -c "import json; print(json.load(open('out/m400-s1-rtf100.json'))['digest'])" > out/rtf100-first-digest
cmp out/rtf100-first-digest out/rtf100-rerun-digest && echo "determinism: rtf100 digest reproduced"

echo "== 4. summary =="
python3 - <<'EOF'
import json
print(f"{'arm':22} {'digest':18} {'mints':>6} {'quad%':>6} {'panels%':>8} {'walk%':>6} {'reads':>6}  bins")
for f in ['out/default-s1.json','out/m400-s1-rtf1.json','out/m400-s1-rtf100.json','out/m400-s3-rtf100.json']:
    d = json.load(open(f)); c = d['census']
    cy = c.get('cycles/leavers') or c.get('cycles/made', {})
    q = cy.get('quad_frac_median', float('nan')); p = cy.get('panels_frac_median', float('nan'))
    w = cy.get('walk_frac_median', float('nan')); r = cy.get('reads_median', 0)
    bins = {k: v['mints'] for k, v in c['cadence_bins_interval_over_period'].items()}
    print(f"{f[4:-5]:22} {d['digest'][:16]:18} {c['mints']:>6} {100*q:>6.2f} {100*p:>8.2f} {100*w:>6.2f} {r:>6.0f}  {bins}")
    for k, v in sorted(c.items()):
        if isinstance(v, dict) and 'passages' in k:
            print(f"  passages: mints {v['mints']} quad {100*v['quad_frac_median']:.2f}% reads {v['reads_median']:.0f}")
EOF
