#!/usr/bin/env python3
"""News-channel scaling at one body as the light cone grows (run 20261008-1859-scout-141c).

Units G = c = 1. Observer is a test body at the origin of a 2D disk of sources on
circular Keplerian orbits (Omega = a^-1.5), surface density rho held fixed as the
cone radius R grows (the board's fixed-distribution risk).

Channels at the observer:
  naive     : one cursor per source; every change is delivered and counted.
  aggregate : sources grouped into log2 shells; each shell's net force series is
              quantized at Q; sub-quantum events accumulate per shell and fire one
              arrival when the accumulator crosses Q. Events with size >= Q fire
              individually (cataclysms).

Everything is measured as an arrival RATE (intensive), so windows can differ per R.
"""
import json
import math
import sys

import numpy as np

RNG = np.random.default_rng(20261008)

# ----------------------------------------------------------------------------
# Case S (calibration): smooth uniform disk, no events. Circular orbits make the
# retarded force series closed-form (retardation is a per-source phase shift).
# Per-source change rate is exactly r_i = G m_i Omega_i / a_i^2 (constant).
# The shell-sum rate with random phases is the RMS of the vector sum (cross terms
# vanish in expectation); E|v| = sqrt(pi/4) * RMS for a 2D isotropic Gaussian.
# ----------------------------------------------------------------------------

def case_smooth(rho, r0, R, m=1.0):
    """Analytic per-source and shell-sum change rates (closed form, circular orbits).

    Retardation is a per-source phase shift, so each source's force vector rotates
    at Omega_i with constant magnitude G m_i / a_i^2: its change rate is exactly
    G m_i Omega_i / a_i^2 = m a^-3.5. The shell sum with random phases has
    E|dF/dt| = sqrt(pi/4) * RMS of the per-source rate vectors (2D Gaussian).
    """
    edges = r0 * np.exp2(np.arange(1, math.log2(R / r0) + 1e-9))
    edges = np.concatenate([[r0], edges])
    if edges[-1] < R:
        edges = np.append(edges, R)
    naive_rate = 0.0
    agg_rate = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        area = math.pi * (hi * hi - lo * lo)
        n = max(int(area * rho), 8)
        a = np.sqrt(RNG.uniform(lo * lo, hi * hi, n))
        r_i = m * a ** -3.5  # G m Omega / a^2 with Omega = a^-1.5
        w = rho * area / n   # population weight per sample
        naive_rate += r_i.sum() * w
        agg_rate += math.sqrt(math.pi / 4) * math.sqrt(w * (r_i**2).sum())
    return naive_rate, agg_rate


