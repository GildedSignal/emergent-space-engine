"""Probe 2: energy error growth over 10^4 orbits at p=20, e=0.2 (kill: exponent > 0.2)."""
import math, time
from gv1 import s2_mass, s4_mass, ic_bound_periapsis, energy_mass, PI

def run_energy(p, e, eta, order, korbits, maxfact=80.0):
    x, y, wx, wy, E0, L0, sc = ic_bound_periapsis(p, e)
    T = 0.0
    phi = 0.0
    ph_prev = 0.0
    steps = 0
    pts = []
    k = 0                       # completed orbits (periapsis count - 1)
    maxerr = 0.0
    samples = []                # (orbit index, running max |dE/E0|)
    maxsteps = int(maxfact*korbits/eta) + 1000
    sqrt = math.sqrt
    atan2 = math.atan2
    twopi = 2.0*PI
    s2 = s2_mass
    s4 = s4_mass
    while k < korbits and steps < maxsteps:
        r = sqrt(x*x + y*y)
        dt = eta*r*sqrt(r)
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

if __name__ == "__main__":
    t0 = time.perf_counter()
    for (eta, order, K) in [(1/32, 2, 10000), (1/16, 2, 10000), (1/64, 4, 10000)]:
        t1 = time.perf_counter()
        k, maxerr, samples, steps = run_energy(20.0, 0.2, eta, order, K)
        s_all = fit_slope(samples, 10, 10**4)
        s_late = fit_slope(samples, 10**3, 10**4)
        # sample table
        marks = [10, 100, 1000, 5000, 10000]
        idx = {}
        for k_, m_ in samples:
            for mk in marks:
                if k_ - 10 < mk <= k_:
                    idx[mk] = m_
        tab = "  ".join(f"n={mk}:{idx.get(mk, float('nan')):.2e}" for mk in marks)
        print(f"eta={eta:.4f} order={order}: orbits={k} steps={steps} "
              f"max|dE/E|={maxerr:.3e}")
        print(f"   running max: {tab}")
        print(f"   growth exponent: {s_all:.3f} over [10,1e4] orbits, "
              f"{s_late:.3f} over [1e3,1e4]  (kill if > 0.2)")
        print(f"   [{time.perf_counter()-t1:.1f} s]")
    print(f"wall: {time.perf_counter()-t0:.1f} s")
