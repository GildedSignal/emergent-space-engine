#!/usr/bin/env python3
"""E-axis extension: the experiment the checker named for gold.

The original falsifier kicked only L (dE = 0 in every case). This script adds:
  (a) E kicks at matched fractional distance (dE/E = dL/L) with T_t in the
      error map; an E-axis scan err vs kick/(1-E) (distance to unbinding) at
      two weak-field depths (scale-free test); a strong-field E kick;
  (b) crossings on the E axis: plunge-via-E (separatrix tilt) and the
      escape-side crossing (E >= 1), with the completed tri-predicate
          bound   <=> E < 1  and 3 real roots and r[1] > 2M
          escape  <=> E >= 1 and 3 real roots
          plunge  otherwise
      checked against an independent grid truth (sign scan of
      f(r) = E^2 - (1-2/r)(1+L^2/r^2); no cubic solver), and against the
      author's original is_bound, whose escape-side failure is recorded.
Oracle: exact Schwarzschild quadrature `cycle()` copied verbatim from
falsifier.py (validated in validate_oracle.py). M = 1. RK4 validation and the
predicate's integrated-orbit ground truth live in validate_oracle.py (part c).
Bounds: one process, < 100 MB, < 60 s.
"""
import json
import numpy as np

N_NODES = 400
W = np.pi
CHEB = np.cos(np.pi * (np.arange(N_NODES) + 0.5) / N_NODES)


def roots_of(E, L):
    """Positive real roots of (E^2-1) r^3 + 2 r^2 - L^2 r + 2 L^2 = 0, ascending."""
    c = [E * E - 1.0, 2.0, -L * L, 2.0 * L * L]
    r = np.roots(c)
    ok = [x.real for x in r if abs(x.imag) < 1e-9 * max(1.0, abs(x.real))]
    return sorted(ok)


def is_bound_orig(E, L):
    """The original run's predicate (wrong on the escape side)."""
    r = roots_of(E, L)
    return len(r) == 3 and r[1] > 2.0 + 1e-12 and r[2] > r[1] * (1 + 1e-12)


def classify3(E, L):
    """Completed tri-predicate from the invariants alone (sign tests)."""
    r = roots_of(E, L)
    if len(r) == 3:
        if E < 1.0 and r[1] > 2.0:
            return "bound"
        if E >= 1.0:
            return "escape"
    return "plunge"


GRID = np.logspace(np.log10(2.0000001), 6.0, 120000)


def truth_grid(E, L):
    """Independent classification: sign changes of f(r) = E^2 - V^2 on a fine
    log grid. f -> E^2-1 at infinity, so: E<1 needs an odd number of changes
    (3 = has an outer turning point = bound iff the band pericentre is outside
    the horizon); E>=1 needs an even number (2 = barrier with an allowed outer
    region = escape; 0 = falls through = plunge)."""
    f = E * E - (1.0 - 2.0 / GRID) * (1.0 + L * L / GRID**2)
    s = np.signbit(f)
    idx = np.nonzero(s[:-1] != s[1:])[0]
    k = len(idx)
    roots = [float(np.sqrt(GRID[i] * GRID[i + 1])) for i in idx]  # geometric mid
    if E < 1.0:
        return ("bound" if (k == 3 and roots[1] > 2.0) else "plunge"), roots, k
    return ("escape" if k == 2 else "plunge"), roots, k


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


def lin_update(E, L, dE, dL):
    """The §3 multiply-add: cycle + derivatives * kick (verbatim from falsifier.py)."""
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
    """Extended case: truth class from the independent grid classifier, never
    from the predicate under test; multiply-add evaluated for every class."""
    c0 = cycle(E, L)
    if c0 is None:
        print(f"[{name}] seed (E={E:.6f}, L={L:.6f}) not bound; skipped")
        results.append(dict(case=name, skipped=True, E=E, L=L))
        return None
    truth, roots, k = truth_grid(E + dE, L + dL)
    lin = lin_update(E, L, dE, dL)
    row = dict(case=name, E=E, L=L, dE=dE, dL=dL, note=note,
               cycle0=dict(dphi=c0[0], T_t=c0[1], T_tau=c0[2]),
               truth_class=truth, truth_grid_changes=k,
               predicate_orig_bound=bool(is_bound_orig(E + dE, L + dL)),
               predicate3=classify3(E + dE, L + dL),
               lin=dict(dphi=lin[0], T_t=lin[1], T_tau=lin[2]),
               misclassified=None)
    if truth == "bound":
        ex = cycle(E + dE, L + dL)
        row["truth_cycle"] = dict(dphi=ex[0], T_t=ex[1], T_tau=ex[2])
        row["relerr"] = dict(dphi=abs(lin[0] - ex[0]) / ex[0],
                             T_t=abs(lin[1] - ex[1]) / ex[1],
                             T_tau=abs(lin[2] - ex[2]) / ex[2])
        print(f"[{name}] E={E:.6f} dE/E={dE/E:.1e} relerr dphi={row['relerr']['dphi']:.3e} "
              f"T_t={row['relerr']['T_t']:.3e} T_tau={row['relerr']['T_tau']:.3e}")
    else:
        # the multiply-add fabricated a finite cycle for a non-bound truth
        row["misclassified"] = dict(kind=f"fabricated cycle for {truth}",
                                    fab_dphi=lin[0], fab_T_t=lin[1],
                                    predicate3_correct=row["predicate3"] == truth,
                                    predicate_orig_correct=row["predicate_orig_bound"] == (truth == "bound"))
        print(f"[{name}] E={E:.6f} truth: {truth.upper()}; multiply-add fabricated "
              f"dphi={lin[0]:.4f} T_t={lin[1]:.2f}; predicate3={row['predicate3']} "
              f"({'OK' if row['predicate3'] == truth else 'WRONG'}), "
              f"orig is_bound={row['predicate_orig_bound']} "
              f"({'OK' if row['misclassified']['predicate_orig_correct'] else 'WRONG'})")
    results.append(row)
    return row


