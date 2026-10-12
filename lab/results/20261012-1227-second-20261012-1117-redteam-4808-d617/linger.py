"""E3: linger — residence time in the band and multiply-add drift accrued.

Bodies seeded as captures put them there (mu in (0.05, 0.3]); random-sign kicks
dL/L = 1e-4 at periapsis (the fixed-u_p family); absorbed at mu <= 0 (plunge,
roots merged) or mu > 3 (out of the near-separatrix region).  The drift is the
shipped jet's error (law.md: exact offset plus stored derivatives, re-anchored
at 730 quanta of accumulated offset) against exact GR, accrued per kick.
Also: entry from above — seeds at mu in (0.3, 0.6), fraction ever entering the
band.
"""
import numpy as np, sys
sys.path.insert(0, '.')
from cycle import *
from scipy.interpolate import CubicSpline

rng = np.random.default_rng(617)
S = 1e-4
TRIGGER = 730.0 * S
NW = 4096
MAXK = 2_000_000

def run(e, mu_lo, mu_hi, n=NW):
    up, L0 = seed_from_pe(6 + 2 * e + 0.3, e)      # fixes u_p of the family
    fam = build_family(up)
    Lg, mug, dg = fam["L"], fam["mu"], fam["dphi"]
    dphi_s = CubicSpline(Lg, dg)
    dd_s = CubicSpline(Lg, fam["ddphi"])
    mu_s = CubicSpline(Lg, mug)
    Lsep = fam["L_sep"]
    # seed L from mu target
    Lseed = np.interp(rng.uniform(mu_lo, mu_hi, n), mug, Lg)
    L = Lseed.copy(); La = L.copy()
    steps = np.zeros(n, dtype=np.int64)
    drift = np.zeros(n); n_re = np.zeros(n, dtype=np.int64)
    fate = np.full(n, -1)                          # 0 plunge, 3 escape, 2 censored
    active = np.ones(n, dtype=bool)
    for k in range(MAXK):
        idx = np.flatnonzero(active)
        if idx.size == 0: break
        Lk = L[idx]; Lak = La[idx]
        # cycle runs at Lk: jet error accrues
        drift[idx] += (dphi_s(Lak) + dd_s(Lak) * (Lk - Lak)) - dphi_s(Lk)
        # kick
        L[idx] = Lk * (1 + S * rng.choice((-1.0, 1.0), idx.size))
        re = np.abs(L[idx] - Lak) / Lak > TRIGGER
        La[idx[re]] = L[idx[re]]; n_re[idx[re]] += 1
        steps[idx] += 1
        Ek = E_of(up, L[idx])
        mu = mu_s(L[idx])
        died = (mu <= 1e-6) | ~np.isfinite(mu)   # region lost: plunge
        esc = (Ek >= 1.0) | (mu > 3.0)           # unbound or far above band
        fate[idx[died & ~esc]] = 0; fate[idx[esc & ~died]] = 3
        active[idx[died | esc]] = False
    fate[active] = 2
    return dict(steps=steps, drift=drift, fate=fate, n_re=n_re, Lsep=Lsep,
                fam_e=fam["e0"])

for e in [0.9, 0.99]:
    r = run(e, 0.05, 0.3)
    st, dr, fa = r["steps"], r["drift"], r["fate"]
    print(f"== e={e}: seeds mu in (0.05,0.3] (in-band births), n={NW} ==")
    print(f"  fates: plunge={np.mean(fa==0):.3f} escape(mu>3)={np.mean(fa==3):.3f} censored@{MAXK}={np.mean(fa==2):.3f}")
    print(f"  residence kicks: median={np.median(st):.3g} mean={st.mean():.3g} p90={np.percentile(st,90):.3g}")
    print(f"  drift while resident (rad): median={np.median(dr):.3g} p90={np.percentile(dr,90):.3g} max={dr.max():.3g}")
    print(f"  re-anchors per body: median={np.median(r['n_re']):.3g} max={r['n_re'].max()}")
    print(f"  budget B (5e-3 rad) exceeded by {np.mean(np.abs(dr)>5e-3):.3f} of bodies")

print()
for e in [0.9, 0.99]:
    r = run(e, 0.3, 0.6)
    st, fa = r["steps"], r["fate"]
    print(f"== e={e}: seeds mu in (0.3,0.6] (entry from above), n={NW} ==")
    print(f"  fates: plunge={np.mean(fa==0):.3f} escape={np.mean(fa==3):.3f} censored={np.mean(fa==2):.3f}")
    # entry into the band must be inferred from min mu visited; re-run cheaply:
    # (a walker that plunged necessarily crossed the band)
    print(f"  => fraction that ever entered the band = fraction that plunged (mu<=0 crossing)")
