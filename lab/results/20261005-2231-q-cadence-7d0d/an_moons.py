"""Analyze the moon grid: N*(f,e), error type (walk vs saturate), and the fit."""
import numpy as np
from cad import TWOPI

MU = 1e-3; GM_P = MU; GM_S = 1 - MU
RH = (MU / 3) ** (1 / 3)


def nstar_for(res, f, e0, Ns, refN=512, aps_tol=0.10, emax_lo=0.8, emax_hi=1.25):
    ref = [r for r in res if r["f"] == f and r["e0"] == e0 and r["N"] == refN][0]
    ref["wdot"] = np.array(ref["wdot"]); ref["emax"] = np.array(ref["emax"])
    bound_ref = ref["a_end"] > 0  # all bound in doll sense; use emax sane
    ks = None
    for N in Ns:
        r = [x for x in res if x["f"] == f and x["e0"] == e0 and x["N"] == N][0]
        r["wdot"] = np.array(r["wdot"]); r["emax"] = np.array(r["emax"])
        ok = np.abs(r["wdot"] / ref["wdot"] - 1) < aps_tol
        ok &= (r["emax"] / ref["emax"] > emax_lo) & (r["emax"] / ref["emax"] < emax_hi)
        ok &= np.isfinite(r["wdot"]) & np.isfinite(ref["wdot"])
        if ok.mean() >= 0.99:
            ks = N
            break
    return ks, ref


def main():
    res = np.load("moon_grid.npy", allow_pickle=True).tolist()
    Ns = [2, 3, 4, 6, 8, 12, 16, 24, 32]
    fs = sorted({r["f"] for r in res})
    es = sorted({r["e0"] for r in res})
    print("N* table (rows f, cols e0):")
    print("f\\e  " + "  ".join(f"{e:.2f}" for e in es))
    grid = {}
    for f in fs:
        row = []
        for e0 in es:
            ks, ref = nstar_for(res, f, e0, Ns)
            row.append(ks if ks is not None else -1)
            grid[(f, e0)] = ks
        print(f"{f:.2f}  " + "  ".join(f"{v:2d}" for v in row))
    # classical check
    for f in fs:
        ref = [r for r in res if r["f"] == f and r["e0"] == 0.05 and r["N"] == 512][0]
        a0 = f * RH; n = np.sqrt(GM_P / a0 ** 3)
        tau = (GM_S / GM_P) * a0 ** 3
        wd = np.median(ref["wdot"])
        print(f"classical f={f}: meas {wd:+.5f} cl {0.75*n*tau:+.5f} ratio {wd/(0.75*n*tau):.3f}")
    # error-type: half-horizon vs full-horizon apsidal rate deviation, at the frontier N
    print("\nwalk check (|wdot_half/wdot_full - 1| at N=8 and N=16, e=0.05):")
    for f in fs:
        for N in (8, 16):
            r = [x for x in res if x["f"] == f and x["e0"] == 0.05 and x["N"] == N][0]
            ref = [x for x in res if x["f"] == f and x["e0"] == 0.05 and x["N"] == 512][0]
            r["wdot"] = np.array(r["wdot"]); ref["wdot"] = np.array(ref["wdot"])
            d = np.abs(r["wdot"] / ref["wdot"] - 1)
            print(f"  f={f} N={N}: median dev {np.median(d):.3f}")
        break
    np.save("moon_nstar.npy", grid, allow_pickle=True)


if __name__ == "__main__":
    main()
