#!/usr/bin/env python3
"""Red-team falsifier for docs/representation.md. M=G=c=1, float64, equatorial.
A: Binet band stitching (binet-m16, r1 spec) precession/period error at e>0.7.
B: cycle multiply-add gains: exact-GR radial cycle, d(Dphi)/dL, dT/dE, truncation.
C: past-light-cone root count for an orbiting emitter seen at high beta.
"""
import numpy as np
from scipy.integrate import solve_ivp

# ---------- exact GR Schwarzschild (u=1/r, ' = d/dphi) ----------
def rhs(phi, y, L2):
    u, up, t, E, L = y
    return [up, 1.0/L2 + 3*u*u - u, E/(L*u*u*(1-2*u)), 0, 0]

def seed_from_pa(rp, ra):
    """GR osculating orbit through periapsis rp and apoapsis ra. Returns (u_p, L)."""
    up_, ua_ = 1.0/rp, 1.0/ra
    num = (1-2*ua_) - (1-2*up_)
    den = (1-2*up_)*up_**2 - (1-2*ua_)*ua_**2
    L2 = num/den
    return up_, np.sqrt(L2)

def cycle_exact(u_p, L, n=1):
    """Integrate one radial cycle from periapsis; return (dphi, T, E)."""
    L2 = L*L
    E = np.sqrt((1-2*u_p)*(1+L2*u_p*u_p))
    u_pp = 1.0/L2 + 3*u_p*u_p - u_p   # u'' at periapsis (<0)
    eps0 = 1e-6
    y0 = [u_p + 0.5*u_pp*eps0*eps0, u_pp*eps0, 0.0, E, L]
    def peri(phi, y, L2): return y[1]
    peri.direction = -1.0; peri.terminal = True
    s = solve_ivp(rhs, [1e-12, 100*np.pi+50], y0, args=(L2,), events=peri,
                  method='DOP853', rtol=1e-11, max_step=0.05,
                  atol=[1e-13, 1e-13, 1e-8, 1, 1])
    return s.t_events[0][0], s.y[2,-1], E

# ---------- Binet band model (r1 spec, m=16) ----------
M2LOG2 = 1.0/np.log(2.0)
def band_edges():
    # u edges dyadic: u = 2^(-k/m) for integer k; band index k(u) = floor(-log2(u)*m)
    return None

def band_index(u, m):
    return int(np.floor(-np.log2(u)*m))

def band_center_u(k, m):
    return 2.0**(-(k+0.5)/m)

def step_band(u, up, k, m, L):
    """Propagate inside band k until edge crossing or turning point.
    Return (kind, new_u, new_up, dphi). kind in {edge, turn}."""
    uc = band_center_u(k, m)
    w2 = 1.0 - 6.0*uc
    C = 1.0/(L*L) - 3.0*uc*uc
    up2 = C/w2 if abs(w2) > 1e-14 else C*1e14   # particular solution of u'' + w2*u = C
    e_in, e_out = 2.0**(-k/m), 2.0**(-(k+1)/m)   # larger u, smaller u
    cands = []  # (dphi, kind, u2, p2)
    if w2 > 1e-14:
        w = np.sqrt(w2)
        x0, v0 = u - up2, up/w
        R = np.hypot(x0, v0)
        al = np.arctan2(v0, x0)
        def recon(th):
            x = R*np.cos(th - al); v = -R*np.sin(th - al)
            return up2 + x, v*w
        # turns: th = al + n*pi
        for n in range(3):
            th = al + n*np.pi
            if th > 1e-13:
                u2, p2 = recon(th); cands.append((th/w, 'turn', u2, p2))
        for tgt in (e_in - up2, e_out - up2):
            if R > 0 and abs(tgt) <= R:
                a = np.arccos(tgt/R)
                for th in (al + a, al - a, al + a + 2*np.pi, al - a + 2*np.pi):
                    if th > 1e-13:
                        u2, p2 = recon(th); cands.append((th/w, 'edge', u2, p2))
    elif w2 < -1e-14:
        q = np.sqrt(-w2)
        x0, s0 = u - up2, up/q
        def recon(th):
            x = x0*np.cosh(th) + s0*np.sinh(th)
            p = q*(x0*np.sinh(th) + s0*np.cosh(th))
            return up2 + x, p
        if abs(s0) < abs(x0) and x0 != 0:
            r = -s0/x0
            if abs(r) < 1:
                th = np.arctanh(r)
                if th > 1e-13:
                    u2, p2 = recon(th); cands.append((th/q, 'turn', u2, p2))
        A, B = (x0+s0)/2, (x0-s0)/2
        for tgt in (e_in - up2, e_out - up2):
            D = tgt*tgt - 4*A*B
            if D >= 0:
                for ex in ((tgt+np.sqrt(D))/2, (tgt-np.sqrt(D))/2):
                    if ex > 0 and A != 0:
                        th = np.log(ex/A)
                        if th > 1e-13:
                            u2, p2 = recon(th); cands.append((th/q, 'edge', u2, p2))
    else:  # parabolic band w~0: u'' = const
        acc = 1.0/(L*L) - 3*uc*uc - uc
        c = up2 + 0*uc
        # u(d) = u + up d + 0.5*acc d^2 with acc = up2 + w2*0 ... use w2=0: u''=up2 - u ~ treat linear
        # w2==0 exactly is measure-zero; approximate with tiny w
        w = np.sqrt(max(abs(w2), 1e-12))
        x0, v0 = u - up2, up/w
        R = np.hypot(x0, v0); al = np.arctan2(v0, x0)
        for n in range(3):
            th = al + n*np.pi
            if th > 1e-13:
                x = R*np.cos(th-al); v=-R*np.sin(th-al)
                cands.append((th/w, 'turn', up2+x, v*w))
    if not cands: return ('lost', u, up, 0.0)
    d, kind, u2, p2 = min(cands, key=lambda c: c[0])
    if not np.isfinite(u2) or not np.isfinite(p2): return ('lost', u, up, 0.0)
    return (kind, u2, p2, d)

