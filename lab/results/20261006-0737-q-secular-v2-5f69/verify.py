"""Final truth verification, all from saved artifacts (planets only).

Usage: python3 verify.py
  [A] fixed helio (1e-12) vs bary (1e-14): both internally converged; must now agree.
  [B] hand-coded planets-only WH (h=0.125, 0.1875) vs bary: WH discretization scale.
  [C] LL drivers (old alpha^2 matrix vs corrected) vs bary.
  [E] shipped truth/conv/kick zp vs bary: THE truth check (Saturn's e history).
"""
import numpy as np

import exact_check as X
import wh_run as W

ARCSEC = 206265 * 2 * np.pi


def load(name):
    d = np.load(f"exact_{name}.npz")
    return d["zs"], d["zj"], d["t"]


def main():
    zsB, zjB, t = load("1e-14_bary")
    zsH, zjH, _ = load("1e-12_helio")
    dS = np.abs(zsH - zsB)
    print(f"[A] fixed-helio(1e-12) vs bary(1e-14): max|dz_S|={dS.max():.2e} "
          f"max|dz_J|={np.abs(zjH - zjB).max():.2e}")
    print(f"    bary |z_S|: min {np.abs(zsB).min():.4f} @t={t[np.argmin(np.abs(zsB))]:.0f} "
          f"end {np.abs(zsB[-1]):.4f} | |z_J|: max {np.abs(zjB).max():.4f} "
          f"end {np.abs(zjB[-1]):.4f}")
    i6 = np.argmax(dS > 1e-6) if (dS > 1e-6).any() else -1
    print(f"    t(|dz_S|>1e-6) = {t[i6] if i6 >= 0 else float('inf'):.0f}")

    for h in (0.1875, 0.125):
        zs, zj = X.wh_planets(h)
        np.savez(f"whplanets_{h}.npz", zs=zs, zj=zj)
        dS = np.abs(zs - zsB)
        i6 = np.argmax(dS > 5e-3) if (dS > 5e-3).any() else -1
        print(f"[B] hand WH h={h} vs bary: max|dz_S|={dS.max():.2e} "
              f"max|dz_J|={np.abs(zj - zjB).max():.2e} "
              f"t(|dz_S|>5e-3)={t[i6] if i6 >= 0 else float('inf'):.0f}")


def main2():
    """[C]+[E] only (after [A]/[B] done)."""
    zsB, zjB, t = load("1e-14_bary")
    _ce(zsB, zjB, t)


def _ce(zsB, zjB, t):
    M_old, M_new = X.matrices()
    z_old, g_old = X.ll_planet_z(t, M_old)
    z_new, g_new = X.ll_planet_z(t, M_new)
    print(f"[C] LL g: old = {np.round(g_old * ARCSEC, 2)} \"/yr, "
          f"new = {np.round(g_new * ARCSEC, 2)} \"/yr "
          f"(real solar system w/ U,N: g5=4.3, g6=28.2)")
    for nm, zll in (("old", z_old), ("new", z_new)):
        dS = np.abs(zll[:, 1] - zsB)
        dJ = np.abs(zll[:, 0] - zjB)
        print(f"    LL-{nm}: max|dz_S|={dS.max():.4f} |z_S|(T)={np.abs(zll[-1, 1]):.4f} "
              f"max|dz_J|={dJ.max():.4f} |z_J|(T)={np.abs(zll[-1, 0]):.4f}")
    print(f"    exact: |z_S|(T)={np.abs(zsB[-1]):.4f} |z_J|(T)={np.abs(zjB[-1]):.4f}")

    # [E] shipped runs' planet histories
    import os
    for pfx in ("truth", "conv", "kick"):
        f = f"{pfx}_zp.npz"
        if not os.path.exists(f):
            print(f"[E] {pfx}: not finished yet")
            continue
        zp = np.load(f)["z"]                    # (nst, 2) complex64, [J, S]
        dS = np.abs(zp[:, 1].astype(complex) - zsB)
        dJ = np.abs(zp[:, 0].astype(complex) - zjB)
        # horizon: first crossing of 5e-3 (10% of Saturn's e scale)
        i5 = np.argmax(dS > 5e-3) if (dS > 5e-3).any() else -1
        print(f"[E] {pfx} zp vs bary: max|dz_S|={dS.max():.2e} max|dz_J|={dJ.max():.2e} "
              f"t(|dz_S|>5e-3)={t[i5] if i5 >= 0 else float('inf'):.0f}")
        print(f"    {pfx} |z_S|: min {np.abs(zp[:, 1]).min():.4f} "
              f"@t={t[np.argmin(np.abs(zp[:, 1]))]:.0f} end {np.abs(zp[-1, 1]):.4f}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "ce":
        main2()
    else:
        main()
