#!/usr/bin/env python3
"""H_live of a quiet belt: entropy of the scar field (deviation from the birth program).

Sun + Jupiter-like secondary (test-particle WH: exact Kepler drift about the Sun, direct +
indirect tide kicks from Jupiter, Jupiter exact two-body). Floats explore; this measures an
information floor, never a canonical outcome. 2D planar, AU/yr, GM_sun = 4 pi^2.
"""
import json
import zlib
import numpy as np
from scipy.spatial import cKDTree

MU = 4.0 * np.pi * np.pi            # GM_sun
MJ = 9.54e-4                        # Jupiter mass / Sun
MUJ = MU * MJ
MUJ2 = MU * (1.0 + MJ)              # Sun-Jupiter two-body

RNG = np.random.default_rng(20261007)

def _stumpff(z):
    """Branchless Stumpff C(z), S(z)."""
    zs = np.where(z == 0.0, 1.0, z)
    sz = np.sqrt(np.abs(z))
    sz3 = np.where(sz == 0.0, 1.0, sz) ** 3
    C = np.where(z > 0, (1.0 - np.cos(sz)) / zs, (np.cosh(sz) - 1.0) / (-zs))
    S = np.where(z > 0, (sz - np.sin(sz)) / (zs * sz), (np.sinh(sz) - sz) / sz3)
    return C, S

def kepler_drift(x, y, vx, vy, dt, mu):
    """Universal-variable f&g Kepler drift (vectorized). Advance (x,y,vx,vy) by dt."""
    r0 = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    rv = x * vx + y * vy
    alpha = 2.0 / r0 - v2 / mu       # 1/a
    sqmu = np.sqrt(mu)
    chi = sqmu * np.abs(dt) * alpha  # warm start (ellipse)
    chi = np.where(chi == 0.0, sqmu * dt / r0, chi)
    for _ in range(5):
        C, S = _stumpff(alpha * chi * chi)
        F = (rv / sqmu) * chi * chi * C + (1.0 - alpha * r0) * chi ** 3 * S + r0 * chi - sqmu * dt
        dF = chi * chi * C + (1.0 - alpha * r0) * chi ** 3 * S + r0  # = r
        chi = chi - F / dF
    C, S = _stumpff(alpha * chi * chi)
    f = 1.0 - chi * chi / r0 * C
    g = dt - chi ** 3 * S / sqmu
    nx = f * x + g * vx
    ny = f * y + g * vy
    r1 = np.hypot(nx, ny)
    gdot = 1.0 - chi * chi / r1 * C
    fdot = (sqmu / (r0 * r1)) * chi * (alpha * chi * chi * S - 1.0)
    nvx = fdot * x + gdot * vx
    nvy = fdot * y + gdot * vy
    return nx, ny, nvx, nvy

def elements(x, y, vx, vy, mu):
    r = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / r - v2 / mu)
    ex = ((v2 - mu / r) * x - (x * vx + y * vy) * vx) / mu
    ey = ((v2 - mu / r) * y - (x * vx + y * vy) * vy) / mu
    return a, ex, ey

def ent(vals):
    _, c = np.unique(vals, return_counts=True)
    p = c / c.sum()
    return float(-(p * np.log2(p)).sum())

def bits_by_zlib(arrs):
    raw = b"".join(a.astype(np.int32).tobytes() for a in arrs)
    return 8.0 * len(zlib.compress(raw, 9)) / len(arrs[0])

def quant(v, g):
    return np.round(v / g).astype(np.int64)

def analyze(t, birth, cur, a0, grids, tag, out):
    da = (cur[0] - birth[0]) / birth[0]                 # Δa/a
    dex = cur[1] - birth[1]                             # Δ(e cos ϖ)
    dey = cur[2] - birth[2]                             # Δ(e sin ϖ)
    ex0, ey0 = birth[1], birth[2]
    # generator floor: kNN in birth state (a, free e-vector); a program + the shared
    # ephemeris re-derives a smooth function of birth state.
    scale = np.array([1.0 / 0.5, 1.0 / 0.01, 1.0 / 0.01])
    pts = np.stack([a0 - 1.0, ex0, ey0], 1) * scale
    tree = cKDTree(pts)
    _, nn = tree.query(pts, k=9)
    nn = nn[:, 1:]                                      # drop self
    res = {}
    for gname, (gd, ge) in grids.items():
        qa, qx, qy = quant(da, gd), quant(dex, ge), quant(dey, ge)
        scarred = (qa != 0) | (qx != 0) | (qy != 0)
        ka, kx, ky = (np.median(qa[nn], 1).round().astype(np.int64),
                      np.median(qx[nn], 1).round().astype(np.int64),
                      np.median(qy[nn], 1).round().astype(np.int64))
        ra, rx, ry = qa - ka, qx - kx, qy - ky
        med3 = np.median(np.abs(ra)) + np.median(np.abs(rx)) + np.median(np.abs(ry))
        p999 = (np.percentile(np.abs(ra), 99.9) + np.percentile(np.abs(rx), 99.9)
                + np.percentile(np.abs(ry), 99.9))
        H_raw = ent(qa) + ent(qx) + ent(qy)
        H_res = ent(ra) + ent(rx) + ent(ry)
        z_raw = bits_by_zlib([qa, qx, qy])
        z_res = bits_by_zlib([ra, rx, ry]) + 3 * 8 * 8 / len(a0)
        res[gname] = dict(scarred=float(scarred.mean()), H_raw=H_raw, H_knn=H_res,
                          zlib_raw=z_raw, zlib_knn=z_res,
                          res_med_quanta=float(med3), res_p999_quanta=float(p999))
    out[tag] = res
    print(f"t={t:7.2f} yr  " + "  ".join(
        f"[{g}] sc={v['scarred']:.3f} Hraw={v['H_raw']:6.2f} Hknn={v['H_knn']:5.2f} "
        f"zraw={v['zlib_raw']:5.2f} zknn={v['zlib_knn']:5.2f} med={v['res_med_quanta']:4.1f} "
        f"p999={v['res_p999_quanta']:7.1f}"
        for g, v in res.items()), flush=True)

