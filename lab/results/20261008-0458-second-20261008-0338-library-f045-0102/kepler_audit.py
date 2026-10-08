# Audit the author's kepler_step: is the (x,y,vx,vy) roundtrip exact for all phases?
# Take a fixed orbit (a, e, om), start at many mean anomalies, step by dt = P/K,
# then step BACK by -dt... can't (code not symmetric). Instead: step forward dt,
# recompute elements; a, e, om must be invariant. Flag any drift in a/e/om.
import math, importlib.util
spec = importlib.util.spec_from_file_location("sp", "shock_probe.py")
# can't import: shock_probe prints on import. Re-implement its functions verbatim.
def ecc_vec(x, y, vx, vy):
    r = math.hypot(x, y); v2 = vx*vx + vy*vy
    rv = x*vx + y*vy
    ex = (v2 - 1.0/r)*x - rv*vx
    ey = (v2 - 1.0/r)*y - rv*vy
    return ex, ey

def kepler_step(x, y, vx, vy, dt):
    h = x*vy - y*vx
    ex, ey = ecc_vec(x, y, vx, vy)
    e = math.hypot(ex, ey)
    a = 1.0 / (2.0/math.hypot(x, y) - (vx*vx+vy*vy))
    if a <= 0: raise ValueError("unbound")
    n = a ** -1.5
    cosf = (ex*x + ey*y) / (e * math.hypot(x, y)) if e > 1e-14 else x / math.hypot(x, y)
    cosf = max(-1.0, min(1.0, cosf))
    f0 = math.acos(cosf)
    if (x*vx + y*vy) < 0: f0 = 2*math.pi - f0
    def E_of_f(f):
        return 2*math.atan2(math.sqrt(1-e)*math.sin(f/2), math.sqrt(1+e)*math.cos(f/2))
    E0 = E_of_f(f0)
    M0 = E0 - e*math.sin(E0)
    M1 = M0 + n*dt
    M1 = (M1 + math.pi) % (2*math.pi) - math.pi
    E = M1 if e < 0.8 else math.pi
    for _ in range(60):
        d = (E - e*math.sin(E) - M1) / (1 - e*math.cos(E))
        E -= d
        if abs(d) < 1e-15: break
    f1 = 2*math.atan2(math.sqrt(1+e)*math.sin(E/2), math.sqrt(1-e)*math.cos(E/2))
    p = a*(1-e*e)
    r1 = p/(1+e*math.cos(f1))
    v2 = 2.0/r1 - 1.0/a
    v = math.sqrt(v2)
    hdot = math.sqrt(p)
    vr = math.sqrt(max(0.0, v2 - hdot*hdot/(r1*r1)))
    if f1 > math.pi: vr = -vr
    vt = hdot/r1
    om = math.atan2(ey, ex)
    px, py = r1*math.cos(f1), r1*math.sin(f1)
    x1 = px*math.cos(om) - py*math.sin(om)
    y1 = px*math.sin(om) + py*math.cos(om)
    vpx, vpy = vr*math.cos(f1) - vt*math.sin(f1), vr*math.sin(f1) + vt*math.cos(f1)
    vx1 = vpx*math.cos(om) - vpy*math.sin(om)
    vy1 = vpx*math.sin(om) + vpy*math.cos(om)
    return x1, y1, vx1, vy1

def wrap(a): return (a + math.pi) % (2*math.pi) - math.pi

for e_test in (1e-6, 1e-4, 1e-3, 1e-2, 0.05):
    a_test = 0.0173  # tau=0.25 orbit
    worst_a = worst_e = worst_om = 0.0
    nbad = 0
    for i in range(360):
        f = i * 2*math.pi/360
        r = a_test*(1-e_test**2)/(1+e_test*math.cos(f))
        v = math.sqrt(2/r - 1/a_test)
        hz = math.sqrt(a_test*(1-e_test**2))
        vr = math.sqrt(max(0.0, v*v - hz*hz/(r*r)))
        if f > math.pi: vr = -vr
        vt = hz/r
        # om = 0.4 rad fixed
        om = 0.4
        cf, sf = math.cos(f), math.sin(f)
        x = r*(math.cos(om)*cf - math.sin(om)*sf)
        y = r*(math.sin(om)*cf + math.cos(om)*sf)
        vpx, vpy = vr*cf - vt*sf, vr*sf + vt*cf
        vx = vpx*math.cos(om) - vpy*math.sin(om)
        vy = vpx*math.sin(om) + vpy*math.cos(om)
        P = a_test**1.5
        for K in (16, 1):
            x1,y1,vx1,vy1 = kepler_step(x,y,vx,vy, P/K)
            ex1,ey1 = ecc_vec(x1,y1,vx1,vy1)
            e1 = math.hypot(ex1,ey1); a1 = 1.0/(2.0/math.hypot(x1,y1) - (vx1*vx1+vy1*vy1))
            om1 = math.atan2(ey1,ex1)
            da = abs(a1-a_test)/a_test; de = abs(e1-e_test)
            dom = abs(wrap(om1-om))
            if dom > 3: nbad += 1  # pi-flip class
            worst_a = max(worst_a, da); worst_e = max(worst_e, de); worst_om = max(worst_om, dom)
    print(f"e={e_test:8.1e}  worst |da|/a={worst_a:9.2e}  worst |de|={worst_e:9.2e}  worst |dom|={worst_om:9.2e}  om-pi-flips={nbad}")
