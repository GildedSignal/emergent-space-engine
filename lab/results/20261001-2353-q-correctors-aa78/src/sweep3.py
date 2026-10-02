import numpy as np, sys, json
sys.path.insert(0, ".")
from replica import *

MU = 2.0 ** -10 / (1 + 2.0 ** -10)      # planet (Giant) mass fraction, total mass 1
GM_P, GM_S = MU, 1.0 - MU
n = 1.0
RSOI = 0.0403

def planet_state(t):
    ang = n * t
    xp = np.array([(1 - MU) * np.cos(ang), (1 - MU) * np.sin(ang)])
    vp = np.array([-n * (1 - MU) * np.sin(ang), n * (1 - MU) * np.cos(ang)])
    xs = np.array([-MU * np.cos(ang), -MU * np.sin(ang)])
    return xp, vp, xs

def cj_rot(st, t):
    """barycentric rotating Jacobi constant, n=1, total mass 1 (moonlets, doll 1)."""
    xp, vp, xs = planet_state(t)
    r = st[:, :2] + xp[None, :]
    w = st[:, 2:] + vp[None, :]
    vrot = np.stack([w[:, 0] + r[:, 1], w[:, 1] - r[:, 0]], axis=1)
    r1 = np.linalg.norm(r - xs[None, :], axis=1)
    r2 = np.linalg.norm(st[:, :2], axis=1)
    Om = 0.5 * np.sum(r * r, axis=1) + GM_S / r1 + GM_P / r2
    return 2 * Om - np.sum(vrot * vrot, axis=1)

# ---------------- part A: moonlets entirely inside the doll (plane-faithful doll 1)
moonlets = [(0.3, 0.15, 0.3, 0.1, +1), (0.5, 0.25, 2.0, 1.0, +1),
            (0.7, 0.35, 4.0, 2.5, -1), (0.9, 0.4, 5.5, 4.2, +1)]   # (a/RSOI, e, varpi, M0, dir)
sta = []
for f, e, w, M0, d in moonlets:
    s = state_from_elements(GM_P, f * RSOI, e, w, M0)
    if d < 0:
        s[2:] *= -1.0
    sta.append(s)
sta = np.stack(sta)
Pa = TWOPI * np.sqrt((np.array([m[0] for m in moonlets]) * RSOI) ** 3 / GM_P)
Ta = 40.0

def tide_accel(st, t):
    xp, vp, xs = planet_state(t)
    u = st[:, :2] + xp[None, :] - xs[None, :]
    r = np.linalg.norm(u, axis=1)
    up = xp - xs
    return -GM_S * u / r[:, None] ** 3 + GM_S * up

def runA(scheme, k):
    gm = np.full(4, GM_P)
    it = Integrator(scheme, gm, tide_accel)
    cj0 = cj_rot(sta, 0.0)
    errs = np.zeros((5, 4)); errs[0] = 0
    for i in range(int(round(Ta / (Pa[1] / 2 ** k)))):
        for m in range(4):
            pass
    # step all moonlets with a shared tau (mid period) but sample per body period
    tau = Pa[1] / 2 ** k
    ns = int(round(Ta / tau))
    cnt = 1
    for i in range(ns):
        st = it.step(sta.copy() if i == 0 else st, tau)
        cnt += 1
    return None  # replaced below

