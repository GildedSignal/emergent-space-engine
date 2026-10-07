#!/usr/bin/env python3
"""Falsifier for the premise red-team 20261007-1420-redteam-9fbd.

Question: does r1's frozen Binet band rule for light (u'' + (1 - 6 u_k) u = -3 u_k^2,
u and u' continuous across bands, u_k at the band's geometric centre, bands
r_k = 2^(k/m)) reproduce exact Schwarzschild null deflection BELOW b = 10
(r1/B3 sample b in [10,1000] = [1.92,192] b_crit), where every secondary image
and the photon ring lives (b_crit = 3*sqrt(3) M ~ 5.196 M)?

And the same question for massive precession below p = 10 (r1 samples p in
[10,1000] only), near the ISCO where dln(w^2)/dln u = -6u/(1-6u) amplifies the
band placement error.

Exact truth: null Binet u'' + u = 3 M u^2; timelike u'' + u = M/L^2 + 3 M u^2.
Band rule (r1): u'' + (1 - 6 u_k) u = c_k, c_k = -3 u_k^2 (light) or
M/L^2 - 3 u_k^2 (massive). RK4 in phi, float64. < 60 s, one process, < 100 MB.
"""
import json
import time
import numpy as np

M = 1.0
BC = 3.0 * np.sqrt(3.0)  # photon capture impact parameter, M = 1

# ---------------------------------------------------------------- configuration
LIGHT_B_OVER_BC = [10.0 / BC, 1.5, 1.2, 1.1, 1.05, 1.02, 1.01, 1.003, 0.97, 0.9]
MASSIVE = [  # (p or r, e); e == 0 -> exact circular at r
    (7.0, 0.0), (8.0, 0.0), (8.0, 0.3), (12.0, 0.5), (20.0, 0.5),
]
MODELS = [("exact", 0), ("m16", 16), ("m32", 32), ("m64", 64)]
PHI0_LIGHT = 0.02


def band_uk(u, m):
    i = np.floor(m * np.log2(u))
    return 2.0 ** ((i + 0.5) / m)


def acceleration(u, mass, l2, is_band, mval):
    """u'' for each case."""
    exact = np.where(mass, M / l2, 0.0) + 3.0 * u * u - u
    uk = band_uk(u, mval)
    band = np.where(mass, M / l2, 0.0) - 3.0 * uk * uk - (1.0 - 6.0 * uk) * u
    return np.where(is_band, band, exact)


def rk4(u, up, dphi, mass, l2, is_band, mval):
    k1u = up
    k1p = acceleration(u, mass, l2, is_band, mval)
    k2u = up + 0.5 * dphi * k1p
    k2p = acceleration(u + 0.5 * dphi * k1u, mass, l2, is_band, mval)
    k3u = up + 0.5 * dphi * k2p
    k3p = acceleration(u + 0.5 * dphi * k2u, mass, l2, is_band, mval)
    k4u = up + dphi * k3p
    k4p = acceleration(u + dphi * k3u, mass, l2, is_band, mval)
    u2 = u + (dphi / 6.0) * (k1u + 2 * k2u + 2 * k3u + k4u)
    up2 = up + (dphi / 6.0) * (k1p + 2 * k2p + 2 * k3p + k4p)
    return u2, up2


def make_light_cases():
    n = len(LIGHT_B_OVER_BC)
    u0, up0, b_arr = [], [], []
    for ratio in LIGHT_B_OVER_BC:
        b = ratio * BC
        b_arr.append(b)
        u0.append(np.sin(PHI0_LIGHT) / b)
        up0.append(np.cos(PHI0_LIGHT) / b)
    cases = []
    for name, m in MODELS:
        for j in range(n):
            cases.append(dict(
                family="light", model=name, mval=m if m else 1,
                is_band=m > 0, mass=False, l2=1.0, e=None,
                u0=u0[j], up0=up0[j], phi0=PHI0_LIGHT,
                tag="b/bc=%.4g" % LIGHT_B_OVER_BC[j], b=b_arr[j],
            ))
    return cases


