#!/usr/bin/env bash
# Regenerates every number in dossier.md from the run's own script (float instrument;
# the oracle ports live inside the script, verbatim in form from
# xtask/src/gr_oracle.rs and gr_oracle_extended.rs at the run's base commit).
# No tree edits needed. Runtime ~10 s; requires python3 with numpy and scipy.
set -euo pipefail
cd "$(dirname "$0")"
python3 -c "import numpy, scipy" || pip install --quiet numpy scipy
python3 binet_refit.py report.json
python3 - <<'EOF'
import json
r = json.load(open('report.json'))
print("== sampler (256 frozen seeds; prec/per = pass fractions at the frozen bars) ==")
for m in (8, 16, 32):
    for arm in ('FROZEN', 'CONT', 'GEO'):
        d = r[f'sampler_m{m}_{arm}']
        print(f"{arm:6s} m={m:2d}: prec {d['precession_pass']:.4f} per {d['period_pass']:.4f} "
              f"crossings_med {d['median_crossings']:.0f} "
              f"adv_changed>1e-6 {d['advance_changed_beyond_1e-6']} "
              f"med_adv_err {d['median_adv_err']:.2e}")
print("== deterministic e=0 circles (instrument-limited: see dossier) ==")
for m in (8, 16, 32):
    for arm in ('FROZEN', 'CONT', 'GEO'):
        d = r[f'circles_m{m}_{arm}']
        print(f"circles m={m} {arm}: n={d['n']} worst adv {d['worst_advance_rel']:.2e} "
              f"worst per {d['worst_period_rel']:.2e}")
print("== strong-field rows (instrument-limited) ==")
for k, v in r['strong_field_m16'].items():
    print(k, {a: f"{x['adv_err']:.2e}/{x['period_err']:.2e}" for a, x in v.items()})
print("== isco (instrument-limited) ==", r['isco_m16'])
print("== capture misclassified (instrument-limited) ==", r['capture_misclassified'])
print("== repeat: cycle 2 identical to cycle 1 (of 16 seeds) ==", r['repeat_ok_of_16'])
EOF
