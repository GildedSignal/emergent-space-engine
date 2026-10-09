"""Second-author run: repair the index so "acceleration only" is true.

Original run 20261009-1936-system-8716 claimed one encounter rule,
    candidate := cone AND wrap(dl0) <= |dn|(1+3 ebar^2) H + 5(e_i+e_j) + skin,
on one U-sorted scan with binned phase windows. The checker (silver) falsified the
shipped INDEX, not the rule: the per-bin window used a linearized drift term
2.4*dU*H/Ubar, i.e. dn proportional to dU only. But n = a^-1.5 = (U(1-e^2))^1.5 has an
e-component: at constant p (constant U), e-spread alone shears pairs, and the index
dropped rule-passing pairs (66/495 true encounters missed on a const-p bimodal-e belt).

The repair (this run): each bin stores the min and max of the occupants' OWN exact
mean motions n = a^-1.5. n is monotone in the body's elements, so
    dn_bound(i, bin) = max(|n_i - nmin_bin|, |n_i - nmax_bin|)
is the EXACT supremum of |dn| over all pairs (i, j in bin) - no linearization, no
constant. The per-bin window becomes
    w = min(TAU, dn_bound*(1+3 eb^2)*H + 5*(e_i + emax_bin) + skin_l),
    eb = max(e_i, emax_bin).
Every factor dominates the rule's per-pair factor (dn_bound >= |dn_ij|,
eb >= ebar_ij, emax_bin >= e_j), so w >= rule sweep for every occupant: the bisect
window can never exclude a rule-passing pair, and emission still applies the full
per-pair rule. Emitted set = naive per-pair rule over all pairs, by construction.
This file carries the proof's measurement: command `equiv` checks set equality
against a vectorized naive rule, old vs new.

Everything else (rule constants incl. the 5(e_i+e_j) chart term, truth sampler,
cone_only, ideal_trigger) is copied verbatim from the original exp.py. The old
unified() is kept verbatim as unified_old to reproduce the checker's finding on
fresh instances of the adversarial class.

Commands (each <= ~80 s on this 8-vCPU runner):
  smoke    dev scene, not registered (tuning only)
  equiv    set equality old/new vs naive + recall on the original scenes and the
           checker's adversarial class (fresh instances)
  equiv3   set equality on the fresh-seed registered scenes
  truth3   recall vs truth on the fresh-seed registered scenes (5-constant a priori)
  sweep2   tightness sweep, fresh seeds, N=512
  scale2   regenerates the fleet-scaling record the original could not:
           N in {512,1024,2048} x e0 in {0.02,0.002}, arc 0.5
  truthres truth-resolution control (T=1024 vs 4096) on a fresh belt
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
    x0 = a * (np.cos(E) - e)
    y0 = a * np.sqrt(1 - e ** 2) * np.sin(E)
    c, s = np.cos(varpi), np.sin(varpi)
    return x0 * c - y0 * s, x0 * s + y0 * c


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

    # ---- truth (verbatim) ---------------------------------------------------------
    def truth(self, T):
        N = self.N
        ts = np.linspace(0, self.H, T, endpoint=False)
        M = self.M0[None, :] + self.n[None, :] * ts[:, None]
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

    # ---- per-pair rule (verbatim) ---------------------------------------------------
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

    # ---- naive rule over ALL pairs, vectorized (same float ops as rule) --------------
    def naive(self):
        i0, i1 = np.triu_indices(self.N, 1)
        dU = np.abs(self.U[i0] - self.U[i1])
        Rij = np.hypot(self.V[i0] - self.V[i1], self.W[i0] - self.W[i1])
        cone = dU <= Rij + self.skin_u
        dn = np.abs(self.n[i0] - self.n[i1])
        ebar = 0.5 * (self.e[i0] + self.e[i1])
        sweep = dn * (1 + 3 * ebar * ebar) * self.H + 5 * (self.e[i0] + self.e[i1]) + self.skin_l
        d = np.abs(self.lam0[i0] - self.lam0[i1]) % TAU
        ok = cone & (np.minimum(d, TAU - d) <= sweep)
        return set(zip(i0[ok].tolist(), i1[ok].tolist()))

    # ---- cone_only (verbatim) --------------------------------------------------------
    def cone_only(self):
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

    # ---- ORIGINAL index, verbatim (the falsified one) --------------------------------
    def unified_old(self):
        N = self.N
        cand, evals, touches = set(), 0, 0
        bw = self.U.mean() * (4 * np.pi / (3 * self.H))
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

    # ---- REPAIRED index: exact |dn| bound from per-bin n extremes ---------------------
    def unified(self):
        """One rule on one structure; the bin window now bounds |dn| exactly.

        dn_bound from the bin occupants' own n = a^-1.5 extremes is the exact sup of
        |dn_ij| over the bin (n monotone in the body's elements), and eb = max(e_i,
        emax_bin) dominates ebar_ij, so w >= rule sweep for every occupant: the window
        is pure acceleration, emission is the per-pair rule."""
        N = self.N
        cand, evals, touches = set(), 0, 0
        bw = self.U.mean() * (4 * np.pi / (3 * self.H))     # slow-band split: perf only
        bwf = bw / 32.0
        bins = {}
        for i in np.argsort(self.U):
            bins.setdefault(int(self.U[i] // bwf), []).append(int(i))
        for v in bins.values():
            v.sort(key=lambda j: self.lam0[j])
        e_arr, n_arr = self.e, self.n
        emax_bin = {k: max(e_arr[vv] for vv in v) for k, v in bins.items()}
        nmin_bin = {k: min(n_arr[vv] for vv in v) for k, v in bins.items()}
        nmax_bin = {k: max(n_arr[vv] for vv in v) for k, v in bins.items()}
        Us = np.sort(self.U)
        usr = np.argsort(self.U)
        posu = np.searchsorted(Us, self.U)
        Rm = float(self.R.max())
        lam, U, e = self.lam0, self.U, self.e
        for i in usr:
            Ui = U[i]
            span = self.R[i] + Rm + 2 * self.skin_u
            inner = min(bw, span)
            b0, b1 = int((Ui - inner) // bwf), int((Ui + inner) // bwf)
            for bk in range(b0, b1 + 1):
                v = bins.get(bk)
                if not v:
                    continue
                # exact sup of |n_i - n_j| over j in bin, from the occupants' own n
                dn_b = max(abs(n_arr[i] - nmin_bin[bk]), abs(n_arr[i] - nmax_bin[bk]))
                eb = max(e[i], emax_bin[bk])
                w = min(TAU, dn_b * (1 + 3 * eb * eb) * self.H
                        + 5 * (e[i] + emax_bin[bk]) + self.skin_l)
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

    # ---- ideal_trigger (verbatim) ------------------------------------------------------
    def ideal_trigger(self, rank=4):
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


def equiv_row(sc, T=1024, with_truth=True):
    nv = sc.naive()
    old, _ = sc.unified_old()
    new, st = sc.unified()
    row = {
        "scene": sc.name, "N": sc.N, "H": sc.H, "naive": len(nv),
        "old_drops": len(nv - old), "old_adds": len(old - nv),
        "new_drops": len(nv - new), "new_adds": len(new - nv),
        "new_evals": st["evals"],
    }
    if with_truth:
        truth = sc.truth(T)
        row["true"] = len(truth)
        row["old_recall"] = round(len(truth & old) / max(1, len(truth)), 6)
        row["new_recall"] = round(len(truth & new) / max(1, len(truth)), 6)
    return row


# ---- scene generators (mk_* verbatim; mk_constp is the checker's adversarial class) ----
def mk_belt(N, b=4e-3, H=8.0, uniform_e=False, seed=1, emin=None, emax=None):
    rng = np.random.default_rng(seed)
    a = rng.uniform(0.8, 1.2, N)
    if emin is not None:
        e = rng.uniform(emin, emax, N)
    elif uniform_e:
        e = rng.uniform(0, 0.2, N)
    else:
        e = np.minimum(rng.rayleigh(0.06, N), 0.15)
    nm = "belt" + ("-hi" if emin is not None else ("-unife" if uniform_e else ""))
    return Scene(nm, a, e, rng.uniform(0, TAU, N), rng.uniform(0, TAU, N), b, H)


def mk_fleet(N, s, b=4e-3, H=8.0, arc=None, base=1.05, seed=2, e0=None):
    rng = np.random.default_rng(seed)
    a = base + s * rng.standard_normal(N)
    e_base = 0.02 if e0 is None else e0
    e = np.abs(e_base + s * 0.05 * rng.standard_normal(N))
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


def mk_constp(N, es, H, b=4e-3, seed=301, p=1.0):
    """Constant-p (identical U): all shear comes from e-spread; dU = 0 exactly."""
    rng = np.random.default_rng(seed)
    e = rng.choice(np.asarray(es), N)
    a = p / (1.0 - e ** 2)
    return Scene(f"constp {es} H={H:g}", a, e,
                 rng.uniform(0, TAU, N), rng.uniform(0, TAU, N), b, H)


METHODS = [
    ("cone-only", lambda sc: sc.cone_only()),
    ("unified", lambda sc: sc.unified()),
    ("ideal-trigger", lambda sc: sc.ideal_trigger()),
]

# Registered fresh-seed scenes (seeds >= 100). Predictions are written against this
# exact list; the 5(e_i+e_j) rule constant is untouched from the original run.
REG = {
    "F1": lambda: mk_fleet(512, 1e-3, arc=0.5, seed=201),
    "F2": lambda: mk_fleet(512, 3e-2, arc=0.5, seed=202),
    "F3": lambda: mk_fleet(512, 0.1, arc=0.5, seed=203),
    "F4": lambda: mk_fleet(512, 1e-3, H=16.0, arc=0.5, seed=204),
    "B1": lambda: mk_belt(768, seed=101),
    "B2": lambda: mk_belt(512, uniform_e=True, seed=102),
    "M1": lambda: mk_mixed(640, 128, seed=103),
    "A1": lambda: mk_constp(512, (0.05, 0.35), 16.0, seed=301),   # checker's killer class
    "A2": lambda: mk_constp(512, (0.0,), 8.0, seed=302),          # replaced below
    "A3": lambda: mk_constp(512, (0.02, 0.2, 0.55), 24.0, seed=303),  # beyond e-domain
    "A4": lambda: mk_belt(256, emin=0.4, emax=0.55, seed=104),    # beyond e-domain
}
REG["A2"] = lambda: mk_constp(512, tuple(np.linspace(0.0, 0.35, 8)), 8.0, seed=302)


def scale_fleet(N, e0, s=1e-3, arc=0.5, seed=401):
    return mk_fleet(N, s, arc=arc, seed=seed, e0=e0)


if __name__ == "__main__":
    cmd = sys.argv[1]
    out = []
    if cmd == "smoke":  # dev only, not registered
        sc = mk_constp(200, (0.02, 0.2, 0.45), 12.0, seed=99)
        out.append(equiv_row(sc, with_truth=True))
    elif cmd == "equiv":  # originals + checker's adversarial class, fresh instances
        for sc in (mk_belt(768, seed=1), mk_mixed(640, 128, seed=3),
                   mk_fleet(512, 1e-3, arc=0.5, seed=2),
                   mk_constp(512, (0.05, 0.35), 16.0, seed=311),
                   mk_constp(512, tuple(np.linspace(0.0, 0.35, 8)), 8.0, seed=312),
                   mk_belt(256, emin=0.4, emax=0.55, seed=1)):
            out.append(equiv_row(sc, with_truth=True))
    elif cmd == "equiv3":  # registered fresh scenes, equality only (no truth)
        for k in ("F1", "F2", "F3", "F4", "B1", "B2", "M1", "A1", "A2", "A3", "A4"):
            out.append(equiv_row(REG[k](), with_truth=False))
    elif cmd == "truth3":  # registered fresh scenes vs truth, 5-constant a priori
        for k in ("F1", "F2", "F3", "F4", "B1", "B2", "M1", "A1", "A2", "A3", "A4"):
            out += report(REG[k](), METHODS)
    elif cmd == "sweep2":
        for m, s in enumerate((1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 0.3)):
            out += report(mk_fleet(512, s, arc=0.5, seed=210 + m), METHODS)
    elif cmd == "scale2":  # regenerates the fleet-scaling record
        for e0 in (0.02, 0.002):
            for N in (512, 1024, 2048):
                sc = scale_fleet(N, e0, seed=401 + N + int(e0 * 1000))
                nv = sc.naive()
                cu, su = sc.cone_only()
                un, sn = sc.unified()
                out.append({
                    "scene": "fleet-scale", "e0": e0, "N": N, "C2": N * (N - 1) // 2,
                    "naive": len(nv), "new_drops": len(nv - un), "new_adds": len(un - nv),
                    "cand_cone": len(cu), "cand_unified": len(un),
                    "frac_unified": round(len(un) / (N * (N - 1) // 2), 4),
                    "frac_cone": round(len(cu) / (N * (N - 1) // 2), 4),
                    "per_body_unified": round(len(un) / N, 2),
                    "evals_cone": su["evals"], "evals_unified": sn["evals"],
                })
    elif cmd == "truthres":  # truth-resolution control, fresh seed
        sc = mk_belt(256, seed=105)
        t1, t4 = sc.truth(1024), sc.truth(4096)
        cand, _ = sc.unified()
        out.append({"scene": "belt256-truthres", "true_T1024": len(t1), "true_T4096": len(t4),
                    "new_pairs_at_T4096": len(t4 - t1),
                    "recall_T4096": round(len(t4 & cand) / max(1, len(t4)), 6)})
    for r in out:
        print(json.dumps(r))
