#!/usr/bin/env python3
# Second author 20261007-0528-...-67be: the checker's named gold experiment.
# A cadence study on a resonance lattice (2:1, 3:2, 3:1, 5:3; detunings 0,
# +-2/3 W, +-2 W in first-order-equivalent units; 3 phases; horizons 100 and
# 200 orbits), cost counted in TIDE EVALS + anchors (not bare kicks), with
# de-phased (DEPH-2.5, GOLDEN) and grid-anchored trigger (TRIG2G) policies the
# original run lacked. Core layer/truth copied verbatim from cadence.py (the
# run's shipped code); only instrumentation added.
import math, time, os, json, sys

MU = 1e-3
W = 2.5*MU**(2.0/3.0)          # resonance half-width scale, fractional freq (S2d's definition)

def prop(GM, st, t):
    a, e, w, M0, t0 = st
    M = M0 + math.sqrt(GM/(a*a*a))*(t - t0)
    Ea = M
    for _ in range(8): Ea -= (Ea - e*math.sin(Ea) - M)/(1.0 - e*math.cos(Ea))
    cE = math.cos(Ea); sE = math.sin(Ea)
    b = a*math.sqrt(1.0-e*e); r = a*(1.0-e*cE); g = math.sqrt(GM*a)/r
    xp = a*(cE-e); yp = b*sE; vxp = -g*sE; vyp = g*(b/a)*cE
    cw = math.cos(w); sw = math.sin(w)
    return xp*cw-yp*sw, xp*sw+yp*cw, vxp*cw-vyp*sw, vxp*sw+vyp*cw

def elems(GM, x, y, vx, vy):
    r = math.hypot(x, y); v2 = vx*vx + vy*vy
    a = GM/(2.0*GM/r - v2); rv = x*vx + y*vy; q = v2 - GM/r
    ex = (q*x - rv*vx)/GM; ey = (q*y - rv*vy)/GM
    e = math.hypot(ex, ey); w = math.atan2(ey, ex)
    nu = math.atan2(y, x) - w
    ec = min(e, 0.995)
    Ea = 2.0*math.atan2(math.sqrt(1.0-ec)*math.sin(0.5*nu), math.sqrt(1.0+ec)*math.cos(0.5*nu))
    return a, e, w, Ea - e*math.sin(Ea)

def per_pos(p, t):
    c, s = math.cos(p["n"]*t), math.sin(p["n"]*t)
    return p["d"]*c, p["d"]*s

def tide(sc, x, y, t):
    ax = ay = 0.0
    for p in sc["per"]:
        px, py = per_pos(p, t)
        pr = math.hypot(px, py)
        mx = px - x; my = py - y
        d2 = mx*mx + my*my; dd = d2*math.sqrt(d2)
        ax += p["mu"]*(mx/dd - px/pr**3)
        ay += p["mu"]*(my/dd - py/pr**3)
    return ax, ay

# ---------------- lattice scenes ----------------
# resonance R = P_per/P_b = p/q with q n_b = p n_per at centre (body a detuned
# by eps = delta*W/q so that Delta_1/W = |delta| identically for every lattice
# row; first-order rows: 2:1, 3:2 (p-q=1); second-order: 3:1, 5:3 (p-q=2)).
LAT = [((2,1)), ((3,2)), ((3,1)), ((5,3))]
DELTAS = [0.0, -2/3, 2/3, -2.0, 2.0]
PHASES = [0.0, math.pi/4, math.pi/2]

def scene(pq, delta, ph, n_orb=200):
    p, q = pq
    eps = delta*W/q                      # fractional mean-motion offset from exact centre
    a_body = (1.0+eps)**(-2.0/3.0)       # n_b = 1+eps, GM = 1
    d = p**(2.0/3.0)/q**(2.0/3.0)       # perturber placed at exact commensurability
    nper = 1.0/d**1.5
    D1 = abs(q*(1.0+eps) - p*nper)       # first-order-relevant distance, n_b units
    return dict(GM=1.0, per=[dict(mu=MU, d=d, n=nper)], a=a_body, e=0.02,
                n_orb=n_orb, ts=1024, t0_ph=ph, pq=f"{p}:{q}", delta=delta,
                eps=eps, D1_over_W=D1/W, dPdW=(q*(1.0+eps)-p*nper)/W)

def scene_S1(n_orb=60):
    GM = 3.986004418e14
    per = [dict(mu=4.9048695e12, d=3.844e8, n=2*math.pi/(27.321661*86400.0)),
           dict(mu=1.32712440018e20, d=1.495978707e11, n=2*math.pi/(365.256363*86400.0))]
    return dict(GM=GM, per=per, a=6.771e6, e=0.0, n_orb=n_orb, ts=1024,
                t0_ph=0.0, pq="S1", delta=0.0, eps=0.0, D1_over_W=1e9, dPdW=1e9)

