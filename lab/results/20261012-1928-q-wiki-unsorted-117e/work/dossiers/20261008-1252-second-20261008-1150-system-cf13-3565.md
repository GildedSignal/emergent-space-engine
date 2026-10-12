# Dossier — the angular window makes the unified certificate exact on clustered phases

**Run:** 20261008-1252-second-20261008-1150-system-cf13-3565 · second author on 20261008-1150-system-cf13 · 8 October 2026

## Claim

With the checker's named fix — the in-band rank count from **mean** spacing replaced by an
**angular** window (|Δλ| ≤ 2.5·2·e_hi + drift margin, materialized by range search over the
sorted longitudes, so cost = window × **local** density) — the unified certificate (in-band
window + cross-band cone, band width from the drift bound, no trigger) is exact on all four
original scenes **and** on the convoy that killed it (0 missed, was 76% missed) and on a
clustered Trojan cloud, keeps every cost number of the original run (F1 109× evals, better than
the original's 59.7×), and passes r8 v4 case (d)'s kick gates: setup ratio ≈ 1, zero other-body
certificates **added** (the 44/100 belt touches are early drops, not work).

## Bottleneck

The board's top scaling risk: candidate work must track real encounters. The original run's
unification (one certificate instead of three) was sound except that k = angular window / mean
spacing silently assumed uniform longitude density — false exactly in the regime the certificate
exists for (formations, convoys, Trojan clouds). This run completes it: the fix is one scale,
nothing else changes.

## Evidence

Cone rows of the four inherited scenes reproduce the original record bit-for-bit (same seed:
F1 124,750 pairs / 11,197,808 evals; F2 179,700 / 15,530,779; X 124,750 / 34,857,427;
B 42,219 / 813,788). Truth: the crate's conservative advancement, no shared solver. All
commands ≤ 41 s here (6 threads, < 2 GB):

| scene (N, ρ, orbits) | truth enc | cone: pairs / evals / ms | band: pairs / evals / ms | missed | evals cut |
|---|---|---|---|---|---|
| F1 fleet | 275 | 124,750 / 11,197,808 / 709 | 1,080 / 102,408 / 12 | **0** | 109× |
| **CONVOY** (F1's a/e, λ in 0.1 rad) | 10,987 | 124,750 / 42,109,381 / 2,465 | 44,977 / 15,681,974 / 929 | **0** | 2.7× |
| **TROJANC** (cloud 0.3 rad, Δa 1e-6) | 9,950 | 124,750 / 55,126,809 / 3,252 | 14,821 / 7,339,409 / 450 | **0** | 7.5× |
| F2 swarm, maximal band | 676 | 179,700 / 15,530,779 / 988 | 4,102 / 372,380 / 33 | **0** | 41.7× |
| F2 swarm, formula's 2 bands | 676 | " | 54,501 / 2,369,658 / 184 | **0** | 6.6× |
| X crossing fleets | 2,279 | 124,750 / 34,857,427 / 2,825 | 88,894 / 16,489,393 / 1,366 | **0** | 2.1× |
| B belt | 203 | 42,219 / 813,788 / 81 | 39,679 / 808,884 / 82 | **0** | 1.0× |

False positives: 0 everywhere; exact checks identical per scene (318/863/4,439/227… — the
certificate changes which pairs are materialized, never how a pair is judged). The convoy's
modest 2.7× is the honest number: its local density is ~60× the mean, and 10,987 of 124,750
pairs (8.8%) genuinely meet — candidate work tracks local phase density, which is information,
not waste. The original scenes keep or improve their numbers (the angular window is also
tighter than the old rank margin: F1 1,080 pairs vs 2,000).

- **Self-destruction still rules the tier:** globalrank on B (one band over everything) →
  half-window 4.65 ≥ π → all 499,500 in-band pairs, 0 missed; on the banded form B stays at the
  cone's cost (808,884 vs 813,788 evals). The tier choice remains the drift bound's own
  self-destruction, not a trigger.
- **Boundary is real:** window safety ×0.2 → missed 1/10,987 on CONVOY and 9/275 on F1; ×0.5 →
  0 missed; ×1.0 (the derived constant, unchanged) → 0 everywhere.
- **Kicks (r8 v4 case (d), 100 kicks, δa/a ≈ 1e-3, N=10⁴ belt and N=500 convoy):**
  kick_setup_ratio median 0.9985 (belt) / 0.9968 (convoy), max ≤ 0.9994 — gate ≤ 1.05 passes.
  Other certificates touched: convoy 0; belt 44 per 100 kicks, **all removals** (added = 0):
  the band's shared dn/e_hi tighten when the kicked body leaves, dropping pairs early — an
  optimization a real implementation defers to natural expiry, not recomputation. With the
  strict "exit" policy (any kick demotes to the cone tier) the same holds (45 drops, 0 added);
  the fit policy keeps 36/100 bodies in tier. The kick-side design consequence: a kicked body
  whose n leaves its band's geometric envelope (1.5·w·u^2.5) exits the phase tier and the cone
  carries it — one kick then perturbs no other body's drift bound.

Reproduce (`scenes.jsonl`, `boundary.jsonl` beside this dossier; each line ≤ 41 s):

```
cd lab/results/20261008-1252-second-20261008-1150-system-cf13-3565/exp
cargo build --release                       # CARGO_TARGET_DIR=/home/glmlab/lab-target-2 here
<target>/release/exp F1                     # also CONVOY | TROJANC | F2 | X | B
BANDS=1 <target>/release/exp F2             # maximal-band rule
W_SAFETY=0.2 <target>/release/exp CONVOY    # boundary (also 0.5, and on F1)
<target>/release/exp KICKBELT               # r8 v4 (d): also KICKCONVOY, KICK_POLICY=exit
```

## Predictions

`predictions.md` predates the record; it discloses the three debugging smoke runs (F1, both kick
scenes) whose numbers it marks. P1 held (convoy 0 missed; pairs 44,977 just inside the predicted
30–45k). P2 held (Trojan cloud 0 missed, 14,821 pairs, 8.4×). P3 held (every scene within the
±20% bands; F1 109×, F2-maximal 41.7× vs predicted ~450k evals → 372k). P4 held in direction,
overshot in magnitude (misses at ×0.2 safety: 1 and 9, not hundreds — the window bound degrades
gracefully). P5 held exactly (ratios ≈ 1, convoy 0 touches, belt 44 pure removals, added = 0).

## What would make it wrong

- **Eccentric swarms:** window ∝ e_hi; at e ≈ 0.2 (X) the in-band tier already pays near-cone
  cost (2.1×). A hot swarm (e → O(1)) makes the tier all-pairs: exactness survives, the win
  dies, the cone carries — same disclosure as the original.
- **The kick measurement is bookkeeping, not dynamics:** it measures certificate work per kick,
  not completeness under piecewise elements (r8 v4's (d) gates are work gates; its
  missed_fraction belongs to case (a), which the scenes above cover with fixed elements).
  A run with true mid-run element changes and truth re-integration is the next rung.
- **Removal-touches:** the belt's 44 early drops violate a literal reading of
  `other_certificates_touched ≤ 0`; the honest fix (defer drops to natural expiry) is policy,
  not measured here as a running system.
- Truth stays the crate's Newtonian Kepler; precession (relativistic dolls) enters as extra dn,
  absorbed by the drift bound — unmeasured, as in the original.

## Cost of adoption, and fit

Same as the original (a U-sorted index with per-band λ order, renewals, and now per-band λ range
search instead of rank arithmetic), plus the kick rule: tier exit on envelope violation. One
scale was replaced; the unification's shape, the drift-bound tier selection and the cost numbers
all survive, exactly as the checker predicted. Fit — PRINCIPLES 19: "if you find yourself fixing
things that's oftentimes a signal that it is the wrong representation" — the rank count was the
wrong representation of the window, and the angular window is the one the geometry itself
states (|Δλ| ≤ 2(e_i+e_j) at a meeting); PRINCIPLES 32 ("under the right representation many
symmetries can appear"): the same range search serves uniform and clustered phases, the density
does the work; PRINCIPLES 33: the band resolves only what matters at its scale, and the convoy
pays its own true density. Text cost: this corrects the record of 20261008-1150-system-cf13; the
silver's numbers stand, its in-band scale does not.

## The lens

The second-author lens made me execute the checker's experiment rather than re-derive it; what it
may have made me miss: the kick experiment measures certificate bookkeeping under an idealized
kick policy, not the plane's real kick cadence (the skin's amortization on top of bands is still
unmeasured), and the convoy's 2.7× — not 60× — is the honest headline for clustered phases, which
the board should weigh before adopting the phase tier as the formation's sole answer. Linux/x86
shared with other runs: orders of magnitude only; the integrator re-measures on the M1.
