#!/usr/bin/env python3
"""Changeover comparison on the plane's model (run 20261001-2353-q-changeover-e04a).

Model (docs/law.md "Perturbed motion"; crates/universe motion tests): star (1-mu) fixed
at the origin of its doll, planet mu on a prescribed circle (sep=1, Omega=1, period
P=2pi), ship a test particle, no indirect term. Exact invariant:
  C = v^2/2 - (1-mu)/|x| - mu/|x-xp| - Omega*L_z.
Judge: B12's (xtask/src/behave/handoff.rs + fit.rs): err = |C(t)-C(0)|/|C(0)| at P/8
samples over 200 periods, growth exponent = windowed log-log fit of the last 90%,
floor 1e-12, err_max 1e-4, median over judged seeds.

Schemes (all share the same WH DKD core: exact Kepler drift about the star, planet kick
at the step midpoint):
  symba     the incumbent mechanism (crates/universe/src/force.rs): the planet's pull is
            split across levels by smooth weights of the separation only,
            B_l = S((r-R_l/2)/(R_l/2)), S=y^2(3-2y), shells R_l = 2^(1-l)*R_edge,
            W_0=B_0, W_l = B_l*prod_{i<l}(1-B_i), deepest takes the rest; level l kicks
            W_l at cadence H/4^l, engaged while the pair can reach shell R_l within the
            interval. LEVELS=4 here (the shipped plane has 3 and captures at SOI/4; the
            lens's 0.1 R_H passes lie below that, so one level deeper, same law).
  mercurius Heaviside handoff (Rein et al. 2019): base WH everywhere; a base step whose
            start separation is inside 3 R_H is integrated by DOP853 rtol 1e-12 instead.
            Handoffs counted on flag changes.
  trace     (Lu, Hernandez & Rein 2024): base WH; after each step, take the adjoint step
            back; if the roundtrip error > eps, halve and retry (recursively, floor H/64).
            Retries are the events.
  wh-fixed  no changeover at H=P/64 (negative control).
  wh-dense  no changeover at H=P/512 (the dense-stepping cost control).
  soi-switch  events3's killed configuration: the drift switches dominant body (star
            Kepler <-> planet Kepler in planet-relative coordinates) at the SOI,
            selected by the state at the step start (negative control).
  truth     DOP853 rtol 1e-12 on the same model (positive control; pass counting).
"""
import math, random, json, sys, time

MU = 1e-3
GMS = 1.0 - MU
OM = 1.0
P = 2.0 * math.pi
RH = (MU / 3.0) ** (1.0 / 3.0)     # 0.06934
SOI = MU ** 0.4                     # 0.06310 (Laplace, the doll's edge)
LEVELS = 4
RATIO = 4
SH = [SOI * 2.0 ** (1 - l) for l in range(LEVELS)]   # R_0=2 SOI, ..., R_3=SOI/4
PLANET_R = 4.84e-5

def planet(t):
    return (math.cos(t), math.sin(t))

def planet_v(t):
    return (-math.sin(t), math.cos(t))

def jacobi(x, y, vx, vy, t):
    px, py = planet(t)
    r1 = math.hypot(x, y)
    r2 = math.hypot(x - px, y - py)
    return 0.5 * (vx * vx + vy * vy) - GMS / r1 - MU / r2 - OM * (x * vy - y * vx)

def planet_acc(x, y, t):
    px, py = planet(t)
    dx, dy = x - px, y - py
    r = math.hypot(dx, dy)
    r3 = r * r * r
    return (-MU * dx / r3, -MU * dy / r3), r

def model_acc(x, y, t):
    r1 = math.hypot(x, y)
    r3 = r1 * r1 * r1
    (ax, ay), _ = planet_acc(x, y, t)
    return (-GMS * x / r3 + ax, -GMS * y / r3 + ay)

