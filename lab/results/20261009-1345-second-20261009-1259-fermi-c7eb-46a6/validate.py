#!/usr/bin/env python3
"""Validate the impulse coefficient on REAL truth encounters (RK4, Sun + two belt bodies).

For each dumped sample (initial/final Newton states at t±Δ from the shipped crate, chosen so the
mutual force is negligible at the ends), integrate the full 3-body system (Sun = 1, planar, G = 1)
with scalar-loop RK4 at three masses, plus a no-mutual control. Measured Δa_i = a_osc(end) − a_i.
Predictions:
  impulse (this run):  Δa = xpm_i · m_j · Δa_tick(a_i)          [Δv_i = 2 m_j b/(d² v_rel)]
  author (prior run):  Δa = (2/3)·2atan(2m/(d·v²))·a            [their analysis.py lines 55-56]
Masses are picked from the AUTHOR's formula (the hypothesis under test) to give Δa ≈ 1e-11 at
their prediction — non-circular: if the author is 13× high, the measured signal is ~1e-12 and
still above the integrator floor shown by the control.
"""
import json, math, sys

TAU = 2 * math.pi
TICK = 2.0 ** 32

def accel(x, y, vx, vy, x2, y2, m_other):
    # body 1 heliocentric accel; Sun = 1 at origin; mutual from body 2 (mass m_other)
    r1 = math.sqrt(x * x + y * y)
    dx, dy = x2 - x, y2 - y
    d = math.sqrt(dx * dx + dy * dy)
    d3 = d * d * d
    return (-x / (r1 * r1 * r1) + m_other * dx / d3,
            -y / (r1 * r1 * r1) + m_other * dy / d3)

def rk4_body1(y0, t0, t1, h, m2, x2_0, y2_0, vx2_0, vy2_0, m1):
    """RK4 both bodies; returns body 1's state at t1. Scalar loops (8 floats beat numpy here)."""
    n = int(round((t1 - t0) / h))
    h = (t1 - t0) / n
    x, y, vx, vy = y0
    x2, y2, vx2, vy2 = x2_0, y2_0, vx2_0, vy2_0

    def derivs(x, y, vx, vy, x2, y2, vx2, vy2):
        a1x, a1y = accel(x, y, 0, 0, x2, y2, m2)
        a2x, a2y = accel(x2, y2, 0, 0, x, y, m1)
        return vx, vy, a1x, a1y, vx2, vy2, a2x, a2y

    for _ in range(n):
        k1 = derivs(x, y, vx, vy, x2, y2, vx2, vy2)
        k2 = derivs(x + .5*h*k1[0], y + .5*h*k1[1], vx + .5*h*k1[2], vy + .5*h*k1[3],
                    x2 + .5*h*k1[4], y2 + .5*h*k1[5], vx2 + .5*h*k1[6], vy2 + .5*h*k1[7])
        k3 = derivs(x + .5*h*k2[0], y + .5*h*k2[1], vx + .5*h*k2[2], vy + .5*h*k2[3],
                    x2 + .5*h*k2[4], y2 + .5*h*k2[5], vx2 + .5*h*k2[6], vy2 + .5*h*k2[7])
        k4 = derivs(x + h*k3[0], y + h*k3[1], vx + h*k3[2], vy + h*k3[3],
                    x2 + h*k3[4], y2 + h*k3[5], vx2 + h*k3[6], vy2 + h*k3[7])
        x += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        y += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        vx += h / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
        vy += h / 6 * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3])
        x2 += h / 6 * (k1[4] + 2 * k2[4] + 2 * k3[4] + k4[4])
        y2 += h / 6 * (k1[5] + 2 * k2[5] + 2 * k3[5] + k4[5])
        vx2 += h / 6 * (k1[6] + 2 * k2[6] + 2 * k3[6] + k4[6])
        vy2 += h / 6 * (k1[7] + 2 * k2[7] + 2 * k3[7] + k4[7])
    return x, y, vx, vy

