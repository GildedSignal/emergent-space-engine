"""Belt-scale cadence test: is the kick cadence one mechanism (f') or three (cadence rule, skin, secular carrier)?

Heliocentric restricted 3-body, planet on an exact circular orbit (mu=0.01, a_P=4).
Wisdom-Holman split: exact Kepler drift (the compiled tube) + kicks from the planet
(direct + indirect term). Truth = fixed dt at KICKS_TRUE per body orbit.

Variants (all integrate the SAME bodies; only the kick schedule differs):
  fixed-N     : dt = P_b/N always (the plane's standing rhythm)
  adapt-N     : v2-style dt = ds * f'(U_P + c), composite f'(y) = 1/y^2 + 1/(b y),
                ds set so the far-field cadence is N per orbit (one smooth function
                of the state; no windows, no switch)
  win-N       : skin only: kicks at dt = P_b/N_inside while d < R_win; outside, exact
                Kepler jumps in P_b/16 chunks until the window opens (position-only checks)
  winsec-N-M  : win-N plus one kick every P_b/M outside the window (secular carrier)

Metrics vs truth: pump ratio = (max e - e0)/(max e_truth - e0); dWpi error = |total
unwrapped d(varpi) - truth's| / max(|truth's|, 0.05 rad); final |e - e_truth|;
kicks used per body orbit; Jacobi drift of each map (sanity, not a bar).
"""
import numpy as np, json, time, sys
SCENES = {"hard": (3.4, 0.15, 1.2, 60, 512), "belt": (2.35, 0.05, 1.9, 120, 1024)}[sys.argv[1] if len(sys.argv)>1 else "belt"]
A0G, E0G, RWIN, ORBITS, KICKS_TRUE = SCENES
e0g = E0G

MU = 0.01
AP = 4.0
NP_ = np.sqrt((1.0 + MU) / AP**3)
RWIN = 1.9
RH = AP * (MU / 3.0) ** (1.0 / 3.0)          # planet Hill radius
CC = MU / RH                                   # v2 constant c
BB = 30.0 * CC                                 # v2 constant b
E0 = E0G
SEEDS = 6
ORBITS = ORBITS
KICKS_TRUE = KICKS_TRUE

def planet(t):
    return np.stack([AP * np.cos(NP_ * t), AP * np.sin(NP_ * t)], -1)

def elems(r, v):
    r2 = np.sum(r * r, -1); vv = np.sum(v * v, -1); rn = np.sqrt(r2)
    a = 1.0 / (2.0 / rn - vv)
    ev = (vv - 1.0 / rn)[..., None] * r - np.sum(r * v, -1)[..., None] * v
    e = np.sqrt(np.sum(ev * ev, -1))
    return a, e, ev, rn

def drift(r, v, dt):
    """Exact Kepler drift about GM=1 (the tube read)."""
    a, e, ev, rn = elems(r, v)
    ex, ey = ev[..., 0], ev[..., 1]
    ee = np.maximum(e, 1e-12)
    cw = np.where(e < 1e-9, 1.0, ex / ee); sw = np.where(e < 1e-9, 0.0, ey / ee)
    rv = np.sum(r * v, -1)
    cE = np.clip((1.0 - rn / a) / ee, -1, 1); sE = np.clip(rv / (ee * np.sqrt(a)), -1, 1)
    E = np.arctan2(sE, cE)
    M = E - e * np.sin(E)
    M = M + dt * a**-1.5
    for _ in range(6):
        E = M + e * np.sin(E)
    cE, sE = np.cos(E), np.sin(E)
    rn = a * (1.0 - e * cE)
    sn = np.sqrt(np.maximum(1 - e * e, 0.0))
    nu = np.arctan2(sn * sE, cE - e)
    ang = np.arctan2(sw, cw) + nu
    h = np.sqrt(np.maximum(a * (1 - e * e), 1e-18))
    r = np.stack([rn * np.cos(ang), rn * np.sin(ang)], -1)
    vp = np.stack([-np.sin(ang), np.cos(ang)], -1) * ((1.0 + e * np.cos(nu)) * h / rn**2)[..., None]
    vr = np.stack([np.cos(ang), np.sin(ang)], -1) * ((e * np.sin(nu)) * h / rn**2)[..., None]
    return r, vr + vp

