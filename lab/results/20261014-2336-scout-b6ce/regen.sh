#!/bin/sh
# Regenerates every number in dossier.md from this run's own script.
# No repo edits are needed (the run's patch is empty: read-only scout on shipped code).
# Wall time: ~90 s. Requires python3 with numpy.
set -e
cd "$(dirname "$0")"
[ -f work/patch.diff ] && patch -p1 --dry-run < work/patch.diff >/dev/null 2>&1 && echo "(patch present, applied by runner)"
mkdir -p out
python3 work/scan_tier.py out/scan_tier.json
python3 - <<'EOF'
import json
rows = json.load(open("out/scan_tier.json"))
print(f"{'arm':>16} {'N':>7} {'ship/mint':>10} {'tier/mint':>9} {'cut':>6} {'miss':>5} {'naiveMiss':>9} {'MB/mint':>8} {'heldGB':>7} {'truth/mint':>9}")
for r in rows:
    print(f"{r['window']+','+r['tag']:>16} {r['n']:>7} {r['shipped_cand_mean']:>10.0f} {r['tier_cand_mean']:>9.0f} "
          f"{r['cut_mean']:>6.1f} {r['miss_tier']:>5} {r['miss_naive']:>9} {r['standing_mb_per_mint']:>8.3f} "
          f"{r['flight_held_gb']:>7.2f} {r['truth_hits_mean']:>9.1f}")
EOF
echo "regen OK"
