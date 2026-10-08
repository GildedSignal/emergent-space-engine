# Instrument the author's kicked_run: how often does the f1<0 wrap flip omega by pi,
# and what eccentricity does the toy actually carry? If flips * 2e*v >> kick sizes,
# A(tau) is instrument noise, not shock convexity.
import math
MU_S = 1.0e-3; R = 1.0; R_HILL = R*(MU_S/3.0)**(1.0/3.0); N_ORB = 300

def ecc_vec(x, y, vx, vy):
    r = math.hypot(x, y); v2 = vx*vx+vy*vy; rv = x*vx+y*vy
    return (v2-1.0/r)*x - rv*vx, (v2-1.0/r)*y - rv*vy

def kepler_step(x, y, vx, vy, dt, stats=None):
    h = x*vy-y*vx
    ex, ey = ecc_vec(x,y,vx,vy)
    e = math.hypot(ex,ey)
    a = 1.0/(2.0/math.hypot(x,y)-(vx*vx+vy*vy))
    if a <= 0: raise ValueError
    n = a**-1.5
    cosf = (ex*x+ey*y)/(e*math.hypot(x,y)) if e > 1e-14 else x/math.hypot(x,y)
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
    if stats is not None and f1 < 0: stats[0] += 1; stats[1] = max(stats[1], e)
    p = a*(1-e*e); r1 = p/(1+e*math.cos(f1))
    v2 = 2.0/r1 - 1.0/a; hdot = math.sqrt(p)
    vr = math.sqrt(max(0.0, v2 - hdot*hdot/(r1*r1)))
    if f1 > math.pi: vr = -vr
    vt = hdot/r1
    om = math.atan2(ey,ex)
    px, py = r1*math.cos(f1), r1*math.sin(f1)
    x1 = px*math.cos(om)-py*math.sin(om); y1 = px*math.sin(om)+py*math.cos(om)
    vpx, vpy = vr*math.cos(f1)-vt*math.sin(f1), vr*math.sin(f1)+vt*math.cos(f1)
    vx1 = vpx*math.cos(om)-vpy*math.sin(om); vy1 = vpx*math.sin(om)+vpy*math.cos(om)
    return x1,y1,vx1,vy1

def sec_pos(t, phi): th = t + phi; return R*math.cos(th), R*math.sin(th)
def tide(x, y, t, phi):
    sx, sy = sec_pos(t, phi)
    dx, dy = sx-x, sy-y; d3 = (dx*dx+dy*dy)**1.5; s3 = R**3
    return MU_S*(dx/d3 - sx/s3), MU_S*(dy/d3 - sy/s3)

for tau in (0.05, 0.10, 0.17, 0.25):
    for phi in (0.0, math.pi/2, math.pi):
        a_m = tau*R_HILL
        x, y = a_m, 0.0; vx, vy = 0.0, 1.0/math.sqrt(a_m)
        P = a_m**1.5; K = 16; dt = P/K; t = 0.0
        stats = [0, 0.0]; emax = 0.0
        for _ in range(N_ORB*K):
            x,y,vx,vy = kepler_step(x,y,vx,vy,dt,stats)
            ax, ay = tide(x,y,t+dt,phi)
            vx += ax*dt; vy += ay*dt; t += dt
            emax = max(emax, math.hypot(*ecc_vec(x,y,vx,vy)))
        nsteps = N_ORB*K
        print(f"tau={tau:5.2f} phi={phi/math.pi:4.2f}pi  flips={stats[0]:5d}/{nsteps} ({100*stats[0]/nsteps:5.2f}%)  e_at_flip_max={stats[1]:9.2e}  e_max_run={emax:9.2e}  inj_vel_scale={2*stats[1]*(1/math.sqrt(a_m)) if stats[0] else 0:.2e}")
