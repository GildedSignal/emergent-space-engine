"""Design of the figure-eight transfer: 50 identical resonant encounters of a ship with
the moving planet, every 3 yr, inside/outside alternation (T_i = 3/4 yr = 4 orbits per
cycle in, T_o = 3/2 yr = 2 orbits out), so the doll chain closes EXACTLY (patched conics
are periodic) and the 100 SOI crossings are well defined.

Shooting unknowns: the inertial directions of v_inf_in / v_inf_out (theta_in, theta_out).
Conditions: the outgoing leg ellipse has period exactly 3/4 yr (encounter k leaves inward
for odd... E0 in=outer/out=inner per parity) and the incoming leg period exactly 3/2 yr.
Units AU, yr, Msun, G=4pi^2. Writes design.json.
"""
import json
import math

G = 4.0*math.pi**2
MSTAR, MPL = 1.0, 3.0e-6
AP, WP = 1.0, 2.0*math.pi
RP = 6371.0/1.495978707e8
SOI = AP*(MPL/MSTAR)**0.4
MU_P = G*MPL
U = 6.0/(1.495978707e8/3.15576e7)      # 6 km/s in AU/yr


def planet_state(t):
    c, s = math.cos(WP*t), math.sin(WP*t)
    return (AP*c, AP*s), (-AP*WP*s, AP*WP*c)


def stumpc(z):
    if z > 1e-8:
        return (1.0-math.cos(math.sqrt(z)))/z
    if z < -1e-8:
        return (math.cosh(math.sqrt(-z))-1.0)/(-z)
    return 0.5 - z/24.0 + z*z/720.0


def stumps(z):
    if z > 1e-8:
        s = math.sqrt(z)
        return (s-math.sin(s))/s**3
    if z < -1e-8:
        s = math.sqrt(-z)
        return (math.sinh(s)-s)/s**3
    return 1.0/6.0 - z/120.0 + z*z/5040.0


def kepler_prop(mu, s0, dt):
    x, y, vx, vy = s0
    r0 = math.hypot(x, y)
    v2 = vx*vx+vy*vy
    rv = x*vx+y*vy
    alpha = 2.0/r0 - v2/mu
    sq = math.sqrt(mu)
    chi = sq*dt*alpha if alpha > 1e-12 else sq*dt/r0
    for _ in range(200):
        z = alpha*chi*chi
        C, S = stumpc(z), stumps(z)
        F = (r0*rv/sq)*chi*chi*C + (1.0-alpha*r0)*chi**3*S + r0*chi - sq*dt
        dF = (r0*rv/sq)*chi*(1.0-z*S) + (1.0-alpha*r0)*chi*chi*C + r0
        d = F/dF
        chi -= d
        if abs(d) < 1e-14*abs(chi)+1e-16:
            break
    z = alpha*chi*chi
    C, S = stumpc(z), stumps(z)
    f = 1.0 - chi*chi*C/r0
    g = dt - chi**3*S/sq
    xn, yn = f*x+g*vx, f*y+g*vy
    rn = math.hypot(xn, yn)
    fd = sq/(rn*r0)*(z*chi*S - chi)
    gd = 1.0 - chi*chi*C/rn
    return (xn, yn, fd*x+gd*vx, fd*y+gd*vy)


def hyp_pericenter_state(theta_in, theta_out):
    """Planet-frame pericenter state (pos, vel) of the flyby with v_inf directions."""
    ni = (math.cos(theta_in), math.sin(theta_in))
    no = (math.cos(theta_out), math.sin(theta_out))
    cross = ni[0]*no[1]-ni[1]*no[0]
    dot = ni[0]*no[0]+ni[1]*no[1]
    delta = math.atan2(cross, dot)                     # signed turn, |delta|<pi
    e = 1.0/math.sin(abs(delta)/2.0)
    rp = (e-1.0)*MU_P/(U*U)
    nrm = math.hypot(ni[0]+no[0], ni[1]+no[1])
    px, py = (ni[0]+no[0])/nrm, (ni[1]+no[1])/nrm      # pericenter bisector
    sgn = 1.0 if delta > 0 else -1.0
    vpx, vpy = -sgn*py, sgn*px                          # pericenter velocity dir
    vp = math.sqrt(U*U + 2.0*MU_P/rp)
    return (rp*px, rp*py, vp*vpx, vp*vpy), rp, e, delta