def run_scene(name, N, sig_e, T, dt, outs):
    print(f"=== scene {name}: N={N} sigma_e={sig_e} T={T} dt={dt} ===", flush=True)
    a0 = RNG.uniform(1.0, 1.5, N)
    e0 = RNG.rayleigh(sig_e, N)
    w0 = RNG.uniform(-np.pi, np.pi, N)
    M0 = RNG.uniform(-np.pi, np.pi, N)
    E0 = M0.copy()
    for _ in range(10):
        E0 = M0 + e0 * np.sin(E0)
    cE, sE = np.cos(E0), np.sin(E0)
    x = a0 * (cE - e0); yy = a0 * np.sqrt(1.0 - e0 * e0) * sE
    cw, sw = np.cos(w0), np.sin(w0)
    x, yy = x * cw - yy * sw, x * sw + yy * cw
    denom = 1.0 - e0 * cE
    vx0 = -np.sqrt(MU / a0) * sE / denom
    vy0 = np.sqrt(MU / a0) * np.sqrt(1.0 - e0 * e0) * cE / denom
    vx, vy = vx0 * cw - vy0 * sw, vx0 * sw + vy0 * cw
    # Jupiter at periapsis
    aJ, eJ = 5.2, 0.048
    xJ, yJ = aJ * (1 - eJ), 0.0
    vJ = np.sqrt(MU / aJ * (1 + eJ) / (1 - eJ))
    vxJ, vyJ = 0.0, vJ
    birth = elements(x, yy, vx, vy, MU)
    out = {}
    grids = {"g20": (2.0**-20, 2.0**-20), "g24": (2.0**-24, 2.0**-24), "g28": (2.0**-28, 2.0**-28)}
    oset = set(outs)
    t = 0.0
    steps = int(round(T / dt))
    for s in range(steps + 1):
        if s in oset or s == 0:
            analyze(t, birth, elements(x, yy, vx, vy, MU), a0, grids, f"{name}@{s}", out)
        if s == steps:
            break
        dx, dy = x - xJ, yy - yJ
        d3 = (dx * dx + dy * dy) ** 1.5
        rJ3 = (xJ * xJ + yJ * yJ) ** 1.5
        ax = MUJ * (-dx / d3 - xJ / rJ3)
        ay = MUJ * (-dy / d3 - yJ / rJ3)
        vx += 0.5 * dt * ax; vy += 0.5 * dt * ay
        x, yy, vx, vy = kepler_drift(x, yy, vx, vy, dt, MU)
        xJ, yJ, vxJ, vyJ = kepler_drift(xJ, yJ, vxJ, vyJ, dt, MUJ2)
        dx, dy = x - xJ, yy - yJ
        d3 = (dx * dx + dy * dy) ** 1.5
        rJ3 = (xJ * xJ + yJ * yJ) ** 1.5
        ax = MUJ * (-dx / d3 - xJ / rJ3)
        ay = MUJ * (-dy / d3 - yJ / rJ3)
        vx += 0.5 * dt * ax; vy += 0.5 * dt * ay
        t += dt
    return out

if __name__ == "__main__":
    res = {}
    dt = 1.0 / 32.0
    res["main"] = run_scene("main", 8192, 0.01, 100.0, dt, [32, 96, 320, 960, 3200])
    res["tail"] = run_scene("tail", 8192, 0.1, 30.0, dt, [32, 96, 320, 960])
    with open("lab/results/20261007-1334-quant-7334/hlive.json", "w") as f:
        json.dump(res, f, indent=1)
    print("saved hlive.json")
