#!/usr/bin/env python3
"""H_live probe: scar bits per body per game-time, on the law's own storage grids.

Model (pre-registered in predictions.md):
- Kepler conjunction MC per neighbour pair (Binet-cone crossing condition: |da| <= e1+e2+rho).
- At each conjunction, sample common true anomaly theta ~ U(0, 2pi):
    dr  = | a1 - a2 - a1 e1 cos(th-w1) + a2 e2 cos(th-w2) |   (first order in e)
    vr  = e1 sin(th-w1) - e2 sin(th-w2);  vt = 0.5*(a1-a2)    (units v_k = 1, GM = a = 1)
    v_rel = sqrt(vr^2 + vt^2)
  Encounter iff dr < rho. Impact parameter b = rho*sqrt(u), u~U(0,1) (uniform in area).
- Gravity impulse: dv = 2*mu/(b*v_rel); each body takes +-dv*cos(phi), phi~U (tangential part
  -> da; radial part -> dphase). Contacts: b < R_c -> dv = v_rel (elastic, order 1).
- Principle 6: sub-quantum influences accumulate (a per-body accumulator); a quantum lands
  on the integer offset only when |acc| >= q.
- Two grids: q_cert = rho/a (what the encounter certificate resolves);
  q_doll  = (a/a_min)*2^-32 with a_min = 0.05 (the 32-bit (E,L) memo-key grid of the doll).
- Bits: Elias-delta per non-zero field, F = 2 fields (da, dphase), + 2 bits presence.
- Program refit every R_refit orbits: subtract the collective mean offset (exact, integer);
  the program's own sigma growth is O(bits) per population, negligible per body.
Validation: a direct time-stepped belt (no conjunction logic) checks the MC's encounter rate.
"""
import json, math, sys
import numpy as np

RNG = np.random.default_rng(20261008)
V_K = 1.0  # orbital speed at a=1, GM=1


def elias_delta_bits(x):
    """Elias delta code length for positive integer x (0 -> 0)."""
    bits = np.zeros_like(x, dtype=np.float64)
    m = x > 0
    xn = x[m]
    n = np.floor(np.log2(xn)).astype(np.int64) + 1      # length in binary
    ln = np.floor(np.log2(n)).astype(np.int64) + 1      # length of the length
    bits[m] = n + ln - 1.0
    return bits


