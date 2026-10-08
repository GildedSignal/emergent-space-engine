# Shared harness: the author's toy with the propagator branch-corrected.
# kepler_step_orig: verbatim from shock_probe.py. kepler_step_fixed: one branch fixed
# (descending branch is f in (pi, 2pi) OR f < 0). Everything else identical.
import math
MU_S = 1.0e-3; R = 1.0; R_HILL = R*(MU_S/3.0)**(1.0/3.0); N_ORB = 300

def ecc_vec(x, y, vx, vy):
    r = math.hypot(x, y); v2 = vx*vx+vy*vy; rv = x*vx+y*vy
    return (v2-1.0/r)*x - rv*vx, (v2-1.0/r)*y - rv*vy

def kepler_core(x, y, vx, vy, dt, fixed):
    ex, ey = ecc_vec(x, y, vx, vy)
    e = math.hypot(ex, ey)
    a = 1.0/(2.0/math.hypot(x, y)-(vx*vx+vy*vy))
    if a <= 0: raise ValueError("unbound")
    n = a**-1.5
    cosf = (ex*x+ey*y)/(e*math.hypot(x, y)) if e > 1e-14 else x/math.hypot(x, y)
    cosf = max(-1.0, min(1.0, cosf)); f0 = math.acos(cosf)
    if (x*vx+y*vy) < 0: f0 = 2*math.pi - f0
    E0 = 2*math.atan2(math.sqrt(1-e)*math.sin(f0/2), math.sqrt(1+e)*math.cos(f0/2))
    M0 = E0 - e*math.sin(E0)
    M1 = (M0 + n*dt + math.pi) % (2*math.pi) - math.pi
    E = M1 if e < 0.8 else math.pi
    for _ in range(60):
        d = (E - e*math.sin(E) - M1)/(1 - e*math.cos(E)); E -= d
        if abs(d) < 1e-15: break
    f1 = 2*math.atan2(math.sqrt(1+e)*math.sin(E/2), math.sqrt(1-e)*math.cos(E/2))
    p = a*(1-e*e); r1 = p/(1+e*math.cos(f1))
    v2 = 2.0/r1 - 1.0/a; hdot = math.sqrt(p)
    vr = math.sqrt(max(0.0, v2 - hdot*hdot/(r1*r1)))
    if fixed:
        if f1 < 0 or f1 > math.pi: vr = -vr     # descending branch, both conventions
    else:
        if f1 > math.pi: vr = -vr               # author's branch (f1<0 wrong)
    vt = hdot/r1; om = math.atan2(ey, ex)
    px, py = r1*math.cos(f1), r1*math.sin(f1)
    x1 = px*math.cos(om)-py*math.sin(om); y1 = px*math.sin(om)+py*math.cos(om)
    vpx, vpy = vr*math.cos(f1)-vt*math.sin(f1), vr*math.sin(f1)+vt*math.cos(f1)
    return x1, y1, vpx*math.cos(om)-vpy*math.sin(om), vpx*math.sin(om)+vpy*math.cos(om)

def sec_pos(t, phi): th = t + phi; return R*math.cos(th), R*math.sin(th)
def tide(x, y, t, phi):
    sx, sy = sec_pos(t, phi)
    dx, dy = sx-x, sy-y; d3 = (dx*dx+dy*dy)**1.5; s3 = R**3
    return MU_S*(dx/d3 - sx/s3), MU_S*(dy/d3 - sy/s3)
def accel_full(x, y, t, phi):
    r3 = (x*x+y*y)**1.5; tx, ty = tide(x, y, t, phi)
    return -x/r3+tx, -y/r3+ty
def rk4_truth(x, y, vx, vy, T, n, phi):
    h = T/n; t = 0.0
    for _ in range(n):
        ax1, ay1 = accel_full(x, y, t, phi)
        x2, y2, vx2, vy2 = x+vx*h/2, y+vy*h/2, vx+ax1*h/2, vy+ay1*h/2
        ax2, ay2 = accel_full(x2, y2, t+h/2, phi)
        x3, y3, vx3, vy3 = x+vx2*h/2, y+vy2*h/2, vx+ax2*h/2, vy+ay2*h/2
        ax3, ay3 = accel_full(x3, y3, t+h/2, phi)
        x4, y4, vx4, vy4 = x+vx3*h, y+vy3*h, vx+ax3*h, vy+ay3*h
        ax4, ay4 = accel_full(x4, y4, t+h, phi)
        x += h*(vx+2*vx2+2*vx3+vx4)/6.0; y += h*(vy+2*vy2+2*vy3+vy4)/6.0
        vx += h*(ax1+2*ax2+2*ax3+ax4)/6.0; vy += h*(ay1+2*ay2+2*ay3+ay4)/6.0
        t += h
    return x, y, vx, vy
def wrap2pi(a): return a % (2*math.pi)
def kicked_run(a_moon, K, n_orb, phi, fixed):
    x, y = a_moon, 0.0; vx, vy = 0.0, 1.0/math.sqrt(a_moon)
    P = a_moon**1.5; dt = P/K; t = 0.0
    ex0, ey0 = ecc_vec(x, y, vx, vy); om0 = math.atan2(ey0, ex0)
    for _ in range(n_orb*K):
        x, y, vx, vy = kepler_core(x, y, vx, vy, dt, fixed)
        ax, ay = tide(x, y, t+dt, phi)
        vx += ax*dt; vy += ay*dt; t += dt
    ex1, ey1 = ecc_vec(x, y, vx, vy); om1 = math.atan2(ey1, ex1)
    return wrap2pi(om1-om0)/n_orb
def truth_run(a_moon, n_orb, phi, steps_per_orb=4000):
    T = n_orb*a_moon**1.5
    x, y = a_moon, 0.0; vx, vy = 0.0, 1.0/math.sqrt(a_moon)
    ex0, ey0 = ecc_vec(x, y, vx, vy); om0 = math.atan2(ey0, ex0)
    x, y, vx, vy = rk4_truth(x, y, vx, vy, T, n_orb*steps_per_orb, phi)
    ex1, ey1 = ecc_vec(x, y, vx, vy); om1 = math.atan2(ey1, ex1)
    return wrap2pi(om1-om0)/n_orb
