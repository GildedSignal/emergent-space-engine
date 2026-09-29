#!/usr/bin/env python3
"""E1 (decisive): does 'kicks, with averaging' survive mean-motion resonance?

Truth   : velocity-Verlet N-body (star + 2 planets, 2D), full forces.
Model B : the design's event layer, phase kept — exact Kepler cycles between
          conjunctions; each synodic encounter window is integrated densely
          (full forces, small dt). This is representation.md sec.2/sec.3:
          generators between events, integration only where no generator exists.
Model A : the design's costed layer ("tidal kicks, with averaging" sec.6, from
          H0190's first-order quadrupole averaging) — each perturber replaced by
          its orbit-averaged ring; planets ride exact Kepler cycles whose
          elements drift by the ring's secular per-cycle rates.

Case 1 (held out): period ratio exactly 2.0  -> deep inside 2:1 MMR.
Case 2 (control) : period ratio 2.15          -> no commensurability nearby.
"""
import math, sys

TWOPI = 2.0 * math.pi

def solve_kepler(M, e):
    E = M % TWOPI
    for _ in range(14):
        d = (E - e * math.sin(E) - M % TWOPI) / (1.0 - e * math.cos(E))
        E -= d
        if abs(d) < 1e-14:
            break
    return E

def state_from_elements(a, e, varpi, M):
    E = solve_kepler(M, e)
    r = a * (1.0 - e * math.cos(E))
    f = 2.0 * math.atan2(math.sqrt(1.0 + e) * math.sin(E / 2.0),
                         math.sqrt(1.0 - e) * math.cos(E / 2.0))
    p = a * (1.0 - e * e)
    vr = math.sqrt(1.0 / p) * e * math.sin(f)
    vt = math.sqrt(1.0 / p) * (1.0 + e * math.cos(f))
    lam = varpi + f
    cl, sl = math.cos(lam), math.sin(lam)
    return (r * cl, r * sl, vr * cl - vt * sl, vr * sl + vt * cl)

def elements_from_state(x, y, vx, vy):
    r = math.hypot(x, y)
    v2 = vx * vx + vy * vy
    a = -1.0 / (2.0 * (v2 / 2.0 - 1.0 / r))
    rv = x * vx + y * vy
    ex = (v2 - 1.0 / r) * x - rv * vx
    ey = (v2 - 1.0 / r) * y - rv * vy
    e = math.hypot(ex, ey)
    varpi = math.atan2(ey, ex)
    cosE = (1.0 - r / a) / e if e > 1e-12 else 1.0
    cosE = max(-1.0, min(1.0, cosE))
    Ea = math.acos(cosE)
    if rv < 0.0:
        Ea = TWOPI - Ea
    M = Ea - e * math.sin(Ea)
    return a, e, varpi, M

def accel_full(i, st, m):
    """heliocentric-full accel on planet i (indices 1,2; star index 0 fixed)."""
    x, y = st[i][0], st[i][1]
    ax = -x / (x * x + y * y) ** 1.5
    ay = -y / (x * x + y * y) ** 1.5
    for j in (1, 2):
        if j == i:
            continue
        xj, yj = st[j][0], st[j][1]
        dx, dy = xj - x, yj - y
        inv3 = (dx * dx + dy * dy) ** -1.5
        rj = math.hypot(xj, yj)
        ax += m[j] * (dx * inv3 - xj / rj ** 3)
        ay += m[j] * (dy * inv3 - yj / rj ** 3)
    return ax, ay

# ---------------- truth ----------------

def run_truth(m, st, t_end, dt, sample_every):
    st = [list(s) for s in st]
    E0 = 0.5 * m[0] * (st[0][2] ** 2 + st[0][3] ** 2) - sum(
        m[0] * m[j] / math.hypot(st[j][0], st[j][1]) for j in (1, 2))
    for j in (1, 2):
        E0 += 0.5 * m[j] * (st[j][2] ** 2 + st[j][3] ** 2)
    E0 -= m[1] * m[2] / math.hypot(st[2][0] - st[1][0], st[2][1] - st[1][1])
    ac = {i: accel_full(i, st, m) for i in (1, 2)}
    t = 0.0; nxt = 0.0; out = []
    while t < t_end:
        for i in (1, 2):
            st[i][2] += 0.5 * dt * ac[i][0]; st[i][3] += 0.5 * dt * ac[i][1]
            st[i][0] += dt * st[i][2]; st[i][1] += dt * st[i][3]
        ac = {i: accel_full(i, st, m) for i in (1, 2)}
        for i in (1, 2):
            st[i][2] += 0.5 * dt * ac[i][0]; st[i][3] += 0.5 * dt * ac[i][1]
        t += dt
        while t >= nxt - 1e-12 and t <= t_end:
            a1, e1, w1, _ = elements_from_state(*st[1])
            _, e2, w2, _ = elements_from_state(*st[2])
            lam1 = math.atan2(st[1][1], st[1][0]); lam2 = math.atan2(st[2][1], st[2][0])
            out.append((nxt, e1, e2, (2 * lam2 - lam1 - w1) % TWOPI))
            nxt += sample_every
    E = 0.5 * m[0] * (st[0][2] ** 2 + st[0][3] ** 2) - sum(
        m[0] * m[j] / math.hypot(st[j][0], st[j][1]) for j in (1, 2))
    for j in (1, 2):
        E += 0.5 * m[j] * (st[j][2] ** 2 + st[j][3] ** 2)
    E -= m[1] * m[2] / math.hypot(st[2][0] - st[1][0], st[2][1] - st[1][1])
    return out, abs(E - E0) / abs(E0)