# ---- E1/E2: E kicks at matched fractional distance (dE/E = 1e-4 = dL/L) ----
E1, L1 = from_band(50.0, 200.0)         # the original P1 seed (weak field)
r1 = case("E1-weak-p80-dEkick", E1, L1, 1e-4 * E1, 0.0)
E2, L2 = from_band(7.5, 30.0)           # the original P2 seed (strong field)
r2 = case("E2-strong-p12-dEkick", E2, L2, 1e-4 * E2, 0.0)
stiffness = dict(
    note="axis stiffness at matched fractional kick 1e-4, weak field: "
         "err_E(T_t)/err_L(T_t)",
    err_L_T_t=9.696047073311268e-12,   # original P1, dL/L=1e-4 (reproduced above)
    err_E_T_t=r1["relerr"]["T_t"] if r1 and "relerr" in r1 else None)
stiffness["ratio"] = stiffness["err_E_T_t"] / stiffness["err_L_T_t"]
print(f"\naxis stiffness (weak field, matched fractional kick): "
      f"{stiffness['ratio']:.2e}")

# ---- E3: scan err vs kick/(1-E), weak field far from the separatrix --------
FS = (3e-3, 1e-2, 3e-2, 1e-1, 3e-1)
scan1 = []
for f in FS:
    dE = f * (1.0 - E1)
    r = case(f"E3-weak-scan-f{f:.0e}", E1, L1, dE, 0.0)
    scan1.append(dict(f=f, dE=dE, err_dphi=r["relerr"]["dphi"], err_T_t=r["relerr"]["T_t"],
                      err_T_tau=r["relerr"]["T_tau"]))
lf = np.log([s["f"] for s in scan1])
slope_T = np.polyfit(lf, np.log([s["err_T_t"] for s in scan1]), 1)[0]
slope_phi = np.polyfit(lf, np.log([s["err_dphi"] for s in scan1]), 1)[0]
print(f"E3 weak-field E-scan: slope(T_t)={slope_T:.3f} slope(dphi)={slope_phi:.3f}")

# ---- E4: scale-free test at half the distance to unbinding -----------------
E4, L4 = from_band(100.0, 400.0)        # 1-E is ~2x smaller, same physics regime
scan2 = []
for f in FS:
    dE = f * (1.0 - E4)
    r = case(f"E4-weak2-scan-f{f:.0e}", E4, L4, dE, 0.0)
    scan2.append(dict(f=f, dE=dE, err_dphi=r["relerr"]["dphi"], err_T_t=r["relerr"]["T_t"],
                      err_T_tau=r["relerr"]["T_tau"]))
ratios = [s2["err_T_t"] / s1["err_T_t"] for s1, s2 in zip(scan1, scan2)]
print(f"E4 scale-free: 1-E = {1-E1:.5f} vs {1-E4:.5f}; err2/err1 (T_t) = "
      f"{['%.2f' % x for x in ratios]}")

# ---- E5: plunge via E kick (the separatrix tilts: dL_sep/dE ~ 18) ----------
Ls97 = L_sep_of(0.97)
E5 = case("E5-plunge-via-E", 0.97, Ls97 * (1 + 1e-3), 1e-3, 0.0,
          note="E kick crosses the plunge separatrix at fixed L (tilt)")

# ---- E6: the escape side of the bound region -------------------------------
E6a = case("E6a-escape-unbind", E1, L1, 1.02 - E1, 0.0,
           note="weak-field orbit kicked past E=1 with L >> L_crit: escape")
Ls999 = L_sep_of(0.999)
E6b = case("E6b-E1.005-lowL", 0.999, Ls999 * (1 + 1e-3), 1.005 - 0.999, 0.0,
           note="kicked past E=1 but L < L_crit(1.005): falls in (plunge), not escape")
E6c = case("E6c-escape-thin", 0.999, 4.2, 1.005 - 0.999, 0.0,
           note="kicked past E=1 with L > L_crit: escape just above the barrier")

with open("falsifier2-out.json", "w") as f:
    json.dump(dict(cases=results, stiffness=stiffness,
                   scan_weak=dict(seed_E=E1, seed_L=L1, one_minus_E=1 - E1, rows=scan1,
                                  slope_T_t=float(slope_T), slope_dphi=float(slope_phi)),
                   scan_weak2=dict(seed_E=E4, seed_L=L4, one_minus_E=1 - E4, rows=scan2,
                                   err2_over_err1_T_t=ratios)), f, indent=1)
print("\nwrote falsifier2-out.json")
