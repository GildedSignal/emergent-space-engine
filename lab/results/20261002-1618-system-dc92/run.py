#!/usr/bin/env python3
"""Eikonal river composition probe (system lens, run 20261002-1618-system-dc92).

Claim under test: for N static sources the river flow can be
    beta = -grad(chi),  |grad chi|^2 = -2 Phi,   Phi = sum_i -M_i/r_i,
chi being the Jacobi/Maupertuis action of free fall from rest at infinity.
For one mass chi = 2*sqrt(2Mr) -> exactly Doran. Theorems: curl-free
(beta is a gradient), Newtonian-exact for N (d2X/dT2 = -grad Phi for bodies
released at rest). Measured here: two-mass circumbinary periastron advance
vs Newtonian and vs the one-mass equivalent, plus controls.

Rays: free fall from rest at R_FAR; along a ray we carry Hess(chi) via
dH/dT = 2 Hess(Phi), and dx/dtheta (variational) for the Newton solve.
Query = root-find the ray through a point; beta = ray velocity, H = Hess chi.
"""
import json, math, sys, time
import numpy as np
from scipy.integrate import solve_ivp

t_start = time.time()
R_FAR = 1e5
R_CACHE = 8.0
K_RAYS = 1024

# ---------------- field: N static point masses ----------------
class Field:
    def __init__(self, masses):
        self.masses = masses
        self.Mt = sum(m for m, _, _ in masses)
    def phi(self, x, y):
        s = 0.0
        for m, mx, my in self.masses:
            r = math.hypot(x - mx, y - my)
            s -= m / r
        return s
    def grad(self, x, y):
        gx = gy = 0.0
        for m, mx, my in self.masses:
            dx = x - mx; dy = y - my; r3 = (dx * dx + dy * dy) ** 1.5
            gx += m * dx / r3; gy += m * dy / r3
        return gx, gy
    def hess(self, x, y):
        hxx = hxy = hyy = 0.0
        for m, mx, my in self.masses:
            dx = x - mx; dy = y - my; r2 = dx * dx + dy * dy
            r3 = r2 ** 1.5; r5 = r2 ** 2.5
            hxx += m * (1.0 / r3 - 3 * dx * dx / r5)
            hyy += m * (1.0 / r3 - 3 * dy * dy / r5)
            hxy += m * (-3 * dx * dy / r5)
        return hxx, hxy, hyy

# ---------------- ray ODE: [x,y,vx,vy,ax,ay,bx,by] ----------------
# a = dx/dtheta (congruence derivative), b = dv/dtheta.
# Hess chi is RECOVERED at query time from (v, a, b): the naive transport
# dH/dT = Hess(Phi) + H^2 is exact but has a positive-eigenvalue runaway.
def ray_rhs(s, f):
    x, y, vx, vy, ax_, ay_, bx_, by_ = s
    gx, gy = f.grad(x, y)
    hxx, hxy, hyy = f.hess(x, y)
    return (vx, vy, -gx, -gy, bx_, by_,
            -(hxx * ax_ + hxy * ay_), -(hxy * ax_ + hyy * ay_))

def ray_rhs_np(T, s, f):
    return ray_rhs(list(s), f)

def build_table(f):
    """K rays from rest at R_FAR, integrated to the first crossing of R_CACHE."""
    ths = np.linspace(0.0, 2 * math.pi, K_RAYS, endpoint=False)
    tab = np.empty((K_RAYS, 8))
    for k, th in enumerate(ths):
        c, s_ = math.cos(th), math.sin(th)
        x0 = R_FAR * c; y0 = R_FAR * s_
        st = [x0, y0, 0.0, 0.0, -R_FAR * s_, R_FAR * c, 0.0, 0.0]
        def ev(T, s, f):
            return math.hypot(s[0], s[1]) - R_CACHE
        ev.terminal = True; ev.direction = -1
        sol = solve_ivp(ray_rhs_np, (0.0, 1e12), st, args=(f,), method="DOP853",
                        rtol=1e-10, atol=1e-12, events=ev)
        assert sol.status == 1, f"ray {k} never reached cache circle"
        tab[k] = sol.y[:, -1]
    return ths, tab

