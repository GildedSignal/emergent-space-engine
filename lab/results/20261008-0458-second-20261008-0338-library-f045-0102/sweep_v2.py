# Decisive sweeps on the v2 (corrected) harness.
import numpy as np, math, sys
from v2 import kicked_v2, truth_v2, R_HILL
mode, n_orb = sys.argv[1], int(sys.argv[2])
broken = (mode == "broken")
taus = [0.05, 0.10, 0.13, 0.17, 0.20, 0.25, 0.30]
PHIS = np.arange(12)/12*2*np.pi
print(f"# v2 mode={mode} n_orb={n_orb} mu=1e-3 12 phases K=(1,4,16) truth 4000/orbit")
print("#  tau  medA16   q25   q75   minA16  maxA16 frac>1  medA4 | medTruth  medErr1  medErr16")
for tau in taus:
    a = tau*R_HILL
    try:
        wt = truth_v2(a, n_orb, PHIS)
        w1 = kicked_v2(a, 1, n_orb, PHIS, broken)
        w4 = kicked_v2(a, 4, n_orb, PHIS, broken)
        w16 = kicked_v2(a, 16, n_orb, PHIS, broken)
    except ValueError as ex:
        print(f"{tau:5.2f}  failed: {ex}"); continue
    e1, e4, e16 = np.abs(w1-wt), np.abs(w4-wt), np.abs(w16-wt)
    A16 = e1/e16; A4 = e1/e4
    print(f"{tau:5.2f}  {np.median(A16):7.3f} {np.quantile(A16,0.25):6.3f} {np.quantile(A16,0.75):6.3f} "
          f"{A16.min():7.3f} {A16.max():7.3f} {np.mean(A16>1):6.2f}  {np.median(A4):6.3f} | "
          f"{np.median(wt):8.3e} {np.median(e1):8.3e} {np.median(e16):8.3e}")
    sys.stdout.flush()
