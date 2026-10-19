#!/usr/bin/env python3
"""Second-author summary: the 12800 extinction table, the corrected 6400 row, poly_r."""
import glob
import numpy as np
from late import series, w64, fn, peak_period


def arm(path, late=4096):
    meta, con = series(path)
    w = w64(con)
    nb = len(w) // 32
    blocks = [fn(w[j * 32:(j + 1) * 32]) for j in range(nb)]
    lw = w64(con[-late:])
    l8 = con[-8192:] if len(con) >= 8192 else con
    wl8 = w64(l8)
    T, sh = peak_period(con[:2048])
    return {
        "meta": meta, "n": int(meta["n"]), "side": int(meta["side"]),
        "seed": meta["seed"], "H": len(con), "w": w, "con": con,
        "blocks": [round(b, 1) for b in blocks],
        "mean64": float(w.mean()), "m_whole": float(w.std(ddof=1) / w.mean() * 100),
        "F64_whole": fn(w), "F1": float(con.var(ddof=1) / con.mean()),
        "m_late": float(lw.std(ddof=1) / lw.mean() * 100),
        "F64_late": fn(lw), "mean64_late": float(lw.mean()),
        "p99p50": float(np.percentile(con, 99) / np.percentile(con, 50)),
        "p99p50_l8": float(np.percentile(l8, 99) / np.percentile(l8, 50)),
        "mxp50_l8": float(wl8.max() / np.percentile(wl8, 50)),
        "b0mxp50": float(w[:32].max() / np.percentile(w[:32], 50)),
        "T_early": T, "sh_e": sh,
    }


def extinct(blocks, thr=6.0):
    """first block index after which all blocks stay <= thr, else None"""
    for j in range(len(blocks)):
        if all(b <= thr for b in blocks[j:]):
            return j
    return None


if __name__ == "__main__":
    print("== 12800 extinction (fill 0.7, vmax 2^16, burn 1024, horizon 24576) ==")
    print(f"{'seed':>4} {'blocks_F64 (2048 ch each)':>58} {'ext@blk':>7} {'m_whole':>8} "
          f"{'m@8192':>7} {'m@12288':>8} {'m_late4k':>8} {'F64_late':>8} {'F1':>5} "
          f"{'p99/50':>7} {'p99/50_l8':>9} {'mxp50_l8':>8} {'b0mx/p50':>8} {'T_e':>5} {'T/side':>6}")
    for f in sorted(glob.glob("data/ext_n12800_s*.csv")):
        a = arm(f)
        truncs = {}
        for H in (8192, 12288):
            wt = w64(a["con"][:H])
            truncs[H] = float(wt.std(ddof=1) / wt.mean() * 100)
        e = extinct(a["blocks"])
        print(f"{a['seed']:>4} {str(a['blocks']):>58} {str(e):>7} "
              f"{a['m_whole']:7.2f}% {truncs[8192]:6.2f}% {truncs[12288]:7.2f}% "
              f"{a['m_late']:7.2f}% {a['F64_late']:8.2f} {a['F1']:5.2f} "
              f"{a['p99p50']:7.3f} {a['p99p50_l8']:9.3f} {a['mxp50_l8']:8.3f} "
              f"{a['b0mxp50']:8.3f} {a['T_early']:5d} {a['T_early']/a['side']:6.1f}")
        print(f"      mean64 {a['mean64']:.0f}  F64_whole {a['F64_whole']:.2f} = mean64*m^2 "
              f"{a['mean64']*(a['m_whole']/100)**2:.2f}  spec_share_early {a['sh_e']:.2f}")

    print("\n== The n-invariant instrument: late-4096 window F64 (raw late-m carries a")
    print("   1/sqrt(mean64) counting floor; F64_late = m^2 * mean64 is scale-free) ==")
    for f in (["data/lad_n400_s1.csv", "data/lad_n1600_s1.csv"]
              + sorted(glob.glob("data/lad_n6400_s*.csv"))
              + sorted(glob.glob("data/ext_n12800_s*.csv"))):
        a = arm(f)
        ml = a["mean64_late"] if "mean64_late" in a else (a["F64_late"] / (a["m_late"] / 100) ** 2)
        print(f"n{a['n']:>6} s{a['seed']} mean64_late {ml:8.0f} "
              f"m_late4k {a['m_late']:5.2f}% F64_late {a['F64_late']:5.2f}")
    print("\n== 6400 corrected row + late-m (seeds 1-3, horizon 8192) ==")
    for f in sorted(glob.glob("data/lad_n6400_s*.csv")):
        a = arm(f)
        print(f"s{a['seed']} F64 {a['F64_whole']:6.2f} mean64 {a['mean64']:7.0f} "
              f"m {a['m_whole']:5.2f}% m_late4k {a['m_late']:4.2f}% F64_late {a['F64_late']:5.2f} "
              f"F1 {a['F1']:5.2f} p99/50 {a['p99p50']:.3f} b0mx/p50 {a['b0mxp50']:.3f} "
              f"blocks {a['blocks']}")
    print("\n== poly_r corrected cell (seed 1, radii 0.75,1) ==")
    for f in sorted(glob.glob("data/poly_r6400_s1.csv")):
        a = arm(f)
        print(f"F64 {a['F64_whole']:6.2f} mean64 {a['mean64']:7.0f} m {a['m_whole']:5.2f}% "
              f"b0mx/p50 {a['b0mxp50']:.3f} T {a['T_early']} sh {a['sh_e']:.2f} blocks {a['blocks']}")
