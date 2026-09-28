#!/usr/bin/env python3
"""Self-checks of the judge (each < 60 s): the frozen GR oracle's single-mass rows at 1e-12,
the contract's worked example and exact circle, the Newtonian limit, closed-form infall.

Usage: selfcheck.py [ORACLE_ROWS.jsonl]   (default artifacts/evidence/gr-oracle-20260928/rows.jsonl)
Prints one JSON object per check and exits 1 if any fails.
"""
import json
import math
import os
import sys
import time

from flint import arb, ctx

import geodesic_judge as gj

TOL = 1e-12
PREC = 256


class Pseudo:
    """Anchor at an exact periapsis (turning point) built from invariants, M = 1, Q = 1."""

    def __init__(self, null, rp):
        self.M, self.Q, self.t0 = 1, 1, 0
        self.null = null
        self.eps = 0 if null else 1
        self.rdot_sign = 0
        self.rprime_sign = -1          # periapsis: u0 = u2
        self.E_one = False
        self.radial = False
        self.circular = False
        self.n = None
        self.c = 1


def periapsis_geo(null, E, L, rp):
    ctx.prec = PREC
    g = gj.Geo.__new__(gj.Geo)
    g.A = Pseudo(null, rp)
    g.prec = PREC
    g.Mb, g.Qb = arb(1), arb(1)
    g.r0 = rp
    g.E, g.L, g.rdot0 = E, L, arb(0)
    g.sL, g.Lab, g.eps = 1, L, (0 if null else 1)
    g.u0, g.uh = 1 / rp, arb(1) / 2
    g.info, g.period, g.horizon, g.escape, g.zinf = {}, False, False, False, None
    g._setup_cubic()
    g._finish()
    return g


def bound_geo(p, e):
    p, e = arb(p), arb(e)
    E = (((p - 2) ** 2 - 4 * e * e) / (p * (p - 3 - e * e))).sqrt()
    L = p / (p - 3 - e * e).sqrt()
    g = periapsis_geo(False, E, L, p / (1 + e))
    assert g.period
    return g


def null_geo_from_r0(r0):
    r0 = arb(r0)
    b = r0 / (1 - 2 / r0).sqrt()
    return periapsis_geo(True, arb(1), b, r0), b


def null_geo_from_b(b):
    ctx.prec = PREC
    b = arb(b)
    # periapsis: largest root r of r^3 - b^2 r + 2 b^2 = 0 (u2 of 1/b^2 - u^2 + 2u^3)
    r = b
    for _ in range(200):
        f = r ** 3 - b * b * r + 2 * b * b
        df = 3 * r * r - b * b
        r = (r - f / df).mid()
    return periapsis_geo(True, arb(1), b, r)


def pg_f(r):
    s, s2 = r.sqrt(), arb(2).sqrt()
    return 2 * (2 * r).sqrt() + 2 * ((s - s2) / (s + s2)).log()


def shapiro_leg(g, r0, r1):
    """Schwarzschild t from the periapsis r0 to r1, minus sqrt(r1^2 - r0^2)."""
    u1 = 1 / arb(r1)
    z = 2 * arb.pi() - ((g.m - u1) / g.h).acos()
    T = g.Tprim.at_ball(z) - g.F0z0
    t = T - (pg_f(arb(r1)) - pg_f(arb(r0)))
    return t - (arb(r1) ** 2 - arb(r0) ** 2).sqrt()


def rel(a, b):
    return abs(float(((a - b) / b).mid())) if b != 0 else abs(float(a.mid()))