def cycle_band(u_p, L, m=16, max_steps=200000, join="cont"):
    """One radial cycle (periapsis->periapsis) in the band model.
    join='cont': u,u' continuous (rung r1 letter). join='EL': E,L conserved at
    rings, u' = -sign*sqrt((E^2-V(u))/L^2) (design line: crossings conserve E,L).
    Returns (dphi, T, crossings) or None if lost/plunged."""
    L2 = L*L
    E = np.sqrt((1-2*u_p)*(1+L2*u_p*u_p))
    u, up = u_p, 0.0
    phi = 0.0; t = 0.0; cross = 0; turned = False
    for _ in range(max_steps):
        k = band_index(u, m)
        kind, u2, p2, d = step_band(u, up, k, m, L)
        if kind == 'lost' or not np.isfinite(u2): return None
        if kind == 'edge':
            # u2 can land exactly ON the shared edge; nudge one ulp into the
            # direction of motion so band_index assigns the band being entered.
            u2 = np.nextafter(u2, 2.0 if u2 > u else 0.0)
        if join == "EL" and kind == 'edge':
            V = (1-2*u2)*(1+L2*u2*u2)
            arg = (E*E - V)/L2
            if arg < 0: return None
            p2 = np.sign(p2 or 1.0)*np.sqrt(arg)
        try:
            xm = 0.5*(u+u2)
            fm = E/(L*xm*xm*(1-2*xm))
            f0 = E/(L*u*u*(1-2*u)); f1 = E/(L*u2*u2*(1-2*u2))
            if not all(map(np.isfinite, (fm, f0, f1))): return None
            t += d/6*(f0 + 4*fm + f1)
        except Exception:
            return None
        phi += d
        u, up = u2, p2
        if u > 0.45: return None
        if kind == 'turn':
            if turned:
                return phi, t, cross
            turned = not turned
        else:
            cross += 1
    return None

print("="*78)
print("A. Binet band stitching (m=16) vs exact GR, p=10 fixed, e swept")
print("   r1 sampled only e<=0.7; seeds p log-U [10,1000]")
print("="*78)
p_fix = 10.0
def uL_of(p, e):
    rp, ra = p/(1+e), p/(1-e)
    return seed_from_pa(rp, ra)
