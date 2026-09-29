#!/usr/bin/env python3
"""Smoke tests for rings.py before the decisive run (cases here are NOT metric seeds)."""
import math
import sys
sys.path.insert(0, '.')
from rings import (periapsis_elliptic, deflection_quadrature, deflection_tail,
                   bound_constants, bound_period_quad, seed_state, binet_run,
                   river_run, tilt_run, square_run, ring_band, _cell_of)

ok = True
def check(name, got, want, rtol):
    global ok
    err = abs(got - want) / abs(want)
    flag = "OK " if err <= rtol else "FAIL"
    if err > rtol:
        ok = False
    print(f"{flag} {name}: got={got:.8e} want={want:.8e} rel={err:.2e}")

# --- oracle vs its own series
p, e = 100.0, 0.5
check("periapsis series p=100 e=.5", periapsis_elliptic(p, e),
      6 * math.pi / p * (1 + (18 + e * e) / (4 * p)), 2e-3)
check("periapsis series p=1000 e=.1", periapsis_elliptic(1000.0, 0.1),
      6 * math.pi / 1000 * (1 + 18.01 / 4000), 1e-3)
b = 100.0
check("deflection series b=100", deflection_quadrature(b), 4 / b + 15 * math.pi / (4 * b * b), 1e-4)
check("deflection series b=1000", deflection_quadrature(1000.0),
      4 / 1000 + 15 * math.pi / 4e6, 1e-3)
pp, ee = 20.0, 0.2
E, L = bound_constants(pp, ee)
T, tau = bound_period_quad(pp, ee)
a = pp / (1 - ee * ee)
check("period series t p=20 e=.2", T, 2 * math.pi * a ** 1.5 * (1 + 3 / a), 2e-3)
check("period series tau p=20 e=.2", tau, 2 * math.pi * a ** 1.5 * (1 + 1.5 / a), 2e-3)
print(f"     tail b=10 r0=1e4: {deflection_tail(10.0, 1e4):.3e}  b=1000: {deflection_tail(1000.0, 1e4):.3e}")

# --- binet on p=20 e=0.5 (picture case, not a metric seed)
for m in (8, 16, 32):
    E, L, u_apo = seed_state(20.0, 0.5)
    res = binet_run(m, E, L, u_apo, ncycles=3)
    dphi, dt, nc, rp, ra = res['cycles'][0]
    adv_or = periapsis_elliptic(20.0, 0.5)
    T_or = bound_period_quad(20.0, 0.5)[0]
    check(f"binet-m{m} advance p=20 e=.5", dphi - 2 * math.pi, adv_or, 0.02)
    check(f"binet-m{m} period  p=20 e=.5", dt, T_or, 0.005)
    d2 = res['cycles'][1][0] - 2 * math.pi
    print(f"     binet-m{m} cycle2 vs cycle1 advance: {abs(d2 - (dphi - 2*math.pi)):.2e}, "
          f"crossings={nc}, r_p={rp:.4f} r_a={ra:.4f} (exact {20/1.5:.4f}/{40:.4f})")

# --- river on p=20 e=0.5
for m in (16, 32):
    E, L, u_apo = seed_state(20.0, 0.5)
    r_apo = 1.0 / u_apo
    k = ring_band(r_apo, m)
    Rc = exp((k + 0.5) * math.log(2) / m)
    beta = -math.sqrt(2.0 / Rc)
    p_t = L / r_apo
    pr1 = -beta * math.sqrt((1.0 + p_t * p_t) / (1.0 - beta * beta))
    # roots for H=E, pick |v_r| smallest
    from rings import _pr_roots_ring, _vr_of
    roots = _pr_roots_ring(E, L, r_apo, beta, False)
    best = min(roots, key=lambda rt: abs(_vr_of(rt[1], rt[0], beta, False)))
    p_r0, p_t0 = best
    res = river_run(m, r_apo, 0.0, p_r0, p_t0, E, ncycles=3)
    dphi, dt, nc, rp, ra = res['cycles'][0]
    adv_or = periapsis_elliptic(20.0, 0.5)
    T_or = bound_period_quad(20.0, 0.5)[0]
    check(f"river-m{m} advance p=20 e=.5", dphi - 2 * math.pi, adv_or, 0.02)
    check(f"river-m{m} period  p=20 e=.5", dt, T_or, 0.005)
    print(f"     river-m{m} crossings={nc} r_p={rp:.4f} r_a={ra:.4f}")

# --- square on p=20 e=0.5
E, L, u_apo = seed_state(20.0, 0.5)
r_apo = 1.0 / u_apo
lvl, i, j, s, cx, cy, rc = _cell_of(r_apo, 0.0)
beta = -math.sqrt(2.0 / rc)
bx, by = beta * cx / rc, beta * cy / rc
from rings import _pr_roots_edge
p_t = L / r_apo
r1, r2 = _pr_roots_edge(E, p_t, bx, by, False)
cands = []
for pr in (r1, r2):
    g = math.sqrt(1 + pr * pr + p_t * p_t)
    cands.append((abs(pr / g + bx), pr))