def check_oracle(path):
    rows = [json.loads(l) for l in open(path)]
    out = []
    for r in rows:
        c = r["case"]
        if c == "periapsis_advance":
            if r["e"] == 0:
                # exact circle: double root u1 = u2 = 1/p, u3 = 1/2 - 2/p; the same chi
                # integrand dphi/dchi = 1/sqrt(2M (u3 - u)) with h = 0
                ctx.prec = PREC
                p = arb(r["p"])
                u, u3 = 1 / p, arb(1) / 2 - 2 / p
                v = gj.integ(lambda z, an: 1 / (2 * (u3 - u) + 0 * z).sqrt(analytic=an), arb(0),
                             (2 * arb.pi()).mid()) + (2 * arb.pi() - (2 * arb.pi()).mid()) / (2 * (u3 - u)).sqrt() \
                    - 2 * arb.pi()
            else:
                g = bound_geo(r["p"], r["e"])
                v = g.PG - 2 * arb.pi()
            out.append({"row": c, "p": r["p"], "e": r["e"], "judge": v.mid().str(20, radius=False),
                        "oracle": r["elliptic_rad"], "rel": rel(v, arb(r["elliptic_rad"]))})
        elif c == "bound_period":
            g = bound_geo(r["p"], r["e"])
            out.append({"row": c + "_coordinate", "p": r["p"], "e": r["e"], "judge": g.PT.mid().str(20, radius=False),
                        "oracle": r["quadrature_coordinate"], "rel": rel(g.PT, arb(r["quadrature_coordinate"]))})
            out.append({"row": c + "_proper", "p": r["p"], "e": r["e"], "judge": g.PH.mid().str(20, radius=False),
                        "oracle": r["quadrature_proper"], "rel": rel(g.PH, arb(r["quadrature_proper"]))})
        elif c == "light_deflection":
            g = null_geo_from_b(r["b"])
            chi_inf = 2 * arb.pi() - g.zinf
            v = g.Gprim.at_ball(g.zinf) - g.Gprim.at_ball(chi_inf) - arb.pi()
            out.append({"row": c, "b": r["b"], "judge": v.mid().str(20, radius=False),
                        "oracle": r["quadrature_rad"], "rel": rel(v, arb(r["quadrature_rad"]))})
        elif c == "shapiro_delay":
            g, b = null_geo_from_r0(r["r0"])
            v = shapiro_leg(g, r["r0"], r["r1"]) + shapiro_leg(g, r["r0"], r["r2"])
            out.append({"row": c, "r0": r["r0"], "judge": v.mid().str(20, radius=False),
                        "oracle": r["quadrature_one_way"], "rel": rel(v, arb(r["quadrature_one_way"]))})
        elif c == "clock_rate":
            ctx.prec = PREC
            R = arb(r["r"])
            # flow-frame Lorentz factors: static u = -beta; circular v = sqrt(M/r) tangential
            st = (1 - 2 / R).sqrt()
            out.append({"row": "clock_static", "r": r["r"], "judge": st.mid().str(20, radius=False),
                        "oracle": r["static_dtau_dt"], "rel": rel(st, arb(r["static_dtau_dt"]))})
            if r["circular_orbit_dtau_dt"] is not None:
                u2 = 1 / R + 2 / R
                ci = (1 - u2).sqrt()
                out.append({"row": "clock_circular", "r": r["r"], "judge": ci.mid().str(20, radius=False),
                            "oracle": r["circular_orbit_dtau_dt"], "rel": rel(ci, arb(r["circular_orbit_dtau_dt"]))})
    for o in out:
        o["pass"] = o["rel"] <= TOL
    return out


def check_contract_examples():
    res = []
    j = gj.Judge(1, 25, 0, (30, 40), (-3, -4), False)
    a1 = j.query(1)
    d = j.diagnostics()
    th = arb(d["T_h"])
    ok = a1["at"] == "Free" and a1["x"] == [26, 35] and abs(float((th - arb(496) / 75).mid())) < 1e-30
    a7 = j.query(7)
    ok = ok and a7 == {"at": "Absorbed", "chronon": 7, "tau": a7["tau"], "prec": a7["prec"]}
    # singularity (r = 0) at 20/3 for the same free fall: 2/(3 sqrt 2) * 50^(3/2) / 25
    ctx.prec = PREC
    sing = 2 / (3 * arb(2).sqrt()) * arb(50) * arb(50).sqrt() / 25
    ok = ok and abs(float((sing - arb(20) / 3).mid())) < 1e-60
    res.append({"check": "worked example (26,35), T_h = 496/75, singularity 20/3", "T1": a1["x"],
                "T_h": d["T_h"][:30], "T7": a7["at"], "pass": ok})
    j = gj.Judge(1, 3, 0, (9, 0), (0, 1), False)
    d = j.diagnostics()
    xs = [j.query(T)["x"] for T in (1, 2, 3)]
    ctx.prec = PREC
    exp = [[int((9 * (arb(T) / 9).cos()).floor().unique_fmpz()), int((9 * (arb(T) / 9).sin()).floor().unique_fmpz())]
           for T in (1, 2, 3)]
    ok = d["chart"] == "circular" and xs == exp and d["omega_per_chronon"].startswith("0.11111111111")
    res.append({"check": "exact circle r = 9M (Q = 3, k = (0, 1)), stable", "x": xs, "expected": exp,
                "omega": d["omega_per_chronon"][:20], "pass": ok})
    return res


def kepler_xy(M, x0, v0, t):
    """Newtonian two-body position (float) at time t from (x0, v0)."""
    r0 = math.hypot(*x0)
    vr0 = (x0[0] * v0[0] + x0[1] * v0[1]) / r0
    h = x0[0] * v0[1] - x0[1] * v0[0]
    en = 0.5 * (v0[0] ** 2 + v0[1] ** 2) - M / r0
    a = -M / (2 * en)
    n = math.sqrt(M / a ** 3)
    ecc_c = 1 - r0 / a
    ecc_s = r0 * vr0 / math.sqrt(M * a)
    # Lagrange f-g functions with the eccentric-anomaly difference dE:
    # n t = dE - ecc_c sin dE + ecc_s (1 - cos dE)
    dE = n * t
    for _ in range(200):
        F = dE - ecc_c * math.sin(dE) + ecc_s * (1 - math.cos(dE)) - n * t
        dF = 1 - ecc_c * math.cos(dE) + ecc_s * math.sin(dE)
        dE -= F / dF
    f = 1 - a / r0 * (1 - math.cos(dE))
    g = t - (dE - math.sin(dE)) / n
    return (f * x0[0] + g * v0[0], f * x0[1] + g * v0[1])


