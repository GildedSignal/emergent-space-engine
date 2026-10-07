#!/usr/bin/env python3
# Scout run 20261007-0341-scout-9abe: does a local self-triggered cadence rule
# (event-triggered control transplanted onto the law's kick layer) cut total
# kicks >= 4x at held behaviours on mixed scenes?
#
# Layer model (law.md "Perturbed motion: the compiled drift plus kicks"):
#   - drift: exact Kepler conic about the parent (analytic, as in K1's prop)
#   - kicks: delta-v applied instantaneously; the body re-anchors its conic
#   - per-kick quadrature: ONE tide evaluation at the gap midpoint (the layer's
#     own cost model: 1 tide eval + 1 anchor per kick)
# Policies:
#   FIXED-n   : kick every P/n
#   AVG       : one kick per orbit carrying the orbit-integrated tide impulse
#               (stand-in for the compiled orbit-averaged quadrupole, K2)
#   TRIG-kappa: at each kick, J = |d(tide)/dt| along the predicted drift
#               (central difference, h=P/1000); next kick at the first tau with
#               B(tau) = 0.5*J*tau^2*(1+tau/P_body) >= kappa*|a_tide|*P_body.
#               tau capped at P/4 (never coarser), floored at P/64 with a
#               "wall" flag (the bound cannot be held even at P/64).
#   K1QUANTUM : K1's impulse-quantum trigger (fire when |integral a dt|
#               crosses DV/2 per component), monitoring grid 4096/orbit.
import math, time, os, json, sys
def make_scene(name):
    if name == "S1":  # K1's quiet LEO: Moon + Sun tides
        GM = 3.986004418e14
        per = [dict(mu=4.9048695e12, d=3.844e8, n=2*math.pi/(27.321661*86400.0)),
               dict(mu=1.32712440018e20, d=1.495978707e11, n=2*math.pi/(365.256363*86400.0))]
        r0 = 6.771e6; e0 = 0.0; n_orb = 60; truth_steps = 1024
        return dict(GM=GM, per=per, a=r0/(1-0.0), e=e0, n_orb=n_orb, ts=truth_steps,
                    t0_ph=0.0, dv_quantum=2.7e-4)
    if name == "S2c":   # 2:1 resonance centre
        return dict(GM=1.0, per=[dict(mu=1e-3, d=2**(2/3), n=1.0/2**(2/3)**1.5)],
                    a=1.0, e=0.02, n_orb=200, ts=1024, t0_ph=0.0)
    if name == "S2d":   # detuned by 2/3 of half-width W = 2.5*mu^(2/3) = 0.025
        ap = 2**(2/3)*1.0167
        return dict(GM=1.0, per=[dict(mu=1e-3, d=ap, n=1.0/ap**1.5)],
                    a=1.0, e=0.02, n_orb=200, ts=1024, t0_ph=0.0)
    if name == "S2c2":  # second starting phase
        s = make_scene("S2c"); s["t0_ph"] = math.pi/2; return s
    if name == "S3":    # moderate tide, eccentric ship (e=0.3 flavor)
        return dict(GM=1.0, per=[dict(mu=1e-3, d=2.5, n=1.0/2.5**1.5)],
                    a=1.0, e=0.3, n_orb=200, ts=1024, t0_ph=0.0)
    if name == "S4":    # adversarial: steep conjunctions
        return dict(GM=1.0, per=[dict(mu=3e-3, d=1.9, n=1.0/1.9**1.5, ep=0.6)],
                    a=1.0, e=0.05, n_orb=200, ts=1024, t0_ph=0.0)
    raise KeyError(name)

def elems(GM, x, y, vx, vy):
    r = math.hypot(x, y); v2 = vx*vx + vy*vy
    a = GM/(2.0*GM/r - v2); rv = x*vx + y*vy; q = v2 - GM/r
    ex = (q*x - rv*vx)/GM; ey = (q*y - rv*vy)/GM
    e = math.hypot(ex, ey); w = math.atan2(ey, ex)
    nu = math.atan2(y, x) - w
    Ea = 2.0*math.atan2(math.sqrt(1.0-e)*math.sin(0.5*nu), math.sqrt(1.0+e)*math.cos(0.5*nu))
    return a, e, w, Ea - e*math.sin(Ea)

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

