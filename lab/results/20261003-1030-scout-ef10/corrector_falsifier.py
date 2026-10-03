#!/usr/bin/env python3
"""Scout falsifier: do symplectic correctors (Wisdom-Holman-Tou 1996 / Laskar-Robutel 2001,
as implemented in WHFast, Rein & Tamayo 2015, arXiv:1506.01084) buy fewer kicks per orbit
at the same behaviour, on the engine's own split?

Engine structure under test (docs/law.md, 'Perturbed motion'):
  exact Kepler drift about the dominant mass (the tube: zero work)
  + kicks carrying everything else (parent tide / secondary), fixed step in the drift's phase.
Toy: massless particle, primary M=1, secondary m2 on a prescribed circular orbit a_out
(the 'analytic generator' body). DKD Wisdom-Holman map, n kicks per orbit.

Corrector: applied ONLY at init (real->mapping) and at output (mapping->real),
Z(a,b) = Kepler(a) Kick(-b) Kepler(-2a) Kick(b) Kepler(a), coefficients from
rebound src/integrator_whfast.c (Wisdom's compact form).

Metrics (behaviour, not trajectory identity):
  prec : apsidal precession rate (rad / inner orbit), least-squares slope of unwrapped
         argument of periapsis over the run; error relative to the oracle run.
  dCJ  : max relative error of the Jacobi constant (CRTBP invariant) over the run
         (the engine's B12-style boundedness judge).

Usage: python3 corrector_falsifier.py smoke|sweep|heldout
Writes results to results-<mode>.json and prints a table.
"""
import json, math, sys

# ---- system (tuned so the plain map's bias is measurable; NOT a decisive-case choice) ----
M2   = 0.3    # secondary mass (primary = 1)
AOUT = 4.5    # secondary semi-major axis (P_out/P_in = 8.37, off the resonances)
NOUT = math.sqrt((1.0 + M2) / AOUT**3)

# ---- corrector coefficients (rebound integrator_whfast.c, exact) ----
A1 = 0.41833001326703777398908601289259374469640768464934
A2 = 0.83666002653407554797817202578518748939281536929867
B31 = -0.024900596027799867499350357910273437184309981229127
B51 = -0.0083001986759332891664501193034244790614366604097090
B52 =  0.041500993379666445832250596517122395307183302048545
A3 = 1.2549900398011133219672580386777812340892230539480
A4 = 1.6733200530681510959563440515703749787856307385973
A5 = 2.0916500663351888699454300644629687234820384232467
B71 =  0.0024926811426922105779030593952776964450539008582219
B72 = -0.018270923246702131478062356884535264841652263842597
B73 =  0.053964399093127498721765893493510877532452806339655
B111 =  0.00020361579647854651301632818774633716473696537436847
B112 = -0.0023487215292295354188307328851055489876255097419754
B113 =  0.012309078592019946317544564763237909911330686448336
B114 = -0.038121613681288650508647613260247372125243616270670
B115 =  0.072593394748842738674253180742744961827622366521517

TWO_PI = 2.0 * math.pi

def stumpff(z):
    if z < 1e-4:
        c1 = 1.0 - z/6.0*(1.0 - z/20.0*(1.0 - z/42.0))
        c2 = 0.5 - z/24.0*(1.0 - z/30.0*(1.0 - z/56.0))
        c3 = 1.0/6.0 - z/120.0*(1.0 - z/42.0*(1.0 - z/72.0))
    else:
        x = math.sqrt(z)
        c0 = math.cos(x); c1 = math.sin(x) / x
        c2 = (1.0 - c0) / z; c3 = (1.0 - c1) / z
    return c1, c2, c3

