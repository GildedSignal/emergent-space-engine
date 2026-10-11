#!/usr/bin/env python3
"""Circular rank (min(|i-j|, n-|i-j|) in the sorted phase ordering) for mean
anomaly and mean longitude, all scenarios. The original probe's rank metric is
LINEAR in the mod-2pi sorted order, which counts pairs straddling the 0/2pi
branch cut as rank ~n even when their phase offset is ~0; the fleet's M and
lambda arcs are centered at 0, so this is not a corner case here."""
import sys, json
sys.argv = ['probe2', 'conj', '1e-4']
import probe2
import numpy as np

def circ_ranks(fam, events, kappa=None):
    a, e, w, M0 = fam['a'], fam['e'], fam['w'], fam['M0']
    n = len(a); nv = np.sqrt(probe2.GM/a**3)
    krate = (np.zeros(n) if kappa is None else np.asarray(kappa)*nv/(2*np.pi))
    rM, rL = [], []
    cache = {}
    for i, j, tc, _ in events:
        key = round(tc, 9)
        if key not in cache:
            M = (M0 + nv*tc) % (2*np.pi)
            L = (M0 + nv*tc + w + krate*tc) % (2*np.pi)
            iM = np.argsort(M, kind='stable'); iL = np.argsort(L, kind='stable')
            pM = np.empty(n, int); pM[iM] = np.arange(n)
            pL = np.empty(n, int); pL[iL] = np.arange(n)
            cache[key] = (pM, pL)
        pM, pL = cache[key]
        rM.append(min(abs(pM[i]-pM[j]), n-abs(pM[i]-pM[j])))
        rL.append(min(abs(pL[i]-pL[j]), n-abs(pL[i]-pL[j])))
    return np.array(rM), np.array(rL)

def window_table(r):
    return {str(k): round(float((r <= k).mean()), 4) for k in (4, 8, 16, 32, 64, 128, 256)}

out = {}
fams = probe2.fleets()
b = probe2.boundary_case()
for name, fam, dense in (('S0', fams['S0'], False), ('S1', fams['S1'], False),
                         ('S2', fams['S2'], False), ('S4', fams['S4'], True),
                         ('S5 boundary', b, True)):
    if dense:
        ev = probe2.find_contacts2(fam, all_pairs=True, spP=64, r_all=1e-4+6e-3)
    else:
        ev = probe2.find_contacts2(fam)
    rM, rL = circ_ranks(fam, ev)
    e = fam['e']
    ii = np.array([x[0] for x in ev]); jj = np.array([x[1] for x in ev])
    bound = 2*(e[ii]+e[jj])
    res = dict(events=len(ev),
               circ_M_median=float(np.median(rM)), circ_M_frac_le_4=round(float((rM <= 4).mean()), 4),
               circ_M_frac_le_32=round(float((rM <= 32).mean()), 4),
               circ_L_median=float(np.median(rL)),
               circ_L_windows=window_table(rL),
               circ_L_max=int(rL.max()),
               lam_bound_2ei_ej_p100=float(bound.max()),
               circ_L_rank_over_bound_p50=float(np.median(rL)),
               e_max=float(e.max()))
    if name == 'S2 interception':
        half = len(fam['a'])//2
        cross = [k for k, x in enumerate(ev) if (x[0] < half) != (x[1] < half)]
        rc = rL[cross]; rcM = rM[cross]
        res['cross_circ_L_median'] = float(np.median(rc)); res['cross_circ_L_max'] = int(rc.max())
        res['cross_circ_M_median'] = float(np.median(rcM))
    out[name] = res
    print(name, json.dumps(res), flush=True)
json.dump(out, open(probe2.sys.path[0]+'/circ.json', 'w'), indent=1)
