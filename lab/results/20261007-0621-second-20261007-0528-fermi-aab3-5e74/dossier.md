# Dossier — 20261007-0621-second (second author on 20261007-0528-fermi-aab3)

## Claim

The checker's named experiment (the b-h-live build: instrument H_live in `xtask universe
--bench`) requires crate edits, which this lens may not make, so I ran its cheapest decisive
part — pinning the impulse accounting and the f_emb arithmetic on the real population — and
the run's claim **holds, with the f_emb uncertainty removed entirely**: at 10⁹ bodies the
embryo/planet H_live term is set by the *total embedded perturber mass* M_pert (not by any
f_emb × μ split), and under every physical M_pert (≤ 10⁻³ M_star; even 10⁻², ten Jupiters,
stays 5× below) both creation and tube materialization sit 1.7–8 orders below the 8 GB
floor at the worst mass split. The correct per-conjunction kick at belt scales is
δv/v ≈ (4/3)μ/b² (measured slope −2.00), so the author's 2μ/b is 5× low and the checker's
2μ/(0.0175 b) is 10× high at 0.1–0.2 AU; both wrong laws misjudge b_bits by 5–10×.

## Bottleneck

Same as the parent run: HANDOFF's "H_live: not measured yet" against board item "fitting
10⁹ in 8 GB". The silver verdict's blocker was that the largest term (creation) spanned ~6
orders on unmeasured f_emb and the impulse table was ~57× off. This run replaces both with
measured laws: the six orders collapse into the single physical knob M_pert ∈ [belt mass,
star-bounded disk], and the gate for the b-h-live build becomes "measure the belt's M_pert
(top of its mass function), not f_emb".

## Evidence

Everything regenerates from this folder: `python3 enc3.py && python3 gate2.py`
(warm: ~4 s; cold, if `enc3-raw-*.json` are deleted: ~6 min for 2896 exact restricted
3-body integrations, 8 workers, < 1 GB). numpy 1.26 / scipy 1.11, machine shared with the
window's other runs. Numerical controls: μ=0 re-integrations of the same encounter windows
give net element drift ≤ 4.3×10⁻¹³, six orders below the smallest binned kicks (2.7×10⁻⁷).

1. **The kick law, measured** (`enc3.py`, DOP853 rtol 1e-12, Sun + circular perturber +
   massless belt-0 rock, one conjunction per window, net Δ(a,e) across the pass; binned
   medians over 700–1100 encounters per mass):
   - 10²² kg, b ∈ [0.087, 0.205] AU: δv/v = 1.49×10⁻⁶ → 2.65×10⁻⁷, log-slope **−2.00**,
     normalization 1.66–1.72× the shear law (4/3)μ/b². The checker's law is 10× high at
     0.2 AU; the author's 5× low; even the true-local-v_rel impulse is 2.5–4× high
     (adiabatic cancellation).
   - 10²⁴ kg tracks shear within 1.5–2.2× at all b ≥ 0.006 AU; b_strong (δv/v = 10⁻³)
     measured at 0.0348 AU = 5.05 Hill radii (the Hill control holds).
   - 10²⁶ kg: kicks ≥ 2.9×10⁻³ across the whole belt — every conjunction qualifies
     (b_bits and b_strong belt-wide; handled as saturation, not extrapolation).
2. **b_bits(10²² kg) = 0.106 AU** (author: 0.01; checker: ~0.5). b_strong(10²²) = 3.5×10⁻³
   AU (shear-scaled from the measured 10²⁴ crossing; 2.4 Hill radii).
3. **The rate curve extended to b = 0.5 AU** (the author sampled ρ ≤ 10⁻³ only): R ∝ b
   below ~0.013 AU (epicyclic), R = 1.72·N·b² above (belt-Δa-limited; measured R(0.106) =
   193/orbit at belt-0 local density, matching the analytic form exactly).
4. **The f_emb × μ degeneracy cancels.** Per-rock rate = R(b_bits)·f_emb with
   f_emb = M_pert/(μ·N_rock): creation = R(b_bits)·M_pert/μ·bits/T_orbit, independent of
   the split in the shear regime (where R ∝ b_bits² ∝ μ). Worst case over ALL splits
   (f_emb ≤ 1), from `gate2.py` (which supersedes enc3.py's own stage-4 gate table: the
   latter lacks saturation handling) — bits maximize at 1.4×10¹⁷ kg planetesimals, tubes
   at 2.4×10²⁰ kg ≈ the regime transition μ* = 3q(e·a)²/4:
   | M_pert (M_star) | creation (bits/s, worst split) | tubes/s | 6 GB share fills in |
   |---|---|---|---|
   | 5×10⁻¹⁰ (a 10⁹-rock belt itself) | 7.7×10⁻⁶ | 1.0×10⁻⁷ | 1.2×10⁸ game-yr |
   | 5×10⁻⁶ (the stated 10²⁵ kg) | 0.077 | 1.0×10⁻³ | 1.2×10⁴ game-yr |
   | 10⁻⁴ (heavy disk) | 1.5 | 0.020 | 585 game-yr |
   | 10⁻³ (max physical disk) | 14.8 | 0.203 | 58.5 game-yr |
   | 10⁻² (ten Jupiters — absurd) | 126 | 2.03 | 5.9 game-yr |
   Tube floor = 10.4/s (0.375×10⁹ tubes over 3.6×10⁷ game-s). Breaching it needs
   ≥ 5×10⁻² M_star of embedded μ*-scale perturbers — a hidden companion star inside the
   belt, at which point the belt-density model has already failed.
5. **r8 v2 claim check, honestly redone at frozen N = 10⁴** (the rung pins N; σ_e
   log-uniform [10⁻³, 3×10⁻²], ρ log-uniform [10⁻⁵, 3×10⁻⁴]): at (σ_e = 3×10⁻³,
   ρ = 10⁻⁵) my model gives candidates ×1.09, encounters ×1.52 — the checker's in-band
   match reproduced. At the author's assumed σ_e = 10⁻² the encounter count misses ×5.6
   (ρ = 10⁻⁵) to ×153 (ρ = 3×10⁻⁴). So "reproduced within a factor 2" needed both N
   floated (4250) and a low, undisclosed σ_e draw (~25th percentile of the band).
6. **Engine side, not done here:** the b-h-live build itself (digest-safe H_live from
   engine state, `xtask universe --bench`) is a crate/xtask change — forbidden and beyond
   the window. What this run gives that build: the two laws it must reproduce (kick ∝ μ/b²
   beyond the epicyclic scale, R ∝ b / b²), and its instrument target (M_pert, the belt
   mass function's top end — one number — rather than f_emb).

## Predictions (predictions.md, written before the integration)

- P1 (b_strong within factor 2 of 3 r_H): held as a bound — out of sampled range for
  10²² kg directly (no bin below 6×10⁻³ AU had δv ≥ 10⁻³); the 10²⁴ kg control measured
  5.05 r_H and shear-scaling gives 3.5×10⁻³ AU = 2.4 r_H for 10²² kg, inside the window.
- P2 (slope ∈ [−2.6, −1.6], shear normalization within ×3): **held** — slope −2.00,
  normalization 1.7×.
- P3 (b_bits ∈ [0.03, 0.2]): **held** — 0.106 AU.
- P4 (mass-bounded creation < 100 bits/s at ≤ 10⁻³ M_star; ≤ 1 at stated): **held** —
  14.8 and 0.077 bits/s; the 6-order f_emb span collapsed to the M_pert range above.
- P5 (reproduce the checker's in-band r8 match): held — ×1.09 / ×1.52, inside their
  ×1.2–1.8 band.

## What would make it wrong

- The kick law is measured for a *circular* perturber and coplanar belt-0 geometry; an
  inclined or eccentric heavy perturber (a migrating Jupiter) resonantly pumps the belt
  faster than any single-conjunction law — the resonance/migration epoch is outside this
  experiment (the board already knows resonance needs phase feedback, r4/r9).
- Net per-conjunction Δ(a,e) counts the forced secular oscillation for heavy perturbers
  (10²⁶ kg rows); a program holding the planet can absorb part of it, so those rows
  overcount distinctions (conservative direction).
- Bits-per-kick set to 2 (author used 3); the worst-split creation scales with it —
  ×1.5–3 uncertainty, no order changes.
- M_pert is still unmeasured in any engine scene; my bound is physical (star dominance),
  not measured. The b-h-live build must measure it.
- Floor arithmetic inherits the parent run's assumptions (16 B tubes, 6 GB share,
  3.6×10⁷ game-s horizon); reabsorption ignored (conservative).

## Cost of adoption, fit with PRINCIPLES

Adoption cost ~zero (no engine change): the priority call stands — gate f_ind, build
nothing for encounter memory — now with the gate variable corrected to M_pert and the
worst case tabulated. PRINCIPLES #24 "the memory floor is information-theoretic": the
floor's largest dynamical term is now bounded by a mass argument, not a population
assumption. #10 "run the simplest falsifying test first": 2896 exact integrations settled
a 6-order parameter dispute. #32 "symmetry is found, not given": the f_emb × μ split
drops out entirely in the shear regime — the representation that makes it cancel is the
mass budget.

## The lens (what the second-author lens may have missed)

I inherited the parent's scene model (one belt, embryos embedded, no migration, no
inclinations). The worst-split search is over a smooth μ grid with the two-regime b_bits
law — a migrating resonant chain or a game-engineered dense swarm around a planet breaks
the "embedded in belt-0 density" premise, and with it the M_pert bound's tightness (not
its direction: those cases concentrate mass, which the table shows is the *less*
dangerous split per unit mass, but they also raise local density, which raises R at fixed
M_pert). The 10²⁶ kg regime's forced-secular overcounting is unquantified. Single-window
net kicks average over conjunction phase; resonant phantasms (repeating conjunctions at
the same longitude) can correlate successive kicks — the 60-game-year fill times at
10⁻³ M_star have unquantified correlated-kick corrections of order the libration physics
r4 already flagged.
