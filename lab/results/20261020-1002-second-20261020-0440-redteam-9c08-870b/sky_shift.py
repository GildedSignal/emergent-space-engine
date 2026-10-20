#!/usr/bin/env python3
"""r13-sky-shift: the sky-cell aggregate under the observer's own gamma, on the game's 2D sky.

Run 9c08 measured the geometric law (one shift per sky cell errs k^4 brightness by E(gamma*theta_f)
alone) but modelled the view record's aggregate from the wiki's field list. The cell struct on the
record's own branch (959a, struct CellSums) stores `lum += row.luminosity` with
`row.luminosity = lum * shift^4` -- the exact seen-flux sum, member by member. So the rung's two
representations are:

  exact-sum  (candidate, = the shipped record's field list + the letter L58 type-x-log-k table):
             brightness served from the per-cell running sum sum(lum_i k_i^4) (exact); colour-k
             served from a per-cell equal-ln-k histogram with B bins over the cell's [k_min,k_max]
             (the letter's own table; B frozen in the rung after a pilot).
  one-shift  (negative, = the letter L59 "aggregates are one sample each"): one lum-weighted shift
             per cell, kbar = sum(lum k)/sum(lum) (equal rest luminosity: the plain mean); the
             cell's brightness and colour both rebuilt from kbar.
  flat-gamma (positive, instrument control): the exact-sum readout at gamma 1.0001 and 1.33, where
             9c08 measured the channel to read zero; it must read zero here too, else VOID.

Geometry: the game's sky is a CIRCLE (the record's 786 cells = 2*pi/theta_f, direction served as
[cos,sin] -- 959a serve code), members uniform in the sky angle; the 3D isotropic sky is kept as
the comparison arm (9c08's idealisation). Exact SR throughout: k = gamma(1 + beta cos phi_s),
cos phi' = (cos phi_s + beta)/(1 + beta cos phi_s), sin phi' = sin phi_s / k (2D);
k = gamma(1 + beta u), u = cos theta_s (3D). This k is the record's own row formula
(shift = (1 - n.v_o)/rate_o over (1 - n.v)/rate) evaluated on a cold sky: identical algebra.

Readouts judged per multi-member cell (n >= 2; singleton cells serve the member's exact row in the
record, so they are outside the aggregate's domain). Truth for a cell = that cell's member set:
brightness sum(lum k^4), colour <ln k>_flux = sum(k^4 ln k)/sum(k^4).

  env: SKY_SEED (default 20261020), METRICS_OUT (default metrics.json), NS (default 2_000_000)
"""
import json
import os
import platform

import numpy as np

RUN = os.path.dirname(os.path.abspath(__file__))

# ---- the frozen case set (rung r13-sky-shift.md) -------------------------------------------
#   cases:  gamma*theta_f in {1, 4, 8000} x {2D, 3D} x {stock 8e-3, fine 1e-3}
#   controls: gamma in {1.0001, 1.33} x {2D, 3D} x stock
FLOORS = {"stock": 8e-3, "fine": 1e-3}
CASES = []  # (gamma, floor_name, sky, is_control)
for gf in (1.0, 4.0, 8000.0):
    for fn, tf in FLOORS.items():
        for sky in ("2D", "3D"):
            CASES.append((gf / tf, fn, sky, False))
for g in (1.0001, 1.33):
    for sky in ("2D", "3D"):
        CASES.append((g, "stock", sky, True))

BINS = 128          # frozen after pilot: equal-ln-k bins per cell (see evidence pilot table)
HIST_PILOT = [16, 32, 64, 128, 256]   # reported, not gated


def wquantile(v, q, w):
    order = np.argsort(v)
    cw = np.cumsum(w[order])
    cw = cw / cw[-1]
    return v[order][np.searchsorted(cw, q)]


