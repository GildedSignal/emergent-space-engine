#!/usr/bin/env python3
"""Decisive pass: realized (a,e) via apoapsis tracking + E,L conservation."""
import json, math, time
import run as R

def orbit_full(rhs, s0, norbits, spo, Mt, r_start, ev=None):
    T_orb = 2 * math.pi * math.sqrt(r_start ** 3 / Mt)
    h = T_orb / spo
    s = list(s0)
    rs = []
    for _ in range(norbits * spo):
        k1 = rhs(s)
        s2 = [s[j] + 0.5 * h * k1[j] for j in range(4)]
        k2 = rhs(s2)
        s3 = [s[j] + 0.5 * h * k2[j] for j in range(4)]
        k3 = rhs(s3)
        s4 = [s[j] + h * k3[j] for j in range(4)]
        k4 = rhs(s4)
        s = [s[j] + h / 6 * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j]) for j in range(4)]
        rs.append((math.hypot(s[0], s[1]), math.atan2(s[1], s[0]), s))
    peris = []; apos = []
    for i in range(1, len(rs) - 1):
        r0, a0, _ = rs[i - 1]; r1, a1, _ = rs[i]; r2, a2, _ = rs[i + 1]
        if r1 < r0 and r1 <= r2: peris.append((r1, a1, rs[i][2]))
        if r1 > r0 and r1 >= r2: apos.append((r1, a1, rs[i][2]))
    def slope(pts):
        raw = [p[1] for p in pts]
        un = [raw[0]]
        for i in range(1, len(raw)):
            d = (raw[i] - raw[i - 1] + math.pi) % (2 * math.pi) - math.pi
            un.append(un[i - 1] + d)
        import numpy as np
        idx = np.arange(len(un), dtype=float)
        A = np.vstack([idx, np.ones_like(idx)]).T
        sl, _ = np.linalg.lstsq(A, np.array(un), rcond=None)[0]
        return float(sl)
    rmin = min(p[0] for p in peris); rmax = max(p[0] for p in apos)
    out = dict(slope_peri=slope(peris), slope_apo=slope(apos),
               rmin=rmin, rmax=rmax, n_peri=len(peris), n_apo=len(apos))
    if ev is not None:
        # E and L conservation for the river law (static field => both conserved)
        E0 = L0 = None; dE = dL = 0.0
        for _, _, st in rs[::7]:
            X, Y, px, py = st
            (bx, by), _, _ = ev.query(X, Y)
            E = math.sqrt(1 + px * px + py * py) + bx * px + by * py
            L = X * py - Y * px
            if E0 is None: E0, L0 = E, L
            dE = max(dE, abs(E - E0)); dL = max(dL, abs(L - L0))
        out["dE_max"] = dE; out["dL_max"] = dL
    return out

if __name__ == "__main__":
    res = {}
    for name, masses in [("A", [(0.015, -0.75, 0.0), (0.015, 0.75, 0.0)])]:
        f = R.Field(masses)
        t0 = time.time()
        ths, tab = R.build_table(f)
        ev = R.RiverEval(f, ths, tab)
        print("table", round(time.time() - t0, 1), flush=True)
        v0 = R.v_newtonian(f.Mt)
        s0 = R.start_state_river(R.RP, v0, ev.query(R.RP, 0.0)[0])
        t0 = time.time()
        res["river"] = orbit_full(R.river_rhs_factory(ev), s0, 20, 120, f.Mt, R.RP, ev=ev)
        print("river orbit", round(time.time() - t0, 1), res["river"], flush=True)
        res["newtonian"] = orbit_full(R.newtonian_rhs_factory(f),
                                      R.start_state(R.RP, v0), 20, 240, f.Mt, R.RP)
    json.dump(res, open("results-decisive.json", "w"), indent=1, default=float)
    print(json.dumps(res, indent=1, default=float))
