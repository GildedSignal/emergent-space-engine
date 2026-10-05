#!/usr/bin/env python3
"""P2 — Holonomy of integer-shear handoff loops (three dolls), R3's shears.

R3 (Opus memo, adopted): a boost is three integer shears S_t(a) S_x(b) S_t(a)
with a = -tanh(eta/2) dyadic and b = -sinh(eta) = 2a/(1-a^2) the exact rational
a implies; a rotation is S_x(a) S_y(b) S_x(a) with a = -tan(theta/2),
b = sin(theta) = -2a/(1+a^2). Out-and-back is the identity bit for bit.

This probe measures what that leaves open: a LOOP of handoffs A->B->C->A,
n times, for one event offset. Defects separated:

  D1 (atlas consistency, no floors, exact rationals):
     - 'pairwise': each pair's relative velocity computed in float and quantized
       independently -> the rational loop is NOT the identity.
     - 'derived': each frame quantizes its own boost once (one exact rational
       matrix); pair maps are exact products L_B^-1 L_A -> the loop is exactly I.
  D2 (floor holonomy): the integer loop with floors, with and without a
     sigma-delta remainder carried per shear step.

Controls: out-and-back exact; single-handoff defect vs the un-floored rational
map with the same coefficients (<= ~1 unit per event at moderate beta).
"""
import json
from fractions import Fraction
import numpy as np

NB = 24  # shear coefficient word: a = -p / 2^NB


def floordiv(num, den):
    return num // den  # Python floor division is exact on negatives


def shear_add(c_num, c_den, v, u, carry=None):
    """v += floor(c*u); optional sigma-delta remainder carry (denominator units)."""
    if carry is None:
        return v + floordiv(c_num * u, c_den), None
    y = c_num * u + carry
    q = floordiv(y, c_den)
    return v + q, y - q * c_den


def boost_params(beta, n=NB):
    eta = float(np.arctanh(beta))
    a_exact = -np.tanh(eta / 2)
    p = int(round(-a_exact * (1 << n)))
    a_num, a_den = -p, 1 << n
    b_num = 2 * a_num * a_den
    b_den = a_den * a_den - a_num * a_num
    return (a_num, a_den), (b_num, b_den)


def rot_params(theta, n=NB):
    """Shear coefficients for rotation by theta. |theta| > pi/2 is split into
    an exact negation (rotation by pi) plus a residual away from the tan blow-up
    (the trap Opus's R3 note names: tan(theta/2) amplifies rounding near pi)."""
    neg = False
    if abs(theta) > np.pi/2:
        theta = theta - np.pi if theta > 0 else theta + np.pi
        neg = True
    a_exact = -np.tan(theta / 2)
    p = int(round(-a_exact * (1 << n)))
    a_num, a_den = -p, 1 << n
    b_num = -2 * a_num * a_den
    b_den = a_den * a_den + a_num * a_num
    return (a_num, a_den), (b_num, b_den), neg


def rot3(a, b, s, carries=None, neg=False):
    """R(theta) on (x,y): x += a*y ; y += b*x ; x += a*y; optional exact
    negation when the original angle exceeded pi/2 (R = N o R(residual))."""
    t, x, y = s
    if neg:
        x, y = -x, -y
    if carries is None:
        x = x + floordiv(a[0] * y, a[1])
        y = y + floordiv(b[0] * x, b[1])
        x = x + floordiv(a[0] * y, a[1])
        return (t, x, y), None
    x, carries[0] = shear_add(a[0], a[1], x, y, carries[0])
    y, carries[1] = shear_add(b[0], b[1], y, x, carries[1])
    x, carries[2] = shear_add(a[0], a[1], x, y, carries[2])
    return (t, x, y), carries



def boost3(a, b, s, carries=None):
    """B(eta) on (t,x): t += a*x ; x += b*t ; t += a*x."""
    t, x, y = s
    if carries is None:
        t = t + floordiv(a[0] * x, a[1])
        x = x + floordiv(b[0] * t, b[1])
        t = t + floordiv(a[0] * x, a[1])
        return (t, x, y), None
    t, carries[0] = shear_add(a[0], a[1], t, x, carries[0])
    x, carries[1] = shear_add(b[0], b[1], x, t, carries[1])
    t, carries[2] = shear_add(a[0], a[1], t, x, carries[2])
    return (t, x, y), carries