def force(r, t):
    rp = planet(t)
    d = rp - r
    dn = np.sqrt(np.sum(d * d, -1))
    return MU * (d / dn[..., None] ** 3 - rp / AP**3), dn

def fpri(y):
    return 1.0 / y**2 + 1.0 / (BB * y)

def upot(dn):
    return MU / dn

def jacobi(r, v, t):
    rp = planet(t); vp = NP_ * np.stack([-rp[:, 1], rp[:, 0]], -1)
    rb = r - MU / (1 + MU) * rp
    vb = v - MU / (1 + MU) * vp
    vrot = vb + NP_ * np.stack([-rb[:, 1], rb[:, 0]], -1)
    dn = np.sqrt(np.sum((r - rp) ** 2, -1))
    rn = np.sqrt(np.sum(r * r, -1))
    return 2 * (1.0 / rn + MU / dn) + NP_**2 * np.sum(rb * rb, -1) - np.sum(vrot * vrot, -1)

def init(a0, seed):  # uses global E0
    rng = np.random.default_rng(seed)
    M0 = rng.uniform(0, 2 * np.pi, SEEDS)
    w0 = rng.uniform(0, 2 * np.pi, SEEDS)
    nu = 2 * np.arctan2(np.sqrt(1 + E0) * np.sin(M0 / 2), np.sqrt(1 - E0) * np.cos(M0 / 2))
    rn = a0 * (1 - E0 * np.cos(M0))
    ang = w0 + nu
    r = np.stack([rn * np.cos(ang), rn * np.sin(ang)], -1)
    h = np.sqrt(a0 * (1 - E0**2))
    vp = np.stack([-np.sin(ang), np.cos(ang)], -1) * ((1 + E0 * np.cos(nu)) * h / rn**2)[..., None]
    vr = np.stack([np.cos(ang), np.sin(ang)], -1) * ((E0 * np.sin(nu)) * h / rn**2)[..., None]
    return r, vr + vp

