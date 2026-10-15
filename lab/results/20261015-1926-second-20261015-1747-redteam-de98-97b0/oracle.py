#!/usr/bin/env python3
"""Second author on 20261015-1747-redteam-de98: the adjudicating oracle.

The checker's named gap: "the adjudicating oracle is missing" — a resummed,
ν→0-exact EOB evaluated at matched real invariants on p̄∈[8,50], plus regenerable
controls. This script is that oracle plus the record fixes.

Oracle: 3PN EOB from primary sources (fetched this run, see dossier):
  Damour arXiv:1212.3169 (lectures), eq. 17 & around:
    A(u) = 1 − 2u + 2νu³ + a₄νu⁴,   a₄ = 94/3 − 41π²/32
    D(u) ≡ A(u)B(u) = 1 − 6νu² + 2(3ν−26)νu³,   D(ν→0) = 1
    Q: z₁ = z₂ = 0, z₃ = 2ν(4−3ν)  (quartic mass-shell deformation)
  eqs. 24–25: Ĥ_EOB = (1/ν)√(1+2ν(Ĥ_eff−1)); tortoise P_{R*} = (A/B)^{1/2}P_R
    (stated in the text: R* = ∫dR(B/A)^{1/2}), so in canonical areal (r, p_r):
    Ĥ_eff² = (A²/D)p_r² + A(1+j²u²) + z₃u²(A⁵/D²)p_r⁴.
  The EOB energy map IS the design's map (r3 v3 / representation.md §1):
  Ĥ_eff = 1 + ĥ + (ν/2)ĥ² — the same inversion de98 used for the doll. At matched
  real invariants the doll (geodesic of A₀ = 1−2u) and the EOB therefore share the
  SAME effective (E, j): the difference is the potential alone, and no baseline
  subtraction is needed (the ν→0 error is machine zero by construction).
  4PN-fit bracket: A += ν(a₅c + a₅log·ln u)u⁵, a₅c = 23.5 (fiducial, GSF-informed),
  a₅log = 64/5 — Damour–Nagar arXiv:1406.6913 eqs. 28–29. Bracket only.

Doll, DJS-2PN reference, labels, quadratures: de98's eob_doll.py verbatim (its
instrument was checker-validated: RK 6.5e-12 doll, φ-parametrized ADM RK 2e-12).

Conventions compared:
  conv_de98  labels owned by the DJS orbit's turning points (de98's grid), matched
             real invariants (ĥ, j).
  conv_doll  labels owned by the doll's geodesic turning points (the shipped law's
             own orbit), same matched-invariants comparison.
  conv_tp    ecfd's form: identical geometric turning points for both orbits.

History this run discloses (de98's predictions.md promised an EOB reference and the
shipped instrument switched to DJS-ADM undisclosed; the checker flagged it): both
instruments are now in one record.
"""
import json
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, fsolve

EPS = 1e-30
A4 = 94.0 / 3.0 - 41.0 * np.pi ** 2 / 32.0   # Damour 1212.3169 eq. 17
A5C, A5LOG = 23.5, 64.0 / 5.0                # Damour-Nagar 1406.6913 eqs. 28-29


# ---------------------------------------------------------------- de98 verbatim
def H_adm(r, pr, j, nu, order=2):
    p2 = pr * pr + j * j / (r * r)
    H = 0.5 * p2 - 1.0 / r
    H = H + (3 * nu - 1) * p2**2 / 8.0 - ((3 + nu) * p2 + nu * pr * pr) / (2.0 * r) + 1.0 / (2 * r * r)
    if order >= 2:
        H2 = (1 - 5 * nu + 5 * nu * nu) * p2**3 / 16.0
        H2 += ((5 - 20 * nu - 3 * nu * nu) * p2**2 - 2 * nu * nu * pr * pr * p2
               - 3 * nu * nu * pr**4) / (8.0 * r)
        H2 += ((5 + 8 * nu) * p2 + 3 * nu * pr * pr) / (2.0 * r * r)
        H2 -= (1 + 3 * nu) / (4.0 * r**3)
        H = H + H2
    return H


def dH(which, r, pr, j, nu, order):
    if which == "j":
        return H_adm(r, pr, j + EPS * 1j, nu, order).imag / EPS
    if which == "r":
        return H_adm(r + EPS * 1j, pr, j, nu, order).imag / EPS
    return H_adm(r, pr + EPS * 1j, j, nu, order).imag / EPS