class RiverEval:
    """Query beta(X) and Hess chi(X) by root-finding the ray through X."""
    def __init__(self, f, ths, tab):
        self.f = f; self.ths = ths; self.tab = tab
        self.warm = None
        self.nq = 0
        self.asym = 0.0
    def _interp(self, th):
        u = (th % (2 * math.pi)) / (2 * math.pi) * K_RAYS
        k0 = int(u) % K_RAYS; k1 = (k0 + 1) % K_RAYS; w = u - math.floor(u)
        return self.tab[k0] * (1 - w) + self.tab[k1] * w
    def _step(self, s, h):
        k1 = ray_rhs(s, self.f)
        s2 = [s[i] + 0.5 * h * k1[i] for i in range(8)]
        k2 = ray_rhs(s2, self.f)
        s3 = [s[i] + 0.5 * h * k2[i] for i in range(8)]
        k3 = ray_rhs(s3, self.f)
        s4 = [s[i] + h * k3[i] for i in range(8)]
        k4 = ray_rhs(s4, self.f)
        return [s[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(8)]
    def _segment(self, th, r0):
        s = list(self._interp(th))
        n = 0
        while True:
            n += 1
            if n > 4000:
                raise RuntimeError("segment runaway")
            h = min(0.3 * math.hypot(s[0], s[1]), 1.5)
            s1 = self._step(s, h)
            if not (s1[0] == s1[0] and s1[1] == s1[1]):
                raise RuntimeError("NaN in segment")
            if math.hypot(s1[0], s1[1]) <= r0:
                lo, hi = 0.0, h; s_lo = s
                for _ in range(22):
                    mid = 0.5 * (lo + hi)
                    s_mid = self._step(s_lo, mid)
                    if math.hypot(s_mid[0], s_mid[1]) > r0:
                        lo = mid
                    else:
                        hi = mid
                return self._step(s_lo, hi)
            s = s1
    def query(self, X, Y):
        self.nq += 1
        r0 = math.hypot(X, Y); tgt = math.atan2(Y, X)
        th = self.warm if self.warm is not None else tgt
        sc = None
        for it in range(10):
            try:
                sc = self._segment(th, r0)
            except RuntimeError:
                th = tgt + 1e-3 * (it + 1)   # reset and retry nearby
                continue
            ang = math.atan2(sc[1], sc[0])
            g = (ang - tgt + math.pi) % (2 * math.pi) - math.pi
            # d(ang)/dtheta = (x*ay - y*ax)/r^2 with a = dx/dtheta = (sc[7],sc[8])
            dgdth = (sc[0] * sc[5] - sc[1] * sc[4]) / (sc[0] ** 2 + sc[1] ** 2)
            if abs(dgdth) < 1e-14:
                th = tgt + 1e-3 * (it + 1)
                continue
            dth = g / dgdth
            dth = max(-0.1, min(0.1, dth))
            th -= dth
            if abs(dth) < 1e-13:
                break
        if sc is None:
            raise RuntimeError(f"query failed at ({X},{Y})")
        self.warm = th
        beta = (sc[2], sc[3])
        # recover grad beta (and H = -grad beta) from the congruence Jacobian
        x, y, vx, vy, ax_, ay_, bx_, by_ = sc
        det = ax_ * vy - ay_ * vx
        gth = (vy / det, -vx / det)          # grad(theta)
        gT = (-ay_ / det, ax_ / det)         # grad(T) along the congruence
        gx, gy = self.f.grad(x, y)
        bdot = (-gx, -gy)                    # ray acceleration = beta dot
        gbx = bx_ * gth[0] + bdot[0] * gT[0]
        gby = bx_ * gth[1] + bdot[0] * gT[1]
        Hxx = -gbx
        Hyy = -(by_ * gth[1] + bdot[1] * gT[1])
        Hxy = -0.5 * ((bx_ * gth[1] + bdot[0] * gT[1]) + (by_ * gth[0] + bdot[1] * gT[0]))
        self.asym = abs((bx_ * gth[1] + bdot[0] * gT[1]) - (by_ * gth[0] + bdot[1] * gT[0]))
        H = (Hxx, Hxy, Hyy)
        resid = sc[2] ** 2 + sc[3] ** 2 + 2 * self.f.phi(sc[0], sc[1])
        return beta, H, resid

# ---------------- generic 4-dim RK4 orbit ----------------
def _integrate(s, rhs, norbits, spo, Mt_for_period, r_start):
    T_orb = 2 * math.pi * math.sqrt(r_start ** 3 / Mt_for_period)
    h = T_orb / spo
    T = 0.0; traj = []
    for _ in range(norbits * spo):
        k1 = rhs(s)
        s2 = [s[j] + 0.5 * h * k1[j] for j in range(4)]
        k2 = rhs(s2)
        s3 = [s[j] + 0.5 * h * k2[j] for j in range(4)]
        k3 = rhs(s3)
        s4 = [s[j] + h * k3[j] for j in range(4)]
        k4 = rhs(s4)
        s = [s[j] + h / 6 * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j]) for j in range(4)]
        T += h
        traj.append((T, math.hypot(s[0], s[1]), math.atan2(s[1], s[0])))
    return pericenters(traj)

