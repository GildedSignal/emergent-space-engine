#!/usr/bin/env python3
"""Tail analysis for the remnant's fate past 49k (run 3b67).

Reads the beltewalk flights' .global.tsv / .events.tsv / .snap.tsv and reports:
  prefix reproduction against c644 (positive control),
  hazard windows and tail fit, remnant/core structure at 49k vs end,
  per-ring death flux early vs tail, late-death residency (P4), ke_in growth (P5),
  standing contacts/ch cost.

Usage: analyze_tail.py FLIGHT_DIR [REF_DEAD PREFIX_CONTACTS]  (ref defaults: 492/63,461,214)
"""
import json
import math
import sys
from collections import defaultdict

Q = 1 << 20
MU = 70 * (1 << 52)
H_SPLIT = 49152  # c644 horizon: prefix must reproduce


def load_global(d):
    t, c, esc, n_in, ke_in = [], [], [], [], []
    for line in open(f"{d}.global.tsv"):
        f = line.split()
        t.append(int(f[0])); c.append(int(f[1])); esc.append(int(f[3]))
        n_in.append(int(f[4])); ke_in.append(int(f[6]))
    return t, c, esc, n_in, ke_in


def load_events(d):
    U, D = [], []
    for line in open(f"{d}.events.tsv"):
        k, t, bid, ring = line.split()
        (U if k == "U" else D).append((int(t), int(bid), int(ring)))
    return U, D


def load_snaps(d):
    """snap rows: t id ring ct cl x y kx ky -> {t: {id: (ring, ct, x, y, kx, ky)}}"""
    snaps = defaultdict(dict)
    with open(f"{d}.snap.tsv") as fh:
        for line in fh:
            f = line.split()
            t, bid = int(f[0]), int(f[1])
            snaps[t][bid] = (int(f[2]), int(f[3]), int(f[4]), int(f[5]), int(f[6]), int(f[7]))
    return snaps


def rq(x, y):
    return math.hypot(x, y) / Q


