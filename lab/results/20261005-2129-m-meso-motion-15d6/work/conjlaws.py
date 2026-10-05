"""Conjunction-event law: the encounter as ONE exact event.

Representation under test (this run's candidate C1):
  the interaction leg of the split (ship x planet, while inside the encounter
  window) is the two-body Hamiltonian of the pair; its flow is the exact
  Kepler map.  One event = advance both bodies heliocentrically by 2w,
  advance the relative state by the pair's two-body flow over 2w, attribute
  the difference.  No substeps, no quadrature, no rebind of a compiled shape
  beyond the elements of the new orbit.

Floats explore here (lab rule); the closed forms are the claim, and the
production form is integer (fixed-schedule Newton + Paeth rotations).

Units: G = 1, AU, yr.  2D complex positions/velocities.
"""
import numpy as np

TWOPI = 2.0 * np.pi
KMS = 1.0 / 4.74057          # 1 AU/yr = 4.74057 km/s


# ---------------------------------------------------------------- elements
def elements(r, v, mu):
    """h, e, ev, a, energy from a 2D state (r, v complex, mu = G(m1+m2))."""
    h = (r.conj() * v).imag                    # signed specific ang. momentum
    R = np.abs(r)
    V2 = (v * v.conj()).real
    rdotv = (r.conj() * v).real
    ev = ((V2 - mu / R) * r - rdotv * v) / mu  # eccentricity vector
    e = np.abs(ev)
    energy = V2 / 2.0 - mu / R
    a = -mu / (2.0 * energy)
    return h, e, ev, a, energy


def _E_from_f(f, e):
    c = np.clip((1.0 - e) / (1.0 + e), 0.0, None)
    return 2.0 * np.arctan2(np.sqrt(c) * np.sin(f / 2.0),
                            np.cos(f / 2.0))

def _f_from_E_hyp(H, e):
    c = (e + 1.0) / (e - 1.0)
    return 2.0 * np.arctan2(np.sqrt(c) * np.sinh(H / 2.0),
                            np.cosh(H / 2.0))


def _state_from_f(f, p, e, h, varpi, mu):
    R = p / (1.0 + e * np.cos(f))
    ur = np.exp(1j * (varpi + f))
    sgn = np.sign(h)
    vr = (mu / h) * e * np.sin(f)
    vt = (mu / h) * (1.0 + e * np.cos(f))
    return R * ur, vr * ur + vt * (1j * ur * sgn)


def propagate(r, v, mu, dt):
    """Exact 2D two-body propagation over dt (ellipse or hyperbola).
    Vectorized over leading axes of r, v.  Parabolic states are nudged.
    Retrograde states are mirrored to prograde internally and mirrored back.
    """
    r = np.asarray(r, dtype=complex)
    v = np.asarray(v, dtype=complex)
    h0, e, ev, a, _ = elements(r, v, mu)
    retro = h0 < 0
    r = np.where(retro, r.conj(), r)
    v = np.where(retro, v.conj(), v)
    ev = np.where(retro, ev.conj(), ev)
    h = np.abs(h0)
    e = np.maximum(e, 1e-12)
    ev = np.where(e < 1e-10, 1.0 + 0j, ev / np.abs(ev) * e)
    varpi = np.angle(ev)
    R = np.abs(r)
    rdotv = (r.conj() * v).real
    f0 = np.angle(r * np.conj(ev))
    ellip = a > 0
    # --- anomaly now
    E0 = _E_from_f(f0, e)
    M0 = E0 - e * np.sin(E0)
    Hh0 = np.arccosh(np.clip((1.0 - R / a) / e, 1.0, None))
    Hh0 = np.where(rdotv < 0, -Hh0, Hh0)
    Mh0 = e * np.sinh(Hh0) - Hh0
    # --- advance the anomaly
    n = np.sqrt(mu / np.abs(a) ** 3)
    M1 = M0 + n * dt
    Mh1 = Mh0 + n * dt
    # --- solve Kepler: Newton from two starters (mean + Barker cube root),
    #     pick by residual (near-parabolic paths defeat a single starter)
    def _ell_newton(E):
        for _ in range(12):
            E = E - (E - e * np.sin(E) - M1) / (1.0 - e * np.cos(E))
        return E
    def _hyp_newton(H):
        for _ in range(12):
            H = np.clip(H - (e * np.sinh(H) - H - Mh1) / (e * np.cosh(H) - 1.0), -30.0, 30.0)
        return H
    bark = np.cbrt(6.0 * np.maximum(np.abs(M1), 1e-300)) * np.sign(M1)
    Ea = _ell_newton(np.where(ellip, M1 + e * np.sin(M1), 0.0))
    Eb = _ell_newton(np.where(ellip, bark, 0.0))
    resa = np.abs(Ea - e * np.sin(Ea) - M1)
    resb = np.abs(Eb - e * np.sin(Eb) - M1)
    E = np.where(resa <= resb, Ea, Eb)
    barkh = np.cbrt(6.0 * np.maximum(np.abs(Mh1), 1e-300)) * np.sign(Mh1)
    Ha = _hyp_newton(np.where(ellip, 0.0, np.arcsinh(Mh1 / e)))
    Hb = _hyp_newton(np.where(ellip, 0.0, barkh))
    rha = np.abs(e * np.sinh(Ha) - Ha - Mh1)
    rhb = np.abs(e * np.sinh(Hb) - Hb - Mh1)
    Hh = np.where(rha <= rhb, Ha, Hb)
    f_ell = 2.0 * np.arctan2(np.sqrt(np.clip(1.0 + e, 0.0, None)) * np.sin(E / 2.0),
                             np.sqrt(np.clip(1.0 - e, 0.0, None)) * np.cos(E / 2.0))
    f_hyp = _f_from_E_hyp(Hh, e)
    f = np.where(ellip, f_ell, f_hyp)
    p = h * h / mu
    r1, v1 = _state_from_f(f, p, e, h, varpi, mu)
    r1 = np.where(retro, r1.conj(), r1)
    v1 = np.where(retro, v1.conj(), v1)
    return r1, v1