def drift(s, dt):
    """Exact two-body drift (universal variables, M=1). s=[x,y,vx,vy]."""
    if dt == 0.0:
        return
    x, y, vx, vy = s
    r0 = math.hypot(x, y); v2 = vx*vx + vy*vy
    beta = 2.0/r0 - v2          # >0 ellipse
    eta = x*vx + y*vy
    c1b = 1.0 - beta*r0         # = r0*v2 - 1 (chi^3 coefficient, Vallado)
    def F(ch):
        z = beta*ch*ch
        c1, c2, c3 = stumpff(z)
        G1 = ch*c1; G2 = ch*ch*c2; G3 = ch*ch*ch*c3
        return r0*ch + eta*G2 + c1b*G3 - dt, G1, G2, G3, z
    ch = dt * math.sqrt(beta) if beta > 0 else dt / r0
    for _ in range(12):
        f, G1, G2, G3, z = F(ch)
        c1, c2, c3 = stumpff(z)
        r = r0 + eta*G1 + c1b*G2          # f'(chi) = r
        dch = f / r
        ch -= dch
        if abs(dch) <= 1e-13*abs(ch):
            break
    if abs(f) > 1e-9*abs(dt):                # Newton failed: bisection fallback
        lo = min(0.0, 2.0*ch, -abs(dt))
        hi = max(0.0, 2.0*ch, abs(dt))
        while F(lo)[0] > 0.0:
            lo *= 2.0
        while F(hi)[0] < 0.0:
            hi *= 2.0
        for _ in range(100):
            mid = 0.5*(lo + hi)
            if F(mid)[0] < 0.0:
                lo = mid
            else:
                hi = mid
        ch = 0.5*(lo + hi)
    f, G1, G2, G3, z = F(ch)
    c1, c2, c3 = stumpff(z)
    r = r0 + eta*G1 + c1b*G2
    ff = 1.0 - G2/r0
    gg = dt - G3
    fd = -G1/(r0*r)
    gd = 1.0 - G2/r
    nx = ff*x + gg*vx; ny = ff*y + gg*vy
    s[0] = nx; s[1] = ny
    s[2] = fd*x + gd*vx; s[3] = fd*y + gd*vy

def accel(x, y, t):
    """Perturbing acceleration in the primary-centric frame (direct + indirect)."""
    th = NOUT*t
    c, sn = math.cos(th), math.sin(th)
    dx = AOUT*c - x; dy = AOUT*sn - y
    d2 = dx*dx + dy*dy; d = math.sqrt(d2)
    k = M2 / (d2*d)
    ki = M2 / (AOUT*AOUT)
    return k*dx - ki*c, k*dy - ki*sn

def kick(s, t, dur):
    ax, ay = accel(s[0], s[1], t)
    s[2] += dur*ax; s[3] += dur*ay

def Zop(s, t, a, b):
    """One elementary corrector step: K(a) I(-b) K(-2a) I(b) K(a)."""
    drift(s, a)
    kick(s, t, -b)
    drift(s, -2.0*a)
    kick(s, t, b)
    drift(s, a)

def apply_corrector(s, t, h, inv, order):
    if order == 3:
        Zop(s, t,  A1*h, -inv*B31*h)
        Zop(s, t, -A1*h,  inv*B31*h)
    elif order == 5:
        Zop(s, t, -A2*h, -inv*B51*h)
        Zop(s, t, -A1*h, -inv*B52*h)
        Zop(s, t,  A1*h,  inv*B52*h)
        Zop(s, t,  A2*h,  inv*B51*h)
    elif order == 7:
        Zop(s, t, -A3*h, -inv*B71*h)
        Zop(s, t, -A2*h, -inv*B72*h)
        Zop(s, t, -A1*h, -inv*B73*h)
        Zop(s, t,  A1*h,  inv*B73*h)
        Zop(s, t,  A2*h,  inv*B72*h)
        Zop(s, t,  A3*h,  inv*B71*h)
    elif order == 11:
        Zop(s, t, -A5*h, -inv*B111*h)
        Zop(s, t, -A4*h, -inv*B112*h)
        Zop(s, t, -A3*h, -inv*B113*h)
        Zop(s, t, -A2*h, -inv*B114*h)
        Zop(s, t, -A1*h, -inv*B115*h)
        Zop(s, t,  A1*h,  inv*B115*h)
        Zop(s, t,  A2*h,  inv*B114*h)
        Zop(s, t,  A3*h,  inv*B113*h)
        Zop(s, t,  A4*h,  inv*B112*h)
        Zop(s, t,  A5*h,  inv*B111*h)
    elif order == 'corrupt3':        # planted negative: wrong sign of inv
        Zop(s, t,  A1*h,  inv*B31*h)
        Zop(s, t, -A1*h, -inv*B31*h)
    else:
        raise ValueError(order)

