#!/usr/bin/env python3
# Premise probe K1 (GLM, 28 Sep 2026): kicks per orbit in low Earth orbit.
# Formula: Kepler conic about Earth. Unknown: Moon and Sun tides (exact point-mass tidal
# acceleration in the Earth frame). A kick fires when round(I/dv) changes in either
# component; at each kick the conic is re-anchored with error-feedback lattice rounding
# (5x5 sigma box on the carried cE, cL), as in reanchor.py.
import math, time, os

GM_E = 3.986004418e14; GM_M = 4.9048695e12; GM_S = 1.32712440018e20
DM = 3.844e8;      NM = 2.0*math.pi/(27.321661*86400.0)   # Moon, circular geocentric
DS = 1.495978707e11; NS = 2.0*math.pi/(365.256363*86400.0) # Sun, circular geocentric
R0 = 6.771e6; DV = 2.7e-4                                    # r, velocity quantum
N0 = math.sqrt(GM_E/R0**3); P = 2.0*math.pi/N0; VC = N0*R0

def elems(x, y, vx, vy):
    r = math.hypot(x, y); v2 = vx*vx + vy*vy
    a = GM_E/(2.0*GM_E/r - v2); rv = x*vx + y*vy; q = v2 - GM_E/r
    ex = (q*x - rv*vx)/GM_E; ey = (q*y - rv*vy)/GM_E
    e = math.hypot(ex, ey); w = math.atan2(ey, ex)
    nu = math.atan2(y, x) - w
    Ea = 2.0*math.atan2(math.sqrt(1.0-e)*math.sin(0.5*nu), math.sqrt(1.0+e)*math.cos(0.5*nu))
    return a, e, w, Ea - e*math.sin(Ea)

def prop(st, t):
    a, e, w, M0, t0 = st
    M = M0 + math.sqrt(GM_E/(a*a*a))*(t - t0)
    Ea = M
    for _ in range(8): Ea -= (Ea - e*math.sin(Ea) - M)/(1.0 - e*math.cos(Ea))
    cE = math.cos(Ea); sE = math.sin(Ea)
    b = a*math.sqrt(1.0-e*e); r = a*(1.0-e*cE); g = math.sqrt(GM_E*a)/r
    xp = a*(cE-e); yp = b*sE; vxp = -g*sE; vyp = g*(b/a)*cE
    cw = math.cos(w); sw = math.sin(w)
    return xp*cw-yp*sw, xp*sw+yp*cw, vxp*cw-vyp*sw, vxp*sw+vyp*cw

def tide(x, y, t):
    cm = math.cos(NM*t); sm = math.sin(NM*t)
    mx = DM*cm-x; my = DM*sm-y
    d2 = mx*mx+my*my; dd = d2*math.sqrt(d2)
    ax = GM_M*(mx/dd - cm/(DM*DM)); ay = GM_M*(my/dd - sm/(DM*DM))
    cs = math.cos(NS*t); ss = math.sin(NS*t)
    sx = DS*cs-x; sy = DS*ss-y
    d2 = sx*sx+sy*sy; dd = d2*math.sqrt(d2)
    ax += GM_S*(sx/dd - cs/(DS*DS)); ay += GM_S*(sy/dd - ss/(DS*DS))
    return ax, ay

def anchor(x, y, vx, vy, t, cE, cL):
    r = math.hypot(x, y)
    Et = 0.5*(vx*vx+vy*vy) - GM_E/r; Lt = x*vy - y*vx
    bx = math.floor(vx/DV+0.5); by = math.floor(vy/DV+0.5)
    vq = VC*DV; lq = R0*DV; best = None
    for i in range(-2, 3):
        for j in range(-2, 3):
            ux = (bx+i)*DV; uy = (by+j)*DV
            dE = 0.5*(ux*ux+uy*uy) - GM_E/r - Et; dL = x*uy - y*ux - Lt
            c = ((cE+dE)/vq)**2 + ((cL+dL)/lq)**2
            if best is None or c < best[0]: best = (c, ux, uy, dE, dL)
    _, ux, uy, dE, dL = best
    return elems(x, y, ux, uy)+(t,), cE+dE, cL+dL

def main():
    ORB = 150; SPB = 4096; dt = P/SPB
    st, cE, cL = anchor(R0, 0.0, 0.0, VC, 0.0, 0.0, 0.0)
    Ix = Iy = 0.0; kicks = 0; t = 0.0; mE = mL = 0.0; nanch = 1
    t0 = time.time()
    for _ in range(ORB*SPB):
        tm = t + 0.5*dt
        xf, yf, _, _ = prop(st, tm)
        ax, ay = tide(xf, yf, tm)
        Ix += ax*dt; Iy += ay*dt; t += dt
        if abs(Ix) >= 0.5*DV or abs(Iy) >= 0.5*DV:
            nx = math.floor(Ix/DV+0.5); ny = math.floor(Iy/DV+0.5)
            kicks += abs(nx) + abs(ny)
            xe, ye, vxe, vye = prop(st, t)
            st, cE, cL = anchor(xe, ye, vxe+Ix, vye+Iy, t, cE, cL)
            nanch += 1; mE = max(mE, abs(cE)); mL = max(mL, abs(cL))
            Ix = Iy = 0.0
    wall = time.time() - t0
    print(f"K1: orbits={ORB} steps/orbit={SPB} kicks={kicks} anchors={nanch}")
    print(f"K1: kicks/orbit = {kicks/ORB:.2f}   (kill if > 1e3)")
    print(f"K1: kick rate = {kicks/ORB/P:.3e} /s/body")
    print(f"K1: max|cE|={mE:.3g} J/kg ({mE/(VC*DV):.1f} quanta)  max|cL|={mL:.3g} m2/s ({mL/(R0*DV):.1f} quanta)")
    print(f"K1: wall={wall:.1f}s  load={os.getloadavg()[0]:.2f}")

main()