def make_massive_cases():
    # model-major order: index = k * len(MASSIVE) + j (matches the row builder)
    params = []
    for (p, e) in MASSIVE:
        if e == 0.0:
            r = p
            u0 = 1.0 / r
            l2 = r * r / (r - 3.0 * M)  # exact circular: L^2 = M r^2 / (r - 3M)
        else:
            u0 = (1.0 + e) / p
            l2 = p  # Newtonian semi-latus relation; defines the orbit
        params.append((p, e, u0, l2))
    cases = []
    for name, m in MODELS:
        for (p, e, u0, l2) in params:
            cases.append(dict(
                family="massive", model=name, mval=m if m else 1,
                is_band=m > 0, mass=True, l2=l2, e=e, p=p, b=None,
                u0=u0, up0=0.0, phi0=0.0, tag="p=%g,e=%g" % (p, e),
            ))
    return cases


def run(cases, dphi, maxphi, force_done=None):
    n = len(cases)
    is_light = np.array([c["family"] == "light" for c in cases])
    u = np.array([c["u0"] for c in cases])
    up = np.array([c["up0"] for c in cases])
    phi = np.array([c["phi0"] for c in cases])
    phi0 = phi.copy()
    ustart = u.copy()
    mass = np.array([c["mass"] for c in cases])
    l2 = np.array([c["l2"] for c in cases])
    is_band = np.array([c["is_band"] for c in cases])
    mval = np.array([float(c["mval"]) for c in cases])

    captured = np.zeros(n, bool)
    done = np.zeros(n, bool) if force_done is None else force_done.copy()
    phi_exit = np.full(n, np.nan)       # light: outbound crossing of u_start
    peri_phi = np.full((n, 3), np.nan)  # massive: first three u-maxima (r-min)
    nperi = np.zeros(n, int)
    steps = int(maxphi / dphi)

    for _ in range(steps):
        if done.all():
            break
        u_old, up_old, phi_old = u, up, phi
        u, up = rk4(u, up, dphi, mass, l2, is_band, mval)
        phi = phi_old + dphi

        # capture: reaches the horizon r = 2 (u = 0.5)
        hit = (~done) & (~captured) & (u >= 0.5)
        captured |= hit

        # light exit: falls back to launch u, outbound, past periapsis
        ex = ((~done) & (~captured) & np.isnan(phi_exit) & is_light
              & (u <= ustart) & (up < 0) & (phi - phi0 > 1.0))
        if ex.any():
            t = (ustart[ex] - u_old[ex]) / (u[ex] - u_old[ex])
            phi_exit[ex] = phi_old[ex] + t * dphi
        done_light = (~captured) & (~np.isnan(phi_exit))

        # massive periapsis: u' crosses + -> -
        cross = (~done) & (~captured) & (up_old > 0) & (up <= 0) & (nperi < 3)
        if cross.any():
            pos = np.nonzero(cross)[0]
            t = up_old[pos] / (up_old[pos] - up[pos])
            ph_c = phi_old[pos] + t * dphi
            for q, idx in enumerate(pos):
                peri_phi[idx, nperi[idx]] = ph_c[q]
                nperi[idx] += 1
        done_massive = (~captured) & (nperi >= 3)

        done = done | done_light | done_massive | captured
    return captured, phi_exit, peri_phi