# ------------------------------------------------------------- the event
def encounter_event(r_b, v_b, r_p, v_p, mu_p, mu_sun, w, planet_arc=None, use_pair_flow=False):
    """One exact event over a window of half-width w (Strang composition).

    drift(w) [Sun] -> pair-flow(2w) [exact two-body about the planet,
    in the planet's frame] -> drift(w) [Sun].  Second order in the split;
    the pair leg is the closed-form Kepler map.  planet_arc(t_rel) must
    return the planet's unperturbed heliocentric state w + 2w later; if
    None, the planet is treated as fixed on its given (circular) state.
    """
    # drift half (Sun)
    r1, v1 = drift_flow(r_b, v_b, mu_sun, w)
    if planet_arc is not None:
        rp1, vp1 = planet_arc(w)
    else:
        rp1, vp1 = propagate(r_p, v_p, mu_sun, w)
    # interaction leg: the pair's two-body flow over the full window
    if use_pair_flow:
        d2, V2 = pair_flow(r1 - rp1, v1 - vp1, mu_p, 2.0 * w)
    else:
        d2, V2 = propagate(r1 - rp1, v1 - vp1, mu_p, 2.0 * w)
    # the planet does not advance under the pair operator (its frame's origin)
    r2, v2 = rp1 + d2, vp1 + V2
    # drift half (Sun)
    return drift_flow(r2, v2, mu_sun, w)


def impulse_event(r_b, v_b, r_p, v_p, mu_p):
    """Negative control: straight-line impulse (Laplace-style), |dv| = 2 mu/(U b)."""
    d = r_b - r_p
    V = v_b - v_p
    U = np.abs(V)
    bvec = d - (d.conj() * V).real * V / (U * U)
    b = np.abs(bvec)
    bhat = bvec / np.maximum(b, 1e-300)
    dv = -2.0 * mu_p / (U * np.maximum(b, 1e-300)) * bhat
    return r_b, v_b + dv


# ------------------------------------------------------- conjunction finding
def body_state_at_M(r0, v0, mu, t, t0):
    return propagate(r0, v0, mu, t - t0)


def closest_approach(r_b, v_b, r_p0, v_p0, mu_sun, t_star, w_syn, iters=40):
    """Refine the closest-approach time near t_star by ternary search on |d|."""
    lo, hi = t_star - 0.25 * w_syn, t_star + 0.25 * w_syn

    def dist(t):
        rb, _ = propagate(r_b, v_b, mu_sun, t)
        rp, _ = propagate(r_p0, v_p0, mu_sun, t)
        return np.abs(rb - rp)

    for _ in range(iters):
        m1 = lo + (hi - lo) / 3.0
        m2 = hi - (hi - lo) / 3.0
        if dist(m1) < dist(m2):
            hi = m2
        else:
            lo = m1
    t = 0.5 * (lo + hi)
    rb, vb = propagate(r_b, v_b, mu_sun, t)
    rp, vp = propagate(r_p0, v_p0, mu_sun, t)
    return t, rb, vb, rp, vp


