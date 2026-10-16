#!/usr/bin/env python3
# Premise probe K2 (GLM, 28 Sep 2026): first-order averaging of the Moon+Sun quadrupole,
# with short-period terms, inside the formula. Coplanar circular perturbers.
#
# Formulas (r << d, u = ship's absolute angle, phi_p = perturber phase, k_p = GM_p/d_p^3):
#   quadrupole tide along a circle of radius a_r, exact identity (self-checked):
#     a_x = k a_r [ (1/2) cos u + (3/2) cos(u - 2 phi) ]
#     a_y = k a_r [ (1/2) sin u - (3/2) sin(u - 2 phi) ]
#   bounded short-period displacement (zeroed at the anchor t0, u0):
#     dx = -(k a_r/(2 n^2))(cos u - cos u0) - (3/2)(k a_r/w2^2)(cos psi - cos psi0)
#     dy = -(k a_r/(2 n^2))(sin u - sin u0) + (3/2)(k a_r/w2^2)(sin psi - sin psi0)
#     psi = u - 2 phi, w2 = n - 2 n_p, n = sqrt(GM_E/a_r^3)
#   secular rate (stated; no effect on a circular equatorial trajectory):
#     dvarpi/dt = (3/2) k_p/n  (Moon 1.14e-10 rad/s, Sun 5.2e-11 rad/s)
# Unknown for kicks = exact tide - quadrupole (= octupole and higher, order r/d).
import math, time, os

GM_E = 3.986004418e14; GM_M = 4.9048695e12; GM_S = 1.32712440018e20
DM = 3.844e8;      NM = 2.0*math.pi/(27.321661*86400.0)
DS = 1.495978707e11; NS = 2.0*math.pi/(365.256363*86400.0)
R0 = 6.771e6; DV = 2.7e-4
N0 = math.sqrt(GM_E/R0**3); P = 2.0*math.pi/N0; VC = N0*R0
KM = GM_M/(DM**3); KS = GM_S/(DS**3)

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

def sp(anc, t):
    # short-period displacement and velocity; anc = (u0, n, ar, t0)
    u0, na, ar, t0 = anc
    tau = t - t0; u = u0 + na*tau
    cu = math.cos(u); su = math.sin(u); cu0 = math.cos(u0); su0 = math.sin(u0)
    dx = dy = dvx = dvy = 0.0
    for (k, np_) in ((KM, NM), (KS, NS)):
        w2 = na - 2.0*np_
        A = k*ar; psi = u - 2.0*np_*t; psi0 = u0 - 2.0*np_*t0
        cp, sp_ = math.cos(psi), math.sin(psi); cp0, sp0 = math.cos(psi0), math.sin(psi0)
        c1 = 0.5*A/(na*na); c2 = 1.5*A/(w2*w2); c3 = 0.5*A/na; c4 = 1.5*A/w2
        dx += -c1*(cu-cu0) - c2*(cp-cp0)
        dy += -c1*(su-su0) + c2*(sp_-sp0)
        dvx += c3*(su-su0) + c4*(sp_-sp0)
        dvy += -c3*(cu-cu0) + c4*(cp-cp0)
    return dx, dy, dvx, dvy

def tide_exact(x, y, t):
    cm = math.cos(NM*t); sm = math.sin(NM*t)
    mx = DM*cm-x; my = DM*sm-y
    d2 = mx*mx+my*my; dd = d2*math.sqrt(d2)
    ax = GM_M*(mx/dd - cm/(DM*DM)); ay = GM_M*(my/dd - sm/(DM*DM))
    cs = math.cos(NS*t); ss = math.sin(NS*t)
    sx = DS*cs-x; sy = DS*ss-y
    d2 = sx*sx+sy*sy; dd = d2*math.sqrt(d2)
    ax += GM_S*(sx/dd - cs/(DS*DS)); ay += GM_S*(sy/dd - ss/(DS*DS))
    return ax, ay

