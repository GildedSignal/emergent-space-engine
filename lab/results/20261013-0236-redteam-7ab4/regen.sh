#!/usr/bin/env bash
# Regenerates every number in dossier.md from the run's own probe (float, ~4 s).
# The harness applies work/patch.diff (which carries this folder) before running this.
set -euo pipefail
cd "$(dirname "$0")"
python3 news_scar.py > regen-run.txt 2>&1
echo "--- decisive tables (full log: regen-run.txt) ---"
sed -n '1,60p' regen-run.txt
python3 - <<'EOF'
import json
d = json.load(open("scar.json"))
print("\nCHECKS against dossier.md:")
print("E1 exponent (dossier: 1.963):", round(d["fit"]["exponent"], 3))
print("E1 k_bar@0.3 (dossier: 0.70):", round(d["fit"]["k_bar_0.3"], 2))
print("E1 twin_max (dossier: 0.0):", d["fit"]["twin_max"])
b = {(r["beta_c"], r["cad_div"]): r for r in d["burn"]}
for k in [(0.05, 8), (0.05, 32), (0.1, 8), (0.1, 32), (0.3, 8), (0.3, 32)]:
    r = b[k]
    print(f"E2 beta={k[0]} cad={k[1]}: lag@ageT={r['lag_at_ageT']:.4f} "
          f"pred={r['plateau_pred']:.4f} scar_E={r['scar_E']:.3e}")
print("E5 dt conv rel diff:", d["dt_conv"])
EOF
