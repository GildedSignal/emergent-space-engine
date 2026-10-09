#!/usr/bin/env python3
"""P6: the visible-secondary envelope. r* sweep at M=1, D_OL=2000, D_OS=10000
(the checker's attack #1): two-image alignments exist only while r* < b_E
(~80 here); at r* >= b_E the would-be secondary is born occulted.
Truth-only census. Writes envelope-out.json.
"""
import numpy as np, json, time
import falsifier as F
from bh import roots_on_grid

def main():
    t0 = time.time()
    etas = np.unique(np.concatenate([[0.0, 5.0, 10.0], np.arange(20.0, 401.0, 20.0)]))
    thetas = np.linspace(-0.25, 0.25, 1201)
    rows = []
    for R in (50.0, 60.0, 70.0, 80.0, 90.0, 100.0):
        F.R_STAR = R
        n2 = 0; ex = []
        for eta in etas:
            L, Srel, rS = F.geom(eta)
            roots = roots_on_grid(thetas, L, Srel, rS)
            if len(roots) >= 2:
                n2 += 1; ex.append(round(float(eta), 1))
        rows.append(dict(r_star=R, alignments_with_two_images=n2,
                         two_image_etas=ex, b_E=80.0))
    out = dict(wall_s=round(time.time()-t0, 1), n_alignments_tested=len(etas), rows=rows)
    print(json.dumps(out, indent=1))
    with open('envelope-out.json', 'w') as fh:
        json.dump(out, fh, default=float)

if __name__ == '__main__':
    main()