def handoff(params, s, carries=None):
    """params = [rot(phi), boost, rot(-phi)] with optional neg flags."""
    (ar, br, nr), (ab, bb), (arn, brn, nrn) = params
    s, c1 = rot3(ar, br, s, carries[0] if carries else None, neg=nr)
    s, c2 = boost3(ab, bb, s, carries[1] if carries else None)
    s, c3 = rot3(arn, brn, s, carries[2] if carries else None, neg=nrn)
    return (s, [c1, c2, c3]) if carries else (s, None)


def handoff_params_pairwise(v_from, v_to):
    """Quantize this pair's relative boost (magnitude and direction) independently."""
    import numpy as _np
    bx, by = v_from
    cx, cy = v_to
    dot = bx*cx + by*cy
    g = 1.0 / np.sqrt(1 - bx*bx - by*by)
    ux = cx - bx + (dot / (1 + g)) * bx
    uy = cy - by + (dot / (1 + g)) * by
    den = 1 - dot
    ux, uy = ux/den, uy/den
    beta = float(np.hypot(ux, uy))
    phi = float(np.arctan2(uy, ux))
    ab, bb = boost_params(beta)
    ar, br, nr = rot_params(phi)
    arn, brn, nrn = rot_params(-phi)
    return [(ar, br, nr), (ab, bb), (arn, brn, nrn)]


def rot3_undo(a, b, s, neg=False):
    """Exact inverse of rot3(a,b,s,neg): subtract the same floored amounts,
    then undo the negation."""
    t, x, y = s
    x = x - floordiv(a[0] * y, a[1])
    y = y - floordiv(b[0] * x, b[1])
    x = x - floordiv(a[0] * y, a[1])
    if neg:
        x, y = -x, -y
    return (t, x, y)


def boost3_undo(a, b, s):
    t, x, y = s
    t = t - floordiv(a[0] * x, a[1])
    x = x - floordiv(b[0] * t, b[1])
    t = t - floordiv(a[0] * x, a[1])
    return (t, x, y)


def handoff_undo(params, s):
    (ar, br, nr), (ab, bb), (arn, brn, nrn) = params
    s = rot3_undo(arn, brn, s, neg=nrn)
    s = boost3_undo(ab, bb, s)
    s = rot3_undo(ar, br, s, neg=nr)
    return s


def inverse_params(params):
    (ar, br), (ab, bb), (arn, brn) = params
    # inverse of R(phi) B R(-phi) is R(phi) B^-1 R(-phi) with negated b, and a
    # shear inverse negates a: exact reverse of each step in reverse order.
    return [((-arn[0], arn[1]), (-brn[0], brn[1])),
            ((-ab[0], ab[1]), (-bb[0], bb[1])),
            ((-ar[0], ar[1]), (-br[0], br[1]))]


# --------- exact rational (unfloored) variants with the same coefficients ---------
def rot3_rat(a, b, sf):
    t, x, y = sf
    x = x + Fraction(a[0], a[1]) * y
    y = y + Fraction(b[0], b[1]) * x
    x = x + Fraction(a[0], a[1]) * y
    return (t, x, y)


def boost3_rat(a, b, sf):
    t, x, y = sf
    t = t + Fraction(a[0], a[1]) * x
    x = x + Fraction(b[0], b[1]) * t
    t = t + Fraction(a[0], a[1]) * x
    return (t, x, y)


def handoff_rat(params, sf):
    (ar, br, nr), (ab, bb), (arn, brn, nrn) = params

    def rot_r(a, b, sf, neg):
        t, x, y = sf
        if neg:
            x, y = -x, -y
        x = x + Fraction(a[0], a[1]) * y
        y = y + Fraction(b[0], b[1]) * x
        x = x + Fraction(a[0], a[1]) * y
        return (t, x, y)

    sf = rot_r(ar, br, sf, nr)
    t, x, y = sf
    t = t + Fraction(ab[0], ab[1]) * x
    x = x + Fraction(bb[0], bb[1]) * t
    t = t + Fraction(ab[0], ab[1]) * x
    sf = (t, x, y)
    sf = rot_r(arn, brn, sf, nrn)
    return sf


