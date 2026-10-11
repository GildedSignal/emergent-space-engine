# Dossier: run 20261010-2314-second-20261010-2141-dynamics-cd52-f2e3 (lens: second author)

**Claim (one sentence):** The silver's record now regenerates from shipped code and its
checker-named experiment is run, and it splits the original claim: **no clean fixed-cadence
operating point stands and strengthens** (μ=1e-4: every cadence 8–256 corrupts, fb up to
2.2e6, and the E1 "truth base" cad256 is itself corrupted; μ=1e-5: some seed of nearly every
cell corrupts at every cadence 64–1024, with fallback medians *rising* with refinement
(0 → 4e4 → 1.3e5 at N=200); N=800 (K=0.062) fails the strict conjunction gate at every
cadence), but the **"λ ≈ 2–14/orbit is manufactured chaos" mechanism is refuted**: λ_exp is
dt-robust or *rising* under 16× step refinement at every μ and N (ratios s1024/s64 = 1.14,
1.38, 1.56 at N = 50, 200, 800; 1.11 and 1.23 at μ = 1e-6, 1e-7), and λ/Ω is monotone in the
density K = Δa/R_H (0.12, 0.23, 0.29, 0.47, 0.70 at K = 0.72, 0.335, 0.39, 0.155, 0.062,
spon 64), crossing the Wisdom–Tremaine level ≈ 0.5Ω near K ≈ 0.15 — so λ_max ~ 0.1–1 Ω is the
belt's **real** surprise floor (H_live's physical floor, set by K, not by the step), the
surprise instrument is valid without the changeover wherever the conjunction gate passes,
and the changeover's domain is K ≲ 0.1 (at game N, belts are always Hill-dense: K ~ 10⁻³).

## What the checker named, and what I did

1. **"results.json cannot be regenerated"** — shipped fit.py matched log labels to the
   *buggy-matrix* curves (`curves/{label}_s{seed}.dat`) while matrix2.sh writes `r_`-prefixed
   corrected curves; its law/λ_exp fitted pre-fix curves while λ_raw/dH/fb came from corrected
   runs; cad128 had no curve (null).
   → `fit2.py` fits **only** corrected curves (shipped `r_*` plus this run's `r2_cad64/r2_cad256`
   reruns), fit math unchanged, and writes `results2.json`: all 11 matrix2 labels fit with both
   seeds, `law=exp` everywhere at μ ≥ 1e-5, λ_exp 2.05–16.74, dH 0.16–33, fb 4.5e4–2.2e6
   (seed-level; medians 8.2e4–2.0e6).
2. **A second, undisclosed record bug (found here):** the shipped fit.py float pattern
   `[\d.e-]+` (no `+`) silently dropped **every log row with dH ≥ 1** (`3.307e+01`) — exactly
   the corrupted rows the claim is about; the shipped results.json was a table of clean seed-2
   rows only (5 of 11 labels, E1/E2 absent). Fixed in fit2.py; corrected E2 on shipped curves:
   **α = 0.821 (R² 0.799)**.
3. **E1's missing corrected truth base:** reran cad64 and cad256 (N=200, μ=1e-4, 200 orbits,
   2 seeds). cad64 is bit-identical to matrix2's n200 rows (same cell) — cross-run
   bit-reproducibility re-verified. Corrected E1 (ratios to cad256): 8→0.12, 32→0.53,
   64→0.51, 128→0.29, 256→1.00 — non-monotone, and the base itself is corrupted (λ_exp 16.7,
   fb 2.0e6): **no cadence is a truth at μ=1e-4**; E1's ratios are corruption-vs-corruption,
   which is the finding.
4. **The one experiment for gold:** dt×N×μ scan of λ_max at μ ≤ 1e-5 — spon {64,256,1024} ×
   N {50,200,800} at μ=1e-5 (N=800 at T=25, licensed below), μ {1e-6,1e-7} × spon {64,1024} at
   N=200, 3 seeds each, 50 orbits, every run with a **conjunction census** (per-pair minimum
   sampled separation; gates b < √(m·dt) and b < (m·dt²)^⅓; `belt2.c` = shipped
   `belt_lyap.c` + census behind `--conj`, dynamics byte-identical — all five anchors
   reproduce matrix2_raw.log and wm5 bit-exactly, curve files included).

## Evidence

Regenerate: `gcc -O3 -fopenmp -o belt2 belt2.c -lm` (selftest 1.6e-11/1.0e-10 as shipped);
`./block_light.sh; ./block_light2.sh; ./block_heavy.sh; ./block_heavy2.sh` (logs
`light_raw.log`, `light2_raw.log`, `heavy_raw.log`, `heavy2_raw.log`); `python3 analyze.py`
(matrix tables + prediction tests, saved in `analysis.txt`); `python3 fit2.py` (record).

**dt-axis (manufactured λ must collapse under refinement; real λ must not):**

| cell | K | λ_exp s64 | s256 | s1024 | ratio |
|---|---|---|---|---|---|
| N=50, μ=1e-5, T=50 | 0.391 | 1.82 | 1.79 | 2.07 | 1.14 |
| N=200, μ=1e-5, T=50 | 0.155 | 2.97 | 3.40 | 4.09 | 1.38 |
| N=800, μ=1e-5, T=25 | 0.062 | 4.39 | 5.73 | 6.86 | 1.56 |
| N=200, μ=1e-6, T=50 | 0.335 | 1.42 | — | 1.57 | 1.11 |
| N=200, μ=1e-7, T=50 | 0.721 | 0.73 | — | 0.90 | 1.23 |

