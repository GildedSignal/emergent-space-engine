#!/usr/bin/env python3
"""Falsifier for the fleet-doll premise (representation.md §1). Plain floats.

Truth: exact star-only two-body motion of a massless member (RK4, inertial,
star = 1 at origin, G = 1), parent = analytic massless Keplerian marker.
Model: the Clohessy-Wiltshire closed form with the mean motion n, evaluated
in the parent's rotating frame, from CW initial conditions at pericenter.
Error = |CW - truth| / a. The closed form used here is the standard one
(x = (4x0+2yd0/n) - (3x0+2yd0/n)cos + (xd0/n)sin;
 y = y0 + (2xd0/n)(cos-1) + 2(3x0+2yd0/n)sin - (6nx0+3yd0)t),
verified against a numerical CW integration to machine precision (control).

Cases: parent eccentricity e_p in {0, 0.1, 0.3, 0.7}; member ICs:
  ellipse: x0 = a, xd0 = 0, y0 = 0, yd0 = -2 n a   (the periodic CW member;
           uses the mean motion n, so at e_p > 0 the IC itself is what the
           closed form would call periodic -- flagged in the dossier)
  rest:    x0 = a, all relative velocities 0        (a formation at rest in
           the rotating frame; identical physical initial state for model
           and truth -- the clean model-error test)
a/R = 0.01 (the doc's own scale, H0203's dr/R).
Sampling: error at integer periods, plus the envelope (max |err|/a within
each period, sampled 4x per period).
Controls: e_p = 0 must stay small; step halving; closed form vs numerical CW.
"""
import json
import math

A_REL = 0.01
R = 1.0
N = 1.0
PERIOD = 2 * math.pi
STEPS_PER_PERIOD = 8000
N_PERIODS = 100
SAMPLES = [1, 2, 5, 10, 20, 50, 100]
ES = [0.0, 0.1, 0.3, 0.7]
ICS = ["ellipse", "rest"]
SUB = 4  # error samples per period, for the envelope


