#!/usr/bin/env python3
"""Falsifier: does the design's view gather (one Newton solve on the emission
time + a deflection(b) memo for direction) read emitters at the right retarded
time in curved spacetime?

Oracle: Schwarzschild null geodesics from first integrals (M=1, c=1, equatorial).
  path:      (du/dphi)^2 = 1/b^2 - u^2 + 2u^3
  time:      dt/dphi     = 1/(b u^2 (1-2u))
Attacked gather: emission time from t_obs - t_e = Euclidean distance (the only
light-time the spec's mechanism implies; the deflection memo fixes the angle
only). Instrument checks (flat closed forms, RK4 Binet cross-check, exact
radial anchor) live in check_oracle.py.

Emitter: exact circular orbit, dphi/dt = r^(-3/2) (exact in Schwarzschild
coordinate time). Observer static at r_o = 1000, phi = 0. Primary image.
"""
import json
import math

R_O = 1000.0
U_O = 1.0 / R_O
BCRIT = 3.0 * math.sqrt(3.0)
PX = 1920.0          # 1080p width
FOV = math.pi / 2.0  # 90 degrees over the screen width


def simpson(f, a, b, n):
    if n % 2:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += f(a + i * h) * (4.0 if i % 2 else 2.0)
    return s * h / 3.0


def g_curved(b, u):
    return 1.0 / (b * b) - u * u + 2.0 * u * u * u


def g_flat(b, u):
    return 1.0 / (b * b) - u * u


def turning_u1(b, curved=True):
    """smallest root u in (0, 1/3) of g=0 (periapsis of escaping photon)."""
    g = g_curved if curved else g_flat
    lo, hi = 1e-15, (1.0 / 3.0) if curved else (1.0 / b)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if g(b, mid) > 0.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def branch_int(b, u_a, u_b, u_turn, curved, want_time, n=1200):
    """integral from u_a to u_b (u_a < u_b) of
    [1 if not want_time else 1/(b u^2 (1-2u))] / sqrt(g).
    u_b may be a turning point (g=0) or a near-tangential endpoint; the
    substitution u = u_b - s^2 handles both smoothly."""
    g = g_curved if curved else g_flat

    def weight(u):
        if not want_time:
            return 1.0
        lap = (1.0 - 2.0 * u) if curved else 1.0
        return 1.0 / (b * u * u * lap)

    if abs(u_turn - u_b) < 1e-14 and u_turn > 1e-12:
        def integrand(s):
            u = u_turn - s * s
            if s == 0.0:
                v0 = g(b, u_turn)
                if v0 > 1e-30:
                    return 0.0  # not a turning point: the du term wins
                gp0 = (-2.0 * u_turn + 6.0 * u_turn * u_turn) if curved else -2.0 * u_turn
                return 2.0 * weight(u_turn) / math.sqrt(abs(gp0))
            val = g(b, u)
            if val <= 0.0:
                return 0.0
            return 2.0 * s * weight(u) / math.sqrt(val)

        s_hi = math.sqrt(u_turn - u_a)
        return simpson(integrand, 0.0, s_hi, n)

    def integrand(u):
        val = g(b, u)
        return weight(u) / math.sqrt(val)

    return simpson(integrand, u_a, u_b, n)



def path_phi_T(b, u_e, inbound, curved=True, n=1200):
    """returns (Delta phi swept, coordinate time) from emission (u_e) to r_o."""
    u1 = turning_u1(b, curved) if curved else (1.0 / b)
    if not inbound:
        # u decreases monotonically u_e -> u_o; u_e may be near-tangential
        phi = branch_int(b, U_O, u_e, u_e, curved, False, n)
        T = branch_int(b, U_O, u_e, u_e, curved, True, n)
        return phi, T
    phi = branch_int(b, u_e, u1, u1, curved, False, n) + branch_int(b, U_O, u1, u1, curved, False, n)
    T = branch_int(b, u_e, u1, u1, curved, True, n) + branch_int(b, U_O, u1, u1, curved, True, n)
    return phi, T


def solve_b(phi_target, u_e, curved=True):
    """b such that the photon sweeps phi_target from (r_e, phi_e) to (r_o)."""
    b_max = (1.0 / (u_e * math.sqrt(1.0 - 2.0 * u_e)) if curved else 1.0 / u_e)
    b_max *= 1.0 - 1e-9  # stay strictly inside the tangential endpoint
    phi_tan, _ = path_phi_T(b_max, u_e, False, curved)
    if phi_target <= phi_tan:
        lo, hi = 1e-9, b_max
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            p, _ = path_phi_T(mid, u_e, False, curved, 400)
            if p < phi_target:
                lo = mid
            else:
                hi = mid
        b = 0.5 * (lo + hi)
        p, T = path_phi_T(b, u_e, False, curved, 3000)
        return b, p, T, False
    lo, hi = BCRIT * (1.0 + 1e-7), b_max
    p_hi, _ = path_phi_T(hi, u_e, True, curved, 400)
    p_lo, _ = path_phi_T(lo, u_e, True, curved, 400)
    if not (p_lo > phi_target > p_hi):
        return None  # capped: deep strong lensing
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        p, _ = path_phi_T(mid, u_e, True, curved, 400)
        if p > phi_target:
            lo = mid
        else:
            hi = mid
    b = 0.5 * (lo + hi)
    p, T = path_phi_T(b, u_e, True, curved, 3000)
    return b, p, T, True