def sample_cells(gamma, theta_f, sky, ns, seed):
    """exact-SR sky sampling; returns per-member (cell index, k)."""
    beta = float(np.sqrt(1.0 - 1.0 / gamma**2))
    rng = np.random.default_rng(seed)
    if sky == "2D":
        phi = rng.uniform(0.0, 2.0 * np.pi, ns)          # members uniform in the sky angle
        c, s = np.cos(phi), np.sin(phi)
        k = gamma * (1.0 + beta * c)
        # aberration: cos phi' = (c+beta)/(1+beta c), sin phi' = s/(gamma(1+beta c)) = s/k
        pp = np.arctan2(s / k, (c + beta) / (1.0 + beta * c))  # (-pi, pi]
        pp = np.mod(pp, 2.0 * np.pi)
        ncell = int(np.ceil(2.0 * np.pi / theta_f))
        cell = np.minimum((pp / theta_f).astype(np.int64), ncell - 1)
    else:
        u = rng.uniform(-1.0, 1.0, ns)                   # members isotropic (uniform in cos theta)
        k = gamma * (1.0 + beta * u)
        ctp = (u + beta) / (1.0 + beta * u)
        tp = np.arccos(np.clip(ctp, -1.0, 1.0))
        ncell = int(np.ceil(np.pi / theta_f))
        cell = np.minimum((tp / theta_f).astype(np.int64), ncell - 1)
    return cell, k


def cell_readouts(cell, k, bins_list):
    """per multi-member cell: the truth and each readout's errors (dict per n>=2 cell)."""
    order = np.argsort(cell, kind="stable")
    cs, ks = cell[order], k[order]
    starts = np.flatnonzero(np.r_[True, cs[1:] != cs[:-1]])
    counts = np.diff(np.r_[starts, cs.size])
    out = []
    for st, cnt in zip(starts, counts):
        if cnt < 2:
            continue
        kk = ks[st:st + cnt]
        n = kk.size
        k4 = kk**4
        S4 = k4.sum()
        L4 = float((k4 * np.log(kk)).sum() / S4)          # exact flux-weighted mean ln k
        lnk = np.log(kk)
        row = {"n": int(n), "S4": float(S4), "L4": L4}
        # one-shift: kbar = mean(k) (equal emitted luminosity per member; the letter L59)
        kb = kk.mean()
        row["err_r1a_bright"] = abs(kb**4 * n - S4) / S4
        row["err_r1a_colour"] = abs(np.log(kb) - L4) / np.log(2.0)
        # the rest of 9c08's bracket, reported not gated
        kb1b = float((k4 * kk).sum() / S4)
        row["err_r1b_bright"] = abs(kb1b**4 * n - S4) / S4
        row["err_r1b_colour"] = abs(np.log(kb1b) - L4) / np.log(2.0)
        k3 = (S4 / n) ** 0.25
        row["err_r3_bright"] = abs(k3**4 * n - S4) / S4       # ~0 by construction
        row["err_r3_colour"] = abs(np.log(k3) - L4) / np.log(2.0)
        k4c = float(np.exp(lnk.mean()))
        row["err_r4_bright"] = abs(k4c**4 * n - S4) / S4
        row["err_r4_colour"] = abs(np.log(k4c) - L4) / np.log(2.0)  # ~0 by construction
        # exact-sum brightness: the served value IS S4 -> error identically 0 (algebraic identity)
        row["err_exact_bright"] = 0.0
        # the L58 table: equal-ln-k histogram over the cell's own [k_min,k_max]
        lo, hi = lnk.min(), lnk.max()
        for B in bins_list:
            edges = np.linspace(lo, hi, B + 1) if hi > lo else np.full(B + 1, lo)
            which = np.clip(np.searchsorted(edges, lnk, side="right") - 1, 0, B - 1)
            w = np.bincount(which, weights=k4, minlength=B)
            ctr = 0.5 * (edges[:-1] + edges[1:])
            served = float((w * ctr).sum() / w.sum())
            row[f"hist_colour_{B}"] = abs(served - L4) / np.log(2.0)
            served4 = np.exp(4.0 * ctr)
            row[f"hist_bright_{B}"] = abs(float((w * served4).sum()) - S4) / S4
        out.append(row)
    return out


def case_metrics(gamma, theta_f, sky, ns, seed, bins_list):
    """per-case aggregates over multi-member cells: p99 (seen-flux-weighted) brightness error,
    max colour error, for the one-shift and exact-sum readouts."""
    cell, k = sample_cells(gamma, theta_f, sky, ns, seed)
    rows = cell_readouts(cell, k, bins_list)
    if not rows:
        raise RuntimeError("no multi-member cell")
    S4s = np.array([r["S4"] for r in rows])
    err_r1a = np.array([r["err_r1a_bright"] for r in rows])
    err_ex = np.array([r["err_exact_bright"] for r in rows])
    col_r1a = np.array([r["err_r1a_colour"] for r in rows])
    col_ex = np.array([r[f"hist_colour_{BINS}"] for r in rows])
    return {
        "gamma": gamma, "theta_f": theta_f, "sky": sky,
        "cells_multi": len(rows),
        "bright_p99_r1a": float(wquantile(err_r1a, 0.99, S4s)),
        "bright_p99_exact": float(wquantile(err_ex, 0.99, S4s)),
        "bright_max_r1a": float(err_r1a.max()),
        "colour_max_r1a": float(col_r1a.max()),
        "colour_max_exact": float(col_ex.max()),
        "rows": rows,
    }


