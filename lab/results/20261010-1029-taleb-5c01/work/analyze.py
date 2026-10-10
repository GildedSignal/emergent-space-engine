#!/usr/bin/env python3
import json, sys

def row(tag, d):
    t, m = d['true'], d['missed']
    pct = 100.0 * m / max(1, t)
    v = d.get('verdicts', {})
    vstr = ' '.join(f"{k}:{n}" for k, n in sorted(v.items()))
    print(f"{tag:28s} true={t:6d} miss={m:5d} ({pct:5.1f}%) [{vstr}] kinds C{d['kinds']['C']}/W{d['kinds']['W']}/F{d['kinds']['F']} win_over={d.get('win_over')} mo={d['method_only']}")

def main(path):
    for l in open(path):
        l = l.strip()
        if not l.startswith('{'):
            print('NON-JSON:', l[:100]); continue
        try:
            d = json.loads(l)['missmap']
        except Exception as e:
            print('PARSE FAIL:', e, l[:120]); continue
        tag = f"a={d['a_hw']:.0e} se={d['sig_e']:.0e} rho={d['rho']:.0e} sl={d['sig_lam']} sd={d['seed']} o={d['orbits']:.0f} +{d['debris'][0]}x{d['debris'][1]}"
        row(tag, d)

if __name__ == '__main__':
    main(sys.argv[1])
