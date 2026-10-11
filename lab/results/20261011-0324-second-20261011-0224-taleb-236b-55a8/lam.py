#!/usr/bin/env python3
"""Mean-anomaly vs mean-longitude ordering for the rank-k certificate, all
scenarios (checker 1's point 4 dismissed the ordering objection with the
formula "lambda offset ~ Delta w at crossings"; the correct leading order is
DeltaM* ~ -Delta w and DeltaLambda* ~ 2(e_j sin nu_j - e_i sin nu_i), second
order in the dispersion — this measures which is right)."""
import sys, json
sys.argv = ['probe2', 'conj', '1e-4']
import probe2

fams = probe2.fleets()
out = {}
for name in ('S0', 'S1', 'S2'):
    fam = fams[name]
    ev = probe2.find_contacts2(fam)
    res, rl, rf = probe2.summarize(fam, ev)
    # lambda offsets at contact, directly
    a, e, w, M0 = fam['a'], fam['e'], fam['w'], fam['M0']
    nv = probe2.np.sqrt(probe2.GM/a**3)
    ii = probe2.np.array([x[0] for x in ev]); jj = probe2.np.array([x[1] for x in ev])
    tt = probe2.np.array([x[2] for x in ev])
    dlam = ((M0[ii]+nv[ii]*tt+w[ii]) - (M0[jj]+nv[jj]*tt+w[jj]) + probe2.np.pi) % (2*probe2.np.pi) - probe2.np.pi
    dM = ((M0[ii]+nv[ii]*tt) - (M0[jj]+nv[jj]*tt))
    res['dlam_at_contact_abs_p50'] = float(probe2.np.median(probe2.np.abs(dlam)))
    res['dM_at_contact_abs_p50'] = float(probe2.np.median(probe2.np.abs(dM)))
    out[name] = res
    print(name, json.dumps(res), flush=True)
json.dump(out, open(probe2.sys.path[0]+'/lam.json', 'w'), indent=1)
