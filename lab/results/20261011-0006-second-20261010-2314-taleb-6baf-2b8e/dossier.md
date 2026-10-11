# Dossier — 20261011-0006-second-20261010-2314-taleb-6baf-2b8e (lens: second author)

**Claim.** The checker's named experiment is done and the original claim survives
in corrected form: a frozen birth-key program still dies in ≤ 0.4 planet orbits
(regenerated bit-exact from shipped code), but every headline number changes —
the true key-crossing physics at the 16-bit tube grid is a **synodic sweep of
≈ 460 cells/ship/P_p** (exact 1/q scaling, ×16.0 per 4 bits, 8→20 bits), a
**synodic-aware program absorbs all but one key update per synodic period
(0.55 events/ship/P_p, ~20 cells/P_p of secular drift, linear forever: fit
1.001 at 1200 P_p)**, misaligned rolling-mean programs see 11–23 events/P_p
with a **real fat tail (p99/med 4.1, top-1% share 3.9%) concentrated 100% in
the inner band**, the mature footprint at the tube grid is **20.7 bits/ship at
100 P_p, ≈ 22.1 at 1200 P_p** (k-NN at 10⁶ ships; the "12.7-bit floor" was
log₂N+0.72), and the reprogrammer bandwidth at 10⁹ ships is **≈ 900
(secular) to 4×10⁴ (misaligned) events/wall-s at RTF 100** — the dossier's
"2–4×10⁸" was 3–5 orders high.

**Bottleneck.** Same as the original run (HANDOFF risk 2, H_live). What this
second pass adds for the integrator: (i) the churn the compiler must consume is
set by *program quality*, spanning three orders (460 → 23 → 0.55) — the
phase-locked sampler (per-ship T_syn from a, one line of analytic input) is the
representation that makes the secular floor cheap; (ii) the allocator's tail is
real but spatial (inner band for ripple-dominated programs, outer band for
secular drift), not eccentricity-driven; (iii) the memory number for
bottleneck 5 is now measured with an N-scalable estimator: the mature belt at
the tube grid costs ~21–22 bits/ship against 0.126 at birth.

**Evidence** (from this folder; each ≤ 60 s except the 10⁶-ship run at 21 min;
numpy float64, counts on integer cell indices; machine: shared 8-vCPU runner,
load 2.9–3.1, memfree recorded in every JSON):

```
# 1. shipped-code record regenerates (9 runs, from headers on the run branch):
bash regen.sh                      # belt_s1/s2/hot_s3, ctl_s1/s2, 4 rings
(cd regen && python3 analyze.py)   # -> metrics-regen.json
#   differs from the original metrics.json ONLY in wall_s_max (timing).
# 2. unsaturated instruments (this run's hlive2.py; ceiling 129.53/P_p):
python3 hlive2.py --tag belt_s1 --seed 1 --N 4000 --po 300   # +s2,s3; ctl with --mu 0
python3 hlive2.py --tag belt_long_s1 --seed 1 --N 4000 --po 1200
sed 's/SM_STRIDE, SM_W = 1, 1024/SM_STRIDE, SM_W = 1, 2048/' hlive2.py > hlive2w2048.py
python3 hlive2w2048.py --tag belt_w2048 --seed 1 --N 4000 --po 300 --dump_po 1
# 3. belt-scale entropy (k-NN; ~21 min under contention):
python3 hlive_big.py --tag big --seed 11 --N 1048576 --po 100
python3 entropy.py && python3 analyze2.py    # -> entropy.json, metrics2.json
```

Numbers (metrics2.json; 3 seeds agree to <1%):

- **Sweep law (new).** Swept cell distance |Δi_a|+|Δi_L| per step, cadence-free:
  med 1.9 / 28.7 / **459** / 7349 cells/P_p at 8/12/16/20 bits — ratios
  15.4 / 16.0 / 16.0, the exact 1/q law. The naive changed-per-sample count at
  stride 1 reads 117.3 at bits16 = 90.5% of its 129.5 ceiling (multi-cell
  crossings per step near conjunction); the shipped 31.7 was the same
  saturation at stride 4. The synodic oscillation, not secular drift, sets the
  raw key churn; it is the cheapest thing for a program to model away.
