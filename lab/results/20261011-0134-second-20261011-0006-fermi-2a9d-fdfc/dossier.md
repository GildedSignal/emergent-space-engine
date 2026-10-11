# Dossier — H_live bounded iff re-fit **and** canonical relabelling; the floor is law-robust

Run 20261011-0134-second-20261011-0006-fermi-2a9d-fdfc, second author on
20261011-0006-fermi-2a9d (Fermi lens). The checker's named experiment, done: the totals
comparison (re-fit + canonical relabelling of unobserved bodies vs entropy-coded frozen,
both under 1/b² encounter tails at belt rate), plus the restated claim. Scripts:
`totals.py` (3 laws × 8192 orbits, 7 min, < 1 GB; G asserted bit-exact against the
author's `results.json`), `budget2.py` (< 1 s, reads `totals.json`). Raw points in
`totals.json`. Built from the run's own scripts (`h_live.py`'s evolve/measure, verbatim).

## Claim (restated around what actually bounds H_live)

H_live is bounded **iff the store both re-fits the generator and canonically relabels
unobserved bodies** (label cost → 0 for bodies the player has never pinned). Re-fit
**alone** bounds nothing: its total (residual + label permutation) is ≥ the entropy-coded
frozen cost at **every checkpoint of all three jump laws** (42/42; G 15.05 vs 10.79,
T1 16.01 vs 11.75, T2 19.62 vs 15.33 bits at t = 8192). With relabelling, the floor is
**flat in t and law-robust: 4.26–4.30 bits/body** at lab N (m* = 16384 knots), falling to
a measured **1.80–1.83 bits/column** at m = 2.6×10⁵ knots (program cost 0.008 bits at
10⁹) — even under the checker's |Δ| = K/U² tail, whose second moment is 667× the
Gaussian's. The binding deadline is the relabelling **law decision**, and it is set by
the engine's real jump tail: **1.14×10⁴ orbits** under the K/U² tail (the checker's ~10⁴,
confirmed), 1.15×10⁶ under the physical areal-1/b tail, 9.4×10⁶ under the Gaussian — the
author's "not urgent" survives only under the gentlest tail.

## Bottleneck

Same as the parent run: board risk "distinctions created per game-second (H_live)";
bottleneck 5. This run completes the accounting the parent left one experiment short of,
and hands `b-h-live` three numbers: the law-robust floor (1.8 bits/column at 2.6×10⁵
knots), the tail-dependence of the relabelling deadline (10⁴–10⁷ orbits), and the
confirmation that the checker's E[Δ²] = 6.6×10⁶ reconstructs exactly (K = 25, cap 10⁴,
median 100: 1.67×10⁶ continuous + 5×10⁶ in the 5% pile at the cap).

## Evidence

### The totals comparison (`python3 totals.py`, 7 min; `python3 budget2.py`, < 1 s)

N = 2²⁰, s = 1 cell/orbit, r = 2.135×10⁻³ (r8 v2 belt 0), T = 8192, checkpoints at
powers of two; jump laws median-matched (|Δ| = 100 cells) and capped at 10⁴: **G** the
author's Gaussian (J = 100, E[Δ²] = 10⁴), **T1** the areal 1/b impulse (Pareto-α2,
E[Δ²] = 5.40×10⁴ measured), **T2** the checker's |Δ| = K/U², U uniform (E[Δ²] = 6.66×10⁶
measured — their 6.6×10⁶). Reproduction: **G matches the author's run 1 bit for bit**
(14/14 checkpoints, H(δ) = 2.1047938…; asserted in-script, `G_reproduction_pass`).

| law | frozen(8192) | label(8192) | floor(8192) | resid@2.6e5 | spread(8192) | noRelabel(8192) |
|---|---|---|---|---|---|---|
| G  | 10.79 | 10.79 | **4.26** | 1.80 | 428 | 15.05 |
| T1 | 11.75 | 11.75 | **4.26** | 1.81 | 983 | 16.01 |
| T2 | 15.33 | 15.32 | **4.30** | 1.83 | 10803 | 19.62 |

- **Floor flat in t**: 4.25–4.30 bits from t = 512 to 8192 in every law
  (floor(8192)/floor(1024) = 1.00); growth was table resolution, absorbed by m*.
- **Law-robust**: T2's spread is 25× G's, its floor is +0.04 bits. Uniform-in-rank
  knots spend resolution where bodies are; the 1/U² tail's far bodies are few and the
  cap pile is dense — heavy tails do not price the quantile program. (Prediction said
  7–12 bits; the mechanism is better than guessed, in both directions: G's floor missed
  high by 0.46 because program cost binds at lab N beyond m = 16384.)
- **noRelabel ≥ frozen at 42/42 checkpoints** — the checker's refutation extends to both
  tails; relabelled total < frozen from t = 2 in every law.

### The corrected 10⁹ budget (`budget2.py`; 3 walking columns, fits over t ∈ [1024, 8192])

| row | bits/body | GB | verdict |
|---|---|---|---|
| frozen, 62-bit record × 3 cols (law.md line 13) | 186 | 23.25 | **breaks at t = 0 — the format, not time** |
| frozen, entropy-coded, G / T1 / T2 @ t = 8192 | 32.4 / 35.3 / 46.0 | 4.05 / 4.41 / 5.75 | fits |
| re-fit, NO relabelling, G / T1 / T2 | 45.1 / 48.0 / 58.9 | 5.6 / 6.0 / 7.4 | fits, but ≥ frozen everywhere |
| **re-fit + relabelling, G / T1 / T2 (prog free at 10⁹)** | **5.4 / 5.4 / 5.5** | **0.68** | **fits, flat in t** |