def forward_detail(gamma, theta_f, sky, ns, seed):
    """the forward cell's numbers for the evidence table (9c08's headline cell)."""
    cell, k = sample_cells(gamma, theta_f, sky, ns, seed)
    m = cell == 0
    kk = k[m]
    if kk.size < 2:
        return {"n": int(kk.size)}
    k4 = kk**4
    S4 = k4.sum()
    L4 = float((k4 * np.log(kk)).sum() / S4)
    kb = kk.mean()
    beta = float(np.sqrt(1.0 - 1.0 / gamma**2))
    span = (1.0 - beta * np.cos(theta_f)) / (1.0 - beta)
    return {"n": int(kk.size), "flux_share": float(S4 / (k**4).sum()),
            "k_span": float(span), "r1a_bright": float(abs(kb**4 * kk.size - S4) / S4),
            "r1a_colour": float(abs(np.log(kb) - L4) / np.log(2.0))}


def quadrature_check():
    """independent continuum cross-check (Gauss-Legendre, machine precision) of the forward
    ring's exact sum(k^4) and the R1a (one-shift) brightness error, both skies."""
    import numpy.polynomial.legendre as L
    x, wgt = L.leggauss(4000)
    out = []
    for gf in (1.0, 4.0):
        for fn, tf in FLOORS.items():
            g = gf / tf
            beta = float(np.sqrt(1.0 - 1.0 / g**2))
            for sky in ("2D", "3D"):
                if sky == "2D":
                    def pprime(phi):
                        c, s = np.cos(phi), np.sin(phi)
                        return np.arctan2(s / (g * (1 + beta * c)), (c + beta) / (1 + beta * c))
                    lo, hi = 0.0, np.pi
                    for _ in range(200):
                        mid = 0.5 * (lo + hi)
                        if pprime(mid) < tf:
                            lo = mid
                        else:
                            hi = mid
                    phib = 0.5 * (lo + hi)
                    ph = 0.5 * phib * (x + 1.0)
                    ww = 0.5 * phib * wgt / (2 * np.pi)
                    kk = g * (1 + beta * np.cos(ph))
                else:
                    ub = (np.cos(tf) - beta) / (1 - beta * np.cos(tf))
                    uu = 0.5 * (1 - ub) * x + 0.5 * (1 + ub)
                    ww = 0.5 * (1 - ub) * wgt / 2.0
                    kk = g * (1 + beta * uu)
                S4 = float((ww * kk**4).sum())
                S1 = float((ww * kk).sum())
                N = float(ww.sum())
                out.append({"gamma": g, "floor": fn, "sky": sky,
                            "quad_r1a_bright": abs((S1 / N)**4 * N - S4) / S4})
    return out


def ops_update(config):
    """counted arithmetic operations of the per-due-event aggregate update, beyond the shipped
    row math (shift, lum*k^4, blackbody -- common to every configuration).

    shipped record (959a sums_add): n+=1; lum += row.luminosity (= sum lum*k^4, the exact
    seen-flux sum); lc[3] += color*luminosity (3 FMA); ls += light_seconds*luminosity (FMA);
    sh += shift*luminosity (FMA); kinds += 1  =>  8 ops.
    exact-sum candidate: the shipped 8 (sum lum*k^4 already in) + the L58 table:
    ln k (1), (ln k - base)*scale (2), bin clamp (0), bin += (1)  => extra 4.
    one-shift (the L59 collapse): n+=1; sum_lum += lum; sum_lum_k += k*lum (FMA) => 3, and the
    k^4/lc/ls/sh/kinds updates are gone => extra 3 - 8 = -5.
    """
    shipped = 1 + 1 + 3 + 1 + 1 + 1
    if config == "exact-sum":
        return 4
    if config == "one-shift":
        return 3 - shipped
    if config == "flat-gamma":
        return 4
    raise ValueError(config)


