#!/usr/bin/env python3
"""Ships what the original run only claimed, and grounds the tri-predicate.

(1) The dossier's "an independent RK4 integration of the Binet ODE agrees to
    2e-4 at p~80" was not regenerable from shipped code. Here it is: hand-rolled
    RK4 on the Binet system u'' = 1/L^2 + 3u^2 - u, t' = E/(L u^2 (1-2u)),
    pericentre to pericentre, two step sizes + Richardson.
(2) Proper-time DOP853 integration of the geodesics (scipy) peri->apo->peri
    for three bound seeds (weak, strong, near-separatrix): dphi and T_t vs the
    Chebyshev quadrature `cycle()` copied verbatim from falsifier.py.
(3) The completed tri-predicate (bound / plunge / escape) vs an independent
    grid truth (sign scan of f(r) = E^2 - V^2; no cubic solver) over ~3.7k
    (E, L) samples, margin orbits excluded and counted.
(4) Eleven orbits integrated in proper time with terminal events (r = 2.05
    down = plunge; r = 1e4 up = escape; pr = 0 = turning point): the physical
    ground truth of each class, including the E5 kicked invariants.
M = 1. Bounds: one process, < 100 MB, < 60 s.
"""
import json
import numpy as np
from scipy.integrate import solve_ivp

N_NODES = 400
W = np.pi
CHEB = np.cos(np.pi * (np.arange(N_NODES) + 0.5) / N_NODES)


def roots_of(E, L):
    c = [E * E - 1.0, 2.0, -L * L, 2.0 * L * L]
    r = np.roots(c)
    ok = [x.real for x in r if abs(x.imag) < 1e-9 * max(1.0, abs(x.real))]
    return sorted(ok)


def is_bound_orig(E, L):
    r = roots_of(E, L)
    return len(r) == 3 and r[1] > 2.0 + 1e-12 and r[2] > r[1] * (1 + 1e-12)


def classify3(E, L):
    r = roots_of(E, L)
    if len(r) == 3:
        if E < 1.0 and r[1] > 2.0:
            return "bound"
        if E >= 1.0:
            return "escape"
    return "plunge"


def cycle(E, L):
    r = roots_of(E, L)
    if len(r) != 3:
        return None
    a, b = r[1], r[2]
    c3 = r[0]
    m, d = 0.5 * (a + b), 0.5 * (b - a)
    rr = m + d * CHEB
    q = -(E * E - 1.0) * (rr - c3) / rr**3
    if np.any(q <= 0):
        return None
    sq = np.sqrt(q)
    dphi = 2.0 * L * W * np.mean(1.0 / (rr * rr * sq))
    T_t = 2.0 * E * W * np.mean(1.0 / ((1.0 - 2.0 / rr) * sq))
    T_tau = 2.0 * W * np.mean(1.0 / sq)
    return dphi, T_t, T_tau


def from_band(a, b):
    L2 = ((1 - 2 / b) - (1 - 2 / a)) / ((1 - 2 / a) / a**2 - (1 - 2 / b) / b**2)
    L = np.sqrt(L2)
    E = np.sqrt((1 - 2 / a) * (1 + L2 / a**2))
    return E, L


def L_sep_of(E):
    grid = np.linspace(2 * np.sqrt(3.0) + 1e-4, 3000.0, 12000)
    flags = [is_bound_orig(E, L) for L in grid]
    if not any(flags):
        return None
    i0 = flags.index(True)
    if i0 == 0:
        return grid[0]
    lo, hi = grid[i0 - 1], grid[i0]
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if is_bound_orig(E, mid):
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


GRID = np.logspace(np.log10(2.0000001), 6.0, 120000)


def truth_grid(E, L):
    f = E * E - (1.0 - 2.0 / GRID) * (1.0 + L * L / GRID**2)
    s = np.signbit(f)
    idx = np.nonzero(s[:-1] != s[1:])[0]
    roots = [float(np.sqrt(GRID[i] * GRID[i + 1])) for i in idx]
    k = len(roots)
    if E < 1.0:
        return ("bound" if (k == 3 and roots[1] > 2.0) else "plunge"), roots
    return ("escape" if k == 2 else "plunge"), roots


