"""One candidate structure for encounters: one U-sorted scan + one continuous phase rule.

Claim under test: the Binet-cone tier (belts) and the phase-rank certificate (fleets) are
one rule on one structure, with no concentration trigger:

    candidate(pair) := cone(pair) AND  wrap_dist(lam0_i, lam0_j) <= sweep(pair)
    sweep(pair)     := |n_i - n_j| (1 + 3 ebar^2) H + 3 (e_i + e_j) + skin_l

Physics of the bound: Delta lambda(t) = Delta lambda(0) + Delta n t + [2 e_i sin M_i -
2 e_j sin M_j] + O(e^2); the bracket is a bounded oscillation (amplitude <= 2(e_i+e_j),
no secular part in Kepler), so over [0, H] the reachable set of Delta lambda is a window
of half-width |Delta n| H + 2(e_i+e_j), inflated by chart safety (x1.5 -> 3(e_i+e_j),
+3 ebar^2 on the drift). Conjunction requires Delta lambda(t) = 0 at a crossing longitude,
hence the rule. Fast shear (|Delta n| H >= pi) makes the window the whole circle: the rule
degenerates to the cone alone (belt pairs). Slow shear (fleet) keeps only phase-near
pairs: rank-like pruning emerges from the formula; there is no fleet category anywhere.

cone(pair): exact coplanar Kepler intersection |dU| <= sqrt(dV^2 + dW^2), inflated by
skin_u = 2 b U^2 so pairs that pass within b without crossing survive.

Index (acceleration only; the emitted set equals the naive per-pair rule over all
radial-overlap pairs): bodies sorted by U. The slow band (|dU| <= bw, bw chosen so
|dn| H <= 2 pi inside) is covered by fine U-bins (bw/32) whose occupants are sorted by
lambda; each bin is queried with its own window w_bin = min(TAU, 2.4 d_bin H / Ubar +
3 (e_i + e_max_bin) + skin_l). Beyond the slow band the scan continues outward in U while
radial overlap is possible, applying the same per-pair rule. A kick re-cells one body.

Element conventions: u(theta) = U + V cos(theta) + W sin(theta), U = 1/p,
V = e cos(varpi)/p, W = e sin(varpi)/p, phase = true longitude lambda(0), n = a^-1.5.
"""
import bisect
import json
import sys

import numpy as np

TAU = 2 * np.pi


def lam0_to_M0(e, varpi, lam0):
    f = lam0 - varpi
    E = 2 * np.arctan2(np.sqrt(1 - e) * np.sin(f / 2), np.sqrt(1 + e) * np.cos(f / 2))
    return (E - e * np.sin(E)) % TAU


def positions(a, e, varpi, M0, t):
    n = a ** -1.5
    M = M0 + n * t
    E = M.copy()
    for _ in range(6):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    x = a * (np.cos(E) - e)
    y = a * np.sqrt(1 - e ** 2) * np.sin(E)
    c, s = np.cos(varpi), np.sin(varpi)
    return x * c - y * s, x * s + y * c


