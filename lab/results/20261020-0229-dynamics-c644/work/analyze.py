#!/usr/bin/env python3
"""Analyze beltewalk flights: the contact e-walk as a first-passage process.

Reads <arm>.snap.tsv / .events.tsv / .global.tsv (+ .head) and prints every number the
dossier cites. All physics in raw lattice units (positions/velocities in 1/Q, Q = 2^20,
MU = 70*2^52); osculating elements are float-derived from the integer state (analysis
only, never canonical).
"""
import json, math, sys
from pathlib import Path

Q = 1 << 20
MU = 70 * (1 << 52)
RP_GATE = 2.1 * Q  # 9b3b's safe-side constant (2.1q strict)
ORBIT_70Q = 7036  # ch, Kepler T at a = 70q

def load(arm):
    import gzip, os
    def op(name):
        p = f"{arm}.{name}"
        if not os.path.exists(p) and os.path.exists(p + ".gz"):
            return gzip.open(p + ".gz", "rt")
        return open(p)
    snaps = {}
    for line in op("snap.tsv"):
        t, bid, ring, ct, cl, x, y, kx, ky = map(int, line.split())
        snaps.setdefault(bid, []).append((t, ring, ct, cl, x, y, kx, ky))
    events = {"D": [], "U": []}
    try:
        for line in op("events.tsv"):
            parts = line.split()
            if len(parts) == 4:
                k, t, bid, ring = parts
                events[k].append((int(t), int(bid), int(ring)))
    except FileNotFoundError:
        pass
    glob = [tuple(map(int, l.split())) for l in op("global.tsv")]
    return snaps, events, glob

def elem(x, y, kx, ky):
    r = math.hypot(x, y)
    v2 = kx * kx + ky * ky
    eps = v2 / 2 - MU / r
    L = x * ky - y * kx
    if eps >= 0:
        return r, v2, None, math.sqrt(max(0.0, 1 + 2 * eps * L * L / (MU * MU))), None
    a = -MU / (2 * eps)
    e = math.sqrt(max(0.0, 1 + 2 * eps * L * L / (MU * MU)))
    return r, v2, a, e, a * (1 - e)

