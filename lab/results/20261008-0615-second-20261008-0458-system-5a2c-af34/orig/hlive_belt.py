"""H_live in a belt: what mints memory distinctions?

Static-program scar billing (naive) vs shared-record split rate (true information),
under a Jupiter-like secondary. Keys follow crates/space's memo quantization:
12 relative bits of scale (r_p) and 12 of shape (1-e gap).

Arms: originals, twins at +0.4 quantum, twins at +0.1 quantum in log2(r_p).
Shear (smooth, re-absorbable) separates proportionally to the offset; chaos
saturates both arms to the same separation.

Run:  python3 hlive_belt.py main   -> the decisive run (predictions.md)
      python3 hlive_belt.py dtest  -> cadence invariance (dt vs dt/2)
"""
import sys
import numpy as np

GM = 4.0 * np.pi ** 2          # AU^3 / yr^2 (G * M_sun)
MU_J = 9.5459e-4               # Jupiter mass ratio
A_J, E_J = 5.2044, 0.0489      # Jupiter orbit
PJ = 2 * np.pi / np.sqrt(GM * (1 + MU_J) / A_J ** 3)


def belt(n, rng):
    """Bodies in three arms: originals, twins at +0.4 quantum, twins at +0.1 quantum."""
    m = n // 3
    a = rng.uniform(2.1, 3.3, m)
    e = np.minimum(rng.rayleigh(0.07, m), 0.35)
    lam = rng.uniform(0, 2 * np.pi, m)
    varpi = rng.uniform(0, 2 * np.pi, m)
    rp = a * (1 - e)
    arms = [rp * 2.0 ** (q * 2.0 ** -12) / (1 - e) for q in (0.0, 0.4, 0.1)]
    a_all = np.concatenate(arms)
    e_all = np.concatenate([e, e, e])
    lam_all = np.concatenate([lam, lam, lam])
    varpi_all = np.concatenate([varpi, varpi, varpi])
    return a_all, e_all, lam_all, varpi_all, m


def state(a, e, lam, varpi):
    """Planar Kepler state from elements (M from mean longitude)."""
    M = (lam - varpi) % (2 * np.pi)
    E = M.copy()
    for _ in range(8):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    cE, sE = np.cos(E), np.sin(E)
    r = a * (1 - e * cE)
    xo, yo = a * (cE - e), a * np.sqrt(1 - e ** 2) * sE
    cw, sw = np.cos(varpi), np.sin(varpi)
    x, y = xo * cw - yo * sw, xo * sw + yo * cw
    n = np.sqrt(GM / a ** 3)
    fac = n * a * a / r
    vxo, vyo = -fac * sE, fac * np.sqrt(1 - e ** 2) * cE
    vx, vy = vxo * cw - vyo * sw, vxo * sw + vyo * cw
    return np.stack([x, y, vx, vy])


def jup(t):
    nJ = np.sqrt(GM * (1 + MU_J) / A_J ** 3)
    M = nJ * t
    E = M.copy()
    for _ in range(8):
        E = E - (E - E_J * np.sin(E) - M) / (1 - E_J * np.cos(E))
    cE, sE = np.cos(E), np.sin(E)
    x, y = A_J * (cE - E_J), A_J * np.sqrt(1 - E_J ** 2) * sE
    return x, y


def accel(x, y, xj, yj):
    r2 = x * x + y * y
    r = np.sqrt(r2)
    ax = -GM * x / (r * r2)
    ay = -GM * y / (r * r2)
    dx, dy = x - xj, y - yj
    d2 = dx * dx + dy * dy
    d = np.sqrt(d2)
    k = MU_J * GM / (d * d2)
    return ax - k * dx, ay - k * dy


def elements(x, y, vx, vy):
    """Osculating (a, e) from a heliocentric planar state."""
    r = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    en = 0.5 * v2 - GM / r
    a = -GM / (2 * en)
    lz = x * vy - y * vx
    ex = (vy * lz) / GM - x / r
    ey = (-vx * lz) / GM - y / r
    return a, np.hypot(ex, ey)


def keys(a, e):
    rp = a * (1.0 - e)
    ks = np.round(np.log2(np.maximum(rp, 1e-9)) * 2.0 ** 12).astype(np.int64)
    kh = np.round(np.log2(np.maximum(1.0 - e, 1e-9)) * 2.0 ** 12).astype(np.int64)
    return ks, kh