def tide_quad(x, y, t):
    cm = math.cos(NM*t); sm = math.sin(NM*t)
    s = x*cm + y*sm
    ax = KM*(3.0*s*cm - x); ay = KM*(3.0*s*sm - y)
    cs = math.cos(NS*t); ss = math.sin(NS*t)
    s = x*cs + y*ss
    ax += KS*(3.0*s*cs - x); ay += KS*(3.0*s*ss - y)
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
    st = elems(x, y, ux, uy)+(t,)
    a = st[0]
    anc = (math.atan2(y, x), math.sqrt(GM_E/(a*a*a)), r, t)
    return st, anc, cE+dE, cL+dL

def main():
    # self-check: harmonic decomposition identity vs direct quadrupole
    worst = 0.0
    for i in range(200):
        th = 2.0*math.pi*i/200.0; t = i*30.0
        x = R0*math.cos(th); y = R0*math.sin(th)
        axd, ayd = tide_quad(x, y, t)
        u = th
        ax = KM*R0*(0.5*math.cos(u) + 1.5*math.cos(u-2*NM*t)) \
           + KS*R0*(0.5*math.cos(u) + 1.5*math.cos(u-2*NS*t))
        ay = KM*R0*(0.5*math.sin(u) - 1.5*math.sin(u-2*NM*t)) \
           + KS*R0*(0.5*math.sin(u) - 1.5*math.sin(u-2*NS*t))
        worst = max(worst, abs(axd-ax)+abs(ayd-ay))
    print(f"K2 selfcheck: |decomposition - direct quadrupole| max = {worst:.2e} m/s2")
    # octupole scale check: exact tide vs quadrupole along the circle
    wo = 0.0; wq = 0.0
    for i in range(500):
        th = 2.0*math.pi*i/500.0; t = i*11.0
        x = R0*math.cos(th); y = R0*math.sin(th)
        ax, ay = tide_exact(x, y, t); qx, qy = tide_quad(x, y, t)
        wo = max(wo, math.hypot(ax-qx, ay-qy)); wq = max(wq, math.hypot(qx, qy))
    print(f"K2 residual scale: max|exact-quad|/max|quad| = {wo/wq:.3f}  (r/d = {R0/DM:.4f})")

    ORB = 1500; SPB = 512; dt = P/SPB
    st, anc, cE, cL = anchor(R0, 0.0, 0.0, VC, 0.0, 0.0, 0.0)
    Ix = Iy = 0.0; kicks = 0; t = 0.0; mE = mL = 0.0; nanch = 1
    t0 = time.time()
    for _ in range(ORB*SPB):
        tm = t + 0.5*dt
        xc, yc, _, _ = prop(st, tm)
        dx, dy, _, _ = sp(anc, tm)
        xf = xc+dx; yf = yc+dy
        ax1, ay1 = tide_exact(xf, yf, tm)
        ax2, ay2 = tide_quad(xf, yf, tm)
        Ix += (ax1-ax2)*dt; Iy += (ay1-ay2)*dt; t += dt
        if abs(Ix) >= 0.5*DV or abs(Iy) >= 0.5*DV:
            nx = math.floor(Ix/DV+0.5); ny = math.floor(Iy/DV+0.5)
            kicks += abs(nx) + abs(ny)
            xe, ye, vxe, vye = prop(st, t)
            dx, dy, dvx, dvy = sp(anc, t)
            st, anc, cE, cL = anchor(xe+dx, ye+dy, vxe+dvx+Ix, vye+dvy+Iy, t, cE, cL)
            nanch += 1; mE = max(mE, abs(cE)); mL = max(mL, abs(cL))
            Ix = Iy = 0.0
    wall = time.time() - t0
    print(f"K2: orbits={ORB} steps/orbit={SPB} kicks={kicks} anchors={nanch}")
    print(f"K2: kicks/orbit = {kicks/ORB:.4f}   (kill if K1 reduction < 10x)")
    print(f"K2: max|cE|={mE:.3g} J/kg ({mE/(VC*DV):.1f} quanta)  max|cL|={mL:.3g} m2/s ({mL/(R0*DV):.1f} quanta)")
    print(f"K2: wall={wall:.1f}s  load={os.getloadavg()[0]:.2f}")

main()