def frame_matrix_float(beta_x, beta_y):
    eta = float(np.arctanh(np.hypot(beta_x, beta_y)))
    phi = float(np.arctan2(beta_y, beta_x))
    ch, sh = np.cosh(eta), np.sinh(eta)
    c, s = np.cos(phi), np.sin(phi)
    M = np.eye(3)
    M[0, 0] = ch; M[0, 1] = sh*c; M[0, 2] = sh*s
    M[1, 0] = sh*c; M[2, 0] = sh*s
    nn = np.array([[c*c, c*s], [c*s, s*s]])
    M[1:, 1:] = np.eye(2) + (ch - 1)*nn
    return M


def decompose_boost_rot(M):
    """M = R(theta) B(eta, phi) (rotation AFTER boost in column convention).
    Returns (eta, phi, theta). phi from the dominant eigenvector of S S^T."""
    # closed-form polar decomposition in the Lorentz group: Lambda = R(theta) B(eta, phi)
    # first row (unaffected by a LEFT rotation) gives the boost direction:
    ch = M[0, 0]
    sh = float(np.hypot(M[1, 0], M[2, 0]))
    eta = float(np.arcsinh(sh))
    phi = float(np.arctan2(M[0, 2], M[0, 1]))
    # first column is the rotated boost direction: psi = phi + theta
    psi = float(np.arctan2(M[2, 0], M[1, 0]))
    theta = psi - phi
    if theta > np.pi: theta -= 2*np.pi
    if theta < -np.pi: theta += 2*np.pi
    return eta, phi, theta


def handoff_params_derived(L_from, L_to):
    """Pairwise handoff from per-frame boost matrices: full Lorentz map
    (boost + Wigner rotation), quantized to the shear lattice."""
    Mrel = np.linalg.inv(L_to) @ L_from
    eta, phi, theta = decompose_boost_rot(Mrel)
    ab, bb = boost_params(float(np.tanh(eta)))
    ar, br, nr = rot_params(-phi)
    arn, brn, nrn = rot_params(phi)
    at, bt, nt = rot_params(theta)
    return [(ar, br, nr), (ab, bb), (arn, brn, nrn), (at, bt, nt)]


def handoff4(params, s, carries=None):
    """handoff with an extra final rotation stage (the Wigner angle)."""
    (ar, br, nr), (ab, bb), (arn, brn, nrn), (at, bt, nt) = params
    s, c1 = rot3(ar, br, s, carries[0] if carries else None, neg=nr)
    s, c2 = boost3(ab, bb, s, carries[1] if carries else None)
    s, c3 = rot3(arn, brn, s, carries[2] if carries else None, neg=nrn)
    s, c4 = rot3(at, bt, s, carries[3] if carries else None, neg=nt)
    return (s, [c1, c2, c3, c4]) if carries else (s, None)


def handoff4_undo(params, s):
    (ar, br, nr), (ab, bb), (arn, brn, nrn), (at, bt, nt) = params
    s = rot3_undo(at, bt, s, neg=nt)
    s = rot3_undo(arn, brn, s, neg=nrn)
    s = boost3_undo(ab, bb, s)
    s = rot3_undo(ar, br, s, neg=nr)
    return s


# --------- derived atlas: per-frame quantized rational Lorentz matrices ---------
def frame_matrix(beta_x, beta_y):
    """Quantize the frame's own rapidity magnitude and direction once; exact
    rational 3x3 boost matrix (active, from rest to velocity)."""
    eta = float(np.arctanh(np.hypot(beta_x, beta_y)))
    phi = float(np.arctan2(beta_y, beta_x))
    aq = Fraction(int(round(-np.tanh(eta/2) * (1 << NB))), 1 << NB)
    phq = Fraction(int(round(phi * (1 << 16))), 1 << 16)
    ch = (1 + aq*aq) / (1 - aq*aq)
    sh = 2*aq / (1 - aq*aq)
    # cos/sin of the rational angle, snapped to large-denominator rationals:
    c = Fraction(float(np.cos(float(phq)))).limit_denominator(10**12)
    s = Fraction(float(np.sin(float(phq)))).limit_denominator(10**12)
    nn = [[c*c, c*s], [c*s, s*s]]
    M = [[Fraction(0)]*3 for _ in range(3)]
    M[0][0] = ch
    M[0][1] = sh * c; M[0][2] = sh * s
    M[1][0] = sh * c; M[2][0] = sh * s
    for i in (1, 2):
        for j in (1, 2):
            M[i][j] = (Fraction(1) if i == j else Fraction(0)) + (ch - 1) * nn[i-1][j-1]
    return M


