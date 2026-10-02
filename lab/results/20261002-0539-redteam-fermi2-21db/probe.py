#!/usr/bin/env python3
"""Red-team of the Fermi frame's phase 2 (Schwarzschild tide), before it is built.

Oracle: exact Schwarzschild geodesics (origin tube + members), Fermi coordinates
reconstructed exactly (parallel-transported tetrad + orthogonal projection).
Laws in the frame (integrated finely; epoch/quantization cost is phase 1's, E3):
  L1: x" = -E_true(tau) x   (the premise: the Schwarzschild tidal tensor projected
      on the parallel-transported frame; law.md dense order)
  L2: x" = -E_naive(tau) x  (phase 1's kernel (M/r^3)(I - 3 rr^T) reused with a
      relativistic tube readout: axis = the coordinate radial direction)
  L3: x" = -Ebar x           (E_true orbit-averaged: the averaging temptation)

Units G = c = M = 1. Equatorial (the game is 2D). Floats explore; this probe
measures representation validity, not integer exactness.
"""
import argparse, json, math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline

M = 1.0

def f_of(r): return 1.0 - 2.0 * M / r

def gdot(a, b, r):
    f = f_of(r)
    return -f * a[0] * b[0] + a[1] * b[1] / f + r * r * a[2] * b[2]

# Riemann, static orthonormal frame, indices 0=t,1=r,2=ph; template with w=M/r^3=1.
_RT = np.zeros((3, 3, 3, 3))
_BASE = {(0, 1, 0, 1): -2.0, (0, 2, 0, 2): 1.0, (1, 2, 1, 2): 1.0}
# symmetry group: identity; swap(a,b)[-]; swap(c,d)[-]; swap pairs[+]; compositions
_GRP = [((0, 1, 2, 3), +1.0), ((1, 0, 2, 3), -1.0), ((0, 1, 3, 2), -1.0),
        ((2, 3, 0, 1), +1.0), ((1, 0, 3, 2), +1.0), ((3, 2, 0, 1), -1.0),
        ((2, 3, 1, 0), -1.0), ((3, 2, 1, 0), +1.0)]
RT = np.zeros((3, 3, 3, 3))
for a in range(3):
    for b in range(3):
        for c in range(3):
            for d in range(3):
                for perm, chi in _GRP:
                    q = (a, b, c, d)
                    key = (q[perm[0]], q[perm[1]], q[perm[2]], q[perm[3]])
                    if key in _BASE:
                        RT[a, b, c, d] = chi * _BASE[key]
                        break

def geo_rhs(s, y):
    t, r, ph, ut, ur, uph = y
    f = f_of(r)
    return [ut, ur, uph,
            -2 * M / (r * r * f) * ut * ur,
            -M * f / (r * r) * ut * ut + M / (r * r * f) * ur * ur + r * f * uph * uph,
            -2 * uph * ur / r]

def trans_rhs(u, e, r):
    f = f_of(r)
    et, er, eph = e
    return [-M / (r * r * f) * (u[1] * et + u[0] * er),
            -M * f / (r * r) * u[0] * et + M / (r * r * f) * u[1] * er + r * f * u[2] * eph,
            -(u[1] * eph + u[2] * er) / r]

def origin_rhs(tau, y):
    dy = geo_rhs(tau, y[:6])
    return dy + list(trans_rhs(y[3:6], y[6:9], y[1])) + list(trans_rhs(y[3:6], y[9:12], y[1]))

def plunge_ev(tau, y): return y[1] - 2.05
plunge_ev.terminal, plunge_ev.direction = True, -1

def to_orth(V, r):
    f = math.sqrt(f_of(r))
    return np.array([V[0] * f, V[1] / f, r * V[2]])

