"""R2 selector: which belt bodies may become secular phasors (zero kicks)?

Pre-registered rules, computed ONLY from the planets' parameters (mu, a, e) and each
body's constructed (a, e_free) -- never from the truth run's outcomes.

Units: GM_sun = 1, AU, time unit = 1/(2 pi) yr (n = a^{-1.5}).

Admit body i iff ALL of:
  (S1) mean-motion distance: for every planet P and every reduced rational p/q with
       1 <= q <= 7, |p - q| <= 7 in range:
           |n_i/n_P - p/q| / (p/q)  >=  KAPPA_M * W_pq(e_eff)
       W_pq = C_order(k) * sqrt(mu_P) * e_eff^(k/2),  k = |p - q|,
       e_eff = max(e_free, |z_forced(a)|, 0.02).
  (S2) secular distance: for each planet eigenmode g_k:
           |A(a) - g_k| >= KAPPA_S * |B_k(a)|,  B_k = sum_P B_P(a) V[P,k] c_k-normalized
  (S3) linearity: |z_forced(a)| + e_free <= 0.35.
  (S4) Hill distance at conjunction: (a_P - a_i) >= 3 R_Hill,P.

Formulas validated numerically before the run (see run notes): the a^2-form of A(a)
reproduces both Wisdom-Holman truth (p2, 0.4-3% inner belt) and independent
double-averaged quadrature (0.1% in the e^2 coefficient, 1% in the ee' cross term).
"""
import math
import numpy as np
from scipy.integrate import quad

PLANETS = [
    dict(name="J", mu=9.54e-4, a=5.2026, e=0.0484),
    dict(name="S", mu=2.858e-4, a=9.5370, e=0.0539),
]

A_BELT = (2.0, 3.3)

KAPPA_M = 2.0      # safety factor on MMR half-widths (width model uncertain to ~2x)
KAPPA_S = 2.0      # secular guard in units of the mode coupling
C_ORDER = {1: 1.5, 2: 2.2, 3: 3.5, 4: 3.2}  # calibrated to observed Kirkwood zone half-widths
C_DEFAULT = 2.2
E_FLOOR = 0.02
E_LIN_MAX = 0.35
HILL_FACTOR = 3.0

ARCSEC_PER_UNIT = 206265 * 2 * math.pi  # rad/time-unit -> "/yr

_laplace_cache = {}

def laplace_b(s, j, alpha):
    key = (s, j, round(alpha, 12))
    if key not in _laplace_cache:
        f = lambda p: math.cos(j * p) / (1 - 2 * alpha * math.cos(p) + alpha * alpha) ** s
        _laplace_cache[key] = quad(f, 0, 2 * math.pi, epsabs=1e-14, limit=200)[0] / math.pi
    return _laplace_cache[key]

def planet_matrix():
    """Mutual LL matrix M of the two planets: M[i,i] from b^{(1)}, M[i,j] = -pref b^{(2)}.
    Same convention as wh_run.planet_matrix (v2): inner row alpha^2 b, outer row alpha b
    (quadrupole limit; run 008e used alpha^2 in both rows)."""
    n = np.array([p["a"] ** -1.5 for p in PLANETS])
    M = np.zeros((2, 2))
    for i in range(2):
        for j in range(2):
            if i == j:
                continue
            pi_, pj = PLANETS[i], PLANETS[j]
            alpha = min(pi_["a"], pj["a"]) / max(pi_["a"], pj["a"])
            row_alpha = alpha ** 2 if pi_["a"] < pj["a"] else alpha
            pref = n[i] * pj["mu"] / 4 * row_alpha
            M[i, i] += pref * laplace_b(1.5, 1, alpha)
            M[i, j] = -pref * laplace_b(1.5, 2, alpha)
    return M

def planet_modes():
    """Eigenvalues g (real) and eigenvectors; z_P(t) = sum_k V[P,k] c_k e^{i g_k t}."""
    M = planet_matrix()
    g, V = np.linalg.eig(M)
    assert np.allclose(g.imag, 0, atol=1e-12), g
    g = g.real
    order = np.argsort(g)
    return g[order], V[:, order], np.linalg.inv(V[:, order])

def belt_AB(a):
    """Test-particle A(a) and couplings B_P(a) (interior to both planets)."""
    n = a ** -1.5
    A = 0.0
    BP = np.zeros(2)
    for idx, p in enumerate(PLANETS):
        alpha = a / p["a"]
        pref = n * p["mu"] / 4 * alpha * alpha
        A += pref * laplace_b(1.5, 1, alpha)
        BP[idx] = -pref * laplace_b(1.5, 2, alpha)
    return A, BP

