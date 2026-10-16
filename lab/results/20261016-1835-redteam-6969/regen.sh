#!/bin/sh
# Regenerates every number in dossier.md. Runtime ~35 s, <100 MB.
set -e
cd "$(dirname "$0")"
python3 eob_flank.py flank.json > flank_stdout.txt 2>&1
python3 - <<'EOF'
import json
d = json.load(open('flank.json'))
print('C0 (r-quad vs chi-integral, max rel):', d['controls']['C0_schw_quad_vs_analytic_maxrel'])
for c in d['controls']['C1_adm2_nu0_vs_exact']:
    print('C1 p=%g e=0.3 2PN-floor resid_rel=%+.3e' % (c['p'], c['resid_rel']))
print()
print('%4s %3s | %10s %10s %10s %10s | %12s' % ('p','e','eps(nu=0)','eps(.05)','eps(.125)','eps(.25)','nu-induced'))
for row in d['grid']:
    es = [row['nu%s'%n]['eps_doll_vs_2PN'] for n in ('0.0','0.05','0.125','0.25')]
    print('%4.0f %4.1f | %+10.4f %+10.4f %+10.4f %+10.4f | %+12.4f' % (row['p'], row['e'], es[0], es[1], es[2], es[3], es[3]-es[0]))
print()
print('circular (e=0) dOm/Om at fixed j:')
for row in d['grid']:
    if row['e'] == 0.0:
        for nu in ('0.0','0.25'):
            c = row['nu'+nu]
            if c.get('om_phi_2PN') is not None and c['om_phi_2PN'] == c['om_phi_2PN']:
                print('p=%5.0f nu=%s dOm/Om=%+.4e' % (row['p'], nu, c['om_phi_2PN']/c['om_phi_doll'] - 1.0))
EOF
