#!/usr/bin/env python3
"""H_live probe: canonical distinctions (quantized (E,L) key changes) per body
per orbit and per second, for a quiescent belt vs a short-period population.
Law context (docs/law.md): the tube stores quantized (E,L) in 32 bits (memo key);
kicks are integers of the law; scars are the sparse difference from a program.
Units: AU, yr, Msun, G = 4*pi^2. Floats explore; all *decided* numbers are
integer bin-change counts."""
import numpy as np

rng = np.random.default_rng(20261007)
G = 4 * np.pi**2

# ---------- belt ----------
N = 20000
a = rng.uniform(2.2, 3.2, N)
e0 = np.minimum(rng.rayleigh(0.07, N), 0.30)
varpi0 = rng.uniform(0, 2 * np.pi, N)
# Jupiter
muJ = 9.5458e-4
aJ = 5.2
eJ = 0.0489
varpiJ = 0.0

n = np.sqrt(G / a**3)
# Laplace-Lagrange coefficients (exact series sum) for alpha = a/aJ < 1
alpha = a / aJ


def b32(k, al, terms=60):
    s = np.zeros_like(al)
    for j in range(terms):
        c = 1.0
        for m in range(j + k):
            c = c * (2 * k + m) / (m + 1)
        s = s + c * al**j  # al^(j) * C(2k+j-1, j) form: use standard 2F1 series
    return s


def b32_exact(k, al, terms=80):
    # b_{3/2}^{(k)}(alpha) = sum_j C(2k+j-1, j) * C(2k+2j-1, j+... use 2F1:
    # b = (2/pi) * _2F1(k+1/2, k+3/2; 1; al^2) * ... standard: b_{s}^{(m)} = (2/pi)*
    # int_0^pi cos(m psi) dpsi/(1-2 al cos psi + al^2)^s ; evaluate numerically instead.
    psi = np.linspace(0, np.pi, 4001)
    cs = np.cos(k * psi)
    den = 1 - 2 * al[:, None] * np.cos(psi) + al[:, None] ** 2
    val = np.trapz(cs / den**1.5, psi, axis=1) * 2 / np.pi
    return val


b1 = b32_exact(1, alpha)
b2 = b32_exact(2, alpha)
Ajj = (n / 4) * muJ * alpha * b1
Ajk = (n / 4) * muJ * alpha * b2
kf_abs = Ajk * eJ / Ajj  # forced eccentricity magnitude
kf_ang = varpiJ + np.pi  # sign: k_f = -(Ajk/Ajj) k_J

# analytic small-alpha check (positive control)
kf_pred = (5.0 / 4.0) * alpha * eJ
ctrl_LL = np.max(np.abs(kf_abs - kf_pred) / kf_pred)

# secular e(t): |k_f + (k0-kf) e^{i A t}|; sample 2,000 yr at 200 points
T = 2000.0
ts = np.linspace(0, T, 200)
k0 = e0 * np.exp(1j * varpi0)
kf = kf_abs * np.exp(1j * kf_ang)
A = Ajj[:, None]
e_t = np.abs(kf[:, None] + (k0 - kf)[:, None] * np.exp(1j * A * ts[None, :]))

# L = sqrt(G a (1-e^2)) (h, scaled): L/L_ref over the grid
Lgrid = lambda ee, aa: np.sqrt(aa * (1 - ee**2))


def quant(path_e, bits_L):
    L = Lgrid(path_e, a[:, None])
    Lmin, Lmax = 2.2 * np.sqrt(1 - 0.30**2) * 0.99, 3.2 * 1.01
    iL = np.floor((L - Lmin) / (Lmax - Lmin) * 2**bits_L).astype(np.int64)
    d = np.diff(iL, axis=1)
    changes = np.count_nonzero(d)
    per_body_orbit = changes / N / (T / (2 * np.pi / np.sqrt(G / a**3).mean()))
    return per_body_orbit, d[d != 0]


def bits_of(deltas):
    if deltas.size == 0:
        return 0.0
    vals, cnt = np.unique(deltas, return_counts=True)
    p = cnt / cnt.sum()
    return float(-(p * np.log2(p)).sum())


def entropy_rate(events_per_orbit, deltas):
    r = min(events_per_orbit, 1.0)  # events per orbit as change probability proxy
    # canonical rate: h(r) + r*H(step) per orbit (r as fraction of orbits changed)
    h = 0.0 if r <= 0 or r >= 1 else -(r * np.log2(r) + (1 - r) * np.log2(1 - r))
    return h + r * bits_of(deltas)


print("== control: LL forced-e vs asymptotic (5/4)*alpha*eJ ==", f"{ctrl_LL:.4f} (expect ~0.05 at alpha~0.5: higher-order alpha terms)")
for bits_L, tag in ((16, "16+16"), (8, "8+8")):
    rate_L, dL = quant(e_t, bits_L)
    print(f"belt secular L-key changes/orbit/body [{tag}]: {rate_L:.3e}; step entropy {bits_of(dL):.2f} bits")