def main():
    t_start = time.time()
    results = []

    # ---- light ----
    light = make_light_cases()
    dphi_light, maxphi_light = 1.5e-4, 10.5
    captured, phi_exit, _ = run(light, dphi_light, maxphi_light)
    captured2, phi_exit2, _ = run(light, 2 * dphi_light, maxphi_light)  # step ctrl
    flat_sweep = np.pi - 2 * PHI0_LIGHT
    for j, ratio in enumerate(LIGHT_B_OVER_BC):
        row = {"b_over_bc": ratio, "b": ratio * BC}
        for k, (name, m) in enumerate(MODELS):
            idx = k * len(LIGHT_B_OVER_BC) + j
            row[name + "_cap"] = bool(captured[idx])
            row[name] = ("captured" if captured[idx]
                         else float((phi_exit[idx] - PHI0_LIGHT) - flat_sweep))
        row["exact_ctrl"] = (0.0 if captured[j]
                             else float(phi_exit[j] - phi_exit2[j]))
        results.append(row)

    # ---- massive ----
    massive = make_massive_cases()
    dphi_m, maxphi_m = 3.0e-4, 36.0
    skip = np.array([c["model"] == "exact" and c["e"] == 0.0 for c in massive])
    capm, _, peri = run(massive, dphi_m, maxphi_m, force_done=skip)
    nm = len(MASSIVE)
    for j, (p, e) in enumerate(MASSIVE):
        row = {"p": p, "e": e}
        for k, (name, m) in enumerate(MODELS):
            idx = k * nm + j
            row[name + "_plunged"] = bool(capm[idx])
            if capm[idx]:
                row[name] = "plunged"
            elif name == "exact" and e == 0.0:
                row[name] = float(2 * np.pi / np.sqrt(1 - 6.0 / p))
            else:
                row[name] = float(peri[idx, 1] - peri[idx, 0])
        row["exact_ctrl"] = 0.0
        results.append(row)

    # ---- anchors ----
    b10 = 10.0
    series = 4 / b10 + 15 * np.pi / (4 * b10 ** 2) + 128 / (3 * b10 ** 3)
    out = {
        "machine": {
            "note": "shared GitHub Actions runner, Linux x86_64",
            "loadavg": open("/proc/loadavg").read().strip(),
            "wall_s": time.time() - t_start,
        },
        "anchors": {
            "light_b10_exact": results[0]["exact"],
            "light_b10_series_3term": series,
            "massive_r7_exact_analytic": 2 * np.pi / np.sqrt(1 - 6 / 7),
        },
        "light": [r for r in results if "b_over_bc" in r],
        "massive": [r for r in results if "p" in r],
    }
    with open("metrics.json", "w") as f:
        json.dump(out, f, indent=1, default=float)

    # ---- report ----
    print("== LIGHT: deflection alpha (rad); b_crit = 3*sqrt(3) = %.4f ==" % BC)
    print("%9s %10s %10s %10s %10s | %9s %9s" % ("b/bc", "exact", "m16", "m32", "m64", "err16%", "err32%"))
    for r in out["light"]:
        if isinstance(r["exact"], float):
            e16 = 100 * (r["m16"] - r["exact"]) / r["exact"]
            e32 = 100 * (r["m32"] - r["exact"]) / r["exact"]
            print("%9.4f %10.5f %10.5f %10.5f %10.5f | %+8.2f%% %+8.2f%%" % (
                r["b_over_bc"], r["exact"], r["m16"], r["m32"], r["m64"], e16, e32))
        else:
            print("%9.4f exact=%s m16=%s m32=%s m64=%s" % (
                r["b_over_bc"], r["exact"], r["m16"], r["m32"], r["m64"]))
    print("\n== MASSIVE: radial period Dphi (rad); precession = Dphi - 2*pi ==")
    print("%14s %10s %10s %10s | %10s %10s" % ("case", "exact", "m16", "m32", "err16%", "err32%"))
    for r in out["massive"]:
        vals = [r["exact"], r["m16"], r["m32"], r["m64"]]
        if all(isinstance(v, float) for v in vals):
            ex = r["exact"]
            e16 = 100 * (r["m16"] - ex) / (ex - 2 * np.pi)
            e32 = 100 * (r["m32"] - ex) / (ex - 2 * np.pi)
            e64 = 100 * (r["m64"] - ex) / (ex - 2 * np.pi)
            print("p=%-4g e=%-4g %10.4f %10.4f %10.4f %10.4f | %+9.2f%% %+9.2f%% %+9.2f%%" % (
                r["p"], r["e"], ex, r["m16"], r["m32"], r["m64"], e16, e32, e64))
        else:
            print("RAW", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})
    print("\nanchors:", out["anchors"])
    print("step-doubling controls: light max |dalpha| = %.2e rad, massive max |dphi| = %.2e rad" % (
        max(abs(r["exact_ctrl"]) for r in out["light"]),
        max(abs(r["exact_ctrl"]) for r in out["massive"])))
    print("wall: %.1f s" % out["machine"]["wall_s"])


if __name__ == "__main__":
    main()