# ---------- exact Kepler drift (universal variables) ----------
def _CS(z):
    try:
        if z > 1e-8:
            s = math.sqrt(z)
            return (1 - math.cos(s)) / z, (s - math.sin(s)) / (s * s * s)
        if z < -1e-8:
            s = math.sqrt(-z)
            return (1 - math.cosh(s)) / z, (math.sinh(s) - s) / (s * s * s)
        return 0.5 - z / 24.0 + z * z / 720.0, 1.0 / 6.0 - z / 120.0 + z * z / 5040.0
    except (OverflowError, ValueError):
        return float("nan"), float("nan")

def kepler(x, y, vx, vy, mg, dt):
    r0 = math.hypot(x, y)
    v2 = vx * vx + vy * vy
    alpha = 2.0 / r0 - v2 / mg
    vr0 = (x * vx + y * vy) / r0
    sq = math.sqrt(mg)
    chi = sq * abs(alpha) * dt if alpha != 0.0 else sq * dt / r0
    for _ in range(80):
        z = alpha * chi * chi
        C, S = _CS(z)
        F = r0 * vr0 / sq * chi * chi * C + (1 - alpha * r0) * chi ** 3 * S + r0 * chi - sq * dt
        if abs(F) < 1e-14:
            break
        dF = r0 * vr0 / sq * chi * (1 - alpha * chi * chi * S) + (1 - alpha * r0) * chi * chi * C + r0
        chi -= F / dF
    z = alpha * chi * chi
    C, S = _CS(z)
    if not (math.isfinite(C) and math.isfinite(S)):
        return float("nan"), float("nan"), float("nan"), float("nan")
    f = 1 - chi * chi / r0 * C
    g = dt - chi ** 3 / sq * S
    xn = f * x + g * vx
    yn = f * y + g * vy
    rn = math.hypot(xn, yn)
    fd = sq / (r0 * rn) * chi * (alpha * chi * chi * S - 1)
    gd = 1 - chi * chi * C / rn
    return xn, yn, fd * x + gd * vx, fd * y + gd * vy