def measure(s, t):
    x, y, vx, vy = s
    r = math.hypot(x, y); v2 = vx*vx + vy*vy
    a = 1.0/(2.0/r - v2)
    rv = x*vx + y*vy
    ex = (v2 - 1.0/r)*x - rv*vx
    ey = (v2 - 1.0/r)*y - rv*vy
    e = math.hypot(ex, ey)
    w = math.atan2(ey, ex)
    # Jacobi constant, barycentric rotating frame
    mu2 = M2/(1.0 + M2); mu1 = 1.0/(1.0 + M2)
    th = NOUT*t; c, sn = math.cos(th), math.sin(th)
    bx = x - mu2*AOUT*c;          by = y - mu2*AOUT*sn
    bvx = vx + mu2*AOUT*NOUT*sn;  bvy = vy - mu2*AOUT*NOUT*c
    ux = c*bx + sn*by;  uy = -sn*bx + c*by
    uvx = c*bvx + sn*bvy; uvy = -sn*bvx + c*bvy
    # rotating-frame velocity: v_rot = v_inertial (in rotating axes) - omega x r
    rvx = uvx + NOUT*uy;  rvy = uvy - NOUT*ux
    r1 = math.hypot(ux + mu2*AOUT, uy)
    r2 = math.hypot(ux - mu1*AOUT, uy)
    CJ = NOUT*NOUT*(ux*ux + uy*uy) + 2.0*((1.0)/r1 + M2/r2) - (rvx*rvx + rvy*rvy)
    return a, e, w, CJ

def run(e0, n, order, orbits, out_every=1, m2=None, aout=None):
    global M2, AOUT, NOUT
    if m2 is not None:
        M2 = m2; AOUT = aout; NOUT = math.sqrt((1.0 + m2)/aout**3)
    """WH DKD map, n kicks per orbit. order None|3|5|'corrupt3'."""
    h = TWO_PI / n
    s = [1.0 - e0, 0.0, 0.0, math.sqrt((1.0 + e0)/(1.0 - e0))]
    t = 0.0
    if order:
        apply_corrector(s, t, h, 1.0, order)     # real -> mapping
    CJ0, ws, CJs, es = None, [], [], []
    for k in range(1, orbits + 1):
        for _ in range(n):
            drift(s, h/2); t += h/2
            kick(s, t, h)
            drift(s, h/2); t += h/2
        if k % out_every == 0:
            if order:
                sc = s[:]
                apply_corrector(sc, t, h, -1.0, order)   # mapping -> real
                a, e, w, CJ = measure(sc, t)
            else:
                a, e, w, CJ = measure(s, t)
            if CJ0 is None:
                CJ0 = CJ
            ws.append(w); CJs.append((CJ - CJ0)/abs(CJ0)); es.append(e)
    # unwrap and fit slope of w vs orbit index
    for i in range(1, len(ws)):
        d = ws[i] - ws[i-1]
        while d > math.pi:  ws[i] -= TWO_PI; d = ws[i] - ws[i-1]
        while d < -math.pi: ws[i] += TWO_PI; d = ws[i] - ws[i-1]
    N = len(ws)
    xs = [(i + 1)*out_every for i in range(N)]
    xm = sum(xs)/N; ym = sum(ws)/N
    slope = sum((x - xm)*(y - ym) for x, y in zip(xs, ws)) / sum((x - xm)**2 for x in xs)
    resid = max(abs(y - ym - slope*(x - xm)) for x, y in zip(xs, ws))
    return {
        'prec': slope, 'fit_resid': resid,
        'dCJ_max': max(abs(c) for c in CJs),
        'dCJ_last': abs(CJs[-1]),
        'e_max_drift': max(abs(e - es[0]) for e in es),
    }

