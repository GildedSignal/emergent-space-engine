import numpy as np, sys
sys.path.insert(0, ".")
from replica import *

# star GM=1; two planets (Home-like mu=2^-18 is too weak; use mu=2^-10 'Giant' and
# mu=2^-13) so the perturbation is visible. Plane-faithful: star fixed, direct pulls.
GM_S = 1.0
mus = np.array([1e-3, 3e-3])
a_s = np.array([1.0, 1.6])
e_s = np.array([0.05, 0.02])
w_s = np.array([0.3, 2.1])
M_s = np.array([0.2, 4.0])
P = TWOPI * np.sqrt(a_s ** 3 / GM_S)
Pmin = P.min()

st0 = np.stack([state_from_elements(GM_S, a_s[i], e_s[i], w_s[i], M_s[i] * 0 + 1.0) for i in range(2)])

def accel(st, t):
    # direct pulls between the two planets (plane: doll-0 secondaries)
    d = st[0, :2] - st[1, :2]
    r = np.linalg.norm(d)
    a0 = -mus[1] * d / r ** 3
    a1 = mus[0] * d / r ** 3
    return np.stack([a0, a1])

def energy(st):
    r = np.linalg.norm(st[:, :2], axis=1)
    v2 = np.sum(st[:, 2:] ** 2, axis=1)
    E = np.sum(0.5 * mus * v2 - mus * GM_S / r)
    d = np.linalg.norm(st[0, :2] - st[1, :2])
    return E - mus[0] * mus[1] / d

E0 = energy(st0)
Norb = 30
print("scheme k kicks/orbit  max|dE|     growth-order")
res = {}
for scheme in ["dkd", "saba2", "saba3", "whc3", "whc5"]:
    for k in [3, 4, 5, 6]:
        it = Integrator(scheme, [GM_S, GM_S], accel)
        st = st0.copy()
        nst = Norb * int(Pmin / (Pmin / 2 ** k) * 1)  # steps for Norb inner orbits
        nst = int(np.round(Norb * Pmin / (Pmin / 2 ** k)))
        err = 0.0
        for i in range(nst):
            st = it.step(st, Pmin / 2 ** k)
            if i % 64 == 0 or i == nst - 1:
                err = max(err, abs(energy(st) - E0))
        kicks_per_orbit = KICKS_PER_STEP[scheme] * 2 ** k
        res[(scheme, k)] = err
        print(f"{scheme:6s} {k}  {kicks_per_orbit:4d}     {err:.3e}")
print("\nstep-halving slope (log2 err ratio) per scheme:")
for scheme in ["dkd", "saba2", "saba3", "whc3", "whc5"]:
    sl = [np.log2(res[(scheme, k)] / res[(scheme, k - 1)]) for k in [4, 5, 6] if res[(scheme, k)] > 0 and res[(scheme, k - 1)] > 0]
    print(f"{scheme:6s} {[f'{x:+.1f}' for x in sl]}  (expect ~2 dkd, ~2 whc3(smaller), ~4 saba)")
