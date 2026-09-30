#!/usr/bin/env python3
"""Taleb lens run 20260930-2250: fragility of the tau regime selector (B14).

Circular restricted three-body (planet + Sun + test moon), planetocentric,
units normalized so the moon's initial osculating a = 1 and n = 1.
  Truth : full CR3BP acceleration (direct Sun term + indirect term).
  Law F : Hill quadrupole tide per step (the dense fallback stand-in).
  Law S : orbit-averaged quadrupole (law.md's tau < tau0 regime). Coplanar
          quadrupole averaging gives e(t) = e0 exactly, so S is blind to any
          eccentricity pump (evection, chaos overlap); its error IS the pump.

Subcommands: controls | sweep | chatter.  Each prints and writes JSON.
"""
import json
import sys
import time

import numpy as np

MU_SUN = 1000.0              # GM_sun / GM_planet (Sun/Jupiter ~ 1050)
RH = (1.0 / (3.0 * MU_SUN)) ** (1 / 3)   # Hill radius in a_p units = 0.0693
ESCAPE_RH = 1.5              # escaped beyond this many Hill radii
STEPS_PER_ORB = 128          # leapfrog steps per moon orbit
ESCAPE_R = 2.5               # escaped beyond this (in a0 units)
SAMPLE_EVERY = 16            # steps between osculating-element samples
SEEDS_M0 = [0.0, np.pi / 2, np.pi, 3 * np.pi / 2]
SEEDS_W = [0.0, np.pi / 2]   # 4 seeds: (M0, varpi) cross product


def kepler_start(e0, retro):
    """States at the 4 seeds; a=1, n=1, periapsis along +x, rotated by varpi."""
    out = []
    for M0 in SEEDS_M0:
        for w in SEEDS_W:
            E = M0
            for _ in range(12):
                E = E - (E - e0 * np.sin(E) - M0) / (1 - e0 * np.cos(E))
            b = np.sqrt(1 - e0 ** 2)
            r = np.array([np.cos(E) - e0, b * np.sin(E)])
            v = (1.0 / (1 - e0 * np.cos(E))) * np.array([-np.sin(E), b * np.cos(E)])
            c, s = np.cos(w), np.sin(w)
            Rm = np.array([[c, -s], [s, c]])
            r, v = Rm @ r, Rm @ v
            if retro:
                v = np.array([v[0], -v[1]])
            out.append((r, v))
    return out


