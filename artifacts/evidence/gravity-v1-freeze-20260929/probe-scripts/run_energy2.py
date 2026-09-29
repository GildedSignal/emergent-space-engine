"""Probe 2 diagnostics: is the energy drift caused by the state-dependent step rule?
Control runs with a FIXED dt, and longer variable-step runs to test saturation."""
import math, time
from gv1 import s2_mass, s4_mass, ic_bound_periapsis, energy_mass, PI

def run_energy(p, e, eta, order, korbits, fixed_dt=None, maxfact=80.0):
    x, y, wx, wy, E0, L0, sc = ic_bound_periapsis(p, e)
    T = 0.0
    phi = 0.0
    ph_prev = 0.0
    steps = 0
    pts = []
    k = 0
    maxerr = 0.0
    samples = []
    maxsteps = int(maxfact*korbits/eta) + 1000
    sqrt = math.sqrt
    atan2 = math.atan2
    twopi = 2.0*PI
    s2 = s2_mass
    s4 = s4_mass
    while k < korbits and steps < maxsteps:
        r = sqrt(x*x + y*y)
        dt = fixed_dt if fixed_dt else eta*r*sqrt(r)
        if order == 2:
            x, y, wx, wy, ab = s2(x, y, wx, wy, dt)
        else:
            x, y, wx, wy, ab = s4(x, y, wx, wy, dt)
        if ab:
            break
        T += dt
        steps += 1
        ph = atan2(y, x)
        d = ph - ph_prev
        if d > PI:
            d -= twopi
        elif d < -PI:
            d += twopi
        phi += d
        ph_prev = ph
        p3 = (T, sqrt(x*x + y*y), phi)
        if len(pts) >= 2:
            (ta, ra, fa), (tb, rb, fb) = pts[-2], pts[-1]
            tc, rc, fc = p3
            if ra > rb and rb <= rc:
                d1 = (rb - ra)/(tb - ta)
                d2 = (rc - rb)/(tc - tb)
                cc = (d2 - d1)/(tc - ta)
                if cc > 0.0:
                    k += 1
                    err = abs(energy_mass(x, y, wx, wy) - E0)/E0
                    if err > maxerr:
                        maxerr = err
                    if k % 10 == 0:
                        samples.append((k, maxerr))
                pts = [p3]
            else:
                pts.append(p3)
                if len(pts) > 3:
                    pts = pts[-3:]
        else:
            pts.append(p3)
    return k, maxerr, samples, steps

def fit_slope(samples, kmin, kmax):
    xs, ys = [], []
    for k, m in samples:
        if kmin <= k <= kmax and m > 0.0:
            xs.append(math.log(k))
            ys.append(math.log(m))
    n = len(xs)
    mx = sum(xs)/n
    my = sum(ys)/n
    return sum((a-mx)*(b-my) for a, b in zip(xs, ys))/sum((a-mx)**2 for a in xs)

def show(tag, k, maxerr, samples):
    marks = [10, 100, 1000, 5000, 10000, 20000, 30000]
    idx = {}
    for k_, m_ in samples:
        for mk in marks:
            if k_ - 10 < mk <= k_:
                idx[mk] = m_
    tab = "  ".join((f"n={mk}:{idx.get(mk, float('nan')):.2e}")
                    for mk in marks if mk <= k)
    print(f"{tag}: orbits={k} max|dE/E|={maxerr:.3e}")
    print(f"   {tab}")
    print(f"   exponent [1e3,{k}] = {fit_slope(samples, 1000, k):.3f}")

if __name__ == "__main__":
    t0 = time.perf_counter()
    p, e = 20.0, 0.2
    rp, ra = p/(1+e), p/(1-e)
    rref = math.sqrt(rp*ra)
    # control 1: fixed dt (same orbit count), isolates the variable-step effect
    for (eta, order, K) in [(1/32, 2, 10000), (1/64, 4, 10000)]:
        t1 = time.perf_counter()
        dt_fix = eta*rref*math.sqrt(rref)
        k, me, smp, st = run_energy(p, e, eta, order, K, fixed_dt=dt_fix)
        show(f"FIXED dt (={eta:.4f}*rref^1.5) order={order}", k, me, smp)
        print(f"   [{time.perf_counter()-t1:.1f} s]")
    # control 2: variable step, longer, does it saturate?
    for (eta, order, K) in [(1/32, 2, 30000), (1/16, 4, 10000)]:
        t1 = time.perf_counter()
        k, me, smp, st = run_energy(p, e, eta, order, K)
        show(f"VAR dt eta={eta:.4f} order={order}", k, me, smp)
        print(f"   [{time.perf_counter()-t1:.1f} s]")
    print(f"wall: {time.perf_counter()-t0:.1f} s")
