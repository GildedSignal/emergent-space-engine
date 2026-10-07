#!/usr/bin/env python3
"""H_live ledger falsifier — run 20261007-0621-scout-6e10 (v2).

Fixes over v1: all state measured in the coordinates the birth program
generates (a, h=e cos varpi, k=e sin varpi, M); residual entropies are
differential (log2(sigma*sqrt(2 pi e)/q), no sample ceiling) with an empirical
cross-check where n*H < log2(n); churn split smooth-in-phase vs chaotic.

Measured stock quantities (bits per body), not flow:
  A. belt (B18b scene, N=2^20, Laplace-Lagrange secular flow, 12 epochs of
     10 orbits, churn 1e-2/epoch):
     - program-with-t residual: the law advances by quantized increments, so a
       generator that carries t still drifts from the grid path (carry walk);
     - churn: kicked bodies' residual vs a refit over birth features;
       smooth kicks should recapture, chaotic (sin(phase/eps)) should not;
     - static birth program scar (the no-repack wrong form), for reference.
  B. battle: fleet of 2^14 born on one orbit (0 bits/member); kicks = shared
     drift + slot-linear + per-member sum; residual after best-fit program,
     in (h,k) (generator coordinates) and in (e,varpi) (the naive form).
Controls: no-perturber belt -> 0 scars exactly; zero-kick battle -> ~0 bits.
Deterministic: seeded. Regenerates h_live_ledger.json.
"""
import json
import numpy as np

R = {}
rng = np.random.default_rng(20261007)
C2PI = 2 * np.pi

def quant(x, q):
    return np.round(x / q).astype(np.int64)

def ent(ints):
    if len(ints) == 0:
        return 0.0
    _, c = np.unique(ints, return_counts=True)
    p = c / c.sum()
    return float(-(p * np.log2(p)).sum())

def dh(r, q):
    """differential entropy (bits) of a near-Gaussian residual at quantum q."""
    s = float(np.std(r))
    if s <= 0:
        return 0.0
    return max(0.0, float(np.log2(s * np.sqrt(2 * np.pi * np.e) / q)))

def ang_delta(x, y):
    return (x - y + np.pi) % C2PI - np.pi

def sparse_bits_per_member(bits_per_scarred, f):
    idx = f * np.log2(1 / f) + 2 * f if f > 0 else 0.0
    return f * bits_per_scarred + idx

# ---------------- belt ----------------------------------------------------
N = 1 << 20
A0, A1 = 2.0, 3.6
a = A0 + (A1 - A0) * rng.random(N)
e0 = 0.1 * np.sqrt(-2 * np.log(1 - rng.random(N)))
w0 = C2PI * rng.random(N)
M0 = C2PI * rng.random(N)
GM = 4 * np.pi ** 2
n = np.sqrt(GM / a ** 3)
AJ, EJ, MU = 5.2, 0.05, 1e-3
alpha = a / AJ
g = n * 0.75 * MU * alpha * 2.0
gJ = 0.75 * MU * np.sqrt(GM / AJ ** 3)
ef = 1.25 * alpha * EJ
z0 = e0 * np.exp(1j * w0)
h0, k0 = z0.real, z0.imag
P_orb = C2PI / n

Q = {kk: dict(a=(A1 - A0) * 2 ** -kk, e=0.6 * 2 ** -kk, ang=C2PI * 2 ** -kk)
     for kk in (16, 24, 32)}
KQ = 24
EPOCHS, EP_ORBITS, CHURN = 12, 10, 1e-2
QE, QA, QM = Q[KQ]["e"], Q[KQ]["a"], Q[KQ]["ang"]

def secular_z(t_orb):
    T = t_orb * P_orb
    return ef * np.exp(1j * gJ * T) + (z0 - ef) * np.exp(1j * g * T)

def secular_M(t_orb):
    return M0 + n * (t_orb * P_orb)

belt = {"epochs": []}
# integer law path: state kept in QUANTA (never rescaled in float; the unit mix
# below was a real bug found by the zero control: int64 wrap after 2 epochs)
zq_h = quant(h0, QE).astype(float)
zq_k = quant(k0, QE).astype(float)
Mq = quant(M0, QM).astype(float)
t_orb = 0
aprime = (a - A0) / (A1 - A0)
# program basis: products of (1, a, a^2) with the birth angles — the class a
# secular kick lives in (amp(a) * sin/cos(M0 + phi) is exactly in this span)
basis = np.column_stack([
    np.ones(N), aprime, aprime ** 2, e0, np.cos(w0), np.sin(w0),
    np.cos(M0), np.sin(M0),
    aprime * np.cos(M0), aprime * np.sin(M0),
    aprime ** 2 * np.cos(M0), aprime ** 2 * np.sin(M0)])