def osc_a(r, v):
    return 1.0 / (2.0 / r - v * v)

def main():
    rows = []
    for f in sys.argv[1:]:
        for line in open(f):
            rows.append(json.loads(line))
    # subsample the co-orbital belt (long windows dominate runtime)
    rows = [r for k, r in enumerate(rows) if not (r["belt"] == "coorbital" and k % 2)]
    print(f"samples: {len(rows)}")
    out = []
    for s in rows:
        a_i, d, v, delta = s["ai"], s["d"], s["vrel"], s["delta"]
        m0 = 3e-11 * d * v * v / (4 * a_i)          # author-form mass for Δa ≈ 1e-11
        masses = [0.3 * m0, m0, 3 * m0]
        P_min = TAU * min(a_i, s["aj"]) ** 1.5
        h = min(P_min / 2000.0, d / (50.0 * v))
        si0, sj0 = s["si0"], s["sj0"]
        ai_true = osc_a(math.hypot(*s["si1k"][:2]), math.hypot(*s["si1k"][2:]))
        da_tick_i = (2.0 / 3.0) * a_i / (TAU * a_i ** 1.5 * TICK)
        xc, yc, vxc, vyc = rk4_body1(si0, -delta, delta, h, 0.0, *sj0, 0.0)
        ctrl = osc_a(math.hypot(xc, yc), math.hypot(vxc, vyc)) - ai_true
        for m in masses:
            xm, ym, vxm, vym = rk4_body1(si0, -delta, delta, h, m, *sj0, m)
            meas = osc_a(math.hypot(xm, ym), math.hypot(vxm, vym)) - ai_true
            imp = s["xpm_i"] * m * da_tick_i
            auth = (2.0 / 3.0) * 2.0 * math.atan(2 * m / (d * v * v)) * a_i
            out.append(dict(belt=s["belt"], d=d, v=v, m=m, ctrl=ctrl, meas=meas, imp=imp, auth=auth))
    json.dump(out, open("validate-rows.json", "w"))
    import numpy as np
    arr = lambda k: np.array([r[k] for r in out])
    meas, imp, auth, ctrl, vv, mm = arr("meas"), arr("imp"), arr("auth"), arr("ctrl"), arr("v"), arr("m")
    sig = np.abs(meas)
    keep = sig > 3 * np.abs(ctrl)
    print(f"runs: {len(out)}  above control floor (3x): {keep.sum()}")
    print(f"control |Δa| max {np.abs(ctrl).max():.2e} vs signal |Δa| median {np.median(sig):.2e}")
    for name, pred in (("impulse", imp), ("author", auth)):
        r = np.corrcoef(np.log(np.abs(pred[keep])), np.log(sig[keep]))[0, 1]
        slope = np.polyfit(np.log(np.abs(pred[keep])), np.log(sig[keep]), 1)[0]
        ratio = sig[keep] / np.abs(pred[keep])
        print(f"  {name:8s}: corr={r:.4f} slope={slope:.3f}  meas/pred median={np.median(ratio):.3f} "
              f"p16/p84={np.percentile(ratio,16):.2f}/{np.percentile(ratio,84):.2f}")
    lg = np.log(sig[keep] / mm[keep]); lv = np.log(vv[keep])
    alpha = np.polyfit(lv, lg, 1)[0]
    print(f"  v_rel exponent of measured Δa/m: {alpha:.3f}  (impulse: -1, author: -2)")
    for belt in sorted(set(r["belt"] for r in out)):
        idx = [i for i, r in enumerate(out) if r["belt"] == belt and keep[i]]
        if idx:
            ra = np.median([meas[i] / auth[i] for i in idx])
            ri_ = np.median([meas[i] / imp[i] for i in idx])
            print(f"    {belt:26s} n={len(idx):3d} meas/impulse={ri_:.3f} meas/author={ra:.3f}")

if __name__ == "__main__":
    main()
