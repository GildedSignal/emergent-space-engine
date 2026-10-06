#!/usr/bin/env python3
"""Series-in-q structure (how chi enters) and GL node counts near the
separatrix (which integrands lose smoothness as chi -> 1).

Outputs: series_nodes.json + printed tables.
"""
import json, os, sys, time
from multiprocessing import Pool
from mpmath import mp, mpf, sqrt, cos, pi, acos

WDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, WDIR)


# ---------------------------------------------------------------- series in q
def series_fit(k, chi, sense, npts=9):
    """Fit Delta phi and Delta t/R^1.5 in half-integer powers of q at small q.

    Returns the fitted coefficients of q^1, q^(3/2), q^2 for the odd-in-chi
    part (chi - 0) and for the full value.
    """
    import kerr_ref as K
    mp.dps = 34
    a = mpf(chi)
    qs = [mpf(10) ** (-2 - 0.25 * i) for i in range(npts)]  # 1e-2 .. ~1e-4
    dphi0, dt0 = [], []
    dphi1, dt1 = [], []
    for q in qs:
        EL0 = K.EL_from_shape(k, q, 0, sense)
        EL1 = K.EL_from_shape(k, q, chi, sense)
        r0 = K.increments_converged(EL0[0], EL0[1], 0, n0=64)
        r1 = K.increments_converged(EL1[0], EL1[1], chi, n0=64)
        dphi0.append(r0["dphi"] - 2 * pi)
        dphi1.append(r1["dphi"] - 2 * pi)
        R = 1 / q
        dt0.append(r0["dt"] / R ** 1.5)
        dt1.append(r1["dt"] / R ** 1.5)
    # fit dphi_odd(q) = c1 q + c32 q^1.5 + c2 q^2 (+ c52 q^2.5) by least
    # squares on the small-q subset (Vandermonde in q^(1/2) powers)
    def fit(vals, powers, qsub):
        # normal equations via mpmath
        n_p = len(powers)
        A = [[q ** p for p in powers] for q in qsub]
        y = vals
        ATA = [[sum(A[i][r] * A[i][c] for i in range(len(A))) for c in range(n_p)]
               for r in range(n_p)]
        ATy = [sum(A[i][r] * y[i] for i in range(len(A))) for r in range(n_p)]
        # solve
        import mpmath as m
        M = m.matrix(ATA)
        v = m.matrix(ATy)
        sol = m.lu_solve(M, v)
        return [float(x) for x in sol]

    qsub = qs[:6]
    odd_phi = [dphi1[i] - dphi0[i] for i in range(len(qs))]
    odd_t = [dt1[i] - dt0[i] for i in range(len(qs))]
    res = {}
    res["phi_odd_coeffs_q1_q32_q2_q52"] = fit(odd_phi[:6], [1, 1.5, 2, 2.5], qsub)
    res["phi0_coeffs_q1_q2_q3"] = fit(dphi0[:6], [1, 2, 3], qsub)
    res["t_odd_coeffs_q2_q52_q3"] = fit(odd_t[:6], [2, 2.5, 3], qsub)
    # theory anchors
    res["theory_phi_q1_schw"] = float(6 * pi * k)
    res["theory_LT_q32"] = float(-12 * pi * chi * k ** 1.5)
    return res


def series_scan():
    out = {}
    for sense in ("pro", "retro"):
        for k in (mpf(3) / 4, mpf(5) / 8):
            for chi in (mpf(1) / 2, mpf(9) / 10):
                tag = f"{sense}-k{float(k):.3f}-chi{float(chi)}"
                out[tag] = series_fit(k, chi, sense)
                print(tag, out[tag], flush=True)
    return out


# ---------------------------------------------------------------- node counts
def node_count(k, q, chi, sense, tol=mpf(10) ** -13, nmax=8192):
    """Minimal even GL order n on the half cycle [0, pi] for all three
    increments to reach `tol` relative, against a converged n=4096 value."""
    import kerr_ref as K
    mp.dps = 30
    EL = K.EL_from_shape(k, q, chi, sense)
    if EL is None:
        return None
    E, L = EL
    ref = K.increments(E, L, chi, n=4096)
    dphi, dt, dtau, roots = K.integrands(E, L, chi)
    u1, up, u3 = roots
    e = (up - u1) / (up + u1)
    p = (1 + e) / up

    def integrals(n):
        xs, ws = K.gauss_legendre(n)
        Sphi = St = Sta = mpf(0)
        for x, w in zip(xs, ws):
            psi = (pi / 2) * (x + 1)
            u = (1 + e * cos(psi)) / p
            fac = w * pi / 2
            Sphi += fac * dphi(u)
            St += fac * dt(u)
            Sta += fac * dtau(u)
        return Sphi * 2, St * 2, Sta * 2

    n = 16
    while n <= nmax:
        v = integrals(n)
        ok = all(abs(v[i] - [ref["dphi"], ref["dt"], ref["dtau"]][i])
                 > tol * abs([ref["dphi"], ref["dt"], ref["dtau"]][i])
                 for i in range(3))
        if not ok:
            return n
        n *= 2
    return nmax


def nodes_scan():
    import kerr_ref as K
    out = []
    for chi in (0, mpf(1) / 2, mpf(9) / 10, mpf(998) / 1000):
        for sense in ("pro", "retro"):
            k = mpf(5) / 8  # e = 0.6
            qs = K.q_sep_of_k(k, chi, sense)
            if qs is None:
                continue
            for delta in (mpf(10) ** -1, mpf(10) ** -2, mpf(10) ** -3,
                          mpf(10) ** -4):
                q = qs * (1 - delta)
                n = node_count(k, q, chi, sense)
                out.append({"chi": float(chi), "sense": sense, "k": float(k),
                            "q_over_qsep": float(1 - delta), "n_gl": n})
                print(out[-1], flush=True)
    # also e = 0.9 near sep at chi = 0.998 pro (the extreme)
    for k in (mpf(10) / 19,):
        qs = K.q_sep_of_k(k, mpf(998) / 1000, "pro")
        for delta in (mpf(10) ** -2, mpf(10) ** -3):
            n = node_count(k, qs * (1 - delta), mpf(998) / 1000, "pro")
            out.append({"chi": 0.998, "sense": "pro", "k": float(k),
                        "q_over_qsep": float(1 - delta), "n_gl": n})
            print(out[-1], flush=True)
    return out


if __name__ == "__main__":
    t0 = time.time()
    res = {"series": {}, "nodes": []}
    with Pool(2) as pool:
        r1 = pool.apply_async(series_scan)
        r2 = pool.apply_async(nodes_scan)
        try:
            res["series"] = r1.get(timeout=900)
        except Exception as e:
            print("series failed:", repr(e)[:200])
        try:
            res["nodes"] = r2.get(timeout=900)
        except Exception as e:
            print("nodes failed:", repr(e)[:200])
    with open(os.path.join(WDIR, "series_nodes.json"), "w") as f:
        json.dump(res, f, indent=1)
    print("wrote series_nodes.json", time.time() - t0, "s")
