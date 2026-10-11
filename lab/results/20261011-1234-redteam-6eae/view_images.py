#!/usr/bin/env python3
"""Decisive falsifier (v3): image multiplicity of the past-light-cone gather near
Schwarzschild. M=1. Null geodesics u'' + u = 3M u^2, u = 1/r, phi the parameter.

A static observer at (r_o, phi=0) traces rays backward over sky angle psi in (0, pi)
measured from the outward radial direction (one half of the 2D sky; the mirror half gives
the mirror images by symmetry). Each surviving ray crosses the emitter circle r = r_e once,
at unwrapped azimuth Phi(psi). Images of a static emitter at (r_e, phi_e) = crossings of
the curve Phi(psi) with the levels phi_e + 2 pi Z, counted over adjacent surviving pairs:
|floor((Phi_j - phi_e)/2pi) - floor((Phi_{j+1} - phi_e)/2pi)| summed. Density-independent;
caustic folds count as distinct images. Total images include the mirror half:
m_total(phi_e) = m(phi_e) + m(2 pi - phi_e).

Instrument history: v1 binned rays per azimuth (conflated density with multiplicity) and had
a keyword-arg bug (M=1e-3) plus an M=0 u<0 leak; v2's weak-field control launched at r=4000,
born below the escape cut. v3: escape cut parameterized; control measures the GR bend as
phi_total(M=1) - phi_total(M=0) on identical finite-radius geometry.
"""
import json
import numpy as np

U_HORIZON = 0.5
PHI_MAX = 12 * np.pi


def trace(r_o, r_e, psi, M=1.0, h=3e-3, phi_max=PHI_MAX, u_escape=None):
    if u_escape is None:
        u_escape = 1.0 / 250.0
    n = psi.size
    u = np.full(n, 1.0 / r_o)
    w = -(1.0 / r_o) * np.sqrt(max(1.0 - 2.0 * M / r_o, 1e-12)) / np.tan(psi)
    phi = np.zeros(n)
    active = np.ones(n, dtype=bool)
    u_e = 1.0 / r_e
    prev_cu = u - u_e
    Phi = np.full(n, np.nan)
    total_phi = np.zeros(n)
    plunged = np.zeros(n, dtype=bool)
    crossed = np.zeros(n, dtype=bool)

    def f(x):
        return -x + 3.0 * M * x * x

    for _ in range(int(phi_max / h)):
        ia = np.where(active)[0]
        if ia.size == 0:
            break
        ua, wa = u[ia], w[ia]
        k1u, k1w = wa, f(ua)
        k2u, k2w = wa + 0.5 * h * k1w, f(ua + 0.5 * h * k1u)
        k3u, k3w = wa + 0.5 * h * k2w, f(ua + 0.5 * h * k2u)
        k4u, k4w = wa + h * k3w, f(ua + h * k3u)
        un = ua + (h / 6.0) * (k1u + 2 * k2u + 2 * k3u + k4u)
        wn = wa + (h / 6.0) * (k1w + 2 * k2w + 2 * k3w + k4w)
        cu = un - u_e
        hit = (~crossed[ia]) & (prev_cu[ia] * cu < 0)
        if np.any(hit):
            ih = ia[hit]
            fr = prev_cu[ih] / (prev_cu[ih] - cu[hit])
            Phi[ih] = phi[ih] + fr * h
            crossed[ih] = True
        prev_cu[ia] = cu
        u[ia], w[ia], phi[ia] = un, wn, phi[ia] + h
        total_phi[ia] = phi[ia]
        dead = (un < u_escape) | (un > U_HORIZON) | (un <= 0.0) | ~np.isfinite(un)
        if np.any(dead):
            idd = ia[dead]
            active[idd] = False
            prev_cu[idd] = 0.0
            plunged[idd[un[dead] > U_HORIZON]] = True
    return {"psi": psi, "Phi": Phi, "total_phi": total_phi, "plunged": plunged,
            "b": r_o * np.sin(psi) / np.sqrt(1.0 - 2.0 * M / r_o)}


def multiplicity(Phi, phi_e):
    a, b = Phi[:-1], Phi[1:]
    ok = np.isfinite(a) & np.isfinite(b)
    la = np.floor((a[ok] - phi_e) / (2 * np.pi))
    lb = np.floor((b[ok] - phi_e) / (2 * np.pi))
    return int(np.abs(la - lb).sum())


def image_directions(psi, Phi, phi_e, n_first=6):
    a, b = Phi[:-1], Phi[1:]
    ok = np.where(np.isfinite(a) & np.isfinite(b))[0]
    out = []
    for j in ok:
        la = int(np.floor((a[j] - phi_e) / (2 * np.pi)))
        lb = int(np.floor((b[j] - phi_e) / (2 * np.pi)))
        lo, hi = min(la, lb), max(la, lb)
        for lev in range(lo + 1, hi + 1):
            target = phi_e + lev * 2 * np.pi
            if not (min(a[j], b[j]) < target < max(a[j], b[j])):
                continue
            fa, fb = a[j] - target, b[j] - target
            t = fa / (fa - fb)
            out.append(float(np.degrees(psi[j] + t * (psi[j + 1] - psi[j]))))
    return sorted(out)[:n_first]