# ---------------- model B: cycles + dense encounter windows ----------------

def run_modelB(m, a1, e1, w1, M1, a2, e2, w2, M2, t_end, nsub=800, sample_every=0.5):
    t = 0.0; nxt = 0.0; out = []; nev = 0
    while t < t_end:
        n1 = a1 ** -1.5; n2 = a2 ** -1.5
        Tsyn = TWOPI / abs(n2 - n1)
        # dense window centred on the conjunction at t (both start in conjunction)
        st = {1: list(state_from_elements(a1, e1, w1, M1)),
              2: list(state_from_elements(a2, e2, w2, M2))}
        h = Tsyn / nsub
        ac = {i: accel_full(i, st, m) for i in (1, 2)}
        for _ in range(nsub):
            for i in (1, 2):
                st[i][2] += 0.5 * h * ac[i][0]; st[i][3] += 0.5 * h * ac[i][1]
                st[i][0] += h * st[i][2]; st[i][1] += h * st[i][3]
            ac = {i: accel_full(i, st, m) for i in (1, 2)}
            for i in (1, 2):
                st[i][2] += 0.5 * h * ac[i][0]; st[i][3] += 0.5 * h * ac[i][1]
        nev += 1
        t_new = t + Tsyn
        while nxt <= t_new + 1e-12 and nxt <= t_end:
            tt = nxt
            s1 = state_from_elements(a1, e1, w1, M1 + n1 * (tt - t))
            s2 = state_from_elements(a2, e2, w2, M2 + n2 * (tt - t))
            lam1 = math.atan2(s1[1], s1[0]); lam2 = math.atan2(s2[1], s2[0])
            out.append((tt, e1, e2, (2 * lam2 - lam1 - w1) % TWOPI))
            nxt += sample_every
        # sample inside window too (post-kick values, from the new elements)
        a1, e1, w1, M1 = elements_from_state(*st[1])
        a2, e2, w2, M2 = elements_from_state(*st[2])
        t = t_new
        if e1 > 0.99 or e2 > 0.99 or a1 <= 0.05 or a2 <= 0.05:
            break
    return out, nev

# ---------------- model A: cycles + ring-averaged secular rates ----------------

def ring_points(a, e, w, K):
    pts = []
    for j in range(K):
        s = state_from_elements(a, e, w, TWOPI * j / K)
        pts.append((s[0], s[1]))
    return pts

def accel_ring(xi, yi, ring, mpt):
    ax = -xi / (xi * xi + yi * yi) ** 1.5
    ay = -yi / (xi * xi + yi * yi) ** 1.5
    for (xj, yj) in ring:
        dx, dy = xj - xi, yj - yi
        inv3 = (dx * dx + dy * dy) ** -1.5
        ax += mpt * dx * inv3
        ay += mpt * dy * inv3
    return ax, ay

def secular_cycle_rate(a, e, w, ring, mring_tot, K, nsub):
    """Element change over one full period under the static averaged ring.
    Each of the K ring points carries mring_tot/K."""
    s = list(state_from_elements(a, e, w, 0.0))
    n = a ** -1.5
    h = TWOPI / n / nsub
    mpt = mring_tot / K
    ax, ay = accel_ring(s[0], s[1], ring, mpt)
    for _ in range(nsub):
        s[2] += 0.5 * h * ax; s[3] += 0.5 * h * ay
        s[0] += h * s[2]; s[1] += h * s[3]
        ax, ay = accel_ring(s[0], s[1], ring, mpt)
        s[2] += 0.5 * h * ax; s[3] += 0.5 * h * ay
    a2, e2, w2, M2 = elements_from_state(*s)
    dw = (w2 - w + math.pi) % TWOPI - math.pi
    return (a2 - a, e2 - e, dw, TWOPI)

