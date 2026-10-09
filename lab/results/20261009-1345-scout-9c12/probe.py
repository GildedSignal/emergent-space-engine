#!/usr/bin/env python3
"""Causal-frontier cascade probe (run 20261009-1345-scout-9c12).

Model (predictions.md): a scar is a body's position-equivalent error eps
(relative units). Encounter with impact parameter b transfers
eps_child = C_a/b^2 * eps * |cos| to the partner. Live = eps >= q.
Below q the transfer accumulates on the partner (principle 6) and can
cross q later (amplified by chaos). Planet flybys amplify the flyer's own
error by f_p in [139, 634] (self) and birth children at f_p * eps.

Vectorized time-stepped Monte-Carlo, orbits as time unit.
"""
import json, os, sys, time
import numpy as np

C_A = 2.67e5          # 2 G m tau / v_rel, m^2 (belt bodies, see predictions)
BMIN, BMAX = 1e3, 2.6e5
F_P_LO, F_P_HI = 139.0, 634.0
EPS_CAP = 0.5
DUST_CAP = 100_000    # tracked dust entries; extras only counted
LIVE_CAP = 600_000


def run(name, *, N=10**6, n0=8, n_fleet=0, eps0=8e-4, q=1e-6,
        nu_a=1.1, nu_fleet=20.0, nu_p=0.0, lam=0.0, T=100.0,
        dt=0.1, seed=0, note=""):
    rng = np.random.default_rng(seed)
    bmin2, bmax2 = BMIN * BMIN, BMAX * BMAX
    t_start = time.time()
    eps = np.full(n0, eps0)
    fleet = np.zeros(n0, dtype=bool)
    if n_fleet:
        fleet[:] = True          # first n_fleet of the n0 live are fleet members
    dust = np.empty(0)
    n_dust_extra = 0
    births_cum = dust_cross_cum = 0
    ast_cum = fly_cum = 0
    capped = False
    log = []
    steps = int(round(T / dt))
    growth = np.exp(lam * dt)
    for s in range(steps):
        t = (s + 1) * dt
        if lam:
            eps *= growth
            if dust.size:
                dust *= growth
            np.minimum(eps, EPS_CAP, out=eps)
        eps[0] = max(eps[0], eps0)                    # the player re-burns
        L = eps.size
        nu = np.where(fleet, nu_fleet, nu_a)
        counts = rng.poisson(nu * dt)
        E = int(counts.sum())
        if E:
            ast_cum += E
            par = np.repeat(np.arange(L), counts)
            b2 = bmin2 + rng.random(E) * (bmax2 - bmin2)
            tr = (C_A / b2) * eps[par] * rng.random(E)   # |cos| ~ U(0,1)
            is_born = tr >= q
            nb = int(np.count_nonzero(is_born))
            room = N - L
            if nb > room:
                idx = np.flatnonzero(is_born)
                idx = idx[rng.permutation(nb)[:room]]
                sel = np.zeros(E, dtype=bool); sel[idx] = True
                is_born = sel; nb = room; capped = True
            if nb:
                new = tr[is_born]
                np.minimum(new, EPS_CAP, out=new)
                eps = np.concatenate((eps, new))
                fleet = np.concatenate((fleet, np.zeros(nb, dtype=bool)))
                births_cum += nb
            nd = E - int(np.count_nonzero(is_born))
            if nd:
                pd = (dust.size + n_dust_extra) / N
                hit = rng.random(nd) < pd            # partner already dusted
                m = int(np.count_nonzero(hit))
                if m and dust.size:
                    tgt = rng.integers(0, dust.size, m)
                    dust += np.bincount(tgt, weights=tr[~is_born][hit],
                                        minlength=dust.size)
                new_d = nd - m
                if new_d:
                    vals = tr[~is_born][~hit]
                    if dust.size + new_d <= DUST_CAP:
                        dust = np.concatenate((dust, vals))
                    else:
                        take = max(0, DUST_CAP - dust.size)
                        if take:
                            dust = np.concatenate((dust, vals[:take]))
                        n_dust_extra += new_d - take
        if nu_p > 0 and eps.size:
            L = eps.size
            cp = rng.poisson(nu_p * dt, L)
            Ep = int(cp.sum())
            if Ep:
                fly_cum += Ep
                parp = np.repeat(np.arange(L), cp)
                fp = F_P_LO + (F_P_HI - F_P_LO) * rng.random(Ep)
                # self-amplification of the flyer's own error (scatter-max)
                amp = np.minimum(eps[parp] * (1.0 + fp * rng.random(Ep)), EPS_CAP)
                np.maximum.at(eps, parp, amp)
                trp = fp * eps[parp] * rng.random(Ep)
                nbp = int(np.count_nonzero(trp >= q))
                room = N - eps.size
                if nbp > room:
                    nbp = room; capped = True
                if nbp:
                    new = trp[trp >= q][:nbp]
                    np.minimum(new, EPS_CAP, out=new)
                    eps = np.concatenate((eps, new))
                    fleet = np.concatenate((fleet, np.zeros(nbp, dtype=bool)))
                    births_cum += nbp
        # dust crossings
        if dust.size:
            crossed = dust >= q
            nc = int(np.count_nonzero(crossed))
            if nc:
                vals = dust[crossed]
                np.minimum(vals, EPS_CAP, out=vals)
                room = N - eps.size
                if nc > room:
                    vals = vals[:room]; capped = True; nc = room
                if nc:
                    eps = np.concatenate((eps, vals))
                    fleet = np.concatenate((fleet, np.zeros(nc, dtype=bool)))
                    births_cum += nc
                    dust_cross_cum += nc
                    dust = dust[~crossed]
        if eps.size > LIVE_CAP:                       # safety for runtime
            eps = eps[:LIVE_CAP]; fleet = fleet[:LIVE_CAP]; capped = True
        if abs(t - round(t)) < dt / 2 and round(t) >= 1:
            log.append(dict(t=round(t), n_live=int(eps.size),
                            n_dusted=int(dust.size + n_dust_extra),
                            births_cum=births_cum,
                            dust_cross=dust_cross_cum,
                            ast_cum=ast_cum, fly_cum=fly_cum,
                            eps_max=float(eps.max()),
                            eps_mean=float(eps.mean())))
    wall = time.time() - t_start
    # growth exponent fit on second half (if growing and unsaturated)
    expo = None
    half = [r for r in log if r["t"] >= T / 2 and 0 < r["n_live"] < N // 2]
    if len(half) >= 6:
        x = np.array([r["t"] for r in half], float)
        y = np.log(np.array([r["n_live"] for r in half], float))
        expo = float(np.polyfit(x, y, 1)[0])
    out = dict(name=name, note=note, q=q, nu_p=nu_p, lam=lam, nu_a=nu_a,
               nu_fleet=nu_fleet, n0=n0, n_fleet=n_fleet, N=N, T=T, dt=dt,
               seed=seed, wall_s=round(wall, 2), capped=capped,
               exponent_per_orbit=expo, log=log)
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      f"out-{name}.json")
    with open(fn, "w") as fh:
        json.dump(out, fh, indent=1)
    tail = log[-1]
    mid = log[len(log) // 2]
    print(f"{name:14s} T={T:5.0f} n_live {n0}->{tail['n_live']:>8d} "
          f"(mid {mid['n_live']:>7d}) births {births_cum:>8d} "
          f"dusted {tail['n_dusted']:>7d} flybys {fly_cum:>7d} "
          f"expo {expo if expo is None else round(expo, 4)} "
          f"cap={capped} wall {wall:.1f}s")
    return out


if __name__ == "__main__":
    print("state:", json.dumps(dict(load=os.getloadavg().__str__(),
                                    t=time.strftime("%H:%M:%S"))))
    run("base", note="pure belt, q=1e-6")
    run("base-s7", seed=7, note="seed variance check of base")
    run("q1e-8", q=1e-8, note="floor sweep")
    run("q1e-9", q=1e-9, note="floor sweep, predicted always-fertile")
    run("cross-p1e-1", nu_p=1e-1, note="planet crossers, 0.1/orbit")
    run("cross-p1e-2", nu_p=1e-2, note="planet crossers, 0.01/orbit")
    run("chaos", lam=0.1, note="compounding errors, 0.1/orbit")
    run("fleet", n0=10**4, n_fleet=10**4, note="co-orbital fleet pocket")
