#!/usr/bin/env python3
"""Physics sanity: the I2 Hermite reduction and the t/tau/adv closed forms vs mpmath.quad."""
import mpmath as mp
import verify  # same directory; carries the corrected I2/F/E/Pi1/Closed

mp.mp.dps = 30
worst_i2 = 0.0
for m in [0.1, 0.5, 0.9, 0.99]:
    for n in [0.3, 1.0, 5.0]:
        for th in [0.1, 0.7, 1.2, 1.5]:
            lhs = verify.I2(n, th, m)
            rhs = mp.quad(lambda t: 1 / ((1 + n * mp.sin(t) ** 2) ** 2 * mp.sqrt(1 - m * mp.sin(t) ** 2)), [0, th])
            worst_i2 = max(worst_i2, float(abs(lhs - rhs) / rhs))
print(f"I2 Hermite reduction worst rel err vs quad: {worst_i2:.3e}")

worst_ch = {"t": 0.0, "tau": 0.0, "adv": 0.0}
for k, q in [(1 / 1.3, 0.1), (1 / 1.9, 1 / 10.0), (0.999, 1e-4)]:
    c = verify.Closed(mp.mpf(k), mp.mpf(q))
    for psi in [0.3, 1.0, 2.0, 3.0]:
        x = lambda p: k + (1 - k) * mp.cos(p)
        g = lambda p: 1 / mp.sqrt(1 - q * (2 * x(p) + 4 * k))
        tquad = mp.quad(lambda p: c.t_num * g(p) / (x(p) ** 2 * (1 - 2 * q * x(p))), [0, psi])
        tauquad = mp.quad(lambda p: mp.sqrt(k - q * (3 * k * k + (1 - k) ** 2)) * g(p) / x(p) ** 2, [0, psi])
        advquad = mp.quad(lambda p: g(p) - 1, [0, psi])
        worst_ch["t"] = max(worst_ch["t"], float(abs(c.t(psi) - tquad) / tquad))
        worst_ch["tau"] = max(worst_ch["tau"], float(abs(c.tau(psi) - tauquad) / tauquad))
        worst_ch["adv"] = max(worst_ch["adv"], float(abs(c.adv(psi) - advquad)))
print("channel closed forms vs direct quadrature:", {k2: f"{v:.3e}" for k2, v in worst_ch.items()})
