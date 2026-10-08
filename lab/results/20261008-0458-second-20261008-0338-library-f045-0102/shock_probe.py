# Shock-asymmetry probe: does batching kicks hurt more as an orbit nears its Hill edge?
# Toy of the plane's own structure: exact Kepler drift about the parent + tidal kicks
# from a circular secondary, sampled at cadence K per orbit, SAME total impulse budget.
# Observable: apsidal advance per orbit vs a fine-step RK4 truth in the full field.
import math

MU_S = 1.0e-3      # secondary mass (parent mass = 1)
R = 1.0            # secondary semimajor axis (circular)
R_HILL = R * (MU_S / 3.0) ** (1.0 / 3.0)
N_ORB = 300        # orbits per run

def accel(x, y, vx, vy):
    # parent at origin (free-fall with the secondary removed: heliocentric split, indirect term included)
    r3 = (x * x + y * y) ** 1.5
    ax, ay = -x / r3, -y / r3
    th = 1.3 * math.pi / 3  # secondary angle advanced by caller; placeholder replaced below
    return ax, ay

def sec_pos(t):
    th = t  # n_sec = 1
    return R * math.cos(th), R * math.sin(th)

def tide(x, y, t):
    # full attraction of the secondary + indirect term (heliocentric frame)
    sx, sy = sec_pos(t)
    dx, dy = sx - x, sy - y
    d3 = (dx * dx + dy * dy) ** 1.5
    s3 = R ** 3
    return MU_S * (dx / d3 - sx / s3), MU_S * (dy / d3 - sy / s3)

def accel_full(x, y, t):
    r3 = (x * x + y * y) ** 1.5
    tx, ty = tide(x, y, t)
    return -x / r3 + tx, -y / r3 + ty

def rk4_truth(x, y, vx, vy, T, n):
    h = T / n
    t = 0.0
    for _ in range(n):
        ax1, ay1 = accel_full(x, y, t)
        x2, y2, vx2, vy2 = x + vx*h/2, y + vy*h/2, vx + ax1*h/2, vy + ay1*h/2
        ax2, ay2 = accel_full(x2, y2, t + h/2)
        x3, y3, vx3, vy3 = x + vx2*h/2, y + vy2*h/2, vx + ax2*h/2, vy + ay2*h/2
        ax3, ay3 = accel_full(x3, y3, t + h/2)
        x4, y4, vx4, vy4 = x + vx3*h, y + vy3*h, vx + ax3*h, vy + ay3*h
        ax4, ay4 = accel_full(x4, y4, t + h)
        x += h*(vx + 2*vx2 + 2*vx3 + vx4)/6.0
        y += h*(vy + 2*vy2 + 2*vy3 + vy4)/6.0
        vx += h*(ax1 + 2*ax2 + 2*ax3 + ax4)/6.0
        vy += h*(ay1 + 2*ay2 + 2*ay3 + ay4)/6.0
        t += h
    return x, y, vx, vy

def ecc_vec(x, y, vx, vy):
    r = math.hypot(x, y); v2 = vx*vx + vy*vy
    rv = x*vx + y*vy
    ex = (v2 - 1.0/r)*x - rv*vx
    ey = (v2 - 1.0/r)*y - rv*vy
    return ex, ey