def helio_energy_L(r, v, mu):
    V2 = (v * v.conj()).real
    E = V2 / 2.0 - mu / np.abs(r)
    L = (r.conj() * v).imag
    return E, L


def jacobi_circular(r, v, mu_p, n_p, rp0):
    """Jacobi constant of the circular restricted problem (any a_p units)."""
    # rotating-frame speed: v_rot = v - n x r ; n along z
    vrot = v - 1j * n_p * r
    r1 = np.abs(r)                       # distance to Sun (Sun at origin)
    r2 = np.abs(r - rp0)                 # distance to planet
    return (n_p * np.abs(r)) ** 2 + 2.0 / r1 + 2.0 * mu_p / r2 - (vrot * vrot.conj()).real


def tail_moments_circ(r_b, v_b, t0, t1, mu_p, mu_sun, a_p, n_p, t_eval, n=97):
    """First-order state correction at t_eval from the planet's force along
    the Sun-only drift arc [t0, t1] (Simpson):  dv = int a dt',
    dr = int (t_eval - t') a dt'."""
    ts = np.linspace(t0, t1, n)
    ws = np.ones(n)
    ws[1:-1:2] = 4.0
    ws[2:-1:2] = 2.0
    rb, _ = propagate(np.asarray(r_b, dtype=complex), np.asarray(v_b, dtype=complex),
                      mu_sun, ts - t0)
    rp = a_p * np.exp(1j * n_p * ts)
    d = rb - rp
    acc = -mu_p * d / np.abs(d) ** 3
    h = (t1 - t0) / (n - 1)
    dv = (ws * acc).sum(axis=0) * h / 3.0
    dr = (ws * (t_eval - ts) * acc).sum(axis=0) * h / 3.0
    return dr, dv


def pair_flow(d0, V0, mu_p, dt, sub=256):
    """The interaction leg: closed-form Kepler when well conditioned,
    fixed-count symplectic substeps when degenerate (near-straight or
    near-parabolic relative states).  Returns (d, V) after dt."""
    d1, V1 = propagate(d0, V0, mu_p, dt)
    ok = np.all(np.isfinite(d1)) and np.all(np.isfinite(V1))
    if ok:
        h, e, ev, a, _ = elements(d0, V0, mu_p)
        R0 = np.abs(d0)
        ok = (np.abs(np.abs(d1) - R0) < 5.0 * R0 + 10.0 * np.abs(V0) * abs(dt)) \
             and np.abs(d1) > 1e-9 * max(R0, 1e-9)
    if ok:
        return d1, V1
    # leapfrog fallback
    d = np.asarray(d0, dtype=complex).copy()
    V = np.asarray(V0, dtype=complex).copy()
    hstep = dt / sub
    def acc(dd):
        return -mu_p * dd / np.abs(dd) ** 3
    a0 = acc(d)
    for _ in range(sub):
        d = d + V * hstep + 0.5 * a0 * hstep * hstep
        a1 = acc(d)
        V = V + 0.5 * (a0 + a1) * hstep
        a0 = a1
    return d, V


def drift_flow(r, v, mu, dt, sub=256):
    """Sun/drift leg: closed-form Kepler when well conditioned, fixed-count
    leapfrog otherwise (near-parabolic corners defeat the element route)."""
    r1, v1 = propagate(r, v, mu, dt)
    R0 = np.abs(r)
    ok = np.all(np.isfinite(r1)) and np.all(np.isfinite(v1)) \
        and np.all(np.abs(r1) < 10.0 * (R0 + np.abs(v) * abs(dt)) + 10.0) \
        and np.all(np.abs(r1) > 1e-12 * max(R0, 1e-12))
    if ok:
        return r1, v1
    d = np.asarray(r, dtype=complex).copy()
    V = np.asarray(v, dtype=complex).copy()
    hstep = dt / sub
    def acc(dd):
        return -mu * dd / np.abs(dd) ** 3
    a0 = acc(d)
    for _ in range(sub):
        d = d + V * hstep + 0.5 * a0 * hstep * hstep
        a1 = acc(d)
        V = V + 0.5 * (a0 + a1) * hstep
        a0 = a1
    return d, V