out = {}

# ---- (1) RK4 Binet at p ~ 80 -------------------------------------------------
E, L = from_band(50.0, 200.0)
a_pt, b_pt = 50.0, 200.0
u0, w0, t0 = 1.0 / a_pt, 0.0, 0.0


def binet_rk4(n_steps):
    h = None
    # estimate total angle span first: ~ 2 pi (Kepler) + advance; use 8 rad cap
    phi_max = 8.0
    h = phi_max / n_steps
    u, w, t, phi = u0, w0, t0, 0.0

    def deriv(u, w):
        return w, 1.0 / (L * L) + 3.0 * u * u - u

    def dtdp(u):
        return E / (L * u * u * (1.0 - 2.0 * u))

    while phi < phi_max:
        w_old = w
        k1u, k1w = deriv(u, w)
        k1t = dtdp(u)
        k2u, k2w = deriv(u + 0.5 * h * k1u, w + 0.5 * h * k1w)
        k2t = dtdp(u + 0.5 * h * k1u)
        k3u, k3w = deriv(u + 0.5 * h * k2u, w + 0.5 * h * k2w)
        k3t = dtdp(u + 0.5 * h * k2u)
        k4u, k4w = deriv(u + h * k3u, w + h * k3w)
        k4t = dtdp(u + h * k3u)
        u += h * (k1u + 2 * k2u + 2 * k3u + k4u) / 6.0
        w += h * (k1w + 2 * k2w + 2 * k3w + k4w) / 6.0
        t += h * (k1t + 2 * k2t + 2 * k3t + k4t) / 6.0
        phi_prev, phi = phi, phi + h
        # next pericentre: after the apocentre (u minimum) w crosses 0 falling
        if phi > 4.0 and w_old > 0.0 >= w:
            frac = w_old / (w_old - w)
            dphi = phi_prev + frac * h
            T_t = t + frac * h * dtdp(u)
            return dphi, T_t
    raise RuntimeError("no pericentre return within span")


r20 = binet_rk4(200_000)
r40 = binet_rk4(400_000)
rich = [(r20[i] - r40[i]) for i in range(2)]
quad = cycle(E, L)
relerr = lambda x, y: abs(x - y) / abs(y)
binet = dict(seed="from_band(50,200), p~80, e~0.6", E=E, L=L,
             quad=dict(dphi=quad[0], T_t=quad[1]),
             rk4_200k=dict(dphi=r20[0], T_t=r20[1]),
             rk4_400k=dict(dphi=r40[0], T_t=r40[1]),
             relerr_400k=dict(dphi=relerr(r40[0], quad[0]), T_t=relerr(r40[1], quad[1])),
             richardson_step=dict(dphi=rich[0], T_t=rich[1]))
out["binet_rk4"] = binet
print(f"(1) RK4-Binet p~80: quad dphi={quad[0]:.9f} T_t={quad[1]:.6f}")
print(f"    rk4@400k        dphi={r40[0]:.9f} T_t={r40[1]:.6f}")
print(f"    relerr dphi={binet['relerr_400k']['dphi']:.2e} "
      f"T_t={binet['relerr_400k']['T_t']:.2e}; richardson {rich[0]:.2e} {rich[1]:.2e}")

# ---- (2) DOP853 proper time, peri->apo->peri --------------------------------


def geodesic_period(E, L):
    r = roots_of(E, L)
    a, b = r[1], r[2]

    def rhs(tau, y):
        rr, pr = y[0], y[1]
        ar = -(1.0 / rr**2) * (1.0 + L * L / rr**2) + (1.0 - 2.0 / rr) * L * L / rr**3
        return [pr, ar, L / rr**2, E / (1.0 - 2.0 / rr)]

    def ev_peri(tau, y):  # pr rising through 0 (after falling from apo)
        return y[1]
    def ev_apo(tau, y):
        return y[1]
    ev_peri.terminal = True
    ev_peri.direction = 1.0
    ev_apo.terminal = True
    ev_apo.direction = -1.0
    # apo -> peri
    s1 = solve_ivp(rhs, (0.0, 1e9), [b, 0.0, 0.0, 0.0], rtol=1e-12, atol=1e-13,
                   events=ev_peri, dense_output=False)
    # peri -> apo
    s2 = solve_ivp(rhs, (0.0, 1e9), [a, 0.0, s1.y[2, -1], s1.y[3, -1]], rtol=1e-12,
                   atol=1e-13, events=ev_apo)
    return (s2.y[2, -1], s2.y[3, -1], s1.status, s2.status)