p_r0 = min(cands)[1]
res = square_run(r_apo, 0.0, p_r0, p_t, E, ncycles=3)
if res['cycles']:
    dphi, dt, nc, rp, ra = res['cycles'][0]
    adv_or = periapsis_elliptic(20.0, 0.5)
    T_or = bound_period_quad(20.0, 0.5)[0]
    print(f"     square advance rel err {abs(dphi-2*math.pi-adv_or)/adv_or:.3e}, "
          f"period rel err {abs(dt-T_or)/T_or:.3e}, crossings={nc}")
else:
    print(f"FAIL square produced no cycles: {res}")

# --- tilt on p=20 e=0.5 (expect Newtonian: ~zero anomaly, wrong period)
E, L, u_apo = seed_state(20.0, 0.5)
r_apo = 1.0 / u_apo
k = ring_band(r_apo, 16)
Rc = exp((k + 0.5) * math.log(2) / 16)
beta = -math.sqrt(2.0 / Rc)
p_t = L / r_apo
pr1 = -beta * math.sqrt((1.0 + p_t * p_t) / (1.0 - beta * beta))
g0 = math.sqrt(1 + pr1 * pr1 + p_t * p_t)
res = tilt_run(16, r_apo, 0.0, 0.0, p_t / g0, ncycles=3)
if res['cycles']:
    dphi, dt, nc, rp, ra = res['cycles'][0]
    print(f"     tilt anomaly={dphi - 2*math.pi:+.4e} (GR {periapsis_elliptic(20.0, 0.5):.4e}) "
          f"period rel err vs GR {abs(dt - bound_period_quad(20.0,0.5)[0])/bound_period_quad(20.0,0.5)[0]:.2e}")
else:
    print(f"FAIL tilt produced no cycles: {res}")

# --- light b=100: binet + river vs oracle
b = 100.0
r0 = 1e4
u0 = 1.0 / r0
up0 = math.sqrt(1.0 / b**2 - u0 * u0 + 2 * u0**3)
res = binet_run(32, 1.0, b, u0, w0=up0, light=True, ncycles=1, escape_u=u0, max_pieces=20000)
import math as _m
def binet_bend(res, u_in, up_in, phi_in):
    # incoming direction
    rad = -up_in / u_in**2
    tang = 1.0 / u_in
    n = math.hypot(rad, tang)
    vin = (rad * math.cos(phi_in) - tang * math.sin(phi_in),
           rad * math.sin(phi_in) + tang * math.cos(phi_in))
    u_out, w_out = res['u'], res['w']
    phi_out = res['phi']
    rad = -w_out / u_out**2
    tang = 1.0 / u_out
    n = math.hypot(rad, tang)
    vout = (rad * math.cos(phi_out) - tang * math.sin(phi_out),
            rad * math.sin(phi_out) + tang * math.cos(phi_out))
    dot = max(-1.0, min(1.0, vin[0]*vout[0] + vin[1]*vout[1]))
    return math.acos(dot)
phi_in = math.atan2(-b, -math.sqrt(r0*r0 - b*b))
if res['escaped']:
    bend = binet_bend(res, u0, up0, phi_in) + 2 * deflection_tail(b, r0)
    check("binet-m32 light bend b=100", bend, deflection_quadrature(b), 0.01)
else:
    print(f"FAIL binet light b=100 not escaped: absorbed={res['absorbed']} to={res['timeout']} phi={res['phi']:.2f}")

from rings import _pr_roots_ring as prr
x0, y0 = -math.sqrt(r0*r0 - b*b), -b
k0 = ring_band(r0, 32)
Rc = exp((k0 + 0.5) * math.log(2) / 32)
beta = -math.sqrt(2.0 / Rc)
H = 1.0 + beta * (x0 / r0)   # p=(1,0): beta.p = beta*x/r
res = river_run(32, x0, y0, 1.0, 0.0, H, light=True, ncycles=1, escape_r=r0, max_events=200000)
if res['escaped']:
    ang_out = math.atan2(res['py'], res['px'])
    bend = ang_out - 0.0 + 2 * deflection_tail(b, r0)
    check("river-m32 light bend b=100", bend, deflection_quadrature(b), 0.01)
else:
    print(f"FAIL river light b=100: absorbed={res['absorbed']} to={res['timeout']}")

# --- capture: E=1 from r=100, L=2 (absorb) and L=6 (escape)
for Lc in (2.0, 6.0):
    r0c = 100.0
    u_start = 1.0 / r0c
    w_start = math.sqrt(2 * u_start / Lc**2 - u_start**2 + 2 * u_start**3)
    res = binet_run(16, 1.0, Lc, u_start, w0=w_start, ncycles=1, escape_u=u_start,
                    max_pieces=20000)
    exp_abs = Lc < 4.0
    got_abs = res['absorbed']
    flag = "OK " if got_abs == exp_abs else "FAIL"
    if got_abs != exp_abs:
        ok = False
    print(f"{flag} binet-m16 capture L={Lc}: absorbed={got_abs} expected={exp_abs}")

print("\nALL OK" if ok else "\nSOME FAILURES")