def run_modelA(m, a1, e1, w1, M1, a2, e2, w2, M2, t_end, K=16,
               refresh=10, nsub=240, sample_every=0.5):
    """Each planet rides its exact Kepler cycle; at each of its own period
    boundaries its elements step by the ring-averaged secular rates (refreshed
    from current elements every `refresh` cycles)."""
    el = {1: [a1, e1, w1, M1], 2: [a2, e2, w2, M2]}
    tnext = {1: TWOPI / a1 ** 1.5, 2: TWOPI / a2 ** 1.5}
    rate = {1: None, 2: None}; since = {1: refresh, 2: refresh}
    tepoch = {1: 0.0, 2: 0.0}
    t = 0.0; nxt = 0.0; out = []; ncyc = 0
    while True:
        i = 1 if tnext[1] <= tnext[2] else 2
        j = 2 if i == 1 else 1
        t = tnext[i]
        if t > t_end:
            break
        a_i, e_i, w_i, _ = el[i]; a_j, e_j, w_j, _ = el[j]
        if since[i] >= refresh:
            ring = ring_points(a_j, e_j, w_j, K)
            rate[i] = secular_cycle_rate(a_i, e_i, w_i, ring, m[j], K, nsub)
            since[i] = 0
        while nxt <= t + 1e-12 and nxt <= t_end:
            tt = nxt
            ss = {}
            for q in (1, 2):
                a_q, e_q, w_q, M_q = el[q]
                ss[q] = state_from_elements(a_q, e_q, w_q,
                                             M_q + a_q ** -1.5 * (tt - tepoch[q]))
            lam1 = math.atan2(ss[1][1], ss[1][0]); lam2 = math.atan2(ss[2][1], ss[2][0])
            out.append((tt, el[1][1], el[2][1], (2 * lam2 - lam1 - el[1][2]) % TWOPI))
            nxt += sample_every
        el[i][0] += rate[i][0]; el[i][1] += rate[i][1]; el[i][2] += rate[i][2]
        el[i][3] = 0.0
        tepoch[i] = t
        ncyc += 1; since[i] += 1
        tnext[i] = t + TWOPI / el[i][0] ** 1.5
        if el[i][1] > 0.99 or el[i][1] < 0 or el[i][0] <= 0.05:
            break
    return out, ncyc

def summarize(name, out):
    if not out:
        return f"  {name:12s} (no data)"
    es = [o[1] for o in out]
    ph = [o[3] for o in out]
    Rl = abs(sum(math.cos(p) + 1j * math.sin(p) for p in ph)) / len(ph)
    return (f"  {name:12s} e1: {min(es):.4f} -> {max(es):.4f} (gain {max(es)/es[0]:.2f}x), "
            f"phi concentration {Rl:.3f}")

def main():
    m_star = 1.0
    cases = [("2:1-resonant m=3e-3", 2.0, 3e-3, 2000),
             ("control-2.15 m=3e-3", 2.15, 3e-3, 2000),
             ("2:1-resonant m=1e-3", 2.0, 1e-3, 4000),
             ("control-2.55 m=1e-3", 2.55, 1e-3, 4000)]
    for label, ratio, mp, n_orbits in cases:
        m = [m_star, mp, mp]
        a1 = 1.0; a2 = ratio ** (2.0 / 3.0)
        e1_0 = e2_0 = 0.05
        w1_0, w2_0 = 0.5, 2.0
        t_end = n_orbits * TWOPI
        st0 = [(-0.0, -0.0, 0.0, 0.0)]
        for (a, e, w) in ((a1, e1_0, w1_0), (a2, e2_0, w2_0)):
            st0.append(state_from_elements(a, e, w, 0.0))
        outT, ed = run_truth(m, st0, t_end, TWOPI / 600.0, 0.5)
        outB, nevB = run_modelB(m, a1, e1_0, w1_0, 0.0, a2, e2_0, w2_0, 0.0, t_end)
        outA, ncycA = run_modelA(m, a1, e1_0, w1_0, 0.0, a2, e2_0, w2_0, 0.0, t_end)
        print(f"== {label} (ratio {ratio}, m={mp}, {n_orbits} orbits) ==")
        print(f"  truth energy drift {ed:.2e}")
        print(summarize("truth", outT))
        print(summarize("B phase-kept", outB) + f" [{nevB} encounters]")
        print(summarize("A averaged", outA) + f" [{ncycA} cycles]")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