def case_smooth_grid(rho, r0, R, m=1.0, T=200.0, dt=None, n_cap=200_000):
    """Direct time-grid check of the shell-sum rate (random phases, closed form)."""
    edges = np.exp2(np.arange(0, math.log2(R / r0) + 1e-9))
    edges = r0 * np.concatenate([[0.0], edges])
    edges[0] = r0
    if edges[-1] < R:
        edges = np.append(edges, R)
    a_list, m_list = [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        area = math.pi * (hi * hi - lo * lo)
        n = min(max(int(area * rho), 4), n_cap // len(edges))
        a_list.append(np.sqrt(RNG.uniform(lo * lo, hi * hi, n)))
        m_list.append(np.full(n, rho * area / n * m))
    a = np.concatenate(a_list)
    mi = np.concatenate(m_list)
    phi = RNG.uniform(0, 2 * math.pi, len(a))
    Om = a ** -1.5
    if dt is None:
        dt = 0.002 * 2 * math.pi * a.min() ** 1.5
    t = np.arange(0.0, T, dt)
    # force time series in chunks (memory cap)
    tv = 0.0
    prev = None
    CH = 200_000
    for s in range(0, len(t), CH):
        tc = t[s : s + CH]
        ph = Om[None, :] * (tc[:, None] - a[None, :]) + phi[None, :]
        fx = (mi[None, :] / a[None, :] ** 2 * np.cos(ph)).sum(1)
        fy = (mi[None, :] / a[None, :] ** 2 * np.sin(ph)).sum(1)
        f = np.stack([fx, fy], 1)
        if prev is not None:
            f = np.vstack([prev, f])
        tv += np.abs(np.diff(f, axis=0)).sum()
        prev = f[-1:]
    return tv / T


# ----------------------------------------------------------------------------
# Cases E (decisive) and C (cataclysms): Poisson surprise events.
# Event on source at radius a changes its retarded force at the observer by
# s(a) = G * delta / a^2 (mass change). Arrival time = t_e + a (c = 1).
# ----------------------------------------------------------------------------

def shells(r0, R, n_min=24):
    """Multiplicative shell edges covering [r0, R]; at least n_min shells."""
    k = max(int(math.ceil(math.log2(R / r0))), n_min)
    return r0 * np.exp2(np.linspace(0, math.log2(R / r0), k + 1))




def run_event_case(r0, Rlist, rho, lam, delta, Q, seed=7):
    """Sweep R; arrival rates per unit time for both channels (binned exact Poisson).

    Within a radius bin all sources share a (event size s = delta/a^2 constant),
    so the per-bin arrival count over window T is Poisson with mean
    lam * area * T. Sub-Q bins accumulate into their octave shell; the shell
    fires floor(total/Q) arrivals over the window (order within the octave
    affects only the final partial carry, O(1) per shell).
    """
    out = []
    for R in Rlist:
        rng = np.random.default_rng(seed + int(1000 * math.log(R)))
        ed = shells(r0, R)
        mid = np.sqrt(ed[:-1] * ed[1:])
        areas = math.pi * (ed[1:] ** 2 - ed[:-1] ** 2)
        T = 40.0 * R / Rlist[0] + 4.0 * R  # long enough that rates are stationary
        k = rng.poisson(lam * areas * T)  # events per bin over window T
        s = delta / mid**2  # event size per bin
        naive = int(k.sum())
        # quantum: individually if s >= Q, else accumulate per log2 shell of width 1 octave
        fire = np.where(s >= Q, k, 0).sum()
        # accumulation: shells of one octave in radius
        oct_idx = np.floor(np.log2(mid / r0)).astype(int)
        acc = {}
        carry = {}
        for b in range(len(mid)):
            if s[b] >= Q:
                continue
            key = oct_idx[b]
            acc[key] = acc.get(key, 0.0) + k[b] * s[b]
        for key, tot in acc.items():
            fire += math.floor(tot / Q)
        out.append(
            dict(R=float(R), T=T, naive_rate=naive / T, quantum_rate=float(fire) / T,
                 n_sources=float((rho * math.pi * (R * R - r0 * r0))),
                 r_cut=float(math.sqrt(delta / Q)) if Q > 0 else float("inf"),
                 n_shells=int(len(ed) - 1))
        )
    return out

def run_event_case_bursty(r0, Rlist, rho, lam, delta, Q, n_bursts=200, seed=11):
    """Adversarial: every source fires in synchronous bursts (all arrivals at once).

    Bunching sums sizes before thresholding; a burst of total size B fires
    floor(B/Q) arrivals, so the count cannot exceed the spread case's sum/Q
    bound. Checks that correlation does not inflate the quantum channel.
    """
    out = []
    for R in Rlist:
        rng = np.random.default_rng(seed + int(1000 * math.log(R)))
        ed = shells(r0, R)
        mid = np.sqrt(ed[:-1] * ed[1:])
        areas = math.pi * (ed[1:] ** 2 - ed[:-1] ** 2)
        T = 14.0 * R
        epochs = np.sort(rng.uniform(0, T, n_bursts))
        lam_t = lam * T / n_bursts  # same total event budget, all bunched
        oct_idx = np.floor(np.log2(mid / r0)).astype(int)
        s = delta / mid**2
        naive = 0
        fires = 0.0
        acc = {}
        for _t in epochs:
            k = rng.poisson(lam_t * areas)
            naive += int(k.sum())
            for b in range(len(mid)):
                if s[b] >= Q:
                    fires += k[b]
                else:
                    acc[oct_idx[b]] = acc.get(oct_idx[b], 0.0) + k[b] * s[b]
        fires += sum(math.floor(v / Q) for v in acc.values())
        out.append(dict(R=float(R), T=T, naive_rate=naive / T,
                        quantum_rate=float(fires) / T))
    return out


def run_cataclysm_case(r0, Rlist, Lam_total, delta_big, Q):
    """Rare events, size delta_big/a^2 >= Q everywhere: both channels see ~Lam_total."""
    out = []
    for R in Rlist:
        rng = np.random.default_rng(99 + int(1000 * math.log(R)))
        T = 40.0 * R / Rlist[0] + 4.0 * R
        k = rng.poisson(Lam_total * T)
        out.append(dict(R=float(R), T=T, naive_rate=k / T, quantum_rate=k / T))
    return out


# ----------------------------------------------------------------------------
# Case M1 (held-out): coherent lopsided disk, pattern speed Om_p constant.
# Shell j contributes amplitude A_j ~ 2 pi eps G rho da / a_j at the observer;
# the total amplitude grows ~ ln R, so the quantized TV rate grows ~ ln R.
# ----------------------------------------------------------------------------

def case_m1(rho, r0, Rlist, eps, Om_p, Q):
    out = []
    for R in Rlist:
        ed = shells(r0, R)
        A = 2 * math.pi * eps * rho * (ed[1:] - ed[:-1]) / ed[:-1]
        amp = A.sum()
        out.append(dict(R=float(R), naive_rate=None, agg_rate=amp * Om_p / Q,
                        amplitude=amp))
    return out


def main():
    res = {}
    rho = 1.0 / math.pi  # N = R^2 - r0^2 sources
    r0 = 1.0

    # S: smooth disk calibration, R sweep (analytic; grid check at R=16)
    S = []
    for R in [4.0, 16.0, 64.0, 256.0, 1024.0]:
        n, a = case_smooth(rho, r0, R)
        S.append(dict(R=R, naive_rate=n, agg_rate_rms=a))
    g = case_smooth_grid(rho, r0, 16.0, T=400.0)
    res["smooth"] = dict(sweep=S, grid_check_R16_tv_rate=g)

    # E: decisive sweep, three decades, two Q values (P4)
    Rlist = [4.0, 8.0, 16.0, 32.0, 64.0, 128.0, 256.0, 512.0, 1024.0]
    for name, delta, Q in [("Q1", 1.0, 1e-3), ("Q2", 1.0, 1e-2), ("Q3", 1.0, 1e-4)]:
        res[f"events_{name}"] = run_event_case(r0, Rlist, rho, lam=1e-2, delta=delta, Q=Q)
    # seed spread for the decisive case (Q1)
    spread = []
    for sd in range(5):
        rr = run_event_case(r0, Rlist, rho, lam=1e-2, delta=1.0, Q=1e-3, seed=100 + sd)
        spread.append([r["quantum_rate"] for r in rr])
    res["events_Q1_seed_spread"] = dict(
        R=Rlist, mean=[float(m) for m in np.mean(spread, 0)],
        std=[float(m) for m in np.std(spread, 0)])

    # adversarial: fully correlated bursts (bunched arrivals)
    res["events_Q1_bursty"] = run_event_case_bursty(r0, Rlist, rho, lam=1e-2,
                                                    delta=1.0, Q=1e-3)

    # C: cataclysms (held-out P5)
    res["cataclysms"] = run_cataclysm_case(r0, Rlist, Lam_total=0.05, delta_big=1e6, Q=1e-3)

    # M1: coherent lopsided disk (held-out P6)
    res["m1"] = case_m1(rho, r0, Rlist, eps=0.01, Om_p=0.1, Q=1e-3)

    def slope(rows, key):
        x = np.log2([r["R"] for r in rows])
        y = np.log10([r[key] for r in rows])
        return float(np.polyfit(x[-4:], y[-4:], 1)[0])  # slope over top decade

    summ = {}
    summ["smooth_naive_slope_topdecade"] = slope(res["smooth"]["sweep"], "naive_rate")
    summ["smooth_agg_slope_topdecade"] = slope(res["smooth"]["sweep"], "agg_rate_rms")
    for name in ["events_Q1", "events_Q2", "events_Q3"]:
        summ[f"{name}_naive_slope"] = slope(res[name], "naive_rate")
        summ[f"{name}_quantum_slope"] = slope(res[name], "quantum_rate")
        # log-fit: quantum_rate ~ a + b * n_shells
        x = np.array([r["n_shells"] for r in res[name]], float)
        y = np.array([r["quantum_rate"] for r in res[name]], float)
        b = np.polyfit(x, y, 1)[0]
        summ[f"{name}_quantum_per_shell"] = float(b)
    summ["m1_agg_slope_topdecade"] = slope(res["m1"], "agg_rate")
    res["summary"] = summ

    print(json.dumps(summ, indent=1))
    for name in ["events_Q1", "events_Q2", "events_Q3"]:
        print(f"\n[{name}]  R  naive_rate  quantum_rate  r_cut  n_shells")
        for r in res[name]:
            print(f"  {r['R']:8.0f}  {r['naive_rate']:10.4g}  {r['quantum_rate']:10.4g}  "
                  f"{r['r_cut']:8.3g}  {r['n_shells']}")
    print("\n[smooth]", json.dumps(res["smooth"], indent=1)[:800])
    print("\n[m1]", json.dumps(res["m1"][-3:], indent=1))
    print("\n[cataclysms]", json.dumps(res["cataclysms"][-3:], indent=1))
    print("\n[bursty Q1] R naive quantum")
    for r in res["events_Q1_bursty"]:
        print(f"  {r['R']:8.0f}  {r['naive_rate']:10.4g}  {r['quantum_rate']:10.4g}")
    print("\n[seed spread Q1] R mean std")
    for R_, m_, s_ in zip(res["events_Q1_seed_spread"]["R"],
                          res["events_Q1_seed_spread"]["mean"],
                          res["events_Q1_seed_spread"]["std"]):
        print(f"  {R_:8.0f}  {m_:10.4g}  {s_:10.4g}")
    with open("news_scaling.json", "w") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    sys.exit(main())
