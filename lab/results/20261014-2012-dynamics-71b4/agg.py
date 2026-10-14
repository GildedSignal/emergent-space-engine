#!/usr/bin/env python3
"""Aggregate the decisive runs into the dossier table + matched-rate ratios."""
import glob
import json

import numpy as np


def meta(name):
    if '_A' in name or name.startswith('A'):
        return 'A'
    if '_C' in name or 'C_' in name or name.startswith('C'):
        return 'C'
    return 'Q'


rows = []
for f in sorted(glob.glob('runs/*.npz')):
    z = np.load(f, allow_pickle=True)
    name = f.split('/')[-1].replace('.npz', '')
    d = np.asarray(z['dmax'], dtype=float)
    s = np.asarray(z['slope'], dtype=float)
    rows.append(dict(
        run=name, rule=meta(name),
        rate_med=float(np.median(z['rate'])),
        D_med=float(np.median(d)),
        D_p90=float(np.sort(d)[int(0.9 * (len(d) - 1))]),
        slope_med=float(np.median(s)),
        slope_p90=float(np.sort(s)[int(0.9 * (len(s) - 1))]),
        lock_med=float(np.median(z['lock'])),
        dphi_med=float(np.median(z['dphi_std']))))

print(f"{'run':28s} {'rate':>6s} {'D_med':>9s} {'D_p90':>9s} {'sl_med':>6s} "
      f"{'sl_p90':>6s} {'lock':>5s} {'dphi':>5s}")
for r in rows:
    print(f"{r['run']:28s} {r['rate_med']:6.2f} {r['D_med']:9.2e} {r['D_p90']:9.2e} "
          f"{r['slope_med']:6.3f} {r['slope_p90']:6.3f} {r['lock_med']:5.2f} "
          f"{r['dphi_med']:5.3f}")

# clock frontier (rule A, H=400, 32 bodies) and ratios at matched rate
A = [r for r in rows if r['run'].startswith('A_K')]
if A:
    ar = np.array([[r['rate_med'], r['D_med']] for r in A])

    def clock_D(rate):
        return 10 ** np.interp(np.log10(rate), np.log10(ar[:, 0]), np.log10(ar[:, 1]))

    print("\nmatched-rate excess over the clock frontier (D at H=400):")
    for r in rows:
        if r['run'].startswith(('C_', 'Q_')):
            print(f"  {r['run']:28s} rate={r['rate_med']:5.2f}  D/clock = "
                  f"{r['D_med'] / clock_D(r['rate_med']):8.1f}x  slope={r['slope_med']:.3f}")

json.dump(rows, open('runs/table.json', 'w'), indent=1)