print(f"{'p':>5} {'e':>4} {'a':>8} {'dphi_GR':>9}  (relerr cycle | relerr advance | relerr T | crossings, per join)")
for (p_fix, e) in [(10,0.5),(10,0.6),(10,0.65),(13,0.7),(13,0.8),(13,0.9),(13,0.95),(13,0.98),(13,0.99)]:
    if 6+2*e > p_fix*(1+e)/(1+e): pass
    # p = a(1-e^2); r_peri = p/(1+e); require p > 6+2e (bound, r1 rule)
    a = p_fix/(1-e*e)
    u_p, L = uL_of(p_fix, e)
    if p_fix <= 6+2*e:
        print(f"{e:6.2f}  p={p_fix} violates p>6+2e={6+2*e:.1f} (plunge) -- excluded")
        continue
    dG, TG, E = cycle_exact(u_p, L)
    advG = dG - 2*np.pi
    row = f"{p_fix:5.0f} {e:4.2f} {a:8.1f} {dG:9.4f} "
    for join in ("cont", "EL"):
        dB = cycle_band(u_p, L, 16, join=join)
        if dB is None:
            row += f" | {join}: LOST      LOST       LOST"
            continue
        dphiB, TB, cr = dB
        advB = dphiB - 2*np.pi
        row += f" | {join}: {abs(dphiB-dG)/dG:7.3%}adv {abs(advB-advG)/advG:8.2%} T {abs(TB-TG)/TG:7.3%} x{cr}"
    print(row)

print()
print("="*78)
print("B. cycle multiply-add gains (exact GR cycles; kicks are 1st-order updates)")
print("   design: 'a kick updates the cycle by a multiply-add', budget: 1 floor unit/event")
print("="*78)
def gains(u_p, L, rel_kick=1e-4):
    dG, TG, E = cycle_exact(u_p, L)
    dG2, TG2, E2 = cycle_exact(u_p, L*(1+rel_kick))
    dGm, TGm, _ = cycle_exact(u_p, L*(1-rel_kick))
    dL = L*rel_kick
    dphidL = (dG2-dGm)/(2*dL)
    # linear-update truncation error for a kick of +dL (and -dL)
    lin_p = dG + dphidL*dL
    lin_m = dG - dphidL*dL
    err_p = dG2 - lin_p   # >0 means convex: systematic under-correction
    err_m = dGm - lin_m
    return dG, TG, E, dphidL, err_p, err_m
print(f"{'case':>28} {'dphi':>10} {'gainL':>10} {'err(+dL)':>11} {'err(-dL)':>11} {'same_sign':>9}")
cases = []
for p in [12, 10, 9, 8.5, 8.2, 8.05]:
    e = 0.9
    cases.append((f"e=0.9 p={p} (crit~{6+2*e:.1f})", uL_of(p, e)))
for e in [0.9, 0.95, 0.98, 0.99]:
    p = 1.3*(6+2*e)  # fixed margin above critical
    cases.append((f"e={e} p={p:.1f} (crit~{6+2*e:.1f})", uL_of(p, e)))
for name, (u_p, L) in cases:
    try:
        dG, TG, E, dphidL, ep, em = gains(u_p, L, 1e-4)
        gainL = abs(dphidL)*L/dG
        print(f"{name:>28} {dG:10.3f} {gainL:10.1f} {ep:11.3e} {em:11.3e} {str(np.sign(ep)==np.sign(em)):>9}")
    except Exception as ex:
        print(f"{name:>28}  failed: {ex}")

print()
print("="*78)
print("C. past-light-cone roots for orbiting emitter, observer at beta")
print("   design: 'each visible tube crosses the observer's past light cone once'")
print("="*78)
for beta in [0.0, 0.9, 0.99, 0.995]:
    gam = 1/np.sqrt(1-beta*beta)
    R, Om = 1.0, 0.2
    n_roots_all = []
    for tobj in np.linspace(100, 100+gam*5, 50):  # observer frame; frame=1/60 obs-proper
        dt_frame = gam/60.0
        # roots of f(te)=tobs - te - |x_e(te)-x_o(tobs)| over te window
        te = np.linspace(tobj-60, tobj, 400001)[1:-1]
        xe = np.stack([R*np.cos(Om*te), R*np.sin(Om*te)], 0)
        xo = np.array([beta*tobj, 0.0])
        f = tobj - te - np.linalg.norm(xe-xo, axis=0)
        s = np.sign(f)
        roots = int(np.sum(s[:-1]*s[1:] < 0))
        n_roots_all.append(roots)
    print(f"beta={beta:5.3f} k={np.sqrt((1+beta)/(1-beta)):7.2f}  roots per gather: "
          f"min={min(n_roots_all)} max={max(n_roots_all)} (monotone f => 1 root)")
