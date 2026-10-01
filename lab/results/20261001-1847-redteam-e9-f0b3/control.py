#!/usr/bin/env python3
"""Red-team control for gate E9's oracle (wt/judge2 xtask/src/engine_judge/schwarzschild.rs).

Three-way comparison:
  (R) the judge's construction, mirrored faithfully in Python (difference ODEs,
      Killing constants, exponential-map genesis, equal-proper-time projection);
  (M) an INDEPENDENT absolute-coordinate integrator: raw second-order geodesic
      equations with textbook diagonal-metric Christoffels (no Killing constants,
      no difference variables), my own Riemann tensor, my own Fermi-simultaneity
      solve (orthogonality Newton step);
  (A) independent analytic derivations: turning-point (E,L), circular epicycle
      kappa, geodetic rate, Riemann-projected tidal matrix.

Judge's dimensionless units: r in units of r_p, lambda = tau/sqrt(r_p^3/M),
alpha = M/r_p. Offsets ~1e-5 (engine initial extent), scales s of that offset.
"""
import math, time, os

TAU = 2.0 * math.pi
R_LATTICE = float(1 << 40)
Q = float(1 << 20)
EPS = 1e-5
SAMPLES = 400
SUBSTEPS = 512

def f_of(a, r): return 1.0 - 2.0 * a / r

# ---------------- my generic diagonal-metric machinery (independent) -------------
def gamma3(a, r):
    """Gamma[c][i][j] for (t, r, phi) from standard diagonal-metric formulas."""
    f = f_of(a, r)
    A, B, C = f / a, 1.0 / f, r * r
    dA, dB, dC = 2.0 / (r * r), -(2.0 * a / (r * r)) / (f * f), 2.0 * r
    G = [[[0.0] * 3 for _ in range(3)] for _ in range(3)]
    G[0][0][1] = G[0][1][0] = dA / (2 * A)
    G[1][0][0] = dA / (2 * B)
    G[1][1][1] = dB / (2 * B)
    G[1][2][2] = -dC / (2 * B)
    G[2][1][2] = G[2][2][1] = dC / (2 * C)
    return G

def dgamma3_dr(a, r):
    dG = [[[0.0] * 3 for _ in range(3)] for _ in range(3)]
    f = f_of(a, r)
    common = a * (-2.0 / (r ** 3 * f) + 2.0 * a / (r ** 4 * f * f))
    dG[0][0][1] = dG[0][1][0] = common
    dG[1][1][1] = -common
    dG[1][0][0] = 2.0 * a / r ** 4 - 2.0 * f / r ** 3
    dG[1][2][2] = -(2.0 * a / r + f)
    dG[2][1][2] = dG[2][2][1] = -1.0 / (r * r)
    return dG

def metric3(a, r, x, y):
    f = f_of(a, r)
    return -f / a * x[0] * y[0] + x[1] * y[1] / f + r * r * x[2] * y[2]

