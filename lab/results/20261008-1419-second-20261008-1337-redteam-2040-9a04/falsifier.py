#!/usr/bin/env python3
"""Falsifier for representation.md §3: 'a kick updates the cycle by a multiply-add.'

Oracle: exact Schwarzschild timelike geodesics (M=1). Per radial cycle the design stores
constants (Δφ, Δt, Δτ); a kick changes (E, L) and the claim is that first-order response
reproduces the recompiled cycle. We compute the cycle by exact quadrature (Chebyshev over
the turning-point band, the same integral family as `bound_period_quad`, H0183), take the
derivatives of the *exact* map by central differences (the ideal version of the stored
derivatives), and compare the linear update against recompilation after the kick.

Bounds: one process, < 100 MB, < 60 s.
"""
import json
import numpy as np

N_NODES = 400
W = np.pi  # \int_0^\pi g dtheta = pi * mean(g); validated against an independent RK4 Binet integration (2e-4 agreement) and the 1PN series
CHEB = np.cos(np.pi * (np.arange(N_NODES) + 0.5) / N_NODES)


def roots_of(E, L):
    """Positive real roots of (E^2-1) r^3 + 2 r^2 - L^2 r + 2 L^2 = 0, ascending."""
    c = [E * E - 1.0, 2.0, -L * L, 2.0 * L * L]
    r = np.roots(c)
    ok = [x.real for x in r if abs(x.imag) < 1e-9 * max(1.0, abs(x.real))]
    return sorted(ok)


def is_bound(E, L):
    r = roots_of(E, L)
    return len(r) == 3 and r[1] > 2.0 + 1e-12 and r[2] > r[1] * (1 + 1e-12)


def cycle(E, L):
    """(dphi, T_t, T_tau) per radial cycle for a bound orbit. None if not bound."""
    r = roots_of(E, L)
    if len(r) != 3:
        return None
    a, b = r[1], r[2]           # pericentre, apocentre (allowed band)
    c3 = r[0]                   # plunge-side root
    m, d = 0.5 * (a + b), 0.5 * (b - a)
    rr = m + d * CHEB
    q = -(E * E - 1.0) * (rr - c3) / rr**3   # E^2 - V = q*(r-a)(b-r), q>0 on (a,b)
    if np.any(q <= 0):
        return None
    sq = np.sqrt(q)
    dphi = 2.0 * L * W * np.mean(1.0 / (rr * rr * sq))
    T_t = 2.0 * E * W * np.mean(1.0 / ((1.0 - 2.0 / rr) * sq))
    T_tau = 2.0 * W * np.mean(1.0 / sq)
    return dphi, T_t, T_tau


def from_band(a, b):
    """(E, L) of the exact orbit with turning points at a (peri) and b (apo)."""
    L2 = ((1 - 2 / b) - (1 - 2 / a)) / ((1 - 2 / a) / a**2 - (1 - 2 / b) / b**2)
    L = np.sqrt(L2)
    E = np.sqrt((1 - 2 / a) * (1 + L2 / a**2))
    return E, L


def L_sep_of(E):
    """Plunge-side separatrix angular momentum at fixed E.

    At fixed E the bound region in L is an interval (plunge edge below, circular
    edge above); we bracket it on a coarse grid and bisect the lower edge.
    """
    grid = np.linspace(2 * np.sqrt(3.0) + 1e-4, 3000.0, 12000)
    flags = [is_bound(E, L) for L in grid]
    if not any(flags):
        return None
    i0 = flags.index(True)
    if i0 == 0:
        return grid[0]
    lo, hi = grid[i0 - 1], grid[i0]
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if is_bound(E, mid):
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def lin_update(E, L, dE, dL):
    """The §3 multiply-add: cycle + derivatives * kick, derivatives of the exact map.

    The difference step shrinks adaptively so both samples stay inside the bound
    region (a fixed step can straddle the separatrix, which is the point).
    """
    c0 = cycle(E, L)
    out = list(c0)
    if dE != 0:
        for h in (1e-6, 3e-7, 1e-7, 3e-8, 1e-8):
            cp, cm = cycle(E + h, L), cycle(E - h, L)
            if cp and cm:
                out = [out[k] + (cp[k] - cm[k]) / (2 * h) * dE for k in range(3)]
                break
        else:
            raise RuntimeError("no E-step stays bound")
    if dL != 0:
        for h in (1e-6, 3e-7, 1e-7, 3e-8, 1e-8):
            dp, dm = cycle(E, L + h), cycle(E, L - h)
            if dp and dm:
                out = [out[k] + (dp[k] - dm[k]) / (2 * h) * dL for k in range(3)]
                break
        else:
            raise RuntimeError("no L-step stays bound")
    return out


results = []