# ---------- synodic scattering impulses (E-key random walk, Kac crossing rate) ----------
nJ = np.sqrt(G / aJ**3)
syn = 1.0 / np.abs(1.0 / (2 * np.pi / n) - 1.0 / (2 * np.pi / nJ))  # synodic period, yr
conj_per_orbit = (2 * np.pi / n) / syn
b_min = aJ * (1 - eJ) - a * (1 + e0)  # closest approach at conjunction
vrel = np.sqrt(G / a + G / aJ - 2 * np.sqrt(G / a * G / aJ))  # circular-speed difference vector approx
dv = 2 * G * muJ / (b_min * vrel)  # impulse per conjunction (AU/yr)
vcirc = np.sqrt(G / a)
frac_dv = dv / vcirc
# per-conjunction fractional E step ~ 2*dv_t/v with random sign; use |Dv|/v with tangential half
step_dE = 2 * 0.5 * frac_dv  # E fractional step sigma (order)
Ewidth = (G / 2) * (1.0 / 2.0 - 1.0 / 3.2)  # |E(2.0)-E(3.2)| with E=-G/(2a), positive
step_bins_16 = step_dE * (G / (2 * a)) / (Ewidth / 2**16)  # per-conjunction |dE| in 16-bit bins
naive = (conj_per_orbit * step_bins_16 * np.sqrt(2 / np.pi)).mean()
# tide truncation: a two-body encounter resolves only inside the tidal radius;
# beyond it the exchange is secular (already in the LL term), not diffusive.
b_tide = a * (muJ / 3) ** (1.0 / 3.0)
resolved = b_min < b_tide
crossings_per_orbit = np.where(resolved, conj_per_orbit * step_bins_16 * np.sqrt(2 / np.pi), 0.0).mean()
print(f"belt E-key: conjunctions/orbit {conj_per_orbit.mean():.3f}; min conjunction gap {b_min.min():.2f} AU vs tidal radius ~{b_tide.mean():.2f} AU; resolved-encounter bodies: {int(resolved.sum())}")
print(f"belt E-key naive uncapped impulse would claim {naive:.0f} bins/orbit: artifact of the two-body formula beyond the tidal radius")

# ---------- leak control: muJ=0 ----------
e_t0 = np.repeat(e0[:, None], 200, axis=1)
r0, d0 = quant(e_t0, 16)
print("== control: muJ=0 L-key changes (must be 0.0):", r0, "==")

# ---------- assembly ----------
r_orbit_16, dL16 = quant(e_t, 16)
r_orbit_8, dL8 = quant(e_t, 8)
E_orbit_16 = crossings_per_orbit
tot16 = r_orbit_16 + E_orbit_16  # generator-absent accounting: L-cycling counts as key changes
tot8 = r_orbit_8 + E_orbit_16  # E stays 0; only L-grid coarsens
P_belt = 2 * np.pi / np.sqrt(G / 2.7**3)  # yr
P_belt_s = P_belt * 3.156e7
print(f"\nBELT total key-change events/orbit/body: 16+16: {tot16:.3e}  8+8: {tot8:.3e}")
bits_orbit = entropy_rate(min(tot16, 1), dL16)
print(f"bits/orbit/body (16+16, h(r)+rH(step)): {bits_orbit:.3f}")
print(f"bits/s/body: {bits_orbit / P_belt_s:.3e}")

# ---------- hot population (parameterized; labeled estimate) ----------
P_hot = 5.8e3  # s, LEO-scale orbit
for kappa in (0.1, 1.0, 4.0):
    bps = kappa * 1.5 / P_hot  # ~1.5 bits per event
    print(f"HOT kappa={kappa}/orbit: {bps:.3e} bits/s/body; x1e6 bodies = {bps*1e6/8:.1f} B/s")

# ---------- budget arithmetic (derived, printed) ----------
print("\n== derived budget arithmetic ==")
one_hr_sim = 3600 * 100          # one play-hour at RTF 100 (sim seconds)
hundred_hr = 100 * one_hr_sim
belt_bps = bits_orbit / P_belt_s
print(f"1e9 belt bodies: {belt_bps*1e9/8:.3e} B/s -> {belt_bps*1e9*hundred_hr/8/1e9:.3e} GB per 100 play-hr (RTF100)")
for f in (1e-6, 1e-5, 1e-4, 1e-3):
    hot_bps = f * 1e9 * 1.0 * 1.5 / P_hot
    print(f"f_hot={f:.0e} (kappa=1): {hot_bps/8:.3e} B/s -> {hot_bps*hundred_hr/8/1e9:.2f} GB per 100 play-hr")
