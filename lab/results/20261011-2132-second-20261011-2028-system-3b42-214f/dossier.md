# Dossier — run 20261011-2132-second-20261011-2028-system-3b42-214f (second author on 20261011-2028-system-3b42)

## Claim

Both of the checker's named gold experiments are done, and the original claim **holds**:
the encounter tier's same-key (straggler) branch freezes as an **arc window on the tube's own
phase axis** — width `W = 1.5·(4·e_hi + 3·e_hi²) + dn_cell·t_end` from the key cell's constants
alone — with **zero missed encounters at every n and every dial**, **same-key candidates per
real encounter constant in n** (5.3→5.6 at the engine dial, n 400→3200, both terms ∝ n²), and
the birth-fixed branch (equal integer periods) permanent and 25–32× cheaper than all-pairs; and
the strong-field key order survives because **U(L)|E never turns in the stored (bound) domain**
(0/200 E-columns through the separatrix-adjacent region; the dossier's worry was conjecture),
with the (E,L)-key lattice zero-miss (7,924,025/7,924,025 exact-tier pairs, inflation 1.002) and
the Newtonian-contiguity U-scan complete (0 misses) at r_p down to 4.6 GM.

One correction to the author's record: rank-k is **not** the certificate (member clustering
inside the arc breaks it — measured); the sound form is the arc window, which the phase-sorted
tube store serves natively. The checker's probe ("rank bound grows with local phase density",
rank-4 coverage 45.8%→15.9%) is confirmed and explained: rank-k ∝ m at fixed distribution
(kappa_req ≈ 0.10 constant in n), so a **fixed** rank certificate cannot survive a dense band,
but the **closure-scaled window** does, at constant cost per real encounter.

## Bottleneck

Board focus items 3 and 6 (encounters without per-body state; candidate work tracks real
encounters). This closes the two gaps the checker named between the run and gold: the unfrozen
straggler rule and the unmeasured strong-field key order.

## Evidence

All numbers from `cargo run --release -p emergent-encounters --example second_lattice --offline
{belt,coorbital,straggler,strongfield}` (script saved at `work/second_lattice.rs`, wired as the
crate example; JSON lines in `metrics-*.json`). Determinism: two full runs bit-identical in
every counter (only wall-time digits move); the `belt` and `coorbital` modes reproduce the
original run's stored record **byte for byte** (9/9 lines; 2093/1496 events, worst rank 2/10).
Peak RSS 2.9 MB. Total wall ≈ 250 s, single-threaded truth.

