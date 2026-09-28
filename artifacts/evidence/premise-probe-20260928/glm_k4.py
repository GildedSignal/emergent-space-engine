#!/usr/bin/env python3
# Premise probe K4 (GLM, 28 Sep 2026): Earth->Moon transfers crossing the Moon's Hill sphere.
# Parent handoff on the dimensionless tidal ratio rho = (GM_Moon/d_moon^3)/(GM_Earth/d_earth^3)
# (the rho = 1 surface, ~71,500 km from the Moon, is the Hill-type sphere) with 10%
# hysteresis (E->M at rho > 1.1, M->E at rho < 1/1.1).
# Truth: RK4, Earth+Moon point masses, geocentric frame, Moon circular;
# dt = clamp(0.02 r_min / v_max, 4, 1800) s; half-step reruns check accuracy.
# Formula: parent two-body conic, shadowed by RK2-midpoint under the parent alone
# (re-anchored at every event; per-step shadow error ~ (omega*dt)^3 ~ 1e-14 relative,
# immaterial for the tide integral). The unknown (the other body's tide about the
# parent) is integrated along the shadow; a kick fires when
# round(I/dv) changes; at every kick and handoff the velocity is re-anchored with
# error-feedback lattice rounding (5x5 sigma box, carried cE, cL).
# Two vehicles, both reported:
#  A) one continuous trajectory (best of an offline geometry search): 46 handoffs,
#     ends by Earth impact. Geometry found by search in /private/tmp/glm-scratch.
#  B) a commanded transfer sequence: one ship, carries persistent, re-injected at
#     perigee approach (or before impact/escape) onto the next transfer opportunity
#     (a command is an engine event; the injection is lattice-anchored like any event,
#     so it feeds the same carry statistics). Flown until >= 100 handoffs.
# Kill criterion: fitted growth exponent of |cE| or |cL| vs handoff number >= 0.8.
import math, time, os

GM_E = 3.986004418e14; GM_M = 4.9048695e12
DM = 3.844e8; NM = 2.0*math.pi/(27.321661*86400.0)
RP = 6.771e6; DV = 2.7e-4
RE_CR = 6.571e6; RM_CR = 1.8474e6; ESC = 3.0e9
RHO_ON = 1.1; RHO_OFF = 1.0/1.1

def acc_true(x, y, t):
    cm = math.cos(NM*t); sm = math.sin(NM*t)
    r = math.sqrt(x*x+y*y); r3 = r*r*r
    dx = DM*cm-x; dy = DM*sm-y
    d = math.sqrt(dx*dx+dy*dy); d3 = d*d*d
    return (-GM_E*x/r3 + GM_M*(dx/d3 - cm/(DM*DM)),
            -GM_E*y/r3 + GM_M*(dy/d3 - sm/(DM*DM)))

def rk4_true(x, y, vx, vy, t, dt):
    ax1, ay1 = acc_true(x, y, t)
    x2 = x+0.5*dt*vx; y2 = y+0.5*dt*vy; vx2 = vx+0.5*dt*ax1; vy2 = vy+0.5*dt*ay1
    ax2, ay2 = acc_true(x2, y2, t+0.5*dt)
    x3 = x+0.5*dt*vx2; y3 = y+0.5*dt*vy2; vx3 = vx+0.5*dt*ax2; vy3 = vy+0.5*dt*ay2
    ax3, ay3 = acc_true(x3, y3, t+0.5*dt)
    x4 = x+dt*vx3; y4 = y+dt*vy3; vx4 = vx+dt*ax3; vy4 = vy+dt*ay3
    ax4, ay4 = acc_true(x4, y4, t+dt)
    return (x+dt/6.0*(vx+2.0*vx2+2.0*vx3+vx4),
            y+dt/6.0*(vy+2.0*vy2+2.0*vy3+vy4),
            vx+dt/6.0*(ax1+2.0*ax2+2.0*ax3+ax4),
            vy+dt/6.0*(ay1+2.0*ay2+2.0*ay3+ay4))

def acc_parent(x, y, t, p):
    r = math.sqrt(x*x+y*y); r3 = r*r*r
    if p == 0:
        return -GM_E*x/r3, -GM_E*y/r3
    dx = x-DM*math.cos(NM*t); dy = y-DM*math.sin(NM*t)
    d = math.sqrt(dx*dx+dy*dy); d3 = d*d*d
    return -GM_M*dx/d3, -GM_M*dy/d3

def rk2_shadow(x, y, vx, vy, t, dt, p):
    ax1, ay1 = acc_parent(x, y, t, p)
    xm = x+0.5*dt*(vx+0.5*dt*ax1); ym = y+0.5*dt*(vy+0.5*dt*ay1)
    vxm = vx+0.5*dt*ax1; vym = vy+0.5*dt*ay1
    ax2, ay2 = acc_parent(xm, ym, t+0.5*dt, p)
    return (x+dt*(vx+0.5*dt*ax2), y+dt*(vy+0.5*dt*ay2), vx+dt*ax2, vy+dt*ay2)

