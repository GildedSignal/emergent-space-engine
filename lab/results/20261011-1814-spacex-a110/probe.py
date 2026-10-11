#!/usr/bin/env python3
"""Co-orbital certificate degradation probe (lab run 20261011-1814-spacex-a110).

Adopted encounters design (docs/law.md; r8 v2/q-candidate-degree; gold
20261006-0346-taleb-09b5): a window tier (Binet-cone candidate pairs on
(U,V,W), paid per element change) plus, when co-orbital concentration fires,
a phase-neighbour certificate (rank k along the orbit, O(n*k)).

This probe measures, on 2D Kepler swarms about one mass (GM=1, a=1, v=1,
orbit=2*pi; no mutual gravity, as in r8: candidates = orbit overlap,
encounters = close conjunctions):

  enc/body/orbit   real encounters (exact Kepler miss < b at a refined
                   true-longitude conjunction) -- the truth both tiers serve
  cone/enc         window-tier work proxy: Binet-cone pairs x 1.1 element
                   changes/body/orbit, per encounter
  swaps/enc        phase-tier steady work proxy: every conjunction is one
                   adjacent transposition of the phase (longitude) order;
                   a certificate must pay the churn it certifies through
  d0               partner's rank in the longitude order at certificate
                   epoch t=0 (d=1 neighbours); the operational meaning of
                   "rank 4": certify k neighbours now, catch encounters in
                   the next H without rebuild
  d_half           the same, epoch T/2 over encounters in [T/2, T]

Degradation axes: phase packing (packed convoy slots -> uniform ring),
sigma_a (age/spread), sigma_e, b (encounter radius: ship scale to fleet
spacing), plus a two-fleet engagement pass.
"""
import numpy as np
import json, time

TWO_PI = 2.0 * np.pi

