#!/usr/bin/env python3
"""Float prototype: Marck-frame Schwarzschild tide (phase 2) vs the E9 oracle's exact pairs.

Independent derivation, validated against E9's own geodesic-pair oracle:
- comoving tidal components C_rr, C_phiphi, C_rphi (beta form),
- Fermi-frame rotation rate omega_rot (geodetic),
- closed-form candidates for sigma(tau).

Units: M = 1, c = 1, equatorial. Lambda = proper time.
"""
import numpy as np

TAU = 2 * np.pi

# ---------------------------------------------------------------- oracle (E9 style, independent)
def connection(a, r, u, v):
    f = 1.0 - 2.0 * a / r
    g = a / (r * r * f)
    return np.array([
        g * (u[0] * v[1] + u[1] * v[0]),
        f / (r * r) * u[0] * v[0] - g * u[1] * v[1] - f * r * u[2] * v[2],
        (u[1] * v[2] + u[2] * v[1]) / r,
    ])

def metric(a, r, x, y):
    f = 1.0 - 2.0 * a / r
    return -f / a * x[0] * y[0] + x[1] * y[1] / f + r * r * x[2] * y[2]

def rk4_step(y, h, rhs):
    k1 = rhs(y)
    k2 = rhs(y + h / 2 * k1)
    k3 = rhs(y + h / 2 * k2)
    k4 = rhs(y + h * k3)
    return y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

class System:
    """Reference geodesic + two parallel-transported spatial axes. y = [r, dr, t, phi, ax1(3), ax2(3)]."""
    def __init__(self, a, energy, angular):
        self.a, self.energy, self.angular = a, energy, angular
    def tangent(self, y):
        return np.array([self.energy / (1 - 2 * self.a / y[0]), y[1], self.angular / y[0] ** 2])
    def rhs(self, y):
        dy = np.zeros_like(y)
        r, w = y[0], y[1]
        dy[0] = w
        dy[1] = -1 / r**2 + self.angular**2 / r**3 - 3 * self.a * self.angular**2 / r**4
        u = self.tangent(y)
        dy[2] = u[0]
        dy[3] = u[2]
        for start in (4, 7):
            g = connection(self.a, r, u, y[start:start+3])
            dy[start:start+3] = -g
        return dy

def initial(a, e):
    p = (1 + e) / a
    energy = np.sqrt(((p - 2)**2 - 4 * e * e) / (p * (p - 3 - e * e)))
    angular = np.sqrt((1 + e) / (1 - (3 + e * e) * a / (1 + e)))
    f = 1 - 2 * a
    y = np.zeros(10)
    y[0] = 1.0
    u = np.array([energy / f, 0.0, angular])
    ax1 = np.array([0.0, f**0.5, 0.0])
    ax2 = np.array([a * angular / f**0.5, 0.0, energy / f**0.5])
    y[2:4] = 0.0
    y[4:7] = ax1
    y[7:10] = ax2
    return System(a, energy, angular), y

def period_lambda(a, e, points=4096):
    if e == 0.0:
        return TAU * (1 - 3 * a) ** 0.5
    p = (1 + e) / a
    h = TAU / points
    c = np.cos(np.arange(points + 1) * h)
    w = np.ones(points + 1); w[1:-1:2] = 4; w[2:-1:2] = 2
    integ = (1 + e) ** 1.5 * np.sqrt((p - 3 - e * e) / (p - 6 - 2 * e * c)) / (1 + e * c) ** 2
    return (w * integ).sum() * h / 3

# ---------------------------------------------------------------- my phase-2 quantities
def beta_from_state(a, r, dr, L, E):
    """Local static-frame velocity components from geometric state.
    dr = dr/dtau (M=1 units), L, E conserved. Returns (beta_r, beta_phi)."""
    f = 1 - 2 * a / r
    gam = E / f**0.5                     # u^that
    ut = gam / f**0.5
    beta_phi = (L / r) / gam
    beta_r = (dr / f**0.5) / gam
    return beta_r, beta_phi

