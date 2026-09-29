"""Port of xtask/src/gr_oracle_extended.rs (1PN two-body oracle), G=M=c=1 (M = m1+m2).

eih_invariants(p,e,nu) -> (rp, vt, energy, angular): 1PN harmonic-CM invariants of the
orbit whose 1PN harmonic radial turning radii are exactly p/(1+e), p/(1-e).
damour_deruelle(E,J,nu) -> (periastron advance, radial period): DD 1PN quasi-Keplerian.
schwarzschild_from_invariants(x, L, p_guess) -> (p, e): exact Schwarzschild Darwin
elements of the geodesic with binding x=E-1 and angular momentum L (verbatim port).
bound_period_quad(p,e) -> (t, tau): exact Schwarzschild coordinate/proper radial period.
"""
import numpy as np

def eih_invariants(p, e, nu):
    rp = p / (1.0 + e)
    ra = p / (1.0 - e)
    j0 = np.sqrt(p)
    corr = lambda r: (-(1.0 - 3.0*nu)*j0**4/(8.0*r**4)
                      - (3.0 + nu)*j0*j0/(2.0*r**3)
                      + 1.0/(2.0*r*r))
    den = j0*(1.0/(rp*rp) - 1.0/(ra*ra))
    if abs(den) < 1e-300:  # e -> 0 limit (Rust original would be 0/0 here)
        dcorr = lambda r: (1.0 - 3.0*nu)*j0**4/(2.0*r**5) + 1.5*(3.0 + nu)*j0*j0/r**4 - 1.0/r**3
        dj = dcorr(rp)*rp**3/(2.0*j0)
    else:
        dj = -(corr(rp) - corr(ra)) / den
    vt = (j0 + dj)/rp * (1.0 - 0.5*(1.0 - 3.0*nu)*j0*j0/(rp*rp) - (3.0 + nu)/rp)
    v2 = vt*vt
    energy = 0.5*v2 - 1.0/rp + 0.375*(1.0 - 3.0*nu)*v2*v2 \
        + 0.5/rp*((3.0 + nu)*v2 + 1.0/rp)
    angular = rp*vt*(1.0 + 0.5*(1.0 - 3.0*nu)*v2 + (3.0 + nu)/rp)
    return rp, vt, energy, angular

def damour_deruelle(energy, angular, nu):
    q = -2.0*energy
    n = q**1.5 * (1.0 + q*(-15.0 + nu)/8.0)
    return 6.0*np.pi/(angular*angular), 2.0*np.pi/n

def schwarzschild_from_invariants(binding_energy, angular, p_guess):
    l2 = angular*angular
    e2 = (1.0 + binding_energy)**2
    p = p_guess
    for _ in range(30):
        f = (l2 + 4.0)/p - 8.0*l2/(p*p) + 16.0*l2/p**3 - e2
        df = -(l2 + 4.0)/(p*p) + 16.0*l2/p**3 - 48.0*l2/p**4
        step = f/df
        p -= step
        if abs(step) < 2e-14*p:
            break
    return p, np.sqrt(p - 3.0 - p*p/l2)

def bound_constants(p, e):
    energy = np.sqrt(((p - 2.0)**2 - 4.0*e*e)/(p*(p - 3.0 - e*e)))
    angular = p/np.sqrt(p - 3.0 - e*e)
    return energy, angular

_GL_CACHE = {}
def _gl(n):
    if n not in _GL_CACHE:
        _GL_CACHE[n] = np.polynomial.legendre.leggauss(n)
    return _GL_CACHE[n]

def quad_0_2pi(f, n=400):
    """Gauss-Legendre on [0, 2pi] for smooth periodic-ish integrands."""
    x, w = _gl(n)
    chi = np.pi + np.pi*x
    vals = f(chi)
    return float(np.pi*np.dot(w, vals))

def geodesic_dphi_and_period(p, e):
    """Exact Schwarzschild periastron advance (total dphi - 2pi) and coordinate-time
    radial period, by quadrature over Darwin's chi; same integrands as the Rust
    bound_period_quad (t piece)."""
    energy, angular = bound_constants(p, e)
    c = np.cos(np.pi + np.pi*_gl(400)[0])  # placeholder, replaced below
    def dphi_dchi(chi):
        r = p/(1.0 + e*np.cos(chi))
        return np.sqrt(p/(p - 6.0 - 2.0*e*np.cos(chi)))
    def dt_dchi(chi):
        r = p/(1.0 + e*np.cos(chi))
        return np.sqrt(p/(p - 6.0 - 2.0*e*np.cos(chi))) * r*r/angular * energy/(1.0 - 2.0/r)
    total_dphi = quad_0_2pi(dphi_dchi)
    T = quad_0_2pi(dt_dchi)
    return total_dphi - 2.0*np.pi, T

if __name__ == "__main__":
    # Darwin identity check: advance = 2pi(1/sqrt(1-6/p)-1), e-independent
    for (p, e) in [(20.0, 0.0), (20.0, 0.6), (100.0, 0.3), (1000.0, 0.6)]:
        adv, T = geodesic_dphi_and_period(p, e)
        darwin = 2.0*np.pi*(1.0/np.sqrt(1.0 - 6.0/p) - 1.0)
        print(f"p={p} e={e} adv={adv:.15f} darwin={darwin:.15f} rel={abs(adv-darwin)/darwin:.2e} T={T:.12f}")