class Grid:
    """Velocity-Verlet over (case, seed) with per-case end times."""

    def __init__(self, cases, law, n_pl_orb=None, steps_per_orb=STEPS_PER_ORB,
                 moon_orb=None):
        self.cases, self.law = cases, law
        nc = len(cases)
        ns = len(SEEDS_M0) * len(SEEDS_W)
        self.shape = (nc, ns)
        r = np.zeros((nc, ns, 2))
        v = np.zeros((nc, ns, 2))
        for ic, c in enumerate(cases):
            for js, (rr, vv) in enumerate(kepler_start(c["e0"], c["retro"])):
                r[ic, js], v[ic, js] = rr, vv
        self.r, self.v = r, v
        self.R = np.array([1.0 / (RH * c["tau"]) for c in cases])     # (nc,)
        self.np_sun = np.sqrt((1 + MU_SUN) / self.R ** 3)
        self.esc_r = ESCAPE_RH * RH * self.R  # ESCAPE_RH Hill radii, a0 units                 # (nc,)
        self.h = 2 * np.pi / steps_per_orb
        if moon_orb is not None:
            self.T_end = np.full(len(cases), moon_orb * 2 * np.pi)
        else:
            self.T_end = n_pl_orb * 2 * np.pi / self.np_sun
        self.alive = np.ones((nc, ns), bool)
        self.t = 0.0
        self.max_e = np.zeros((nc, ns))
        self.final_e = np.zeros((nc, ns))
        self.final_a = np.zeros((nc, ns))
        self.esc = np.zeros((nc, ns), bool)
        self.esc_orb = np.full((nc, ns), np.nan)   # escape time, planet orbits
        self.J0 = None
        self.Jdrift = np.zeros((nc, ns))

    def sun(self, t):
        ang = self.np_sun[:, None] * t
        Rs = np.stack([self.R[:, None] * np.cos(ang),
                       self.R[:, None] * np.sin(ang)], -1)          # (nc,1,2)
        return Rs

    def accel(self, r, t):
        Rs = self.sun(t)
        rn = np.linalg.norm(r, axis=-1, keepdims=True)
        if self.law == "F":
            Rhat = Rs / self.R[:, None, None]
            rd = (r * Rhat).sum(-1, keepdims=True)
            return -r / rn ** 3 + MU_SUN / self.R[:, None, None] ** 3 * (3 * rd * Rhat - r)
        d = Rs - r   # sun-relative: (R - r), tide = GM_s[(R-r)/|R-r|^3 - R/R^3]
        dn = np.linalg.norm(d, axis=-1, keepdims=True)
        return -r / rn ** 3 + MU_SUN * (d / dn ** 3 - Rs / self.R[:, None, None] ** 3)

    def jacobi(self, r, v, t):
        # Barycentric CR3BP Jacobi constant, computed from planetocentric state.
        Rs = self.sun(t)                                   # (nc,1,2)
        Om = self.np_sun[:, None, None]
        c = MU_SUN / (1 + MU_SUN)                          # barycentre offset
        rho = r - c * Rs
        Rdot = Om * np.stack([-Rs[..., 1], Rs[..., 0]], -1)
        u = v - c * Rdot                                   # barycentric inertial v
        vrot = u - Om * np.stack([-rho[..., 1], rho[..., 0]], -1)
        dn = np.linalg.norm(r - Rs, axis=-1)
        rn = np.linalg.norm(r, axis=-1)
        U = 1.0 / rn + MU_SUN / dn + 0.5 * (Om[..., 0] ** 2) * (rho ** 2).sum(-1)
        return 2 * U - (vrot ** 2).sum(-1)

    def elements(self):
        rn = np.linalg.norm(self.r, axis=-1)
        eps = 0.5 * (self.v ** 2).sum(-1) - 1.0 / rn
        a_o = -1.0 / (2 * eps)
        hh = self.r[..., 0] * self.v[..., 1] - self.r[..., 1] * self.v[..., 0]
        return a_o, np.sqrt(np.maximum(0.0, 1 + 2 * eps * hh ** 2))

    def run(self):
        h = self.h
        a1 = self.accel(self.r, 0.0)
        if self.law == "truth":
            self.J0 = self.jacobi(self.r, self.v, 0.0)
        nsteps = int(np.ceil(self.T_end.max() / h))
        rs_chunk = []
        t0 = time.time()
        for k in range(nsteps):
            act = self.alive
            if act.all():
                self.v += 0.5 * h * a1
                self.r += h * self.v
                self.t += h
                a1 = self.accel(self.r, self.t)
                self.v += 0.5 * h * a1
                rn = np.linalg.norm(self.r, axis=-1)
                gone = rn > self.esc_r[:, None]
            else:
                self.v[act] += 0.5 * h * a1[act]
                self.r[act] += h * self.v[act]
                self.t += h
                a1 = self.accel(self.r, self.t)
                self.v[act] += 0.5 * h * a1[act]
                rn = np.linalg.norm(self.r, axis=-1)
                rn = np.where(act, rn, 0.0)
                gone = act & (rn > self.esc_r[:, None])
            if gone.any():
                self.esc[gone] = True
                plorb = np.broadcast_to(
                    (self.t * self.np_sun / (2 * np.pi))[:, None],
                    self.esc_orb.shape)
                self.esc_orb[gone] = plorb[gone]
                self.alive[gone] = False
            if self.law == "truth" and k % 1024 == 0:
                Jn = self.jacobi(self.r, self.v, self.t)
                self.Jdrift = np.where(
                    self.alive, np.maximum(self.Jdrift,
                                    np.abs(Jn - self.J0) / np.abs(self.J0)),
                    self.Jdrift)
            if k % SAMPLE_EVERY == 0:
                a_o, e_o = self.elements()
                self.max_e = np.where(act, np.maximum(self.max_e, e_o),
                                      self.max_e)
                self.final_e = np.where(act, e_o, self.final_e)
                self.final_a = np.where(act, a_o, self.final_a)
                rs_chunk.append(np.where(act, rn, np.nan))
        rhist = np.stack(rs_chunk, axis=2)          # (nc, ns, nsamp)
        left, mid, right = rhist[:, :, :-2], rhist[:, :, 1:-1], rhist[:, :, 2:]
        ok = ~np.isnan(mid) & ~np.isnan(left) & ~np.isnan(right)
        isapo = (mid > left) & (mid >= right) & ok
        self.apo = [[mid[ic, js][isapo[ic, js]] for js in range(self.shape[1])]
                    for ic in range(self.shape[0])]
        self.rhist = rhist
        self.wall = time.time() - t0
        self.nsteps = nsteps
        return self

    def summary(self):
        rows = []
        for ic, c in enumerate(self.cases):
            rows.append(dict(
                tau=c["tau"], e0=c["e0"], retro=bool(c["retro"]), law=self.law,
                n_esc=int(self.esc[ic].sum()),
                esc_seeds=[bool(x) for x in self.esc[ic]],
                esc_orb_pl=[None if np.isnan(x) else round(float(x), 2)
                            for x in self.esc_orb[ic]],
                max_e=[round(float(x), 4) for x in self.max_e[ic]],
                final_e=[round(float(x), 4) for x in self.final_e[ic]],
                final_a=[round(float(x), 4) for x in self.final_a[ic]],
                Jdrift=[round(float(x), 6) for x in self.Jdrift[ic]]))
        return rows