def sample_scene(name, N, awidth, sigma_e, rho, mu, Rc, Torb):
    a = 1.0 + awidth * RNG.random(N)
    e = RNG.rayleigh(sigma_e, N)
    w = 2 * np.pi * RNG.random(N)
    # neighbour pairs by Binet-cone crossing condition
    order = np.argsort(a)
    a_s, e_s, w_s = a[order], e[order], w[order]
    lo = np.searchsorted(a_s, a_s - (e_s + e_s + rho), side="left")
    hi = np.searchsorted(a_s, a_s + (e_s + e_s + rho), side="right")
    ii, jj = [], []
    for k in range(N):
        if hi[k] - lo[k] > 1:
            m = np.arange(lo[k] + 1, hi[k])
            ii.append(np.full(len(m), k)); jj.append(m)
    if not ii:
        return dict(scene=name, pairs=0, enc_rate=0.0)
    i = np.concatenate(ii); j = np.concatenate(jj)
    da = a_s[j] - a_s[i]
    # synodic conjunctions per orbit (n = a^-1.5): f = |n_j - n_i| / 2pi ~ 1.5*da/2pi
    f = np.abs(a_s[j] ** -1.5 - a_s[i] ** -1.5) / (2 * np.pi)
    lam = f * Torb                                   # expected conjunctions per pair
    nc = RNG.poisson(lam)
    tot = nc.sum()
    if tot == 0:
        return dict(scene=name, pairs=len(i), conj=0, enc_rate=0.0)
    # sample conjunction events (pair index repeated)
    pid = np.repeat(np.arange(len(i)), nc)
    th = 2 * np.pi * RNG.random(tot)
    r1 = a_s[i[pid]] * (1 - e_s[i[pid]] * np.cos(th - w_s[i[pid]]))
    r2 = a_s[j[pid]] * (1 - e_s[j[pid]] * np.cos(th - w_s[j[pid]]))
    dr = np.abs(r1 - r2)
    vr = e_s[i[pid]] * np.sin(th - w_s[i[pid]]) - e_s[j[pid]] * np.sin(th - w_s[j[pid]])
    vt = 0.5 * (a_s[j[pid]] - a_s[i[pid]])
    vrel = np.sqrt(vr * vr + vt * vt) + 1e-12
    enc = dr < rho
    ne = int(enc.sum())
    out = dict(scene=name, pairs=int(len(i)), conj=int(tot), enc=int(ne),
               enc_rate=ne / (N * Torb))
    if ne == 0:
        out.update(kick_da_med=0.0, contacts=0)
        return out
    u = RNG.random(ne)
    b = rho * np.sqrt(u)
    dv_grav = 2 * mu / (b * vrel[enc])
    contact = b < Rc
    dv = np.where(contact, vrel[enc], dv_grav)        # contact: elastic order-1
    phi = 2 * np.pi * RNG.random(ne)
    d_tan = dv * np.cos(phi)                          # -> da (per conjunction, split 1/2 each)
    out.update(kick_da_med=float(np.median(d_tan)), contacts=int(contact.sum()),
               kick_da_p90=float(np.quantile(d_tan, 0.9)))

    def accumulate(q, refit):
        acc = np.zeros(N); off = np.zeros(N, dtype=np.int64)
        offs_hist = []
        ev = np.concatenate([i[pid][enc], j[pid][enc]])
        half = np.concatenate([d_tan * 0.5, -d_tan * 0.5])
        # event times uniform over the run; refits happen at even orbital marks
        t_ev = RNG.random(2 * ne) * Torb
        o = np.argsort(t_ev)
        ev, half = ev[o], half[o]
        t_ev = t_ev[o]
        marks = np.linspace(0, Torb, int(Torb / refit) + 1)[1:]
        mi = 0
        for tk in marks:
            sel = (t_ev < tk) & (t_ev >= (marks[mi - 1] if mi else 0))
            np.add.at(acc, ev[sel], half[sel])
            landed = np.trunc(acc / q).astype(np.int64)
            off += landed
            acc -= landed * q
            # program refit: choose the centre (0, mean, median) by exact stored bits,
            # as the design chooses program-vs-packed form by exact byte count
            best, bits_best = off, np.inf
            for c in (0, int(np.trunc(off.mean())), int(np.median(off))):
                cand = off - c
                bb = elias_delta_bits(cand).sum()
                if bb < bits_best:
                    bits_best, best = bb, cand
            off = best
            offs_hist.append(off.copy())
            mi += 1
        sel = t_ev >= marks[-1] if len(marks) else slice(None)
        np.add.at(acc, ev[sel], half[sel])
        landed = np.trunc(acc / q).astype(np.int64)
        off += landed
        return off, offs_hist

    out_q = {}
    for gname, q in (("cert", rho), ("doll", 20 * 2.0 ** -32)):
        off, hist = accumulate(q, refit=10.0)
        out_q[gname] = dict(
            bits_per_body=float(elias_delta_bits(off).sum() * 2 / N + 2 * (off != 0).mean()),
            touched=float((off != 0).mean()),
            max_off=int(np.abs(off).max()),
            bits_hist=[float(elias_delta_bits(h).sum() * 2 / N + 2 * (h != 0).mean()) for h in hist],
        )
    out["grids"] = out_q
    return out

def fleet_scene(name, N, awidth, sigma_e, rho, mu, Rc, Torb, K=200_000):
    """Co-orbital fleet: all pairs cross, so sample K of the ~N^2/2 pairs (rates are
    intensive: each sampled pair carries weight (N*(N-1)/2)/K)."""
    a = 1.0 + awidth * RNG.random(N)
    e = RNG.rayleigh(sigma_e, N)
    w = 2 * np.pi * RNG.random(N)
    i = RNG.integers(0, N, K); j = RNG.integers(0, N, K)
    m = i != j
    i, j = i[m], j[m]
    f = np.abs(a[j] ** -1.5 - a[i] ** -1.5) / (2 * np.pi)
    nc = RNG.poisson(f * Torb)
    tot = int(nc.sum())
    out = dict(scene=name, pairs=int(N * (N - 1) / 2), sampled=len(i), conj=tot)
    lam_prox = (N - 1) * rho / np.pi                  # expected neighbours within along-track rho
    out["proximity_fraction"] = float(1 - math.exp(-lam_prox))
    if tot == 0:
        out.update(enc_rate=0.0, contacts=0, kick_da_med=0.0, grids={})
        return out
    pid = np.repeat(np.arange(len(i)), nc)
    th = 2 * np.pi * RNG.random(tot)
    dr = np.abs(a[i[pid]] - a[j[pid]]
                - a[i[pid]] * e[i[pid]] * np.cos(th - w[i[pid]])
                + a[j[pid]] * e[j[pid]] * np.cos(th - w[j[pid]]))
    enc = dr < rho
    ne = int(enc.sum())
    out["enc"] = ne
    out["enc_rate"] = ne * (N * (N - 1) / 2) / len(i) / (N * Torb)
    if ne == 0:
        out.update(contacts=0, kick_da_med=0.0, grids={})
        return out
    vr = e[i[pid][enc]] * np.sin(th[enc] - w[i[pid][enc]]) - e[j[pid][enc]] * np.sin(th[enc] - w[j[pid][enc]])
    vrel = np.sqrt(vr * vr) + 1e-12
    b = rho * np.sqrt(RNG.random(ne))
    dv = 2 * mu / (b * vrel)
    contact = b < Rc
    dv = np.where(contact, vrel, dv)
    out["contacts"] = int(contact.sum())
    out["kick_da_med"] = float(np.median(dv))
    out["grids"] = {}
    return out



