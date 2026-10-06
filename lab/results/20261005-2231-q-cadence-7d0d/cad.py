"""Float replica of the plane's kick layer (docs/law.md 'Perturbed motion').

Drift: exact Kepler in the doll (elliptic / hyperbolic anomaly, Newton in numpy),
anomaly taken directly from the state; retrograde orbits mirrored (exact).
Kick: DKD — drift H/2, perturbing acceleration at the midpoint tick (full
differential pull, never linearized) x H, drift H/2; rebind at every kick.
Step in the drift's own phase: H = P/N, P the current (osculating) period.

Planar (2D) restricted three-body scenes.
"""
import numpy as np

TWOPI = 2.0 * np.pi


def elements(x, y, vx, vy, gm):
    r = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    rdotv = x * vx + y * vy
    h = x * vy - y * vx
    E = v2 / 2 - gm / r
    a = -gm / (2 * E)
    ecc = np.sqrt(np.maximum(0.0, 1 + 2 * E * h * h / (gm * gm)))
    w = np.arctan2((v2 - gm / r) * y - rdotv * vy, (v2 - gm / r) * x - rdotv * vx)
    return a, ecc, w, h


def kepler_E(M, e):
    E = M + e * np.sin(M)
    for _ in range(5):
        f = E - e * np.sin(E) - M
        E = E - f / (1 - e * np.cos(E))
    if np.max(np.abs(e), initial=0) > 0.7:
        for _ in range(8):
            f = E - e * np.sin(E) - M
            E = E - f / (1 - e * np.cos(E))
    return E


def kepler_H(M, e):
    M = np.abs(M)
    Hh = np.log(1.0 + M / e + np.sqrt(1.0 + (M / e) ** 2))
    for _ in range(10):
        f = e * np.sinh(Hh) - Hh - M
        Hh = Hh - f / (e * np.cosh(Hh) - 1)
    return np.sign(M) * Hh


def state_from(M, a, e, w, gm):
    x = np.empty_like(a, dtype=float); y = np.empty_like(a, dtype=float)
    vx = np.empty_like(a, dtype=float); vy = np.empty_like(a, dtype=float)
    ell = e < 1
    cw = np.cos(w); sw = np.sin(w)
    if ell.any():
        E = kepler_E(M[ell], e[ell])
        cE, sE = np.cos(E), np.sin(E)
        n = np.sqrt(gm / a[ell] ** 3)
        den = 1 - e[ell] * cE
        xf = a[ell] * (cE - e[ell]); yf = a[ell] * np.sqrt(1 - e[ell] ** 2) * sE
        vxf = -a[ell] * n * sE / den; vyf = a[ell] * np.sqrt(1 - e[ell] ** 2) * n * cE / den
        x[ell] = xf * cw[ell] - yf * sw[ell]; y[ell] = xf * sw[ell] + yf * cw[ell]
        vx[ell] = vxf * cw[ell] - vyf * sw[ell]; vy[ell] = vxf * sw[ell] + vyf * cw[ell]
    if (~ell).any():
        Hh = kepler_H(M[~ell], e[~ell])
        cH, sH = np.cosh(Hh), np.sinh(Hh)
        n = np.sqrt(gm / (-a[~ell]) ** 3)
        den = e[~ell] * cH - 1
        xf = a[~ell] * (e[~ell] - cH); yf = a[~ell] * np.sqrt(e[~ell] ** 2 - 1) * sH
        vxf = -a[~ell] * n * sH / den; vyf = a[~ell] * np.sqrt(e[~ell] ** 2 - 1) * n * cH / den
        x[~ell] = xf * cw[~ell] - yf * sw[~ell]; y[~ell] = xf * sw[~ell] + yf * cw[~ell]
        vx[~ell] = vxf * cw[~ell] - vyf * sw[~ell]; vy[~ell] = vxf * sw[~ell] + vyf * cw[~ell]
    return x, y, vx, vy