def kepler(a, e, w, M):
    """(r, theta) from mean anomaly M; Newton on Kepler's equation (e<=0.6)."""
    E = M + e * np.sin(M)
    for _ in range(6):
        E = E - (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    r = a * (1.0 - e * np.cos(E))
    th = w + 2.0 * np.arctan2(np.sqrt(1.0 + e) * np.sin(E / 2.0),
                              np.sqrt(1.0 - e) * np.cos(E / 2.0))
    return r, th

def theta_rate(a, e, nn, r):
    """exact d(theta)/dt = h / r^2, h = n a^2 sqrt(1-e^2)."""
    return nn * a * a * np.sqrt(1.0 - e * e) / (r * r)

def swarm(rng, n, sig_a, sig_e, packing, a_lo=None):
    """packing='slots': contiguous phase lattice (a convoy); 'ring': uniform."""
    if a_lo is None:
        a = np.clip(rng.normal(1.0, sig_a, n), 0.5, 1.5)
    else:
        a = np.clip(rng.normal(a_lo, sig_a, n), 0.5, 1.5)
    e = np.clip(rng.rayleigh(sig_e, n), 0.0, 0.6)
    w = rng.uniform(0.0, TWO_PI, n)
    if packing == "slots":
        M = (TWO_PI * np.arange(n) / n + rng.uniform(-0.05, 0.05, n) * TWO_PI / n) % TWO_PI
    else:
        M = rng.uniform(0.0, TWO_PI, n)
    return a, e, w, M

def two_fleets(rng, n_per, sig_a, sig_e, da, dth):
    """Two packed convoys on orbits 1-da and 1+da, phase centres 0 and dth,
    so they close (synodic) and pass through each other mid-run."""
    a = np.concatenate([rng.normal(1.0 - da, sig_a, n_per),
                        rng.normal(1.0 + da, sig_a, n_per)])
    e = np.clip(np.concatenate([rng.rayleigh(sig_e, n_per),
                                rng.rayleigh(sig_e, n_per)]), 0.0, 0.6)
    w = rng.uniform(0.0, TWO_PI, 2 * n_per)
    slot = TWO_PI / n_per
    M = np.concatenate([rng.uniform(-0.05, 0.05, n_per) * slot,
                        dth + rng.uniform(-0.05, 0.05, n_per) * slot]) % TWO_PI
    return np.clip(a, 0.5, 1.5), e, w, M

def cone_pair_count(a, e, w):
    p = a * (1.0 - e * e)
    U = 1.0 / p; V = e * np.cos(w) / p; W = e * np.sin(w) / p
    n = len(U); cnt = 0; step = 1024
    for s in range(0, n, step):
        sl = slice(s, min(s + step, n))
        dU2 = (U[sl, None] - U[None, :]) ** 2
        ok = dU2 <= (V[sl, None] - V[None, :]) ** 2 + (W[sl, None] - W[None, :]) ** 2
        cnt += int(np.count_nonzero(np.triu(ok, k=1 + s)))
    return cnt

def conj_times(a, e, w, M0, nn, T_tot):
    """Mean-longitude conjunction times, then Newton to true-longitude
    alignment. Returns i, j, t (refined), miss."""
    n = len(a)
    ii, jj = np.triu_indices(n, k=1)
    L0 = w + M0
    dn = nn[ii] - nn[jj]
    adn = np.abs(dn)
    keep = adn > 1e-13
    ii, jj, dn, adn = ii[keep], jj[keep], dn[keep], adn[keep]
    # first conjunction: (L0i + nn_i t) - (L0j + nn_j t) hits a multiple of 2pi
    dL0 = np.mod((L0[jj] - L0[ii]) * np.sign(dn), TWO_PI)  # grows through 2pi
    t0 = dL0 / adn
    K = np.floor((T_tot - t0) * adn / TWO_PI).astype(np.int64) + 1
    K[K < 0] = 0
    tot = int(K.sum())
    if tot == 0:
        return (np.array([], np.int32), np.array([], np.int32),
                np.array([]), np.array([]))
    pair_idx = np.repeat(np.arange(len(ii)), K)
    starts = np.zeros(len(ii)); starts[1:] = np.cumsum(K)[:-1]
    ks = np.arange(tot) - np.repeat(starts, K)
    ev_i = np.empty(tot, np.int32); ev_j = np.empty(tot, np.int32); ev_t = np.empty(tot)
    step = 2_000_000
    for s in range(0, tot, step):
        sl = slice(s, min(s + step, tot))
        p = pair_idx[sl]
        ev_i[sl] = ii[p]; ev_j[sl] = jj[p]
        ev_t[sl] = (dL0[p] + TWO_PI * ks[sl]) / adn[p]
    m = ev_t < T_tot
    ev_i, ev_j, ev_t = ev_i[m], ev_j[m], ev_t[m]
    del pair_idx, ks, ii, jj, dn, adn, K, keep
    # Newton refine to true-longitude alignment (2 rounds is enough from a
    # mean-longitude start at these e; do 3)
    for _ in range(3):
        Mi = np.mod(M0[ev_i] + nn[ev_i] * ev_t, TWO_PI)
        Mj = np.mod(M0[ev_j] + nn[ev_j] * ev_t, TWO_PI)
        ri, ti = kepler(a[ev_i], e[ev_i], w[ev_i], Mi)
        rj, tj = kepler(a[ev_j], e[ev_j], w[ev_j], Mj)
        dth = np.mod(ti - tj + np.pi, TWO_PI) - np.pi   # wrap to (-pi, pi]
        rate = (theta_rate(a[ev_i], e[ev_i], nn[ev_i], ri)
                - theta_rate(a[ev_j], e[ev_j], nn[ev_j], rj))
        slow = np.abs(rate) < 1e-9
        dt = np.where(slow, 0.0, dth / np.where(slow, 1.0, rate))
        ev_t = ev_t - dt
        # keep only events that still land inside the horizon
        ok = (ev_t >= 0) & (ev_t < T_tot)
        if not ok.all():
            ev_i, ev_j, ev_t, dth = ev_i[ok], ev_j[ok], ev_t[ok], dth[ok]
            ri, rj = ri[ok], rj[ok]
    # final miss at the refined times (exact separation; at true-longitude
    # alignment this is |r_i - r_j|, computed from full state for safety)
    Mi = np.mod(M0[ev_i] + nn[ev_i] * ev_t, TWO_PI)
    Mj = np.mod(M0[ev_j] + nn[ev_j] * ev_t, TWO_PI)
    ri, ti = kepler(a[ev_i], e[ev_i], w[ev_i], Mi)
    rj, tj = kepler(a[ev_j], e[ev_j], w[ev_j], Mj)
    miss = np.sqrt(ri * ri + rj * rj - 2.0 * ri * rj * np.cos(ti - tj))
    return ev_i, ev_j, ev_t, miss

def order_positions(a, e, w, M0, nn, t):
    M = np.mod(M0 + nn * t, TWO_PI)
    _, th = kepler(a, e, w, M)
    th = np.mod(th, TWO_PI)   # kepler returns w + nu in [0, 4pi): wrap first
    order = np.argsort(th, kind='stable')
    pos = np.empty(len(th), np.int64); pos[order] = np.arange(len(th))
    return pos

def circ_d(pos, i, j, n):
    d = np.abs(pos[i] - pos[j])
    return np.minimum(d, n - d)

def run_config(name, a, e, w, M0, b, T_orbits, note=""):
    t_start = time.time()
    n = len(a)
    nn = a ** -1.5
    T_tot = TWO_PI * T_orbits
    cp = cone_pair_count(a, e, w)
    ii, jj = np.triu_indices(n, k=1)
    swaps_total = float(np.sum(np.abs(nn[ii] - nn[jj])) * T_tot / TWO_PI)
    del ii, jj
    ev_i, ev_j, ev_t, miss = conj_times(a, e, w, M0, nn, T_tot)
    enc = miss < b
    ei, ej, et = ev_i[enc], ev_j[enc], ev_t[enc]
    n_enc = int(len(ei))
    pos0 = order_positions(a, e, w, M0, nn, 0.0)
    d0 = circ_d(pos0, ei, ej, n) if n_enc else np.array([], np.int64)
    th = T_tot / 2.0
    late = et >= th
    dH = None
    if late.any():
        posH = order_positions(a, e, w, M0, nn, th)
        dH = circ_d(posH, ei[late], ej[late], n)
    def pct(x, q):
        return float(np.percentile(x, q)) if len(x) else None
    res = {
        "name": name, "note": note, "n": n, "b": b, "T_orbits": T_orbits,
        "events": int(len(ev_i)),
        "swaps_body_orbit": swaps_total / (n * T_orbits),
        "cone_pairs": cp, "cone_per_body": 2.0 * cp / n,
        "enc": n_enc,
        "enc_body_orbit": n_enc / (n * T_orbits),
        "swaps_per_enc": swaps_total / n_enc if n_enc else None,
        "cone_per_enc": cp * 1.1 * T_orbits / n_enc if n_enc else None,
        "d0_med": pct(d0, 50), "d0_p99": pct(d0, 99), "d0_max": int(d0.max()) if n_enc else None,
        "d0_le4": float(np.mean(d0 <= 4)) if n_enc else None,
        "d0_le8": float(np.mean(d0 <= 8)) if n_enc else None,
        "dH_med": pct(dH, 50) if dH is not None else None,
        "dH_p99": pct(dH, 99) if dH is not None else None,
        "dH_le4": float(np.mean(dH <= 4)) if dH is not None else None,
        "wall_s": round(time.time() - t_start, 1),
    }
    return res

def main():
    out = []
    def add(name, mk, b, T, note=""):
        rng = np.random.default_rng(abs(hash(name)) % 10_000)
        out.append(run_config(name, *mk(rng), b, T, note))

    B = 3e-3   # default b/a: fleet-spacing encounter scale (~450 km at 1 AU)
    SE = 0.03  # default eccentricity noise

    # controls
    add("ctrl-fresh-convoy", lambda r: swarm(r, 4096, 1e-6, 0.01, "slots"), B, 256,
        "the gold taleb-09b5 case: packed convoy, one orbit")
    add("ctrl-belt-ring", lambda r: swarm(r, 1024, 3e-2, 0.15, "ring"), B, 8,
        "window tier's home ground; cross-check vs r8 v2's 786/enc")

    # convoy aging: same fleet, growing engine/age spread (packed slots)
    for k, sa in enumerate([3e-5, 1e-4, 3e-4, 1e-3]):
        T = {3e-5: 128, 1e-4: 64, 3e-4: 32, 1e-3: 16}[sa]
        add(f"convoy-sa{sa:g}", lambda r, sa=sa: swarm(r, 4096, sa, 0.01, "slots"), B, T)

    # dispersed ring (phases uniformized: an old swarm), sigma_a sweep
    for k, sa in enumerate([1e-4, 1e-3, 3e-3, 1e-2]):
        T = {1e-4: 64, 1e-3: 16, 3e-3: 8, 1e-2: 4}[sa]
        add(f"ring-sa{sa:g}", lambda r, sa=sa: swarm(r, 1024, sa, SE, "ring"), B, T)

    # eccentricity sweep in the middle (orbits crossing)
    for k, se in enumerate([0.0, 0.03, 0.15]):
        add(f"ring-se{se:g}", lambda r, se=se: swarm(r, 1024, 1e-3, se, "ring"), B, 16)

    # b sweep: fleet spacing -> ship scale (both tiers' 1/b law?)
    for k, b2 in enumerate([1e-4, 1e-2]):
        add(f"b{b2:g}-ring-mid", lambda r: swarm(r, 1024, 1e-3, SE, "ring"), b2, 16)
        add(f"b{b2:g}-convoy-aged", lambda r: swarm(r, 4096, 1e-4, 0.01, "slots"), b2, 64)

    # n scaling in the middle
    for k, n in enumerate([512, 2048]):
        add(f"nscale-n{n}", lambda r, n=n: swarm(r, n, 1e-3, SE, "ring"), B, 16)

    # two-fleet engagement pass
    add("twofleet-pass", lambda r: two_fleets(r, 512, 1e-4, 0.01, 3e-2, np.pi), B, 8,
        "packed convoys closing at synodic rate, pass mid-run")

    with open("results.json", "w") as f:
        json.dump(out, f, indent=1)
    hdr = (f"{'config':22s} {'n':>5s} {'T':>4s} {'b':>6s} {'enc':>5s} {'enc/b/o':>8s} "
           f"{'swp/b/o':>8s} {'cone/n':>7s} {'swp/enc':>8s} {'cone/enc':>9s} "
           f"{'d0md':>6s} {'d0p99':>7s} {'d0mx':>6s} {'d0<=4':>6s} {'d0<=8':>6s} "
           f"{'dHmd':>6s} {'dH<=4':>6s} {'w_s':>5s}")
    print(hdr); print("-" * len(hdr))
    for r in out:
        def f2(x, w=8):
            return f"{x:{w}.2f}" if x is not None else "--".rjust(w)
        print(f"{r['name']:22s} {r['n']:5d} {r['T_orbits']:4.0f} {r['b']:6.0e} "
              f"{r['enc']:5d} {f2(r['enc_body_orbit'], 8)} {f2(r['swaps_body_orbit'], 8)} "
              f"{f2(r['cone_per_body'], 7)} {f2(r['swaps_per_enc'], 8)} "
              f"{f2(r['cone_per_enc'], 9)} {f2(r['d0_med'], 6)} {f2(r['d0_p99'], 7)} "
              f"{f2(r['d0_max'], 6)} {f2(r['d0_le4'], 6)} {f2(r['d0_le8'], 6)} "
              f"{f2(r['dH_med'], 6)} {f2(r['dH_le4'], 6)} {r['wall_s']:5.1f}")

if __name__ == "__main__":
    main()
