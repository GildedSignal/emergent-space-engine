#!/usr/bin/env bash
# Regenerates every dossier number: applies work/patch.diff if needed, builds, runs the
# census matrix (the plane bench with ES_SURPRISE=1), and prints the analysis.
# Total wall time on the lab's shared runner: ~2 min (build warm), ~6 min cold.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root

if ! grep -q census_on crates/universe/src/universe.rs; then
  git apply lab/results/20261013-2252-dynamics-ea91/work/patch.diff
fi
cargo build --release -p xtask

X=${CARGO_TARGET_DIR:-target}/release/xtask
R=lab/results/20261013-2252-dynamics-ea91
for spec in "1 48 100 30 tune" "3 400 100 55 ho1" "7 48 100 55 ho2" "3 48 1 30 ho3"; do
  set -- $spec
  ES_SURPRISE=1 "$X" universe --bench --seed "$1" --members "$2" --rtf "$3" --seconds "$4" --unpaced \
    > "$R/census-$5.json"
done

python3 "$R/analyze.py" > "$R/analysis.json"
python3 - "$R/analysis.json" <<'EOF'
import json, sys
for r in json.load(open(sys.argv[1])):
    rs = r.get('rank_stability', {}); pr = r['promotions']; st = r['stream']; tl = r['steady_tail']
    print('{} digest {} | bodies {} items {} | gini {} top10 {} zipf {}'.format(
        r['scene'], r['digest'], r['bodies'], r['items'], r['all']['gini'], r['all']['top10_share'], r['all']['zipf_slope']))
    print('   promotions: {} (dead {:.0%}) | live promoted rho={} natives rho={} (null {})'.format(
        pr['promoted'], pr['dead_frac'], rs.get('spearman_promoted'), rs.get('spearman_native'), rs.get('spearman_poisson_null')))
    print('   stream: fano {} zero {} | steady tail fano {} top1pct {} zero {}'.format(
        st['fano'], st['zero_frac'], tl['fano'], tl['top1pct_frames_share'], tl['zero_frac']))
EOF
