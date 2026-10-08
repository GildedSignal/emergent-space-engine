# Predictions — written before the decisive record

Disclosure: code was debugged with smoke runs of F1, KICKCONVOY and KICKBELT (their numbers
appear below marked [smoke]). No other scene, no BANDS/W_SAFETY variant, and no saved record
existed when this file was written. The cone rows of the four inherited scenes are fixed by the
seed and were known from the prior run's record (f1/f2/x/b.jsonl).

The checker's named experiment: angular in-band window (|Δλ| ≤ 2.5·2·e_hi + drift margin,
range search over sorted longitudes), 0 missed on all four scenes + CONVOY + clustered Trojan
cloud; kicks judged by r8 v4 case (d)'s gates.

## P1 — CONVOY (the killer case, unrun so far)

The rank form missed 11,736/15,497 (76%) because k came from mean spacing. The angular window
is density-free: expected truth ≈ 10–20k encounters (draw sequence differs from the checker's
sampler), band **missed = 0**, pairs ≈ 30–45k vs cone's 124,750 (≈3×; the convoy's local density
is genuinely ~60× mean, so the win is bounded by cloud-width/window ≈ 0.2/0.06).

## P2 — TROJANC (clustered co-orbital cloud, unrun)

Cloud 0.3 rad, a-spread 1e-6: the cloud barely shears (dn·T ≈ 2e-4 rad). Truth ≈ 5–20k;
band missed = 0, pairs ≈ 12–25k vs 124,750 (≈5–8×).

## P3 — the four inherited scenes keep the prior run's numbers (±20%)

F1 [smoke: 1,080 pairs, 102,408 evals, 0 missed — 109× evals vs cone; the angular window is
tighter than the old k=4 ranks]. F2 maximal band (BANDS=1): ≈ 5k pairs, ≈ 450k evals, 0 missed;
formula's 2 bands: ≈ 90k pairs, ≈ 2–2.5M evals (cross-band cone dominates), 0 missed.
X: ≈ 80–95k pairs, ≈ 15–18M evals, 0 missed (≈2× vs cone, as disclosed before).
B: band ≡ cone (≈ 41.8k pairs, 813,788 evals identical), 0 missed; globalrank self-destructs
to all 499,500 in-band pairs (half-window ≥ π), 0 missed, ≈ 3.4 s.

## P4 — the window boundary is real

W_SAFETY=0.2 (window shrunk 5×) on CONVOY and F1: missed > 0 (hundreds). W_SAFETY=1: 0.

## P5 — kicks (r8 v4 case (d), both policies, [smoke] numbers already seen)

KICKCONVOY: kick_setup_ratio_median ≈ 1.0 (≤ 1.05 gate), other_certificates_touched = 0.
KICKBELT: ratio ≈ 1.0; touches ≤ ~50 per 100 kicks, and **other_added = 0** — every touch is
a removal (an early drop of a pair whose band window tightened when the kicked body left);
the strict ≤ 0 gate fails on the removals unless drops are deferred to natural expiry.

## What would falsify the fix

Any missed > 0 on any scene at W_SAFETY=1 (the window bound or its constants are wrong), or
CONVOY pairs ≈ all-pairs (the density argument is wrong and the convoy is genuinely quadratic),
or kick ratio > 1.05 (a kick cascades).
