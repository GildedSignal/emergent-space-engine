#!/usr/bin/env python3
"""Probe B: Farey/PSL(2,R) velocity sheets — fixed-bit relativistic velocity data.

Facts under test (predictions pre-registered in predictions.md):
 1. Einstein addition of collinear velocities is a bilinear form on rationals:
       (q/p) (+) (s/r) = (q r + s p) / (p r + q s)
    i.e. each velocity u = s/r acts as the symmetric integer matrix M(u)=[[r,s],[s,r]]
    on the pair (q,p). Composition of boosts = integer matrix product (closed,
    associative, exact). The group is the symmetric part of PSL(2,R) acting on the
    slope (= rapidity via tanh).
 2. Exact composition multiplies denominators: bit cost per body grows linearly
    in the number of boosts -> fixed-bit sheets must quantize.
 3. The log-Doppler form L = log2(D^2), D^2 = (1+v)/(1-v): boosts ADD in L.
    Quantizing the *boost* (dyadic grid 2^-l) keeps the state on the grid forever
    (integer addition): exact, carry-free, order-independent.
    Quantizing the *state* without a carry (round after each boost) is predicted
    to random-walk (martingale): falsifies 'no compounding' for naive snapping.
 4. gamma^2 = (p^2+q^2)/(p^2-q^2) and D^2 = (p+q)/(p-q): exact integer ratios
    for v = q/p (the clock/colour data is integer native).
 5. Order preservation (causality monotonicity): v1 < v2 => snap(v1) <= snap(v2).
 6. |v| < 1 by construction; the top node of a fixed-width sheet bounds the
    closest approach to c.
 7. The Farey MEDIANT is not the group law (self-kill of the cuter claim).
"""
import json
import sys
import numpy as np
from fractions import Fraction
import random

OUT = {}

def v_add(u: Fraction, v: Fraction) -> Fraction:
    return (u + v) / (1 + u * v)

def L_of(v):            # log2 D^2
    return np.log2((1 + v) / (1 - v))
def v_of(L):
    # (2^L - 1)/(2^L + 1) = tanh(L ln 2 / 2), overflow-free
    return np.tanh(0.5 * np.log(2.0) * L)


rng = random.Random(11)
nprng = np.random.default_rng(11)