def run(n, T, steps_per_PJ, seed=7, checkpoints=None, quiet=False, extras=True):
    n = 3 * (n // 3)
    rng = np.random.default_rng(seed)
    a0, e0, lam, varpi, m = belt(n, rng)
    s = state(a0, e0, lam, varpi)
    dt = PJ / steps_per_PJ
    nst = int(round(T / dt))
    ks0, kh0 = keys(a0, e0)
    prev = (ks0.copy(), kh0.copy())
    crossings = np.zeros(n, np.int64)
    same4 = (ks0[0:m] == ks0[m:2 * m]) & (kh0[0:m] == kh0[m:2 * m])
    same1 = (ks0[0:m] == ks0[2 * m:3 * m]) & (kh0[0:m] == kh0[2 * m:3 * m])
    # checkpoints: roughly geometric from 1 to nst, always including 0 and nst
    if checkpoints is None:
        checkpoints = sorted(set(np.unique(np.round(np.geomspace(1, nst, 30)).astype(int)).tolist()) | {0, int(nst)})
    rows = []
    t = 0.0
    ci = 0
    for step in range(nst + 1):
        if ci < len(checkpoints) and step == checkpoints[ci]:
            ci += 1
            a, e = elements(s[0], s[1], s[2], s[3])
            ks, kh = keys(a, e)
            crossings += (np.abs(ks - prev[0]) > 0).astype(np.int64)
            crossings += (np.abs(kh - prev[1]) > 0).astype(np.int64)
            prev = (ks, kh)
            off = (ks != ks0) | (kh != kh0)
            dk4 = np.abs(ks[0:m] - ks[m:2 * m]) + np.abs(kh[0:m] - kh[m:2 * m])
            dk1 = np.abs(ks[0:m] - ks[2 * m:3 * m]) + np.abs(kh[0:m] - kh[2 * m:3 * m])
            rows.append(dict(
                t=t, orbits=t / (2 * np.pi * 2.7 ** 1.5 / np.sqrt(GM)),
                frac_off=float(off[0:m].mean()),
                cross_per_body=float(crossings[0:m].mean()),
                split4=float((dk4[same4] >= 2).mean()) if same4.any() else 0.0,
                split1=float((dk1[same1] >= 2).mean()) if same1.any() else 0.0,
                med4=float(np.median(dk4[same4])) if same4.any() else 0.0,
                med1=float(np.median(dk1[same1])) if same1.any() else 0.0,
                p90_4=float(np.percentile(dk4[same4], 90)) if same4.any() else 0.0,
                p90_1=float(np.percentile(dk1[same1], 90)) if same1.any() else 0.0,
            ))
            if not quiet:
                r = rows[-1]
                print(f"t={r['t']:7.1f} orb={r['orbits']:6.1f} off={r['frac_off']*100:5.1f}% "
                      f"cr/b={r['cross_per_body']:8.1f} | s4={r['split4']*100:5.1f}% m4={r['med4']:4.1f} "
                      f"p90_4={r['p90_4']:5.1f} | s1={r['split1']*100:5.1f}% m1={r['med1']:4.1f} "
                      f"p90_1={r['p90_1']:5.1f}", flush=True)
        if step == nst:
            break
        xj, yj = jup(t + dt / 2)
        s[0] += s[2] * dt / 2
        s[1] += s[3] * dt / 2
        ax, ay = accel(s[0], s[1], xj, yj)
        s[2] += ax * dt
        s[3] += ay * dt
        s[0] += s[2] * dt / 2
        s[1] += s[3] * dt / 2
        t += dt
    if not extras:
        return rows, None, None
    a, e = elements(s[0], s[1], s[2], s[3])
    ks, kh = keys(a, e)
    key = ks * (1 << 20) + kh
    dk4 = np.abs(ks[0:m] - ks[m:2 * m]) + np.abs(kh[0:m] - kh[m:2 * m])
    occ = []
    rng2 = np.random.default_rng(11)
    for nn in (1024, 2048, 4096, 8192, 16384):
        idx = rng2.choice(m, min(nn, m), replace=False)
        occ.append((nn, len(np.unique(key[idx]))))
    bands = np.linspace(2.1, 3.3, 13)
    prof = []
    for lo, hi in zip(bands[:-1], bands[1:]):
        sel = (a0[0:m] >= lo) & (a0[0:m] < hi) & same4
        if sel.sum() >= 5:
            prof.append((0.5 * (lo + hi), int(sel.sum()), float((dk4[sel] >= 2).mean())))
    return rows, occ, prof


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "main"
    if mode == "dtest":
        for sp in (150, 300):
            rows, _, _ = run(6144, T=1200.0, steps_per_PJ=sp, seed=5,
                             checkpoints=sorted(set(np.unique(np.linspace(0, 15200, 8).astype(int)))),
                             extras=False)
            r = rows[-1]
            print(f"dt PJ/{sp}: cross/body={r['cross_per_body']:.1f} off={r['frac_off']*100:.1f}% "
                  f"split4={r['split4']*100:.1f}% split1={r['split1']*100:.1f}% "
                  f"med4={r['med4']:.1f} med1={r['med1']:.1f}")
        sys.exit(0)
    rows, occ, prof = run(16384, T=2400.0, steps_per_PJ=150)
    print("occupancy (subsample size, distinct keys):", occ)
    print("twin split profile by birth a (a_mid, pairs, frac split>=2q):")
    for a_mid, k, f in prof:
        print(f"  a={a_mid:.2f} n={k:4d} split={f*100:5.2f}%")
    ns = np.array([o[0] for o in occ], float)
    ks_ = np.array([o[1] for o in occ], float)
    sl = np.polyfit(np.log(ns), np.log(ks_), 1)[0]
    print(f"distinct-key growth exponent vs N: {sl:.2f}  (linear=1)")
    b = sl
    c = ks_[-1] / ns[-1] ** b
    for N in (1e6, 1e8, 1e9):
        print(f"  projected distinct keys at N={N:.0e}: {c*N**b:.3e}")
    # separation growth law: median separation vs t (shear=power law, chaos=exp)
    ts = np.array([r["orbits"] for r in rows if r["orbits"] > 1])
    m4 = np.array([r["med4"] for r in rows if r["orbits"] > 1])
    p4 = np.array([r["p90_4"] for r in rows if r["orbits"] > 1])
    ok = m4 > 0
    if ok.sum() > 3:
        pw = np.polyfit(np.log(ts[ok]), np.log(m4[ok]), 1)[0]
        print(f"median twin separation growth: sep ~ orbits^{pw:.2f} (shear~1, chaos~exp)")
