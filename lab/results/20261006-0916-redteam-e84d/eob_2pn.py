#!/usr/bin/env python3
"""Attack 2: the 1PN effective-one-body doll vs the true 2PN periastron advance.

Doll: relative motion = exact Schwarzschild geodesics with M = m1+m2; the 1PN EOB map
is time-preserving (real Omega = effective Omega, Damour 1983), so at matched invariant
frequency X = (M*Omega)^{2/3} the doll's advance is the test-mass one:
    k_doll = (1 - 6X)^{-1/2} - 1 = 3X + 13.5 X^2 + ...
Truth (2PN, gauge-invariant, Damour-Schaefer 1988 / Kopeikin 2020 eq. 13), e_T = 0:
    k_true = 3X [1 + X (b1(nu) - b2(nu))]
    b1 = 39/4 x1^2 + 27/4 x2^2 + 15 nu,  b2 = 13/4 (x1^2+x2^2) + nu/3
Parse check at nu=0: b1-b2 = 27/4-13/4 = 3.5 = exact Schwarzschild 2PN coefficient.
"""
import numpy as np
import json

def b1b2(nu):
    x2 = 0.5 * (1 + np.sqrt(1 - 4 * nu))
    x1 = 1 - x2
    b1 = 39 / 4 * x1**2 + 27 / 4 * x2**2 + 15 * nu
    b2 = 13 / 4 * (x1**2 + x2**2) + nu / 3
    return b1, b2

out = []
# parse + method check: nu -> 0 must reproduce exact Schwarzschild
for nu in [0.0, 1e-8, 0.01, 0.1, 0.25]:
    b1, b2 = b1b2(nu)
    out.append({"nu": nu, "b1_minus_b2": b1 - b2})
# relative error of the 1PN doll vs 2PN truth: (k_true - k_doll)/k_true ~ nu-dependent
print(json.dumps(out))
print()
rows = []
for nu in [0.25, 0.1, 0.01]:
    b1, b2 = b1b2(nu)
    for p in [20, 50, 100, 270, 1000]:
        X = 1.0 / p
        k_doll = 3 * X * (1 + 3.5 * X)          # exact Schwarzschild to 2PN
        k_true = 3 * X * (1 + (b1 - b2) * X)
        rows.append({"nu": nu, "p_over_M": p, "rel_adv_error": (k_true - k_doll) / k_true})
for r in rows:
    print(r)
# 1% boundary: X* = 0.01/(b1-b2-3.5)
for nu in [0.25, 0.1]:
    b1, b2 = b1b2(nu)
    Xstar = 0.01 / (b1 - b2 - 3.5)
    print(f"nu={nu}: 1% advance-error boundary at p = {1/Xstar:.0f} M")
