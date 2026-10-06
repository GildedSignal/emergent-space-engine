"""Tolerance ladder for the exact planet integrations: is the 8.4e-3 exact-vs-exact
gap unconverged numerics, or chaos amplifying roundoff (physical)?
Each config saved to npz; compare.py-style pairwise diffs computed at the end."""
import sys
import time

import numpy as np

import exact_check as X


def run_one(name):
    rtol, mode = name.split("_")
    rtol = float(rtol)
    t0 = time.time()
    if mode == "helio":
        zs, zj, sol = X.exact_helio_tol(rtol)
        nfev = sol.nfev
    else:
        zs, zj = X.exact_bary_tol(rtol)
        nfev = -1
    np.savez(f"exact_{name}.npz", zs=zs, zj=zj, t=X.stor_times)
    print(f"{name}: {time.time()-t0:.0f}s nfev={nfev} "
          f"|z_S| end {np.abs(zs[-1]):.4f} min {np.abs(zs).min():.4f}", flush=True)


def compare():
    import glob
    files = sorted(glob.glob("exact_*.npz"))
    d = {f[6:-4]: np.load(f) for f in files}
    names = list(d)
    print("pairwise max|dz| (upper triangle) and divergence-onset time (|dz|>1e-6):")
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = d[names[i]], d[names[j]]
            dS = np.abs(a["zs"] - b["zs"])
            dJ = np.abs(a["zj"] - b["zj"])
            idx = np.argmax(dS > 1e-6) if (dS > 1e-6).any() else -1
            ton = a["t"][idx] if idx >= 0 else float("inf")
            print(f"  {names[i]} vs {names[j]}: max|dz_S|={dS.max():.2e} "
                  f"max|dz_J|={dJ.max():.2e} t(|dz_S|>1e-6)={ton:.0f}")


if __name__ == "__main__":
    if sys.argv[1] == "cmp":
        compare()
    else:
        run_one(sys.argv[1])