class Origin:
    def __init__(self, y0, tau_end, n_dense=4000):
        ev = solve_ivp(origin_rhs, [0, tau_end], y0, method="DOP853",
                       rtol=1e-12, atol=1e-13, dense_output=True,
                       max_step=tau_end / 500, events=plunge_ev)
        assert ev.success, ev.message
        self.plunged = len(ev.t_events[0]) > 0
        self.tau_end = float(ev.t[-1])
        self.tau = np.linspace(0, self.tau_end, n_dense)
        Y = ev.sol(self.tau)
        self.Y, self.t, self.r, self.ph = Y, Y[0], Y[1], Y[2]
        # E_true: Rhat_{ABCD} e_a^A u^C e_b^B u^D (vectorised over grid)
        n = self.tau.size
        U = np.empty((n, 3)); E1 = np.empty((n, 3)); E2 = np.empty((n, 3))
        for i in range(n):
            r = self.r[i]
            U[i] = to_orth(Y[3:6, i], r); E1[i] = to_orth(Y[6:9, i], r); E2[i] = to_orth(Y[9:12, i], r)
        w = M / self.r**3
        Ehat = np.einsum("acbd,nc,nd->nab", RT, U, U)      # electric part seen by u
        E = np.empty((n, 2, 2))
        E[:, 0, 0] = w * np.einsum("na,nab,nb->n", E1, Ehat, E1)
        E[:, 0, 1] = w * np.einsum("na,nab,nb->n", E1, Ehat, E2)
        E[:, 1, 0] = E[:, 0, 1]
        E[:, 1, 1] = w * np.einsum("na,nab,nb->n", E2, Ehat, E2)
        self.E = E
        # inertial x-axis angle in the Fermi axes
        f_ = np.sqrt(f_of(self.r))
        cph, sph = np.cos(self.ph), np.sin(self.ph)
        v1 = np.array([cph, -sph / self.r]); v2 = np.array([sph, cph / self.r])  # (r^,ph^) coeffs
        a1 = v1[0] * Y[6] / f_of(self.r) + self.r**2 * v1[1] * Y[8]
        a2 = v1[0] * Y[9] / f_of(self.r) + self.r**2 * v1[1] * Y[11]
        self.alpha = np.unwrap(np.arctan2(a2, a1))
        self.spl = {"r": CubicSpline(self.tau, self.r), "ph": CubicSpline(self.tau, self.ph),
                    "alpha": CubicSpline(self.tau, self.alpha),
                    "E11": CubicSpline(self.tau, E[:, 0, 0]), "E12": CubicSpline(self.tau, E[:, 0, 1]),
                    "E22": CubicSpline(self.tau, E[:, 1, 1])}
        dev = 0.0
        for i in range(0, n, 40):
            r = self.r[i]; u = Y[3:6, i]
            dev = max(dev, abs(gdot(u, u, r) + 1), abs(gdot(Y[6:9, i], Y[6:9, i], r) - 1),
                      abs(gdot(Y[9:12, i], Y[9:12, i], r) - 1), abs(gdot(Y[6:9, i], Y[9:12, i], r)),
                      abs(gdot(u, Y[6:9, i], r)), abs(gdot(u, Y[9:12, i], r)))
        self.tetrad_dev = dev
        self.thnaive = np.unwrap(self.ph - self.alpha)     # naive kernel axis, Fermi axes
        ax = np.unwrap(np.arctan2(2 * E[:, 0, 1], E[:, 0, 0] - E[:, 1, 1]) / 2)
        # principal axis of -E (stretch axis): eigen of -E has angle of E's minor axis; use E's
        self.ax = ax

# ---------------------------------------------------------------- oracle members
class Member:
    def __init__(self, y0, s_end):
        self.ev = solve_ivp(geo_rhs, [0, s_end], y0, method="DOP853", rtol=1e-12, atol=1e-13,
                            dense_output=True, events=plunge_ev)
        self.plunged = len(self.ev.t_events[0]) > 0
        s = np.linspace(0, self.ev.t[-1], 40001)
        Y = self.ev.sol(s)
        self.ts, self.rs, self.phs = Y[0], Y[1], Y[2]

