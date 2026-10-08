# Direct: uniform M0, fixed e, one kepler_step of P/16. Report f1<0 fraction,
# omega-flip fraction, and the ACTUAL state error vs an exact reference (same
# M0+dt rebuilt from scratch with the correct branch).
import math
def ecc_vec(x, y, vx, vy):
    r = math.hypot(x, y); v2 = vx*vx+vy*vy; rv = x*vx+y*vy
    return (v2-1.0/r)*x - rv*vx, (v2-1.0/r)*y - rv*vy

def state_from(a, e, om, f):
    p = a*(1-e*e); r = p/(1+e*math.cos(f)); v = math.sqrt(2.0/r - 1.0/a); h = math.sqrt(p)
    vr = math.sqrt(max(0.0, v*v - h*h/(r*r)))
    if f > math.pi: vr = -vr
    vt = h/r
    cf, sf = math.cos(f), math.sin(f)
    x = r*(math.cos(om)*cf - math.sin(om)*sf); y = r*(math.sin(om)*cf + math.cos(om)*sf)
    vpx, vpy = vr*cf - vt*sf, vr*sf + vt*cf
    vx = vpx*math.cos(om) - vpy*math.sin(om); vy = vpx*math.sin(om) + vpy*math.cos(om)
    return x, y, vx, vy

def kepler_step(x, y, vx, vy, dt):
    ex, ey = ecc_vec(x,y,vx,vy); e = math.hypot(ex,ey)
    a = 1.0/(2.0/math.hypot(x,y)-(vx*vx+vy*vy)); n = a**-1.5
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
    p = a*(1-e*e); r1 = p/(1+e*math.cos(f1))
    v2 = 2.0/r1 - 1.0/a; hdot = math.sqrt(p)
    vr = math.sqrt(max(0.0, v2 - hdot*hdot/(r1*r1)))
    if f1 > math.pi: vr = -vr
    vt = hdot/r1; om = math.atan2(ey,ex)
    px, py = r1*math.cos(f1), r1*math.sin(f1)
    x1 = px*math.cos(om)-py*math.sin(om); y1 = px*math.sin(om)+py*math.cos(om)
    vpx, vpy = vr*math.cos(f1)-vt*math.sin(f1), vr*math.sin(f1)+vt*math.cos(f1)
    return x1, y1, vpx*math.cos(om)-vpy*math.sin(om), vpx*math.sin(om)+vpy*math.cos(om)

a, e, om = 0.0173, 1e-3, 0.4
P = a**1.5; dt = P/16
n_f1neg = n_bigerr = 0
worst = 0.0
N = 3600
for i in range(N):
    # uniform M0 via E0 uniform (e small)
    E0 = i*2*math.pi/N
    M0 = E0 - e*math.sin(E0)
    E0u = M0 + e*math.sin(M0)  # approx invert; good enough at e=1e-3
    # build state at E0u directly:
    f0 = 2*math.atan2(math.sqrt(1+e)*math.sin(E0u/2), math.sqrt(1-e)*math.cos(E0u/2))
    x0,y0,vx0,vy0 = state_from(a, e, om, f0 % (2*math.pi))
    x1,y1,vx1,vy1 = kepler_step(x0,y0,vx0,vy0,dt)
    # exact reference: advance M by n*dt, rebuild with the correct branch f in [0,2pi)
    M1 = (M0 + dt*a**-1.5) % (2*math.pi)
    E1 = M1 + e*math.sin(M1)
    for _ in range(50):
        E1 = E1 - (E1 - e*math.sin(E1) - M1)/(1 - e*math.cos(E1))
    f1 = 2*math.atan2(math.sqrt(1+e)*math.sin(E1/2), math.sqrt(1-e)*math.cos(E1/2)) % (2*math.pi)
    xr,yr,vxr,vyr = state_from(a, e, om, f1)
    err = math.hypot(x1-xr, y1-yr)/a + math.hypot(vx1-vxr, vy1-vyr)/(1/math.sqrt(a))
    if err > worst: worst = err; worst_at_M0 = M0
    if err > 1e-9: n_bigerr += 1
    if (i*2*math.pi/N) > math.pi: n_f1neg += 1  # rough: M0 in upper half -> M1 wraps neg
print(f"N={N}, e={e}: fraction M0>pi (wrap candidates)={n_f1neg/N:.2f}, bigerr(>1e-9) fraction={n_bigerr/N:.3f}, worst err={worst:.2e} at M0={worst_at_M0:.3f}")
