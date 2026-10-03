"""Component study: the kick layer (parent tide on a doll) in the Hill regime.

Units: star-planet distance D=1, G(M_s+M_p)=1, so the planet's mean motion n_p=1.
Planetocentric frame, planar circular restricted three-body problem (same family
as r9 / B14: mu_p/mu_s = 1e-3).
"""
import numpy as np
from scipy.integrate import solve_ivp

MU_P = 1e-3 / (1 + 1e-3)      # planet GM
MU_S = 1.0 / (1 + 1e-3)       # star GM
D = 1.0                        # star-planet distance
NP = 1.0                       # planet mean motion about the star
RH = (MU_P / 3.0) ** (1.0 / 3.0)   # Hill radius
TWO_PI = 2 * np.pi


def n_moon(a):
    return np.sqrt(MU_P / a**3)


def state_from_elements(a, e, w, M, s):
    """Planar Kepler state around the planet. s=+1 prograde, -1 retrograde."""
    E = M.copy() if isinstance(M, np.ndarray) else M
    for _ in range(80):
        f = E - e * np.sin(E) - M
        fp = 1 - e * np.cos(E)
        d = f / fp
        E = E - d
        if np.max(np.abs(d)) < 1e-14:
            break
    cE, sE = np.cos(E), np.sin(E)
    r = a * (1 - e * cE)
    P, Q = a * (cE - e), a * np.sqrt(1 - e**2) * sE
    n = n_moon(a)
    Pd = -a * n * sE / (1 - e * cE)
    Qd = a * np.sqrt(1 - e**2) * n * cE / (1 - e * cE)
    cw, sw = np.cos(w), np.sin(w)
    x = P * cw - s * Q * sw
    y = P * sw + s * Q * cw
    vx = Pd * cw - s * Qd * sw
    vy = Pd * sw + s * Qd * cw
    return np.array([x, y, vx, vy])


def elements_from_state(y):
    x, yv, vx, vy = y
    r = np.hypot(x, yv)
    v2 = vx**2 + vy**2
    a = 1.0 / (2.0 / r - v2 / MU_P)
    ex = ((v2 - MU_P / r) * x - (x * vx + yv * vy) * vx) / MU_P
    ey = ((v2 - MU_P / r) * yv - (x * vx + yv * vy) * vy) / MU_P
    e = np.hypot(ex, ey)
    w = np.arctan2(ey, ex)
    return a, e, w


def star_pos(t):
    return np.array([np.cos(NP * t), np.sin(NP * t)])


def tide_acc(t, x, yv):
    sx, sy = np.cos(NP * t), np.sin(NP * t)
    dx, dy = sx - x, sy - yv
    d3 = (dx * dx + dy * dy) ** 1.5
    return (MU_S * (dx / d3 - sx), MU_S * (dy / d3 - sy))


def rhs_truth(t, y):
    x, yv, vx, vy = y
    r = np.hypot(x, yv)
    axg = -MU_P * x / r**3
    ayg = -MU_P * yv / r**3
    ax, ay = tide_acc(t, x, yv)
    return np.array([vx, vy, axg + ax, ayg + ay])