def check_newtonian_limit():
    """At large r/M the judge must approach Kepler with a deviation ~ M/r (1PN)."""
    out = []
    devs = []
    for scale in (10 ** 6, 10 ** 8, 10 ** 10):
        M, Q = 1, 2 ** 20            # a period spans many chronons
        x0 = (scale, 0)
        v = math.sqrt(M / scale) * 1.1
        k0 = (0, int(round(Q * v)))
        j = gj.Judge(M, Q, 0, x0, k0, False)
        g = j.geo(0)
        P = float((g.PT / g.Qb).mid())
        T = int(P * 0.37)
        kk, Z = g.solve(arb(Q * T))
        X = g.X_at(kk, Z)
        J = (float(X[0].mid()), float(X[1].mid()))
        K = kepler_xy(M, x0, (k0[0] / Q, k0[1] / Q), Q * T)
        dev = math.hypot(J[0] - K[0], J[1] - K[1]) / scale
        d = g.diagnostics()
        a = float(arb(d["p_over_M"]).mid()) / (1 - float(arb(d["e"]).mid()) ** 2)
        pt_rel = float((g.PT / (2 * arb.pi() * arb(a) ** 1.5)).mid()) - 1
        devs.append(dev)
        out.append({"r_over_M": scale, "position_dev_over_r": dev, "period_ratio_minus_1": pt_rel,
                    "one_pn_3_over_a": 3 / a})
    ok = devs[1] < devs[0] / 30 and devs[2] < devs[1] / 30 and all(
        abs(o["period_ratio_minus_1"] / o["one_pn_3_over_a"] - 1) < 1e-3 for o in out)
    return [{"check": "Newtonian limit: deviation from Kepler ~ M/r, period ratio 1 + 3/a", "rows": out,
             "pass": ok}]