def scene_S3():
    dP = (1.0 - 4*2.5**-1.5)/W   # nearest commensurability 4:1 (second order)
    return dict(GM=1.0, per=[dict(mu=MU, d=2.5, n=1.0/2.5**1.5)], a=1.0, e=0.3,
                n_orb=200, ts=1024, t0_ph=0.0, pq="S3", delta=0.0, eps=0.0,
                D1_over_W=abs(dP), dPdW=dP)

# ---------------- truth with horizon snapshots ----------------
def truth_snap(sc, horizons):
    GM = sc["GM"]; n = sc["n_orb"]; ts = sc["ts"]
    a0 = sc["a"]; P = 2*math.pi*math.sqrt(a0**3/GM); dt = P/ts
    M0 = sc["t0_ph"]; e = sc["e"]
    Ea = M0
    for _ in range(10): Ea -= (Ea - e*math.sin(Ea) - M0)/(1.0 - e*math.cos(Ea))
    cE, sE = math.cos(Ea), math.sin(Ea)
    b = a0*math.sqrt(1-e*e); r = a0*(1-e*cE); g = math.sqrt(GM*a0)/r
    x = a0*(cE-e); y = b*sE; vx = -g*sE; vy = g*(b/a0)*cE
    t = 0.0
    snaps = {}
    def acc(x, y, t):
        ax, ay = tide(sc, x, y, t)
        r3 = math.hypot(x, y)**3
        return ax - GM*x/r3, ay - GM*y/r3
    hs = sorted(horizons)
    for i in range(n*ts):
        k1 = acc(x, y, t); k1 = (vx, vy, k1[0], k1[1])
        k2 = acc(x+0.5*dt*k1[0], y+0.5*dt*k1[1], t+0.5*dt)
        k2 = (vx+0.5*dt*k1[2], vy+0.5*dt*k1[3], k2[0], k2[1])
        k3 = acc(x+0.5*dt*k2[0], y+0.5*dt*k2[1], t+0.5*dt)
        k3 = (vx+0.5*dt*k2[2], vy+0.5*dt*k2[3], k3[0], k3[1])
        k4 = acc(x+dt*k3[0], y+dt*k3[1], t+dt)
        k4 = (vx+dt*k3[2], vy+dt*k3[3], k4[0], k4[1])
        x += dt/6.0*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
        y += dt/6.0*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        vx += dt/6.0*(k1[2]+2*k2[2]+2*k3[2]+k4[2])
        vy += dt/6.0*(k1[3]+2*k2[3]+2*k3[3]+k4[3])
        t += dt
        while hs and (i+1) >= hs[0]*ts:
            af, ef, _, _ = elems(GM, x, y, vx, vy)
            snaps[hs.pop(0)] = (af, ef)
    return snaps

# ---------------- instrumented layer ----------------
PHI = 1.6180339887498949

def layer2(sc, policy, kappa=None, n_fixed=None, horizons=(50, 100), rate=None, grid=None):
    """cadence.py's layer() + eval/anchor counting + horizon snapshots.
    grid: if set, tau is snapped UP to a multiple of P0/grid (anchored steps)."""
    GM = sc["GM"]; n_orb = sc["n_orb"]
    a0 = sc["a"]; P0 = 2*math.pi*math.sqrt(a0**3/GM)
    M0 = sc["t0_ph"]; e = sc["e"]
    Ea = M0
    for _ in range(10): Ea -= (Ea - e*math.sin(Ea) - M0)/(1.0 - e*math.cos(Ea))
    cE, sE = math.cos(Ea), math.sin(Ea)
    b = a0*math.sqrt(1-e*e); r = a0*(1-e*cE); g = math.sqrt(GM*a0)/r
    x = a0*(cE-e); y = b*sE; vx = -g*sE; vy = g*(b/a0)*cE
    st = (a0, e, 0.0, M0, 0.0)
    t = 0.0; kicks = 0; walls = 0; ev = 0; anchors = 0; bisect = 0
    hs = sorted(horizons); snaps = {}
    T_end = n_orb*P0
    gstep = P0/grid if grid else None
    while t < T_end - 1e-9:
        P = 2*math.pi*math.sqrt(st[0]**3/GM)
        if policy == "FIXED":
            tau = P/n_fixed
        elif policy == "AVG":
            tau = P
        elif policy == "DEPH":
            tau = P/rate
        elif policy == "GOLD":
            tau = P/PHI
        elif policy in ("TRIG", "TRIG2", "TRIG2G"):
            a_now = tide(sc, x, y, t); ev += 1
            amag = math.hypot(*a_now)
            h = P/1000.0
            x1, y1, _, _ = prop(GM, st, t+h)
            a1 = tide(sc, x1, y1, t+h); ev += 1
            J = math.hypot(a1[0]-a_now[0], a1[1]-a_now[1])/h
            ref = kappa*P*max(amag, J*P/1024.0)
            if policy in ("TRIG", "TRIG2G"):
                f = lambda tau: 0.5*J*tau*tau*(1+tau/P) - ref
            else:
                f = lambda tau: 0.5*J*tau*tau*(1+tau/P) - ref*math.sqrt(tau/P)
            lo, hi = 0.0, P
            if f(hi) < 0:
                tau = hi
            else:
                for _ in range(60):
                    mid = 0.5*(lo+hi)
                    if f(mid) < 0: lo = mid
                    else: hi = mid
                bisect += 60
                tau = lo
            if policy == "TRIG2G" and gstep:
                import math as _m
                tau = max(gstep, _m.ceil(tau/gstep - 1e-12)*gstep)
            if tau < P/64.0:
                tau = P/64.0; walls += 1
        else:
            raise KeyError(policy)
        xe, ye, vxe, vye = prop(GM, st, t+0.5*tau)
        ax, ay = tide(sc, xe, ye, t+0.5*tau); ev += 1
        xe, ye, vxe, vye = prop(GM, st, t+tau)
        vx = vxe + ax*tau; vy = vye + ay*tau
        t += tau; kicks += 1; anchors += 1
        while hs and t >= hs[0]*P0 - 1e-9:
            af, ef, _, _ = elems(GM, xe, ye, vx, vy)
            snaps[hs[0]] = (af, ef, kicks/hs[0])
            hs.pop(0)
        newel = elems(GM, x if False else xe, ye, vx, vy)
        if newel[1] > 0.995 or not (0.1*a0 < newel[0] < 10*a0):
            for h in hs: snaps[h] = (float("nan"), float("nan"), kicks/h)
            return dict(snaps=snaps, kicks=kicks, walls=walls, ev=ev,
                        anchors=anchors, bisect=bisect, unbound=True)
        st = (newel + (t,))
        x, y = xe, ye
    af, ef, _, _ = elems(GM, *prop(GM, st, T_end))
    for h in hs: snaps[h] = (af, ef, kicks/h)
    return dict(snaps=snaps, kicks=kicks, walls=walls, ev=ev, anchors=anchors,
                bisect=bisect, unbound=False)

