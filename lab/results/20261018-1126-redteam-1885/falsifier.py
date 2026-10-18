#!/usr/bin/env python3
"""Premise red-team 20261018-1126: 'Aggregates are one sample each' at relativistic speed.

Target: docs/representation.md L58-59, L116.
  - L58: 'A blackbody is seen at k.T with beaming k^4, which in log form are additions.
          A type x log k table gives the sprite.'
  - L59: 'Aggregates are one sample each, and the screen caps the work at about one
          sample per pixel.'
  - L116: 'The view | <= 1 sample per pixel per frame | GPU'

Exact SR: k = 1/(gamma (1 - beta.n)) per member; bolometric seen flux = k^4 L0/N per
member (I_nu/nu^3 invariant); seen colour temperature = k T0. Truth = sum over members.

Fleet model (exact, no approximation): for members approaching along +x,
k = 1/(gamma (1-beta)) = e^phi with phi the rapidity toward the observer
(gamma (1-beta) = e^{-phi}), so a line-of-sight velocity dispersion sig_beta is a
RAPIDITY dispersion sig_phi = gamma^2 sig_beta (d phi/d beta = gamma^2) and ln k is
exactly normal: the fleet arms are lognormal by construction. The shared-log-word
readout must therefore sit at exp(-8 sig_phi^2) - 1 of the truth in EVERY arm
(per-arm analytic assertion; failure = instrument broken = VOID).

Observer arm: static crowd (all members share velocity 0) with angular extent; the
PLAYER moves at beta_O. k_i = 1/(gamma_O (1 - beta_O cos theta_i)).

Readouts modelled after the letter: one sampled member carries the aggregate's sprite
(brightness = N x sample flux, colour = sample k); the shared-log-word reading carries
one log k for the aggregate (geometric mean: 'log form are additions').

All randomness: numpy PCG64, fixed seeds, full-entropy draws. Runtime ~3 s.
"""
import json
import zlib
import numpy as np

N = 1_000_000          # members per crowd
DRAWS = 10_000         # one-sample draws per arm (frame samples)
FRAMES = 600           # strobe time series length (median over 599 jumps)
OUT = {}
VOID = []