def oracle(e0, orbits=600):
    return run(e0, 128, 5, orbits)

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'smoke'
    if mode == 'smoke':
        s = [0.8, 0.0, 0.0, math.sqrt((1.0 + 0.2)/(1.0 - 0.2))]
        s0 = s[:]
        drift(s, TWO_PI*math.sqrt(1.0**3))      # one full period (a=1)
        print('roundtrip dx=%.3e dv=%.3e' % (abs(s[0]-s0[0]), abs(s[2]-s0[2])))
        for n in (16, 64):
            r = run(0.2, n, None, 400)
            print('plain n=%2d: prec=%.6e resid=%.2e dCJmax=%.2e dCJlast=%.2e'
                  % (n, r['prec'], r['fit_resid'], r['dCJ_max'], r['dCJ_last']))
        o = oracle(0.2, 400)
        print('oracle  : prec=%.6e resid=%.2e dCJmax=%.2e' % (o['prec'], o['fit_resid'], o['dCJ_max']))
        print('quadrupole est prec ~ %.3e' % (0.75*NOUT*(M2/(1+M2))*(1.0/AOUT**3)*(1+1.5*0.04)))
        return
    if mode == 'sweep':
        E = [0.2, 0.6]; NS = [2, 4, 8, 16, 32, 64]; ORD = [None, 3, 5, 'corrupt3']
        out = {'meta': {'M2': M2, 'AOUT': AOUT, 'orbits': 600,
                        'thresholds': {'prec_rel': 0.01, 'dCJ': 1e-4}}, 'cases': {}}
        for e0 in E:
            o = oracle(e0)
            out['meta']['oracle_prec_e%s' % e0] = o['prec']
            print('e=%.1f oracle prec=%.6e resid=%.2e dCJ=%.2e'
                  % (e0, o['prec'], o['fit_resid'], o['dCJ_max']))
            for order in ORD:
                for n in NS:
                    r = run(e0, n, order, 600)
                    rel = abs(r['prec'] - o['prec'])/abs(o['prec'])
                    ok = (rel <= 0.01) and (r['dCJ_max'] <= 1e-4)
                    out['cases']['e%s-%s-n%d' % (e0, order, n)] = dict(r, prec_rel=rel, ok=ok)
                    print('e=%.1f %-8s n=%2d: prec_rel=%8.2e dCJ=%8.2e ok=%s'
                          % (e0, str(order), n, rel, r['dCJ_max'], ok))
        json.dump(out, open('results-sweep.json', 'w'), indent=1)
    if mode == 'heldout':
        E = [0.4, 0.85]; NS = [2, 4, 8, 16, 32, 64]
        out = {'meta': {'M2': M2, 'AOUT': AOUT, 'orbits': 600}, 'cases': {}}
        for e0 in E:
            o = oracle(e0)
            out['meta']['oracle_prec_e%s' % e0] = o['prec']
            print('e=%.2f oracle prec=%.6e resid=%.2e dCJ=%.2e' % (e0, o['prec'], o['fit_resid'], o['dCJ_max']))
            for order in (None, 3, 5):
                for n in NS:
                    r = run(e0, n, order, 600)
                    rel = abs(r['prec'] - o['prec'])/abs(o['prec'])
                    ok = (rel <= 0.01) and (r['dCJ_max'] <= 1e-4)
                    out['cases']['e%s-%s-n%d' % (e0, order, n)] = dict(r, prec_rel=rel, ok=ok)
                    print('e=%.2f %-4s n=%2d: prec_rel=%8.2e dCJ=%8.2e ok=%s'
                          % (e0, str(order), n, rel, r['dCJ_max'], ok))
        json.dump(out, open('results-heldout.json', 'w'), indent=1)

if __name__ == '__main__':
    main()
