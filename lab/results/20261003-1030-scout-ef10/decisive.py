#!/usr/bin/env python3
"""Decisive sweep + held-out cases. See predictions.md (written first)."""
import json, importlib.util, time
spec = importlib.util.spec_from_file_location("cf", "corrector_falsifier.py")
cf = importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)

NS = [2, 4, 8, 16, 32, 64]
ORD = [None, 3, 5, 7, 11, 'corrupt3']
TH_PREC, TH_DCJ = 0.01, 1e-4

def sweep(cases, orbits, orders, tag):
    out = {'meta': {'orbits': orbits, 'gates': {'prec_rel': TH_PREC, 'dCJ': TH_DCJ},
                    'corrector_kick_cost_per_output': {str(o): (4 if o == 3 else
                        8 if o == 5 else 12 if o == 7 else 20 if o == 11 else 4)
                        for o in orders if isinstance(o, int)}},
           'cases': {}}
    for (m2, e0) in cases:
        o = cf.run(e0, 128, 5, orbits, m2=m2, aout=4.5)   # oracle
        out['meta']['oracle_e%s_m%s' % (e0, m2)] = {'prec': o['prec'], 'resid': o['fit_resid'],
                                                    'dCJ': o['dCJ_max']}
        print('== m2=%g e=%.2f oracle prec=%.5e resid=%.2e dCJ=%.2e'
              % (m2, e0, o['prec'], o['fit_resid'], o['dCJ_max']))
        for order in orders:
            for n in NS:
                r = cf.run(e0, n, order, orbits, m2=m2, aout=4.5)
                rel = abs(r['prec'] - o['prec'])/abs(o['prec'])
                ok = (rel <= TH_PREC) and (r['dCJ_max'] <= TH_DCJ)
                out['cases']['m%s-e%s-%s-n%d' % (m2, e0, order, n)] = dict(
                    r, prec_rel=rel, ok=ok)
                print('  m2=%-5g e=%.2f %-8s n=%2d prec_rel=%8.2e dCJ=%8.2e last=%8.2e ok=%s'
                      % (m2, e0, str(order), n, rel, r['dCJ_max'], r['dCJ_last'], ok))
    json.dump(out, open('results-%s.json' % tag, 'w'), indent=1)
    return out

t0 = time.time()
# grid cases (e=0.2 tuned; e=0.6 in-grid but never run before predictions)
sweep([(0.3, 0.2), (0.3, 0.6), (0.01, 0.2), (0.01, 0.6)], 600, ORD, 'sweep')
# held out entirely
sweep([(0.01, 0.4), (0.3, 0.4), (0.01, 0.85), (0.3, 0.85)], 600, [None, 5, 7], 'heldout')
print('total %.1f s' % (time.time() - t0))