def mat_mul(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def mat_inv(M):
    a, b, c = M[0]; d, e, f = M[1]; g, h, i = M[2]
    A = e*i - f*h; B = -(d*i - f*g); C = d*h - e*g
    det = a*A + b*B + c*C
    cof = [[A, B, C],
           [-(b*i - c*h), a*i - c*g, -(a*h - b*g)],
           [b*f - c*e, -(a*f - c*d), a*e - b*d]]
    return [[cof[i][j]/det for j in range(3)] for i in range(3)]


def main():
    out = {}
    vA, vB, vC = (0.0, 0.0), (0.3, 0.0), (0.2, 0.25)

    # ---------- control 1: out and back ----------
    ok = 0
    for trial in range(200):
        pr = np.random.default_rng(trial)
        beta = float(pr.uniform(0.001, 0.9))
        s = (int(pr.integers(1, 1 << 23)), int(pr.integers(1, 1 << 23)), int(pr.integers(1, 1 << 23)))
        pars = handoff_params_pairwise((0.0, 0.0), (beta, 0.0))
        s1, _ = handoff(pars, s)
        s2 = handoff_undo(pars, s1)
        ok += (s2 == s)
    out['out_and_back_exact'] = [ok, 200]
    print(f"control out-and-back: {ok}/200 exact identity")

    # ---------- control 2: single-handoff defect vs un-floored rational ----------
    single = {}
    for beta in (0.01, 0.3, 0.9):
        pars = handoff_params_pairwise((0.0, 0.0), (beta, 0.0))
        worst = 0
        for trial in range(200):
            pr = np.random.default_rng(1000 + trial)
            s = (int(pr.integers(1, 1 << 23)), int(pr.integers(1, 1 << 23)), int(pr.integers(1, 1 << 23)))
            s1, _ = handoff(pars, s)
            sf = handoff_rat(pars, tuple(Fraction(v) for v in s))
            d = max(abs(s1[i] - sf[i]) for i in range(3))
            worst = max(worst, float(d))
        single[str(beta)] = worst
    out['single_handoff_max_defect_units'] = single
    print('single-handoff max defect (units):', single)

    # ---------- D1: atlas consistency ----------
    pAB = handoff_params_pairwise(vA, vB)
    pBC = handoff_params_pairwise(vB, vC)
    pCA = handoff_params_pairwise(vC, vA)
    s0 = (1 << 20, 1 << 19, -(1 << 18))
    sf0 = tuple(Fraction(v) for v in s0)
    sf = sf0
    d1 = []
    for n in range(1, 257):
        sf = handoff_rat(pAB, sf); sf = handoff_rat(pBC, sf); sf = handoff_rat(pCA, sf)
        if n in (1, 4, 16, 64, 256):
            d1.append((n, float(max(abs(sf[i] - sf0[i]) for i in range(3)))))
    out['D1_pairwise_rational_loop'] = d1
    print('D1 pairwise-quantized rational loop defect (units):', d1)

    LA, LB, LC = frame_matrix(*vA), frame_matrix(*vB), frame_matrix(*vC)
    LAB = mat_mul(mat_inv(LB), LA)   # A -> B
    LBC = mat_mul(mat_inv(LC), LB)   # B -> C
    LCA = mat_mul(mat_inv(LA), LC)   # C -> A
    loopM = mat_mul(LCA, mat_mul(LBC, LAB))
    idM = [[Fraction(int(i == j)) for j in range(3)] for i in range(3)]
    exact_ident = all(loopM[i][j] == idM[i][j] for i in range(3) for j in range(3))
    out['D1_derived_rational_loop_is_identity'] = bool(exact_ident)
    print(f"D1 derived (per-frame quantized, exact products): identity = {exact_ident}")

    # ---------- D2: floor holonomy on the DERIVED atlas, with and without carry ----------
    LAf, LBf, LCf = frame_matrix_float(*vA), frame_matrix_float(*vB), frame_matrix_float(*vC)
    dAB = handoff_params_derived(LAf, LBf)
    dBC = handoff_params_derived(LBf, LCf)
    dCA = handoff_params_derived(LCf, LAf)

    def reconstruct_check():
        worst = 0.0
        for Lf, Lt, name in ((LAf, LBf, 'AB'), (LBf, LCf, 'BC'), (LCf, LAf, 'CA')):
            Mrel = np.linalg.inv(Lt) @ Lf
            eta, phi, theta = decompose_boost_rot(Mrel)
            R = lambda a: np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
            ch, sh = np.cosh(eta), np.sinh(eta)
            c, s = np.cos(phi), np.sin(phi)
            B = np.eye(3)
            B[0, 0] = ch
            B[0, 1:] = sh*np.array([c, s])
            B[1:, 0] = sh*np.array([c, s])
            B[1:, 1:] = np.eye(2) + (ch - 1)*np.array([[c*c, c*s], [c*s, s*s]])
            Mrec = np.eye(3)
            Mrec[0, :] = B[0, :]
            Mrec[1:, 0] = R(theta) @ B[1:, 0]
            Mrec[1:, 1:] = R(theta) @ B[1:, 1:]
            worst = max(worst, float(np.max(np.abs(Mrec - Mrel))))
        return worst
    out['decompose_reconstruction_error'] = reconstruct_check()
    print(f"decompose reconstruction error: {out['decompose_reconstruction_error']:.2e}")
    # control: derived out-and-back
    okd = 0
    for trial in range(200):
        pr = np.random.default_rng(7000 + trial)
        s = (int(pr.integers(1, 1 << 23)), int(pr.integers(1, 1 << 23)), int(pr.integers(1, 1 << 23)))
        s1, _ = handoff4(dAB, s)
        okd += (handoff4_undo(dAB, s1) == s)
    out['derived_out_and_back_exact'] = [okd, 200]
    print(f"control derived out-and-back (4-stage, undo): {okd}/200 exact")

    # the pairwise pure-boost leak, quantified: it is the Wigner angle of the loop
    wigner = abs(decompose_boost_rot(np.linalg.inv(LAf) @ LCf @ np.linalg.inv(LCf) @ LBf @ np.linalg.inv(LBf) @ LAf)[2])
    out['loop_wigner_angle_rad'] = float(wigner)
    print(f"loop Wigner angle (rad): {wigner:.3e}")

    def run_loop(n_loops, use_carry):
        s = s0
        carries = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]] for _ in range(3)] if use_carry else None
        for _ in range(n_loops):
            for k, pars in enumerate((dAB, dBC, dCA)):
                if use_carry:
                    s, carries[k] = handoff4(pars, s, carries[k])
                else:
                    s, _ = handoff4(pars, s)
        return max(abs(s[i] - s0[i]) for i in range(3))

    ns = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    series = {'nocarry': [], 'carry': []}
    for use_carry, key in ((False, 'nocarry'), (True, 'carry')):
        for n in ns:
            series[key].append((n, float(run_loop(n, use_carry))))
    out['D2_floor_loop_series'] = series
    print('D2 floor loop, no carry:', series['nocarry'])
    print('D2 floor loop, carry   :', series['carry'])

    def expo(pts):
        import math
        q = [(math.log2(n), math.log2(max(d, 1e-12))) for n, d in pts if d > 0]
        if len(q) < 4:
            return None
        xs = [p[0] for p in q]; ys = [p[1] for p in q]
        k = len(q)//2
        return (ys[-1] - ys[k]) / (xs[-1] - xs[k]) if xs[-1] > xs[k] else 0.0
    out['D2_exponent_nocarry'] = expo(series['nocarry'])
    out['D2_exponent_carry'] = expo(series['carry'])
    print(f"D2 exponents: nocarry={out['D2_exponent_nocarry']}, carry={out['D2_exponent_carry']}")

    with open('probe2_out.json', 'w') as f:
        json.dump(out, f, indent=1, default=float)


if __name__ == '__main__':
    main()