def arm(name, k, s_analytic=None):
    k = np.asarray(k, dtype=np.float64)
    lnk = np.log(k)
    truth_per_member = k ** 4                      # exact bolometric beaming
    mean_flux = truth_per_member.mean()            # truth total = N * this
    # ---- letter readouts ----
    # (a) one sample each: brightness ratio = k_s^4 / mean(k^4)
    rng = np.random.default_rng(zlib.crc32(name.encode()) % 2**32)
    s = rng.integers(0, len(k), size=DRAWS)
    ratio = truth_per_member[s] / mean_flux
    onesample_med = float(np.median(np.abs(ratio - 1.0)))
    onesample_p90 = float(np.quantile(np.abs(ratio - 1.0), 0.90))
    # (b) shared log word (geometric mean, 'log form are additions')
    logword_bias = float(np.exp(4.0 * lnk.mean()) / mean_flux - 1.0)
    # per-arm analytic control for exactly-lognormal arms
    analytic_bias = float(np.exp(-8.0 * s_analytic ** 2) - 1.0) if s_analytic else None
    if analytic_bias is not None:
        err = abs(logword_bias - analytic_bias)
        if err > 0.02:
            VOID.append((name, logword_bias, analytic_bias, err))
    # (c) strobe: per-frame deterministic sample swap (the traversal re-draws each frame)
    st = rng.integers(0, len(k), size=FRAMES)
    flux_series = truth_per_member[st]
    jumps = np.abs(np.diff(np.log(flux_series)))
    strobe_med = float(np.median(jumps))
    strobe_p90 = float(np.quantile(jumps, 0.90))
    strobe_visible = float(np.mean(jumps > np.log(1.02)))   # >2% contrast steps
    strobe_glaring = float(np.mean(jumps > np.log(1.10)))   # >10% steps
    # integrated-total flicker with P pixels sampling independently
    tot_flick = {}
    for P in (100, 1000):
        idx = rng.integers(0, len(k), size=(FRAMES, P))
        tot = truth_per_member[idx].mean(axis=1) * P
        tot_flick[P] = float(np.median(np.abs(np.diff(np.log(tot)))))
    # (d) tails: fraction of total seen flux in the top members
    f = np.sort(truth_per_member)[::-1]
    csum = np.cumsum(f)
    total = csum[-1]
    tail1 = float(csum[N // 100 - 1] / total)        # top 1% of members
    tail01 = float(csum[N // 1000 - 1] / total)      # top 0.1% of members
    # (e) colour: sample k vs flux-weighted true colour k_F = sum k^5 / sum k^4
    kF = float((k ** 5).sum() / (k ** 4).sum())
    col_med = float(np.median(np.abs(k[s] / kF - 1.0)))
    col_p90 = float(np.quantile(np.abs(k[s] / kF - 1.0), 0.90))
    # (f) cost corollary: samples for 5% and 2% bars at this CV
    cv = float(truth_per_member.std() / truth_per_member.mean())
    n5 = int(np.ceil((cv / 0.05) ** 2))
    n2 = int(np.ceil((cv / 0.02) ** 2))
    OUT[name] = dict(
        sig_lnk=float(lnk.std()), mean_k=float(k.mean()),
        onesample_med=onesample_med, onesample_p90=onesample_p90,
        logword_bias=logword_bias, analytic_bias=analytic_bias,
        strobe_med=strobe_med, strobe_p90=strobe_p90,
        strobe_visible_frac=strobe_visible, strobe_glaring_frac=strobe_glaring,
        total_flicker_P100=tot_flick[100], total_flicker_P1000=tot_flick[1000],
        tail_top1pct=tail1, tail_top0p1pct=tail01,
        colour_med=col_med, colour_p90=col_p90,
        cv_k4=cv, samples_for_5pct=n5, samples_for_2pct=n2,
    )


def fleet(beta_bulk, sig_beta, seed):
    """Exact rapidity model, see module docstring."""
    gamma2 = 1.0 / (1.0 - beta_bulk ** 2)
    phi_bulk = np.arctanh(beta_bulk)
    sig_phi = gamma2 * sig_beta
    rng = np.random.default_rng(seed)
    phi = phi_bulk + sig_phi * rng.standard_normal(N)
    return np.exp(phi), sig_phi


def crowd_static_observer_moving(beta_obs, theta_center, sig_theta, seed):
    rng = np.random.default_rng(seed)
    theta = theta_center + sig_theta * rng.standard_normal(N)
    gamma = 1.0 / np.sqrt(1.0 - beta_obs ** 2)
    return 1.0 / (gamma * (1.0 - beta_obs * np.cos(theta)))


# ============ controls ============
# 1. instrument control: exact lognormal, MC must match the closed form per arm
rng = np.random.default_rng(20261018)
for s_ in (0.10, 0.30):
    mu = 1.0
    k = np.exp(mu + s_ * rng.standard_normal(N))
    arm(f"CONTROL lognormal s={s_:.2f}", k, s_analytic=s_)
    r = OUT[f"CONTROL lognormal s={s_:.2f}"]
    print(f"[control] s={s_}: logword bias {r['logword_bias']:+.4f} "
          f"vs analytic exp(-8s^2)-1 {r['analytic_bias']:+.4f}")

# 2. Newtonian negative: the k=1 readout at beta 0.9 head-on misses beaming entirely
k, _ = fleet(0.9, 0.05, seed=7)
OUT["CONTROL newtonian"] = dict(
    truth_over_newton=float((k ** 4).mean()),
    note="k=1 sprite vs exact mean(k^4) at beta 0.9, sig_beta 0.05 "
         "(sigma_phi 0.263): the instrument sees beaming",
)
print(f"[control] Newtonian readout under-reports the beta 0.9 fleet by "
      f"{OUT['CONTROL newtonian']['truth_over_newton']:.0f}x")

# ============ main sweep: fleet crowds (approach, unresolved) ============
# (beta_bulk, sig_beta, seed); sig_phi = gamma^2 sig_beta computed exactly
grid = [
    (0.10, 0.001, 101), (0.10, 0.05, 102),
    (0.50, 0.001, 103), (0.50, 0.05, 104),
    (0.90, 0.001, 105), (0.90, 0.01, 106), (0.90, 0.03, 107), (0.90, 0.05, 108),
    (0.99, 0.001, 109), (0.99, 0.005, 110), (0.99, 0.01, 111),
    (1e-5, 1e-5, 112),   # the shipped belt's regime (conjunction speeds ~ 1e-5 c)
]
for beta_bulk, sig, seed in grid:
    k, sig_phi = fleet(beta_bulk, sig, seed)
    arm(f"fleet beta={beta_bulk:g} sig={sig:g} (sphi={sig_phi:.3f})", k, s_analytic=sig_phi)

# ============ observer arm: player at beta_O, static crowd with angular extent ============
obs_grid = [
    (0.5, np.pi / 2, 0.05, 201), (0.9, np.pi / 2, 0.05, 202),
    (0.9, np.pi / 2, 0.2, 203), (0.99, np.pi / 2, 0.05, 204),
    (0.9, 0.0, 0.05, 205),
]
for betaO, thc, sth, seed in obs_grid:
    k = crowd_static_observer_moving(betaO, thc, sth, seed)
    arm(f"observer betaO={betaO:g} th={thc:.2f} sth={sth:g}", k)

with open("results.json", "w") as f:
    json.dump(OUT, f, indent=1)

hdr = (f"{'arm':48s} {'s_lnk':>6s} {'1smp med':>8s} {'logword':>8s} "
       f"{'strb med':>8s} {'strb>2%':>7s} {'tail1%':>7s} {'n@5%':>7s} {'colour':>7s}")
print("\n" + hdr)
print("-" * len(hdr))
for name, r in OUT.items():
    if name.startswith(("CONTROL lognormal", "fleet", "observer")):
        print(f"{name:48s} {r['sig_lnk']:6.3f} {r['onesample_med']:8.3f} "
              f"{r['logword_bias']:+8.3f} {r['strobe_med']:8.3f} "
              f"{r['strobe_visible_frac']:7.2f} {r['tail_top1pct']:7.3f} "
              f"{r['samples_for_5pct']:7d} {r['colour_med']:7.3f}")

print(f"\ntotal-flicker (median |d ln F| per frame, P pixels), flagship rows:")
for name, r in OUT.items():
    if name.startswith("fleet") and r["sig_lnk"] > 0.2:
        print(f"  {name}: P100 {r['total_flicker_P100']:.3f}  "
              f"P1000 {r['total_flicker_P1000']:.3f}  tail0.1% {r['tail_top0p1pct']:.3f}  "
              f"colour_p90 {r['colour_p90']:.3f}")

if VOID:
    print("\nVOID: per-arm analytic control failed:", VOID)
else:
    print("\nAll per-arm analytic controls pass (logword = exp(-8 s^2)-1 within 0.02).")
