"""B12 replica: ships crossing a Jupiter-like planet's doll edge (handoff.rs).
Two dolls + handoff exactly as step.rs: inbound heliocentric with SyMBA level
substeps (x4 per shell: 2R_soi, R_soi), handoff at R_soi/4; outbound handoff at
R_soi. Planet frame: solar differential tide, step = passage/2leg per N.
Scene: GM_tot=1, sep=1, mu=1e-3, horizon 200 planet periods, ships born on
circular orbits 1.5-3 R_H from the planet at 30-330 deg, keep 16 that cross
R_soi >= 20 times (reference N=1024 decides). Gate: max |dC/C| <= 1e-4,
growth exponent <= 0.2 (median of rising ships)."""
import numpy as np, json, sys
import cad
from cad import TWOPI, elements, drift, Doll, run

MU = 1e-3
SEP = 1.0
N2 = 1.0
RSOI = MU ** 0.4
RH = (MU / 3) ** (1 / 3)
T_END = 200 * TWOPI

helio = Doll(1.0 - MU, [dict(gm=MU, D=SEP, n=N2, ph=0.0)])   # sun's doll, Jupiter pulls
planet = Doll(MU, [dict(gm=1.0 - MU, D=SEP, n=N2, ph=np.pi)])  # planet's doll, sun's tide


def jacobi(xh, yh, vxh, vyh, t):
    """Jacobi constant from heliocentric state (sun at origin, Jupiter at angle n2 t)."""
    xj, yj = SEP * np.cos(t), SEP * np.sin(t)
    vxj, vyj = -SEP * np.sin(t), SEP * np.cos(t)
    # barycentric
    xb = xh - MU * xj; yb = yh - MU * yj
    vxb = vxh - MU * vxj; vyb = vyh - MU * vyj
    vrx = vxb + yb; vry = vyb - xb   # v_rot = v_bary + z x r_bary (n2=1)
    r1 = np.hypot(xh, yh); r2 = np.hypot(xh - xj, yh - yj)
    return vrx ** 2 + vry ** 2 + 2 * (1 - MU) / r1 + 2 * MU / r2


def ships(n, seed):
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        side = rng.choice([-1.0, 1.0])
        k = 1.5 + 1.5 * rng.uniform()
        alpha = np.radians(30 + 300 * rng.uniform())
        r = SEP * (1 + side * k * RH / SEP)
        v = r ** -0.5
        out.append((r * np.cos(alpha), r * np.sin(alpha), -v * np.sin(alpha), v * np.cos(alpha)))
    return out


def passage_T(xp, yp, vxp, vyp, gm_p):
    """2 x (periapsis->edge leg) for the current planetocentric state, per step_for."""
    a, e, w, h = elements(xp, yp, vxp, vyp, gm_p)
    r = np.hypot(xp, yp)
    if (e < 1) and (a * (1 + e) < RSOI):
        P = TWOPI * np.sqrt(a ** 3 / gm_p)
        return P if np.isfinite(P) and P > 0 else 2.0
    # time from current radius to periapsis then out to RSOI (Kepler, hyperbolic or bound)
    from cad import kepler_E, kepler_H
    ret = h < 0
    ym = np.where(ret, -yp, yp); vym = np.where(ret, -vyp, vyp)
    vr = (xp * vxp + ym * vym) / r
    t_peri = 0.0
    if e >= 1:
        sinhH = r * vr / (e * np.sqrt(gm_p * (-a)))
        Hh = np.arcsinh(sinhH)
        M = e * np.sinh(Hh) - Hh
        n = np.sqrt(gm_p / (-a) ** 3)
        t_peri = M / n
    else:
        cosE = (1 - r / a) / e; sinE = r * vr / (e * np.sqrt(gm_p * a))
        E = np.arctan2(sinE, cosE)
        M = E - e * np.sin(E)
        n = np.sqrt(gm_p / a ** 3)
        t_peri = M / n
    # time periapsis -> RSOI outbound
    if e >= 1:
        Hf = np.arccosh((1 - RSOI / a) / e)
        tf = (e * np.sinh(Hf) - Hf) / np.sqrt(gm_p / (-a) ** 3)
    else:
        Ef = np.arccos(np.clip((1 - RSOI / a) / e, -1, 1))
        tf = (Ef - e * np.sin(Ef)) / np.sqrt(gm_p / a ** 3)
    T = 2 * max(tf, 1e-6)
    return T if np.isfinite(T) else 2.0