def truth_run(a0, e0, w0, M0, s, T_orb=30, rtol=1e-12, npts=3000):
    """Dense reference. Returns element time series and derived rates."""
    y0 = state_from_elements(a0, e0, w0, M0, s)
    T = TWO_PI * T_orb
    ts = np.linspace(0, T, npts)
    sol = solve_ivp(rhs_truth, (0, T), y0, method="DOP853", rtol=rtol,
                    atol=1e-14, t_eval=ts)
    t = sol.t
    x, yv = sol.y[0], sol.y[1]
    r = np.hypot(x, yv)
    v2 = sol.y[2]**2 + sol.y[3]**2
    a = 1.0 / (2.0 / r - v2 / MU_P)
    ex = ((v2 - MU_P / r) * x - (x * sol.y[2] + yv * sol.y[3]) * sol.y[2]) / MU_P
    ey = ((v2 - MU_P / r) * yv - (x * sol.y[2] + yv * sol.y[3]) * sol.y[3]) / MU_P
    e = np.hypot(ex, ey)
    w = np.unwrap(np.arctan2(ey, ex))
    escaped = (a[-1] < 0) or (r[-1] > 1.0)
    # fit window: skip transient
    i0, i1 = int(0.2 * npts), int(0.85 * npts)
    sel = slice(i0, i1)
    if e[sel].min() < 3e-3:
        wdot, apse = np.nan, False
    else:
        wdot = np.polyfit(t[sel], w[sel], 1)[0]
        apse = True
    return dict(t=t, a=a, e=e, w=w, wdot=wdot, apse=apse, escaped=escaped,
                a_med=np.nanmedian(a[sel]), e_med=np.nanmedian(e[sel]),
                e_min=e[sel].min(), e_max=e[sel].max())


# ---------------- candidate 1: double-averaged quadrupole (r9's kick-avg core)

def wdot_2Q(a, e, s):
    """Coplanar double-averaged quadrupole apsidal rate (prograde: advance)."""
    tau = (2.0 / 3.0) * (a / RH)**3
    return s * (3.0 / 8.0) * tau * n_moon(a) * np.sqrt(1 - e**2)


# ---------------- candidate 2: single-averaged quadrupole flow (evection kept)

def avg1Q_run(a0, e0, w0, s, T_orb=30, rtol=1e-10):
    """Slow flow of PhiBar2(a, e, w - lam), lam = n_p t. Zero moon-orbit events.

    Canonical (w, G signed): H = -MU_P^2/(2L^2) - C[(1+1.5e^2) + 7.5 e^2 cos2(w-lam)]
    with C = MU_S a^2 / (4 D^3), L = sqrt(MU_P a), e^2 = 1-(G/L)^2.
    Gdot = dPhi/dw ; wdot = -dPhi/dG.
    """
    L = np.sqrt(MU_P * a0)
    C = MU_S * a0**2 / 4.0
    G0 = s * L * np.sqrt(1 - e0**2)

    def rhs(t, y):
        G, w = y
        e2 = 1 - (G / L)**2
        e2 = max(e2, 1e-12)
        d = 2 * (w - NP * t)
        Gdot = -15 * C * e2 * np.sin(d)
        wdot = (3 * C * G / L**2) * (1 + 5 * np.cos(d))
        return np.array([Gdot, wdot])

    T = TWO_PI * T_orb
    sol = solve_ivp(rhs, (0, T), [G0, w0], method="DOP853", rtol=rtol, atol=1e-14,
                    t_eval=np.linspace(0, T, 2000))
    t = sol.t
    G, w = sol.y
    e = np.sqrt(np.maximum(1 - (G / L)**2, 0))
    w = np.unwrap(w)
    i0, i1 = int(0.2 * len(t)), int(0.85 * len(t))
    sel = slice(i0, i1)
    wdot = np.polyfit(t[sel], w[sel], 1)[0]
    return dict(t=t, e=e, w=w, wdot=wdot, e_med=np.nanmedian(e[sel]),
                e_max=e[sel].max())


# ---------------- candidate 3: kick-N (current design shape: WH split, DKD)

def elements_full(y, s):
    """(a, e, w, M) with the mirrored-element convention used throughout."""
    x, yv, vx, vy = y
    r = np.hypot(x, yv)
    v2 = vx**2 + vy**2
    a = 1.0 / (2.0 / r - v2 / MU_P)
    ex = ((v2 - MU_P / r) * x - (x * vx + yv * vy) * vx) / MU_P
    ey = ((v2 - MU_P / r) * yv - (x * vx + yv * vy) * vy) / MU_P
    e = np.hypot(ex, ey)
    w = np.arctan2(ey, ex)
    theta = np.arctan2(yv, x)
    f = np.arctan2(np.sin(s * (theta - w)), np.cos(s * (theta - w)))
    E = 2 * np.arctan2(np.sqrt(1 - e) * np.sin(f / 2), np.sqrt(1 + e) * np.cos(f / 2))
    M = E - e * np.sin(E)
    return a, e, w, M