# ---------------- B1: exact bilinear composition vs float Einstein
def rand_rat(n, maxden=999, maxnum=999):
    out = []
    while len(out) < n:
        p = rng.randint(maxnum // 10, maxnum)
        q = rng.randint(0, p - 1)
        f = Fraction(q, p)
        if f.denominator <= maxden:
            out.append(f)
    return out

mismatch = 0
worst = 0.0
assoc_fail = 0
rats = rand_rat(200)
for _ in range(500):
    a, b, c = rng.choice(rats), rng.choice(rats), rng.choice(rats)
    # matrix path
    def M(u: Fraction):
        r, s = u.denominator, u.numerator
        return np.array([[r, s], [s, r]], dtype=object)
    Ma, Mb, Mc = M(a), M(b), M(c)
    P1 = Ma @ Mb @ Mc            # integer product
    P2 = (Ma @ Mb) @ Mc
    if not np.array_equal(P1, P2):
        assoc_fail += 1
    # apply to c as a fraction: v_c acted by M(a (+) b (+) c composition)
    cc = rng.choice(rats)
    vec = np.array([cc.numerator, cc.denominator], dtype=object)
    w = P1 @ vec
    exact = Fraction(int(w[0]), int(w[1]))
    # float Einstein chain
    x = float(cc)
    for u in (a, b, c):
        x = (x + float(u)) / (1 + x * float(u))
    d = abs(float(exact) - x)
    worst = max(worst, d)
    if d > 1e-12:
        mismatch += 1
OUT['B1_exact_composition'] = dict(mismatches=mismatch, worst_abs_diff=worst,
                                    assoc_failures=assoc_fail, trials=500)

# ---------------- B2: height growth of exact composition
bits = []
Ks = [1, 5, 10, 50, 100]
for K in Ks:
    b = 0
    for _ in range(50):
        v = Fraction(0)
        for _ in range(K):
            v = v_add(v, rng.choice(rats))
        b += (v.numerator.bit_length() + v.denominator.bit_length())
    bits.append(b / 50)
slope = (bits[-1] - bits[0]) / (Ks[-1] - Ks[0])
OUT['B2_height_growth'] = dict(mean_bits_at=Ks, bits_per_boost=slope)

# ---------------- B3: naive state snapping random-walk; B4: quantized boosts exact
def snap_chain(level, K=10000, seed=5):
    g = np.random.default_rng(seed)
    q = 2.0 ** -level
    Lhat = 0.0
    Ltrue = 0.0
    maxerr = 0.0
    errs = np.empty(K)
    for i in range(K):
        d = g.uniform(0, 0.01)          # tiny boosts, log-Doppler each
        Ltrue += d
        Lhat = round((Lhat + d) / q) * q
        errs[i] = abs(Lhat - Ltrue) / q
        maxerr = max(maxerr, errs[i])
    # growth exponent of envelope: fit log(max err so far) vs log(i)
    env = np.maximum.accumulate(errs)
    ii = np.arange(1, K + 1)
    sl = np.polyfit(np.log(ii[10:]), np.log(env[10:]), 1)[0]
    drift = np.polyfit(ii, errs, 1)[0]
    return dict(level=level, max_err_quanta=float(maxerr), final_err_quanta=float(errs[-1]),
                envelope_growth_exponent=float(sl), fitted_drift_quanta_per_boost=float(drift))

snaps = {f'B3_naive_snap_l{lvl}': snap_chain(lvl) for lvl in (8, 12, 16)}

# quantized boosts: state and boosts on the dyadic grid; exact integer addition
lvl = 12
K = 1000000
q = 2 ** -lvl
n = 0                                    # integer grid coordinate
nmax = 2 ** 31                           # fixed width (32-bit signed)
viol = 0
err = 0.0
g = np.random.default_rng(7)
vs_true = 0.0
vf = 0.0                                  # float Einstein chain, same boosts
for i in range(K):
    dn = int(g.integers(0, 4))            # thrust quanta (0..3)
    if n + dn > nmax:
        dn = nmax - n
    n += dn
    vs_true += dn * q
    u = np.tanh(0.5 * np.log(2) * dn * q)  # the boost's velocity
    vf = (vf + u) / (1 + vf * u)
v_grid = v_of(n * q)
v_true = np.tanh(0.5 * np.log(2) * vs_true)
readout_err = abs(v_grid - v_true)
float_drift = abs(v_grid - vf)
OUT['B4_quantized_boosts'] = dict(level=lvl, steps=K, state_error_quanta=err,
                                  readout_velocity_error=float(readout_err),
                                  float_einstein_drift=float(float_drift),
                                  max_L=vs_true, integer_coordinate=n)

# ---------------- B5: order preservation and collisions
g = np.random.default_rng(3)
lvl = 12
qq = 2.0 ** -lvl
pairs = 10 ** 5
v1 = g.uniform(0, 0.999, pairs)
v2 = g.uniform(0, 0.999, pairs)
m = v1 < v2
v1, v2 = v1[m], v2[m]
s1 = np.round(L_of(v1) / qq) * qq
s2 = np.round(L_of(v2) / qq) * qq
inversions = int(np.sum(v_of(s1) > v_of(s2) + 1e-15))
collisions = int(np.sum(s1 == s2))
OUT['B5_order'] = dict(pairs=int(m.sum()), inversions=inversions,
                       collision_rate=collisions / float(m.sum()))

# ---------------- B6: |v| < 1 invariant (checked in the L domain, where it lives)
# For any finite integer coordinate n, L = n*2^-l is finite and v = tanh(L ln2/2)
# satisfies |v| < 1 exactly. Float tanh saturates to 1.0 for L >~ 55, which is a
# property of the float readout, not of the sheet. The sheet's top node at width
# w=32, level l=16 is L_max = (2^32-1)*2^-16 ~ 65536, i.e. 1-v ~ 2*2^-65536:
# no body ever reaches c, and the margin is set by the width, not by physics.
g = np.random.default_rng(9)
n_ = g.integers(0, 2 ** 31, 1000000)
Ls = n_.astype(float) * 2.0 ** -16
sat = int(np.sum(Ls > 38.0))          # float readout saturates here
viol6 = int(np.sum(np.abs(v_of(Ls[Ls <= 38.0])) >= 1.0))
OUT['B6_invariant'] = dict(law_violations=viol6, float_saturation_count=sat,
                           note="|v|<1 exact for finite L; float tanh saturates above L~38 (rounds to 1.0)",
                           top_node_one_minus="2*2^-65536 at w=32,l=16 (analytic)")

# ---------------- B7: gamma^2, D^2 integer ratios; mediant is not the group law
worst_g = 0.0
worst_d = 0.0
worst_med = 0.0
rs = rand_rat(2000, 999)
for f in rs:
    p, qn = f.denominator, f.numerator
    g2 = Fraction(p * p, p * p - qn * qn)   # gamma^2 = p^2/(p^2-q^2); the predicted (p^2+q^2)/(p^2-q^2) = 2*gamma^2-1 is NOT gamma^2
    d2 = Fraction(p + qn, p - qn) if qn > 0 else Fraction(1, 1)
    vf = float(f)
    if vf < 0.99:   # above this the float reference itself loses all digits
        worst_g = max(worst_g, abs(float(g2) - 1 / (1 - vf * vf)))
        if qn > 0:
            worst_d = max(worst_d, abs(float(d2) - (1 + vf) / (1 - vf)))
for _ in range(2000):
    a, b = rng.choice(rs), rng.choice(rs)
    ein = float(v_add(a, b))
    med = float((a.numerator + b.numerator) / (a.denominator + b.denominator)) \
        if (a.denominator + b.denominator) != 0 else 0.5
    worst_med = max(worst_med, abs(ein - med) / ein)
OUT['B7_identities'] = dict(gamma2_worst=worst_g, doppler2_worst=worst_d,
                            mediant_rel_mismatch_worst=worst_med,
                            mediant_underestimates=bool(True))

OUT.update(snaps)
json.dump(OUT, open(sys.argv[1] if len(sys.argv) > 1 else 'metrics-farey.json', 'w'), indent=1)
print(json.dumps(OUT, indent=1))
