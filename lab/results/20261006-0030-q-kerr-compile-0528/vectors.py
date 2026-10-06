#!/usr/bin/env python3
"""Decisive verification grid: compiler (GL in Darwin psi) vs direct RK4
Hamiltonian geodesic integration. Writes test_vectors.json and prints a
summary. Families: bound, near-ISCO, near-separatrix, unbound, photon,
negative-energy plunge. All inputs chosen by rule before running.
"""
import json, time, math, os, sys
from multiprocessing import Pool
from mpmath import mp, mpf, sqrt, acos, cos, pi, findroot

WDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, WDIR)

CHIS = [0, mpf(9)/10, mpf(998)/1000]  # chi=0.5 verified in tuning (6-case run, 3.6e-15)
ECCS = [0, mpf(1)/10, mpf(3)/10, mpf(3)/5, mpf(9)/10]


def vector_bound(chi, sense, e, qmode, tag):
    """q by rule: 'half' = 0.5 q_sep, 'weak' = 1/200, 'near' = (1-1e-3) q_sep,
    'isco' = (1-1e-5) q_sep."""
    import kerr_ref as K
    k = 1 / (1 + mpf(e))
    qs = K.q_sep_of_k(k, chi, sense)
    if qs is None:
        return None
    q = {"half": qs / 2, "weak": mpf(1) / 200, "near": qs * (1 - mpf(10) ** -3),
         "isco": qs * (1 - mpf(10) ** -5)}[qmode]
    EL = K.EL_from_shape(k, q, chi, sense)
    if EL is None:
        return None
    E, L = EL
    return dict(tag=tag, family="bound", chi=chi, sense=sense, E=E, L=L,
                k=k, q=q, e=e)


def work_bound(v):
    import kerr_ref as K
    import direct_check as D
    mp.dps = 30
    E, L, chi = v["E"], v["L"], v["chi"]
    ref = K.increments_converged(E, L, chi)
    mp.dps = 22
    d = D.cycle_increments(E, L, chi, dps=22)
    errs = {key: (abs(d[key] - ref[key]) / abs(ref[key])) if ref[key] is not None
            else None for key in ("dphi", "dt", "dtau")}
    return dict(tag=v["tag"], family=v["family"], chi=float(v["chi"]),
                sense=v["sense"],
                E=float(v["E"]), L=float(v["L"]), k=float(v["k"]),
                q=float(v["q"]), e=float(v["e"]),
                n_nodes=ref["n_nodes"],
                dphi=str(ref["dphi"]), dt=str(ref["dt"]), dtau=str(ref["dtau"]),
                dphi_direct=float(d["dphi"]), dt_direct=float(d["dt"]),
                dtau_direct=float(d["dtau"]),
                err_dphi=float(errs["dphi"]), err_dt=float(errs["dt"]),
                err_dtau=float(errs["dtau"]),
                H_drift=float(d["H_drift"]), step_check=float(d["step_check"]))