def newton_turning_guesses(hhat, j):
    disc = np.sqrt(1.0 + 2.0 * hhat * j * j)
    ra = (-1.0 - disc) / (2.0 * hhat)
    rp = (-1.0 + disc) / (2.0 * hhat)
    return rp, ra


def solve_turning(g, rp0, ra0):
    try:
        rp = brentq(g, 0.6 * rp0, min(1.4 * rp0, rp0 + 0.35 * (ra0 - rp0)), xtol=1e-14, rtol=1e-15)
        ra = brentq(g, max(0.6 * ra0, ra0 - 0.35 * (ra0 - rp0)), 1.4 * ra0, xtol=1e-14, rtol=1e-15)
    except ValueError:
        return None
    if ra <= rp * 1.0000001:
        return None
    mid = 0.5 * (rp + ra)
    if g(mid) > 0:
        return None
    return rp, ra


def pr_of_r(r, hhat, j, nu, order):
    f = lambda pr: H_adm(r, pr, j, nu, order) - hhat
    lo, hi = 0.0, 30.0
    if f(lo) > 0 or f(hi) < 0:
        return None
    for _ in range(64):
        mid = 0.5 * (lo + hi)
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def adm_k_T(hhat, j, nu, order=2):
    g = lambda r: H_adm(r, 0.0, j, nu, order) - hhat
    rp0, ra0 = newton_turning_guesses(hhat, j)
    if hhat >= 0 or not np.isfinite(rp0):
        return None
    tp = solve_turning(g, rp0, ra0)
    if tp is None:
        return None
    rp, ra = tp
    mid, half = 0.5 * (ra + rp), 0.5 * (ra - rp)

    def ph(theta):
        r = mid + half * np.sin(theta)
        pr = pr_of_r(r, hhat, j, nu, order)
        if pr is None or pr < 1e-290:
            return 0.0
        return (dH("j", r, pr, j, nu, order) / dH("pr", r, pr, j, nu, order)) * half * np.cos(theta)

    def tm(theta):
        r = mid + half * np.sin(theta)
        pr = pr_of_r(r, hhat, j, nu, order)
        if pr is None or pr < 1e-290:
            return 0.0
        return half * np.cos(theta) / dH("pr", r, pr, j, nu, order)

    dphi, _ = quad(ph, -np.pi / 2, np.pi / 2, limit=300, epsabs=1e-13, epsrel=1e-11)
    T, _ = quad(tm, -np.pi / 2, np.pi / 2, limit=300, epsabs=1e-13, epsrel=1e-11)
    return dphi / np.pi - 1.0, 2 * T, rp, ra


def doll_turning(E, L, rmax=2000.0):
    f = lambda r: (1 - 2.0 / r) * (1 + L * L / (r * r)) - E * E
    grid = np.linspace(2.000001, rmax, 400000)
    vals = f(grid)
    roots = []
    idx = np.where(vals[:-1] * vals[1:] < 0)[0]
    for i in idx:
        roots.append(brentq(f, grid[i], grid[i + 1], xtol=1e-14, rtol=1e-15))
    if len(roots) < 2:
        return None
    rp, ra = roots[-2], roots[-1]
    if f(0.5 * (rp + ra)) > 0:
        return None
    return rp, ra


def doll_k_T(E, L):
    tp = doll_turning(E, L)
    if tp is None:
        return None
    rp, ra = tp
    mid, half = 0.5 * (ra + rp), 0.5 * (ra - rp)

    def ph(theta):
        r = mid + half * np.sin(theta)
        s = E * E - (1 - 2.0 / r) * (1 + L * L / (r * r))
        if s <= 0:
            return 0.0
        return L / (r * r) / np.sqrt(s) * half * np.cos(theta)

    def tm(theta):
        r = mid + half * np.sin(theta)
        s = E * E - (1 - 2.0 / r) * (1 + L * L / (r * r))
        if s <= 0:
            return 0.0
        return E / (1 - 2.0 / r) / np.sqrt(s) * half * np.cos(theta)

    dphi, _ = quad(ph, -np.pi / 2, np.pi / 2, limit=300, epsabs=1e-13, epsrel=1e-11)
    T, _ = quad(tm, -np.pi / 2, np.pi / 2, limit=300, epsabs=1e-13, epsrel=1e-11)
    return dphi / np.pi - 1.0, 2 * T, rp, ra