def simulate(s0, N_helio_fn, N_pass_fn, t_end=T_END, C_every=None):
    """All ships together; per-ship frame flag; returns Jacobi series + crossings + kicks."""
    n = len(s0)
    x = np.array([s[0] for s in s0]); y = np.array([s[1] for s in s0])
    vx = np.array([s[2] for s in s0]); vy = np.array([s[3] for s in s0])
    t = np.zeros(n)
    inside = np.zeros(n, bool)          # in planet doll
    was_in = np.zeros(n, bool)
    crossings = np.zeros(n, int)
    kicks = np.zeros(n)
    done = t >= t_end
    C0 = jacobi(x, y, vx, vy, t)
    Cs = [[(0.0, 0.0)] for _ in range(n)]
    xj_prev = np.zeros(n)
    guard = 0
    while not done.all() and guard < 4_000_000:
        guard += 1
        # relative position to Jupiter
        xj = SEP * np.cos(t); yj = SEP * np.sin(t)
        # (t is per-ship; approximate Jupiter at each ship's own t)
        xjr = SEP * np.cos(t); yjr = SEP * np.sin(t)
        dxr = x - xjr; dyr = y - yjr
        rr = np.hypot(dxr, dyr)
        # outbound handoff at RSOI
        go_out = inside & (rr > RSOI)
        # inbound handoff at RSOI/4
        go_in = (~inside) & (rr < RSOI / 4)
        for m in np.where(go_out | go_in)[0]:
            if go_out[m] and inside[m]:
                # planet -> helio
                x[m] += xjr[m]; y[m] += yjr[m]
                vx[m] += -SEP * np.sin(t[m]); vy[m] += SEP * np.cos(t[m])
                inside[m] = False
            elif go_in[m] and not inside[m]:
                x[m] -= xjr[m]; y[m] -= yjr[m]
                vx[m] -= -SEP * np.sin(t[m]); vy[m] -= SEP * np.cos(t[m])
                inside[m] = True
        # count crossings at kick ticks
        now_in = rr < RSOI
        crossings += (now_in != was_in)
        was_in = now_in
        # step size per ship
        H = np.zeros(n)
        for m in np.where(~done)[0]:
            if not inside[m]:
                a, e, w, h = elements(x[m:m+1], y[m:m+1], vx[m:m+1], vy[m:m+1], 1.0 - MU)
                P = TWOPI * np.sqrt(abs(a[0]) ** 3 / (1.0 - MU))
                N = N_helio_fn(a[0], e[0], rr[m])
                lvl = 1
                if rr[m] < RSOI:
                    lvl = 16
                elif rr[m] < 2 * RSOI:
                    lvl = 4
                H[m] = min(P * lvl / max(N, 1), t_end - t[m])
            else:
                Tp = passage_T(x[m:m+1], y[m:m+1], vx[m:m+1], vy[m:m+1], MU)
                N = N_pass_fn
                H[m] = min(Tp / max(N, 1), t_end - t[m])
        act = (~done) & (H > 0)
        # DKD on mixed frames: do drift half for all (per-frame gm), kick, drift half
        gm_arr = np.where(inside, MU, 1.0 - MU)
        x2 = np.where(act, 0, x); y2 = np.where(act, 0, y)
        for frame, gm in ((False, 1.0 - MU), (True, MU)):
            m = act & (inside == frame)
            if m.any():
                xn, yn, vxn, vyn = drift(x[m], y[m], vx[m], vy[m], gm, (H[m] / 2))
                x[m] = xn; y[m] = yn; vx[m] = vxn; vy[m] = vyn
        t += H / 2
        # kicks at midpoint
        for frame in (False, True):
            m = act & (inside == frame)
            if m.any():
                if frame:
                    ax, ay = planet.accel(x[m], y[m], t[m])
                else:
                    ax, ay = helio.accel(x[m], y[m], t[m])
                vx[m] += ax * H[m]; vy[m] += ay * H[m]
        kicks += act
        for frame, gm in ((False, 1.0 - MU), (True, MU)):
            m = act & (inside == frame)
            if m.any():
                xn, yn, vxn, vyn = drift(x[m], y[m], vx[m], vy[m], gm, (H[m] / 2))
                x[m] = xn; y[m] = yn; vx[m] = vxn; vy[m] = vyn
        t += H / 2
        # record Jacobi (convert planet frame to helio)
        if C_every is not None and (guard % C_every == 0):
            xs = np.where(inside, x + SEP * np.cos(t), x)
            ys = np.where(inside, y + SEP * np.sin(t), y)
            vxs = np.where(inside, vx - SEP * np.sin(t), vx)
            vys = np.where(inside, vy + SEP * np.cos(t), vy)
            C = jacobi(xs, ys, vxs, vys, t)
            for m in range(n):
                if act[m]:
                    Cs[m].append((t[m], (C[m] - C0[m]) / abs(C0[m])))
                    Cs[m].append((t[m], (C[m] - C0[m]) / abs(C0[m])))
        done = t >= t_end - 1e-12
    return C0, Cs, crossings, kicks


def growth(errs):
    """log-log slope of the running max of the error series."""
    ts = np.array([e[0] for e in errs]); es = np.array([e[1] for e in errs])
    m = es > 1e-12
    if m.sum() < 3:
        return 0.0, es.max() if len(es) else 0.0
    runmax = np.maximum.accumulate(es[m])
    A = np.vstack([np.log(ts[m][1:]), np.ones(m.sum() - 1)]).T
    sol, *_ = np.linalg.lstsq(A, np.log(runmax[1:]), rcond=None)
    return sol[0], es.max()


    for N in ([8, 32] if mode == "smoke" else [8, 16, 32, 64, 128]):
        C0b, Csb, crb, kkb = simulate([s[i] for i in keep], lambda a, e, rr: N, N, C_every=32)
        exps = []; worst = 0.0
        for m in range(len(keep)):
            ex, mx = growth(Csb[m])
            exps.append(ex); worst = max(worst, mx)
        med = np.median(exps)
        print(f"N={N}: max|dC/C|={worst:.2e} median exponent={med:.3f} kicks/body={kkb.mean():.0f} crossings min={min(crb.tolist()) if len(crb) else 0}")
        res[N] = dict(worst=float(worst), med_exp=float(med), kicks=float(kkb.mean()))
    json.dump(res, open(f"b12_{'smoke' if mode=='smoke' else 'full'}.json", "w"), indent=1)