def kickN_run(a0, e0, w0, M0, s, N, T_orb=30):
    """Exact Kepler drift + tidal kick, fixed step in the drift's own phase.

    DKD: half-drift by dM/2 along the current osculating orbit (elements
    re-derived, as the engine re-reads the compiled cycle), one tidal kick
    dv = a_tide*h at the midpoint, half-drift again. dM = 2*pi/N per step.
    """
    y = state_from_elements(a0, e0, w0, M0, s)
    t = 0.0
    T = TWO_PI * T_orb
    dM_half = np.pi / N
    w_hist, e_hist, t_hist = [], [], []
    step = 0
    rec_step = max(1, int(N * n_moon(a0) * T_orb / (2 * np.pi) / 2400) + 1)
    while t < T:
        a, e, w, M = elements_full(y, s)
        n = n_moon(a)
        h_half = dM_half / n
        y = state_from_elements(a, e, w, M + dM_half, s)   # half drift
        t += h_half
        ax, ay = tide_acc(t, y[0], y[1])                   # kick at midpoint
        y[2] += ax * (2 * h_half)
        y[3] += ay * (2 * h_half)
        t += h_half
        a, e, w, M = elements_full(y, s)
        y = state_from_elements(a, e, w, M + dM_half, s)   # half drift
        if step % rec_step == 0:
            w_hist.append(w)
            e_hist.append(e)
            t_hist.append(t)
        step += 1
    t_hist = np.array(t_hist)
    w_hist = np.unwrap(np.array(w_hist))
    e_hist = np.array(e_hist)
    i0, i1 = int(0.2 * len(t_hist)), int(0.85 * len(t_hist))
    sel = slice(i0, i1)
    if len(t_hist) < 10 or e_hist[sel].min() < 3e-3:
        wdot, apse = np.nan, False
    else:
        wdot = np.polyfit(t_hist[sel], w_hist[sel], 1)[0]
        apse = True
    return dict(wdot=wdot, apse=apse, e_med=np.nanmedian(e_hist[sel]),
                e_max=e_hist[sel].max(), a_end=a, escaped=(a < 0))


# ---------------- multipole truncation check (numerical double averages)

def double_avg_exact(a, e, w, nE=512, nlam=96):
    """Double average of the exact tide mu_s[1/|r-s| - 1/D - (r.s)/D^2],
    against its quadrupole part. Residual = octupole+hexadecapole+..."""
    Es = np.linspace(0, TWO_PI, nE, endpoint=False)
    rs = a * (1 - e * np.cos(Es))
    dM = (1 - e * np.cos(Es)) / np.sum(1 - e * np.cos(Es))
    f_t = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(Es / 2),
                         np.sqrt(1 - e) * np.cos(Es / 2))
    th = w + f_t
    xs, ys = rs * np.cos(th), rs * np.sin(th)
    lams = np.linspace(0, TWO_PI, nlam, endpoint=False)
    fulls, qs = [], []
    for lam in lams:
        ddx, ddy = np.cos(lam) - xs, np.sin(lam) - ys
        dist = np.hypot(ddx, ddy)
        tide_full = MU_S * (1 / dist - 1.0 - (xs * np.cos(lam) + ys * np.sin(lam)))
        proj2 = (xs * np.cos(lam) + ys * np.sin(lam))**2
        tide_q = MU_S * (3 * proj2 - rs**2) / 2
        fulls.append(np.sum(tide_full * dM))
        qs.append(np.sum(tide_q * dM))
    return np.mean(fulls), np.mean(qs), np.mean(fulls) - np.mean(qs)