**1. The frozen straggler rule (checker's experiment 1).** Scene: the crate's own
`narrow-adversarial` spec (uniform ϖ, σ_e 0.025, ρ 3e-3, a ∈ [1, 1.0025], 20 orbits, the
crate's seed), truth on every same-key pair, rank and window instruments in the λ(0) circle
order (the tube store's phase axis), n ∈ {400, 800, 1600, 3200} at two dials:

| dial | n | events | misses | arc/W max | cand/enc | all-pairs/enc |
|---|---|---|---|---|---|---|
| engine (1 a-cell, de 0.01) | 400→3200 | 562→34132 (×3.9/doubling) | **0** | 0.73–0.85 | **5.3→5.6** | 24.5→26.0 |
| closure-matched (16 a-cells) | 400→3200 | 25→2089 | **0** | 0.38–0.58 | **1.8→2.1** | 26–35 |
| birth-fixed (equal periods) | 300→1200 | 299→2749 | **0** | 0.47–0.54 | **0.7→1.1** | 20–35 |

- Soundness: `misses = 0` on all 11 lines; margin instrument `arc_over_w_max ≤ 0.850` (the
  bound derivation: two same-key bodies can meet only near a shared true longitude, where their
  mean longitudes differ by ≤ 2(e_i+e_j)+O(e²), unwound to the epoch by shear dn·t_end).
- Scaling: candidates 2,972→191,813 and events 562→34,132, both ×3.9–4.1 per doubling —
  candidates per real encounter constant in n (the checker's named quantity).
- Negative control: dropping the closure term misses 94→5,317 events at the engine dial
  (the instrument is live); at the closure-matched dial the closure term is unnecessary —
  the quantum, not the rule, absorbs closure there.
- Birth-fixed: dn = 0 exactly (asserted equal integer periods, 11–12 cells flagged), the λ(0)
  order is permanent, one window at key entry covers 50 orbits with zero maintenance.
- Rank shadow: kappa_req ≈ 0.08–0.11 (engine dial), constant in n; fixed rank-4 coverage decays
  0.92→0.25 as n grows — a fixed rank-k certificate does not survive density; the window does.
- Instrument bug found and fixed during the run: sorting λ(0) unwrapped (M+ϖ ∈ [0, 2τ)) splits
  the circle; with the wrap fixed, ranks halve and candidate counts drop ~25–35%. The arc/misses
  instruments were always wrapped (soundness conclusions unaffected).

**2. The strong-field key order (checker's experiment 2).** Exact Schwarzschild geodesics
(μ=G=c=1): (r_p, r_a) sampled (r_p ∈ [4.6, 16.6], r_a up to ~200), (E, L) in closed form,
turning points re-solved from the radial cubic (the two smallest positive roots; the third is
the inner plunge barrier) and required to reproduce the inputs to 1e-9. n = 4,000, E ∈
[0.946, 0.996], ρ = 0.05.

- **U(L)|E does not turn**: 200 E-columns × 512 L-steps from L_sep to L_circ, monotone in
  every column (min relative step 1.19e-4). The dossier's "past the ISCO-adjacent region U(L)
  can turn" is refuted for stored orbits (the strong-field flyby sweep, residual-checked in the
  prototype, is monotone too). So the U-band scan needs no turning-point repair: the key order
  (E-major, L-minor) preserves U contiguity in strong field as in Newtonian.
- **Zero-miss**: key = quantized (E, L), 64×256 cells, per-cell conservative constants compiled
  on a 5×5 sub-grid clipped to the bound domain (the memo entry reading its own turning points):
  `cell_violations = 0` (every member inside its cell's compiled ranges), `missed = 0` of
  7,924,025 exact-tier (per-body radial-overlap) pairs, inflation 1.002.
- **U-scan**: the naive Newtonian-style L-window scan finds 2,762,416 pairs vs the exact U-band
  set 2,762,179 (1.0001×), missing 0; the sorted-U table sweep costs 2,760,209 comparisons
  (tight). Newtonian control belt: 0 misses. Scope: this measures the candidate/order tier
  algebraically (turning points, conservative ranges); integrated Schwarzschild encounters and
  the GR cone test itself remain unmeasured — the phase machinery (experiment 1) is Newtonian.

## Predictions

Written (`predictions.md`) strictly before the straggler matrix was first run; the strong-field
lines had one earlier identical-seed run before the file was written, so their predictions are
confirmations, not held out (the held-out content is the straggler matrix and its kill
criteria). Held: zero misses everywhere (1); arc/W
margin < 1, max 0.850 (1); the negative control fires at the engine dial, 94→5,317 (2) — at the
closure-matched dial it does not fire, which is the dial's design, not a leak (the closure term
is only load-bearing when the quantum is coarser than the closure width); cand/enc constant in
n within ±40% — measured ±3% at the engine dial (3); kappa_req constant, 0.08–0.11 on the
narrow band (4); u_turn_cols = 0/200, missed = 0, violations = 0, inflate 1.002, naive_miss = 0,
Newtonian control clean (5, 6). One number was mispredicted in range only: the birth-fixed
kappa_req (0.02–0.04) sits below the narrow band's (named range was for the narrow band).

## What would make it wrong, and the cost of adopting it

- The arc-window bound is Newtonian (equation of centre + Kepler shear); in the GR doll the
  equation of centre is compiled per key (the memo entry's Δφ per cycle), so W reads the same
  constants — but the GR version of the bound is unmeasured, as is the GR cone test itself.
- The window is horizon-relative: W grows ∝ t_end until it saturates at π (all-pairs) — over
  long horizons a dense narrow band genuinely needs O(m²) per cell once closure exceeds the
  circle; the honest statement is constant work per real encounter at fixed horizon, with the
  quantum/cadence dial (measured at two settings) setting the constant.
- Same-key truth was scoped to same-cell pairs (cross-key zero-miss is the original run's,
  reproduced); at n = 3200 the truth loop is 66 s single-threaded (the whole matrix 250 s).
- Adoption cost is unchanged from the original run (re-point the candidate tier at the tube
  store), plus one rule: the same-key tier queries an arc window, not rank-k neighbours.
- The deleted 96 GB remains a counterfactual (the plane does not link the crate); the result
  forecloses the second per-body structure at wiring time.

## Fit with PRINCIPLES

- #1 "The cheapest compute is compute not done": the window certifies from the cell's
  constants, and its cost tracks real encounters (measured constant per encounter in n).
- #19 "A fix signals the wrong representation": the checker's rank-grows-with-n finding was
  not a patch-away artifact but the wrong unit — rank is the window's uniform-density shadow;
  freezing the window dissolves it.
- #6/#24 (store the generator; the memory floor): zero per-body state beyond the tube, with
  the strong-field constants compiled per key exactly as the memo entry already is.

## The lens

The second-author lens may have made me accept the algebraic strong-field scope (candidate
tier, not integrated GR encounters); the two cheapest decisive parts of the checker's ask were
run, and both the turn question and the zero-miss are closed at the candidate level. The
narrow-band truth is the crate's own Kepler replica — the GR phase bound is derived but
unmeasured. The wrap bug in the rank/candidate instruments was found by refusing to believe an
instrument that disagreed with a sound bound (PRINCIPLES: "measure before claiming"); the
published numbers are from the fixed instrument only.