def kepler_state(t, e):
    M = N * t
    E = M
    for _ in range(80):
        d = (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
        E -= d
        if abs(d) < 1e-15:
            break
    x = R * (math.cos(E) - e)
    y = R * math.sqrt(1 - e * e) * math.sin(E)
    nE = N / (1 - e * math.cos(E))
    vx = -R * nE * math.sin(E)
    vy = R * nE * math.sqrt(1 - e * e) * math.cos(E)
    return x, y, vx, vy


def cw_closed_form(t, ic):
    x0, xd0, y0, yd0 = ic
    c, s = math.cos(N * t), math.sin(N * t)
    x = (xd0 / N) * s - (2 * yd0 / N + 3 * x0) * c + (2 * yd0 / N + 4 * x0)
    y = y0 + (2 * xd0 / N) * (c - 1) + 2 * (3 * x0 + 2 * yd0 / N) * s \
        - (6 * N * x0 + 3 * yd0) * t
    return x, y


def run_case(e, ic_name, steps_per_period):
    a = A_REL * R
    px, py, pvx, pvy = kepler_state(0.0, e)
    omega0 = (px * pvy - py * pvx) / (px * px + py * py)
    if ic_name == "ellipse":
        ic = (a, 0.0, 0.0, -2 * N * a)
    else:
        ic = (a, 0.0, 0.0, 0.0)
    x0, xd0, y0, yd0 = ic
    rn = math.hypot(px, py)
    urx, ury = px / rn, py / rn
    utx, uty = -ury, urx
    x = px + x0 * urx + y0 * utx
    y = py + x0 * ury + y0 * uty
    vx = pvx + xd0 * urx + (yd0 + omega0 * x0) * utx
    vy = pvy + xd0 * ury + (yd0 + omega0 * x0) * uty

    dt = PERIOD / steps_per_period
    ints = {}
    env = {}
    sample_set = set(SAMPLES)
    every = steps_per_period // SUB
    for step in range(1, steps_per_period * N_PERIODS + 1):
        r3i = 1.0 / (x * x + y * y) ** 1.5
        k1x, k1y, k1vx, k1vy = vx, vy, -x * r3i, -y * r3i
        x2, y2 = x + 0.5 * dt * k1x, y + 0.5 * dt * k1y
        r3i = 1.0 / (x2 * x2 + y2 * y2) ** 1.5
        k2x, k2y = vx + 0.5 * dt * k1vx, vy + 0.5 * dt * k1vy
        k2vx, k2vy = -x2 * r3i, -y2 * r3i
        x3, y3 = x + 0.5 * dt * k2x, y + 0.5 * dt * k2y
        r3i = 1.0 / (x3 * x3 + y3 * y3) ** 1.5
        k3x, k3y = vx + 0.5 * dt * k2vx, vy + 0.5 * dt * k2vy
        k3vx, k3vy = -x3 * r3i, -y3 * r3i
        x4, y4 = x + dt * k3x, y + dt * k3y
        r3i = 1.0 / (x4 * x4 + y4 * y4) ** 1.5
        k4x, k4y = vx + dt * k3vx, vy + dt * k3vy
        k4vx, k4vy = -x4 * r3i, -y4 * r3i
        x += (dt / 6.0) * (k1x + 2 * k2x + 2 * k3x + k4x)
        y += (dt / 6.0) * (k1y + 2 * k2y + 2 * k3y + k4y)
        vx += (dt / 6.0) * (k1vx + 2 * k2vx + 2 * k3vx + k4vx)
        vy += (dt / 6.0) * (k1vy + 2 * k2vy + 2 * k3vy + k4vy)
        if step % every == 0:
            t = step * dt
            pxt, pyt, _, _ = kepler_state(t, e)
            dx, dy = x - pxt, y - pyt
            rnt = math.hypot(pxt, pyt)
            urxt, uryt = pxt / rnt, pyt / rnt
            x_true = dx * urxt + dy * uryt
            y_true = -dx * uryt + dy * urxt
            xc, yc = cw_closed_form(t, ic)
            err = math.hypot(x_true - xc, y_true - yc) / a
            exc = math.hypot(x_true - x0, y_true - y0) / a
            k_period = step // steps_per_period + (1 if step % steps_per_period else 0)
            env[k_period] = max(env.get(k_period, 0.0), err)
            if step % steps_per_period == 0:
                k = step // steps_per_period
                if k in sample_set:
                    ints[k] = (err, exc)
    return ints, env


def cw_numeric_control():
    a = A_REL
    x, y, xd, yd = a, 0.0, 0.0, -2 * N * a
    dt = PERIOD / 8000

    def f(X, Y, XD, YD):
        return (XD, YD, 2 * N * YD + 3 * N * N * X, -2 * N * XD)

    worst = 0.0
    for i in range(8000 * N_PERIODS):
        k1 = f(x, y, xd, yd)
        k2 = f(x + .5 * dt * k1[0], y + .5 * dt * k1[1], xd + .5 * dt * k1[2], yd + .5 * dt * k1[3])
        k3 = f(x + .5 * dt * k2[0], y + .5 * dt * k2[1], xd + .5 * dt * k2[2], yd + .5 * dt * k2[3])
        k4 = f(x + dt * k3[0], y + dt * k3[1], xd + dt * k3[2], yd + dt * k3[3])
        x += (dt / 6) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        y += (dt / 6) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        xd += (dt / 6) * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
        yd += (dt / 6) * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3])
        if (i + 1) % 8000 == 0:
            t = (i + 1) * dt
            xc, yc = cw_closed_form(t, (a, 0.0, 0.0, -2 * N * a))
            worst = max(worst, math.hypot(x - xc, y - yc) / a)
    return worst


def main():
    results = {}
    for e in ES:
        for ic in ICS:
            ints, env = run_case(e, ic, STEPS_PER_PERIOD)
            results[f"e={e} {ic}"] = {
                "err_exc_at_periods": {k: [round(v[0], 4), round(v[1], 4)]
                                       for k, v in sorted(ints.items())},
                "err_envelope_max": round(max(env.values()), 4),
                "err_envelope_last10": round(max(list(env.values())[-10:]), 4),
            }
    ints, _ = run_case(0.3, "rest", STEPS_PER_PERIOD // 2)
    results["convergence e=0.3 rest half-step"] = {
        k: round(v[0], 4) for k, v in sorted(ints.items())}
    results["control closed-form vs numerical CW (100 periods)"] = {
        "max_dev_over_a": f"{cw_numeric_control():.2e}"}
    print(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