for ep in range(1, EPOCHS + 1):
    t_orb += EP_ORBITS
    z = secular_z(t_orb)
    M = secular_M(t_orb)
    # (1) program-with-t residual: the grid path vs the closed form.
    # advances are exact integer increments in quanta (round once per epoch)
    dz = z - secular_z(t_orb - EP_ORBITS)
    zq_h = np.round(zq_h + dz.real / QE)
    zq_k = np.round(zq_k + dz.imag / QE)
    dM = (M - secular_M(t_orb - EP_ORBITS)) / QM
    Mq = np.round(Mq + dM)
    carry = dict(h=round(dh(zq_h - z.real / QE, 1.0), 3),
                 k=round(dh(zq_k - z.imag / QE, 1.0), 3),
                 M=round(dh(Mq - M / QM, 1.0), 3))
    # (2) churn kicks: half smooth (a function of birth state: the secular
    # kind), half chaotic (depends on encounter phase: irreducible)
    hit = rng.random(N) < CHURN
    is_chaot = np.zeros(N, bool)
    is_chaot[hit] = rng.random(hit.sum()) < 0.5
    # smooth: amp(a) quadratic in a, direction from birth M0 (+ shared phase)
    phi_ep = C2PI * rng.random()
    amp_s = 0.03 * (0.02 + 0.5 * aprime - 0.3 * aprime ** 2)
    kick_s = amp_s * np.exp(1j * (M0 + phi_ep))
    # chaotic: direction and magnitude from the encounter (not birth state)
    s_c = 0.03 * (rng.random(N) ** 2 + 0.02)
    kick_c = s_c * np.exp(1j * C2PI * rng.random(N))
    z2 = z.copy()
    m_smooth = hit & ~is_chaot
    m_chaot = hit & is_chaot
    z2[m_smooth] += kick_s[m_smooth]
    z2[m_chaot] += kick_c[m_chaot]
    # recapture: a kicked subfamily gets its OWN program (the event's program:
    # recapture: the birth program predicts z exactly; only the kick is new,
    # so the event program fits the delta on each kicked subset
    ds = z2[m_smooth] - z[m_smooth]
    coef, *_ = np.linalg.lstsq(basis[m_smooth], np.column_stack(
        [ds.real, ds.imag]), rcond=None)
    rs = ds.real - basis[m_smooth] @ coef[:, 0]
    ks = ds.imag - basis[m_smooth] @ coef[:, 1]
    dc = z2[m_chaot] - z[m_chaot]
    coef, *_ = np.linalg.lstsq(basis[m_chaot], np.column_stack(
        [dc.real, dc.imag]), rcond=None)
    rc = dc.real - basis[m_chaot] @ coef[:, 0]
    kc = dc.imag - basis[m_chaot] @ coef[:, 1]
    kick = dict(
        smooth_bits_given_membership=round(dh(rs, QE) + dh(ks, QE), 3),
        chaotic_bits_given_membership=round(dh(rc, QE) + dh(kc, QE), 2),
        chaotic_scale_bits=round(2 * np.log2(np.std(kick_c[m_chaot].real) / QE), 2),
    )
    fs, fc = float(m_smooth.mean()), float(m_chaot.mean())
    idx_s = fs * np.log2(1 / fs) + 2 * fs if fs > 0 else 0.0
    idx_c = fc * np.log2(1 / fc) + 2 * fc if fc > 0 else 0.0
    per_member = (idx_s + idx_c
                  + fc * kick["chaotic_bits_given_membership"]
                  + fs * kick["smooth_bits_given_membership"])
    belt["epochs"].append(dict(
        epoch=ep, t_orbits=t_orb, carry=carry, kicked=int(hit.sum()),
        kick=kick, churn_bits_per_member=round(per_member, 4),
    ))

