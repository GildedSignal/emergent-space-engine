"""Shared: the float oracle of the shipped dense-order scene, and the dwell arms.

Scene = exactly crates/space/src/events/dense.rs: planet at the origin, star at
(-1, 0) (separation = 1, mean motion = 1, planet mass fraction mu), rotating
axes, state y = (x, y, vx, vy) with
    dx/dt = vx + y        dvx/dt = a_x + vy
    dy/dt = vy - x        dvy/dt = a_y - vx
    a = -mu q/max(|q|,radius)^3 - (1-mu) d/|d|^3 + (1-mu, 0),   d = q + (1, 0)
(the shipped code softens only the planet term; radius = 2^-16 here).

ICs (the fleet-launch family): a point on the unit circle around the star at
heliocentric angle pi/3 + amp, at rest in the rotating frame -- a tadpole of L4
at its libration turning point, amplitude ~= amp (toward L3 for amp > 0).

The island test: an L4 tadpole never crosses the star-planet line and stays in
the co-orbital zone, so
    in_island: y > 0  and  0.5 < |q| < 1.5  and  0.5 < |d| < 1.5
leaving = crossing to a horseshoe or an encounter, or leaving the zone.
Dwell = continuous stay, first exit reported, cap in periods.

Arms: true (float RK4), q<Q> (+ state rounded to Q per step, the doc's error
model "one floor unit per event, carried forward"), noise<Q> (+/-Q/2 uniform per
step, hash-seeded: one splitmix64 draw per (step, lane, component)).

The kernel is numba-jitted (prange over lanes); the arithmetic per lane is
scalar and identical to the vectorised numpy form.
"""
import numpy as np
from numba import njit, prange

MU = 1e-3
RADIUS = 2.0 ** -16
STAR = 1.0 - MU
TWO_PI = 2.0 * np.pi
ZLO2, ZHI2 = 0.25, 2.25  # 0.5^2, 1.5^2

NPER = 512  # steps per period


@njit(cache=True, inline="always")
def _accel(x, y, out):
    r = np.sqrt(x * x + y * y)
    if r < RADIUS:
        r = RADIUS
    dx = x + 1.0
    d2 = dx * dx + y * y

@njit(cache=True, inline="always")
def _accel2(x, y):
    r = np.sqrt(x * x + y * y)
    if r < RADIUS:
        r = RADIUS
    dx = x + 1.0
    rd = np.sqrt(dx * dx + y * y)
    ir3 = 1.0 / (r * r * r)
    ird3 = 1.0 / (rd * rd * rd)
    return (-MU * x * ir3 - STAR * dx * ird3 + STAR,
            -MU * y * ir3 - STAR * y * ird3)
    ir3 = 1.0 / (r * r * r)
    ird3 = 1.0 / (rd * rd * rd)
    out[0] = -MU * x * ir3 - STAR * dx * ird3 + STAR
    out[1] = -MU * y * ir3 - STAR * y * ird3