def runA(scheme, k):
    gm = np.full(4, GM_P)
    it = Integrator(scheme, gm, tide_accel)
    st = sta.copy()
    cj0 = cj_rot(st, 0.0)
    maxe = np.zeros(4)
    hist = [[0.0] for _ in range(4)]
    tau0 = Pa / 2 ** k
    # each moonlet with its own cadence (the plane: per-body step)
    its = [Integrator(scheme, [GM_P], tide_accel) for _ in range(4)]
    sts = [sta[m:m + 1].copy() for m in range(4)]
    for m in range(4):
        ns = int(round(Ta / tau0[m]))
        ev = ns // 200
        c0 = cj_rot(sts[m], 0.0)[0]
        err = 0.0
        sl = []
        for i in range(ns):
            sts[m] = its[m].step(sts[m], tau0[m])
            if (i + 1) % ev == 0:
                e = abs(cj_rot(sts[m], its[m].t)[0] - c0) / abs(c0)
                err = max(err, e); sl.append(e)
        tt = np.arange(1, len(sl) + 1) * ev * tau0[m]
        s2 = slice(len(sl) // 4, None)
        slope = np.polyfit(np.log(tt[s2]), np.log(np.maximum(np.array(sl)[s2], 1e-300)), 1)[0] if max(sl) > 0 else 0
        maxe[m] = err
        hist[m] = [float(x) for x in sl[::max(1, len(sl) // 10)]]
    return [dict(maxerr=float(maxe[m]), slope=float(slope if m == m else 0)) for m in range(4)] + [None][:0] or [
        dict(maxerr=float(maxe[m]), slope=hist_slope) for m, hist_slope in [(0, 0)]]

# simpler, correct implementation
def runA2(scheme, k):
    out = []
    for m in range(4):
        it = Integrator(scheme, [GM_P], tide_accel)
        st = sta[m:m + 1].copy()
        tau = Pa[m] / 2 ** k
        ns = int(round(Ta / tau))
        ev = max(1, ns // 200)
        c0 = cj_rot(st, 0.0)[0]
        sl = []
        for i in range(ns):
            st = it.step(st, tau)
            if (i + 1) % ev == 0:
                sl.append(abs(cj_rot(st, it.t)[0] - c0) / abs(c0))
        tt = np.arange(1, len(sl) + 1) * ev * tau
        s2 = slice(len(sl) // 4, None)
        slope = np.polyfit(np.log(tt[s2]), np.log(np.maximum(np.array(sl)[s2], 1e-300)), 1)[0] if max(sl) > 0 else 0.0
        out.append(dict(maxerr=float(max(sl)), slope=float(slope)))
    return out

# ---------------- part B: heliocentric crossers in doll 0 (direct planet pull)
flybys = [(0.85, 0.32, 0.3, 0.1), (0.95, 0.25, 2.2, 1.0), (0.9, 0.28, 4.0, 2.5), (0.88, 0.3, 5.5, 4.2)]
stb = []
for a, e, w, M0 in flybys:
    s = state_from_elements(GM_S, a, e, w, M0)
    stb.append(s)
stb = np.stack(stb)
Pb = TWOPI * np.sqrt(np.array([f[0] for f in flybys]) ** 3 / GM_S)
Tb = 120.0

def pull_accel(st, t):
    xp, vp, xs = planet_state(t)
    u = st[:, :2] - xp[None, :]
    r = np.linalg.norm(u, axis=1)
    return -GM_P * u / r[:, None] ** 3

def helio_E(st, t):
    xp, vp, xs = planet_state(t)
    pos = st[:, :2] - xs[None, :]           # star-centric (star at xs)
    vel = st[:, 2:]                          # star-fixed frame velocities
    r1 = np.linalg.norm(pos, axis=1)
    r2 = np.linalg.norm(st[:, :2], axis=1)
    return 0.5 * np.sum(vel * vel, axis=1) - GM_S / r1 - GM_P / r2

def helio_L(st, t):
    xp, vp, xs = planet_state(t)
    pos = st[:, :2] - xs[None, :]
    vel = st[:, 2:]
    return pos[:, 0] * vel[:, 1] - pos[:, 1] * vel[:, 0]

def runB(scheme, k):
    its = [Integrator(scheme, [GM_S], pull_accel) for _ in range(4)]
    EL = [[] for _ in range(4)]
    for m in range(4):
        st = stb[m:m + 1].copy()
        tau = Pb[m] / 2 ** k
        ns = int(round(Tb / tau))
        prev_in = np.linalg.norm(st[0, :2] - planet_state(0)[0]) < RSOI
        for i in range(ns):
            st = its[m].step(st, tau)
            ins = np.linalg.norm(st[0, :2] - planet_state(its[m].t)[0]) < RSOI
            if prev_in and not ins:
                EL[m].append((float(helio_E(st, its[m].t)[0]), float(helio_L(st, its[m].t)[0])))
            prev_in = ins
    return [[list(x) for x in EL[m]] for m in range(4)]

resA = {"runs": {}}
for kref in (10, 11):
    resA[f"ref{kref}"] = runA2("dkd", kref)
    print("A ref", kref, [(f"{r['maxerr']:.1e}", f"{r['slope']:+.2f}") for r in resA[f"ref{kref}"]], flush=True)
for scheme in ("dkd", "saba2", "saba3", "whc3", "whc3b"):
    for k in (1, 2, 3, 4, 5, 6, 7):
        r = runA2(scheme, k)
        resA["runs"][f"{scheme}_k{k}"] = dict(kicks_per_orbit=KICKS_PER_STEP[scheme] * 2 ** k, moons=r)
        print("A", scheme, k, [(f"{x['maxerr']:.1e}", f"{x['slope']:+.2f}") for x in r], flush=True)

resB = {"runs": {}}
for kref in (11,):
    resB[f"ref{kref}"] = runB("dkd", kref)
    print("B ref", kref, [[f"{E:.6f}" for E, L in m][:2] for m in resB[f"ref{kref}"]], flush=True)
for scheme in ("dkd", "saba2", "saba3", "whc3"):
    for k in (2, 3, 4, 5, 6, 7):
        r = runB(scheme, k)
        resB["runs"][f"{scheme}_k{k}"] = dict(kicks_per_orbit=KICKS_PER_STEP[scheme] * 2 ** k, ships=r)
        ref = resB["ref11"]
        worst = 0.0
        for m in range(4):
            for i, (E, L) in enumerate(r[m]):
                if i < len(ref[m]):
                    worst = max(worst, abs(E / ref[m][i][0] - 1))
        print("B", scheme, k, "worst dE/E across passes: %.2e" % worst, "n:", [len(x) for x in r], flush=True)
json.dump({"A": resA, "B": resB}, open("../s3.json", "w"), indent=1)
print("saved")
