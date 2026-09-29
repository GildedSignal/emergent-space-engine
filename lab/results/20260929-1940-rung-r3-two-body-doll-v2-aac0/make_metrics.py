#!/usr/bin/env python3
"""Stage 6: assemble metrics.json from the stage outputs."""
import json, math, os

out = {}
b = json.load(open('binaries_summary.json'))

# events per orbit: the doll computes binary cycles analytically (0 events per radial
# period); the handoff case adds 2 handoffs per star-planet radial period and each
# flyby 2 crossings per planet period (documented in the dossier).
ev = 0.0

for cfg in ('eob-doll', 'test-mass', 'newton-doll'):
    key = {'eob-doll': 'eob', 'test-mass': 'test', 'newton-doll': 'newton'}[cfg]
    d = b[key]
    out[cfg] = {
        'precession_pass_fraction': round(d['precession_pass_fraction'], 4),
        'period_pass_fraction': round(d['period_pass_fraction'], 4),
        'nu_effect_pass_fraction': round(d['nu_effect_pass_fraction'], 4),
        'min_judged_seeds': d['min_judged_seeds'],
        'events_per_orbit': ev,
    }

# handoff + assists are test-mass cases: identical across configs
if os.path.exists('handoff_data.json'):
    h = json.load(open('handoff_data.json'))
    for cfg in out:
        out[cfg]['handoff_energy_growth_exponent'] = round(h['lam'], 4)
else:
    for cfg in out:
        out[cfg]['handoff_energy_growth_exponent'] = None

if os.path.exists('assists.json'):
    a = json.load(open('assists.json'))
    frac = sum(1 for r in a if r['err'] <= 0.01) / len(a)
    for cfg in out:
        out[cfg]['assist_pass_fraction'] = round(frac, 4)
else:
    for cfg in out:
        out[cfg]['assist_pass_fraction'] = None

json.dump(out, open('metrics.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