def work_unbound(v):
    import kerr_ref as K
    import direct_check as D
    mp.dps = 30
    E, L, chi = v["E"], v["L"], v["chi"]
    rs = K.radial_roots(E, L, chi, 1)
    u1, up, u3 = rs
    e = (up - u1) / (up + u1)
    p = (1 + e) / up
    r_w = mpf(2000)
    psi_end = acos((p / r_w - 1) / e)
    ref = K.increments_converged(E, L, chi, psi_end=psi_end)
    mp.dps = 22
    # direct: inbound from r_w, through pericenter, back to r_w
    roots = D.turning_radii(E, L, chi, 1)
    r_peri = sorted(roots)[1]
    y0 = (mpf(r_w), -1, 0, 0)
    # fix pr0 from constraint
    hh = D.H_value(r_w, 0, chi, E, L) + 1 / 2
    gr = (r_w * r_w - 2 * r_w + chi * chi) / (r_w * r_w)
    pr0 = -sqrt(-2 * hh / gr)

    def run(h0):
        y = (r_w, pr0, 0, 0)
        lam = mpf(0)
        for _ in range(500000):
            h = h0 * max(mpf(10) ** -2, min(mpf(10) ** 2, (y[0] / 10) ** 1.5))
            y_new = D._rk4_step(y, h, chi, E, L)
            if y_new[0] <= r_w and lam > 0 and y_new[1] < 0:
                # exited inbound leg? no: inbound means r decreasing; we want
                # the outbound exit r >= r_w with pr > 0
                pass
            if y_new[0] >= r_w and y_new[1] > 0 and lam > 0:
                lo, hi = lam, lam + h
                yl = y
                for _ in range(60):
                    mid = (lo + hi) / 2
                    ym = D.integrate_to(E, L, chi, 1, yl, mid - lo, h0 * 0.5)
                    if ym[0] < r_w:
                        lo, yl = mid, ym
                    else:
                        hi = mid
                y_end = D.integrate_to(E, L, chi, 1, yl, (lo + hi) / 2 - lo,
                                       h0 * 0.25)
                return {"dphi": y_end[3], "dt": y_end[2], "dtau": y_end[0] * 0
                        + (lo + hi) / 2 * 0 + None or y_end[2] * 0 or
                        D_extra_tau(y_end)}
            y, lam = y_new, lam + h
        raise ValueError("unbound did not exit")

    def D_extra_tau(y_end):
        return None

    # simpler: proper time over window = lam at exit (we started at lam=0)
    def run2(h0):
        y = (r_w, pr0, 0, 0)
        lam = mpf(0)
        for _ in range(500000):
            h = h0 * max(mpf(10) ** -2, min(mpf(10) ** 2, (y[0] / 10) ** 1.5))
            y_new = D._rk4_step(y, h, chi, E, L)
            if y_new[0] >= r_w and y_new[1] > 0 and lam > 0:
                lo, hi = lam, lam + h
                yl = y
                for _ in range(60):
                    mid = (lo + hi) / 2
                    ym = D.integrate_to(E, L, chi, 1, yl, mid - lo, h0 * 0.5)
                    if ym[0] < r_w:
                        lo, yl = mid, ym
                    else:
                        hi = mid
                lam_end = (lo + hi) / 2
                y_end = D.integrate_to(E, L, chi, 1, yl, lam_end - lo,
                                       h0 * 0.25)
                return {"dphi": y_end[3], "dt": y_end[2], "dtau": lam_end}
            y, lam = y_new, lam + h
        raise ValueError("unbound did not exit")

    h0 = mpf(10) ** -3
    d1 = run2(h0)
    d2 = run2(h0 / 2)
    errs = {}
    for key in ("dphi", "dt", "dtau"):
        errs[key] = float(abs(d2[key] - d1[key]) / max(abs(d1[key]), mpf(1)))
    errs2 = {}
    for key in ("dphi", "dt", "dtau"):
        errs2[key] = float(abs(d2[key] - ref[key]) / abs(ref[key]))
    return dict(tag=v["tag"], family="unbound", chi=float(chi),
                sense=v["sense"], E=float(E), L=float(L),
                r_peri=float(1 / up), e=float(e),
                n_nodes=ref["n_nodes"],
                dphi=str(ref["dphi"]), dt=str(ref["dt"]), dtau=str(ref["dtau"]),
                window_r=2000.0,
                dphi_direct=float(d2["dphi"]), dt_direct=float(d2["dt"]),
                dtau_direct=float(d2["dtau"]),
                err_dphi=errs2["dphi"], err_dt=errs2["dt"],
                err_dtau=errs2["dtau"], step_check=max(errs.values()))


def work_photon(v):
    import kerr_ref as K
    import direct_check as D
    mp.dps = 30
    b, chi = v["b"], v["chi"]
    shape = K.photon_shape(b, chi, v["sense"])
    up, e = shape["up"], shape["e"]
    p = (1 + e) / up
    r_w = mpf(2000)
    psi_end = acos((p / r_w - 1) / e)
    ref = K.increments_converged(mpf(1), b, chi, mu=0, psi_end=psi_end)
    mp.dps = 22
    d = D.photon_pass(b, chi, r_window=2000.0, dps=22)
    err_phi = float(abs(d["dphi"] - ref["dphi"]) / abs(ref["dphi"]))
    err_t = float(abs(d["dt"] - ref["dt"]) / abs(ref["dt"]))
    return dict(tag=v["tag"], family="photon", chi=float(chi),
                sense=v["sense"], b=float(b), r_peri=float(1 / up),
                n_nodes=ref["n_nodes"], dphi=str(ref["dphi"]),
                dt=str(ref["dt"]), dtau=None, window_r=2000.0,
                dphi_direct=float(d["dphi"]), dt_direct=float(d["dt"]),
                dtau_direct=None, err_dphi=err_phi, err_dt=err_t,
                err_dtau=None, step_check=float(d["step_check"]))


def work_plunge(v):
    import kerr_ref as K
    import direct_check as D
    mp.dps = 30
    E, L, chi = v["E"], v["L"], v["chi"]
    rs = K.radial_roots(E, L, chi, 1)
    u_a = min(r for r in rs if 0 < r < K.horizon_u(chi))
    ref = K.plunge_increments(E, L, chi, u_start=u_a, n=800, dps=30)
    mp.dps = 22
    d = D.plunge_increments(E, L, chi, r_start=1 / u_a, dps=22)
    errs = {key: float(abs(d[key] - ref[key]) / abs(ref[key]))
            for key in ("dphi", "dtau") if d[key] is not None}
    return dict(tag=v["tag"], family="plunge-E<0", chi=float(chi),
                sense=v["sense"], E=float(E), L=float(L),
                r_turn=float(1 / u_a),
                dphi=str(ref["dphi"]), dt=None, dtau=str(ref["dtau"]),
                dphi_direct=float(d["dphi"]), dt_direct=None,
                dtau_direct=float(d["dtau"]),
                err_dphi=errs.get("dphi"), err_dtau=errs.get("dtau"),
                step_check=float(d["step_check"]),
                future_directed=bool(v.get("future", True)))


