#!/usr/bin/env bash
# Regenerates every number in the dossier from the shipped oracles + this run's
# script (work/binet_refit.py, self-contained, stdlib only). ~110 s single-threaded.
set -euo pipefail
cd "$(dirname "$0")"
python3 work/binet_refit.py > work/run_output.txt 2>&1
echo "--- sampler table ---";   sed -n '1,11p' work/run_output.txt
echo "--- port validation ---"; sed -n '/port validation:/,/e=0 family/p' work/run_output.txt | head -8
echo "--- capture/isco/crossings ---"; sed -n '/capture misclassified/,$p' work/run_output.txt
python3 - <<'EOF'
import json
d = json.load(open('work/metrics.json'))
print('--- compile control (agm, from invariants) ---')
print('sampler agm advance worst:', d['sampler']['agm-m16']['advance_err_worst'])
print('--- held-out ---')
for k, v in d['heldout'].items():
    out = {}
    for kk, vv in v.items():
        if kk.startswith('frozen'):
            out[kk] = vv
        else:
            out[kk] = {m: x for m, x in vv.items()}
    print(' ', k, out)
EOF