def analyze(d, ref_dead, ref_contacts):
    t, c, esc, n_in, ke_in = load_global(d)
    U, D = load_events(d)
    H = t[-1]
    out = {"dir": d, "horizon": H}

    # -- positive control: prefix reproduction --------------------------------
    pre_c = sum(x for x, tt in zip(c, t) if tt <= H_SPLIT)
    pre_d = [x for x in D if x[0] <= H_SPLIT]
    out["prefix"] = {
        "contacts": pre_c, "contacts_ref": ref_contacts,
        "dead": len(pre_d), "dead_ref": ref_dead,
        "reproduces": abs(pre_c - ref_contacts) <= ref_contacts // 100
        and abs(len(pre_d) - ref_dead) <= max(1, ref_dead // 100),
    }

    # -- hazard windows --------------------------------------------------------
    dead_ts = [x[0] for x in D]
    alive = [800]
    for tt in t:
        alive.append(alive[-1] - (1 if tt in dead_ts else 0))
    alive = alive[1:]  # alive[i] = alive after chronon t[i]
    win = 8192
    windows = []
    for w0 in range(0, H, win):
        idx = [i for i, tt in enumerate(t) if w0 < tt <= w0 + win]
        if not idx:
            continue
        dths = sum(1 for td in dead_ts if w0 < td <= w0 + win)
        a0, a1 = alive[idx[0]], alive[idx[-1]]
        mean_alive = 0.5 * (a0 + a1)
        haz = dths / (mean_alive * len(idx)) if mean_alive > 0 else 0.0
        windows.append({
            "w": [w0 + 1, w0 + win], "deaths": dths, "alive_end": a1,
            "hazard_e5": round(haz * 1e5, 3),
            "contacts_per_ch": round(sum(c[i] for i in idx) / len(idx), 1),
            "n_in_end": n_in[idx[-1]],
        })
    out["windows"] = windows

    # -- tail fit: ln N vs t on (H_SPLIT, H] ----------------------------------
    tail_idx = [i for i, tt in enumerate(t) if tt > H_SPLIT]
    xs = [t[i] for i in tail_idx]
    ys = [math.log(alive[i]) for i in tail_idx]
    nx = len(xs)
    if nx > 2 and len(set(ys)) > 2:
        mx, my = sum(xs) / nx, sum(ys) / nx
        sxx = sum((x - mx) ** 2 for x in xs)
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        slope = sxy / sxx
        ss_res = sum((y - (my + slope * (x - mx))) ** 2 for x, y in zip(xs, ys))
        ss_tot = sum((y - my) ** 2 for y in ys)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 1.0
    else:
        slope, r2 = 0.0, 1.0
    out["tail_fit"] = {"lam_e5": round(-slope * 1e5, 3), "r2": round(r2, 4),
                       "deaths_tail": len(D) - len(pre_d),
                       "halflife_ch": round(math.log(2) / -slope) if slope < 0 else None}

    # -- remnant/core structure from snapshots --------------------------------
    snaps = load_snaps(d)
    def structure(ts):
        rows = snaps.get(ts)
        if not rows:
            return None
        rs = {bid: rq(v[2], v[3]) for bid, v in rows.items()}
        cts = {bid: v[1] for bid, v in rows.items()}
        dead_by = {b for (td, b, _) in D if td <= ts}
        live = [bid for bid in rows if bid not in dead_by]
        zones = {"lt2.1q": 0, "lt10q": 0, "lt30q": 0, "lt140q": 0}
        for bid in live:
            r = rs[bid]
            for k, lim in (("lt2.1q", 2.1), ("lt10q", 10), ("lt30q", 30), ("lt140q", 140)):
                if r < lim:
                    zones[k] += 1
        core = [rs[bid] for bid in live if rs[bid] < 30]
        rms_core = math.sqrt(sum(r * r for r in core) / len(core)) if core else None
        return {
            "t": ts, "alive": len(live), "zones": zones,
            "rms_core_lt30q": round(rms_core, 2) if rms_core else None,
            "median_r_live": round(sorted(rs[b] for b in live)[len(live) // 2], 2),
        }
    out["structure"] = {str(ts): structure(ts) for ts in
                        [H_SPLIT, (H_SPLIT + H) // 2, H] if structure(ts)}

    # per-body contact rate in the last stride interval (per body per ch)
    last_ts = sorted(snaps)[-1]
    prev_ts = sorted(snaps)[-2]
    rates = []
    for bid, v in snaps[last_ts].items():
        if bid in snaps[prev_ts]:
            rates.append((v[1] - snaps[prev_ts][bid][1]) / (last_ts - prev_ts))
    rates.sort()
    out["late_ct_per_body_ch"] = {
        "median": round(rates[len(rates) // 2], 3),
        "p90": round(rates[int(0.9 * len(rates))], 3),
        "max": round(rates[-1], 3),
    }

    # -- P4: late-death residency ---------------------------------------------
    late_D = [(td, bid, ring) for td, bid, ring in D if td > H_SPLIT]
    resid = []
    snaps_ts = sorted(snaps)
    for td, bid, ring in late_D:
        radii = [rq(snaps[ts][bid][2], snaps[ts][bid][3]) for ts in snaps_ts
                 if H_SPLIT < ts < td and bid in snaps[ts]]
        if radii:
            resid.append(sorted(radii)[len(radii) // 2])
    out["late_deaths"] = {
        "n": len(late_D),
        "median_med_r_q": round(sorted(resid)[len(resid) // 2], 2) if resid else None,
        "frac_core_lt30q": round(sum(1 for r in resid if r < 30) / len(resid), 3) if resid else None,
        "frac_core_lt10q": round(sum(1 for r in resid if r < 10) / len(resid), 3) if resid else None,
        "rings": {str(r): sum(1 for _, _, rg in late_D if rg == r) for r in sorted({rg for _, _, rg in late_D})},
    }

    # -- P5: ke_in growth -------------------------------------------------------
    ke_49 = ke_in[t.index(H_SPLIT)]
    ke_end = ke_in[-1]
    out["ke_in"] = {"at49k": ke_49, "at_end": ke_end, "ratio": round(ke_end / max(1, ke_49), 4)}

    # -- per-ring death flux, early vs tail (c644 leftover) ---------------------
    ring0 = {}
    for _, _, ring in D:
        ring0[ring] = ring0.get(ring, 0) + 1
    early_rings = defaultdict(int)
    for td, _, ring in D:
        if td <= H_SPLIT:
            early_rings[ring] += 1
    tail_rings = defaultdict(int)
    for td, _, ring in D:
        if td > H_SPLIT:
            tail_rings[ring] += 1
    out["ring_flux"] = {
        "early": {str(r): early_rings[r] for r in sorted(early_rings)},
        "tail": {str(r): tail_rings[r] for r in sorted(tail_rings)},
    }

    # -- standing cost ----------------------------------------------------------
    out["standing"] = {
        "contacts_tail_total": sum(c[i] for i in tail_idx),
        "tail_ch": len(tail_idx),
        "mean_ct_ch_last8k": round(sum(x for x, tt in zip(c, t) if tt > H - 8192) / min(8192, H), 1),
    }
    return out


if __name__ == "__main__":
    d = sys.argv[1]
    ref_dead = int(sys.argv[2]) if len(sys.argv) > 2 else 492
    ref_contacts = int(sys.argv[3]) if len(sys.argv) > 3 else 63461214
    print(json.dumps(analyze(d, ref_dead, ref_contacts), indent=1))
