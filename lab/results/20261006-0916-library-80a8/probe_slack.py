#!/usr/bin/env python3
"""Probe: what should trigger the rebuild of a phase-neighbour encounter certificate?

Belt: N bodies, a in [0.9,1.1] AU, Rayleigh e (sigma 0.05, cap 0.25), random periapsis w and
phase M. Truth pair set: |da| <= 0.08 AU at t0 (orbits can overlap). Conjunctions detected
exactly each sub-step. Surprise source: Poisson kicks per body (lambda 2/orbit), each
+/-1 quantum on (a,e,w): q_a=1e-4 AU, q_e=1e-3, q_w=1e-2 rad. Nothing else changes.

Certificate: body i owns certs for its k=4 phase-nearest partners (circular M distance among
a-compatible), built at i's rebuild. A cert predicts crossings at Th + k*T_syn (T_syn from dn
at build; the design's continued-fraction roll-forward). At a close conjunction (2-D distance
< TAU) a cert CATCHES iff its k-nearest predicted crossing is within
w = w0 + |dn_now - dn_cert| * (t - Tc) / |dn_cert|   of the event time.
Cost: cert_builds = 4 * body_rebuilds + renewals (one per predicted crossing passed; only
counted at close events, so B/C costs are UNDER-counted -- conservative against D).

Policies (identical kick and event streams):
  A        : rebuild at every kick (per-change)
  B<m>     : rebuild when the body's own kicks since its rebuild reach m (quantum slack)
  C<R>     : rebuild every R years (cadence), R matched to B16's rebuild count
  D        : rebuild when a shear deadline (|dn|*(t-Tc) > ETA) fires, or own kicks reach 32
  nokick   : lambda=0 with B8 (control)
"""
import numpy as np, heapq, math, json

TAU_CLOSE = 0.01; W0 = 0.25; K = 4; ETA = math.pi / 2; M_D = 32
ORBITS = 60.0; SO = 60; DT = 1.0 / SO; NSTEPS = int(ORBITS * SO)

def init(seed):
    r = np.random.default_rng(seed)
    N = 400
    a = r.uniform(0.9, 1.1, N)
    e = np.minimum(r.rayleigh(0.05, N), 0.25)
    w = r.uniform(0, 2 * np.pi, N)
    M = r.uniform(0, 2 * np.pi, N)
    n = 2 * np.pi * a ** (-1.5)
    ii, jj = np.triu_indices(N, 1)
    m = np.abs(a[ii] - a[jj]) <= 0.08
    ii, jj = ii[m], jj[m]
    cand = [np.flatnonzero(np.abs(a - a[i]) <= 0.08) for i in range(N)]
    cand = [c[c != i] for i, c in enumerate(cand)]
    return r, N, a, e, w, M, n, ii, jj, cand

CAND_G = None  # set by run()

class Pol:
    def __init__(self, name, mode, m=0, R=0.0, eta=ETA):
        self.name, self.mode, self.m, self.R = name, mode, m, R
        self.eta = eta
        self.Tc = -np.ones((400, 400)); self.Th = np.zeros((400, 400)); self.Dn = np.zeros((400, 400))
        self.own = np.full((400, K), -1, np.int32)
        self.Kr = np.zeros(400, np.int64); self.rebuilds = 0; self.renewals = 0
        self.miss = self.struct = self.stale = 0; self.heap = []

    def rebuild(self, i, t, Mc, A, Nc, Kk):
        self.rebuilds += 1
        c = CAND_G[i]
        d = np.abs(Mc[c] - Mc[i]); d = np.minimum(d, 2 * np.pi - d)
        take = c[np.argpartition(d, min(K, len(c) - 1))[:K]]
        for j in self.own[i]:
            if j >= 0: self.Tc[i, j] = -1.0
        self.own[i] = take
        for j in take:
            dn = Nc[i] - Nc[j]
            phi = (Mc[i] - Mc[j]) % (2 * np.pi)
            dt_hat = ((2 * np.pi - phi) if dn > 0 else phi) / abs(dn) if dn != 0 else 1e9
            self.Tc[i, j] = t; self.Th[i, j] = t + dt_hat; self.Dn[i, j] = dn
            if self.mode == "disp":
                heapq.heappush(self.heap, (t + self.eta / max(abs(dn), 1e-9), i))
            elif self.mode == "cad":
                heapq.heappush(self.heap, (t + self.R, i))
        self.Kr[i] = Kk[i]

    def caught(self, i, j, t, Nc):
        for x, y in ((i, j), (j, i)):
            tc = self.Tc[x, y]
            if tc > 0:
                dn = self.Dn[x, y]; T = 2 * np.pi / abs(dn) if dn != 0 else 1e9
                kk = round((t - self.Th[x, y]) / T)
                self.renewals += max(0, kk)
                err = abs(t - (self.Th[x, y] + kk * T))
                wl = W0 + abs((Nc[i] - Nc[j]) - dn) * (t - tc) / max(abs(dn), 1e-9)
                if err <= wl:
                    return True
        return False