def case(name, E, L, dE, dL, note=""):
    c0 = cycle(E, L)
    if c0 is None:
        print(f"[{name}] seed (E={E:.6f}, L={L:.6f}) is not bound; skipped")
        results.append(dict(case=name, skipped=True, E=E, L=L))
        return None
    lin = lin_update(E, L, dE, dL)
    kicked_bound = is_bound(E + dE, L + dL)
    Ls = L_sep_of(E)
    band = roots_of(E, L)
    row = dict(case=name, E=E, L=L, L_sep=Ls, delta_L_over_Lsep=(L - Ls) / Ls,
               pericentre=band[1], apocentre=band[2],
               dE=dE, dL=dL, dL_over_L=dL / L, note=note,
               cycle0=dict(dphi=c0[0], T_t=c0[1], T_tau=c0[2]),
               kicked_bound=bool(kicked_bound))
    if kicked_bound:
        ex = cycle(E + dE, L + dL)
        row["truth"] = dict(dphi=ex[0], T_t=ex[1], T_tau=ex[2])
        row["lin"] = dict(dphi=lin[0], T_t=lin[1], T_tau=lin[2])
        row["relerr"] = dict(dphi=abs(lin[0] - ex[0]) / ex[0],
                             T_t=abs(lin[1] - ex[1]) / ex[1],
                             T_tau=abs(lin[2] - ex[2]) / ex[2])
        print(f"[{name}] peri={band[1]:.3f} apo={band[2]:.3f} dL/Lsep={row['delta_L_over_Lsep']:.2e} "
              f"relerr dphi={row['relerr']['dphi']:.3e} T_t={row['relerr']['T_t']:.3e}")
    else:
        row["truth"] = "PLUNGE"
        row["lin"] = dict(dphi=lin[0], T_t=lin[1], T_tau=lin[2])
        row["relerr"] = "n/a: truth plunges, linear update returns a finite cycle"
        print(f"[{name}] peri={band[1]:.3f} apo={band[2]:.3f} dL/Lsep={row['delta_L_over_Lsep']:.2e} "
              f"truth: PLUNGE; linear update returned finite cycle "
              f"(dphi={lin[0]:.4f}, T_t={lin[1]:.4f}) -> MISCLASSIFIED")
    results.append(row)
    return row


# ---- P1 / P2: ordinary kicks far from the separatrix -------------------------
E, L = from_band(50.0, 200.0)          # p ~ 80, e ~ 0.6 (weak field)
case("P1-weak-p80", E, L, 0.0, 1e-4 * L)
E, L = from_band(7.5, 30.0)            # p = 12, e = 0.6 (strong field)
case("P2-strong-p12", E, L, 0.0, 1e-4 * L)

# ---- P3 / P5: near the separatrix, matched delta_L/L_sep --------------------
for name, E0 in (("P3-nearsep-strong-E0.97", 0.97), ("P5-nearsep-weak-E0.999", 0.999)):
    Ls = L_sep_of(E0)
    L0 = Ls * (1 + 1e-3)
    case(name, E0, L0, 0.0, 1e-4 * L0)

# ---- P4: kick crosses the separatrix ----------------------------------------
Ls97 = L_sep_of(0.97)
L0 = Ls97 * (1 + 1e-3)
case("P4-crossing-plunge", 0.97, L0, 0.0, -2e-3 * Ls97)

# ---- scan: error vs distance to separatrix at fixed kick --------------------
scan = []
for fac in (3e-2, 1e-2, 3e-3, 1e-3, 3e-4):
    L0 = Ls97 * (1 + fac)
    dL = 1e-4 * L0
    r = case(f"scan-d{fac:.0e}", 0.97, L0, 0.0, dL)
    if r is not None and isinstance(r.get("relerr"), dict):
        scan.append(dict(delta=fac, kick_over_delta=dL / (fac * Ls97),
                         err_dphi=r["relerr"]["dphi"], err_T_t=r["relerr"]["T_t"]))
print("\nscan (kick 1e-4 L, E=0.97): delta_L/L_sep, kick/delta -> relerr")
for s in scan:
    print(f"  {s['delta']:.1e} {s['kick_over_delta']:.1e} -> "
          f"dphi {s['err_dphi']:.3e}  T_t {s['err_T_t']:.3e}")

# ---- inspiral walk: many small kicks with the multiply-add only -------------
# Secular shrink dL = -1e-6 L per step (E fixed). Each step compares the
# multiply-add cycle against recompilation; records when the 1% band breaks
# and when the truth crosses the separatrix.
E_w, L_w = 0.97, Ls97 * (1 + 3e-2)
kick = -1e-6 * L_w
walk = dict(E=E_w, kick_per_step=kick, first_pct_break=None, crossing_step=None,
            total_steps=None, delta_at_break=None, samples=[])
step = 0
while step < 200000:
    nxt = cycle(E_w, L_w + kick)
    if nxt is None:
        walk["crossing_step"] = step + 1
        walk["note"] = ("next kick crosses the separatrix; the multiply-add would "
                        "still return a finite cycle")
        break
    lin = lin_update(E_w, L_w, 0.0, kick)
    err = abs(lin[0] - nxt[0]) / nxt[0]
    if walk["first_pct_break"] is None and err > 1e-2:
        walk["first_pct_break"] = step
        walk["delta_at_break"] = (L_w - Ls97) / Ls97
    if step % 200 == 0 or err > 1e-2:
        walk["samples"].append(dict(step=step, delta=(L_w - Ls97) / Ls97,
                                    err_dphi=err, dphi_true=nxt[0]))
    L_w += kick
    step += 1
walk["total_steps"] = step
print(f"\ninspiral (kick {kick:.3e}/step): 1% band breaks at step "
      f"{walk['first_pct_break']} (delta_L/L_sep={walk['delta_at_break']}); "
      f"separatrix crossing at step {walk['crossing_step']}")

with open("falsifier-out.json", "w") as f:
    json.dump(dict(cases=results, scan=scan, inspiral=walk), f, indent=1)
print("\nwrote falsifier-out.json")