def find_negE(chi, n=60):
    """Scan for E<0 timelike orbits with an outer turning point outside the
    horizon; record whether any is bound and where turning points sit."""
    import kerr_ref as K
    mp.dps = 30
    found = []
    max_r_turn = 0
    for i in range(1, n):
        E = -mpf(i) / (2 * n)          # E in (-1/2, 0)
        for j in range(1, 3 * n):
            L = -mpf(j) / n * 3        # L in (-9, 0), retrograde
            rs = K.radial_roots(E, L, chi, 1)
            if not rs:
                continue
            uh = K.horizon_u(chi)
            # outside-horizon positive roots (u < u_h means r > r_+)
            pos = sorted(r for r in rs if 0 < r < uh)
            if len(pos) >= 3:
                found.append(("bound?", float(E), float(L)))
                continue
            if len(pos) in (1, 2):
                # plunging from u_a (outer turning point)
                u_a = pos[0]
                max_r_turn = max(max_r_turn, float(1 / u_a))
                if len(found) < 4:
                    found.append(("plunge", float(E), float(L),
                                  float(1 / u_a)))
    return found, max_r_turn


def main():
    t_start = time.time()
    vectors, jobs = [], []

    # bound grid: chi x sense x e, q = 0.5 q_sep
    for chi in CHIS:
        for sense in ("pro", "retro"):
            for e in ECCS:
                v = vector_bound(chi, sense, e, "half", f"bound-chi{float(chi)}-{sense}-e{float(e)}")
                if v:
                    vectors.append((work_bound, v))
    # weak field
    for sense in ("pro", "retro"):
        v = vector_bound(mpf(9)/10, sense, mpf(3)/10, "weak", f"weak-chi0.9-{sense}")
        if v:
            vectors.append((work_bound, v))
    # near-ISCO and near-separatrix
    for chi in (mpf(9)/10, mpf(998)/1000):
        for sense in ("pro", "retro"):
            v = vector_bound(chi, sense, 0, "isco", f"isco-chi{float(chi)}-{sense}")
            if v:
                vectors.append((work_bound, v))
            v = vector_bound(chi, sense, mpf(3)/5, "near", f"sep-chi{float(chi)}-{sense}")
            if v:
                vectors.append((work_bound, v))
    # unbound
    for chi in (mpf(9)/10,):
        for E0, L0, sense in ((1.05, 3.5, "pro"), (1.05, -3.8, "retro"),
                              (1.3, 3.0, "pro"), (1.3, -3.3, "retro")):
            vectors.append((work_unbound, dict(
                tag=f"unbound-chi{float(chi)}-{sense}-E{E0}", family="unbound",
                chi=chi, sense=sense, E=mpf(E0), L=mpf(L0))))
    # photons
    for chi in (mpf(9)/10, mpf(998)/1000):
        bc_pro = K_bc = None
        import kerr_ref as K0
        mp.dps = 30
        bcp = K0.photon_bc(chi, "pro")
        bcr = K0.photon_bc(chi, "retro")
        for tag, b in ((f"ph-chi{float(chi)}-pro-crit", bcp * mpf('1.02')),
                       (f"ph-chi{float(chi)}-retro-crit", bcr * mpf('1.02')),
                       (f"ph-chi{float(chi)}-weak", abs(bcp) * 6)):
            vectors.append((work_photon, dict(tag=tag, family="photon",
                                              chi=chi,
                                              sense="pro" if b > 0 else "retro",
                                              b=b)))
    # negative energy at chi = 0.998
    mp.dps = 30
    import kerr_ref as K1
    found, max_r = find_negE(mpf(998)/1000, n=14)
    print("E<0 scan: max apoapsis radius found:", max_r,
          "(ergosphere is r<2); bound E<0 count:",
          sum(1 for f in found if f[0] == 'bound?'), flush=True)
    for f in found:
        if f[0] == "plunge":
            vectors.append((work_plunge, dict(tag=f"negE-plunge", family="plunge",
                                              chi=mpf(998)/1000, sense="retro",
                                              E=mpf(f[1]), L=mpf(f[2]))))

    print(f"{len(vectors)} vectors; running on 6 workers...", flush=True)
    def dump(out):
        with open(os.path.join(WDIR, "test_vectors.json"), "w") as f:
            json.dump({"generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
                       "units": "M=c=1; equatorial Boyer-Lindquist",
                       "vectors": out}, f, indent=1)

    with Pool(6) as pool:
        results = []
        for (fn, v) in vectors:
            results.append(pool.apply_async(fn, (v,)))
        out = []
        for r, (fn, v) in zip(results, vectors):
            try:
                out.append(r.get())
                print("done:", v["tag"], flush=True)
            except Exception as exc:
                print("FAIL:", v["tag"], repr(exc)[:200], flush=True)
                out.append({"tag": v["tag"], "error": repr(exc)[:300]})
            dump(out)  # incremental: a timeout still leaves the evidence
    dump(out)
    print("wrote test_vectors.json", time.time() - t_start, "s total")


if __name__ == "__main__":
    main()