def main():
    seed = int(os.environ.get("SKY_SEED", "20261020"))
    ns = int(os.environ.get("NS", "2000000"))
    out_path = os.environ.get("METRICS_OUT", os.path.join(RUN, "metrics.json"))
    state = {"seed": seed, "ns": ns, "nproc": os.cpu_count(),
             "load": os.getloadavg(), "machine": platform.platform()}

    ev = {"state": state, "cases": [], "quadrature": [], "pilot": None}

    # ---- pilot (design, pre-freeze): histogram sizing at the worst case ----------------
    pilot = []
    for sky in ("2D", "3D"):
        cell, k = sample_cells(8000.0 / FLOORS["fine"], FLOORS["fine"], sky, ns, seed)
        rows = cell_readouts(cell, k, HIST_PILOT)
        pilot.append({"sky": sky,
                      "worst_colour_oct": {B: max(r[f"hist_colour_{B}"] for r in rows)
                                           for B in HIST_PILOT},
                      "worst_bright": {B: max(r[f"hist_bright_{B}"] for r in rows)
                                       for B in HIST_PILOT}})
    ev["pilot"] = pilot

    # ---- the frozen case set -----------------------------------------------------------
    for gamma, fn, sky, is_ctrl in CASES:
        m = case_metrics(gamma, FLOORS[fn], sky, ns, seed, [BINS])
        m["is_control"] = is_ctrl
        m["floor"] = fn
        m["forward"] = forward_detail(gamma, FLOORS[fn], sky, ns, seed)
        ev["cases"].append(m)

    ev["quadrature"] = quadrature_check()

    def agg(which, key):
        return max(c[key] for c in ev["cases"] if c["is_control"] == which)

    metrics = {
        "exact-sum": {
            "bright_p99": agg(False, "bright_p99_exact"),
            "colour_oct": agg(False, "colour_max_exact"),
            "ctrl_bright_max": agg(True, "bright_p99_exact"),
            "extra_due_ops": ops_update("exact-sum"),
        },
        "one-shift": {
            "bright_p99": agg(False, "bright_p99_r1a"),
            "colour_oct": agg(False, "colour_max_r1a"),
            "ctrl_bright_max": agg(True, "bright_p99_r1a"),
            "extra_due_ops": ops_update("one-shift"),
        },
        "flat-gamma": {
            "bright_p99": agg(True, "bright_p99_exact"),
            "colour_oct": agg(True, "colour_max_exact"),
            "ctrl_bright_max": agg(True, "bright_p99_exact"),
            "extra_due_ops": ops_update("flat-gamma"),
        },
    }
    with open(out_path, "w") as f:
        json.dump(metrics, f, indent=1)
    ev_path = out_path.replace(".json", "-evidence.json")
    with open(ev_path, "w") as f:
        json.dump(ev, f, indent=1)

    # ---- console digest ----------------------------------------------------------------
    print(f"== r13-sky-shift harness: seed {seed}, ns {ns}, B {BINS} ==")
    print("pilot (gamma*theta_f = 8000, fine floor, worst multi-member cell):")
    for p in pilot:
        print(f"  {p['sky']}: colour_oct by B: " +
              ", ".join(f"{B}:{p['worst_colour_oct'][B]:.4f}" for B in HIST_PILOT))
    print("case                       cells  bright_p99 r1a  bright_p99 ex   colour_max r1a  "
          "colour_max ex | forward cell: n, flux%, r1a_bright, r1a_colour")
    for c in ev["cases"]:
        tag = f"g{c['gamma']:.4g}/{c['floor']}/{c['sky']}" + ("/CTRL" if c["is_control"] else "")
        fwd = c["forward"]
        fs = (f"{fwd.get('n', 0)}, {fwd.get('flux_share', 0):.4f}, "
              f"{fwd.get('r1a_bright', float('nan')):.4f}, {fwd.get('r1a_colour', float('nan')):.4f}"
              ) if fwd.get("n", 0) >= 2 else "sparse"
        print(f"  {tag:26s} {c['cells_multi']:6d}  {c['bright_p99_r1a']:13.6f}  "
              f"{c['bright_p99_exact']:13.3e}  {c['colour_max_r1a']:13.6f}  "
              f"{c['colour_max_exact']:13.6f} | {fs}")
    print("quadrature cross-check (forward ring, continuum):")
    for q in ev["quadrature"]:
        print(f"  g{q['gamma']:.4g}/{q['floor']}/{q['sky']}: quad_r1a_bright = {q['quad_r1a_bright']:.6f}")
    print("metrics:")
    print(json.dumps(metrics, indent=1))


if __name__ == "__main__":
    main()