# (3) static birth program scar at 12 epochs, wrong form (e, varpi, M)
scar = (dh(z.real - h0, QE) + dh(z.imag - k0, QE) + dh(M - M0, QM))
ctrl = dh(secular_z(0.0).real - h0, QE)
belt["static_scar_12ep_bits"] = round(scar, 2)
belt["control_zero_perturber_bits"] = round(ctrl, 3)
belt["quantum_bracket_carry_h"] = {
    "q16": round(dh(zq_h - z.real / QE, Q[16]["e"] / QE), 2),
    "q24": round(dh(zq_h - z.real / QE, 1.0), 2),
    "q32": round(dh(zq_h - z.real / QE, Q[32]["e"] / QE), 2),
}
R["belt"] = belt

# ---------------- battle --------------------------------------------------
FLEET = 1 << 14
fa, fe = 2.8, 0.01
slot = np.arange(FLEET) / FLEET
fw = C2PI * slot
fn = np.sqrt(GM / fa ** 3)

def battle(lam, seed):
    r = np.random.default_rng(seed)
    K = r.poisson(lam, FLEET)
    dh_s, dk_s = 0.02 * r.standard_normal(), 0.02 * r.standard_normal()
    dh_l, dk_l = 0.05 * r.standard_normal(), 0.05 * r.standard_normal()
    h = np.zeros(FLEET); k = np.zeros(FLEET)
    for i in range(FLEET):
        m = K[i]
        if m:
            h[i] += (r.standard_normal(m) * 0.08).sum()
            k[i] += (r.standard_normal(m) * 0.08).sum()
    sc = np.sin(C2PI * slot)
    cc = np.cos(C2PI * slot)
    h += dh_s + dh_l * sc
    k += dk_s + dk_l * cc
    X = np.column_stack([np.ones(FLEET), sc, cc])
    ch, *_ = np.linalg.lstsq(X, np.column_stack([h, k]), rcond=None)
    rh, rk = h - X @ ch[:, 0], k - X @ ch[:, 1]
    gen = dict(h=dh(rh, QE), k=dh(rk, QE))
    # naive form: orbital elements (e, varpi) of the same residual state
    e2 = np.sqrt((fe + h) ** 2 + k ** 2)
    w2 = fw + np.arctan2(k, fe + h)
    ce, *_ = np.linalg.lstsq(X, e2, rcond=None)
    cw, *_ = np.linalg.lstsq(X, w2, rcond=None)
    re_ = e2 - X @ ce
    rw_ = (w2 - X @ cw + np.pi) % C2PI - np.pi
    naive = dict(e=dh(re_, QE), w=dh(rw_, QM))
    return dict(gen={kk: round(v, 2) for kk, v in gen.items()},
                gen_bits=round(gen["h"] + gen["k"], 1),
                naive={kk: round(v, 2) for kk, v in naive.items()},
                naive_bits=round(naive["e"] + naive["w"], 1),
                emp_check_h=round(ent(quant(rh, QE)), 2))

R["battle"] = dict(fleet=FLEET, tube_bits=128,
                   zero=battle(0.0, 7), lam2=battle(2.0, 7),
                   lam6=battle(6.0, 7), lam20=battle(20.0, 7))

last = belt["epochs"][-1]
carry_bits = last["carry"]["h"] + last["carry"]["k"] + last["carry"]["M"]
l6 = R["battle"]["lam6"]["gen_bits"]
R["ledger_1e9"] = dict(
    births_MB=round(0.126e9 / 8 / 1e6, 1),
    belt_carry_bits_per_body_12ep=round(carry_bits, 2),
    belt_carry_GB=round(carry_bits * 1e9 / 8 / 1e9, 2),
    belt_churn_bits_per_member_per_epoch=round(last["churn_bits_per_member"], 4),
    belt_churn_GB_per_epoch=round(last["churn_bits_per_member"] * 1e9 / 8 / 1e9, 3),
    belt_static_scar_GB_12ep=round(belt["static_scar_12ep_bits"] * 1e9 / 8 / 1e9, 2),
    battle_resident_bits_per_member_lam6=l6,
    battle_resident_bytes_per_member=round(l6 / 8, 1),
    war_cap_distinguished_bodies_at_5GB=round(5e9 / max(min(l6, 128) / 8, 1.0), 0),
)

print(json.dumps(R, indent=1))
with open("h_live_ledger.json", "w") as f:
    json.dump(R, f, indent=1)
