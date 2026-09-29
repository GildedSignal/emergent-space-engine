#!/usr/bin/env python3
"""E3: size of the beyond-1PN precession at r3's seed floor (p down to 20 M).
E4: Minsky mutual-update rotation: systematic frequency bias vs step size, and the
    steps/cycle needed to hold 1% precession accuracy (r1's gate) in weak fields."""
import math

# ---------- E3: exact Schwarzschild test-body precession vs 6*pi/p ----------

def precession(p, e, dphi=2 * math.pi / 4000.0):
    """Integrate exact Binet u'' + u = 1/L^2 + 3u^2 (M=1) from periapsis to periapsis."""
    L2 = p                      # Newtonian-consistent choice; fixes near-Kepler orbit
    u = (1 + e) / p
    w = 0.0
    phi = 0.0
    def acc(u, w):
        return 1.0 / L2 + 3.0 * u * u - u
    passed_apo = False
    n = 0
    while n < 2_000_000:
        k1u, k1w = w, acc(u, w)
        k2u, k2w = w + 0.5 * dphi * k1w, acc(u + 0.5 * dphi * k1u, w + 0.5 * dphi * k1w)
        k3u, k3w = w + 0.5 * dphi * k2w, acc(u + 0.5 * dphi * k2u, w + 0.5 * dphi * k2w)
        k4u, k4w = w + dphi * k3w, acc(u + dphi * k3u, w + dphi * k3w)
        u_new = u + dphi / 6.0 * (k1u + 2 * k2u + 2 * k3u + k4u)
        w_new = w + dphi / 6.0 * (k1w + 2 * k2w + 2 * k3w + k4w)
        if not passed_apo:
            if w_new > 0.0 and w < 0.0:
                passed_apo = True
        else:
            if w_new <= 0.0 and w > 0.0:
                frac = w / (w - w_new)
                return phi + frac * dphi, u + frac * (u_new - u)
        u, w, phi = u_new, w_new, phi + dphi
        n += 1
    return float("nan"), u

print("E3: exact Schwarzschild precession vs 1PN (6*pi/p), e = 0.3")
for p in (20, 50, 200, 1000):
    dphi_tot, u_end = precession(p, 0.3)
    adv = dphi_tot - 2 * math.pi
    pn = 6 * math.pi / p
    print(f"  p={p:5d}  exact advance {adv:.6f}  1PN {pn:.6f}  "
          f"rel diff {(adv - pn) / pn * 100:+.2f}%")

# ---------- E4: Minsky rotation bias ----------

print("\nE4: Minsky (forward-Euler mutual update) rotation, intended angle eps per step:")
print("  effective angle theta = arccos(1 - eps^2/2); relative bias = theta/eps - 1 ~ eps^2/24")
print("  requirement for r1's 1% precession gate: bias * Phi_cycle <= 0.01 * Dvarpi,")
print("  with Dvarpi = 6*pi*M/r (e=0), Phi_cycle = 2*pi + Dvarpi\n")
print("  r/M      eps_max   steps/cycle   (vs 512-crossing budget of r1)")
for r in (6, 20, 100, 1000, 10**6):
    adv = 6 * math.pi / r
    Phi = 2 * math.pi + adv
    eps2 = 0.01 * adv * 24.0 / Phi
    eps = math.sqrt(eps2)
    steps = Phi / eps
    print(f"  {r:8g}  {eps:.2e}  {steps:10.0f}")