def check_closed_forms():
    out = []
    for (M, Q, r0) in [(1, 25, 10), (1, 25, 100), (2 ** 40, 2 ** 20, 100 * 2 ** 40), (2 ** 79, 2 ** 40, 10 * 2 ** 79)]:
        j = gj.Judge(M, Q, 0, (r0, 0), (0, 0), False)
        g = j.geo(1)
        q = g.dTh / g.Qb
        cf = gj.closed_form_infall_from_rest(M, Q, r0)
        r = abs(float(((q - cf) / cf).mid()))
        out.append({"check": "infall from rest, quadrature vs closed form", "M": M, "Q": Q,
                    "r0_over_M": r0 // M, "rel": r, "pass": r < 1e-100})
    return out


def _load(path):
    import gzip
    with gzip.open(path, "rt") as f:
        return [json.loads(l) for l in f if l.strip()]


def _key(a):
    """Canonical content of an answer (what the gate compares)."""
    if isinstance(a, list):                       # R2 compact form
        return json.dumps(a)
    if isinstance(a, str):
        return a
    at = a["at"]
    if at == "Free":
        return "F" + ",".join(a["x"])
    if at in ("Absorbed", "OutOfRange"):
        return at[0] + a["chronon"]
    return at


def _settled(a):
    if isinstance(a, list):
        return True
    if isinstance(a, str):
        return a[0] in "AO"
    return a["at"] not in ("UNSETTLED",)


def compare(pa, pb):
    """Identical canonical answers on every case settled in both runs."""
    A, B = _load(pa), _load(pb)
    if A and "rung" in A[0] and A[0].get("rung") == "R2":
        A, B = A[1:], B[1:]
        rows_a = {tuple(r[:4]): r[4] for r in A}
        rows_b = {tuple(r[:4]): r[4] for r in B}
        pairs = [(rows_a[k][i], rows_b[k][i]) for k in rows_a for i in range(8)]
    else:
        ia = {r["id"]: r["answers"] for r in A}
        ib = {r["id"]: r["answers"] for r in B}
        pairs = [(x, y) for k in ia for x, y in zip(ia[k], ib[k])]
    both = [(x, y) for x, y in pairs if _settled(x) and _settled(y)]
    diff = [(x, y) for x, y in both if _key(x) != _key(y)]
    return {"compare": [os.path.basename(pa), os.path.basename(pb)], "answers": len(pairs),
            "settled_in_both": len(both), "differences": len(diff), "first": diff[:3],
            "pass": not diff}


def summary(cases_path, answers_path):
    import collections
    C = _load(cases_path)
    A = {r["id"]: r for r in _load(answers_path)}
    by_class = collections.Counter()
    by_at = collections.Counter()
    unsettled = []
    big = 0
    near = []
    for c in C:
        by_class[" / ".join(str(v) for v in c["class"] if v)] += len(c["T"])
        if max(abs(int(v)) for v in c["x"]) >= 2 ** 62:
            big += len(c["T"])
        for a in A[c["id"]]["answers"]:
            by_at[a["at"]] += 1
            if a["at"] == "UNSETTLED":
                unsettled.append((c["id"], a.get("why")))
            if a["at"] == "Free" and a.get("dist"):
                ds = [d for d in a["dist"] if d is not None]
                if ds:
                    near.append(min(ds))
    n = sum(by_at.values())
    near.sort()
    return {"file": os.path.basename(cases_path), "cases": len(C), "queries": n, "by_result": dict(by_at),
            "by_class": dict(by_class), "unsettled": len(unsettled), "unsettled_ids": unsettled[:20],
            "share_with_|x_c|>=2^62": round(big / max(n, 1), 4),
            "within_2^-40": sum(1 for d in near if d < -40),
            "min_log2_dist": near[0] if near else None}


def fallback_widths(cases_path, out_path):
    """For each fallback case: the true value's nearest integer boundary n and distance (from a
    512-bit evaluation) and the judge's own certified width of X at 64 and 128 bits, which must be
    below 1/4 quantum for the 'one of the two integers adjacent to n' rule to be meaningful."""
    import gzip
    rows = []
    for c in _load(cases_path):
        I = int
        A = gj.Anchor(I(c["M"]), I(c["Q"]), I(c["t0"]), [I(v) for v in c["x"]], [I(v) for v in c["k"]],
                      c["motion"] == "null")
        T = I(c["T"][0])
        g = gj.Geo(A, 512)
        k, Z = g.solve(arb(A.Q * (T - A.t0)))
        X = g.X_at(k, Z)
        coord = min((0, 1), key=lambda i: abs(float((X[i] - (X[i] + arb(1) / 2).floor()).mid())))
        xc = X[coord]
        n = int((xc + arb(1) / 2).mid().floor().unique_fmpz())
        dist = xc - n
        row = {"id": c["id"], "coord": coord, "boundary_n": str(n),
               "log2_dist": float((abs(dist).mid().log() / arb(2).log())) if not dist.contains(0) else None,
               "side": "above" if dist > 0 else ("below" if dist < 0 else "undecided"),
               "allowed": [str(n - 1), str(n)]}
        for p in (64, 128):
            try:
                gp = gj.Geo(A, p)
                kp, Zp = gp.solve(arb(A.Q * (T - A.t0)))
                w = 2 * gp.X_at(kp, Zp)[coord].rad()
                row[f"width_{p}"] = float(w)
            except gj.Undecided:
                row[f"width_{p}"] = None
        w64 = row["width_64"]
        row["width_64_below_quarter"] = (w64 is not None and w64 < 0.25)
        # a 64-bit enclosure this wide around the true value can straddle n
        row["may_force_fallback_at_64"] = (row["log2_dist"] is not None and w64 is not None and w64 > 0
                                           and row["log2_dist"] < math.log2(w64))
        rows.append(row)
    with gzip.open(out_path, "wt") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    ok = sum(r["width_64_below_quarter"] for r in rows)
    return {"fallback_cases": len(rows), "width_64_below_quarter": ok,
            "may_force_fallback_at_64": sum(r["may_force_fallback_at_64"] for r in rows),
            "log2_dist_max": max(r["log2_dist"] for r in rows if r["log2_dist"] is not None)}


def main(argv):
    if len(argv) >= 4 and argv[1] == "fallback":
        print(json.dumps(fallback_widths(argv[2], argv[3])))
        return 0
    if len(argv) >= 4 and argv[1] == "compare":
        r = compare(argv[2], argv[3])
        print(json.dumps(r))
        return 0 if r["pass"] else 1
    if len(argv) >= 4 and argv[1] == "summary":
        print(json.dumps(summary(argv[2], argv[3])))
        return 0
    here = os.path.dirname(os.path.abspath(__file__))
    path = argv[1] if len(argv) > 1 else os.path.join(here, "..", "..", "artifacts", "evidence",
                                                      "gr-oracle-20260928", "rows.jsonl")
    t = time.time()
    results = check_oracle(path) + check_contract_examples() + check_newtonian_limit() + check_closed_forms()
    ok = all(r["pass"] for r in results)
    for r in results:
        print(json.dumps(r))
    print(json.dumps({"all_pass": ok, "seconds": round(time.time() - t, 1)}))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