def lawS_rows(truth_rows):
    """S predicts e(t) = e0 forever: its error is the truth's pump."""
    out = []
    for r in truth_rows:
        pump = max(r["max_e"]) - r["e0"]
        out.append(dict(tau=r["tau"], e0=r["e0"], retro=r["retro"],
                        n_esc=r["n_esc"],
                        e_pump=round(float(pump), 4),
                        med_max_e=round(float(np.median(r["max_e"])), 4)))
    return out


def cmd_controls():
    cases = [dict(tau=0.2, e0=0.05, retro=False),
             dict(tau=0.9, e0=0.3, retro=False)]
    t = Grid(cases, "truth", moon_orb=4096, steps_per_orb=128).run()
    hi = Grid([dict(tau=0.6, e0=0.3, retro=False)], "truth", moon_orb=2048,
              steps_per_orb=256).run()
    lo = Grid([dict(tau=0.6, e0=0.3, retro=False)], "truth", moon_orb=2048,
              steps_per_orb=128).run()
    res = dict(truth=t.summary(),
               truth256=dict(max_e=[round(float(x), 4) for x in hi.max_e[0]],
                             esc=int(hi.esc[0].sum())),
               truth128=dict(max_e=[round(float(x), 4) for x in lo.max_e[0]],
                             esc=int(lo.esc[0].sum())),
               wall=[round(t.wall, 1), round(hi.wall, 1), round(lo.wall, 1)])
    with open("controls.json", "w") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps(res, indent=1))
    return res