def fermi_X(member, origin, i, prev=None):
    """Exact Fermi coordinates of the member at grid index i of the origin.
    prev = (tm_prev, sep_prev) warm-starts an expanding bracket (separations grow
    by e^11 per orbit under shear, so any fixed window loses the foot)."""
    Y = origin.Y[:, i]
    to, ro, pho = Y[0], Y[1], Y[2]
    u, e1, e2 = Y[3:6], Y[6:9], Y[9:12]
    f = f_of(ro)
    def F(tm):
        rm = np.interp(tm, member.ts, member.rs); pm = np.interp(tm, member.ts, member.phs)
        d = (tm - to, rm - ro, pm - pho)
        return -f * d[0] * u[0] + d[1] * u[1] / f + ro * ro * d[2] * u[2]
    if prev is None:
        t_mid, sep = to, max(member.X0n, 1e-6)
    else:
        t_mid, sep = prev
    W = 3.0 * sep + 10.0
    lo, hi = t_mid - W, t_mid + W
    flo, fhi = F(lo), F(hi)
    for _ in range(60):
        if (flo > 0) != (fhi > 0): break
        W *= 2.0
        lo, hi = t_mid - W, t_mid + W
        flo, fhi = F(lo), F(hi)
    if (flo > 0) == (fhi > 0):
        return None
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        fm = F(mid)
        if (fm > 0) == (flo > 0): lo, flo = mid, fm
        else: hi = mid
    tm = 0.5 * (lo + hi)
    rm = np.interp(tm, member.ts, member.rs); pm = np.interp(tm, member.ts, member.phs)
    d = (tm - to, rm - ro, pm - pho)
    X1 = -f * d[0] * e1[0] + d[1] * e1[1] / f + ro * ro * d[2] * e1[2]
    X2 = -f * d[0] * e2[0] + d[1] * e2[1] / f + ro * ro * d[2] * e2[2]
    return np.array([X1, X2]), tm

# ---------------------------------------------------------------- laws
def law_run(origin, X0, V0, kind):
    if kind == "L3":
        # fairest cheap memoisation: constant (median) eigenvalues, axis rate from a
        # linear fit of the true axis angle. Exact for circular; drops the periapsis
        # spike on eccentric tubes (the r9 kill zone).
        E = origin.E
        tr2 = (E[:, 0, 0] + E[:, 1, 1]) / 2
        rad = np.sqrt(((E[:, 0, 0] - E[:, 1, 1]) / 2) ** 2 + E[:, 0, 1] ** 2)
        lm, lp = float(np.median(tr2 - rad)), float(np.median(tr2 + rad))
        b, a = np.polyfit(origin.tau, origin.ax, 1)
        def Efun(t):
            th = a + b * t
            c, s = math.cos(th), math.sin(th)
            R = np.array([[c, -s], [s, c]])
            return R @ np.diag([lp, lm]) @ R.T
    elif kind == "L1":
        s11, s12, s22 = origin.spl["E11"], origin.spl["E12"], origin.spl["E22"]
        def Efun(t):
            return np.array([[s11(t), s12(t)], [s12(t), s22(t)]])
    else:
        rs, phs, als = origin.spl["r"], origin.spl["ph"], origin.spl["alpha"]
        def Efun(t):
            r = float(rs(t)); th = float(phs(t)) - float(als(t))
            nn = np.array([math.cos(th), math.sin(th)])
            return (M / r**3) * (np.eye(2) - 3.0 * np.outer(nn, nn))
    def rhs(t, y):
        return np.concatenate([y[2:], -Efun(t) @ y[:2]])
    ev = solve_ivp(rhs, [0, origin.tau_end], np.concatenate([X0, V0]),
                   method="DOP853", rtol=1e-12, atol=1e-14, dense_output=True)
    assert ev.success
    return ev

# ---------------------------------------------------------------- scenes
def circular_y0(r0):
    L = r0 * math.sqrt(M / (r0 - 3 * M))
    E = (1 - 2 * M / r0) / math.sqrt(1 - 3 * M / r0)
    return np.array([0.0, r0, 0.0, E / f_of(r0), 0.0, L / r0**2])

def ecc_y0(rp, L):
    E = math.sqrt((1 - 2 * M / rp) * (1 + L * L / rp**2))
    return np.array([0.0, rp, 0.0, E / f_of(rp), 0.0, L / rp**2])

def tetradize(y0):
    r0 = y0[1]
    e1 = np.array([0.0, math.sqrt(f_of(r0)), 0.0])
    c = np.array([0.0, 0.0, 1.0])
    e2 = c + gdot(c, y0[3:6], r0) * y0[3:6]
    e2 = e2 / math.sqrt(gdot(e2, e2, r0))
    return np.concatenate([y0, e1, e2])

