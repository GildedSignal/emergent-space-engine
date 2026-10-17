#!/usr/bin/env python3
"""Premise falsifier: opacity/capture is absent from the view's premises.

Truth: exact Schwarzschild null geodesics (M = 1), traced BACKWARD from a static
observer at r_o. Capture iff b < b_c = 3*sqrt(3) (exact predicate, r1/B4's own
cases). Scheme: the doc's gather (representation.md L56-59) and the shipped
`crates/universe/src/view.rs` — straight light, every emitter present, no
opacity test anywhere. Units M = 1. 2-D sky: arrival directions form a circle.

Outputs JSON to stdout. Pure stdlib; runs in a few seconds.
"""
import json
import math

M = 1.0
BC = 3.0 * math.sqrt(3.0)  # critical impact parameter


def trace(b, r_o, dphi=0.004, phi_max=200.0):
    """Backward trace one arriving photon. Initial local angle alpha (rad) from
    the direction pointing AT the black hole; b = r_o sin(alpha)/sqrt(1-2M/r_o).
    Returns dict: outcome capture|escape|critical, windings, deflection."""
    u = 1.0 / r_o
    # du/dphi at the observer for the ray arriving from angle alpha off the BH
    # direction (theta = pi - alpha from outward radial):
    # (du/dphi)^2 = (1-2u_o) u_o^2 cot^2(theta); theta = pi - alpha.
    sin_a = b * math.sqrt(1.0 - 2.0 * M / r_o) / r_o
    alpha = math.asin(max(-1.0, min(1.0, sin_a)))
    theta = math.pi - alpha
    dudphi = -math.sqrt(max(0.0, 1.0 - 2.0 * M * u)) * u / math.tan(theta)
    phi = 0.0
    turned = False
    steps = int(phi_max / dphi)
    for _ in range(steps):
        # RK4 on u'' = -u + 3u^2
        def f(w):
            return (-w + 3.0 * w * w) * M * M if False else (-w + 3.0 * w * w)

        k1u, k1d = dudphi, f(u)
        k2u, k2d = dudphi + 0.5 * dphi * k1d, f(u + 0.5 * dphi * k1u)
        k3u, k3d = dudphi + 0.5 * dphi * k2d, f(u + 0.5 * dphi * k2u)
        k4u, k4d = dudphi + dphi * k3d, f(u + dphi * k3u)
        u_new = u + dphi / 6.0 * (k1u + 2 * k2u + 2 * k3u + k4u)
        dudphi_new = dudphi + dphi / 6.0 * (k1d + 2 * k2d + 2 * k3d + k4d)
        phi += dphi
        if u_new >= 0.5:  # r <= 2M: horizon
            return {"outcome": "capture", "windings": phi / (2 * math.pi), "deflection": None}
        if u_new < 1e-4:
            # escaped past r = 1e4 M
            return {"outcome": "escape", "windings": phi / (2 * math.pi), "deflection": None}
        if not turned and dudphi_new > 0 and u_new < 0.34 and u < 0.34 and phi > 1.0:
            turned = True
        if turned and u_new < u * 0.999 and u_new < 0.01:
            return {"outcome": "escape", "windings": phi / (2 * math.pi), "deflection": None}
        if abs(u_new - 1.0 / 3.0) < 5e-5 and abs(dudphi_new) < 5e-5 and phi > 6 * math.pi:
            return {"outcome": "critical", "windings": phi / (2 * math.pi), "deflection": None}
        u, dudphi = u_new, dudphi_new
    return {"outcome": "critical", "windings": phi / (2 * math.pi), "deflection": None}


def deflection_exact(b, r_o=1e4, dphi=0.002):
    """Total deflection of a ray from infinity to infinity (passing the mass),
    integrated through the observer-side trace: bend = 2*(half-path angle).
    Simpler exact route: integrate u''=-u+3u^2 from u=0 with du/dphi=-1/b up to
    the turning point and back out is symmetric; use phi at u->0 on both sides.
    Here: start at r_o large, inward, integrate until u < u_start again after
    the turn; deflection = (phi_end - pi)."""
    u = 1.0 / r_o
    dudphi = math.sqrt(1.0 / (b * b) - u * u * (1.0 - 2.0 * M * u))  # inward: u rises
    phi = 0.0
    turned = False
    steps = int(400.0 / dphi)
    for _ in range(steps):
        def f(w):
            return -w + 3.0 * w * w

        k1u, k1d = dudphi, f(u)
        k2u, k2d = dudphi + 0.5 * dphi * k1d, f(u + 0.5 * dphi * k1u)
        k3u, k3d = dudphi + 0.5 * dphi * k2d, f(u + 0.5 * dphi * k2u)
        k4u, k4d = dudphi + dphi * k3d, f(u + dphi * k3u)
        u_new = u + dphi / 6.0 * (k1u + 2 * k2u + 2 * k3u + k4u)
        dn = dudphi + dphi / 6.0 * (k1d + 2 * k2d + 2 * k3d + k4d)
        phi += dphi
        if u_new >= 0.5:
            return None  # captured: no deflection, no image on this branch
        if dn < 0:
            turned = True  # past periapsis: u now falls with phi
        if turned and u_new < 1.0 / r_o:
            return phi - math.pi  # straight line would be exactly pi
        u, dudphi = u_new, dn
    return None


