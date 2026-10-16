#!/usr/bin/env bash
# Regenerates every number in dossier.md from this run's scripts (the rebuilt
# walker + the r1v2 freeze execution). No tree edits needed. Runtime ~10 min.
set -euo pipefail
cd "$(dirname "$0")"
python3 -c "import numpy, scipy, matplotlib" 2>/dev/null || pip install --quiet numpy scipy matplotlib
python3 binet_r1v2.py report.json            # sampler/circles/strong/light/capture/isco/longruns + verdict
python3 barriers.py barriers.json            # the model's capture barriers (matter L_hat, photon b_hat)
python3 - <<'EOF'
import json
r = json.load(open('report.json'))
print("== r1v2 execution (freeze: r1v2-rings-band-constant.md) ==")
for cfg, met in r['metrics'].items():
    print(f"{cfg}: prec {met['precession_pass_fraction']:.4f} per {met['period_pass_fraction']:.4f} "
          f"prog {met['prograde_fraction']:.4f} defl {met['deflection_pass_fraction']:.4f} "
          f"cap {met['capture_misclassified']} isco {met['isco_correct']} "
          f"shape {met['shape_kept_fraction']:.4f} rep {met['cycle_repeat_fraction']:.4f} "
          f"cr {met['crossings_per_cycle']:.0f} nc {met['nearcircular_pass_fraction']:.4f} "
          f"(worst {met['_nearcircular_worst']:.2e}) sf {met['strongfield_pass_fraction']:.4f} "
          f"throws {met['sampler_throws']} med {met['median_adv_err']:.2e}")
print("== verdicts ==")
for cfg, v in r['verdict'].items():
    print(f"{cfg}: {'PASS' if v['passes'] else 'FAIL'} {v['fails']}")
d = json.load(open('detail.json'))
for cfg, dd in d.items():
    lr = dd['longruns']
    print(f"{cfg} longruns: n={lr['n']} cycles={lr['cycles']} worst dphi drift {lr['worst_dphi_drift']:.2e} "
          f"worst t drift {lr['worst_t_drift']:.2e} exc {lr['n_exc']} | "
          f"strong: " + " ".join(f"({x['p']},{x['e']}):{x['adv_rel']:.1e}/{x['per_rel']:.1e}" for x in dd['strongrows']))
b = json.load(open('barriers.json'))
for k, v in b.items():
    if k != 'gr':
        print(k, v)
EOF
