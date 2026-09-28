#!/usr/bin/env python3
# Premise probe K3 (GLM, 28 Sep 2026): oblate parent, J2 = 1.08263e-3, Earth equatorial
# radius 6378.137 km, equatorial coplanar orbit. Two runs:
#  A) 'jk': J2 in the unknown (formula = pure Kepler conic), with the tides. Rate counted
#     as sum of |level changes| (no re-anchoring; kicks of dv change e by ~3.5e-8, so the
#     rate impact of re-anchoring is negligible).
#  B) 'jf': J2 inside the formula as the equatorial 1/r^3 term. The exact circular solution
#     of a_r = -GM/r^2 + (3/2) J2 GM R^2 / r^4 is used (radius fixed, Omega = h/r^2 from the
#     lattice anchor); unknown = tides only. Full error-feedback kick machinery.
import math, time, os

GM_E = 3.986004418e14; GM_M = 4.9048695e12; GM_S = 1.32712440018e20
DM = 3.844e8;      NM = 2.0*math.pi/(27.321661*86400.0)
DS = 1.495978707e11; NS = 2.0*math.pi/(365.256363*86400.0)
R0 = 6.771e6; DV = 2.7e-4
J2 = 1.08263e-3; RE = 6.378137e6; CJ = 1.5*J2*GM_E*RE*RE
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

def aj2(x, y):
    r2 = x*x + y*y
    c = CJ/(r2*r2*math.sqrt(r2))
    return -c*x, -c*y

def run_jk():
    ORB = 40; SPB = 4096; dt = P/SPB
    st = elems(R0, 0.0, 0.0, VC)+(0.0,)
    Ix = Iy = 0.0; lx = ly = 0; kicks = 0; t = 0.0
    t0 = time.time()
    for _ in range(ORB*SPB):
        tm = t + 0.5*dt
        xf, yf, _, _ = prop(st, tm)
        ax, ay = tide(xf, yf, tm)
        gx, gy = aj2(xf, yf)
        Ix += (ax+gx)*dt; Iy += (ay+gy)*dt; t += dt
        nx = math.floor(Ix/DV+0.5); ny = math.floor(Iy/DV+0.5)
        kicks += abs(nx-lx) + abs(ny-ly); lx, ly = nx, ny
    wall = time.time() - t0
    print(f"K3a (J2 as kicks): kicks/orbit = {kicks/ORB:.3e}  ({kicks} over {ORB} orbits)  wall={wall:.1f}s")

def run_jf():
    ORB = 150; SPB = 2048; dt = P/SPB
    # formula state: (r, th0, t0, om); anchored sigma-lattice at t=0
    # circular speed with J2: v^2 = GM/r (1 - 1.5 J2 (R/r)^2)
    vcj = math.sqrt(GM_E/R0*(1.0 - 1.5*J2*(RE/R0)**2))
    def sigbox(x, y, vx, vy, cE, cL):
        r = math.hypot(x, y)
        Et = 0.5*(vx*vx+vy*vy) - GM_E/r + 0.5*CJ/(r*r*r)
        Lt = x*vy - y*vx
        bx = math.floor(vx/DV+0.5); by = math.floor(vy/DV+0.5)
        vq = VC*DV; lq = R0*DV; best = None
        for i in range(-2, 3):
            for j in range(-2, 3):
                ux = (bx+i)*DV; uy = (by+j)*DV
                dE = 0.5*(ux*ux+uy*uy) - GM_E/r + 0.5*CJ/(r*r*r) - Et
                dL = x*uy - y*ux - Lt
                c = ((cE+dE)/vq)**2 + ((cL+dL)/lq)**2
                if best is None or c < best[0]: best = (c, ux, uy, dE, dL)
        _, ux, uy, dE, dL = best
        return ux, uy, cE+dE, cL+dL
    t0w = time.time()
    x, y = R0, 0.0
    vx, vy = 0.0, vcj
    vx, vy, cE, cL = sigbox(x, y, vx, vy, 0.0, 0.0)
    r = R0; th = 0.0; ta = 0.0; om = (x*vy - y*vx)/(r*r)
    Ix = Iy = 0.0; kicks = 0; t = 0.0; mE = mL = 0.0; nanch = 1
    for _ in range(ORB*SPB):
        tm = t + 0.5*dt
        thm = th + om*(tm - ta)
        xf = r*math.cos(thm); yf = r*math.sin(thm)
        ax, ay = tide(xf, yf, tm)
        Ix += ax*dt; Iy += ay*dt; t += dt
        if abs(Ix) >= 0.5*DV or abs(Iy) >= 0.5*DV:
            nx = math.floor(Ix/DV+0.5); ny = math.floor(Iy/DV+0.5)
            kicks += abs(nx) + abs(ny)
            tht = th + om*(t - ta)
            xe = r*math.cos(tht); ye = r*math.sin(tht)
            vth = om*r
            vfx = -vth*math.sin(tht); vfy = vth*math.cos(tht)
            vx, vy, cE, cL = sigbox(xe, ye, vfx+Ix, vfy+Iy, cE, cL)
            r = math.hypot(xe, ye); th = tht; ta = t
            om = (xe*vy - ye*vx)/(r*r)
            nanch += 1; mE = max(mE, abs(cE)); mL = max(mL, abs(cL))
            Ix = Iy = 0.0
    wall = time.time() - t0w
    print(f"K3b (J2 in formula): kicks/orbit = {kicks/ORB:.2f}  ({kicks} over {ORB} orbits)  anchors={nanch}")
    print(f"K3b: max|cE|={mE:.3g} J/kg ({mE/(VC*DV):.1f} quanta)  max|cL|={mL:.3g} m2/s ({mL/(R0*DV):.1f} quanta)")
    print(f"K3b: wall={wall:.1f}s  load={os.getloadavg()[0]:.2f}")

print(f"K3: |a_J2| at r0 = {CJ/R0**4:.3e} m/s^2 vs |tide| ~ 1.2e-6 m/s^2")
run_jk()
run_jf()