Deadlines: entropy-coded frozen breaks 8 GB at 1.3×10¹⁰ (G), 5.7×10⁸ (T1), 3.1×10⁵
(T2, local-slope fit 1.11; the asymptotic CLT bound is ~6×10⁷ — either way inside a
10¹⁰-orbit universe, so under the heavy tail even honest entropy coding breaks, while
relabelling is flat at 0.69 GB). The **label-law deadline** (16 bits/column):
9.4×10⁶ / 1.15×10⁶ / **1.14×10⁴** orbits (G/T1/T2).

### Corrections to the parent run's record

- The parent's decisive contrast (4.34 GB fits vs 7.75 GB breaks) was entropy-coded
  re-fit vs fixed-width records; entropy-coded frozen also fits (4.05 GB @ t = 8×10³,
  G). The honest contrast is in the table above, same coding on both sides.
- The parent's "~350 orbits to full scar record" mapped an 8-bit entropy crossing onto a
  62-bit format; the record format is over budget from t = 0 (23.25 GB at 3 columns).
- The parent's "not urgent" (1.2×10⁷) holds only under the Gaussian tail it assumed.

## Predictions

`predictions.md` registered before `totals.py` existed (mtimes 01:41:43 < 01:42:06).
Held: P0 (moments: 5.40×10⁴, 6.66×10⁶, medians 100.0), P1 (bit-exact reproduction),
P2 (T1 11.75 ∈ [11.4, 12.6], slope 0.58 ∈ [0.42, 0.60]; T2 15.33 ∈ [15.0, 16.5], slope
0.95 ∈ [0.9, 1.6]; deadlines 1.15×10⁶ ∈ [10⁶, 4.5×10⁶] and 1.14×10⁴ ∈ [6×10³,
1.5×10⁴]), P4 (42/42 totals verdicts; relabel < frozen from t = 2, predicted t ≥ 128).
Missed, one cause each: P3's floor guesses bracketed wrong — G 4.26 vs [2.8, 3.8]
(program cost binds at lab N) and T2 4.30 vs [7, 12] (the floor is law-robust, the
discovery above; the 10⁹ bound ≤ 8 held at 1.8); P5's T2 frozen-breaks deadline came in
at 3.1×10⁵ by the measured slope against a CLT-derived 5.7×10⁷ — slope-sensitive, both
brackets reported. Nothing retuned; both misses are the same structural fact.

## What would make it wrong

- **The floor's law-robustness is measured on median-matched monotone tails and iid
  exchangeable kicks.** Correlated or resonance-sculpted structure (Kirkwood gaps,
  formations) changes the marginal's *shape*, not just its width; the parent's
  checker already showed the floor holds for a 64-clump formation (2.85 bits), but
  joint (U, e) correlation after encounters is unmeasured — the matching is 1D.
- **Relabelling is a law decision, not code**: it deletes identity of *unobserved*
  bodies. Player-pinned bodies keep labels (their light cone bounds the count); the
  model charges 0 for them, which is right only until the player pins.
- **The 10⁹ floor extrapolates program-cost-freeness and N-independence of the
  residual** (resid is a property of the quantile function, not of N; untested at
  N > 2²⁰, and m beyond 2.6×10⁵ untested).
- **The tail itself is the load-bearing unknown**: T1 vs T2 move the law deadline two
  orders. Measuring the engine's real kick distribution in cells (the parent's named
  gap) decides which column of the deadline table is live.

## Cost of adopting

Same as the parent's (one idle-time shipmem pass: quantile re-fit + sorted match) plus
the relabelling rule for unobserved bodies — a law.md decision that must be Julien's
("identity is provenance" cuts both ways: relabelling is provenance *forgone*, so it
must be a law, not a compression trick). The law's budget line should read: "+ ~2–5
bits per kick true birth (log₂(4.13σ)); steady state = re-fit floor (1.8 bits/column
measured at 2.6×10⁵ knots, law-robust) + labels of player-pinned bodies only; 62 bits
is the record format, over budget from t = 0."

## Fit with PRINCIPLES

- **6. Store the generator, not the generated** — and re-emit it as the ensemble
  drifts; the generator's knots are spent where bodies are, which is why heavy tails
  are free.
- **24. The memory floor is information** — the floor is the relabelled residual
  (measured, flat, law-robust), not any record format.
- **5. The player is the only wildcard** — relabelling is exactly "identity exists
  where the player's light cone has pinned it"; everything exchangeable carries none.
- **22. The simulation decides; heuristics schedule** — which tail the engine really
  has is a measurement (b-h-live), and it alone sets the deadline.

## The lens (what Fermi may have missed)

One column, iid kicks, Monte Carlo at N = 2²⁰: the 10⁹ numbers are extrapolations of
measured floors with program cost divided by 2³⁰, not measured at 10⁹. The relabelling
rule's legality (Julien's call) is outside the lab's authority — this dossier prices the
decision, it does not make it. The m-knot tables are uniform-in-rank; B18b's dyadic
quantile tables are the scale-free version and should re-measure the 1.8-bit floor
before it is frozen. The deadline fit for T2 is slope-sensitive (1.11 local vs 0.5
asymptotic); the honest bracket is 3×10⁵–6×10⁷ for the GB line and ~10⁴ for the label
law, and only the engine's measured tail picks the column.