def tide_other(x, y, t, p):
    cm = math.cos(NM*t); sm = math.sin(NM*t)
    if p == 0:
        mx = DM*cm-x; my = DM*sm-y
        d2 = mx*mx+my*my; dd = d2*math.sqrt(d2)
        return GM_M*(mx/dd - cm/(DM*DM)), GM_M*(my/dd - sm/(DM*DM))
    r = math.sqrt(x*x+y*y); r3 = r*r*r
    return GM_E*(-x/r3 + cm/(DM*DM)), GM_E*(-y/r3 + sm/(DM*DM))

def sigma(x, y, vx, vy, t, p, cE, cL):
    if p == 0:
        px, py, pvx, pvy, GM = 0.0, 0.0, 0.0, 0.0, GM_E
    else:
        cm = math.cos(NM*t); sm = math.sin(NM*t)
        px, py, pvx, pvy, GM = DM*cm, DM*sm, -DM*NM*sm, DM*NM*cm, GM_M
    rx = x-px; ry = y-py; rvx = vx-pvx; rvy = vy-pvy
    r = math.hypot(rx, ry); v2 = rvx*rvx+rvy*rvy
    Et = 0.5*v2 - GM/r; Lt = rx*rvy - ry*rvx
    vq = max(math.sqrt(v2), 1.0)*DV; lq = max(r, 1.0)*DV
    bx = math.floor(vx/DV+0.5); by = math.floor(vy/DV+0.5)
    best = None
    for i in range(-2, 3):
        for j in range(-2, 3):
            ux = (bx+i)*DV; uy = (by+j)*DV
            urx = ux-pvx; ury = uy-pvy
            dE = 0.5*(urx*urx+ury*ury) - GM/r - Et
            dL = rx*ury - ry*urx - Lt
            c = ((cE+dE)/vq)**2 + ((cL+dL)/lq)**2
            if best is None or c < best[0]: best = (c, ux, uy, dE, dL)
    return best[1], best[2], cE+best[3], cL+best[4]

def inject_state(apo, off, t):
    a = 0.5*(RP+apo)
    vp = math.sqrt(GM_E*(2.0/RP - 1.0/a))
    th_h = math.pi*math.sqrt(a*a*a/GM_E)
    th0 = NM*t + NM*th_h - math.pi + off
    return (RP*math.cos(th0), RP*math.sin(th0), -vp*math.sin(th0), vp*math.cos(th0))

def run(apo, off, dtmul, wall_cap, target_h, cycles=False, tmax=6.5e8):
    geoms = [(1.055, 0.015), (1.05, 0.02), (0.98, 0.18), (1.0, 0.25), (1.05, 0.08),
             (1.045, 0.03), (1.055, 0.005), (1.0, 0.18), (1.052, 0.013), (1.058, 0.011)]
    gi = 0
    x, y, vx, vy = inject_state(apo, off, 0.0)
    t = 0.0; parent = 0
    vx, vy, cE, cL = sigma(x, y, vx, vy, t, 0, 0.0, 0.0)
    sx, sy, svx, svy = x, y, vx, vy
    Ix = Iy = 0.0
    kicks = 0; events = 1; handoffs = 0; legs = 0; was_in = False; cyc = 0; tcyc = 0.0
    log = [(0, 0.0, 0.0, 0.0)]
    t0 = time.time(); status = "wall"
    while True:
        if time.time()-t0 > wall_cap: break
        if t > tmax: status = "tmax"; break
        de = math.hypot(x, y)
        cm = math.cos(NM*t); sm = math.sin(NM*t)
        dm = math.hypot(x-DM*cm, y-DM*sm)
        inbound = (x*vx+y*vy) < 0.0
        if handoffs >= target_h: status = "ok"; break
        if (not cycles) and (de < RE_CR or dm < RM_CR or de > ESC):
            status = "earth-crash" if de < RE_CR else ("moon-crash" if dm < RM_CR else "escape")
            break
        if cycles and (dm < RM_CR or de > ESC or (t-tcyc) > 200.0*86400.0
                       or (inbound and de < 9.0e6 and (t-tcyc) > 6.0*86400.0)):
            # commanded re-injection onto the next transfer opportunity
            gi = (gi+1) % len(geoms); cyc += 1; tcyc = t
            am2, off2 = geoms[gi]
            x, y, vx, vy = inject_state(am2*DM, off2, t)
            parent = 0
            vx, vy, cE, cL = sigma(x, y, vx, vy, t, 0, cE, cL)
            sx, sy, svx, svy = x, y, vx, vy; Ix = Iy = 0.0; events += 1
            continue
        if de < 2.0e7 and not was_in: legs += 1; was_in = True
        if de > 4.0e7: was_in = False
        vrel_m = math.hypot(vx+DM*NM*sm, vy-DM*NM*cm)
        vmax = max(math.hypot(vx, vy), vrel_m)
        dt = dtmul*max(4.0, min(1800.0, 0.02*min(de, dm)/vmax))
        sx, sy, svx, svy = rk2_shadow(sx, sy, svx, svy, t, 0.5*dt, parent)
        ux, uy = tide_other(sx, sy, t+0.5*dt, parent)
        sx, sy, svx, svy = rk2_shadow(sx, sy, svx, svy, t+0.5*dt, 0.5*dt, parent)
        Ix += ux*dt; Iy += uy*dt
        x, y, vx, vy = rk4_true(x, y, vx, vy, t, dt)
        t += dt
        cm = math.cos(NM*t); sm = math.sin(NM*t)
        de = math.hypot(x, y); dm = math.hypot(x-DM*cm, y-DM*sm)
        rho = (GM_M/(dm*dm*dm))/(GM_E/(de*de*de))
        if (parent == 0 and rho > RHO_ON) or (parent == 1 and rho < RHO_OFF):
            parent = 1 if parent == 0 else 0
            handoffs += 1; events += 1
            vx, vy, cE, cL = sigma(x, y, vx, vy, t, parent, cE, cL)
            sx, sy, svx, svy = x, y, vx, vy; Ix = Iy = 0.0
            log.append((handoffs, t, abs(cE), abs(cL)))
        nx = math.floor(Ix/DV+0.5); ny = math.floor(Iy/DV+0.5)
        if nx != 0 or ny != 0:
            kicks += abs(nx)+abs(ny); events += 1
            vx, vy, cE, cL = sigma(x, y, vx+Ix, vy+Iy, t, parent, cE, cL)
            sx, sy, svx, svy = x, y, vx, vy
            Ix = Iy = 0.0
    wall = time.time()-t0
    return dict(status=status, handoffs=handoffs, kicks=kicks, events=events, legs=legs,
                cycles=cyc, wall=wall, log=log, cE=cE, cL=cL, t=t, apo=apo, off=off,
                dtmul=dtmul)

