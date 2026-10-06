"""B12 red-team: today's statistic and the recurrence ratio on planted/reference error series.

Data: probe/out/<kind>.f64, shape (16, 1601, 9): t, x, y, vx, vy, r2, a/sep, e, C.
Ports fit.rs::growth_exponent, handoff.rs::b12 (median/floor/cap) and the draft
recurrence_ratio probe in handoff.rs's tests, plus my variants.
"""
import numpy as np

MU, SEP, PR = 1e-3, 5.27e8, 4.84e4
HILL = SEP * (MU / 3) ** (1 / 3)
SOI = SEP * MU ** 0.4
PERIOD = 2 * np.pi * SEP ** 1.5
COARSE, PERIODS = 8, 200
NS = PERIODS * COARSE + 1
FLOOR, ERRMAX, GROWMAX = 1e-12, 1e-4, 0.2
UNIT = HILL / SEP
J = np.arange(NS)
TP = J / COARSE  # time in planet periods


def load(kind):
    return np.fromfile(f"probe/out/{kind}.f64").reshape(16, NS, 9)


def growth_exponent(err):
    err = np.abs(np.asarray(err, float))
    n = len(err)
    first = max(n // 10, 1)
    if n <= first or not np.isfinite(err).all():
        return np.nan
    W = 16
    edge = [n if j == W else int(round(first * (n / first) ** (j / W))) for j in range(W + 1)]
    pts, used = [], 0
    for j in range(W):
        a, b = edge[j], edge[j + 1]
        if b <= a:
            continue
        used += 1
        top = err[a:b].max()
        if top > 0:
            pts.append((np.log(np.sqrt(a * (b - 1))), np.log(top)))
    if used < W // 2:
        return np.nan
    if not pts:
        return 0.0
    if len(pts) < 3:
        return np.nan
    p = np.array(pts)
    return np.polyfit(p[:, 0], p[:, 1], 1)[0]


def median_inf(xs):
    xs = [np.inf if np.isnan(x) else x for x in xs]
    return float(np.median(xs))


def gate(errs, name=""):
    """errs: (16, NS) |error| series. Returns (pass, detail)."""
    errs = np.asarray(errs)
    exps, worst = [], 0.0
    for e in errs:
        top = np.nanmax(e) if np.isfinite(e).any() else np.nan
        worst = max(worst, top) if np.isfinite(top) else np.nan
        if not (top <= FLOOR):  # NaN is not under the floor
            exps.append(growth_exponent(e))
    med = median_inf(exps) if exps else 0.0
    ok = (not np.isnan(worst)) and worst <= ERRMAX and med <= GROWMAX
    return ok, f"{name:22s} gate {'PASS' if ok else 'FAIL'}  median exponent {med:6.3f}  worst err {worst:.2e}  above floor {len(exps)}/16"


def recurrence(err_signed, a_sep, ecc, r2, aw=0.02, ew=0.05, near=(2.0, 8.0), far=(64.0, 200.1), q=0.9):
    near_d, far_d = [], []
    for s in range(16):
        es = err_signed[s]
        mask = (r2[s] > 3 * HILL) & np.isfinite(es)
        cells = {}
        for j in np.where(mask)[0]:
            cells.setdefault((int(np.floor(a_sep[s, j] / aw)), int(np.floor(ecc[s, j] / ew))), []).append((TP[j], es[j]))
        for v in cells.values():
            m = len(v)
            for x in range(m):
                tx, ex_ = v[x]
                for y in range(x):
                    dt = abs(tx - v[y][0])
                    d = abs(ex_ - v[y][1])
                    if near[0] <= dt <= near[1]:
                        near_d.append(d)
                    elif far[0] <= dt <= far[1]:
                        far_d.append(d)
    if not near_d or not far_d:
        return np.nan, len(near_d), len(far_d)
    def pq(v, q):
        v = sorted(v)
        i = min(int(q * len(v)), len(v) - 1)
        return max(v[i], FLOOR)
    return pq(far_d, q) / pq(near_d, q), len(near_d), len(far_d)


# ---------- plants ----------
class SplitMix:
    def __init__(self, seed):
        self.s = seed & 0xFFFFFFFFFFFFFFFF
    def next(self):
        self.s = (self.s + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
        z = self.s
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
        return z ^ (z >> 31)
    def unit(self):
        return (self.next() >> 11) / float(1 << 53)


def ship_seed(ship):
    h = 0x5EED
    for x in ship:
        x = np.float64(x)
        h = ((((h << 17) & 0xFFFFFFFFFFFFFFFF) | (h >> 47)) ^ int(x.view(np.uint64))) & 0xFFFFFFFFFFFFFFFF
    return h


def plants(d, rng_extra=0):
    """d: loaded kind (16,NS,9). Returns dict name -> signed err (16,NS)."""
    a, e, r2 = d[:, :, 6], d[:, :, 7], d[:, :, 5]
    out = {}
    tile = lambda v: np.broadcast_to(np.asarray(v, float), (16, NS)).copy()
    a0, e0 = a[:, :1], e[:, :1]
    u = np.minimum(HILL / r2, 5.0); u0 = u[:, :1]
    out["bounded-a"] = -1e-7 * (np.minimum(a, 10.0) - a0) / UNIT
    out["bounded-e"] = -1e-7 * (e - e0) / 0.01
    out["bounded-r2"] = -1e-7 * (u - u0)
    out["drift"] = tile(-1e-9 * J)
    out["leak"] = tile(-1e-12 * TP)
    out["periodic"] = tile(-1e-7 * np.sin(2 * np.pi * TP / 100.0))
    out["noise-11"] = None  # filled with numpy rng below
    out["walk-13"] = None
    out["walk-12"] = None
    # compound/saturating/plane-jump: seeded per ship like laws.rs plant_compound
    comp = np.zeros((16, NS)); sat = np.zeros((16, NS)); jump = np.zeros((16, NS))
    for s in range(16):
        rng = SplitMix(ship_seed(d[s, 0, 1:5].tolist()))
        inside = False
        acc = 0.0
        cum = []
        walks13, walks12 = [], []
        a13 = a12 = 0.0
        accj = 0.0
        for j in range(NS):
            now = r2[s, j] < 3 * HILL
            if now and not inside:
                acc += (rng.unit() - 0.5) * np.sqrt(12.0)
                a13 += (rng.unit() - 0.5) * np.sqrt(12.0) * 1e-6
                a12 += (rng.unit() - 0.5) * np.sqrt(12.0) * 1e-5
                accj += np.random.default_rng(1000 * s + j).normal(1e-6, 5.4e-6)
            inside = now
            comp[s, j] = 1e-7 * acc
            sat[s, j] = 3e-7 * np.tanh(acc / 30.0)
            jump[s, j] = accj
            walks13.append(a13 * 1e-6); walks12.append(a12 * 1e-6)
        # scale walks so final sizes are ~1.4e-12 and ~1.4e-11 rms-ish (raw above is 1e-6*unit steps)
    out["compound"] = comp
    out["saturating"] = sat
    out["plane-jump"] = jump
    # pure-noise and tiny walks at fixed levels
    g = np.random.default_rng(7 + rng_extra)
    out["noise-11"] = g.normal(0, 1e-11, (16, NS))
    w13 = np.cumsum(g.normal(0, 1, (16, NS)), axis=1); out["walk-13"] = 3e-12 * w13 / np.sqrt(NS)
    w12 = np.cumsum(g.normal(0, 1, (16, NS)), axis=1); out["walk-12"] = 3e-11 * w12 / np.sqrt(NS)
    return out


def main():
    print("== exponent port sanity ==")
    for alpha in (0.0, 0.5, 1.0):
        g = growth_exponent(1e-9 * np.maximum(np.arange(10000), 1) ** alpha)
        assert abs(g - alpha) < 1e-3, (alpha, g)
    print("power laws 0/0.5/1 recovered")
    r13, r12, r11 = load("r13"), load("r12"), load("r11")
    a, e, r2 = r13[:, :, 6], r13[:, :, 7], r13[:, :, 5]
    C0 = r13[:, 0:1, 8]

    print("== reference sanity ==")
    conv = np.abs(r12[:, :, 8] - r13[:, :, 8]) / np.abs(C0)
    print(f"r12-vs-r13 C agreement: median {np.median(conv):.2e}  max {conv.max():.2e}  (gate converged<=1e-9)")
    for nm, rr in [("r11", r11), ("r12", r12), ("r13", r13)]:
        ce = np.abs(rr[:, 0:1, 8] - rr[:, :, 8]) / np.abs(C0)
        print(*gate(ce, f"reference {nm}"), sep="\n  ")
        rat = recurrence((rr[:, :, 8] - C0) / np.abs(C0), rr[:, :, 6], rr[:, :, 7], rr[:, :, 5])
        print(f"  recurrence ratio {rat[0]:.3f} (near {rat[1]} far {rat[2]} pairs)")

    print("\n== plants (on r13 trajectories) ==")
    P = plants(r13)
    rows = []
    for nm, es in P.items():
        g = gate(np.abs(es), nm)
        rat = recurrence(es, a, e, r2)
        rows.append((nm, g[1], rat))
        print(g[1])
        print(f"  recurrence ratio {rat[0]:.3f} (near {rat[1]} far {rat[2]} pairs)")

    print("\n== one-ulp ensemble (plants on nudged trajectories, exponent/ratio spread) ==")
    for kind in ["nxp", "nxm", "nvxp", "nvyp"]:
        d = load(kind)
        dd = plants(d)
        ce = (d[:, :, 8] - d[:, 0:1, 8]) / np.abs(d[:, 0:1, 8])
        ex_b = [growth_exponent(np.abs(dd["bounded-a"][s])) for s in range(16)]
        ex_c = [growth_exponent(np.abs(dd["compound"][s])) for s in range(16)]
        rb = recurrence(dd["bounded-a"], d[:, :, 6], d[:, :, 7], d[:, :, 5])[0]
        rc = recurrence(dd["compound"], d[:, :, 6], d[:, :, 7], d[:, :, 5])[0]
        mr = recurrence(ce, d[:, :, 6], d[:, :, 7], d[:, :, 5])[0]
        print(f"{kind}: bounded-a exp median {median_inf(ex_b):.3f} ratio {rb:.2f} | compound exp median {median_inf(ex_c):.3f} ratio {rc:.2f} | ref-r12 exp median {median_inf([growth_exponent(np.abs(ce[s])) for s in range(16)]):.3f} ratio {mr:.2f}")

    print("\n== sensitivity of the ratio (r13 plants) ==")
    for nm in ["bounded-a", "compound", "plane-jump", "periodic", "noise-11"]:
        line = f"{nm:12s}"
        for aw, ew in [(0.01, 0.025), (0.02, 0.05), (0.04, 0.1)]:
            r = recurrence(P[nm], a, e, r2, aw=aw, ew=ew)[0]
            line += f"  cells({aw}/{ew}): {r:6.2f}"
        for near, far in [((1.0, 4.0), (32.0, 200.1)), ((2.0, 8.0), (64.0, 200.1)), ((4.0, 16.0), (64.0, 200.1))]:
            r = recurrence(P[nm], a, e, r2, near=near, far=far)[0]
            line += f"  win({near[0]:.0f}-{near[1]:.0f}/{far[0]:.0f}+): {r:6.2f}"
        rq = recurrence(P[nm], a, e, r2, q=0.5)[0]
        line += f"  median: {rq:6.2f}"
        print(line)

    print("\n== fate: closest approach under one-ulp nudges (planet radii) ==")
    for kind in ["r12", "nxp", "nxm", "nvxp", "nvyp"]:
        meta = dict(l.split()[1:4:2] for l in open(f"probe/out/{kind}_meta.txt").read().strip().split("\n"))
        cl = np.array([float(meta[str(s)]) for s in range(16)])
        print(f"{kind}: " + " ".join(f"{c:7.3f}" for c in cl))


if __name__ == "__main__":
    main()