def adm_orbit_label(pbar, e, nu, order=2):
    rp_t, ra_t = pbar / (1 + e), pbar / (1 - e)
    h0 = -(1 - e * e) / (2 * pbar)
    j0 = float(np.sqrt(pbar))

    def F(x):
        hhat, j = x
        if j <= 0:
            return [1e3, 1e3]
        g = lambda r: H_adm(r, 0.0, j, nu, order) - hhat
        tp = solve_turning(g, *newton_turning_guesses(hhat, j))
        if tp is None:
            return [1e3, 1e3]
        return [tp[0] - rp_t, tp[1] - ra_t]

    sol = fsolve(F, [h0, j0], xtol=1e-13, maxfev=400)
    if not np.all(np.isfinite(sol)) or sol[1] <= 0:
        return None
    return float(sol[0]), float(sol[1])


# ------------------------------------------------------------------- the oracle
def eob_A(u, nu, order):
    A = 1.0 - 2.0 * u + 2.0 * nu * u ** 3
    if order >= 3:
        A = A + nu * A4 * u ** 4
    if order >= 4:
        A = A + nu * (A5C + A5LOG * np.log(u)) * u ** 5
    return A


def eob_D(u, nu, order):
    D = 1.0 - 6.0 * nu * u ** 2
    if order >= 3:
        D = D + 2.0 * (3.0 * nu - 26.0) * nu * u ** 3
    return D


def eob_H2_coeffs(r, nu, order, fmode):
    """S = c0(r) + c2(r) p_r² + c4(r) p_r⁴ in canonical areal (r, p_r).

    fmode: 'A2overD'  = primary source (P_{R*}=(A/B)^{1/2}P_R ⇒ p_{r*}² = (A²/D)p_r²);
           'A2timesD' = ecfd's shipped form (F = A²·D̄, D̄ = 1−6νu², no Q), 2PN only.
    Q = z₃u²p_{r*}⁴ is 3PN-counted (quartic mass shell): c4 = 0 at order 2.
    """
    u = 1.0 / r
    if fmode == "A2overD":
        A = eob_A(u, nu, order)
        D = eob_D(u, nu, order)
        c2 = A * A / D
        z3 = 2.0 * nu * (4.0 - 3.0 * nu) if order >= 3 else 0.0
        c4 = z3 * u * u * A ** 5 / (D * D)
    elif fmode == "A2only":
        A = eob_A(u, nu, 2)
        c2 = A * A
        c4 = 0.0
    else:
        A = eob_A(u, nu, 2)
        D = eob_D(u, nu, 2)
        c2 = A * A * D
        c4 = 0.0
    return A, c2, c4


def eob_turning(h2, j, nu, order, fmode):
    """Two turning points of Ĥ_eff² = A(1+j²u²) with an allowed (g<0) region between."""
    A = (lambda u: eob_A(u, nu, order if fmode == "A2overD" else 2))
    g = lambda r: A(1.0 / r) * (1.0 + j * j / (r * r)) - h2
    grid = np.geomspace(2.05, 4000.0, 40000)
    vals = g(grid)
    idx = np.where(vals[:-1] * vals[1:] < 0)[0]
    if len(idx) < 2:
        return None
    roots = [brentq(g, grid[i], grid[i + 1], xtol=1e-14, rtol=1e-15) for i in idx[-2:]]
    rp, ra = roots
    if ra <= rp * 1.0000001 or g(0.5 * (rp + ra)) >= 0:
        return None
    return rp, ra