No cell collapses; λ *rises* with refinement — the coarse step underestimates real chaos.
Horizon check: λ(T=25)/λ(T=50) = 0.87 (s64), 0.96 (s1024) at N=200. Clean-seed corroboration:
fb=0 seeds at N=200 fit 2.99/2.97 (s64, T=50) and 2.67/2.35 (s64, T=25) vs 3.79/3.92
(s1024, T=25, fb=0) — the rise is not fb-driven; where seeds split (n50_s1024: 1.66/2.07
clean vs 4.00 with fb=8e4 and a census-flagged sub-√(m·dt) dip) the census explains the
outlier and the median is robust.

**K-axis:** λ/Ω monotone in K at fixed spon (above), crossing ≈ 0.5Ω near K ≈ 0.15 — the
Wisdom–Tremaine dense-ring level appears as a mid-family value, not a universal constant.
At fixed N=200, λ ∝ μ^0.30–0.33 along μ ∈ {1e-5,1e-6,1e-7}: that axis moves K sparse-ward
(K: 0.155→0.335→0.72), and WT mass-insensitivity applies at fixed K, not fixed N —
real-scattering-consistent, and manufactured-inconsistent (every μ is dt-robust).

**Admission gate vs fallback counter:** the census separates what fb conflates. μ=1e-4:
n_sqrt = 5–15 pairs below √(m·dt), n_kill3 ~ 300–450 — fails everywhere. μ=1e-5, N ≤ 200:
n_sqrt = 0–2 (borderline; the (m·dt²)^⅓ gate flags 3–87 pairs — the stricter criterion is
the honest one at these widths). N=800: fails at every cadence — min sampled pair distance
1.3–4.6e-6 « √(m·dt) = 8.8e-6 at s1024, and at s64/s256 the (m·dt²)^⅓ radius *exceeds the
mean spacing* (1.25e-4): **K ≲ 0.1 is unrepresentable at any fixed step** — a dimensionless
trigger for the changeover/encounter tier (the silver's at-scale conclusion, now with a
number). Fallback blindness: fb medians grow with cadence (N=200, μ=1e-5: 0 → 3.8e4 → 1.3e5);
coarse-cadence cleanliness is manufactured blindness to real ejections.

## Predictions (predictions.md, written before the decisive matrix)

- P1 anchors bit-exact: HELD (all five, curve files included).
- P2 dt-robustness band [0.75,1.30]: FAILED *upward* (1.11–1.56). The decision it was written
  to make is unambiguous: manufactured-collapse (fall ≥ 30%) is excluded at every cell.
- P3 λ/Ω ∈ [0.35,0.55] on strictly gate-passing cells: FAILED as a universal — gate-passing
  cells span 0.14–0.62 (0.5Ω sits inside, near K≈0.15); the family including gate-border
  cells spans 0.12–1.09, monotone in K.
- P4 μ-insensitivity at fixed N ≥ 0.6: FAILED (0.38–0.48) — λ ∝ μ^≈0.3, the fixed-N axis
  moves K; consistent with real scattering at varying K, not with manufacture (dt-robust at
  both μ).
- P5 N-flatness: FAILED as stated — λ rises with density; the monotone K-ordering is the
  finding P5 should have been.
- P6 gate separates regimes: HELD (μ=1e-4 everywhere and N=800 at every cadence fail;
  μ ≤ 1e-5, N ≤ 200 pass or border on √(m·dt); (m·dt²)^⅓ is the discriminating radius).
- P7 fallback blindness: HELD (fb medians 0 → 3.8e4 → 1.3e5 with cadence; 8 of 9 μ=1e-5
  families have some fb>0 seed).
- P8 horizon ±15%: HELD (0.87 / 0.96).

## What would make it wrong

Float toy of the law's structure; orders of magnitude only (cloud timing caveat). λ_exp tail
fits on late-corrupting runs could inflate — per-seed checks show fb>0 seeds fit the same λ
as clean twins at μ≤1e-5 horizons, but at μ=1e-4 the λ_exp values remain corruption-dominated
(that is the claim there). Census samples separations at kick instants: between-step dips are
missed, so n_sqrt compared *across* cadence carries a detector bias (finer sampling catches
more dips) — the dt-axis, not the census, is the load-bearing discriminator. No exponent
spectrum/KS entropy (inherited). The μ-at-fixed-N axis conflates m and K; a purer WT test
would vary μ at fixed K (widen the belt) — not run, named for the next rung.

## Cost of adopting

`belt2.c`'s census (~free: one compare per pair per kick) plus the two gate radii
(√(m·dt), (m·dt²)^⅓) as the belt's admission gate in `xtask universe --bench`; K = Δa/R_H
as the dimensionless trigger choosing fixed-cadence cheap path vs changeover; scar cadence
from λ_max(K) ≈ 0.1–1 Ω.

## Fit with PRINCIPLES

"Regimes are chosen by dimensionless numbers" (4): K selects the regime and the representation
boundary. "Compute only surprises" (3): the surprise floor is real and set by K — the belt
program's scar cadence follows the physics, not the integrator's budget. "The simulation tells
us what's next not us" (22): refining the step *increases* measured surprise; the step cannot
legislate the physics. "A failed expectation is not automatically a failed method" (H0183):
P2's band failed upward and thereby decided the question.

## The lens

Second-author lens: I inherited the checker's dt-vs-K frame and it decided cleanly; what I
added beyond it (μ-axis at fixed N) conflates m and K and its "failure" (P4) is a design
artifact worth not repeating. I did not quantify the census detector bias. The e+ regex bug
is the memo-artifact lesson a third time: author and checker shared fit.py's regex, so two
"independent" readings agreed on a silently truncated record — the record's parse is part of
the instrument, and it had never been checked against the log it claimed to summarize.