class Scene:
    def __init__(self, name, a, e, varpi, lam0, b, H):
        self.name, self.N, self.b, self.H = name, len(a), b, H
        self.fleet = np.zeros(len(a), dtype=bool)
        self.a, self.e, self.varpi = a, e, varpi
        self.lam0 = lam0 % TAU
        self.n = a ** -1.5
        self.M0 = lam0_to_M0(e, varpi, lam0)
        p = a * (1 - e ** 2)
        self.U, self.V, self.W = 1.0 / p, e * np.cos(varpi) / p, e * np.sin(varpi) / p
        self.R = np.hypot(self.V, self.W)
        Um = self.U.mean()
        self.skin_u = 2 * b * Um ** 2
        self.skin_l = 2 * b * Um + 0.02
        self.lo = self.U - self.R - self.skin_u
        self.hi = self.U + self.R + self.skin_u
    # ---- truth -----------------------------------------------------------------
    def truth(self, T):
        """Pairs whose sampled min distance < b over [0,H]. Fully vectorised over (t, body)."""
        N = self.N
        ts = np.linspace(0, self.H, T, endpoint=False)
        M = self.M0[None, :] + self.n[None, :] * ts[:, None]        # (T,N)
        E = M.copy()
        for _ in range(6):
            E = E - (E - self.e[None, :] * np.sin(E) - M) / (1 - self.e[None, :] * np.cos(E))
        x0 = self.a * (np.cos(E) - self.e[None, :])
        y0 = self.a * np.sqrt(1 - self.e[None, :] ** 2) * np.sin(E)
        c, s = np.cos(self.varpi)[None, :], np.sin(self.varpi)[None, :]
        X, Y = x0 * c - y0 * s, x0 * s + y0 * c
        best = np.full((N, N), np.inf)
        for k in range(T):
            d = np.hypot(X[k, :, None] - X[k, None, :], Y[k, :, None] - Y[k, None, :])
            np.minimum(best, d, out=best)
        iu = np.triu_indices(N, 1)
        hit = best[iu] < self.b
        return set(zip(iu[0][hit].tolist(), iu[1][hit].tolist()))

    # ---- per-pair rule -----------------------------------------------------------
    def rule(self, i, j):
        dU = abs(self.U[i] - self.U[j])
        Rij = np.hypot(self.V[i] - self.V[j], self.W[i] - self.W[j])
        if dU > Rij + self.skin_u:
            return False
        dn = abs(self.n[i] - self.n[j])
        ebar = 0.5 * (self.e[i] + self.e[j])
        sweep = dn * (1 + 3 * ebar * ebar) * self.H + 5 * (self.e[i] + self.e[j]) + self.skin_l
        d = abs(self.lam0[i] - self.lam0[j]) % TAU
        return min(d, TAU - d) <= sweep

    # ---- methods ------------------------------------------------------------------
    def cone_only(self):
        """r8 v2's element-sort tier: all radial-overlap pairs, cone filter, any phase."""
        order = np.argsort(self.lo)
        cand, evals, touches = set(), 0, 0
        lo, hi = self.lo, self.hi
        for k in range(self.N):
            i = order[k]
            for m in range(k + 1, self.N):
                j = order[m]
                if lo[j] > hi[i]:
                    break
                touches += 1
                evals += 1
                dU = abs(self.U[i] - self.U[j])
                Rij = np.hypot(self.V[i] - self.V[j], self.W[i] - self.W[j])
                if dU <= Rij + self.skin_u:
                    cand.add((i, j) if i < j else (j, i))
        return cand, {"evals": evals, "touches": touches}

    def unified(self):
        """One rule on one structure: U order + binned slow band with per-bin phase windows."""
        N = self.N
        cand, evals, touches = set(), 0, 0
        bw = self.U.mean() * (4 * np.pi / (3 * self.H))     # |dn| H <= 2 pi inside
        bwf = bw / 32.0
        bins = {}
        for i in np.argsort(self.U):
            bins.setdefault(int(self.U[i] // bwf), []).append(int(i))
        for v in bins.values():
            v.sort(key=lambda j: self.lam0[j])
        emax_bin = {k: max(self.e[vv] for vv in v) for k, v in bins.items()}
        umin_bin = {k: min(self.U[vv] for vv in v) for k, v in bins.items()}
        umax_bin = {k: max(self.U[vv] for vv in v) for k, v in bins.items()}
        Us = np.sort(self.U)
        usr = np.argsort(self.U)
        posu = np.searchsorted(Us, self.U)
        Rm = float(self.R.max())
        Um = self.U.mean()
        lam, U, e = self.lam0, self.U, self.e
        for i in usr:
            Ui = U[i]
            span = self.R[i] + Rm + 2 * self.skin_u
            inner = min(bw, span)
            # slow band via bins: per-bin window from the occupants' real U extent
            b0, b1 = int((Ui - inner) // bwf), int((Ui + inner) // bwf)
            for bk in range(b0, b1 + 1):
                v = bins.get(bk)
                if not v:
                    continue
                d_bin = max(abs(umax_bin[bk] - Ui), abs(umin_bin[bk] - Ui))
                w = min(TAU, 2.4 * d_bin * self.H / Um + 5 * (e[i] + emax_bin[bk]) + self.skin_l)
                lo_l, hi_l = lam[i] - w, lam[i] + w
                for rng in ((lo_l, hi_l), (lo_l + TAU, hi_l + TAU), (lo_l - TAU, hi_l - TAU)):
                    a, b = rng
                    if b < 0 or a > TAU:
                        continue
                    l0 = bisect.bisect_left(v, max(0.0, a), key=lambda j: lam[j])
                    l1 = bisect.bisect_right(v, min(TAU, b), key=lambda j: lam[j])
                    for j in v[l0:l1]:
                        if j <= i:
                            continue
                        touches += 1
                        evals += 1
                        if self.lo[i] > self.hi[j] or self.lo[j] > self.hi[i]:
                            continue
                        if self.rule(i, j):
                            cand.add((i, j))
            # outer scan: U order, skip the slow band, radial-overlap bounded
            p = posu[i]
            for direction in (-1, 1):
                m = p + direction
                while 0 <= m < N:
                    j = usr[m]
                    if direction * (U[j] - Ui) > span:
                        break
                    if direction * (U[j] - Ui) > inner:
                        touches += 1
                        evals += 1
                        if not (self.lo[i] > self.hi[j] or self.lo[j] > self.hi[i]) \
                           and self.rule(i, j):
                            cand.add((i, j) if i < j else (j, i))
                    m += direction
        return cand, {"evals": evals, "touches": touches}

    def ideal_trigger(self, rank=4):
        """The repaired design: cone tier outside the oracle fleet, lambda-rank inside it."""
        cand, evals, touches = set(), 0, 0
        order = np.argsort(self.lo)
        lo, hi = self.lo, self.hi
        for k in range(self.N):
            i = order[k]
            for m in range(k + 1, self.N):
                j = order[m]
                if lo[j] > hi[i]:
                    break
                if self.fleet[i] and self.fleet[j]:
                    continue
                touches += 1
                evals += 1
                dU = abs(self.U[i] - self.U[j])
                Rij = np.hypot(self.V[i] - self.V[j], self.W[i] - self.W[j])
                if dU <= Rij + self.skin_u:
                    cand.add((i, j) if i < j else (j, i))
        fl = np.where(self.fleet)[0]
        fl = fl[np.argsort(self.lam0[fl])]
        for k, i in enumerate(fl):
            for j in fl[max(0, k - rank):k + rank + 1]:
                if j <= i:
                    continue
                touches += 1
                evals += 1
                cand.add((i, j))
        return cand, {"evals": evals, "touches": touches}


def report(sc, methods, T=1024):
    truth = sc.truth(T)
    rows = []
    for name, fn in methods:
        cand, st = fn(sc)
        inter = len(truth & cand)
        rows.append({
            "scene": sc.name, "method": name, "N": sc.N, "b": sc.b, "H": sc.H,
            "true": len(truth), "cand": len(cand),
            "recall": round(inter / max(1, len(truth)), 6),
            "evals": st["evals"], "touches": st["touches"],
            "evals_per_true": round(st["evals"] / max(1, len(truth)), 2),
            "cand_per_true": round(len(cand) / max(1, len(truth)), 2),
        })
    return rows


def mk_belt(N, b=4e-3, H=8.0, uniform_e=False, seed=1):
    rng = np.random.default_rng(seed)
    a = rng.uniform(0.8, 1.2, N)
    e = rng.uniform(0, 0.2, N) if uniform_e else np.minimum(rng.rayleigh(0.06, N), 0.15)
    return Scene("belt" + ("-unife" if uniform_e else ""), a, e,
                 rng.uniform(0, TAU, N), rng.uniform(0, TAU, N), b, H)


def mk_fleet(N, s, b=4e-3, H=8.0, arc=None, base=1.05, seed=2):
    rng = np.random.default_rng(seed)
    a = base + s * rng.standard_normal(N)
    e = np.abs(0.02 + s * 0.05 * rng.standard_normal(N))
    varpi = 0.7 + s * rng.standard_normal(N)
    lam = rng.uniform(0, TAU, N) if arc is None else 0.9 + rng.uniform(-arc / 2, arc / 2, N)
    sc = Scene(f"fleet s={s:g}", a, e, varpi, lam, b, H)
    sc.fleet[:] = True
    return sc


def mk_mixed(Nb, Nf, s=1e-3, b=4e-3, H=8.0, seed=3):
    rng = np.random.default_rng(seed)
    a = np.concatenate([rng.uniform(0.8, 1.2, Nb), 1.05 + s * rng.standard_normal(Nf)])
    e = np.concatenate([np.minimum(rng.rayleigh(0.06, Nb), 0.15),
                        np.abs(0.02 + s * 0.05 * rng.standard_normal(Nf))])
    varpi = rng.uniform(0, TAU, Nb + Nf)
    varpi[Nb:] = 0.7 + s * rng.standard_normal(Nf)
    lam = rng.uniform(0, TAU, Nb + Nf)
    lam[Nb:] = 0.9 + rng.uniform(-0.25, 0.25, Nf)
    sc = Scene("mixed", a, e, varpi, lam, b, H)
    sc.fleet[Nb:] = True
    return sc


METHODS = [
    ("cone-only", lambda sc: sc.cone_only()),
    
    ("unified", lambda sc: sc.unified()),
    ("ideal-trigger", lambda sc: sc.ideal_trigger()),
]

if __name__ == "__main__":
    cmd = sys.argv[1]
    out = []
    if cmd in ("truth1", "truth2"):
        scenes = ([mk_fleet(512, 1e-3, arc=0.5), mk_fleet(512, 0.1, arc=0.5),
                   mk_belt(768)] if cmd == "truth1" else
                  [mk_mixed(640, 128), mk_fleet(512, 3e-2, arc=0.5),
                   mk_belt(768, uniform_e=True), mk_fleet(512, 1e-3, H=16.0, arc=0.5)])
        for sc in scenes:
            out += report(sc, METHODS)
    elif cmd == "sweep":
        for s in (1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 0.3):
            out += report(mk_fleet(768, s, arc=0.5), METHODS)
    elif cmd == "scale":
        for N in (2500, 10000):
            for sc in (mk_belt(N, seed=10), mk_mixed(N - N // 10, N // 10, seed=11)):
                for name, fn in METHODS:
                    cand, st = fn(sc)
                    out.append({"scene": sc.name, "method": name, "N": sc.N,
                                "cand": len(cand), **st})
    for r in out:
        print(json.dumps(r))