Ls97 = L_sep_of(0.97)
seeds = {"weak-p80": from_band(50.0, 200.0), "strong-p12": from_band(7.5, 30.0),
         "nearsep-E0.97": (0.97, Ls97 * (1 + 1e-3))}
dop = {}
for nm, (E, L) in seeds.items():
    q = cycle(E, L)
    dphi, T_t, st1, st2 = geodesic_period(E, L)
    dop[nm] = dict(E=E, L=L, quad=dict(dphi=q[0], T_t=q[1]), integ=dict(dphi=dphi, T_t=T_t),
                   relerr=dict(dphi=relerr(dphi, q[0]), T_t=relerr(T_t, q[1])),
                   events_fired=bool(st1 == 1 and st2 == 1))
    print(f"(2) {nm}: dphi relerr={dop[nm]['relerr']['dphi']:.2e} "
          f"T_t relerr={dop[nm]['relerr']['T_t']:.2e} events={dop[nm]['events_fired']}")
out["dop853_period"] = dop

# ---- (3) predicate vs independent grid truth --------------------------------
Es = np.linspace(0.93, 1.05, 61)
Ls = np.concatenate([np.linspace(3.35, 4.5, 40), np.linspace(4.5, 30.0, 20)])
n = nex = nagree = 0
dis = []
for E in Es:
    for L in Ls:
        n += 1
        truth, roots = truth_grid(E, L)
        # margin: near-double roots, unresolvable unbinding, horizon-touching band
        gap = min((roots[i + 1] / roots[i] - 1.0) for i in range(len(roots) - 1)) \
            if len(roots) > 1 else 0.0
        if abs(1.0 - E) < 5e-6 or (gap > 0 and gap < 1e-4) or \
           (len(roots) >= 2 and abs(roots[1] - 2.0) < 1e-4):
            nex += 1
            continue
        pred = classify3(E, L)
        if pred == truth:
            nagree += 1
        else:
            dis.append(dict(E=E, L=L, truth=truth, pred=pred, roots=roots))
sweep = dict(n=n, n_margin_excluded=nex, n_compared=n - nex, n_agree=nagree,
             n_disagree=len(dis), disagreements=dis[:20])
out["predicate_sweep"] = sweep
print(f"(3) predicate vs grid truth: {nagree}/{n - nex} agree "
      f"({nex} margin-excluded of {n}); disagreements={len(dis)}")

# ---- (4) integrated orbits: the physical ground truth -----------------------


def integrate_orbit(E, L, r0, pr0):
    def rhs(tau, y):
        rr, pr = y[0], y[1]
        ar = -(1.0 / rr**2) * (1.0 + L * L / rr**2) + (1.0 - 2.0 / rr) * L * L / rr**3
        return [pr, ar, L / rr**2, E / (1.0 - 2.0 / rr)]

    def ev_plunge(tau, y):
        return y[0] - 2.05
    def ev_escape(tau, y):
        return y[0] - 1e4
    def ev_turn(tau, y):
        return y[1]
    for ev in (ev_plunge, ev_escape, ev_turn):
        ev.terminal = True
    ev_plunge.direction = -1.0
    ev_escape.direction = 1.0
    ev_turn.direction = -1.0 * np.sign(pr0) if pr0 != 0 else 0.0
    s = solve_ivp(rhs, (0.0, 1e7), [r0, pr0, 0.0, 0.0], rtol=1e-10, atol=1e-12,
                  events=[ev_plunge, ev_escape, ev_turn], dense_output=False)
    fired = [nm for nm, te in zip(("plunge(r<2.05)", "escape(r>1e4)", "turn(pr=0)"),
                                  s.t_events) if len(te) > 0]
    return fired, float(s.y[0, -1]), float(s.t[-1])