def validate_rate(N=1500, awidth=0.5, sigma_e=1e-2, rho=1e-4, Torb=8.0, steps_per_orbit=350):
    """Direct time-stepped belt: no conjunction logic; count distance minima below rho."""
    a = 1.0 + awidth * RNG.random(N)
    e = RNG.rayleigh(sigma_e, N)
    w = 2 * np.pi * RNG.random(N)
    M0 = 2 * np.pi * RNG.random(N)
    dt = 1.0 / steps_per_orbit
    order = np.argsort(a)
    a_s = a[order]
    e_s = e[order]
    lo = np.searchsorted(a_s, a_s - (e_s + e_s + 2 * rho), side="left")
    hi = np.searchsorted(a_s, a_s + (e_s + e_s + 2 * rho), side="right")
    ii, jj = [], []
    for k in range(N):
        if hi[k] - lo[k] > 1:
            m = np.arange(lo[k] + 1, hi[k])
            m = m[m != k]                      # never pair a body with itself
            if len(m):
                ii.append(np.full(len(m), k)); jj.append(m)
    i = np.concatenate(ii); j = np.concatenate(jj)
    n = a_s ** -1.5
    enc = 0
    prev_close = np.zeros(len(i), bool)
    nsteps = int(Torb / dt)
    for s in range(nsteps):
        t = s * dt
        M1 = (M0[order][i] + n[i] * t) % (2 * np.pi)
        M2 = (M0[order][j] + n[j] * t) % (2 * np.pi)
        # near-circular positions (first order in e)
        r1 = a_s[i] * (1 - e[order][i] * np.cos(M1 - w[order][i]))
        r2 = a_s[j] * (1 - e[order][j] * np.cos(M2 - w[order][j]))
        az1 = M1 + 2 * e[order][i] * np.sin(M1)
        az2 = M2 + 2 * e[order][j] * np.sin(M2)
        daz = (az1 - az2 + np.pi) % (2 * np.pi) - np.pi   # wrap to [-pi, pi]
        d2 = (r1 - r2) ** 2 + (0.5 * (r1 + r2) * daz) ** 2
        close = d2 < rho * rho
        newly = close & ~prev_close
        enc += int(newly.sum())
        prev_close = close
    return enc / (N * Torb)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "main"
    if mode == "validate":
        r = validate_rate()
        print(json.dumps(dict(direct_rate_per_body_orbit=r), indent=1))
        sys.exit(0)
    scenes = [
        ("belt0_r8",      10_000, 0.5, 1e-2, 1e-4, 1e-10, 1e-8,  100.0),
        ("belt0_rho3e-4", 10_000, 0.5, 1e-2, 3e-4, 1e-10, 1e-8,  100.0),
        ("belt_hot",      10_000, 0.5, 1e-1, 1e-4, 1e-10, 1e-8,  100.0),
        ("belt_shipmass", 10_000, 0.5, 1e-2, 1e-4, 5e-25, 6.7e-10, 100.0),
        ("fleet_tight",   200_000, 1e-6, 1e-7, 1e-4, 5e-25, 6.7e-10, 100.0),
    ]
    res = []
    for sc in scenes:
        fn = fleet_scene if sc[0].startswith("fleet") else sample_scene
        r = fn(*sc)
        res.append(r)
        print(json.dumps(r, default=float)[:600], flush=True)
    with open("h_live_results.json", "w") as f:
        json.dump(res, f, indent=1, default=float)
    print("saved h_live_results.json")