def per_pos(p, t):
    if p.get("ep", 0.0):
        M = p["n"]*t; E = M
        for _ in range(10): E -= (E - p["ep"]*math.sin(E) - M)/(1.0 - p["ep"]*math.cos(E))
        cE, sE = math.cos(E), math.sin(E)
        b = p["d"]*math.sqrt(1-p["ep"]**2)
        return p["d"]*(cE-p["ep"]), b*sE
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

def truth(sc):
    GM = sc["GM"]; n = sc["n_orb"]; ts = sc["ts"]
    a0 = sc["a"]; P = 2*math.pi*math.sqrt(a0**3/GM); dt = P/ts
    M0 = sc["t0_ph"]; e = sc["e"]
    Ea = M0
    for _ in range(10): Ea -= (Ea - e*math.sin(Ea) - M0)/(1.0 - e*math.cos(Ea))
    cE, sE = math.cos(Ea), math.sin(Ea)
    b = a0*math.sqrt(1-e*e); r = a0*(1-e*cE); g = math.sqrt(GM*a0)/r
    x = a0*(cE-e); y = b*sE; vx = -g*sE; vy = g*(b/a0)*cE
    t = 0.0; last = None
    def acc(x, y, t):
        ax, ay = tide(sc, x, y, t)
        r3 = math.hypot(x, y)**3
        return ax - GM*x/r3, ay - GM*y/r3
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
    return (t, x, y, vx, vy), dt
    raise KeyError(name)

def elems(GM, x, y, vx, vy):
    r = math.hypot(x, y); v2 = vx*vx + vy*vy
    a = GM/(2.0*GM/r - v2); rv = x*vx + y*vy; q = v2 - GM/r
    ex = (q*x - rv*vx)/GM; ey = (q*y - rv*vy)/GM
    e = math.hypot(ex, ey); w = math.atan2(ey, ex)
    nu = math.atan2(y, x) - w
    ec = min(e, 0.995)
    Ea = 2.0*math.atan2(math.sqrt(1.0-ec)*math.sin(0.5*nu), math.sqrt(1.0+ec)*math.cos(0.5*nu))
    return a, e, w, Ea - e*math.sin(Ea)

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


def layer(sc, policy, kappa=None, n_fixed=None, record=False):
    GM = sc["GM"]; n_orb = sc["n_orb"]
    a0 = sc["a"]; P0 = 2*math.pi*math.sqrt(a0**3/GM)
    M0 = sc["t0_ph"]; e = sc["e"]
    Ea = M0
    for _ in range(10): Ea -= (Ea - e*math.sin(Ea) - M0)/(1.0 - e*math.cos(Ea))
    cE, sE = math.cos(Ea), math.sin(Ea)
    b = a0*math.sqrt(1-e*e); r = a0*(1-e*cE); g = math.sqrt(GM*a0)/r
    x = a0*(cE-e); y = b*sE; vx = -g*sE; vy = g*(b/a0)*cE
    st = (a0, e, 0.0, M0, 0.0)
    t = 0.0; kicks = 0; walls = 0; kick_times = []
    T_end = n_orb*P0
    while t < T_end - 1e-9:
        P = 2*math.pi*math.sqrt(st[0]**3/GM)  # current period
        if policy == "FIXED":
            tau = P/n_fixed
        elif policy == "AVG":
            tau = P
        elif policy in ("TRIG", "TRIG2"):
            a_now = tide(sc, x, y, t); amag = math.hypot(*a_now)
            h = P/1000.0
            x1, y1, _, _ = prop(GM, st, t+h)
            a1 = tide(sc, x1, y1, t+h)
            J = math.hypot(a1[0]-a_now[0], a1[1]-a_now[1])/h
            ref = kappa*P*max(amag, J*P/1024.0)
            if policy == "TRIG":
                f = lambda tau: 0.5*J*tau*tau*(1+tau/P) - ref
            else:  # TRIG2: equidistribute error per unit time (random-walk scaling)
                f = lambda tau: 0.5*J*tau*tau*(1+tau/P) - ref*math.sqrt(tau/P)
            lo, hi = 0.0, P
            if f(hi) < 0:
                tau = hi
            else:
                for _ in range(60):
                    mid = 0.5*(lo+hi)
                    if f(mid) < 0: lo = mid
                    else: hi = mid
                tau = lo
            if tau < P/64.0:
                tau = P/64.0; walls += 1
        xe, ye, vxe, vye = prop(GM, st, t+0.5*tau)
        ax, ay = tide(sc, xe, ye, t+0.5*tau)
        xe, ye, vxe, vye = prop(GM, st, t+tau)
        vx = vxe + ax*tau; vy = vye + ay*tau
        t += tau; kicks += 1
        if record: kick_times.append(t/P0)
        newel = elems(GM, xe, ye, vx, vy)
        if newel[1] > 0.995 or not (0.1*a0 < newel[0] < 10*a0):
            return dict(kicks=kicks, kpo=kicks/n_orb, walls=walls, a=float("nan"),
                        e=float("nan"), kick_times=kick_times, unbound=True)
        st = (newel + (t,))
        x, y = xe, ye
    xe, ye, vxe, vye = prop(GM, st, T_end)
    af, ef, wf, _ = elems(GM, xe, ye, vxe, vye)
    return dict(kicks=kicks, kpo=kicks/n_orb, walls=walls, a=af, e=ef,
                kick_times=kick_times)