SCENES = [
    dict(name="circ-r1000", y0=lambda: circular_y0(1000.0), T=2*math.pi*1000**1.5),
    dict(name="circ-r50",   y0=lambda: circular_y0(50.0),   T=2*math.pi*50**1.5),
    dict(name="circ-r20",   y0=lambda: circular_y0(20.0),   T=2*math.pi*20**1.5),
    dict(name="circ-r10",   y0=lambda: circular_y0(10.0),   T=2*math.pi*10**1.5),
    dict(name="circ-r6",    y0=lambda: circular_y0(6.0),    T=2*math.pi*6**1.5),
    dict(name="circ-r3.1",  y0=lambda: circular_y0(3.1),    T=2*math.pi*3.1**1.5),
    dict(name="ecc-rp6.5-L3.5", y0=lambda: ecc_y0(6.5, 3.5), T=2*math.pi*7.35**1.5),
    dict(name="plunge-r4",  y0=lambda: ecc_y0(4.0, 2.757),  T=100.0),
]

def do_scene(scene, laws=("L1", "L2", "L3")):
    origin = Origin(tetradize(scene["y0"]()), scene["T"])
    n = len(origin.tau)
    res = dict(name=scene["name"], plunged=origin.plunged, tau_end=origin.tau_end,
               tetrad_dev=origin.tetrad_dev, T_orbit=scene["T"], members=[], kernel={}, epochs={})
    nrm = np.linalg.norm(origin.E, axis=(1, 2))
    Enaive = np.empty_like(origin.E)
    th = origin.thnaive
    nn = np.stack([np.cos(th), np.sin(th)], axis=1)
    Enaive[:, 0, 0] = (M / origin.r**3) * (1 - 3 * nn[:, 0] * nn[:, 0])
    Enaive[:, 0, 1] = (M / origin.r**3) * (-3 * nn[:, 0] * nn[:, 1])
    Enaive[:, 1, 0] = Enaive[:, 0, 1]
    Enaive[:, 1, 1] = (M / origin.r**3) * (1 - 3 * nn[:, 1] * nn[:, 1])
    dax = np.gradient(origin.ax, origin.tau)
    dth = np.gradient(th, origin.tau)
    dE = np.gradient(origin.E, origin.tau, axis=0)
    res["kernel"] = dict(
        max_rel=float((np.linalg.norm(Enaive - origin.E, axis=(1, 2)) / np.maximum(nrm, 1e-300)).max()),
        axis_diff_max=float(np.abs(((origin.ax - th + math.pi/2) % math.pi) - math.pi/2).max()))
    res["epochs"] = dict(
        axis_true=float(np.trapezoid(np.abs(dax), origin.tau) * 256),
        axis_naive=float(np.trapezoid(np.abs(dth), origin.tau) * 256),
        tensor_true=float(np.trapezoid(np.linalg.norm(dE, axis=(1, 2)) / np.maximum(nrm, 1e-300),
                                       origin.tau) * 256))
    # members
    r0 = origin.r[0]; Rcurv = math.sqrt(r0**3 / (2 * M)); x18 = 0.018 * Rcurv
    mem_defs = [(np.array([x18, 0.0]), np.zeros(2), "rad-0.018"),
                (np.array([0.0, x18]), np.zeros(2), "tan-0.018"),
                (np.array([0.1 * Rcurv, 0.0]), np.zeros(2), "rad-0.1"),
                (np.array([0.0, x18]), 0.3 * np.array([1.0, 0.0]), "tan-0.018-v0.3")]
    u, e1, e2 = origin.Y[3:6, 0], origin.Y[6:9, 0], origin.Y[9:12, 0]
    for X0, V0, tag in mem_defs:
        gam = 1 / math.sqrt(1 - V0 @ V0)
        U = gam * (u + V0[0] * e1 + V0[1] * e2)
        P = np.array([origin.t[0], r0, origin.ph[0]]) + X0[0] * e1 + X0[1] * e2
        member = Member(np.concatenate([P, U]), 5 * origin.tau_end + 10)
        if member.plunged or not np.all(np.isfinite(member.rs)):
            res["members"].append(dict(tag=tag, oracle="plunged")); continue
        member.X0n = float(np.linalg.norm(X0)); member.V0n = float(np.linalg.norm(V0))
        # sequential exact reconstruction along a coarse tau grid (warm-started bracket)
        stride = max(1, n // 200)
        Xt, prev = [], None
        for i in range(0, n, stride):
            out = fermi_X(member, origin, i, prev)
            if out is None: break
            Xv, tm = out
            Xt.append(Xv)
            prev = (tm, float(np.linalg.norm(Xv)) + 1e-12)
        Xt = np.array(Xt)
        taus = origin.tau[: len(Xt) * stride: stride]
        mres = dict(tag=tag)
        if len(Xt) < 8:
            mres["oracle"] = "short"
            res["members"].append(mres); continue
        # refit initial Fermi data from the reconstruction itself (kills convention drift)
        k = max(1, len(Xt) // 200)
        Xa = Xt[0]
        hh = taus[2 * k] - taus[0]
        V0f = (-3 * Xt[0] + 4 * Xt[k] - Xt[2 * k]) / (2 * hh)
        mres["refit_X"] = float(np.linalg.norm(Xa - X0))
        mres["refit_V"] = float(np.linalg.norm(V0f - V0))
        # tau10: separation reaches 10x initial (extent death); the battle horizon
        sep = np.linalg.norm(Xt, axis=1)
        j10 = int(np.argmax(sep > 10 * sep[0])) if np.any(sep > 10 * sep[0]) else len(sep) - 1
        if j10 > 0:
            tau10 = float(np.interp(10 * sep[0], sep[j10 - 1: j10 + 1], taus[j10 - 1: j10 + 1]))
        else:
            tau10 = float(taus[j10])
        mres["tau10_over_T"] = tau10 / origin.tau_end
        # shear e-fold rate over the first half of the tau10 window (fit ln|X|)
        w0 = max(3, j10 // 2)
        mres["growth_rate_over_T"] = float(
            np.polyfit(taus[: w0 + 1], np.log(sep[: w0 + 1] + 1e-300), 1)[0] * origin.tau_end)
        # laws, compared only inside tau10 (frame validity)
        idxs = np.unique(np.linspace(0, j10, 60).astype(int))
        for law in laws:
            ev = law_run(origin, Xa, V0f, law)
            Xl = ev.sol(taus[idxs]).T[:, :2]
            cur = np.maximum(np.linalg.norm(Xt[idxs], axis=1), np.linalg.norm(Xa))
            err = np.linalg.norm(Xl - Xt[idxs], axis=1) / cur
            mres[law] = dict(err_end=float(err[-1]), err_max=float(err.max()),
                             err_010=float(err[len(err) // 3]))
        res["members"].append(mres)
    return res

def summary_table(results):
    hdr = (f"{'scene':18s} {'kerE':>6s} {'axdif':>6s} {'epT':>6s} {'epN':>6s} {'epE':>6s} | "
           f"{'member':16s} {'t10/T':>6s} " + " ".join(f"{l+' max/10%/end':>18s}" for l in ("L1", "L2", "L3")))
    print(hdr); print("-" * len(hdr))
    for r in results:
        eps, ker = r["epochs"], r["kernel"]
        for m in r["members"]:
            pre = (f"{r['name']:18s} {ker['max_rel']:6.3f} {ker['axis_diff_max']:6.3f} "
                   f"{eps['axis_true']:6.0f} {eps['axis_naive']:6.0f} {eps['tensor_true']:6.0f} | ")
            if m.get("oracle"):
                print(pre + f"{m['tag']:16s} {m['oracle']}"); continue
            cells = []
            for l in ("L1", "L2", "L3"):
                cells.append(f"{m[l]['err_max']:8.5f}/{m[l]['err_010']:5.4f}/{m[l]['err_end']:5.4f}")
            print(pre + f"{m['tag']:16s} {m['tau10_over_T']:6.3f} " + " ".join(cells))
        print(f"  [tau_end={r['tau_end']:.4g} T={r['T_orbit']:.4g} plunged={r['plunged']} "
              f"tetrad_dev={r['tetrad_dev']:.1e}]")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="all", help="comma list of scene names, or 'controls'")
    ap.add_argument("--out", default="probe-out.json")
    a = ap.parse_args()
    names = ({"circ-r1000", "ecc-rp6.5-L3.5"} if a.only == "controls"
             else {s["name"] for s in SCENES} if a.only == "all" else set(a.only.split(",")))
    results = [do_scene(s) for s in SCENES if s["name"] in names]
    summary_table(results)
    with open(a.out, "w") as fh:
        json.dump(results, fh, indent=1)
    print(f"wrote {a.out}")