def eob_k_T(E_eff, j, nu, order=3, fmode="A2overD", hhat=None):
    """EOB orbit at effective energy E_eff (= 1+ĥ+(ν/2)ĥ²) and angular momentum j.

    Returns (k, T_real, rp, ra) with T_real = T_eff/(1+νĥ): the flow of
    Ĥ_EOB(Ĥ_eff) is the flow of Ĥ_eff rescaled by dĤ_EOB/dĤ_eff = 1/(1+νĥ),
    constant along the orbit.
    """
    h2 = E_eff * E_eff
    tp = eob_turning(h2, j, nu, order, fmode)
    if tp is None:
        return None
    rp, ra = tp
    mid, half = 0.5 * (ra + rp), 0.5 * (ra - rp)

    def parts(r):
        u = 1.0 / r
        A, c2, c4 = eob_H2_coeffs(r, nu, order, fmode)
        return A, c2, c4, A * (1.0 + j * j * u * u)

    def pr_of(r):
        A, c2, c4, c0 = parts(r)
        d = h2 - c0
        if d <= 0:
            return None
        if c4 <= 0.0:
            y = d / c2
        else:
            y = 2.0 * d / (c2 + np.sqrt(c2 * c2 + 4.0 * c4 * d))
        return np.sqrt(y) if y > 0 else 0.0

    def ph(theta):
        r = mid + half * np.sin(theta)
        pr = pr_of(r)
        if pr is None or pr < 1e-290:
            return 0.0
        A, c2, c4, _ = parts(r)
        return (A * j / (r * r)) / (c2 * pr + 2.0 * c4 * pr ** 3) * half * np.cos(theta)

    def tm(theta):
        r = mid + half * np.sin(theta)
        pr = pr_of(r)
        if pr is None or pr < 1e-290:
            return 0.0
        _, c2, c4, _ = parts(r)
        return half * np.cos(theta) / (c2 * pr + 2.0 * c4 * pr ** 3)

    dphi, _ = quad(ph, -np.pi / 2, np.pi / 2, limit=300, epsabs=1e-13, epsrel=1e-11)
    T, _ = quad(tm, -np.pi / 2, np.pi / 2, limit=300, epsabs=1e-13, epsrel=1e-11)
    Tfac = 1.0 if hhat is None else 1.0 / (1.0 + nu * hhat)
    return dphi / np.pi - 1.0, 2 * T * Tfac, rp, ra


def hhat_of_Eeff(E_eff, nu):
    """Invert the design/EOB map: ĥ = (√(1+2ν(E_eff−1)) − 1)/ν (exact)."""
    return (np.sqrt(1.0 + 2.0 * nu * (E_eff - 1.0)) - 1.0) / nu


def Eeff_of_hhat(hhat, nu):
    return 1.0 + hhat + 0.5 * nu * hhat * hhat


def doll_EL_at_turning(rp_t, ra_t):
    """Exact Schwarzschild (E, L) with turning points rp, ra (areal, M=1).

    (du/dφ)² = 2(u−u_p)(u−u_a)(u−u_c)/j² with u_c = 1/2 − u_p − u_a (sum of roots
    of the cubic), so j² = 1/(u_pu_a + u_pu_c + u_au_c) and E² = 1 − 2j²u_pu_au_c.
    Closed form — no fsolve (which goes degenerate as e→0).
    """
    up, ua = 1.0 / ra_t, 1.0 / rp_t
    uc = 0.5 - up - ua
    if uc <= 0:
        return None
    j2 = 1.0 / (up * ua + up * uc + ua * uc)
    E2 = 1.0 - 2.0 * j2 * up * ua * uc
    if E2 <= 0 or E2 >= 1.0:
        return None
    return float(np.sqrt(E2)), float(np.sqrt(j2))
def conv_de98(pbar, e, nu, orders=(2, 3, 4)):
    """de98's grid: labels owned by the DJS orbit's turning points; matched invariants."""
    lab = adm_orbit_label(pbar, e, nu)
    if lab is None:
        return None
    hhat, j = lab
    E_eff = Eeff_of_hhat(hhat, nu)
    out = {"conv": "de98", "pbar": pbar, "e": e, "nu": nu, "hhat": hhat, "j": j, "E_eff": E_eff}
    ref = adm_k_T(hhat, j, nu)
    if ref is not None:
        out["k_djs"], out["T_djs"] = ref[0], ref[1]
    dol = doll_k_T(E_eff, j)
    if dol is None:
        out["doll_plunge"] = True
        return out
    out["doll_plunge"] = False
    out["k_doll"], out["T_doll"] = dol[0], dol[1]
    if "k_djs" in out:
        out["ek_djs"] = (dol[0] - out["k_djs"]) / out["k_djs"]
    for o in orders:
        eo = eob_k_T(E_eff, j, nu, order=o, fmode="A2overD", hhat=hhat)
        if eo is not None:
            out[f"k_eob{o}"], out[f"T_eob{o}"] = eo[0], eo[1]
            out[f"ek_eob{o}"] = (dol[0] - eo[0]) / eo[0]
            out[f"eT_eob{o}"] = (dol[1] - eo[1]) / eo[1]
    return out


