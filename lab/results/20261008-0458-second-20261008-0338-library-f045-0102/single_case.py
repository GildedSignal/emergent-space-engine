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
# --- their kepler_step verbatim ---
def kepler_step(x, y, vx, vy, dt):
    h = x*vy - y*vx
    ex, ey = ecc_vec(x, y, vx, vy)
    e = math.hypot(ex, ey)
    a = 1.0 / (2.0/math.hypot(x, y) - (vx*vx+vy*vy))
    if a <= 0: raise ValueError
    n = a ** -1.5
    cosf = (ex*x + ey*y) / (e * math.hypot(x, y)) if e > 1e-14 else x / math.hypot(x, y)
    cosf = max(-1.0, min(1.0, cosf))
    f0 = math.acos(cosf)
    if (x*vx + y*vy) < 0: f0 = 2*math.pi - f0
    E0 = 2*math.atan2(math.sqrt(1-e)*math.sin(f0/2), math.sqrt(1+e)*math.cos(f0/2))
    M0 = E0 - e*math.sin(E0)
    M1 = M0 + n*dt
    M1 = (M1 + math.pi) % (2*math.pi) - math.pi
    E = M1 if e < 0.8 else math.pi
    for _ in range(60):
        d = (E - e*math.sin(E) - M1) / (1 - e*math.cos(E)); E -= d
        if abs(d) < 1e-15: break
    f1 = 2*math.atan2(math.sqrt(1+e)*math.sin(E/2), math.sqrt(1-e)*math.cos(E/2))
    p = a*(1-e*e); r1 = p/(1+e*math.cos(f1))
    v2 = 2.0/r1 - 1.0/a; hdot = math.sqrt(p)
    vr = math.sqrt(max(0.0, v2 - hdot*hdot/(r1*r1)))
    if f1 > math.pi: vr = -vr
    vt = hdot/r1; om = math.atan2(ey, ex)
    px, py = r1*math.cos(f1), r1*math.sin(f1)
    x1 = px*math.cos(om) - py*math.sin(om); y1 = px*math.sin(om) + py*math.cos(om)
    vpx, vpy = vr*math.cos(f1) - vt*math.sin(f1), vr*math.sin(f1) + vt*math.cos(f1)
    vx1 = vpx*math.cos(om) - vpy*math.sin(om); vy1 = vpx*math.sin(om) + vpy*math.cos(om)
    return x1, y1, vx1, vy1

a, e, om = 0.0173, 1e-3, 0.4
P = a**1.5; dt = P/16
for M0 in (0.1, 2.0, 4.651):
    E0 = M0 + e*math.sin(M0)
    f0 = 2*math.atan2(math.sqrt(1+e)*math.sin(E0/2), math.sqrt(1-e)*math.cos(E0/2)) % (2*math.pi)
    S0 = state_from(a, e, om, f0)
    S1 = kepler_step(*S0, dt)
    M1 = M0 + dt*a**-1.5
    E1 = M1 + e*math.sin(M1)
    f1ref = 2*math.atan2(math.sqrt(1+e)*math.sin(E1/2), math.sqrt(1-e)*math.cos(E1/2)) % (2*math.pi)
    SR = state_from(a, e, om, f1ref)
    ex1, ey1 = ecc_vec(*S1); er1 = math.hypot(ex1, ey1); a1 = 1.0/(2.0/math.hypot(S1[0],S1[1]) - S1[2]**2 - S1[3]**2)
    print(f"M0={M0}: f0={f0:.4f} f1ref={f1ref:.4f}  pos_err={math.hypot(S1[0]-SR[0],S1[1]-SR[1]):.3e}  vel_err={math.hypot(S1[2]-SR[2],S1[3]-SR[3]):.3e}  e1={er1:.6e} a1={a1:.10f}")
    print(f"   S1=({S1[0]:.12f},{S1[1]:.12f},{S1[2]:.9f},{S1[3]:.9f})")
    print(f"   SR=({SR[0]:.12f},{SR[1]:.12f},{SR[2]:.9f},{SR[3]:.9f})")