def kepler_step(x, y, vx, vy, dt):
    # exact 2D Kepler propagation: elements, advance M, rebuild state
    h = x*vy - y*vx
    ex, ey = ecc_vec(x, y, vx, vy)
    e = math.hypot(ex, ey)
    a = 1.0 / (2.0/math.hypot(x, y) - (vx*vx+vy*vy))
    # semi-major axis a; period
    if a <= 0: raise ValueError("unbound")
    n = a ** -1.5
    # true anomaly from e vector
    cosf = (ex*x + ey*y) / (e * math.hypot(x, y)) if e > 1e-14 else x / math.hypot(x, y)
    cosf = max(-1.0, min(1.0, cosf))
    f0 = math.acos(cosf)
    if (x*vx + y*vy) < 0: f0 = 2*math.pi - f0
    # eccentric anomaly
    def E_of_f(f):
        return 2*math.atan2(math.sqrt(1-e)*math.sin(f/2), math.sqrt(1+e)*math.cos(f/2))
    E0 = E_of_f(f0)
    M0 = E0 - e*math.sin(E0)
    M1 = M0 + n*dt
    M1 = (M1 + math.pi) % (2*math.pi) - math.pi
    # Newton for E1
    E = M1 if e < 0.8 else math.pi
    for _ in range(60):
        d = (E - e*math.sin(E) - M1) / (1 - e*math.cos(E))
        E -= d
        if abs(d) < 1e-15: break
    f1 = 2*math.atan2(math.sqrt(1+e)*math.sin(E/2), math.sqrt(1-e)*math.cos(E/2))
    p = a*(1-e*e)
    r1 = p/(1+e*math.cos(f1))
    w = math.sqrt(1.0/p)  # |v| at r=1 scale: v^2 = 2/r - 1/a; use vis-viva
    v2 = 2.0/r1 - 1.0/a
    v = math.sqrt(v2)
    hdot = math.sqrt(p)
    # radial/transverse components
    vr = math.sqrt(max(0.0, v2 - hdot*hdot/(r1*r1)))
    if f1 > math.pi: vr = -vr  # descending after apoapsis
    vt = hdot/r1
    # rotate by argument of periapsis
    om = math.atan2(ey, ex)
    px, py = r1*math.cos(f1), r1*math.sin(f1)
    x1 = px*math.cos(om) - py*math.sin(om)
    y1 = px*math.sin(om) + py*math.cos(om)
    vpx, vpy = vr*math.cos(f1) - vt*math.sin(f1), vr*math.sin(f1) + vt*math.cos(f1)
    vx1 = vpx*math.cos(om) - vpy*math.sin(om)
    vy1 = vpx*math.sin(om) + vpy*math.cos(om)
    return x1, y1, vx1, vy1

def kicked_run(a_moon, K, n_orb=N_ORB):
    # circular moon at periapsis-aligned start, kicks K times per moon orbit, same phase spacing
    x, y = a_moon, 0.0
    vx, vy = 0.0, 1.0/math.sqrt(a_moon)
    P = a_moon ** 1.5
    dt = P / K
    t = 0.0
    ex0, ey0 = ecc_vec(x, y, vx, vy)
    om0 = math.atan2(ey0, ex0)
    for _ in range(n_orb * K):
        x, y, vx, vy = kepler_step(x, y, vx, vy, dt)
        ax, ay = tide(x, y, t + dt)
        vx += ax*dt; vy += ay*dt
        t += dt
    ex1, ey1 = ecc_vec(x, y, vx, vy)
    om1 = math.atan2(ey1, ex1)
    dom = (om1 - om0) % (2*math.pi)
    return dom / n_orb

def truth_run(a_moon, n_orb=N_ORB):
    T = n_orb * a_moon ** 1.5
    x, y = a_moon, 0.0
    vx, vy = 0.0, 1.0/math.sqrt(a_moon)
    ex0, ey0 = ecc_vec(x, y, vx, vy)
    om0 = math.atan2(ey0, ex0)
    x, y, vx, vy = rk4_truth(x, y, vx, vy, T, n_orb * 4000)
    ex1, ey1 = ecc_vec(x, y, vx, vy)
    om1 = math.atan2(ey1, ex1)
    return ((om1 - om0) % (2*math.pi)) / n_orb

print(f"R_HILL = {R_HILL:.4f} AU; moon at tau_Hill radii; {N_ORB} orbits; floats (exploring)")
print("tau_Hill   domega_truth   A(1/4)    A(1/16)   [err(1 batch)/err(fine)]")
for tau in (0.05, 0.10, 0.17, 0.25, 0.35, 0.50):
    a = tau * R_HILL
    if a <= 1e-4: continue
    try:
        wt = truth_run(a)
        w1 = kicked_run(a, 1)
        w4 = kicked_run(a, 4)
        w16 = kicked_run(a, 16)
        e1, e4, e16 = abs(w1-wt), abs(w4-wt), abs(w16-wt)
        A4 = e1/e4 if e4 > 0 else float('inf')
        A16 = e1/e16 if e16 > 0 else float('inf')
        print(f"{tau:6.2f}  {wt:14.3e}  {A4:8.2f}  {A16:8.2f}   err1={e1:.2e} err4={e4:.2e} err16={e16:.2e}")
    except Exception as ex:
        print(f"{tau:6.2f}  failed: {ex}")