- **Secular floor (new instrument).** Phase-locked sampler (each ship sampled
  once per its own synodic period): every ship changes its bits16 key at every
  fire — Hamming rate = fire rate, med **0.550–0.553/P_p** (3 seeds), p99 0.683,
  max/med 1.38; secular drift magnitude **20.6 cells/P_p**; growth fit **1.0015
  at 1200 P_p** (linear, permanent). Control (μ=0): med 0.000 exactly, p99
  0.547 = boundary-jitter upper bound (the deadband, the original run's fix,
  kills this class: control deadband p99 = 0.000).
- **Window family.** Rolling-mean key churn is a property of the window, not
  the belt: med 23.1 (1024-step window, stride 1), 12.1 (2048, stride 1),
  10.85 (2048, stride 4 — the checker's instrument). The original "13/P_p
  forever" headline dies; what is stable is the *tail*: p99 stays 84–94 across
  the family while the median falls — p99/med 4.07, top-1% share 3.9% (the
  shipped counter reported 0.96% from a saturated instrument; the
  pre-registered fat tail was real).
- **Tail structure.** Top-1% churners by instrument: w1024 → **100% inner
  band** (fleet share 29%), secular → **97–99% outer band** (fleet 5.5%), all 3
  seeds; birth-e ratio ≈ 1 (not eccentricity). The allocator inherits a
  *spatial* structure: ripple cost peaks nearest the stirrer, secular drift
  peaks at the far edge.
- **Entropy (k-NN, unit-corrected).** h_birth = −8.49 bits (10⁶-ship sample,
  k-stable within 0.02 across k=1..16; analytic thin-ridge value −7.98);
  h(100 P_p) = −7.46; decompression **+1.03 bits in the first 100 P_p**, then
  +0.81 bits from 100→1200 P_p (N=4000 fixed-instrument delta; growth is
  sub-diffusive, ≈ t^0.24, as the belt's bounded a-range fills). Control: zero
  drift (−7.593 → −7.593). Grid entropy at 16 bits/axis = h + 28.12:
  **19.6 (birth) → 20.7 (100 P_p) → ≈ 22.1 (1200 P_p) bits/ship**. The
  k-NN-at-4000 thin-ridge bias is +0.53 bits at 100 P_p (measured: same 10⁶
  population, 4k-subsample −6.93 vs full −7.46). Plug-in at 10⁶ ships on the
  bits16 grid reads 18.99 vs true 20.66 — still −1.7 bits undersampled
  (678k occupied cells): even the checker's suggested "plug-in at 2²⁰" is not
  converged at the operational grid; k-NN is. (My first k-NN implementation
  mixed nats and bits; fixed in entropy.py/hlive_big.py, and hlive_big's stored
  values corrected exactly via ψ(N)−ψ(k) scaling — the belt-scale sim was not
  re-run, the correction is analytic and stated in analyze2.py.)
- **Bandwidth (corrected arithmetic).** P_p = 2.024 yr; 10⁹ ships; RTF 100
  (1 game-yr = 3.156×10⁵ wall-s): secular floor **861 events/wall-s**,
  misaligned-window program 3.6×10⁴, naive-stride-1 1.8×10⁵. The original
  "0.7–1.6×10¹⁰ events/game-yr ≈ 2–4×10⁸/wall-s" divided by RTF without
  dividing by seconds-per-year — 3–5 orders high. The idle-time reprogrammer's
  load is negligible at every program quality; smoothness is not at risk from
  key churn.
- **What regenerated unchanged.** Half-life 0.0772 P_p (12/16 bits), 0.364
  (8 bits); ring/off-ring contrast absent (ratio 0.935); all nine shipped runs
  and metrics.json bit-identical (regen/, only wall_s_max differs).

**Predictions** (predictions.md, written before all runs): held — P1 (sweep
ratios 15–16, naive16 at 91% of ceiling), P3 (p99/med 4.07 ≥ 2, top-1% 3.9% ≥
2.5%), P4(b) (band concentration, far beyond the 45% bar), P8 (bandwidth).
Failed, each informative — P2 (the W-family median is window-dependent:
23.1/12.1/10.85 — the failure forced the phase-locked instrument and the
program-quality picture); P5a (h_birth = −8.5, not [−3,−1]: the L-ridge
responds to e², not e, at small e — my Fermi estimate was 60× thick);
P6 (k-NN at 4000 vs 10⁶ differ by 0.53 bits — thin-ridge bias, now measured;
plug-in↔k-NN at bits8 holds only where the ridge is wider than the cell);
P7 (plug-in at 2²⁰/bits16 reads 18.2–19.0, not the pure log₂N+0.72 = 20.7 —
collisions have begun; still undersampled by −1.7 bits, so the mechanism held
and the number refined). P5b held by the letter (+0.81 ∈ [0.5,1.5]) with the
honest caveat that growth is sub-diffusive (t^0.24).

**What would make it wrong.** (i) The secular sampler assumes the synodic
period from *current* a is the right phase anchor; near resonance with the
stirrer the libration period, not the synodic beat, is the slow clock, and
2:1-ring populations were not re-measured with it (the shipped ring runs show
no median contrast, but the secular tail there is unmeasured). (ii) Test
particles, one stirrer, 2D, ≤ 1200 P_p: the sub-diffusive exponent is
early-time; the approach to the domain-uniform limit (~log2(1.5·ΔL) + small)
is where growth must stop, untested beyond 1200 P_p. (iii) The grid-entropy
number depends on the domain [1,8]×[0.4,2.5] through the 28.12-bit offset; a
narrower live belt lowers it bit-for-bit. (iv) The 10⁶-ship kNN ran once
(seed 11); k-stability (±0.02) but not seed-stability was checked.

**Cost of adoption.** None in engine code; three design inputs change. (1) The
reprogram cadence target drops from "≥ 13 events/ship/P_p" to 0.55/P_p for a
phase-locked program — one key update per synodic period per ship, with the
per-ship period computed analytically from a (no state, no window). (2)
B18b/shipmem sizing: mature stirred belt ≈ 21–22 bits/ship at the tube grid
(bits16/axis), decompressing from the 0.126-bit birth program by ~20 bits
within 100 P_p and ~0.8 bits more per decade of time — birth-compression
sizing is confirmed as the ruin path, but the mature number is half the
naïve 64-bit-budget worry. (3) The allocator's tail handling: spatially
structured (outer-band secular, inner-band ripple), not per-ship eccentricity
— per-band slack, not per-ship slack.

**Fit with PRINCIPLES.** #3 "Compute only surprises": quantified — the
surprises are one per synodic period per ship (secular), and the 460-cell
synodic sweep is precisely *not* a surprise (derivable from a and the stirrer's
orbit — "redshift and co are not derived but emergent" cuts the other way for
keys: the synodic wiggle is derived, the secular drift is emergent). #32
"Symmetry is found, not given": phase-locking to the ship's own synodic
period is the representation that makes the secular rate trivial to measure
and to compute. #24 "The memory floor is information-theoretic": now measured
with an estimator that scales (k-NN at 10⁶), replacing a number that was
log₂(sample size). #9: five of eight registered predictions failed and each
failure is a design input.

**The lens.** Second-author work: I took the checker's three probes as the
starting point and they held, but following the recipe exactly (stride-2
smoothed rates, plug-in at 2²⁰) would have shipped two numbers that are still
instrument-bound (window-dependent median; undersampled plug-in). The lens
that helped was the checker's own tell — "the ceiling was in their own output"
— applied recursively to my own instruments (stride-1 W1024 vs stride-2
discrepancy → phase-locked sampler; k-dependence → unit bug). What I may have
missed: everything downstream of 1200 P_p, and multi-stirrer belts where
synodic periods interfere.

**Grade (self-assessed, for the checker):** the record regenerates from
shipped code (regen/, metrics-regen.json), the checker's named experiment is
done (unsaturated rates: sweep + window family + secular floor; scalable
entropy: k-NN at 10⁶ with the plug-in pin measured and explained; corrected
bandwidth), and the restated claim keeps the original's surviving core with
the two artifacts dropped and three new mechanisms measured. One substantive
caveat: the 10⁶-ship entropy run predates the unit fix and its values are
corrected analytically rather than re-run (21 min; exact correction, stated).