def pericenters(traj):
    out = []
    for i in range(1, len(traj) - 1):
        T0, r0, a0 = traj[i - 1]; T1, r1, a1 = traj[i]; T2, r2, a2 = traj[i + 1]
        if r1 < r0 and r1 <= r2:
            den = (r0 - 2 * r1 + r2)
            if abs(den) < 1e-300:
                continue
            w = 0.5 * (r0 - r2) / den
            d1 = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
            out.append((T1, r1, a0 + (1 + w) * d1))
    return out

def advance(peris):
    if len(peris) < 4:
        return None
    raw = [p[2] for p in peris]
    un = [raw[0]]
    for i in range(1, len(raw)):
        d = raw[i] - raw[i - 1]
        d = (d + math.pi) % (2 * math.pi) - math.pi
        un.append(un[i - 1] + d)
    idx = np.arange(len(un), dtype=float)
    A = np.vstack([idx, np.ones_like(idx)]).T
    slope, _ = np.linalg.lstsq(A, np.array(un), rcond=None)[0]
    rmin = min(p[1] for p in peris); rmax = max(p[1] for p in peris)
    return dict(slope=float(slope), n_peri=len(un), rmin=float(rmin),
                rmax=float(rmax))

def river_rhs_factory(ev):
    def rhs(s):
        X, Y, px, py = s
        ps = px * px + py * py
        ux = px / math.sqrt(1 + ps); uy = py / math.sqrt(1 + ps)
        (bx, by), (Hxx, Hxy, Hyy), _ = ev.query(X, Y)
        return (ux + bx, uy + by, Hxx * px + Hxy * py, Hxy * px + Hyy * py)
    return rhs

def doran_rhs_factory(masses):
    """Analytic sum of per-mass Doran flows: beta = -sum grad chi_i, H = sum H_i.
    With one mass this is exact Doran; with several it is the additive-chi
    negative control."""
    def rhs(s):
        X, Y, px, py = s
        ps = px * px + py * py
        ux = px / math.sqrt(1 + ps); uy = py / math.sqrt(1 + ps)
        bx = by = 0.0; Hxx = Hxy = Hyy = 0.0
        for m, mx, my in masses:
            dx = X - mx; dy = Y - my; r = math.hypot(dx, dy)
            cp = math.sqrt(2 * m / r); cpp = -0.5 * cp / r
            c, s_ = dx / r, dy / r
            bx += -cp * c; by += -cp * s_
            Hxx += cpp * c * c + (cp / r) * s_ * s_
            Hyy += cpp * s_ * s_ + (cp / r) * c * c
            Hxy += (cpp - cp / r) * c * s_
        return (ux + bx, uy + by, Hxx * px + Hxy * py, Hxy * px + Hyy * py)
    return rhs