def run(pols, lam, seed):
    global CAND_G
    r, N, A, E, W, Mc, Nc, ii, jj, cand = init(seed)
    CAND_G = cand
    Kk = np.zeros(N, np.int64)
    for p in pols:
        p.__init__(p.name, p.mode, p.m, p.R, p.eta)
        for i in range(N): p.rebuild(i, 0.0, Mc, A, Nc, Kk)
    phi_prev = (Mc[ii] - Mc[jj]) % (2 * np.pi)
    close_events = 0; quanta = []
    for step in range(NSTEPS):
        t = step * DT; te = t + DT
        Mc = (Mc + Nc * DT) % (2 * np.pi)
        phi = (Mc[ii] - Mc[jj]) % (2 * np.pi)
        cross = np.where(np.abs(phi - phi_prev) > np.pi)[0]
        for idx in cross:
            i, j = int(ii[idx]), int(jj[idx])
            Mi = Mc[i]
            Ei = Mi + E[i] * math.sin(Mi)
            Ei -= (Ei - E[i] * math.sin(Ei) - Mi) / (1 - E[i] * math.cos(Ei))
            fi = 2 * math.atan2(math.sqrt(1 + E[i]) * math.sin(Ei / 2), math.sqrt(1 - E[i]) * math.cos(Ei / 2))
            Ej = Mi + E[j] * math.sin(Mi)
            Ej -= (Ej - E[j] * math.sin(Ej) - Mi) / (1 - E[j] * math.cos(Ej))
            fj = 2 * math.atan2(math.sqrt(1 + E[j]) * math.sin(Ej / 2), math.sqrt(1 - E[j]) * math.cos(Ej / 2))
            ri = A[i] * (1 - E[i] * math.cos(Ei)); rj = A[j] * (1 - E[j] * math.cos(Ej))
            if math.hypot(ri * math.cos(fi + W[i]) - rj * math.cos(fj + W[j]),
                          ri * math.sin(fi + W[i]) - rj * math.sin(fj + W[j])) < TAU_CLOSE:
                close_events += 1; quanta.append(int(Kk[i] + Kk[j]))
                for p in pols:
                    if p.caught(i, j, te, Nc): continue
                    p.miss += 1
                    if (p.Tc[i, j] > 0) or (p.Tc[j, i] > 0): p.stale += 1
                    else: p.struct += 1
        phi_prev = phi
        if lam > 0:
            hit = r.random(N) < lam * DT
            for i in np.flatnonzero(hit):
                s = r.choice([-1, 1], 3)
                A[i] += s[0] * 1e-4; E[i] += s[1] * 1e-3; W[i] += s[2] * 1e-2
                Nc[i] = 2 * np.pi * A[i] ** (-1.5); Kk[i] += 1
        for p in pols:
            if p.mode in ("quantum", "disp"):
                thr = p.m if p.mode == "quantum" else M_D
                due = np.flatnonzero((Kk - p.Kr) >= thr) if (lam > 0) else []
                for i in due: p.rebuild(i, te, Mc, A, Nc, Kk)
            if p.mode in ("cad", "disp"):
                while p.heap and p.heap[0][0] <= te:
                    _, i = heapq.heappop(p.heap)
                    p.rebuild(i, te, Mc, A, Nc, Kk)
    return close_events, quanta

def rec(p, ev, N=400):
    builds = p.rebuilds * K + p.renewals
    return dict(rebuilds=p.rebuilds, renewals=p.renewals, cert_builds=builds,
                per_body_orbit=round(p.rebuilds / (N * ORBITS), 4),
                misses=p.miss, struct=p.struct, stale=p.stale, close_events=ev)
if __name__ == "__main__":  # regenerable results live in run_one.py; the D-policy heap loop in
    import sys; print("use run_one.py (B,1,16 | nokick | C,R) -- this main includes the hanging D policies"); sys.exit(0)
    out = {}
    ms = [1, 4, 8, 16, 32, 64]
    pols = ([Pol("A", "quantum", 1)] + [Pol(f"B{m}", "quantum", m) for m in ms]
            + [Pol(f"D_e{e:.4f}", "disp", eta=e) for e in (math.pi / 2, math.pi / 8, math.pi / 32, math.pi / 128)])
    ev, q = run(pols, 2.0, 11)
    for p in pols: out[p.name] = rec(p, ev)
    p50, p90, p99 = np.percentile(q, [50, 90, 99]) if q else (0, 0, 0)
    out["_meta"] = dict(N=400, orbits=ORBITS, close_events=ev,
                        cand_per_body=int(np.mean([len(c) for c in CAND_G])),
                        quanta_at_close_event=dict(p50=float(p50), p90=float(p90), p99=float(p99),
                                                   mean=round(float(np.mean(q)), 2)))
    pols0 = [Pol("nokick_B8", "quantum", 8)]
    ev0, _ = run(pols0, 0.0, 11)
    out["nokick_B8"] = rec(pols0[0], ev0)
    R = ORBITS * 400 / max(out["B16"]["rebuilds"], 1)
    polsc = [Pol(f"C_R{R:.3f}", "cad", R=R)]
    evc, _ = run(polsc, 2.0, 11)
    out[polsc[0].name] = rec(polsc[0], evc)
    json.dump(out, open("probe_slack.json", "w"), indent=1)
    print(json.dumps(out, indent=1))