def riemann_lower(a, r):
    G, dG = gamma3(a, r), dgamma3_dr(a, r)
    f = f_of(a, r)
    gdiag = [-f / a, 1.0 / f, r * r]
    Rm = [[[[0.0] * 3 for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for c in range(3):
        for s in range(3):
            for m in range(3):
                for n in range(3):
                    v = 0.0
                    if m == 1: v += dG[c][n][s]
                    if n == 1: v -= dG[c][m][s]
                    for l in range(3):
                        v += G[c][m][l] * G[l][n][s] - G[c][n][l] * G[l][m][s]
                    Rm[c][s][m][n] = gdiag[c] * v
    return Rm

def tidal_in_frame(a, r, u, axes):
    Rm = riemann_lower(a, r)
    C = [[0.0] * 2 for _ in range(2)]
    for i in range(2):
        for j in range(2):
            v = 0.0
            for mu in range(3):
                for al in range(3):
                    for nu in range(3):
                        for be in range(3):
                            v += axes[i][mu] * u[al] * axes[j][nu] * u[be] * Rm[mu][al][nu][be]
            C[i][j] = v
    return C

def rk4(y, h, rhs):
    k1 = rhs(y)
    k2 = rhs([y[i] + 0.5 * h * k1[i] for i in range(len(y))])
    k3 = rhs([y[i] + 0.5 * h * k2[i] for i in range(len(y))])
    k4 = rhs([y[i] + h * k3[i] for i in range(len(y))])
    return [y[i] + h / 6.0 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(len(y))]

# ================= (R) faithful mirror of the judge's oracle =====================
def inv_diff(r, d, power):
    b = r + d
    s = sum((r ** j) * (b ** (power - 1 - j)) for j in range(power))
    return -d * s / ((r ** power) * (b ** power))

class JudgeMirror:
    def __init__(self, a):
        self.a = a

    def conn(self, r, u, v):
        a = self.a
        f = 1.0 - 2.0 * a / r
        g = a / (r * r * f)
        return [g * (u[0] * v[1] + u[1] * v[0]),
                f / (r * r) * u[0] * v[0] - g * u[1] * v[1] - f * r * u[2] * v[2],
                (u[1] * v[2] + u[2] * v[1]) / r]

    def displaced(self, u, axes, x, v):
        a = self.a
        y = [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for c in range(3):
            y[3 + c] = x[0] * axes[0][c] + x[1] * axes[1][c]
            y[6 + c] = u[c] + v[0] * axes[0][c] + v[1] * axes[1][c]
        nrm = math.sqrt(-1.0 / (a * metric3(a, 1.0, y[6:9], y[6:9])))
        for c in range(3):
            y[6 + c] *= nrm
        def rhs(z):
            eta = z[3:6]
            gg = self.conn(z[1], eta, eta)
            gu = self.conn(z[1], eta, z[6:9])
            return list(z[3:6]) + [-gg[c] for c in range(3)] + [-gu[c] for c in range(3)]
        for _ in range(16):
            y = rk4(y, 1.0 / 16.0, rhs)
        return y[0:3], y[6:9]

    def initial(self, e, offsets, scale):
        a = self.a
        p = (1.0 + e) / a
        energy = math.sqrt(((p - 2.0) ** 2 - 4.0 * e * e) / (p * (p - 3.0 - e * e)))
        angular = math.sqrt((1.0 + e) / (1.0 - (3.0 + e * e) * a / (1.0 + e)))
        f = 1.0 - 2.0 * a
        u = [energy / f, 0.0, angular]
        axes = [[0.0, math.sqrt(f), 0.0],
                [a * angular / math.sqrt(f), 0.0, energy / math.sqrt(f)]]
        self.energy, self.angular = energy, angular
        pairs = []
        y0 = [1.0, 0.0, 0.0, 0.0] + axes[0] + axes[1]
        for (x, v) in offsets:
            for sign in (scale, -scale):
                z, vel = self.displaced(u, axes, [c * sign for c in x], [c * sign for c in v])
                r = z[1]
                pairs.append(((1.0 - 2.0 * a / r) * vel[0] - energy,
                              r * r * vel[2] - angular,
                              r - 1.0, vel[1], z[0], z[2]))
                y0.extend([r - 1.0, vel[1], z[0], z[2]])
        return pairs, y0

    def rhs_full(self, y, pairs):
        a, l, energy = self.a, self.angular, self.energy
        r, w = y[0], y[1]
        f = 1.0 - 2.0 * a / r
        u = [energy / f, w, l / (r * r)]
        dy = [w, -1.0 / r ** 2 + l * l / r ** 3 - 3.0 * a * l * l / r ** 4, u[0], u[2]]
        for start in (4, 7):
            g = self.conn(r, u, y[start:start + 3])
            dy.extend([-g[c] for c in range(3)])
        for (i, (de, dl, _, _, _, _)) in enumerate(pairs):
            jb = 10 + 4 * i
            d0, d1 = y[jb], y[jb + 1]      # CURRENT pair state, not genesis constants
            b = r + d0
            fb = 1.0 - 2.0 * a / b
            dl2 = dl * (2.0 * l + dl)
            dy.append(d1)
            dy.append(-inv_diff(r, d0, 2) + dl2 / b ** 3 + l * l * inv_diff(r, d0, 3)
                      - 3.0 * a * (dl2 / b ** 4 + l * l * inv_diff(r, d0, 4)))
            dy.append(de / fb - energy * 2.0 * a * d0 / (r * b * f * fb))
            dy.append(dl / b ** 2 + l * inv_diff(r, d0, 2))
        return dy

    def oracle(self, e, offsets, stride, steps, scale):
        pairs, y0 = self.initial(e, offsets, scale)
        assert len(y0) == 10 + 4 * len(pairs)
        def rhs(y): return self.rhs_full(y, pairs)
        out, invariant = [], 0.0
        y = list(y0)
        a = self.a
        for j in range(SAMPLES + 1):
            axes = [y[4:7], y[7:10]]
            r = y[0]
            f = 1.0 - 2.0 * a / r
            u = [self.energy / f, y[1], self.angular / (r * r)]
            for k in range(2):
                invariant = max(invariant, abs(metric3(a, r, axes[k], axes[k]) - 1.0))
                invariant = max(invariant, abs(math.sqrt(a) * metric3(a, r, u, axes[k])))
            invariant = max(invariant, abs(metric3(a, r, axes[0], axes[1])))
            invariant = max(invariant, abs(a * metric3(a, r, u, u) + 1.0))
            members = []
            for i in range(len(offsets)):
                pl, mi = 10 + 8 * i, 14 + 8 * i
                delta = [(y[pl + 2] - y[mi + 2]) / (2 * scale),
                         (y[pl] - y[mi]) / (2 * scale),
                         (y[pl + 3] - y[mi + 3]) / (2 * scale)]
                pos = [metric3(a, r, delta, axes[c]) * R_LATTICE for c in range(2)]
                members.append(pos)
                members.append([-c for c in pos])
            out.append(members)
            if j < SAMPLES:
                h = stride / steps
                for _ in range(steps):
                    y = rk4(y, h, rhs)
        return out, invariant

def period(a, e):
    if e == 0.0:
        return TAU * math.sqrt(1.0 - 3.0 * a)
    p = (1.0 + e) / a
    points = 4096
    h = TAU / points
    tot = 0.0
    for i in range(points + 1):
        c = math.cos(i * h)
        w = 1.0 if i in (0, points) else (2.0 if i % 2 == 0 else 4.0)
        tot += w * (1.0 + e) ** 1.5 * math.sqrt((p - 3.0 - e * e) / (p - 6.0 - 2.0 * e * c)) / (1.0 + e * c) ** 2
    return tot * h / 3.0

def fixtures(ratio):
    nword = round((1 << 60) * Q / R_LATTICE / math.sqrt(ratio))
    n = nword / float(1 << 60)
    a = (n * R_LATTICE / Q) ** 2
    offsets = []
    for p in [(1.0, 0.0), (0.35, 0.8), (-0.7, 0.45)]:
        x = [round(c * EPS * R_LATTICE) for c in p]
        k = [round(-n * x[1]), round(-n * x[0])]
        offsets.append(([c / R_LATTICE for c in x], [c / (n * R_LATTICE) for c in k]))
    return n, a, offsets

def errors(got, truth, offsets):
    pe = se = 0.0
    for g, t in zip(got, truth):
        mass = sum((1 + i // 2) for i in range(len(t)))
        ct = [sum(t[i][c] * (1 + i // 2) / mass for i in range(len(t))) for c in range(2)]
        cg = [sum(g[i][c] * (1 + i // 2) / mass for i in range(len(g))) for c in range(2)]
        spread = max(math.hypot(*(t[i][c] - ct[c] for c in range(2))) for i in range(len(t)))
        spread = max(spread, 1.0)
        for i in range(len(t)):
            d = max(math.hypot(*t[i]), math.hypot(*offsets[i // 2][0]) * R_LATTICE, 1.0)
            p = math.hypot(*(g[i][c] - t[i][c] for c in range(2))) / d
            s = math.hypot(*(g[i][c] - cg[c] - (t[i][c] - ct[c]) for c in range(2))) / spread
            pe, se = max(pe, p), max(se, s)
    return pe, se

# ================= (M) my independent absolute integrator ========================
class Independent:
    """Raw second-order geodesic equations in (t, r, phi); no Killing constants in
    the RHS, no difference variables. E, L monitored as OUTPUTS only."""
    def __init__(self, a):
        self.a = a

    def geod_rhs(self, y):
        G = gamma3(self.a, y[1])
        v = [y[2], y[3], y[5]]
        acc = []
        for c in range(3):
            s = 0.0
            for al in range(3):
                for be in range(3):
                    s += G[c][al][be] * v[al] * v[be]
            acc.append(-s)
        return [y[2], y[3], acc[0], acc[1], y[5], acc[2]]

    def EL(self, y):
        return f_of(self.a, y[1]) * y[2], y[1] * y[1] * y[5]

    def run_reference_with_axes(self, E, L, stride, steps):
        """Joint 10-word RK4 state: (t, r, tdot, rdot, phi, phidot, axis0(3), axis1(3)).
        Axes transported by the same RK4; u read from the state."""
        a = self.a
        f1 = f_of(a, 1.0)
        y = [0.0, 1.0, E / f1, 0.0, 0.0, L,
             0.0, math.sqrt(f1), 0.0,
             a * L / math.sqrt(f1), 0.0, E / math.sqrt(f1)]
        def rhs(z):
            out = list(self.geod_rhs(z[0:6]))
            G = gamma3(a, z[1])
            v = [z[2], z[3], z[5]]
            for c in (0, 1):
                ax = z[6 + 3 * c: 9 + 3 * c]
                gv = []
                for mu in range(3):
                    s = 0.0
                    for al in range(3):
                        for be in range(3):
                            s += G[mu][al][be] * v[al] * ax[be]
                    gv.append(-s)
                out.extend(gv)
            return out
        samples = []
        for j in range(SAMPLES + 1):
            samples.append((list(y[0:6]), [list(y[6:9]), list(y[9:12])]))
            if j < SAMPLES:
                h = stride / steps
                for _ in range(steps):
                    y = rk4(y, h, rhs)
        return samples

    def run_members(self, init_states, stride, steps):
        ms = [list(s) for s in init_states]
        out = []
        for j in range(SAMPLES + 1):
            out.append([list(m) for m in ms])
            if j < SAMPLES:
                h = stride / steps
                for i in range(len(ms)):
                    for _ in range(steps):
                        ms[i] = rk4(ms[i], h, self.geod_rhs)
        return out

    def project(self, ref_y, ref_axes, member_y):
        r = ref_y[1]
        delta = [member_y[0] - ref_y[0], member_y[1] - r, member_y[4] - ref_y[4]]
        return [metric3(self.a, r, delta, ax) * R_LATTICE for ax in ref_axes]

    def fermi_correct(self, ref_y, ref_axes, member_y):
        """One Newton step to the Fermi-simultaneous member event, then project."""
        a = self.a
        r = ref_y[1]
        u = [ref_y[2], ref_y[3], ref_y[5]]
        delta = [member_y[0] - ref_y[0], member_y[1] - r, member_y[4] - ref_y[4]]
        h = metric3(a, r, delta, u)
        hp = metric3(a, r, [member_y[2], member_y[3], member_y[5]], u)
        dlam = -h / hp
        y2 = rk4(member_y, dlam, self.geod_rhs) if dlam != 0.0 else list(member_y)
        return self.project(ref_y, ref_axes, y2), dlam

def independent_EL(a, e):
    """Turning points r=1 and r_a=(1+e)/(1-e) of rdot^2 = E^2/a - f(r)(1+L^2/r^2)."""
    if e == 0.0:
        L2 = 1.0 / (1.0 - 3.0 * a)   # circular: potential minimum at r=1
        f1 = f_of(a, 1.0)
        return math.sqrt(f1 * (1.0 + a * L2)), math.sqrt(L2)
    ra = (1.0 + e) / (1.0 - e)
    f1, fa = f_of(a, 1.0), f_of(a, ra)
    L2 = (fa - f1) / (a * (f1 - fa / ra ** 2))
    return math.sqrt(f1 * (1.0 + a * L2)), math.sqrt(L2)

def centered_measure(projs, scale=1.0):
    members = []
    for pr in projs:
        row = []
        for i in range(3):
            p = [(pr[2 * i][c] - pr[2 * i + 1][c]) / (2.0 * scale) for c in range(2)]
            row.append(p)
            row.append([-c for c in p])
        members.append(row)
    return members

def main():
    t_start = time.time()
    log = []
    def say(msg):
        print(msg, flush=True)
        log.append(msg)

    say("== 1. Killing constants (independent turning-point vs judge's Darwin forms) ==")
    for a in (0.1, 1e-6):
        for e in (0.3, 0.6):
            jm = JudgeMirror(a)
            jm.initial(e, [], 1.0)
            E_mine, L_mine = independent_EL(a, e)
            say(f"  a={a:g} e={e}: dE/E={abs(jm.energy-E_mine)/E_mine:.3e} "
                f"dL/L={abs(jm.angular-L_mine)/L_mine:.3e}")

    SKIP2 = os.environ.get("SKIP_SEC2")
    say("== 2. Mirror fidelity (judge printed, r=10: e=0 -> 3.05e-8, e=0.6 -> 1.61e-6) ==")
    for e, printed in ((0.0, 3.05e-8), (0.6, 1.61e-6)):
        _, a, offsets = fixtures(10.0)
        jm = JudgeMirror(a)
        dt = period(a, e) / 40.0
        t0 = time.time()
        truth = jm.oracle(e, offsets, dt, SUBSTEPS, 1.0 / 16.0)
        half = jm.oracle(e, offsets, dt, SUBSTEPS, 1.0 / 32.0)
        pe, se = errors(half[0], truth[0], offsets)
        say(f"  e={e}: separation position={pe:.3e} shape={se:.3e} "
            f"(judge printed {printed:.3e}) wall={time.time()-t0:.0f}s "
            f"invariant={max(truth[1], half[1]):.2e}")

    for ratio, e_list in ((10.0, (0.6, 0.0)), (1e6, (0.0,))):
        for e in e_list:
            say(f"== 3/5. ratio={ratio:g} e={e}: absolute pairs vs judge oracle ==")
            n, a, offsets = fixtures(ratio)
            jm = JudgeMirror(a)
            dt = period(a, e) / 40.0
            t0 = time.time()
            truth16, inv16 = jm.oracle(e, offsets, dt, SUBSTEPS, 1.0 / 16.0)
            t_truth = time.time() - t0
            E_i, L_i = independent_EL(a, e)
            ind = Independent(a)
            t0 = time.time()
            refs = ind.run_reference_with_axes(E_i, L_i, dt, SUBSTEPS)
            t_ref = time.time() - t0
            for scale, tag in ((1.0 / 16.0, "s=1/16"), (1.0, "s=1")):
                pairs, _ = jm.initial(e, offsets, scale)
                init_states = [[d2, 1.0 + d0, (jm.energy + de) / f_of(a, 1.0 + d0), d1,
                                d3, (jm.angular + dl) / (1.0 + d0) ** 2]
                               for (de, dl, d0, d1, d2, d3) in pairs]
                t0 = time.time()
                mem = ind.run_members(init_states, dt, SUBSTEPS)
                t_mem = time.time() - t0
                cons = 0.0
                for idx in range(len(init_states)):
                    E0, L0 = ind.EL(mem[0][idx])
                    E1, L1 = ind.EL(mem[-1][idx])
                    cons = max(cons, abs(E1 - E0) / max(abs(E0), 1e-30),
                               abs(L1 - L0) / max(abs(L0), 1e-30))
                projs = [[ind.project(ref[0], ref[1], m) for m in memj]
                         for ref, memj in zip(refs, mem)]
                mine = centered_measure(projs, scale)
                pe, se = errors(mine, truth16, offsets)
                label = ("P1 absolute-vs-difference (pred <1e-9)" if scale == 1.0 / 16.0
                         else "P4 full-extent vs linearized truth (pred <5e-4; band 1e-2)")
                say(f"  {tag}: {label}: position={pe:.3e} shape={se:.3e} "
                    f"EL_drift={cons:.2e}")
                projsF, dmax = [], 0.0
                for ref, memj in zip(refs, mem):
                    row = []
                    for m in memj:
                        pf, dlam = ind.fermi_correct(ref[0], ref[1], m)
                        row.append(pf)
                        dmax = max(dmax, abs(dlam))
                    projsF.append(row)
                mineF = centered_measure(projsF, scale)
                peF, _ = errors(mineF, mine, offsets)
                peT, seT = errors(mineF, truth16, offsets)
                pl = ("pred <1e-7" if scale == 1.0 / 16.0 else "pred ~<1e-5")
                say(f"  {tag}: P2 Fermi-vs-equal-lambda position={peF:.3e} ({pl}) "
                    f"max|dlambda|={dmax:.2e}; Fermi-vs-judge-truth={peT:.3e}/{seT:.3e}")
            say(f"  timing: judge_oracle={t_truth:.0f}s my_ref={t_ref:.0f}s "
                f"my_members={t_mem:.0f}s per 10-period run (python)")

    say("== 6. Circular analytics (a=0.1) ==")
    a = 0.1
    E, L = independent_EL(a, 0.0)
    jm = JudgeMirror(a)
    jm.initial(0.0, [], 1.0)
    say(f"  E: mine={E:.15f} judge={jm.energy:.15f}; L: mine={L:.15f} judge={jm.angular:.15f}")
    ind = Independent(a)
    dt = period(a, 0.0) / 40.0
    refs = ind.run_reference_with_axes(E, L, dt, SUBSTEPS)
    u0 = [refs[0][0][2], refs[0][0][3], refs[0][0][5]]
    axes0 = refs[0][1]
    z, vel = jm.displaced(u0, axes0, [1e-6, 0.0], [0.0, 0.0])
    mem = ind.run_members([[z[0], z[1], vel[0], vel[1], z[2], vel[2]]], dt, SUBSTEPS)
    drs = [m[0][3] for m in mem]
    lam = [j * dt for j in range(SAMPLES + 1)]
    zeros = []
    for j in range(1, SAMPLES + 1):
        if drs[j - 1] * drs[j] < 0:
            zeros.append(lam[j - 1] - drs[j - 1] * (lam[j] - lam[j - 1]) / (drs[j] - drs[j - 1]))
    kappa_est = math.pi / ((zeros[-1] - zeros[1]) / (len(zeros) - 2)) if len(zeros) >= 3 else float("nan")
    kappa_analytic = math.sqrt((1.0 - 6 * a) / (1.0 - 3 * a))
    say(f"  radial epicycle kappa: measured={kappa_est:.9f} analytic={kappa_analytic:.9f} "
        f"rel={abs(kappa_est-kappa_analytic)/kappa_analytic:.2e}")
    lams, angles = [], []
    for j, (ref, axes) in enumerate(refs):
        y, ax = ref[0], axes[1]
        f = f_of(a, y[1])
        theta_ax = y[4] + math.atan2(y[1] * ax[2], math.sqrt(f) * ax[1])
        if angles:
            if theta_ax - angles[-1] > math.pi: theta_ax -= TAU
            elif angles[-1] - theta_ax > math.pi: theta_ax += TAU
        lams.append(j * dt)
        angles.append(theta_ax)
    precess = (angles[40] - angles[0]) / (lams[40] - lams[0])
    geo = 1.0 / math.sqrt(1.0 - 3 * a)
    say(f"  axis1 static-frame rate={precess:.9f} (judge asserts exactly 1; "
        f"dphi/dlambda={geo:.9f}, geodetic vs comoving radial={geo-1:.9f}/lambda)")
    C = tidal_in_frame(a, 1.0, u0, axes0)
    say(f"  my Riemann-projected tide C=[[{C[0][0]:+.6f},{C[0][1]:+.6f}],"
        f"[{C[1][0]:+.6f},{C[1][1]:+.6f}]]")
    pairs, _ = jm.initial(0.0, [([1.0, 0.0], [0.0, 0.0]), ([0.0, 1.0], [0.0, 0.0])], 1e-3)
    init_states = [[d2, 1.0 + d0, (jm.energy + de) / f_of(a, 1.0 + d0), d1, d3,
                    (jm.angular + dl) / (1.0 + d0) ** 2] for (de, dl, d0, d1, d2, d3) in pairs]
    h = dt / SUBSTEPS
    traces = []
    for s in init_states:
        ys = [list(s)]
        for _ in range(4):
            ys.append(rk4(ys[-1], h, ind.geod_rhs))
        traces.append(ys)
    ry0, rax0 = refs[0]
    accel = []
    for i in range(2):
        p = [ind.project(ry0, rax0, traces[2 * i][k]) for k in range(3)]
        m = [ind.project(ry0, rax0, traces[2 * i + 1][k]) for k in range(3)]
        accel.append([((p[2][c] - m[2][c]) - 2 * (p[1][c] - m[1][c]) + (p[0][c] - m[0][c]))
                      / (h * h) / (2 * 1e-3) / R_LATTICE for c in range(2)])
    say(f"  measured d2xi/dlambda2 per unit offset: x-dir={accel[0]}, y-dir={accel[1]}")
    say(f"  (geodesic deviation in Fermi frame: xi'' = -C xi; check -C columns)")

    say(f"== total wall {time.time() - t_start:.0f}s ==")
    with open(__file__ + ".output.txt", "w") as fh:
        fh.write("\n".join(log) + "\n")

if __name__ == "__main__":
    main()