def newtonian_rhs_factory(f):
    def rhs(s):
        X, Y, vx, vy = s
        gx, gy = f.grad(X, Y)
        return (vx, vy, -gx, -gy)
    return rhs

def start_state(rp, speed):
    """Newtonian-matched start: total velocity v0 tangential at (rp, 0)."""
    return [rp, 0.0, 0.0, speed]

def start_state_river(rp, speed, beta0):
    """River start with the SAME total initial velocity: u0 = v0 - beta(X0).
    beta0 = (bx, by) is the flow at (rp, 0). Per unit mass p = gamma_u * u."""
    ux = -beta0[0]; uy = speed - beta0[1]
    q = math.sqrt(1 - ux * ux - uy * uy)
    return [rp, 0.0, ux / q, uy / q]

def doran_beta(masses, X, Y):
    bx = by = 0.0
    for m, mx, my in masses:
        dx = X - mx; dy = Y - my; r = math.hypot(dx, dy)
        cp = math.sqrt(2 * m / r)
        bx += -cp * dx / r; by += -cp * dy / r
    return (bx, by)

A_ORB, ECC = 4.5, 0.2
RP = A_ORB * (1 - ECC)

def v_newtonian(Mt, rp=RP, a=A_ORB):
    return math.sqrt(Mt * (2 / rp - 1 / a))

def run_config(name, masses, norbits=20, spo=120):
    f = Field(masses)
    v0 = v_newtonian(f.Mt)
    out = {"name": name, "Mt": f.Mt, "masses": masses}
    t0 = time.time()
    ths, tab = build_table(f)
    out["table_s"] = round(time.time() - t0, 1)
    ev = RiverEval(f, ths, tab)
    res = advance(_integrate(start_state_river(RP, v0, ev.query(RP, 0.0)[0]),
                             river_rhs_factory(ev),
                              norbits, spo, f.Mt, RP))
    res["queries"] = ev.nq
    mx = 0.0
    for i in range(32):
        X = 4.5 * math.cos(2 * math.pi * i / 32); Y = 4.5 * math.sin(2 * math.pi * i / 32)
        _, _, rr = ev.query(X, Y)
        mx = max(mx, abs(rr))
    res["eikonal_resid_max"] = mx
    out["river_ray"] = res
    out["newtonian"] = advance(_integrate(start_state(RP, v0),
                           newtonian_rhs_factory(f), norbits, 2 * spo, f.Mt, RP))
    return out

if __name__ == "__main__":
    results = {}
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"

    if stage in ("all", "ctl"):
        vB = v_newtonian(0.03)
        results["B_analytic_doran"] = advance(_integrate(
            start_state_river(RP, vB, doran_beta([(0.03, 0.0, 0.0)], RP, 0.0)),
            doran_rhs_factory([(0.03, 0.0, 0.0)]),
             30, 150, 0.03, RP))
        results["E_newtonian_kepler"] = advance(_integrate(
            start_state(RP, vB), newtonian_rhs_factory(Field([(0.03, 0.0, 0.0)])),
            30, 300, 0.03, RP))

    if stage in ("all", "main"):
        results["A_eikonal"] = run_config(
            "A", [(0.015, -0.75, 0.0), (0.015, 0.75, 0.0)])
        results["C_pipeline_onemass"] = run_config("C", [(0.03, 0.0, 0.0)])
        results["F_additive_chi"] = advance(_integrate(
            start_state_river(RP, v_newtonian(0.03),
                              doran_beta([(0.015, -0.75, 0.0), (0.015, 0.75, 0.0)], RP, 0.0)),
            doran_rhs_factory([(0.015, -0.75, 0.0), (0.015, 0.75, 0.0)]),
             30, 150, 0.03, RP))

    if stage in ("all", "nu"):
        results["G_eikonal"] = run_config(
            "G", [(0.0225, -0.375, 0.0), (0.0075, 1.125, 0.0)])

    print(json.dumps(results, indent=1, default=float))
    with open(f"results-{stage}.json", "w") as fh:
        json.dump(results, fh, indent=1, default=float)
    print("wall", round(time.time() - t_start, 1), file=sys.stderr)
