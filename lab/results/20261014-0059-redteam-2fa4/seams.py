#!/usr/bin/env python3
"""The three non-relativistic readout seams, priced in exact SR arithmetic.

S1 (view.rs:395-399): a fleet member's clock rate is rate0*sqrt(1-2*mu/r) — the
member's own kinetic factor sqrt(1-v^2) never enters, so the shipped rate exceeds the
true rate by exactly gamma(beta_m) and Seen.shift (view.rs:308 divides by the rate) is
high by gamma, luminosity (shift**4, view.rs:319) by gamma**4.

S2 (observe.rs:272 `vel = vel + v`): the Doppler numerator uses the Galilean sum of the
doll-chain velocities while the rate is composed exactly; the error is the difference
of the exact and Galilean composed velocities dotted with n, bounded by |v XOR w| =
beta_p*beta_m*(1+beta_p*beta_m)/(1+beta_p*beta_m_dot...) — computed exactly below by
composing the boosts.

S3 (view.rs:288 `vo = vo + dv`): same Galilean composition for a burning observer; in
the root doll (one level) it is exact, so only nested dolls + burn bind.
"""
from math import sqrt, atanh, tanh


def gamma(b):
    return 1.0 / sqrt(1.0 - b * b)


def rapidity_add(b1, b2_scalar, parallel=True):
    """exact SR composition of speeds b1 and b2 in that direction"""
    if parallel:
        return tanh(atanh(b1) + atanh(b2_scalar))
    return sqrt(b1 * b1 + b2_scalar * b2_scalar)  # perpendicular: sqrt sum


print("S1  fleet member: shipped rate / true rate = gamma(beta_m)")
print(f"{'beta_m':>7} {'gamma':>7} {'colour err':>11} {'lum err (g^4-1)':>15}   domain")
for b, where in [(3.05e-5, "the plane's flown battle (2^-15 c)"),
                 (0.14, "1% colour threshold"),
                 (0.31, "5%"),
                 (0.5, ""), (0.7, "contact-law test range"),
                 (0.9, "contact-law test range"), (0.99, "")]:
    g = gamma(b)
    print(f"{b:7.4g} {g:7.4f} {g-1:11.4g} {g**4-1:15.4g}   {where}")

print()
print("S2  nested dolls (planet beta_p, member beta_m perpendicular, worst n):")
print(f"{'beta_p':>8} {'beta_m':>8} {'|v_exact - v_gal|':>18} {'max shift err':>14}")
for bp, bm in [(1e-4, 0.9), (0.1, 0.9), (0.5, 0.9), (0.9, 0.9)]:
    ex = rapidity_add(bp, bm, parallel=False)          # exact composed speed (perp)
    gal = sqrt(bp * bp + bm * bm)                      # Galilean (perp: same!)
    # parallel is the worst case for the difference:
    ex_p = rapidity_add(bp, bm, parallel=True)
    gal = bp + bm
    if gal >= 1.0:
        err = float('inf')  # the Galilean numerator leaves the physical domain entirely
    else:
        num_ex, num_gal = (1 - ex_p) / gamma(ex_p), (1 - gal) / gamma(gal)
        err = abs(num_ex - num_gal) / max(abs(num_ex), 1e-300)
    print(f"{bp:8.4g} {bm:8.4g} {abs(ex_p - gal):18.4g} {err:14.4g}  (parallel)")

print()
print("S3  burning observer in the ROOT doll: exact (one level, no composition).")
print("    The clock side (clocks_with) re-derives the rate with dv in the chain;")
print("    only a nested doll + burn binds, by the S2 arithmetic.")