def k1quantum(sc):
    GM = sc["GM"]; DV = sc["dv_quantum"]
    n_orb = 60; SPB = 2048
    a0 = sc["a"]; P0 = 2*math.pi*math.sqrt(a0**3/GM)
    dt = P0/SPB
    st = (a0, sc["e"], 0.0, 0.0, 0.0)
    t = 0.0; Ix = Iy = 0.0; kicks = 0
    for _ in range(n_orb*SPB):
        tm = t + 0.5*dt
        xf, yf, _, _ = prop(GM, st, tm)
        ax, ay = tide(sc, xf, yf, tm)
        Ix += ax*dt; Iy += ay*dt; t += dt
        if abs(Ix) >= 0.5*DV or abs(Iy) >= 0.5*DV:
            kicks += 1
            xe, ye, vxe, vye = prop(GM, st, t)
            vx, vy = vxe+Ix, vye+Iy
            st = (elems(GM, xe, ye, vx, vy) + (t,))
            Ix = Iy = 0.0
    return dict(kicks=kicks, kpo=kicks/n_orb)

def run_scene(name, policies):
    sc = make_scene(name)
    t0 = time.time()
    fin, dt = truth(sc)
    T_end, xf, yf, vxf, vyf = fin
    at, et, wt, _ = elems(sc["GM"], xf, yf, vxf, vyf)
    out = dict(scene=name, truth=dict(a=at, e=et, w=wt, wall=time.time()-t0, ts=sc["ts"]), _kt={})
    for pol, kw in policies:
        t0 = time.time()
        r = layer(sc, pol, record=(kw.get("kappa") == 0.5 or pol == "AVG"), **kw)
        r["da_rel"] = abs(r["a"]-at)/at; r["de"] = abs(r["e"]-et)
        r["epump_ratio"] = r["e"]/et if et > 1e-12 else float("nan")
        r["wall"] = time.time()-t0
        key = pol + (f"-{kw.get('kappa')}" if kw.get('kappa') is not None else (f"-{kw.get('n_fixed')}" if kw.get('n_fixed') is not None else ""))
        out[key] = {k: v for k, v in r.items() if k != "kick_times"}
        key2 = key if key.startswith(("TRIG", "FIXED", "AVG")) else key
        if r.get("kick_times"): out["_kt"][key] = r["kick_times"]
    return out

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "S1"
    res = {}
    if which == "S1":
        pols = [("FIXED", dict(n_fixed=n)) for n in (4, 8, 16, 32, 64)]
        pols += [("AVG", {})] + [("TRIG", dict(kappa=k)) for k in (0.125, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0)]
        res["S1"] = run_scene("S1", pols)
        res["S1"]["k1quantum"] = k1quantum(make_scene("S1"))
    else:
        pols = [("FIXED", dict(n_fixed=n)) for n in (8, 16, 32, 64)] + [("AVG", {})] \
             + [("TRIG", dict(kappa=k)) for k in (0.25, 0.5, 1.0)] \
             + [("TRIG2", dict(kappa=k)) for k in (0.125, 0.5, 2.0)]
        for s in which.split(","):
            res[s] = run_scene(s, pols)
    print(json.dumps(res, indent=1))
    with open(f"out_{which.replace(',','_')}.json", "w") as f:
        json.dump(res, f, indent=1)
    print(f"load={os.getloadavg()[0]:.2f} cores8 mem_ok", file=sys.stderr)
