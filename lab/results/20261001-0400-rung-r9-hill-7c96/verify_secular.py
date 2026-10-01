"""Check the closed forms behind kick-avg against direct quadrature of the
rotating-frame tidal potential along an exact Kepler orbit (star fixed on +x,
n_p = 1, GM_s/a_ps^3 = 1).

  <Phi_t> = -(1/2) <3 x^2 - r^2>  should equal  -(a^2/2)[alpha/2 + (3/2) beta cos 2w]
  with alpha = 1 + e^2/2, beta = (5/2) e^2.
The average is over the mean anomaly (Gauss-Legendre in eccentric anomaly,
exact for the band-limited integrand).
"""
import numpy as np

GL_X, GL_W = np.polynomial.legendre.leggauss(64)


def quad_avg(a, e, w, retro):
    E = np.pi * (GL_X + 1)                     # eccentric anomaly in [0, 2pi)
    r = a * (1 - e * np.cos(E))
    f = np.arctan2(np.sqrt(1 - e * e) * np.sin(E), np.cos(E) - e)
    dlam = 1 - e * np.cos(E)                   # dM/dE
    th = (w - f) if retro else (w + f)         # angle from the star line, in the direction of motion
    x = r * np.cos(th)
    phi = -0.5 * (3 * x * x - r * r)
    return np.sum(phi * dlam * GL_W) / np.sum(dlam * GL_W)


def closed(a, e, w):
    return -(a ** 2 / 2) * ((1 + 1.5 * e ** 2) / 2 + 1.5 * (2.5 * e ** 2) * np.cos(2 * w))


if __name__ == "__main__":
    worst = 0.0
    for e in (0.0, 0.05, 0.2, 0.5, 0.8):
        for w in (0.3, 1.1, 2.4):
            for retro in (False, True):
                q, c = quad_avg(1.3, e, w, retro), closed(1.3, e, w)
                worst = max(worst, abs(q - c) / max(abs(c), 1e-12))
    print(f"max |quadrature - closed form| / |closed| = {worst:.2e}")