# ---------- B12 fit (xtask/src/behave/fit.rs, ported exactly) ----------
def growth_exponent(err):
    n = len(err)
    first = max(n // 10, 1)
    if n <= first or any(not math.isfinite(e) for e in err):
        return float("nan")
    def edge(j):
        return n if j == 16 else round(first * (n / first) ** (j / 16.0))
    used, pts = 0, []
    for j in range(16):
        a, b = edge(j), edge(j + 1)
        if b <= a:
            continue
        used += 1
        top = max(abs(e) for e in err[a:b])
        if top > 0.0:
            pts.append((math.log(math.sqrt(a * (b - 1))), math.log(top)))
    if used < 8:
        return float("nan")
    if not pts:
        return 0.0
    if len(pts) < 3:
        return float("nan")
    m = float(len(pts))
    mx = sum(p[0] for p in pts) / m
    my = sum(p[1] for p in pts) / m
    sxx = sum((p[0] - mx) ** 2 for p in pts)
    return sum((p[0] - mx) * (p[1] - my) for p in pts) / sxx

# ---------- seeds (B12 recipe, my own RNG) ----------
def make_seeds():
    rng = random.Random(20261001)
    seeds = []
    for i in range(16):   # B12-style: k in U[1.5,3]
        k = 1.5 + 1.5 * rng.random()
        side = 1.0 if rng.random() < 0.5 else -1.0
        alpha = math.radians(30.0 + 300.0 * rng.random())
        seeds.append((k, side, alpha, "b12"))
    for i in range(16):   # deeper, held out: eccentric crossings at da0 = 2 R_H,
        # e in U[0.03,0.15], random periapsis and phase (the k in U[0.5,1.5] circular
        # group was co-orbital-captured and produced no passes at all; truth-measured)
        k = 2.0
        side = 1.0 if rng.random() < 0.5 else -1.0
        e = 0.03 + 0.12 * rng.random()
        om = 2.0 * math.pi * rng.random()
        f0 = math.radians(30.0 + 300.0 * rng.random())
        seeds.append((k, side, ("ecc", e, om, f0), "deep"))
    out = []
    for (k, side, alpha, grp) in seeds:
        if isinstance(alpha, tuple):
            _, e, om, f0 = alpha
            a = 1.0 + side * k * RH
            p = a * (1 - e * e)
            r = p / (1 + e * math.cos(f0))
            th = om + f0
            h = math.sqrt(GMS * p)
            vr = GMS / h * e * math.sin(f0)
            vt = h / r
            x, y = r * math.cos(th), r * math.sin(th)
            vx = vr * math.cos(th) - vt * math.sin(th)
            vy = vr * math.sin(th) + vt * math.cos(th)
            out.append(dict(k=k, side=side, alpha=(e, om, f0), grp=grp, state=(x, y, vx, vy)))
        else:
            r = 1.0 + side * k * RH
            vc = math.sqrt(GMS / r)
            x, y = r * math.cos(alpha), r * math.sin(alpha)
            vx, vy = -vc * math.sin(alpha), vc * math.cos(alpha)
            out.append(dict(k=k, side=side, alpha=alpha, grp=grp, state=(x, y, vx, vy)))
    return out

# ---------- shared run harness ----------
PERIODS = 200
COARSE = 8
NSTEPS = 64              # base steps per period (H = P/64)
HBASE = P / NSTEPS
NSAMP = PERIODS * COARSE + 1

class Ctx:
    __slots__ = ("x", "y", "vx", "vy", "t", "events", "kicks", "retries", "maps", "inner", "handoffs")
    def __init__(self, st):
        self.x, self.y, self.vx, self.vy = st
        self.t = 0.0
        self.events = 0   # encounter-machinery invocations (scheme-specific)
        self.kicks = 0    # planet-force evaluations
        self.retries = 0
        self.maps = 0     # drifts+kicks (WH map applications)
        self.inner = 0    # inner-integrator force evaluations (mercurius)
        self.handoffs = 0

def drift(c, dt):
    c.x, c.y, c.vx, c.vy = kepler(c.x, c.y, c.vx, c.vy, GMS, dt)

def wh_map(c, t, h, count=True):
    """One WH DKD map over [t, t+h]; self-adjoint (planet taken at the midpoint)."""
    drift(c, h / 2)
    tm = t + h / 2
    (ax, ay), _ = planet_acc(c.x, c.y, tm)
    c.vx += h * ax
    c.vy += h * ay
    drift(c, h / 2)
    c.t = t + h
    if count:
        c.kicks += 1
        c.maps += 3

def sample(c, c0, err):
    err.append(abs((jacobi(c.x, c.y, c.vx, c.vy, c.t) - c0) / c0))

def finished(c):
    return math.hypot(c.x, c.y) > 50.0 or planet_dist(c) < PLANET_R

def planet_dist(c):
    px, py = planet(c.t)
    return math.hypot(c.x - px, c.y - py)

def collect(c, c0):
    """Run to 200 periods, sampling every P/8. Returns (err, ok)."""
    err = []
    sample(c, c0, err)
    for step in range(PERIODS * NSTEPS):
        c.step() if hasattr(c, "step") else None
        if (step + 1) % (NSTEPS // COARSE) == 0:
            sample(c, c0, err)
        if finished(c):
            break
    ok = len(err) == NSAMP
    if not ok:
        err += [err[-1]] * (NSAMP - len(err))
    return err, len(err) and ok

# ---------- symba ----------
def Bfun(r, l):
    Rl = SH[l]
    y = (r - Rl * 0.5) / (Rl * 0.5)
    if y <= 0.0:
        return 0.0
    if y >= 1.0:
        return 1.0
    return y * y * (3 - 2 * y)

def Wfun(r, l):
    w = 1.0
    for i in range(min(l, LEVELS)):
        w *= 1.0 - Bfun(r, i)
        if w == 0.0:
            return 0.0
    if l < LEVELS:
        w *= Bfun(r, l)
    return w

def symba_depth(r, vrel, H):
    vcert = 1.25 * (vrel + math.sqrt(2 * MU / max(r, 1e-9)))
    reach = r - vcert * H
    d = 0
    for l in range(LEVELS):
        if reach < SH[l]:
            d = l + 1
    return d

class Symba:
    def __init__(self, st):
        self.c = Ctx(st)
    def step(self):
        c = self.c
        t0 = c.t
        snap = (c.x, c.y, c.vx, c.vy, c.t, c.events, c.kicks, c.maps)
        for guard in range(LEVELS + 2):
            r = planet_dist(c)
            pvx, pvy = planet_v(c.t)
            vrel = math.hypot(c.vx - pvx, c.vy - pvy)
            d = symba_depth(r, vrel, HBASE)
            if d == 0:
                wh_map(c, c.t, HBASE)
                return
            kicks = []
            for l in range(d + 1):
                hl = HBASE / RATIO ** l
                for m in range(RATIO ** l):
                    kicks.append((c.t + (m + 0.5) * hl, l))
            kicks.sort()
            tc = c.t
            under = False
            for (tk, l) in kicks:
                drift(c, tk - tc)
                tc = tk
                (ax, ay), r = planet_acc(c.x, c.y, tk)
                hl = HBASE / RATIO ** l
                w = Wfun(r, l)
                c.vx += w * ax * hl
                c.vy += w * ay * hl
                c.kicks += 1
                c.maps += 1
                if l >= 1:
                    c.events += 1
                if d < LEVELS and r < SH[d]:
                    under = True   # entered the next layer's support: re-run deeper
            drift(c, c.t + HBASE - tc)
            c.t = t0 + HBASE
            if not under:
                return
            # under-engaged (margin beaten): restart the base step one level deeper
            c.x, c.y, c.vx, c.vy, c.t, c.events, c.kicks, c.maps = snap
            c.events += 1
            c.retries += 1
        raise RuntimeError("symba engagement guard exceeded")

# ---------- mercurius ----------
R_SW = 3.0 * RH

class Mercurius:
    def __init__(self, st):
        self.c = Ctx(st)
        self.inside = False
    def step(self):
        c = self.c
        r = planet_dist(c)
        flag = r < R_SW
        if flag != self.inside:
            c.handoffs += 1
            c.events += 1
            self.inside = flag
        if flag:
            sol = dop853(c, HBASE)
            c.inner += sol
        else:
            wh_map(c, c.t, HBASE)

def dop853(c, h):
    from scipy.integrate import solve_ivp
    t0 = c.t
    def f(t, s):
        ax, ay = model_acc(s[0], s[1], t)
        return (s[2], s[3], ax, ay)
    sol = solve_ivp(f, (t0, t0 + h), [c.x, c.y, c.vx, c.vy], method="DOP853",
                    rtol=1e-12, atol=1e-14, t_eval=[t0 + h])
    if not sol.success or sol.y.shape[1] < 1:
        c.x = 1e9   # failed inner integration: mark the run bad (excluded, counted)
        return 0
    yy = list(sol.y)
    c.x, c.y, c.vx, c.vy = float(yy[0][-1]), float(yy[1][-1]), float(yy[2][-1]), float(yy[3][-1])
    c.t = t0 + h
    return sol.nfev

# ---------- trace ----------
class Trace:
    """TRACE (Lu, Hernandez and Rein 2024) in its working form. A DKD map is exactly
    self-adjoint, so a forward/backward roundtrip measures only roundoff (measured: the
    vacuous roundtrip check retried 3-5 times per run and let 0.2-level errors through).
    The informative check is the step's Jacobi error |dC|/|C0| (Rebound's TRACE checks
    the energy); above EPS the step is halved and retried, recursively, and the halves
    are themselves checked. Retries are the events."""
    EPS = 1e-6   # calibrated: far-field per-step |dC/C| at H=P/64 spans 1e-8 (circular) to 2.5e-5 (near passes); encounter peaks are 1e-3+
    def __init__(self, st):
        self.c = Ctx(st)
        self.c0 = jacobi(st[0], st[1], st[2], st[3], 0.0)
    def step(self):
        self.try_step(HBASE)
    def try_step(self, h):
        c = self.c
        t0 = c.t
        snap = (c.x, c.y, c.vx, c.vy)
        wh_map(c, t0, h)
        err = abs((jacobi(c.x, c.y, c.vx, c.vy, c.t) - self.c0) / self.c0)
        if err <= self.EPS or h / 2 < self.HMIN:
            return
        c.retries += 1
        c.events += 1
        c.x, c.y, c.vx, c.vy = snap
        c.t = t0
        self.try_step(h / 2)
        self.try_step(h / 2)
    HMIN = HBASE / 256.0   # resolution floor matching symba's deepest cadence (H/4^4)

# ---------- wh fixed ----------
class WH:
    def __init__(self, st, nsteps):
        self.c = Ctx(st)
        self.h = P / nsteps
        self.leftover = 0.0
    def step(self):
        wh_map(self.c, self.c.t, self.h)

# ---------- soi-switch (events3) ----------
class Soi:
    def __init__(self, st):
        self.c = Ctx(st)
        self.inside = False
    def step(self):
        c = self.c
        t0 = c.t
        h = HBASE
        r = planet_dist(c)
        flag = r < SOI
        if flag != self.inside:
            c.handoffs += 1
            c.events += 1
            self.inside = flag
        if not flag:
            wh_map(c, t0, h)
            return
        # inside: drift = exact Kepler about the planet (planet-relative), kick = the
        # remainder (star's full pull + the prescribed circle's centripetal term).
        px, py = planet(t0)
        rx, ry = c.x - px, c.y - py
        pvx, pvy = planet_v(t0)
        rvx, rvy = c.vx - pvx, c.vy - pvy
        rx, ry, rvx, rvy = kepler(rx, ry, rvx, rvy, MU, h / 2)
        tm = t0 + h / 2
        pxm, pym = planet(tm)
        ax, ay = model_acc(rx + pxm, ry + pym, tm)
        rr = math.hypot(rx, ry)
        ax += MU * rx / rr ** 3 + pxm  # remainder: + mu*rel/r^3 - planet accel (+Omega^2*xp)
        ay += MU * ry / rr ** 3 + pym
        rvx += h * ax
        rvy += h * ay
        rx, ry, rvx, rvy = kepler(rx, ry, rvx, rvy, MU, h / 2)
        c.t = t0 + h
        px, py = planet(c.t)
        pvx, pvy = planet_v(c.t)
        c.x, c.y = rx + px, ry + py
        c.vx, c.vy = rvx + pvx, rvy + pvy
        c.kicks += 1
        c.maps += 3

# ---------- truth ----------
def truth_run(st, fine=256, periods=PERIODS, rtol=1e-13, atol=1e-16):
    """DOP853 in planet-relative coordinates (restricted.rs's trick: the error control
    scales with the distance to the planet, not to the star)."""
    from scipy.integrate import solve_ivp
    ts = [j * P / fine for j in range(periods * fine + 1)]
    x, y, vx, vy = st
    px, py = planet(0.0)
    pvx, pvy = planet_v(0.0)
    s0 = [x - px, y - py, vx - pvx, vy - pvy]
    def f(t, s):
        pxm, pym = planet(t)
        ax, ay = model_acc(s[0] + pxm, s[1] + pym, t)
        return (s[2], s[3], ax + pxm, ay + pym)
    sol = solve_ivp(f, (0.0, periods * P), s0, method="DOP853", rtol=rtol,
                    atol=atol, t_eval=ts)
    Y = []
    for j, t in enumerate(ts):
        pxm, pym = planet(t)
        pvx, pvy = planet_v(t)
        Y.append((sol.y[0][j] + pxm, sol.y[1][j] + pym, sol.y[2][j] + pvx, sol.y[3][j] + pvy))
    return ts, Y

def count_passes(ts, Y):
    """Local minima of the planet distance below 3 R_H: (count, median periapsis/RH)."""
    import statistics
    r = [math.hypot(Y[j][0] - math.cos(ts[j]), Y[j][1] - math.sin(ts[j])) for j in range(len(ts))]
    mins = []
    for j in range(1, len(r) - 1):
        if r[j] < r[j - 1] and r[j] <= r[j + 1] and r[j] < 3.0 * RH:
            mins.append(r[j])
    med = statistics.median(mins) if mins else float("inf")
    return len(mins), med / RH

SCHEMES = {}

def run_one(scheme, st, nsteps=NSTEPS):
    if scheme == "symba":
        S = Symba(st)
    elif scheme == "mercurius":
        S = Mercurius(st)
    elif scheme == "trace":
        S = Trace(st)
    elif scheme == "soi-switch":
        S = Soi(st)
    elif scheme.startswith("wh"):
        S = WH(st, 512 if scheme == "wh-dense" else NSTEPS)
    else:
        raise ValueError(scheme)
    c = S.c
    c0 = jacobi(c.x, c.y, c.vx, c.vy, 0.0)
    err = [0.0]
    bad = False
    npp = NSTEPS if scheme != "wh-dense" else 512
    for step in range(PERIODS * npp):
        try:
            S.step()
        except (OverflowError, ValueError, RuntimeError):
            bad = True
            break
        if not (math.isfinite(c.x) and math.isfinite(c.y) and math.isfinite(c.vx) and math.isfinite(c.vy)):
            bad = True
            break
        if (step + 1) % (npp // COARSE) == 0:
            sample(c, c0, err)
        if finished(c):
            bad = True
            break
    ok = (len(err) == NSAMP) and not bad
    if len(err) < NSAMP:
        err += [err[-1]] * (NSAMP - len(err))
    return dict(err=err, ok=ok, events=c.events, kicks=c.kicks, maps=c.maps,
                inner=c.inner, handoffs=c.handoffs, restarts=c.retries, nsteps_done=len(err) // COARSE)

if __name__ == "__main__":
    t0 = time.time()
    seeds = make_seeds()
    do_schemes = sys.argv[1].split(",") if len(sys.argv) > 1 else \
        ["truth", "symba", "mercurius", "trace", "wh-fixed", "wh-dense", "soi-switch"]
    out = {"seeds": [], "schemes": {}}
    import os
    have_truth = os.path.exists("truth.json")
    old = json.load(open("truth.json"))["seeds"] if have_truth else None
    for i, sd in enumerate(seeds):
        st = sd["state"]
        rec = dict(k=sd["k"], side=sd["side"], alpha=str(sd["alpha"]), grp=sd["grp"])
        if old is not None and i < len(old) and "passes" in old[i]:
            rec.update(truth_err_max=old[i]["truth_err_max"], passes=old[i]["passes"],
                       med_peri=old[i]["med_peri"])
            out["seeds"].append(rec)
            continue
        if "truth" in do_schemes:
            ts, Y = truth_run(st)
            cj = [jacobi(Y[j][0], Y[j][1], Y[j][2], Y[j][3], ts[j]) for j in range(0, len(ts), 32)]
            e = [abs((v - cj[0]) / cj[0]) for v in cj]
            np_, medp = count_passes(ts, Y)
            rec.update(truth_err_max=max(e), passes=np_, med_peri=medp)
            print(f"seed {i:2d} k={sd['k']:.2f} {sd['grp']:4s} passes={np_:3d} medperi={medp:.3f} "
                  f"truthDC={max(e):.1e} ({time.time()-t0:.0f}s)", flush=True)
        out["seeds"].append(rec)
    if not have_truth:
        json.dump(out, open("truth.json", "w"))
    # schemes
    for scheme in [s for s in do_schemes if s != "truth"]:
        import os as _os
        if _os.path.exists(f"run_{scheme}.json"):
            print(f"== {scheme} already done, skip", flush=True)
            continue
        res = []
        for i, sd in enumerate(seeds):
            r = run_one(scheme, sd["state"])
            res.append(r)
            if i < 3 or i == 20:
                print(f"{scheme} seed {i:2d}: expo={growth_exponent(r['err']):.2f} "
                      f"max={max(r['err']):.1e} events={r['events']} kicks/orb={r['kicks']/PERIODS:.0f}", flush=True)
        out["schemes"][scheme] = res
        json.dump(out, open(f"run_{scheme}.json", "w"))
        print(f"== {scheme} done ({time.time()-t0:.0f}s)", flush=True)
    print("ALL DONE", time.time() - t0)