def main():
    rep = {"machine": "linux x8664, 8 vCPU", "units": "M=1", "phi_max": PHI_MAX}

    # control 1: GR bend = phi_total(M=1) - phi_total(M=0), same finite geometry, b = 200 M.
    r_o = 1000.0
    psi = np.array([np.pi - np.arcsin(200.0 * np.sqrt(1 - 2.0 / r_o) / r_o)])
    ue = 1.0 / 900.0
    t1 = trace(r_o, 910.0, psi, M=1.0, h=3e-3, u_escape=ue)
    t0 = trace(r_o, 910.0, psi, M=0.0, h=3e-3, u_escape=ue)
    bend = float(t1["total_phi"][0] - t0["total_phi"][0])
    exp = 4.0 / 200.0  # asymptotic; the [900, inf) tail removes about 0.5% of it
    rep["control_weak_field"] = {"bend": bend, "expected_4_over_b": exp,
                                 "rel_err": abs(bend - exp) / exp}

    # control 2: capture threshold b_c = 3 sqrt(3) M
    ps = np.linspace(np.pi / 2 + 1e-3, np.pi - 1e-4, 12000)
    res = trace(10.0, 1e6, ps, h=3e-4)
    b_esc = res["b"][~res["plunged"]]
    b_c = 3 * np.sqrt(3)
    rep["control_capture"] = {"b_c": b_c, "min_escaping_b": float(b_esc.min()),
                              "rel_err": float(abs(b_esc.min() - b_c) / b_c),
                              "any_below_b_c": bool(b_esc.min() < b_c * 0.999)}

    # control 3: flat M=0 -> multiplicity exactly 1 on every covered azimuth (half-sky)
    ps = np.linspace(0.02, np.pi - 0.02, 16384)
    res = trace(10.0, 20.0, ps, M=0.0)
    mults = [multiplicity(res["Phi"], p) for p in np.linspace(0.05, np.pi - 0.05, 720)]
    cov = float(np.mean([m == 1 for m in mults]))
    rep["control_flat_M0"] = {"max_images": int(max(mults)),
                              "frac_exactly_1_on_covered_half": round(cov, 6),
                              "note": "one sky half: covered azimuths are (0, pi); the mirror half doubles the sky"}
    print("controls:", json.dumps(rep, indent=1))

    sweep = []
    for r_o, r_e in [(10.0, 20.0), (5.0, 20.0), (3.5, 20.0), (3.2, 20.0), (100.0, 200.0)]:
        ps = np.linspace(0.02, np.pi - 0.02, 32768)
        res = trace(r_o, r_e, ps)
        az = np.linspace(0.05, 2 * np.pi - 0.05, 1440)
        tot = np.array([multiplicity(res["Phi"], p) + multiplicity(res["Phi"], 2 * np.pi - p)
                        for p in az])
        row = {"r_o": r_o, "r_e": r_e, "n_rays": int(ps.size),
               "max_total_images": int(tot.max()),
               "frac_ge2": round(float((tot >= 2).mean()), 4),
               "frac_ge3": round(float((tot >= 3).mean()), 4),
               "frac_ge4": round(float((tot >= 4).mean()), 4),
               "deepest_bend_rad": round(float(np.nanmax(res["Phi"])), 3),
               "note": "counts are lower bounds: bend is capped by ray resolution, which itself caps at phi_max"}
        sweep.append(row)
        print(json.dumps(row))

        # corridor zoom: does the count keep growing as resolution does?
        wrap = np.isfinite(res["Phi"]) & (res["Phi"] > np.nanmax(res["Phi"]) - 2 * np.pi)
        psi_w = res["psi"][wrap]
        if psi_w.size > 10:
            lo, hi = float(psi_w.min()), float(psi_w.max())
            psz = np.linspace(lo - 0.2 * (hi - lo), hi + 0.2 * (hi - lo), 131072)
            rz = trace(r_o, r_e, psz, h=1.5e-3)
            az2 = np.linspace(0.05, 2 * np.pi - 0.05, 720)
            # zoom refines the deep-bend region only; multiplicity from the zoom alone
            # undercounts shallow families -- report the deepest bend and the image
            # directions of the behind-hole emitter instead
            rowz = {"r_o": r_o, "zoom_corridor_rad": [lo, hi], "n_rays": int(psz.size),
                    "deepest_bend_rad_zoom": round(float(np.nanmax(rz["Phi"])), 3),
                    "deepest_bend_wraps": round(float(np.nanmax(rz["Phi"]) / (2 * np.pi)), 3)}
            sweep.append(rowz)
            print(json.dumps(rowz))

        if r_o == 10.0:
            full = trace(r_o, r_e, np.linspace(0.02, np.pi - 0.02, 131072), h=1.5e-3)
            dirs = image_directions(full["psi"], full["Phi"], np.pi)
            mirror = image_directions(full["psi"], full["Phi"], np.pi)  # same by symmetry
            rep["emitter_behind_images_r10"] = {
                "phi_e": "pi (exactly behind the hole)",
                "psi_deg_this_half": dirs,
                "psi_deg_mirror_half": [round(360.0 - d, 3) for d in dirs],
                "note": "image directions from one sky half and their mirrors; separation from the hole direction (psi=180 deg)"}
            print("emitter behind:", rep["emitter_behind_images_r10"])

    rep["sweep"] = sweep
    with open("view_images.json", "w") as f:
        json.dump(rep, f, indent=1)


if __name__ == "__main__":
    main()
