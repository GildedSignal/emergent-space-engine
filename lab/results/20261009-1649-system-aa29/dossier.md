# Dossier — one circle rotation, two gates: where the resonance gate and the encounters pass are (and are not) one mechanism

Run: 20261009-1649-system-aa29, lens: the whole system. All numbers below are
regenerable by the commands given; each finishes in well under 60 s.

## Claim

The kick layer's resonance gate and the encounters layer's conjunction predictor
read the same object — the pair's synodic circle rotation whose near-return
structure is the continued-fraction pass `crates/encounters/src/dioph.rs` already
computes — so law.md's separate detector ("a resonance is detected from the
compiled frequencies, p·Ω₁ − q·Ω₂ ≈ 0") can be deleted **as a pairwise gate**.
Measured: one CF pass with per-order constants recalls 94–98% of the seeds where
orbit-averaging fails (FN 2–11 per 600 across μ ∈ {3e-4, 1e-3, 3e-3}, e₀ ∈
{0.02, 0.05}); but the gate's threshold is **not** a frozen constant of the pair
(the failure zone is a forced-beat cusp with no sharp boundary, amplitude ∝
1/detuning), and at μ = 3e-3 pairwise coverage collapses: 40% of seeds land in
resonance-overlap chaos no pair gate can own.

## Bottleneck

Board focus item "fewer kicks per orbit" via the kick/resonance tier, and the
encounters design (Binet cone + CF conjunction schedule). A single CF structure
serving both tiers deletes one component (the standalone resonance detector) and
makes the two thresholds one calibration. Not a 10× compute claim: a
representation unification (principle 19/32) with measured domain of validity.

## Evidence

Float replica, circular restricted three-body (Sun GM=1, Jupiter a fixed ring
a=1, ship massless), α = n_ship/n_J ∈ [1.32, 2.08], two starting phases,
velocity-Verlet 512 orbits at 384 steps/orbit, e-pump low-passed over one
Jupiter orbit. FAIL_pump = pump > 2.5× local 20th-percentile baseline; the
orbit-averaged layer is flat in e here (coplanar circular external perturber is
axisymmetric after double averaging), so any secular pump is behaviour it misses.

Commands (from `lab/results/20261009-1649-system-aa29/`, ~20 s each):

```
python3 sim.py --mu 1e-3 --e0 0.02 --amin 1.32 --amax 2.08 --n 300 --T 512 --out calib.json
python3 sim.py --mu 3e-4 --e0 0.02 ... --out ho_mu3e4.json   # same flags otherwise
python3 sim.py --mu 3e-3 --e0 0.02 ... --out ho_mu3e3.json
python3 sim.py --mu 1e-3 --e0 0.05 ... --out ho_e005.json
# evaluation: gate2.py plus the eval loop in the run log; constants frozen in gate2.py
```

Key numbers (non-chaotic seeds unless said; chaos = a_drift > 0.05):

| run | plain-K pump acc | FN / 600 | μ^(2/3)-K pump acc | chaos fraction |
|---|---|---|---|---|
| μ 1e-3, e₀ 0.02 (calib) | 0.727 | 11 | 0.727 (same μ) | 0.062 |
| μ 3e-4, e₀ 0.02 | 0.717 | **2** | **0.830** | 0.000 |
| μ 3e-3, e₀ 0.02 | 0.539 | 7 | 0.319 | **0.400** |
| μ 1e-3, e₀ 0.05 | 0.682 | 9 | 0.682 (same μ) | 0.093 |

Structure behind the numbers (calib trace, M0 = 0):

- First-order resonances (4:3, 3:2, 2:1) each carry a **forced-beat cusp**:
  pump ∝ 1/detuning with no boundary; 2:1's flank reaches Δα ≈ 0.10 (pump 0.031
  at 8× the quiet-plateau distance). The three cusps' FAIL boundaries collapse
  to q·|Δα| ≈ 0.075–0.08 at μ = 1e-3.
- Adjacent cusps overlap: α ∈ [1.36, 1.50] is a chaotic zone (a_drift up to
  0.19, pump 0.1–0.33) owned by no single pair.
- Island interiors (α ∈ [1.32, 1.343] at 4:3) are phase-locked (raw conjunction
  clustering R̄ = 0.98–1.00) but do not pump within 512 orbits at e₀ = 0.02:
  the detector flags them, the pump label cannot see them. 105–147 of the
  "false positives" per run are exactly these (window-blind label, not detector
  error — but it means a pump-based gate calibration can never be sharp).

## Predictions (predictions.md, frozen before evaluation)

1. LOCK agreement ≥ 90% — **unjudgeable**: my detrended-phase lock metric is
   broken (the linear detrend removes the circulation it should expose; it
   labels 62% of calibration seeds "locked"). Reported as broken, not as passed.
2. Pump agreement ≥ 80%, FP-dominated — **held** (0.69–0.83, and FP is
   island-interior/lock-consistent).
3. μ^(2/3) rescaling beats plain K — **held at μ = 3e-4** (+11 points, FP
   168→58), **contaminated at μ = 3e-3** (40% chaos); the width does scale with
   μ, closer to μ^(2/3) than to a μ-independent cusp constant, but 2 points
   cannot fix the law.
4. Chaos fraction at μ = 3e-3 ≥ 2× μ = 1e-3 — **held, 6.5×** (0.062 → 0.400).

## What would make it wrong

- The lock metric fixed properly (circular statistics on the detrended
  conjunction phase, longer window) could still separate libration islands from
  cusp flanks and vindicate a sharp per-order constant — or confirm no sharp
  boundary exists. That is the one experiment this run is away from silver→gold.
- The replica is 2D coplanar with a fixed-ring Jupiter and a Verlet truth at
  384 steps/orbit; inclined or eccentric perturbers, and the integer law, can
  move the constants (not, I think, the structure).
- Horizon dependence (T = 256 vs 512 compared on the 2:1 flank): cusp amplitude
  at fixed detuning is window-independent; the apparent boundary moved only with
  the baseline. So "the gate constant depends on the certificate horizon" is
  suggested by structure (beats of period < horizon), not cleanly measured here.

## Cost of adoption, fit with PRINCIPLES

law.md's kick section would read: "resonance is read from the pair's
conjunction rotation (the encounters pass), with the certificate horizon in the
window" — deleting the standalone frequency scan. Cost: dioph.rs gains one
window parameter (the resonant-angle half-width) — it already takes (lo, hi)
windows. Principle 19 ("how to have the same mechanics at all scales"): the
synodic near-return structure serves the conjunction schedule, the resonance
gate, and — at overlap — hands off to the dense order, whose selector
(events per cell per light-crossing) is the same crowding question one tier up.
Principle 32 (symmetry found by representation) is the lens's own trap here: the
CF symmetry is real, but the tier boundary is set by response amplitude, not by
the symmetry alone.

## The lens may have missed

I hunted a unification and found its domain instead; a builder's lens would have
asked whether the island-interior seeds (locked, not pumping) need per-conjunction
kicks *now* or only when e grows — a cost question I did not measure. Also
unmeasured: whether the engine's quantized (E, L) memo key changes the constants
(integer grid vs float detuning).

Self-assessment: **silver** — real, reproduced-on-rerun measurements with a
frozen prediction set, one named experiment (a valid libration judge) from gold.