def run(a0, policy, N=16, inside=64, outM=4):
    r, v = init(a0, 20261007)
    Pb = a0**1.5
    T = ORBITS * Pb
    t = np.zeros(SEEDS)
    _, dn = force(r, t)
    kicks = np.zeros(SEEDS)
    checks = np.zeros(SEEDS)  # position-only window checks (skin certificate cost)
    maxe = np.full(SEEDS, E0)
    wpi = np.zeros(SEEDS)
    C0 = jacobi(r, v, t)
    Cworst = np.zeros(SEEDS)
    # far-field ds for adapt: dt_far = ds * f'(U_far), U_far ~ mu / (aP - a0)
    Ufar = MU / (AP - a0)
    ds = (Pb / N) / fpri(Ufar)
    mode = np.zeros(SEEDS, dtype=int)  # 0 outside (win policies), 1 inside
    if policy == "fixed":
        dt = np.full(SEEDS, Pb / N)
    elif policy == "adapt":
        dt = np.full(SEEDS, ds * fpri(upot(dn) + CC))
    elif policy in ("win", "winsec"):
        mode = (dn < RWIN).astype(int)
        dt = np.where(mode == 1, Pb / inside, Pb / 16)
    last_e = np.full(SEEDS, E0)
    step = 0
    while np.any(t < T - 1e-12):
        if policy in ("win", "winsec"):
            outside = mode == 0
            if policy == "winsec" and np.any(outside):
                dt = np.where(mode == 1, Pb / inside, Pb / outM)
            else:
                dt = np.where(mode == 1, Pb / inside, Pb / 16)
                checks += outside
        dt = np.minimum(dt, T - t + 1e-12)
        if policy == "adapt":
            F, dn = force(r, t)
            dt = np.minimum(ds * fpri(upot(dn) + CC), T - t + 1e-12)
            r, v = drift(r, v, dt / 2)
            F, dn = force(r, t)
            v = v + dt[:, None] * F
            r, v = drift(r, v, dt / 2)
            kicks += 1
        elif policy == "fixed":
            r, v = drift(r, v, dt / 2)
            F, dn = force(r, t)
            v = v + dt[:, None] * F
            r, v = drift(r, v, dt / 2)
            kicks += 1
        else:
            F, dn = force(r, t)
            newmode = (dn < RWIN).astype(int)
            # kicks only for inside bodies (and winsec's outside cadence)
            do_kick = (mode == 1) | (policy == "winsec")
            r, v = drift(r, v, dt / 2)
            F, dn = force(r, t)
            v = v + np.where(do_kick, dt, 0.0)[:, None] * F
            r, v = drift(r, v, dt / 2)
            kicks += do_kick
            mode = newmode
        t = t + dt
        a, e, ev, rn = elems(r, v)
        maxe = np.maximum(maxe, e)
        w = np.arctan2(ev[..., 1], ev[..., 0])
        dw = np.mod(w - last_e + np.pi, 2 * np.pi) - np.pi
        wpi = wpi + dw
        last_e = w
        Cworst = np.maximum(Cworst, np.abs(jacobi(r, v, t) - C0))
        step += 1
    # exact drift to T for comparison
    r, v = drift(r, v, T - t)
    return dict(kicks_orbit=kicks.mean() / ORBITS, checks_orbit=checks.mean() / ORBITS,
                maxe=maxe, wpi=wpi, e_final=elems(r, v)[1], Cworst=Cworst.max())

def compare(name, res, truth, a0):
    pump = (res["maxe"] - E0) / np.maximum(truth["maxe"] - E0, 1e-9)
    dwpi = np.abs(res["wpi"] - truth["wpi"])
    dwpirel = dwpi / max(np.abs(truth["wpi"]).mean(), 0.05)
    de = np.abs(res["e_final"] - truth["e_final"])
    row = dict(scene=a0, variant=name, kicks=round(res["kicks_orbit"], 2),
               checks=round(res["checks_orbit"], 2),
               pump_med=round(float(np.median(pump)), 3),
               pump_ok=int(np.sum((pump > 0.8) & (pump < 1.25))),
               dwpi_rel_med=round(float(np.median(dwpirel)), 4),
               de_med=round(float(np.median(de)), 5),
               de_ok=int(np.sum(de < 0.01)),
               Cworst=float(res["Cworst"]))
    return row

def main():
    t0 = time.time()
    out = []
    for a0 in ([A0G, A0G*4/2.52**0 if False else A0G] if False else [A0G]):
        truth = run(a0, "fixed", N=KICKS_TRUE)
        half = run(a0, "fixed", N=KICKS_TRUE // 2)
        conv = float(np.abs(half["wpi"] - truth["wpi"]).mean())
        out.append(dict(scene=a0, conv_dWpi_1024_vs_512=conv))
        for nm, pol, kw in [
            ("fixed-8", "fixed", dict(N=8)), ("fixed-16", "fixed", dict(N=16)),
            ("fixed-32", "fixed", dict(N=32)), ("fixed-64", "fixed", dict(N=64)),
            ("adapt-16", "adapt", dict(N=16)),
            ("adapt-8", "adapt", dict(N=8)),
            ("win-64", "win", dict(inside=64)),
            ("win-128", "win", dict(inside=128)),
        ]:
            res = run(a0, pol, **kw)
            out.append(compare(nm, res, truth, a0))
    print(json.dumps(out, indent=1))
    with open(f"belt_cadence_{sys.argv[1] if len(sys.argv)>1 else 'belt'}.json", "w") as f:
        json.dump(out, f, indent=1)
    print("wall", round(time.time() - t0, 1), "s")

if __name__ == "__main__":
    main()