def conv_doll(pbar, e, nu, orders=(2, 3, 4)):
    """Labels owned by the doll's own orbit: geodesic with turning points p̄/(1±e)."""
    rp_t, ra_t = pbar / (1 + e), pbar / (1 - e)
    EL = doll_EL_at_turning(rp_t, ra_t)
    if EL is None:
        return None
    E, L = EL
    hhat = hhat_of_Eeff(E, nu)
    out = {"conv": "doll", "pbar": pbar, "e": e, "nu": nu, "hhat": hhat, "j": L, "E_eff": E}
    dol = doll_k_T(E, L)
    if dol is None:
        out["doll_plunge"] = True
        return out
    out["doll_plunge"] = False
    out["k_doll"], out["T_doll"] = dol[0], dol[1]
    for o in orders:
        eo = eob_k_T(E, L, nu, order=o, fmode="A2overD", hhat=hhat)
        if eo is not None:
            out[f"k_eob{o}"], out[f"T_eob{o}"] = eo[0], eo[1]
            out[f"ek_eob{o}"] = (dol[0] - eo[0]) / eo[0]
            out[f"eT_eob{o}"] = (dol[1] - eo[1]) / eo[1]
    return out


def conv_tp(pbar, e, nu, order=2, fmode="A2timesD"):
    """ecfd's form: identical geometric turning points (u_p, u_a) for both orbits."""
    uc = 1.0 / pbar
    up, ua = uc * (1 + e), uc * (1 - e)
    A = lambda u: eob_A(u, nu, order if fmode == "A2overD" else 2)
    Ap, Aa = A(up), A(ua)
    j2 = (Aa - Ap) / (Ap * up ** 2 - Aa * ua ** 2)
    if j2 <= 0:
        return None
    j = np.sqrt(j2)
    E_eff = np.sqrt(Ap * (1 + j2 * up ** 2))
    eo = eob_k_T(E_eff, j, nu, order=order if fmode == "A2overD" else 2, fmode=fmode)
    if eo is None:
        return None
    # doll: geodesic with the SAME turning points (exact cubic-root labels)
    EL = doll_EL_at_turning(1 / up, 1 / ua)
    if EL is None:
        return None
    E_d, L_d = EL
    dol = doll_k_T(E_d, L_d)
    if dol is None:
        return None
    return {"conv": "tp", "fmode": fmode, "order": order, "pbar": pbar, "e": e, "nu": nu,
            "k_eob": eo[0], "k_doll": dol[0],
            "ek": (dol[0] - eo[0]) / eo[0],
            "eT": (dol[1] - eo[1]) / eo[1]}


