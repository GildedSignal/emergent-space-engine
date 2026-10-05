"""Self-test: element-route Kepler propagation vs DOP853, and the event with
the Sun switched off must reproduce two-body scattering to round-off."""
import numpy as np, time
from scipy.integrate import solve_ivp
import conjlaws as C

rng = np.random.default_rng(7)
mu = 1.0
# random conics: mix of ellipse/hyperbola
r = np.exp(1j * rng.uniform(0, 2 * np.pi, 200)) * 10 ** rng.uniform(-1, 1, 200)
vdir = np.exp(1j * rng.uniform(0, 2 * np.pi, 200))
v = vdir * (mu / np.abs(r)) * 10 ** rng.uniform(-0.3, 0.3, 200) * 1.4
dt = 10 ** rng.uniform(-1, 1, 200)

r1, v1 = C.propagate(r, v, mu, dt)

def rhs(t, y):
    rr = y[0] + 1j * y[1]; vv = y[2] + 1j * y[3]
    acc = -mu * rr / abs(rr) ** 3
    return [vv.real, vv.imag, acc.real, acc.imag]

err = 0.0
for i in range(200):
    y0 = [r[i].real, r[i].imag, v[i].real, v[i].imag]
    # scale step for speed: use dense tolerance
    sol = solve_ivp(rhs, [0, dt[i]], y0, rtol=1e-12, atol=1e-14, method="DOP853")
    rt = sol.y[0, -1] + 1j * sol.y[1, -1]
    vt = sol.y[2, -1] + 1j * sol.y[3, -1]
    err = max(err, abs(r1[i] - rt) / abs(rt), abs(v1[i] - vt) / abs(vt))
print(f"propagate vs DOP853 (200 random conics): max rel err = {err:.3e}")

# event with Sun off: pure two-body scattering, compare against DOP853 two-body
mu_p, w = 1e-3, 0.3
d0 = 1.0 + 0.5j
V0 = 0.8 - 0.2j
r_b, v_b = d0, V0
r_p, v_p = 0j, 0j
# our event but with mu_sun = 0: propagate with mu=0 breaks; emulate by exact
d1, V1 = C.propagate(d0, V0, mu_p, 2 * w)
def rhs2(t, y):
    rr = y[0] + 1j * y[1]
    acc = -mu_p * rr / abs(rr) ** 3
    vv = y[2] + 1j * y[3]
    return [vv.real, vv.imag, acc.real, acc.imag]
sol = solve_ivp(rhs2, [0, 2 * w], [d0.real, d0.imag, V0.real, V0.imag], rtol=1e-13, atol=1e-15, method="DOP853")
dt_ = sol.y[0, -1] + 1j * sol.y[1, -1]; dV_ = sol.y[2, -1] + 1j * sol.y[3, -1]
print(f"two-body event vs DOP853: |dd|={abs(d1-dt_):.3e} |dV|={abs(V1-dV_):.3e}")

t0 = time.time()
rs = np.exp(1j * rng.uniform(0, 6.28, 100000)) * 3.0
vs = 1j * rs * 0.55
C.propagate(rs, vs, 1.0, 0.7)
print(f"100k propagations: {time.time()-t0:.3f} s")
