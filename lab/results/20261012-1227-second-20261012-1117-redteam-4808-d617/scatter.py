"""E2: the checker's named experiment — do encounters park bodies in the band?

Toy: parabolic bodies (E=1) with periapsis rp uniform in a window near the
hole; ONE impulsive encounter at periapsis, local speed kick k*v_p (v_p =
sqrt(2/rp) exactly), direction uniform.  Exact (E, L) from the local-velocity
map; fates: plunge / band (0 < mu <= 0.3) / bound wider / unbound.
Second channel: bound parents (p = p_crit + 1, e = 0.9) kicked at periapsis
(a battle's ships scattering each other).
"""
import numpy as np, sys
sys.path.insert(0, '.')
from cycle import *

rng = np.random.default_rng(1227)
N = 100_000
BAND = 0.3

def run_parabolic(rp_lo, rp_hi, k, n=N):
    rp = rng.uniform(rp_lo, rp_hi, n)
    u, vt, E0, L0 = parabolic_periapsis_state(rp)
    al = rng.uniform(0, 2 * np.pi, n)
    dv = k * vt
    vt2, vr2 = vt + dv * np.cos(al), dv * np.sin(al)
    E, L = kick_E_L(u, vt2, vr2)
    assert np.all(vt2**2 + vr2**2 < 1.0), "kick exceeds c"
    fate, mu, p, e = classify(E, L, u, BAND)
    cap = (fate == 1) | (fate == 2)
    out = dict(
        plunge=np.mean(fate == 0), band=np.mean(fate == 1),
        bound=np.mean(fate == 2), unbound=np.mean(fate == 3),
        band_giv_cap=np.mean(fate[cap] == 1),
        e_band=(np.min(e[fate == 1]), np.max(e[fate == 1])) if (fate == 1).any() else (np.nan,)*2,
        rp_band=(np.min(rp[fate == 1]), np.percentile(rp[fate == 1], 50), np.max(rp[fate == 1])) if (fate == 1).any() else (np.nan,)*3,
        n_cap=int(cap.sum()),
    )
    return out

print("== parabolic captures: fate fractions (N=1e5 each) ==")
print("rp window    k      plunge  band   bound  unbind  band|captured  band e-range   band rp (min/med/max)")
for (lo, hi) in [(4.0, 8.0), (4.0, 6.0), (4.0, 4.5), (5.0, 8.0)]:
    for k in [1e-4, 1e-3, 1e-2, 3e-2, 1e-1]:
        r = run_parabolic(lo, hi, k)
        print(f"[{lo},{hi}]    {k:6.0e}  {r['plunge']:6.3f} {r['band']:6.3f} {r['bound']:6.3f} "
              f"{r['unbound']:6.3f}  {r['band_giv_cap']:8.3f}     "
              f"[{r['e_band'][0]:.3f},{r['e_band'][1]:.3f}]  "
              f"{r['rp_band'][0]:.2f}/{r['rp_band'][1]:.2f}/{r['rp_band'][2]:.2f}")

print("\n== band|captured vs k, fine sweep, rp in [4,8] ==")
for k in [1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1]:
    r = run_parabolic(4.0, 8.0, k)
    print(f"  k={k:6.0e}: captured={r['n_cap']:6d}  band|cap={r['band_giv_cap']:6.3f}  plunge={r['plunge']:6.3f}")

print("\n== second channel: bound parents (p = p_crit+1, e = 0.9) kicked at periapsis ==")
for k in [1e-2, 3e-2, 1e-1]:
    up, L0 = seed_from_pe(6 + 2 * 0.9 + 1.0, 0.9)
    u = up
    E0 = E_of(up, L0)
    # local velocity at periapsis of a bound orbit: from (E, L)
    # v_t = L u sqrt(1-2u)/E ; v_r = 0 (periapsis)
    vt = L0 * u * np.sqrt(1 - 2 * u) / E0
    n = 200_000
    al = rng.uniform(0, 2 * np.pi, n)
    dv = k * vt
    vt2, vr2 = np.full(n, vt) + dv * np.cos(al), dv * np.sin(al)
    E, L = kick_E_L(np.full(n, u), vt2, vr2)
    fate, mu, p, e = classify(E, L, np.full(n, u), BAND)
    cap = (fate == 1) | (fate == 2)
    print(f"  k={k:6.0e}: plunge={np.mean(fate==0):6.3f} band={np.mean(fate==1):6.3f} "
          f"bound={np.mean(fate==2):6.3f} unbound={np.mean(fate==3):6.3f} "
          f"band|cap={np.mean(fate[cap]==1):6.3f}")
