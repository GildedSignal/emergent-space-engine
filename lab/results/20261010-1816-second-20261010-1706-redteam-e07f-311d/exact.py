#!/usr/bin/env python3
"""Exact-rational adjudicator. For each disputed state (from sweep.out, the
decoded integers r_s = px*2^-40, v_t = vy*2^-50) decides bound vs plunge in
EXACT arithmetic (fractions.Fraction), no rounding anywhere:

  u0 = 1/rs; den = 1-2u0-vt^2; L2 = rs^2 vt^2/den; E2 = (1-2u0)^2/den.
  Turning state (u'(0)=0): u0 is a root of C(u) = 2u^3 - u^2 + (2/L2)u + (E2-1)/L2.
  Factor C(u) = (u-u0)(2u^2 + b u + c); the other roots q1<=q2.
  bound  <=>  E2 < 1 and q1,q2 real (b^2-8c >= 0) and max(q1,q2) > u0.

Independent of the crate (which does the same algebra in BigInt).
Usage: python3 exact.py   (reads sweep.out; writes exact.out)
"""
from fractions import Fraction as F

R = 'lab/results/20261010-1816-second-20261010-1706-redteam-e07f-311d'

def exact_bound(px, vy):
    rs = F(px, 2**40)
    vt = F(vy, 2**50)
    u0 = 1 / rs
    den = 1 - 2 * u0 - vt * vt
    if den <= 0:
        return 'plunge'          # E infinite: no bound region
    L2 = rs * rs * vt * vt / den
    E2 = (1 - 2 * u0) ** 2 / den
    if E2 >= 1:
        return 'plunge'          # unbound energy
    # C(u) = 2u^3 - u^2 + (2/L2) u + (E2-1)/L2; u0 is a root (turning state).
    # 2u^3 - u^2 + (2/L2)u + (E2-1)/L2 = (u - u0)(2u^2 + b u + c)
    # => b = 2u0 - 1 ; c = -C4/... solve: expand and match:
    #   2u^3 + (b - 2u0)u^2 + (c - b u0)u - c u0
    #   b - 2u0 = -1        -> b = 2u0 - 1
    #   c - b u0 = 2/L2     -> c = 2/L2 + b u0
    b = 2 * u0 - 1
    c = 2 / L2 + b * u0
    disc = b * b - 8 * c
    if disc < 0:
        return 'plunge'          # other roots complex: u0 is the lone real root
    # q = (-b +- sqrt(disc))/4 ; bound iff max(q) > u0  <=>  (-b+sqrt(disc))/4 > u0
    # avoid the sqrt: q2 > u0  <=>  sqrt(disc) > 4u0 + b  (both sides compared exactly)
    lhs2, rhs = disc, 4 * u0 + b
    if rhs < 0:
        bigger = True            # sqrt >= 0 > rhs
    else:
        bigger = lhs2 > rhs * rhs
    return 'bound' if bigger else 'plunge'

def main():
    import re
    rows = []
    for line in open(f'{R}/sweep.out'):
        t = line.split()
        if len(t) < 7:
            continue
        # reconstruct the integers from the decoded values (they ARE px*2^-40 etc.)
        px, vy = int(t[4]), int(t[5])
        rows.append((float(t[0]), float(t[1]), t[6], px, vy))
    out = open(f'{R}/exact.out', 'w')
    from collections import Counter
    tally = Counter()
    for r0, eps, law, px, vy in rows:
        ex = exact_bound(px, vy)
        lawb = 'bound' if law == 'bound' else 'refuse'
        agree = (lawb == 'bound') == (ex == 'bound')
        tally[(eps, lawb, ex, agree)] += 1
        if not agree:
            out.write(f"DISAGREE r0={r0:.9f} eps={eps:+.0e} law={law} exact={ex}\n")
    for k in sorted(tally):
        out.write(f"{k}: {tally[k]}\n")
    out.close()
    for k, v in sorted(tally.items()):
        print(k, v)

if __name__ == '__main__':
    main()