def z_forced(a, g, V, Vinv):
    """LL forced term at t=0 of a test particle driven by the planets' modes."""
    z_pl = np.array([p["e"] for p in PLANETS])
    c = Vinv @ z_pl
    A, BP = belt_AB(a)
    zf = 0.0 + 0j
    for k in range(2):
        zf += complex(BP @ V[:, k]) * c[k] / (A - g[k])
    return zf

def resonances():
    """All reduced p/q (q <= 7, |p - q| <= 7) with n_i/n_P in the belt's range, per planet."""
    n_lo, n_hi = A_BELT[1] ** -1.5, A_BELT[0] ** -1.5   # n decreases with a
    out = []
    for p in PLANETS:
        nP = p["a"] ** -1.5
        r_lo, r_hi = n_lo / nP, n_hi / nP
        for q in range(1, 8):
            for pp in range(math.ceil(r_lo * q), math.floor(r_hi * q) + 1):
                if pp <= 0 or pp - q > 7 or math.gcd(pp, q) != 1:
                    continue
                ratio = pp / q
                if ratio < r_lo * 0.95 or ratio > r_hi * 1.05:
                    continue
                a_res = (ratio * nP) ** (-2 / 3)
                out.append(dict(P=p, p=pp, q=q, k=abs(pp - q), ratio=ratio, a=a_res))
    return out

def mmr_halfwidth(r, e_eff):
    C = C_ORDER.get(r["k"], C_DEFAULT)
    return KAPPA_M * C * math.sqrt(r["P"]["mu"]) * e_eff ** (r["k"] / 2)

def select(a, e_free, g, V, Vinv, res):
    """Returns (admitted, reason)."""
    n = a ** -1.5
    A, BP = belt_AB(a)
    zf = z_forced(a, g, V, Vinv)
    e_eff = max(e_free, abs(zf), E_FLOOR)
    for r in res:
        ratio = n / (r["P"]["a"] ** -1.5)
        dist = abs(ratio / r["ratio"] - 1)
        if dist < mmr_halfwidth(r, e_eff):
            return False, f"mmr {r['p']}:{r['q']}{r['P']['name']}"
    for k in range(2):
        Bk = abs(complex(BP @ V[:, k])) * abs((np.linalg.inv(V) @ np.array([p["e"] for p in PLANETS]))[k])
        if abs(A - g[k]) < KAPPA_S * Bk:
            return False, f"secular g{k + 5}"
    if abs(zf) + e_free > E_LIN_MAX:
        return False, "linear"
    for p in PLANETS:
        rh = p["a"] * (p["mu"] / 3) ** (1 / 3)
        if (p["a"] - a) < HILL_FACTOR * rh:
            return False, "hill"
    return True, ""

if __name__ == "__main__":
    g, V, Vinv, _ = planet_modes()[0], planet_modes()[1], planet_modes()[2], None
    res = resonances()
    print(f"g5 = {g[0] * ARCSEC_PER_UNIT:.2f} \"/yr, g6 = {g[1] * ARCSEC_PER_UNIT:.2f} \"/yr")
    print(f"resonances in range ({len(res)}):")
    for r in sorted(res, key=lambda r: r["a"]):
        print(f"  {r['p']}:{r['q']}{r['P']['name']}  a={r['a']:.3f}  order={r['k']}")
    na, ne = 260, 12
    aes = np.linspace(0.02, 0.23, ne)
    fr = []
    for e in aes:
        cnt = sum(select(a, e, g, V, Vinv, res)[0] for a in np.linspace(*A_BELT, na))
        fr.append(cnt / na)
    fr = np.array(fr)
    print(f"\nadmission fraction (uniform a, e_free grid): mean {fr.mean():.3f}")
    for e, f in zip(aes, fr):
        print(f"  e_free={e:.2f}: {f:.3f}")
    print("\nprofile at e_free=0.1 (A in \"/yr, zf, verdict):")
    for a in np.linspace(2.0, 3.3, 27):
        A, BP = belt_AB(a)
        ok, why = select(a, 0.1, g, V, Vinv, res)
        zf = z_forced(a, g, V, Vinv)
        print(f"  a={a:.3f} A={A * ARCSEC_PER_UNIT:6.2f} zf={abs(zf):.3f} admit={ok} {why}")