def main():
    R = {}

    # ---------------- validations (instrument, tuning cases) ----------------
    # V1: ν→0 exactness of the oracle (machine-zero baseline; both f-modes pass —
    # this does NOT discriminate, which is why V2 exists).
    v1 = []
    for pbar, e in [(20, 0.6), (12, 0.3), (50, 0.9), (8.5, 0.1)]:
        row = conv_doll(pbar, e, 1e-9)
        if row and not row["doll_plunge"]:
            v1.append(dict(pbar=pbar, e=e, ek3=row["ek_eob3"], ek2=row["ek_eob2"]))
    R["V1"] = v1
    print("V1 nu->0 baseline at nu=1e-9 (should equal the O(nu) effect at 1e-9, i.e."
 " ~ek(0.25)*4e-9, NOT a truncation floor):",
          [(d["pbar"], f"{d['ek3']:.1e}") for d in v1])

    # V2: the structure check that discriminates the p_r² coefficient sign.
    # Gauge-invariant k at matched invariants through 2PN: the EOB-2PN ν-effect must
    # equal de98's DJS corrected column to 3PN residuals; ecfd's F=A²·D̄ violates.
    v2 = []
    for pbar in (80.0, 100.0, 120.0):
        row = conv_de98(pbar, 0.6, 0.25)
        if row is None or "ek_djs" not in row:
            continue
        lab0 = adm_orbit_label(pbar, 0.6, 1e-6)
        h0, j0 = lab0
        base_djs = adm_k_T(h0, j0, 1e-6)
        base_doll = doll_k_T(Eeff_of_hhat(h0, 1e-6), j0)
        corr_djs = ((row["k_doll"] - row["k_djs"]) / row["k_djs"]
                    - (base_doll[0] - base_djs[0]) / base_djs[0])
        wrong = eob_k_T(row["E_eff"], row["j"], 0.25, order=2, fmode="A2timesD")
        v2.append(dict(pbar=pbar, corr_djs=corr_djs, eob3pn=row["ek_eob3"],
                       eob2pn=row["ek_eob2"],
                       wrong_sign=(row["k_doll"] - wrong[0]) / wrong[0],
                       gap_correct=abs(row["ek_eob3"] - corr_djs),
                       gap_wrong=abs((row["k_doll"] - wrong[0]) / wrong[0] - corr_djs)))
    R["V2"] = v2
    for d in v2:
        print(f"V2 pbar={d['pbar']:.0f}: corrDJS={d['corr_djs']:+.5f}  EOB3PN={d['eob3pn']:+.5f}"
              f"  gap(correct)={d['gap_correct']:.2e}  gap(wrong sign)={d['gap_wrong']:.2e}")

    # V4: reproduce de98's stored DJS rows (their eob_data.json: +13.09% at 20/0.6).
    v4 = []
    for pbar, e in [(20, 0.6), (30, 0.6)]:
        row = conv_de98(pbar, e, 0.25)
        if row and "ek_djs" in row:
            v4.append(dict(pbar=pbar, ek_djs=row["ek_djs"]))
    R["V4"] = v4
    print("V4 DJS rows (de98 stored: +13.09% at 20/0.6, +5.18% at 30/0.6):",
          [(d["pbar"], f"{d['ek_djs']:+.4%}") for d in v4])

    # V5: doll quadrature vs the true weak-field series k = 3/p̄ + 27/(2p̄²) (the
    # famous 1/√(1−6/j²)−1 is NOT exact: its j²-expansion has 27/2j⁴ where the true
    # series has 45/2j⁴ — ecfd's "closed form" control carried this 2PN error).
    v5 = []
    for pbar in (100.0, 300.0):
        row = conv_doll(pbar, 0.01, 1e-9)
        series = 3 / pbar + 27 / (2 * pbar ** 2)
        if row and not row["doll_plunge"]:
            v5.append(dict(pbar=pbar, k_quad=row["k_doll"], series=series,
                           rel=abs(row["k_doll"] - series) / series))
    R["V5"] = v5
    print("V5 doll vs series 3/p̄+27/2p̄² (residual = 3PN term):",
          [(d["pbar"], f"{d['rel']:.2e}") for d in v5])

    # V6: the three controls de98 quoted but did not regenerate.
    # (a) Newtonian closure: a pure H_N = p²/2 − 1/r quadrature must give k = 0
    #     (H_adm has no pure-Newtonian mode; its first correction line is 1PN).
    hN, jN = -0.015, 4.9
    gN = lambda r: 0.5 * jN ** 2 / r ** 2 - 1.0 / r - hN
    tpN = solve_turning(gN, *newton_turning_guesses(hN, jN))
    mid, half = 0.5 * (tpN[1] + tpN[0]), 0.5 * (tpN[1] - tpN[0])

    def phN(theta):
        r = mid + half * np.sin(theta)
        s = (1.0 / r + hN) * 2 - jN ** 2 / r ** 2
        if s <= 0:
            return 0.0
        return (jN / r ** 2) / np.sqrt(s) * half * np.cos(theta)

    dphiN, _ = quad(phN, -np.pi / 2, np.pi / 2, limit=300, epsabs=1e-13, epsrel=1e-11)
    k_newt_val = dphiN / np.pi - 1.0
    tpa = adm_k_T(*(lambda EL: (EL[0] - 1.0, EL[1]))(doll_EL_at_turning(12.5, 50.0)),
                  nu=1e-6)                                   # (c) iso→areal map:
    # de98's construction: the DOLL's invariants (E−1, L) at areal turning points
    # 12.5/50, given to the ADM(ν→0) reference; its turning points are isotropic.
    wf = conv_doll(100, 0.3, 1e-9)                      # (b) weak-field series
    series = 3 / 100 + 27 / (2 * 100 ** 2)
    areal = lambda r: r * (1 + 1 / (2 * r)) ** 2
    R["V6"] = dict(newton_k=k_newt_val,
                   wf_k=wf["k_doll"] if wf and not wf.get("doll_plunge") else None,
                   wf_series=series,
                   iso_p=tpa[2], iso_a=tpa[3],
                   areal_p=areal(tpa[2]), areal_a=areal(tpa[3]))
    print(f"V6 (a) Newtonian k={k_newt_val:.2e}  (b) k(p̄=100,e=.3,ν→0)={wf['k_doll']:.6f}"
          f" vs series {series:.6f}  (c) iso {tpa[2]:.2f}→{areal(tpa[2]):.2f}"
          f" / {tpa[3]:.2f}→{areal(tpa[3]):.2f} (doll areal 12.5 / 50.0)")

    # V3: independent RK check of the EOB quadrature (the EOB half was never
    # independently validated before): integrate the canonical EOB Hamilton
    # equations from periastron to periastron and compare k at strong labels.
    from scipy.integrate import solve_ivp

    def eob_rk_k(E_eff, j, nu, order=3, fmode="A2overD"):
        tp = eob_turning(E_eff * E_eff, j, nu, order, fmode)
        if tp is None:
            return None
        rp, ra = tp

        def Hval(r, pr):
            u = 1 / r
            A, c2, c4 = eob_H2_coeffs(r, nu, order, fmode)
            return np.sqrt(A * (1 + j * j * u * u) + c2 * pr * pr + c4 * pr ** 4)

        def dHdr(r, pr):
            return Hval(r + 1e-20 * 1j, pr).imag / 1e-20

        def rhs(phi, y):
            r, pr = y
            u = 1 / r
            A, c2, c4 = eob_H2_coeffs(r, nu, order, fmode)
            return [(c2 * pr + 2 * c4 * pr ** 3) / (A * j * u * u),
                    -dHdr(r, pr) * Hval(r, pr) / (A * j * u * u)]

        def peri(phi, y):
            return y[1]

        peri.direction = 1
        peri.terminal = True

        s0 = solve_ivp(rhs, [0, 0.05], [rp, 1e-9], rtol=1e-13, atol=1e-16)
        sol = solve_ivp(rhs, [0.05, 80.0], s0.y[:, -1], events=peri,
                        rtol=1e-13, atol=1e-16, max_step=0.05)
        if len(sol.t_events[0]) == 0:
            return None
        return sol.t_events[0][0] / (2 * np.pi) - 1

    v3 = []
    for pbar, e, nu in [(20, 0.6, 0.25), (12, 0.3, 0.25), (30, 0.6, 0.1), (8.5, 0.1, 0.25)]:
        row = conv_doll(pbar, e, nu)
        if row is None or row.get("doll_plunge") or "ek_eob3" not in row:
            continue
        krk = eob_rk_k(row["E_eff"], row["j"], nu)
        if krk is not None:
            v3.append(dict(pbar=pbar, e=e, nu=nu, k_quad=row["k_eob3"], k_rk=krk,
                           rel=abs(row["k_eob3"] - krk) / abs(krk)))
    R["V3"] = v3
    print("V3 EOB quad vs RK relerr:",
          [(d["pbar"], d["e"], f"{d['rel']:.2e}") for d in v3])

    # V7: the decisive structure test at p̄=400 (perturbative): the ν-effect per
    # unit ν must agree between DJS and the EOB through 2PN (gauge-invariant).
    # ecfd's F = A²·D̄ and the no-D variant are the alternatives.
    pbar7, e7 = 400.0, 0.3
    lab7 = adm_orbit_label(pbar7, e7, 1e-9)
    h7, j7 = lab7
    k_djs0 = adm_k_T(h7, j7, 1e-9)[0]
    k_djs1 = adm_k_T(h7, j7, 0.01)[0]
    djs_per_nu = (k_djs1 - k_djs0) / 0.01 / k_djs1 * 100
    v7 = {"djs": djs_per_nu}
    for mode in ("A2overD", "A2timesD", "A2only"):
        k0 = eob_k_T(Eeff_of_hhat(h7, 1e-9), j7, 1e-9, order=2, fmode=mode)[0]
        k1 = eob_k_T(Eeff_of_hhat(h7, 0.01), j7, 0.01, order=2, fmode=mode)[0]
        v7[mode] = (k1 - k0) / 0.01 / k1 * 100
    R["V7"] = v7
    print(f"V7 p̄=400 per-unit-ν effect (%): DJS {v7['djs']:+.4f} | A2/D {v7['A2overD']:+.4f}"
          f" | ecfd A2·D̄ {v7['A2timesD']:+.4f} | no-D A2 {v7['A2only']:+.4f}")
    adj = []
    for fmode, orders in (("A2timesD", (2,)), ("A2overD", (2, 3))):
        for order in orders:
            r = conv_tp(20.0, 0.6, 0.25, order=order, fmode=fmode)
            if r:
                adj.append(r)
    R["adjudication_tp"] = adj
    print("\nAdjudication, conv_tp (ecfd convention) at (20, 0.6, 0.25):")
    for r in adj:
        print(f"   F={r['fmode']:>9} order={r['order']}:  ek={r['ek']:+.4%}  eT={r['eT']:+.4%}")

    # ------------------- the decisive contour (held out) -------------------
    sweep = []
    for conv in ("de98", "doll"):
        for nu in (0.25, 0.1, 0.01):
            for e in (0.1, 0.3, 0.6, 0.9):
                for pbar in (8, 10, 12, 15, 20, 30, 50):
                    if e == 0.9 and pbar < 12:
                        continue
                    row = conv_de98(pbar, e, nu) if conv == "de98" else conv_doll(pbar, e, nu)
                    if row:
                        sweep.append(row)
    R["sweep"] = sweep
    print("\nDecisive contour, ek = k_doll/k_EOB3PN − 1 (matched real invariants):")
    for conv in ("de98", "doll"):
        print(f" labels owned by: {conv}")
        for nu in (0.25, 0.1, 0.01):
            for e in (0.1, 0.3, 0.6, 0.9):
                line = f"  ν={nu} e={e}: "
                for s in [r for r in sweep if r["conv"] == conv and r["nu"] == nu and r["e"] == e]:
                    if s.get("doll_plunge"):
                        line += f"p̄{s['pbar']}:PLUNGE "
                    elif "ek_eob3" in s:
                        b2 = s.get("ek_eob2", float("nan"))
                        b4 = s.get("ek_eob4", float("nan"))
                        line += (f"p̄{s['pbar']:<3g}:{s['ek_eob3']*100:+6.2f}%"
                                 f"[{b2*100:+.1f}/{b4*100:+.1f}] ")
                print(line)

    # P5: ν-linearity at (30, 0.6)
    p5 = {}
    for nu in (0.25, 0.01):
        row = conv_doll(30, 0.6, nu)
        if row and "ek_eob3" in row:
            p5[str(nu)] = row["ek_eob3"]
    R["P5_ratio"] = p5
    if "0.25" in p5 and "0.01" in p5:
        print(f"\nP5 ν-ratio at (30, 0.6): {p5['0.25'] / p5['0.01']:.1f}")

    # P7: fabricated-plunge census, now with an oracle side (EOB bound/unbound).
    census = []
    for nu in (0.25, 0.01):
        rows = []
        for pbar in np.arange(6.5, 8.51, 0.1):
            lab2 = adm_orbit_label(float(pbar), 0.3, nu)
            if lab2 is None:
                continue
            hhat, j = lab2
            E_eff = Eeff_of_hhat(hhat, nu)
            dol = doll_k_T(E_eff, j)
            eo3 = eob_k_T(E_eff, j, nu, order=3, hhat=hhat)
            rows.append(dict(pbar=float(pbar), doll_bound=dol is not None,
                             eob3_bound=eo3 is not None))
        dis = [r for r in rows if r["doll_bound"] != r["eob3_bound"]]
        census.append(dict(nu=nu, n=len(rows), disagree=len(dis),
                           band=[min(d["pbar"] for d in dis), max(d["pbar"] for d in dis)]
                           if dis else None,
                           sense=("doll-plunge/eob-bound" if dis and not dis[0]["doll_bound"]
                                  else ("doll-bound/eob-plunge" if dis else None))))
    R["P7_census"] = census
    for c in census:
        print(f"P7 ν={c['nu']}: {c['disagree']}/{c['n']} labels disagree "
              f"(band {c['band']}, {c['sense']})")

    with open("oracle_data.json", "w") as f:
        json.dump(R, f, indent=1, default=float)


if __name__ == "__main__":
    main()
