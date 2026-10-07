#!/usr/bin/env python3
"""Certificate dynamics for the Diophantine encounter tier (run 20261007-1234-dynamics-da90).

Model: two coplanar test particles on Kepler orbits about the primary (AU, yr, mu=4pi^2).
Conjunctions (equal mean longitude) are exactly equally spaced while elements are constant.
Measuring the conjunction longitude u in body 1's apsidal frame, u advances by
2*pi*alpha per conjunction, alpha = n1/(n1-n2) mod 1, INDEPENDENT of linear apsidal
precession (both mean longitudes drift at n+g; in the u frame precession cancels).
Only the RELATIVE apsidal drift g_rel slides the miss-distance pattern D(u; dvarpi)
along u at w_rel turns per conjunction.

Certificate under study (mirrors crates/encounters): integer rotation s_l=(c+l*d) mod m
over the conjunction longitude, a window [lo,hi] covering the bad-longitude set at
RHO_TRIG (superset of RHO_ENC with safety 2), next hit from first_hit (exact, O(log m)).
Policies:
  absorb   d_int = round((alpha - w_rel)*m): the linear window slide is absorbed into
           the rotation (candidate: linear precession costs nothing).
  noabsorb d_int = round(alpha*m), window frozen at grant time (negative control).
  slide-margin: additionally re-grant when |dvarpi| drifts > MARGIN_WPI since grant.
Work counted: one exact check when the certified hit index is reached + first_hit steps.
A truth encounter strictly before the certified hit is a LATE (the window superset failed
to cover it under that policy): the scheduling contract is broken.

Truth: full analytic scan of every conjunction's distance, vectorised per segment;
snaps and kicks break segments. Encounter = conjunction distance < RHO_ENC.
Snaps: per-conjunction phasor dz = SIGMA_Z*exp(i(2u_k+phi)) accumulates; a component
crossing a multiple of QZ applies that quantum to z1 = e1 exp(i varpi1) (influences
below one quantum accumulate). Generic alpha: bounded accumulator; 2*alpha near p/q:
linear drift (coherence). Kicks: exogenous Jupiter-style flyby impulses on body 1.

Configs: generic resonant precession precessionNoM noabsorb snaps kicks
"""
import argparse
import json
import math

import numpy as np

TWO_PI = 2.0 * np.pi
MU = 4.0 * np.pi ** 2
MU_J = MU / 1047.0  # Jupiter
M_ROT = 1 << 32
QZ = 0.01
SIGMA_Z = 2.0e-4
RHO_ENC = 0.01
RHO_TRIG = 0.02
KICK_PERIOD = 400
MARGIN_WPI = 0.15  # rad of relative apsidal drift tolerated before a slide re-grant