def euclid_dist(phi_e, r_e):
    c = math.cos(phi_e)
    s = math.sin(phi_e)
    return math.sqrt((R_O - r_e * c) ** 2 + (r_e * s) ** 2)


def main():
    out = {"cases": []}
    phases = [0.15 + i * (math.pi - 0.3) / 59.0 for i in range(60)]
    for r_e in [6.0, 8.0, 10.0, 20.0, 50.0]:
        u_e = 1.0 / r_e
        omega = r_e ** -1.5
        beta = math.sqrt(1.0 / (r_e - 2.0))
        rows = []
        capped = 0
        for phi_t in phases:
            res = solve_b(phi_t, u_e, curved=True)
            if res is None:
                capped += 1
                continue
            b, p, T, inbound = res
            d_flat = euclid_dist(-phi_t, r_e)
            dt_shapiro = T - d_flat
            # the gather: solve delta = T - d(phi_true + omega*delta)
            # (its Newton residual uses the Euclidean light time; here the
            # exact fixed point, monotone, by bisection)
            lo, hi = -400.0, 400.0

            def h(delta):
                return delta - T + euclid_dist(-phi_t + omega * delta, r_e)

            if h(lo) > 0 or h(hi) < 0:
                continue
            for _ in range(80):
                mid = 0.5 * (lo + hi)
                if h(mid) < 0:
                    lo = mid
                else:
                    hi = mid
            dt = 0.5 * (lo + hi)
            disp = r_e * omega * abs(dt)          # tangential arc (exact)
            phase_err_deg = math.degrees(omega * dt)  # orbit-phase error
            e1x, e1y = r_e * math.cos(-phi_t), r_e * math.sin(-phi_t)
            p2 = -phi_t + omega * dt
            e2x, e2y = r_e * math.cos(p2), r_e * math.sin(p2)
            v1x, v1y = e1x - R_O, e1y
            v2x, v2y = e2x - R_O, e2y
            cross = abs(v1x * v2y - v1y * v2x)
            dot = v1x * v2x + v1y * v2y
            dtheta = math.atan2(cross, dot)
            px_full = dtheta / FOV * PX
            fov_orbit = 2.2 * r_e / R_O
            px_zoom = dtheta / fov_orbit * PX
            rows.append({
                "phi": phi_t, "b": b, "inbound": inbound,
                "T": T, "d_flat": d_flat, "dt_shapiro": dt_shapiro,
                "dt_gather": dt, "disp_M": disp, "dtheta": dtheta,
                "phase_err_deg": phase_err_deg,
                "px_full": px_full, "px_zoom": px_zoom,
            })
        if not rows:
            continue
        dts = sorted(abs(r["dt_gather"]) for r in rows)
        phs = sorted((r["phase_err_deg"] for r in rows), key=abs)
        worst = max(rows, key=lambda r: r["disp_M"])
        out["cases"].append({
            "r_e": r_e, "beta_local": beta, "omega": omega, "n": len(rows),
            "capped": capped,
            "max_abs_dt": dts[-1], "med_abs_dt": dts[len(dts) // 2],
            "max_disp_M": max(r["disp_M"] for r in rows),
            "max_disp_over_re": max(r["disp_M"] for r in rows) / r_e,
            "max_abs_phase_err_deg": abs(phs[-1]),
            "med_abs_phase_err_deg": abs(phs[len(phs) // 2]),
            "max_px_full": max(r["px_full"] for r in rows),
            "max_px_zoom": max(r["px_zoom"] for r in rows),
            "worst_row": {k: worst[k] for k in
                          ("phi", "b", "inbound", "dt_shapiro", "dt_gather",
                           "disp_M", "phase_err_deg", "px_full", "px_zoom")},
            "min_b": min(r["b"] for r in rows),
        })

    with open("shapiro_results.json", "w") as f:
        json.dump(out, f, indent=1)
    for c in out["cases"]:
        print("r_e=%5.1f beta=%.3f n=%2d cap=%d min_b=%7.3f | |dt| med=%6.2f "
              "max=%6.2f M | phase err med=%6.1f max=%6.1f deg | disp max="
              "%6.3f M (%5.1f%% r_e) | px full=%5.2f zoom=%7.1f | worst row: "
              "phi=%.2f b=%.2f inb=%d dt_shap=%+.1f dt=%+.1f"
              % (c["r_e"], c["beta_local"], c["n"], c["capped"], c["min_b"],
                 c["med_abs_dt"], c["max_abs_dt"],
                 c["med_abs_phase_err_deg"], c["max_abs_phase_err_deg"],
                 c["max_disp_M"], 100 * c["max_disp_over_re"],
                 c["max_px_full"], c["max_px_zoom"],
                 c["worst_row"]["phi"], c["worst_row"]["b"],
                 c["worst_row"]["inbound"], c["worst_row"]["dt_shapiro"],
                 c["worst_row"]["dt_gather"]))


if __name__ == "__main__":
    main()