def cross_time(s0, sign, mu=MU_P):
    """Time (planet frame, signed) from pericentre (|xi|<SOI) until |xi|=SOI outward."""
    lo = 0.0
    dt = 1e-7
    hi = None
    t = dt
    for _ in range(400):
        s2 = kepler_prop(mu, s0, t)
        if math.hypot(s2[0], s2[1]) >= SOI:
            hi = t
            break
        lo = t
        dt *= 1.5
        t += dt
    if hi is None:
        raise RuntimeError("no SOI crossing found")
    for _ in range(90):
        mid = 0.5*(lo+hi)
        sm = kepler_prop(mu, s0, mid)
        if math.hypot(sm[0], sm[1]) < SOI:
            lo = mid
        else:
            hi = mid
    mag = 0.5*(lo+hi)
    return sign*mag, kepler_prop(mu, s0, sign*mag)

def leg_period(helio_state):
    x, y, vx, vy = helio_state
    r = math.hypot(x, y)
    v2 = vx*vx+vy*vy
    a = 1.0/(2.0/r - v2/G)
    if a <= 0.0:
        return 1e3, a            # hyperbolic heliocentric leg: steer Newton back
    return a**1.5, a


def helio(t, xi_state):
    (pp, pv) = planet_state(t)
    x, y, vx, vy = xi_state
    return (pp[0]+x, pp[1]+y, pv[0]+vx, pv[1]+vy)


def residuals(th_in, th_out):
    peri, rp, e, delta = hyp_pericenter_state(th_in, th_out)
    t_in, s_in = cross_time(peri, -1.0)
    t_out, s_out = cross_time(peri, +1.0)
    Tin, ain = leg_period(helio(t_in, s_in))
    Tout, aout = leg_period(helio(t_out, s_out))
    # E0: incoming leg must be the outer 3/2, outgoing the inner 3/4.
    return (Tin-1.5, Tout-0.75), (t_in, t_out, rp, e, delta, ain, aout)


def solve():
    # start from the idealized cone angles measured from Vp
    vi = 2.0*math.pi*math.sqrt(2.0-1.0/0.75**(2.0/3.0))
    vo = 2.0*math.pi*math.sqrt(2.0-1.0/1.5**(2.0/3.0))
    Vp = 2.0*math.pi
    cai = (vi*vi-Vp*Vp-U*U)/(2.0*Vp*U)
    cao = (vo*vo-Vp*Vp-U*U)/(2.0*Vp*U)
    ai, ao = math.acos(cai), math.acos(cao)
    # n_in at +ai from yhat (s=+1): angle = pi/2 - ai ; same-side n_out
    th_in = 0.5*math.pi - ai
    th_out = 0.5*math.pi - ao
    for it in range(60):
        (r1, r2), info = residuals(th_in, th_out)
        if abs(r1) < 1e-13 and abs(r2) < 1e-13:
            break
        h = 1e-7
        (d1, _), _ = residuals(th_in+h, th_out)
        (_, d2), _ = residuals(th_in, th_out+h)
        j11 = (d1-r1)/h
        j22 = (d2-r2)/h
        j12 = ((residuals(th_in, th_out+h)[0][0])-r1)/h
        j21 = ((residuals(th_in+h, th_out)[0][1])-r2)/h
        det = j11*j22-j12*j21
        d1 = (r1*j22-r2*j12)/det
        d2 = (r2*j11-r1*j21)/det
        m = max(abs(d1), abs(d2))
        if m > 0.02:
            d1 *= 0.02/m; d2 *= 0.02/m
        th_in -= d1
        th_out -= d2
    (r1, r2), (t_in, t_out, rp, e, delta, ain, aout) = residuals(th_in, th_out)
    peri, _, _, _ = hyp_pericenter_state(th_in, th_out)
    design = dict(U=U, theta_in=th_in, theta_out=th_out, t_in=t_in, t_out=t_out,
                  rp=rp, e=e, delta=delta, a_in=ain, a_out=aout,
                  r_in=1.5, r_out=0.75, res_in=r1, res_out=r2,
                  SOI=SOI, MU_P=MU_P, RP=RP, G=G,
                  peri=list(peri), iters=it)
    with open("design.json", "w") as f:
        json.dump(design, f, indent=1)
    print(json.dumps(design, indent=1))
    print("rp/R_P =", rp/RP, " delta(deg) =", math.degrees(delta))


if __name__ == "__main__":
    solve()