def kepler_pos(a, e, varpi, M):
    E = M.copy()
    for _ in range(12):
        E = E - (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    x = a * (np.cos(E) - e)
    y = a * np.sqrt(max(1.0 - e * e, 1e-12)) * np.sin(E)
    n = math.sqrt(MU / a ** 3)
    Edot = n / (1.0 - e * np.cos(E))
    xd = -a * np.sin(E) * Edot
    yd = a * np.sqrt(max(1.0 - e * e, 1e-12)) * np.cos(E) * Edot
    c, s = np.cos(varpi), np.sin(varpi)
    return (x * c - y * s) + 1j * (x * s + y * c), (xd * c - yd * s) + 1j * (xd * s + yd * c)


def _min_k(a, m, l, r, steps):
    steps[0] += 1
    if l == 0:
        return 0
    if a == 0:
        return None
    k = (l + a - 1) // a
    if a * k <= r:
        return k
    y = _min_k(m % a, a, a - r % a, a - l % a, steps)
    return None if y is None else (l + m * y + a - 1) // a


def first_hit(c, d, m, lo, hi):
    """Smallest k>=0 with lo <= (c + d*k) mod m <= hi. Exact integer. Port of dioph.rs."""
    steps = 0
    if lo <= c <= hi:
        return 0, 0
    box = [0]
    l2 = (lo + m - c) % m
    h2 = (hi + m - c) % m
    k = _min_k(d % m, m, l2, h2, box)
    return k, box[0]


def sample_window(a1, e1, a2, e2, dvarpi, n_u=1024):
    """Bad-longitude set {u: D(u;dvarpi) < RHO_TRIG} as integer [lo,hi] in u units."""
    us = np.arange(n_u) * (TWO_PI / n_u)
    p1, _ = kepler_pos(a1, e1, 0.0, us)
    p2, _ = kepler_pos(a2, e2, -dvarpi, us + dvarpi)
    bad = np.abs(p1 - p2) < RHO_TRIG
    idx = np.nonzero(bad)[0]
    if len(idx) == 0:
        return []
    ivals = []
    start = idx[0]
    prev = idx[0]
    for i in idx[1:]:
        if i != prev + 1:
            ivals.append((start, prev))
            start = i
        prev = i
    ivals.append((start, prev))
    if len(ivals) >= 2 and ivals[0][0] == 0 and ivals[-1][1] == n_u - 1:
        lo0 = ivals[0][0]
        hi_last = ivals.pop()[1]
        ivals[0] = (lo0 - n_u, hi_last) if ivals else (lo0 - n_u, hi_last)
    out = []
    for lo, hi in ivals:
        lo_i = int(round(lo * M_ROT / n_u)) % M_ROT
        hi_i = int(round(hi * M_ROT / n_u)) % M_ROT
        if hi_i >= lo_i and hi_i - lo_i >= 2:
            out.append((lo_i, hi_i))
    return out


class Pair:
    def __init__(self, rng, cfg):
        self.cfg = cfg
        e1 = float(rng.uniform(0.05, 0.25))
        a1 = float(rng.uniform(2.3, 2.9))
        e2 = float(rng.uniform(0.05, 0.25))
        for _ in range(300):
            a2 = a1 + float(rng.uniform(0.0, 0.8)) * (e1 + e2) * a1
            if a1 * (1 - e1) < a2 * (1 + e2) and a2 * (1 - e2) > a1 * (1 + e1):
                break
        if cfg == "resonant":
            q = int(rng.integers(7, 65))
            p = int(rng.integers(1, q))
            while math.gcd(p, q) != 1:
                p += 1
                if p >= q:
                    p = 1
            Nturn = int(rng.integers(5, 31))
            eta = float(rng.uniform(0.2, 1.0)) * 0.009 / q  # q*eta within ~one window width
            target = Nturn + p / q + eta  # alpha_full = n1/(n1-n2) = N + p/q + eta
            n1 = TWO_PI * a1 ** -1.5
            n2 = n1 * (1.0 - 1.0 / target)
            a2 = (TWO_PI / n2) ** (2.0 / 3.0)
            e2 = min(0.32, max((abs(a2 - a1) / a1 - e1) * 1.05 + 0.02, 0.05))
        self.a1, self.e1, self.a2, self.e2 = a1, e1, a2, e2
        self.varpi1 = float(rng.uniform(0, TWO_PI))
        self.varpi2 = float(rng.uniform(0, TWO_PI))
        # condition on the orbits actually intersecting: D(u; dvarpi) must dip near zero
        us = np.arange(256) * (TWO_PI / 256)
        for _ in range(60):
            dv = (self.varpi1 - self.varpi2) % TWO_PI
            p1, _ = kepler_pos(self.a1, self.e1, 0.0, us)
            p2, _ = kepler_pos(self.a2, self.e2, -dv, us + dv)
            if float(np.min(np.abs(p1 - p2))) <= 3.0 * RHO_TRIG:
                break
            self.varpi2 = float(rng.uniform(0, TWO_PI))
        self.M1_0 = float(rng.uniform(0, TWO_PI))
        self.M2_0 = float(rng.uniform(0, TWO_PI))
        self.t_ev = 0.0
        self.M1_ev = self.M1_0
        g = 4.4e-4 if cfg in ("precession", "precessionNoM", "noabsorb") else 0.0
        self.g1, self.g2 = g, -0.6 * g
        self.phi_f = float(rng.uniform(0, TWO_PI))
        self.next_kick = int(rng.integers(KICK_PERIOD // 2, 3 * KICK_PERIOD // 2))

    def rates(self):
        n1 = TWO_PI * self.a1 ** -1.5
        n2 = TWO_PI * self.a2 ** -1.5
        T = TWO_PI / (n1 + self.g1 - n2 - self.g2)
        alpha = (n1 / (n1 - n2)) % 1.0
        w_rel = (self.g1 - self.g2) * T / TWO_PI
        return n1, n2, T, alpha, w_rel


def truth(rng, pair, K):
    """Segment-wise analytic truth. Conjunction epochs are re-derived after every event
    (element changes move the conjunction grid). Returns segments, events, encounters."""
    segs = []
    events = []  # (conjunction index, kind)
    encs = []
    k0 = 0
    z_full = 0.0 + 0.0j
    qr, qi = 0, 0
    while k0 < K:
        n1, n2, T, alpha, w_rel = pair.rates()
        # mean longitudes at time t, referenced to the last event (t_ev):
        #   lam1(t) = M1_ev + varpi1 + (n1+g1)(t-t_ev);  lam2(t) = M2_0+varpi2_0 + (n2+g2)t
        t_ev = pair.t_ev
        A = pair.M1_ev + pair.varpi1 - (pair.M2_0 + pair.varpi2) - (n2 + pair.g2) * t_ev
        B = (n1 + pair.g1) - (n2 + pair.g2)
        dt0 = ((-A) % TWO_PI) / B
        klen = min(K - k0, 8192)
        j = np.arange(klen)
        t_k = t_ev + dt0 + j * T
        varpi1_k = pair.varpi1 + pair.g1 * (t_k - t_ev)
        varpi2_k = pair.varpi2 + pair.g2 * t_k
        M1 = (pair.M1_ev + n1 * (t_k - t_ev)) % TWO_PI
        M2 = (pair.M2_0 + n2 * t_k) % TWO_PI
        u_rel = M1  # conjunction longitude in body-1 apsidal frame
        p1, _ = kepler_pos(pair.a1, pair.e1, varpi1_k, M1)
        p2, _ = kepler_pos(pair.a2, pair.e2, varpi2_k, M2)
        dist = np.abs(p1 - p2)
        for i in np.nonzero(dist < RHO_ENC)[0]:
            encs.append(int(k0 + j[i]))
        # sub-quantum accumulation: snap when a component's nearest quantum changes
        end = klen
        snap_at = None
        phas = SIGMA_Z * np.exp(1j * (2.0 * u_rel + pair.phi_f))
        acc = z_full + np.cumsum(phas)
        rr = np.floor(acc.real / QZ + 0.5).astype(np.int64)
        ri = np.floor(acc.imag / QZ + 0.5).astype(np.int64)
        cross = np.nonzero((rr != qr) | (ri != qi))[0]
        if len(cross):
            snap_at = int(cross[0])
            end = min(end, snap_at + 1)
        # exogenous kick
        kick_at = None
        if pair.cfg == "kicks":
            jj = int(np.searchsorted(k0 + j, pair.next_kick))
            if jj < klen:
                kick_at = int(k0 + j[jj])
                end = min(end, jj + 1)
        segs.append({
            "k0": k0, "k1": k0 + end, "u": u_rel[:end].copy(), "dist": dist[:end].copy(),
            "alpha": alpha, "w_rel": w_rel,
            "dvarpi0": float((varpi1_k[0] - varpi2_k[0]) % TWO_PI),
            "grel_T": (pair.g1 - pair.g2) * T,
            "a1": pair.a1, "e1": pair.e1, "a2": pair.a2, "e2": pair.e2,
        })
        if snap_at is not None and k0 + snap_at < segs[-1]["k1"]:
            i = snap_at
            t_e = t_k[i]
            acc_i = z_full + phas[: i + 1].sum()
            newr = int(np.floor(acc_i.real / QZ + 0.5))
            newi = int(np.floor(acc_i.imag / QZ + 0.5))
            dz = complex((newr - qr) * QZ, (newi - qi) * QZ)
            znew = pair.e1 * np.exp(1j * pair.varpi1) + dz
            pair.e1 = float(min(abs(znew), 0.35))
            pair.varpi1 = float(np.angle(znew)) % TWO_PI
            z_full = acc_i
            qr, qi = newr, newi
            pair.M1_ev = float(M1[i])
            pair.t_ev = float(t_e)
            events.append((k0 + i, "snap"))
            k0 = k0 + i + 1
            continue
        if kick_at is not None and k0 + end - 1 == kick_at:
            i = end - 1
            t_e = t_k[i]
            b = float(rng.uniform(0.15, 1.5))
            psi = float(rng.uniform(0, TWO_PI))
            dv = 2.0 * MU_J / (b * 1.2)
            v1m = max(float(np.abs(
                kepler_pos(pair.a1, pair.e1, pair.varpi1, np.array([M1[i]]))[1][0])), 0.5)
            da_a = 2.0 * dv * math.cos(psi) / v1m
            pair.a1 *= 1.0 + da_a
            de = 1.5 * dv * math.cos(psi) / v1m
            znew = pair.e1 * np.exp(1j * pair.varpi1) + de * np.exp(1j * psi)
            pair.e1 = float(min(abs(znew), 0.35))
            pair.varpi1 = float(np.angle(znew)) % TWO_PI
            pair.M1_ev = float(M1[i])
            pair.t_ev = float(t_e)
            events.append((kick_at, "kick"))
            pair.next_kick += int(rng.integers(KICK_PERIOD // 2, 3 * KICK_PERIOD // 2))
            k0 = kick_at + 1
            continue
        k0 += end
    return segs, events, encs

def replay(segs, events, encs, policy, K):
    """Walk the truth under one certificate policy. Returns counters."""
    absorb = policy in ("absorb", "noM", "driftwin")
    use_margin = policy not in ("noM", "driftwin")
    ev = sorted(events + [(e, "enc") for e in encs])
    seg_of = sorted((s["k0"], s["k1"], s) for s in segs)

    def seg(k):
        for k0, k1, s in seg_of:
            if k0 <= k < k1:
                return s
        return seg_of[-1][2]

    def dist_at(k):
        s = seg(k)
        return float(s["dist"][k - s["k0"]])

    def u_at(k):
        s = seg(k)
        return float(s["u"][k - s["k0"]])

    r = {"grants": 0, "touches": 0, "hits": 0, "late": 0, "fh_steps": 0,
         "fh": [], "why": {"hit": 0, "cont": 0, "snap": 0, "kick": 0, "slide": 0,
                           "enc_regrant": 0, "eager": 0}}
    k = 0
    while k < K:
        s = seg(k)
        if "w" not in s:
            s["w"] = sample_window(s["a1"], s["e1"], s["a2"], s["e2"], s["dvarpi0"])
        ivals = s["w"]
        alpha_eff = (s["alpha"] - (s["w_rel"] if absorb else 0.0)) % 1.0
        d_int = int(round(alpha_eff * M_ROT)) % M_ROT
        c_int = int(round((u_at(k) / TWO_PI % 1.0) * M_ROT)) % M_ROT
        k_best, st = None, 0
        for lo, hi in ivals:
            kh, stp = first_hit(c_int, d_int, M_ROT, lo, hi)
            if kh is not None and (k_best is None or kh < k_best):
                k_best, st = kh, stp
        if policy == "driftwin" and k_best is not None and s["grel_T"] != 0.0:
            # drift-inclusive window: widen by the total relative drift over the span
            widen = int(round(abs(s["grel_T"]) * k_best / TWO_PI * M_ROT))
            k_best, st = None, 0
            for lo, hi in ivals:
                l2, h2 = (lo - widen) % M_ROT, (hi + widen) % M_ROT
                if l2 <= h2:
                    kh, stp = first_hit(c_int, d_int, M_ROT, l2, h2)
                    if kh is not None and (k_best is None or kh < k_best):
                        k_best, st = kh, stp
        r["grants"] += 1
        r["fh_steps"] += st
        if k_best is None:
            r["why"]["cont"] += 1
            break  # rotation never enters the window: permanent certificate
        if k_best == 0:
            k_hit = k  # hit now: check, advance, re-grant
        else:
            k_hit = min(k + k_best, K - 1)
        r["fh"].append(k_best)
        # earliest invalidator strictly after k, before k_hit
        best = None
        for idx, kind in ev:
            if k < idx < k_hit:
                best = (idx, kind)
                break
        if best is not None:
            idx, kind = best
            if kind == "enc":
                r["late"] += 1
                r["touches"] += 1
                r["hits"] += 1
                r["why"]["enc_regrant"] += 1
                k = idx + 1
                continue
            r["why"][kind] += 1
            k = idx + 1
            continue
        # slide-margin (curvature guard): the linear slide is absorbed into d_int;
        # the margin guards the change of D's SHAPE with dvarpi over the certified span
        if use_margin and s["grel_T"] != 0.0:
            drift = abs(s["grel_T"]) * (min(k_hit, K - 1) - s["k0"])
            if drift > MARGIN_WPI:
                r["why"]["slide"] += 1
                k = max(k_hit, k + 1)
                continue
        r["touches"] += 1
        if dist_at(k_hit) < RHO_ENC:
            r["hits"] += 1
            r["why"]["hit"] += 1
        else:
            r["why"]["cont"] += 1
        k = k_hit + 1
    return r


def fuzz_first_hit(rng, n=300):
    """Instrument control: port matches brute force."""
    for _ in range(n):
        m = int(rng.integers(2, 5000))
        c = int(rng.integers(0, m))
        d = int(rng.integers(0, m))
        w = int(rng.integers(0, m))
        lo = int(rng.integers(0, m))
        hi = min(m - 1, lo + w)
        k, _ = first_hit(c, d, m, lo, hi)
        brute = None
        s = c % m
        for i in range(m + 1):
            if lo <= s <= hi:
                brute = i
                break
            s = (s + d) % m
        if k != brute:
            return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--pairs", type=int, default=500)
    ap.add_argument("--K", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--policy", default="absorb")
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    ok = fuzz_first_hit(rng)
    tot = {"grants": 0, "touches": 0, "hits": 0, "late": 0, "fh_steps": 0,
           "encounters": 0, "snaps": 0, "kicks": 0, "amax": 0.0, "spacing": [],
           "fh": [], "alphas": [], "snap_alpha_d": [], "w_rel": []}
    for _ in range(args.pairs):
        pair = Pair(rng, args.config)
        segs, events, encs = truth(rng, pair, args.K)
        r = replay(segs, events, encs, args.policy, args.K)
        tot["grants"] += r["grants"]
        tot["touches"] += r["touches"]
        tot["hits"] += r["hits"]
        tot["late"] += r["late"]
        tot["fh_steps"] += r["fh_steps"]
        tot["fh"].extend(r["fh"][:60])
        tot["encounters"] += len(encs)
        tot["snaps"] += sum(1 for _, kd in events if kd == "snap")
        tot["kicks"] += sum(1 for _, kd in events if kd == "kick")
        for i in range(1, len(encs)):
            tot["spacing"].append(encs[i] - encs[i - 1])
        a = pair.rates()[3]
        tot["alphas"].append(a)
        tot["w_rel"].append(pair.rates()[4])
        if any(kd == "snap" for _, kd in events):
            tot["snap_alpha_d"].append(min(
                ((a * q - round(a * q)) * q) for q in range(2, 129)))
    fh = np.array(tot.pop("fh")) if tot["fh"] else np.array([0])
    sp = np.array(tot.pop("spacing")) if tot["spacing"] else np.array([0])
    alphas = np.array(tot.pop("alphas"))
    sd = np.array(tot.pop("snap_alpha_d")) if tot["snap_alpha_d"] else np.array([])
    w_rel = np.array(tot.pop("w_rel"))
    res = dict(tot)
    res.update({
        "config": args.config, "policy": args.policy, "pairs": args.pairs, "K": args.K,
        "fuzz_ok": bool(ok), "work_ratio": tot["touches"] / (args.pairs * args.K),
        "fh_median": float(np.median(fh)), "fh_mean": float(np.mean(fh)),
        "spacing_median": float(np.median(sp)),
        "grants_per_pair": tot["grants"] / args.pairs,
        "regrants_per_snap": (tot["grants"] / max(tot["snaps"], 1)) if tot["snaps"] else None,
        "snaps_per_pair": tot["snaps"] / args.pairs,
        "kicks_per_pair": tot["kicks"] / args.pairs,
        "snap_alpha_d_median": float(np.median(sd)) if len(sd) else None,
        "w_rel_max": float(np.max(np.abs(w_rel))),
    })
    best = np.ones(len(alphas))
    for q in range(2, 65):
        p = np.round(alphas * q)
        best = np.minimum(best, np.abs(alphas - p / q) * q * q)
    res["res_frac_q2_64_eps3"] = float(np.mean(best < 3.0))
    print(json.dumps(res))


if __name__ == "__main__":
    main()