POLICIES = [("FIXED", dict(n_fixed=n)) for n in (2, 4, 8, 16, 32, 64)] \
         + [("AVG", {}), ("DEPH", dict(rate=2.5)), ("GOLD", {})] \
         + [("TRIG", dict(kappa=0.25)), ("TRIG", dict(kappa=0.5))] \
         + [("TRIG2", dict(kappa=k)) for k in (0.125, 0.5, 2.0)] \
         + [("TRIG2G", dict(kappa=2.0, grid=4096))]

def pol_key(pol, kw):
    if pol == "FIXED": return f"FIXED-{kw['n_fixed']}"
    if pol == "DEPH": return f"DEPH-{kw['rate']}"
    if pol in ("TRIG", "TRIG2", "TRIG2G"): return f"{pol}-{kw['kappa']}"
    return pol

def run_row(sc, horizons):
    t0 = time.time()
    ts_ = truth_snap(sc, horizons)
    out = dict(pq=sc["pq"], delta=sc["delta"], dPdW=sc["dPdW"], eps=sc["eps"],
               phase=sc["t0_ph"], truth={}, wall_truth=time.time()-t0)
    for h in horizons:
        out["truth"][str(h)] = dict(a=ts_[h][0], e=ts_[h][1])
    for pol, kw in POLICIES:
        t0 = time.time()
        r = layer2(sc, pol, horizons=horizons, **kw)
        row = dict(kicks=r["kicks"], ev=r["ev"], anchors=r["anchors"],
                   bisect=r["bisect"], walls=r["walls"], unbound=r["unbound"],
                   wall=round(time.time()-t0, 2))
        for h in horizons:
            af, ef, kpo = r["snaps"][h]
            at, et = ts_[h]
            row[f"h{h}"] = dict(
                kpo=kpo, a=af, e=ef,
                da_rel=abs(af-at)/at if af == af else float("nan"),
                epump=(ef/et) if (et > 1e-12 and ef == ef) else float("nan"))
        out[pol_key(pol, kw)] = row
    return out

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "pilot"
    res = {}
    t00 = time.time()
    if which == "pilot":
        sc = scene((2, 1), 0.0, 0.0)
        res["2:1_c_p0"] = run_row(sc, (100, 200))
    elif which == "full":
        for pq in LAT:
            for dl in DELTAS:
                for ph in PHASES:
                    key = f"{pq[0]}{pq[1]}_d{dl:+.3f}_p{PHASES.index(ph)}"
                    res[key] = run_row(scene(pq, dl, ph), (100, 200))
        res["S3"] = run_row(scene_S3(), (100, 200))
        res["S1"] = run_row(scene_S1(), (30, 60))
    elif which == "one":
        res["x"] = run_row(scene((3, 2), 0.0, 0.0), (100, 200))
    print(json.dumps(res, indent=1))
    with open(f"out_{which}.json", "w") as f:
        json.dump(res, f, indent=1)
    print(f"total_wall={time.time()-t00:.1f}s load={os.getloadavg()[0]:.2f}", file=sys.stderr)