def main(arms):
    out = {}
    for name in arms:
        snaps, ev, gl = load(name)
        rows = {"snaps": len(snaps)}
        # --- global reproduction (e3b7-comparable) ---
        maxk = max(g[9] for g in gl)
        contacts = sum(g[1] for g in gl)
        esc_end = gl[-1][3]
        late = sum(g[1] for g in gl if g[0] > gl[-1][0] - 4096) / 4096
        early = sum(g[1] for g in gl if g[0] <= 4096) / 4096
        rows["global"] = dict(horizon=gl[-1][0], contacts=contacts, maxk=maxk, esc_end=esc_end,
                              ke0=gl[0][7], ke_end=gl[-1][7], n_in_end=gl[-1][4],
                              contacts_per_ch_early=early, contacts_per_ch_late=late)
        deaths = sorted(ev["D"])
        unbound = {b: t for t, b, _ in ev["U"]}
        rows["n_dead"] = len(deaths)
        dtimes = [t for t, _, _ in deaths]
        rows["first_D"] = min(dtimes) if dtimes else None
        rows["first_U"] = min((t for t, _, _ in ev["U"]), default=None)
        # --- P1: chain per dead body ---
        chain = []
        for tD, bid, ring in deaths:
            s = snaps.get(bid, [])
            t_rp = None
            t_cl = None
            e_gen = None
            k2_gen = None
            t_e_half = None
            k2_at_e_half = None
            for (t, rg, ct, cl, x, y, kx, ky) in s:
                r, v2, a, e, rp = elem(x, y, kx, ky)
                if t <= tD:
                    if e_gen is None:
                        e_gen, k2_gen = e, v2
                    if t_cl is None and cl > 0:
                        t_cl = t
                    if a is not None and rp is not None and rp < RP_GATE and t_rp is None:
                        t_rp = t
                    if t_e_half is None and e > 0.5:
                        t_e_half, k2_at_e_half = t, v2
            chain.append(dict(bid=bid, ring=ring, tD=tD, tU=unbound.get(bid), t_rp=t_rp,
                              t_cl=t_cl, t_e_half=t_e_half, k2_ratio=(k2_at_e_half / k2_gen if k2_gen and k2_at_e_half else None)))
        rows["chain"] = chain
        # orderings
        if chain:
            n = len(chain)
            ok_cl_before_U = sum(1 for c in chain if c["t_cl"] is not None and c["tU"] is not None and c["t_cl"] <= c["tU"]) / n
            ok_rp_before_cl = sum(1 for c in chain if c["t_rp"] is not None and c["t_cl"] is not None and c["t_rp"] <= c["t_cl"]) / n
            ok_U_before_D = sum(1 for c in chain if c["tU"] is not None and c["tU"] <= c["tD"]) / n
            ok_e_before_cl = sum(1 for c in chain if c["t_e_half"] is not None and c["t_cl"] is not None and c["t_e_half"] <= c["t_cl"]) / n
            lags = sorted((c["tD"] - c["t_cl"]) for c in chain if c["t_cl"] is not None)
            rows["p1"] = dict(cl_le_U=ok_cl_before_U, rp_le_cl=ok_rp_before_cl, U_le_D=ok_U_before_D,
                              ehalf_le_cl=ok_e_before_cl,
                              med_lag_clamp_to_D=lags[len(lags)//2] if lags else None,
                              n_with_clamp=sum(1 for c in chain if c["t_cl"] is not None))
        # --- P1b: survivors' osculating-energy drift (k2 conflates orbital phase;
        # epsilon and a are the invariants) and the contact correlation of injection ---
        dead_ids = {b for _, b, _ in deaths}
        drift = []      # (ct_end, a_end/a_0 or None, eps0, epsL) for bodies alive at end
        leavers = []    # eps0 for bodies that left (D: crossed r > 250q)
        pass_ct_eps = []
        for bid, s in snaps.items():
            eps0 = a0 = None
            epsL = aL = ctL = None
            for (t, rg, ct, cl, x, y, kx, ky) in s:
                r = math.hypot(x, y)
                eps = (kx * kx + ky * ky) / 2 - MU / r
                if eps < 0:
                    a = -MU / (2 * eps)
                    if eps0 is None:
                        eps0, a0 = eps, a
                    epsL, aL, ctL = eps, a, ct
                else:
                    if eps0 is None:
                        eps0 = eps
                    epsL, aL, ctL = eps, None, ct
            if eps0 is None or epsL is None:
                continue
            if bid in dead_ids:
                # left the r < 250q region; final eps read from its last snapshot
                # (their actual exit energy, not an assumed zero)
                leavers.append(epsL - eps0)
            else:
                drift.append((ctL, (aL / a0 if aL and a0 else None), eps0, epsL))
                pass_ct_eps.append((ctL, epsL / eps0))
        if drift:
            dar = sorted(d[1] for d in drift if d[1] is not None)
            rows["p1b"] = dict(n=len(drift), n_bound_at_end=len(dar), a_med=dar[len(dar)//2], a_p90=dar[int(0.9*len(dar))], a_max=dar[-1],
                               n_clamped_surv=sum(1 for b, s in snaps.items() if b not in dead_ids and any(row[3] > 0 for row in s)))
        # correlation of |deps| with contacts (Spearman by hand on the survivor set)
        if len(pass_ct_eps) > 10:
            xs = [p[0] for p in pass_ct_eps]; ys = [abs(1 - p[1]) for p in pass_ct_eps]
            def rank(v):
                idx = sorted(range(len(v)), key=lambda i: v[i])
                r = [0.0] * len(v)
                i = 0
                while i < len(idx):
                    j = i
                    while j + 1 < len(idx) and v[idx[j+1]] == v[idx[i]]:
                        j += 1
                    for k2 in range(i, j + 1):
                        r[idx[k2]] = (i + j) / 2
                    i = j + 1
                return r
            rx, ry = rank(xs), rank(ys)
            n = len(xs)
            mx, my = sum(rx)/n, sum(ry)/n
            num = sum((a-mx)*(b-my) for a, b in zip(rx, ry))
            den = (sum((a-mx)**2 for a in rx) * sum((b-my)**2 for b in ry)) ** 0.5
            rows["eps_ct_spearman"] = num / den if den else None
        # --- energy ledger: net injected binding energy over the flight (v^2 units).
        # Leavers exit at eps >= 0 (wide-bound D counted as ~0, disclosed approximation);
        # survivors carry epsL. Net = sum|eps0|_leavers + sum(epsL - eps0)_survivors. ---
        if drift or leavers:
            s0 = sum(d[2] for d in drift)
            sL = sum(d[3] for d in drift)
            l0 = sum(leavers)
            net = -l0 + (sL - s0)
            rows["ledger"] = dict(n_leavers=len(leavers), leaver_eps0_sum=-l0,
                                  surv_eps0_sum=s0, surv_epsL_sum=sL,
                                  net_injected=net,
                                  per_contact=net / contacts if contacts else None)
        if len(pass_ct_eps) > 10:
            rows["eps_drift_med"] = sorted(abs(1 - p[1]) for p in pass_ct_eps)[len(pass_ct_eps)//2]
            rows["eps_drift_max"] = max(abs(1 - p[1]) for p in pass_ct_eps)
            xs2 = [p[0] for p in pass_ct_eps]
            rows["ct_med_last"] = sorted(xs2)[len(xs2)//2]
        # --- P2: diffusion before first death ---
        t0 = rows["first_D"] or gl[-1][0]
        pts = []  # (mean_ct, var_e, n)
        de2 = 0.0
        dct = 0
        by_t = {}
        for bid, s in snaps.items():
            prev = None
            for row in s:
                t, rg, ct, cl, x, y, kx, ky = row
                if t > t0:
                    break
                r, v2, a, e, rp = elem(x, y, kx, ky)
                if prev is not None:
                    de2 += (e - prev[0]) ** 2
                    dct += ct - prev[1]
                prev = (e, ct)
                by_t.setdefault(t, []).append((e, ct))
        for t in sorted(by_t):
            es = [e for e, _ in by_t[t]]
            mct = sum(c for _, c in by_t[t]) / len(by_t[t])
            var = sum((e - sum(es)/len(es))**2 for e in es) / len(es)
            pts.append((t, mct, var, len(es)))
        # fit var vs mean_ct
        xs = [p[1] for p in pts]; ys = [p[2] for p in pts]
        if len(xs) > 2 and max(xs) > 0:
            mx, my = sum(xs)/len(xs), sum(ys)/len(ys)
            sxx = sum((x-mx)**2 for x in xs); sxy = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
            slope = sxy / sxx
            ss_res = sum((y - (my + slope*(x-mx)))**2 for x, y in zip(xs, ys))
            ss_tot = sum((y - my)**2 for y in ys)
            r2 = 1 - ss_res/ss_tot if ss_tot else 0
        else:
            slope, r2 = None, None
        rows["p2"] = dict(first_D=t0, points=len(pts), var_slope=slope, r2=r2,
                          De_per_contact=(de2/dct if dct else None), n_dct=dct,
                          var_first=pts[1][2] if len(pts)>1 else None, var_last=pts[-1][2], mct_last=pts[-1][1])
        # --- P3: by ring ---
        ring0 = {bid: s[0][1] for bid, s in snaps.items()}
        ct_early = {}
        for bid, s in snaps.items():
            for row in s:
                if row[0] == 8192:
                    ct_early[bid] = row[2]
                    break
        rings = sorted(set(ring0.values()))
        per_ring = []
        for rg in rings:
            ids = [b for b in ring0 if ring0[b] == rg]
            dth = [t for t, b, r in deaths if r == rg]
            ec = 1 - RP_GATE / (rg * Q)
            per_ring.append(dict(ring=rg, n0=len(ids), deaths=len(dth), ec=ec,
                                 med_ct_8192=sorted(ct_early[b] for b in ids if b in ct_early)[len([b for b in ids if b in ct_early])//2],
                                 med_tD=sorted(dth)[len(dth)//2] if dth else None,
                                 first_tD=min(dth) if dth else None))
        rows["p3"] = per_ring
        # --- P4: survival ---
        if dtimes:
            N0 = len(snaps)
            surv = []
            for t in sorted(dtimes):
                surv.append((t, N0 - sum(1 for x in dtimes if x <= t)))
            # fit ln N vs t on [first_D, first_D + (last-first)]
            import math as m
            t1, t2 = surv[0][0], surv[-1][0]
            pts4 = [(t, n) for t, n in surv if n > 0]
            xs = [p[0] for p in pts4]; ys = [m.log(p[1]) for p in pts4]
            mx, my = sum(xs)/len(xs), sum(ys)/len(ys)
            sxx = sum((x-mx)**2 for x in xs); sxy = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
            lam = -sxy/sxx if sxx else None
            ss_res = sum((y - (my - lam*(x-mx)))**2 for x, y in zip(xs, ys)) if lam else 0
            ss_tot = sum((y - my)**2 for y in ys)
            rows["p4"] = dict(N0=N0, dead=len(dtimes), lam=lam, r2=1-ss_res/ss_tot if ss_tot else 0,
                              half_life=(m.log(2)/lam if lam else None))
        # --- P5: pass control ---
        if "pass" in name:
            cl_tot = sum(row[3] for s in snaps.values() for row in s)
            rows["p5"] = dict(contacts=contacts, clamps=cl_tot, maxk_drift=(maxk - gl[0][9]) / gl[0][9],
                              nU=len(ev["U"]), nD=len(ev["D"]))
        out[name] = rows
    print(json.dumps(out, indent=1, default=str))

if __name__ == "__main__":
    main(sys.argv[1:])