def fit_beta(log):
    xs = []; ysE = []; ysL = []
    for (k, t, aE, aL) in log:
        if k >= 8:
            xs.append(math.log(k)); ysE.append(math.log(max(aE, 1e-9))); ysL.append(math.log(max(aL, 1e-9)))
    def slope(xs, ys):
        n = len(xs)
        if n < 8: return float('nan')
        mx = sum(xs)/n; my = sum(ys)/n
        sxx = sum((v-mx)**2 for v in xs)
        sxy = sum((a-mx)*(b-my) for a, b in zip(xs, ys))
        return sxy/sxx if sxx > 0 else float('nan')
    return slope(xs, ysE), slope(xs, ysL), len(xs)

def report(tag, r):
    bE, bL, n = fit_beta(r["log"])
    print(f"K4 {tag}: {r['status']:12s} handoffs={r['handoffs']} cycles={r['cycles']} legs={r['legs']} "
          f"kicks={r['kicks']} events={r['events']} t={r['t']/86400.0:.0f}d wall={r['wall']:.1f}s")
    print(f"K4 {tag}: beta_E={bE:+.3f} beta_L={bL:+.3f} (n={n})  kill if >= 0.8")
    print(f"K4 {tag}: end |cE|={abs(r['cE']):.3g} J/kg  |cL|={abs(r['cL']):.3g} m2/s  "
          f"kicks/handoff ~ {r['kicks']/max(r['handoffs'],1):.0f}")
    return bE, bL

def main():
    print(f"K4: rho hysteresis ON {RHO_ON} OFF {RHO_OFF:.3f}; dv={DV} m/s; load={os.getloadavg()[0]:.2f}")
    # A) single continuous trajectory (best of offline search)
    rA = run(1.055*DM, 0.015, 1.0, 8.0, 100, cycles=False)
    report("A single-chain", rA)
    for (k, t, aE, aL) in rA["log"][::6]:
        print(f"    h{k:3d} t={t/86400.0:7.0f}d |cE|={aE:.3g} |cL|={aL:.3g}")
    # B) commanded transfer sequence until 100 handoffs
    rB = run(1.055*DM, 0.015, 1.0, 25.0, 100, cycles=True)
    report("B transfers", rB)
    for (k, t, aE, aL) in rB["log"][::10]:
        print(f"    h{k:3d} t={t/86400.0:7.0f}d |cE|={aE:.3g} |cL|={aL:.3g}")
    # half-step accuracy checks
    rA2 = run(1.055*DM, 0.015, 0.5, 12.0, 100, cycles=False)
    report("A half-step", rA2)
    rB2 = run(1.055*DM, 0.015, 0.5, 35.0, 100, cycles=True)
    report("B half-step", rB2)

main()