def tide_comov(a, r, beta_r, beta_phi):
    """C in the comoving (E_r, E_phi, e_theta) frame, per proper time, M=1: (c_rr, c_phiphi, c_rphi, c_thth)."""
    g2 = 1.0 / (1.0 - beta_r**2 - beta_phi**2)
    gr2 = 1.0 + g2 * beta_r**2
    mu = a / r**3
    c_rr = -mu * (2 + beta_phi**2) / (1 - beta_phi**2)
    c_pp = mu * (gr2 - (g2**2 * beta_r**2 / gr2) * (1 + 2 * beta_phi**2))
    c_rp = mu * 3 * g2**1.5 * beta_r * beta_phi / gr2
    c_tt = -c_rr - c_pp
    return c_rr, c_pp, c_rp, c_tt

def omega_rot(a, r, beta_phi):
    f = (1 - 2 * a / r) ** 0.5
    return beta_phi / (1 - beta_phi**2) * (r - 3 * a) / (r**2 * f)

def fermi_angle_from_axes(a, y):
    """Angle of the comoving radial direction measured in the parallel axes + tilt, from oracle axes."""
    r = y[0]
    u = np.array([y[2] * 0 + 0])  # unused
    e1, e2 = y[4:7], y[7:10]
    # comoving radial E_r = (e_r + gam*beta_r*u)/gr ; need u in coordinate components
    sys = None
    return e1, e2

def main():
    np.set_printoptions(precision=6, suppress=True)
    for (a, e) in [(0.1, 0.0), (0.1, 0.6), (0.05, 0.3), (0.001, 0.6)]:
        sys, y = initial(a, e)
        P = period_lambda(a, e)
        steps = 20000
        h = P / steps
        # accumulate sigma via omega_rot; also record vs oracle axes angle
        sigma_int = 0.0
        rec = []
        L, E = sys.angular, sys.energy
        for i in range(steps + 1):
            r = y[0]; dr = y[1]; phi = y[3]
            beta_r, beta_phi = beta_from_state(a, r, dr, L, E)
            # oracle axes: parallel axes e1,e2 in coordinate components; convert to static orthonormal
            f = 1 - 2 * a / r
            e1, e2 = y[4:7], y[7:10]
            # static orthonormal components: v^hat = (v^t*sqrt(f), v^r/sqrt(f), v^phi*r)
            def to_hat(v):
                return np.array([v[0] / f**0.5, v[1] * f**0.5, v[2] * r])
            e1h, e2h = to_hat(e1), to_hat(e2)
            # spatial parts projected: in-plane angle of e1's spatial part relative to radial dir
            ang_e1 = np.arctan2(e1h[2], e1h[1])  # angle from radial direction in static spatial frame
            # my prediction: the parallel axis e1 sits at angle -(sigma + tilt?) relative to E_r... 
            # E_r spatial direction angle from radial: tilt
            gam = E / f**0.5
            gr = (1 + gam**2 * beta_r**2) ** 0.5
            tilt = np.arctan2(gam**2 * beta_r * beta_phi / gr, gr)
            pred = -(sigma_int) + tilt  # e1 = cos(alpha) E_r + sin(alpha) E_phi, alpha = -sigma => angle from E_r = -sigma; E_r at angle tilt from radial
            if i % (steps // 8) == 0:
                rec.append((i * h / P, ang_e1, pred, r, beta_r, beta_phi))
            # integrate sigma
            sigma_int += omega_rot(a, r, beta_phi) * h
            if i < steps:
                y = rk4_step(y, h, sys.rhs)
        print(f"== a={a} e={e}  P_lambda={P:.6f}")
        for (tn, ang, pred, r, br, bp) in rec[:5]:
            print(f"   t/P={tn:5.3f} r={r:9.6f} axes_ang={ang:+.6f} pred={pred:+.6f} d={ang-pred:+.2e} br={br:+.5f} bp={bp:+.5f}")

if __name__ == "__main__":
    main()