@njit(cache=True)
def _run(ics, nsteps, h, quant, noise, seed, rec_flags, rec_buf):
    """ics (4, n) modified in place as the evolving state; returns esc step per lane.
    rec: when rec_flags[j] is 1, lane j's state every 16 steps goes to rec_buf[j]."""
    n = ics.shape[1]
    h2 = h / 2
    h6 = h / 6
    for j in prange(n):
        x, y, vx, vy = ics[0, j], ics[1, j], ics[2, j], ics[3, j]
        qr, nr = quant[j], noise[j]
        for i in range(1, nsteps + 1):
            # one RK4 step, stages written out
            ax, ay = _accel2(x, y)
            k1x, k1y = vx + y, vy - x
            k1vx, k1vy = ax + vy, ay - vx
            sx, sy, svx, svy = x + k1x * h2, y + k1y * h2, vx + k1vx * h2, vy + k1vy * h2
            ax, ay = _accel2(sx, sy)
            k2x, k2y = svx + sy, svy - sx
            k2vx, k2vy = ax + svy, ay - svx
            sx, sy, svx, svy = x + k2x * h2, y + k2y * h2, vx + k2vx * h2, vy + k2vy * h2
            ax, ay = _accel2(sx, sy)
            k3x, k3y = svx + sy, svy - sx
            k3vx, k3vy = ax + svy, ay - svx
            sx, sy, svx, svy = x + k3x * h, y + k3y * h, vx + k3vx * h, vy + k3vy * h
            ax, ay = _accel2(sx, sy)
            k4x, k4y = svx + sy, svy - sx
            k4vx, k4vy = ax + svy, ay - svx
            x += (k1x + 2 * k2x + 2 * k3x + k4x) * h6
            y += (k1y + 2 * k2y + 2 * k3y + k4y) * h6
            vx += (k1vx + 2 * k2vx + 2 * k3vx + k4vx) * h6
            vy += (k1vy + 2 * k2vy + 2 * k3vy + k4vy) * h6
            if qr > 0.0:
                x = np.round(x / qr) * qr
                y = np.round(y / qr) * qr
                vx = np.round(vx / qr) * qr
                vy = np.round(vy / qr) * qr
            if nr > 0.0:
                for c in range(4):
                    z = (seed + 0x9E3779B97F4A7C15 * (i * 4096 + j * 4 + c)) & 0xFFFFFFFFFFFFFFFF
                    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
                    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
                    u = ((z >> 11) * (1.0 / 9007199254740992.0) - 0.5) * nr
                    if c == 0:
                        x += u
                    elif c == 1:
                        y += u
                    elif c == 2:
                        vx += u
                    else:
                        vy += u
            if esc[j] < 0:
                q2 = x * x + y * y
                d2 = (x + 1.0) ** 2 + y * y
                if y <= 0.0 or q2 <= ZLO2 or q2 >= ZHI2 or d2 <= ZLO2 or d2 >= ZHI2:
                    esc[j] = i
            if rec_flags[j] == 1:
                b = rec_buf[j]
                if (i - 1) % 16 == 0 and (i - 1) < b.shape[0]:
                    b[i - 1, 0] = i
                    b[i - 1, 1] = x
                    b[i - 1, 2] = y
                    b[i - 1, 3] = vx
                    b[i - 1, 4] = vy
            if esc[j] > 0 and rec_flags[j] == 0:
                break
    return esc


def tadpole_ic(amp):
    """Position on the unit circle around the star at angle pi/3 + amp, at rest in
    the rotating frame (vx = -y, vy = x). amp in radians (array)."""
    th = np.pi / 3 + np.asarray(amp, float)
    qx = np.cos(th) - 1.0
    qy = np.sin(th)
    return np.stack([qx, qy, -qy, qx])


def dwell(ics, cap_periods, quant=0.0, noise=0.0, seed=1, dt_periods=None, rec=None):
    """First-exit time in periods (cap_periods if never). ics: (4, n) or (4,).
    rec: list of lane indices whose full trajectory (every 16 steps) is returned."""
    s = np.array(ics, float, copy=True)
    if s.ndim == 1:
        s = s[:, None]
    n = s.shape[1]
    dtp = dt_periods or 1.0 / NPER
    nsteps = int(round(cap_periods / dtp))
    h = dtp * TWO_PI
    qcol = np.full(n, quant, float)
    ncol = np.full(n, noise, float)
    flags = np.zeros(n, np.int8)
    bufsize = nsteps // 16 + 1
    bufs = None
    if rec:
        for j in rec:
            flags[j] = 1
        bufs = [np.full((bufsize, 5), np.nan) for _ in range(n)]
    else:
        bufs = [np.zeros((1, 5)) for _ in range(n)]
    esc = _run(s, nsteps, h, qcol, ncol, seed, flags, bufs)
    esc = np.where(esc < 0, nsteps, esc)
    trajs = {j: bufs[j][np.isfinite(bufs[j][:, 0])] for j in (rec or [])}
    return esc * dtp, trajs


def qrow(a, cap=None):
    cap = cap if cap is not None else a.max()
    return {"p50": float(np.median(a)), "p90": float(np.percentile(a, 90)),
            "p99": float(np.percentile(a, 99)), "max": float(a.max()),
            "capped": float((a >= cap - 1e-9).mean())}