def fval(E, L, r):
    return E * E - (1.0 - 2.0 / r) * (1.0 + L * L / r**2)


orbits = []
cases4 = [
    ("bound-weak", 50.0, 200.0, "bound"),
    ("bound-strong", 7.5, 30.0, "bound"),
    ("bound-thin-0.999L4.2", None, None, "bound"),
    ("escape-E1.02-weakL", None, None, "escape"),
    ("escape-E1.005-L4.2", 1.005, 4.2, "escape"),
    ("escape-E1.5-L10", 1.5, 10.0, "escape"),
    ("escape-E1.0001-L6", 1.0001, 6.0, "escape"),
    ("plunge-E0.97-belowsep", None, None, "plunge"),
    ("plunge-E1.005-lowL", 1.005, 3.9960, "plunge"),
    ("plunge-E1.5-lowL", 1.5, 3.9, "plunge"),
    ("plunge-E5-kicked", None, None, "plunge"),
]
for nm, x, y, expect in cases4:
    if nm == "bound-thin-0.999L4.2":
        E, L = 0.999, 4.2
        r = roots_of(E, L); r0, pr0 = 0.5 * (r[1] + r[2]), np.sqrt(fval(E, L, 0.5 * (r[1] + r[2])))
    elif nm == "bound-weak" or nm == "bound-strong":
        E, L = from_band(x, y)
        r = roots_of(E, L); r0, pr0 = 0.5 * (r[1] + r[2]), np.sqrt(fval(E, L, 0.5 * (r[1] + r[2])))
    elif nm == "escape-E1.02-weakL":
        E, L = 1.02, from_band(50.0, 200.0)[1]
        r = roots_of(E, L); r0, pr0 = r[2] * 1.001, np.sqrt(fval(E, L, r[2] * 1.001))
    elif nm == "plunge-E0.97-belowsep":
        E, L = 0.97, L_sep_of(0.97) * 0.999
        r = roots_of(E, L); r0, pr0 = 0.9 * r[0], -np.sqrt(fval(E, L, 0.9 * r[0]))
    elif nm == "plunge-E5-kicked":
        E, L = 0.97 + 1e-3, L_sep_of(0.97) * (1 + 1e-3)
        r = roots_of(E, L); r0, pr0 = 0.9 * r[0], -np.sqrt(fval(E, L, 0.9 * r[0]))
    else:
        E, L = x, y
        r = roots_of(E, L)
        if expect == "escape":
            r0, pr0 = r[2] * 1.001, np.sqrt(fval(E, L, r[2] * 1.001))
        else:
            if len(r) >= 1 and r[0] > 2.1:
                r0, pr0 = 0.9 * r[0], -np.sqrt(fval(E, L, 0.9 * r[0]))
            else:
                r0, pr0 = 20.0, -np.sqrt(fval(E, L, 20.0))
    assert fval(E, L, r0) > 0, (nm, r0)
    fired, r_end, tau_end = integrate_orbit(E, L, r0, pr0)
    pred = classify3(E, L)
    obs = ("plunge" if fired and fired[0].startswith("plunge") else
           "escape" if fired and fired[0].startswith("escape") else
           "bound" if fired and fired[0].startswith("turn") else "none")
    orbits.append(dict(name=nm, E=E, L=L, start_r=r0, events=fired, r_end=r_end,
                       tau_end=tau_end, predicate3=pred, observed=obs,
                       expect=expect, ok=(pred == obs == expect)))
    print(f"(4) {nm}: predicate3={pred:7s} integrated={obs:7s} "
          f"events={fired} r_end={r_end:.4g} ok={orbits[-1]['ok']}")
out["integrated_orbits"] = orbits
out["integrated_orbits_ok"] = sum(o["ok"] for o in orbits)

with open("validate-out.json", "w") as f:
    json.dump(out, f, indent=1)
print("\nwrote validate-out.json")