def cmd_sweep(fast=False):
    taus = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.70, 0.80, 0.90, 0.95]
    if fast:   # quick reproduction path: same physics, half horizon
        taus = [0.30, 0.40, 0.45, 0.50, 0.70, 0.95]
    cases = []
    for retro in (False, True):
        for e0 in (0.05, 0.3):
            for tau in taus:
                cases.append(dict(tau=tau, e0=e0, retro=retro))
    norb = 2048 if fast else 4096
    t = Grid(cases, "truth", moon_orb=norb, steps_per_orb=128).run()
    f = Grid(cases, "F", moon_orb=norb, steps_per_orb=128).run()
    tres, fres = t.summary(), f.summary()
    S = lawS_rows(tres)
    mism = []
    for rt, rf in zip(tres, fres):
        mis = sum(1 for a, b in zip(rt["esc_seeds"], rf["esc_seeds"]) if a != b)
        deF = max(abs(a - b) for a, b in zip(rt["final_e"], rf["final_e"]))
        mism.append(dict(tau=rt["tau"], e0=rt["e0"], retro=rt["retro"],
                         verdict_mismatch=int(mis),
                         dFinal_e_FvsT=round(float(deF), 4)))
    res = dict(truth=tres, lawF=fres, lawS=S, mismatch=mism,
               wall=dict(truth=round(t.wall, 1), F=round(f.wall, 1)),
               nsteps=t.nsteps)
    with open("sweep-fast.json" if fast else "sweep.json", "w") as fh:
        json.dump(res, fh, indent=1)
    print(f"{'tau':>5} {'e0':>5} {'dir':>4} | esc medMaxE  Jdr | Spump | Fmis dE")
    for s, m in zip(S, mism):
        tr = next(x for x in tres if x["tau"] == s["tau"]
                  and x["e0"] == s["e0"] and x["retro"] == s["retro"])
        print(f"{s['tau']:5.2f} {s['e0']:5.2f} {'ret' if s['retro'] else 'pro':>4} | "
              f"{s['n_esc']:3d} {s['med_max_e']:7.3f} {max(tr['Jdrift']):8.5f} | "
              f"{s['e_pump']:5.3f} | {m['verdict_mismatch']:3d} {m['dFinal_e_FvsT']:5.3f}")
    return res


def cmd_chatter(tau_star):
    """Apoapsis crossings of tau* from truth runs at e0=0.3 (straddling orbits).
    RH in a0 units = 1/tau (a0 = tau*RH_ap), so tau_apo = r_apo * tau."""
    taus = [0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65]
    cases = [dict(tau=tau, e0=0.3, retro=False) for tau in taus]
    t = Grid(cases, "truth", moon_orb=4096, steps_per_orb=128).run()
    rows = []
    for ic, c in enumerate(cases):
        for js in range(self_ns(t)):
            apo = t.apo[ic][js]
            if len(apo) < 4:
                continue
            tau_apo = apo * c["tau"]
            above = tau_apo > tau_star
            switches = int(np.abs(np.diff(above.astype(int))).sum())
            rows.append(dict(tau=c["tau"], seed=js, orbits=int(len(apo)),
                             switches=switches,
                             rate_per_orbit=round(switches / max(1, len(apo)), 4),
                             tau_apo_min=round(float(tau_apo.min()), 4),
                             tau_apo_max=round(float(tau_apo.max()), 4)))
    with open("chatter.json", "w") as fh:
        json.dump(dict(tau_star=tau_star, rows=rows), fh, indent=1)
    for r in rows:
        print(r)
    sw = [r["switches"] for r in rows]
    if sw:
        print("switches: max", max(sw), "p99", int(np.percentile(sw, 99)),
              "mean", round(float(np.mean(sw)), 2))
    return rows


def self_ns(grid):
    return grid.shape[1]


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "controls"
    if cmd == "controls":
        cmd_controls()
    elif cmd == "sweep":
        cmd_sweep(fast=len(sys.argv) > 2 and sys.argv[2] == "fast")
    elif cmd == "chatter":
        cmd_chatter(float(sys.argv[2]) if len(sys.argv) > 2 else 0.5)