def drift(x, y, vx, vy, gm, dt):
    """Exact Kepler drift by dt (any e), anomaly from the state (conditioned at high e)."""
    h = x * vy - y * vx
    ret = h < 0
    ym = np.where(ret, -y, y); vym = np.where(ret, -vy, vy)
    a, e, w, _ = elements(x, ym, vx, vym, gm)
    r = np.hypot(x, ym)
    vr = (x * vx + ym * vym) / r
    ell = e < 1
    M = np.empty_like(a)
    if ell.any():
        e_ = np.maximum(e[ell], 1e-12)
        cosE = (1 - r[ell] / a[ell]) / e_
        sinE = r[ell] * vr[ell] / (e_ * np.sqrt(gm * a[ell]))
        E = np.arctan2(sinE, cosE)
        E = np.where(e[ell] < 1e-12, np.arctan2(ym[ell], x[ell]), E)
        M[ell] = E - e[ell] * np.sin(E)
    if (~ell).any():
        sinhH = r[~ell] * vr[~ell] / (e[~ell] * np.sqrt(gm * (-a[~ell])))
        Hh = np.arcsinh(sinhH)
        M[~ell] = e[~ell] * np.sinh(Hh) - Hh
    n = np.sqrt(gm / np.abs(a) ** 3)
    xn, yn, vxn, vyn = state_from(M + n * dt, a, e, w, gm)
    yn = np.where(ret, -yn, yn); vyn = np.where(ret, -vyn, vyn)
    return xn, yn, vxn, vyn


class Doll:
    """Dominant mass gm at origin; perturbers (gm_j, D_j, n_j, phase_j[, e_j])
    on their own orbits about the origin. Full differential pull."""

    def __init__(self, gm, perturbers):
        self.gm = gm
        self.perturbers = perturbers

    def accel(self, x, y, t):
        ax = np.zeros_like(x); ay = np.zeros_like(y)
        for p in self.perturbers:
            M = p["ph"] + p["n"] * t
            if p.get("e", 0.0):
                E = kepler_E(M, p["e"])
                xs = p["D"] * (np.cos(E) - p["e"]); ys = p["D"] * np.sqrt(1 - p["e"] ** 2) * np.sin(E)
            else:
                xs = p["D"] * np.cos(M); ys = p["D"] * np.sin(M)
            dx = xs - x; dy = ys - y
            d3 = (dx * dx + dy * dy) ** 1.5
            ax += p["gm"] * (dx / d3 - xs / p["D"] ** 3)
            ay += p["gm"] * (dy / d3 - ys / p["D"] ** 3)
        return ax, ay


def run(doll, s0, T, N_fn, sample=None):
    """DKD, per-body cadence N (scalar or N_fn(a,e,w,x,y,t)->N array), H=P/N
    rebound each kick. sample: times; returns element series at the first kick
    past each sample time. Returns (series, final)."""
    x = s0["x"].copy(); y = s0["y"].copy(); vx = s0["vx"].copy(); vy = s0["vy"].copy()
    n_b = len(x); gm = doll.gm
    t = np.zeros(n_b)
    done = np.zeros(n_b, bool)
    kicks = np.zeros(n_b)
    out = None; si = 0
    if sample is not None:
        sample = np.asarray(sample, float)
        nt = len(sample)
        out = dict(t=np.zeros((nt, n_b)), a=np.zeros((nt, n_b)), e=np.zeros((nt, n_b)),
                   w=np.zeros((nt, n_b)), xa=np.zeros((nt, n_b)), ya=np.zeros((nt, n_b)))
    guard = 0
    while not done.all() and guard < 3000000:
        guard += 1
        a, e, w, hh = elements(x, y, vx, vy, gm)
        P = TWOPI * np.sqrt(np.abs(a) ** 3 / gm)
        N = N_fn(a, e, w, x, y, t) if callable(N_fn) else N_fn
        H = P / N
        H = np.where(done, 0.0, np.minimum(H, np.maximum(T - t, 0.0)))
        x, y, vx, vy = drift(x, y, vx, vy, gm, H / 2)
        t += H / 2
        ax, ay = doll.accel(x, y, t)
        vx = vx + ax * H; vy = vy + ay * H
        x, y, vx, vy = drift(x, y, vx, vy, gm, H / 2)
        t += H / 2
        kicks += (H > 0)
        if out is not None:
            while si < nt and (t >= sample[si]).any():
                aa, ee, ww, _ = elements(x, y, vx, vy, gm)
                out["t"][si] = t; out["a"][si] = aa; out["e"][si] = ee
                out["w"][si] = np.where(hh >= 0, ww, -ww)
                out["xa"][si] = x; out["ya"][si] = y
                si += 1
        done |= t >= T - 1e-9
    if out is not None:
        out = {k: v[:si] for k, v in out.items()}
    return out, dict(x=x, y=y, vx=vx, vy=vy, t=t, kicks=kicks)


def fit_rate(t, w):
    """per-body linear fit of the unwrapped apsidal angle (t, w are (nt, n_b))."""
    w = np.unwrap(w, axis=0)
    sl = np.zeros(w.shape[1])
    for j in range(w.shape[1]):
        A = np.vstack([t[:, j], np.ones(t.shape[0])]).T
        sol, *_ = np.linalg.lstsq(A, w[:, j], rcond=None)
        sl[j] = sol[0]
    return sl