def sky_fraction(alpha):
    """2-D sky: blocked arc fraction = 2*alpha / 2*pi."""
    return alpha / math.pi


def main():
    out = {}

    # P1: instrument validity on r1/B4's own photon-capture cases (r_o = 100).
    p1 = {}
    for ratio in (0.9, 0.97, 1.03, 1.1):
        res = trace(ratio * BC, 100.0)
        p1[str(ratio)] = {
            "exact": "capture" if ratio < 1.0 else "escape",
            "integrated": res["outcome"],
            "ok": res["outcome"] == ("capture" if ratio < 1.0 else "escape"),
        }
    out["P1_capture_cases"] = p1
    out["P1_all_ok"] = all(v["ok"] for v in p1.values())

    # P2: numeric capture boundary vs Synge's formula, bisected at each r_o.
    p2 = {}
    for r_o in (100.0, 20.0, 6.0, 3.2):
        synge = math.asin(math.sqrt(27.0) * math.sqrt(1.0 - 2.0 * M / r_o) / r_o)
        # bisect the arrival angle alpha between a capturing and an escaping probe
        lo, hi = 1e-3, math.pi / 2 - 1e-3  # alpha in (0, pi/2) from BH direction
        b_lo = lo  # ensure start states: near 0 => b~0 captures; near pi/2 escapes?
        # alpha -> b: b = r_o sin(alpha)/sqrt(1-2/r_o); alpha small => b small => capture.
        def classifies(alpha):
            b = r_o * math.sin(alpha) / math.sqrt(1.0 - 2.0 * M / r_o)
            return trace(b, r_o)["outcome"]

        # check both ends behave
        c_lo = classifies(lo)
        c_hi = classifies(hi)
        for _ in range(18):
            mid = 0.5 * (lo + hi)
            if classifies(mid) == "capture":
                lo = mid
            else:
                hi = mid
        numeric = 0.5 * (lo + hi)
        p2[str(r_o)] = {
            "alpha_synge_rad": synge,
            "alpha_numeric_rad": numeric,
            "rel_diff": abs(numeric - synge) / synge,
            "end_capture": c_lo,
            "end_escape": c_hi,
        }
    out["P2_boundary"] = p2

    # P3/P4: sky fraction and fabricated rows at N = 10^4.
    N = 10_000
    p34 = {}
    for r_o in (100.0, 20.0, 6.0, 3.2):
        synge = math.asin(math.sqrt(27.0) * math.sqrt(1.0 - 2.0 * M / r_o) / r_o)
        frac = sky_fraction(synge)
        p34[str(r_o)] = {
            "alpha_deg": math.degrees(synge),
            "sky_fraction": frac,
            "fabricated_rows_N1e4": N * frac,
        }
    out["P3P4_shadow"] = p34

    # P5: deflection near the rim, exact integration vs weak-field series.
    p5 = {}
    for ratio in (2.0, 1.5, 1.1, 1.03, 1.01, 1.001):
        b = ratio * BC
        d = deflection_exact(b)
        series = 4.0 / b + 15.0 * math.pi / 4.0 / (b * b) + 128.0 / 3.0 / (b ** 3)
        p5[str(ratio)] = {
            "exact_rad": d,
            "weak_field_series_rad": series,
            "captured": d is None,
        }
    out["P5_rim_deflection"] = p5

    # P6: opaque-body occlusion (flat geometry, no mass: pure trigonometry).
    p6 = {}
    for d_over_R in (10.0, 2.0):
        alpha = math.asin(1.0 / d_over_R)
        frac = sky_fraction(alpha)
        p6[f"d={d_over_R}R"] = {
            "alpha_deg": math.degrees(alpha),
            "sky_fraction": frac,
            "blocked_rows_N1e4": N * frac,
        }
    out["P6_occluder"] = p6

    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
