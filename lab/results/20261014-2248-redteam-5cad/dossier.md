# Dossier — run 20261014-2248-redteam-5cad (lens: premise red-team)

## Claim

Representation.md's thesis 2 — "Even chaos has invariant statistics, and by the shadowing
lemma a deterministic law with the right statistics is a true orbit of nearby initial
conditions" — is false as written in the game's own chaotic regime: a quantized
area-preserving law (the doc's own error model: one floor unit per event, "carried
forward so that it never compounds") does not preserve the trapping-time statistics of
mixed-phase-space chaos, in either direction, and no shadow bound holds.

## Bottleneck

Not a compute bottleneck: a **premise** of the design (bottleneck 0, the representation
from scratch). The sentence licenses the dense order ("chaos, the normal case") to
dispose of trajectory truth. If false, the error **type** in chaos is not "initial
condition uncertainty" (benign, invisible in principle) but "false behaviour class"
(captures that never dissolve, or dissolve too early) — and principle 2 says error type
is the currency. No rung, gate or wiki page tests it (b12-statistic judges error
statistics, not behaviour-class preservation; r5 tests contacts and bit-identity).

## Evidence

All numbers regenerate with `regen.sh` (two scripts, ~85 s total, float64, Linux/x86 —
orders of magnitude only). Model: standard map K = 1.2 (area-preserving; KAM island +
chaotic sea + sticky bands — the universal mixed-phase-space Hamiltonian case), the
engine analogue of temporary captures / resonant trappings (co-orbital fleets live on
rotating-frame islands).

1. **Trapping tail, distorted in both directions (decisive; `dwell_tail.py`).**
   Ensemble: 256 ICs in the chaotic band just beyond each of 32 angles' outermost KAM
   curve; dwell = continuous stay inside the enclosing island disk, cap 10⁵ steps.
   True law: p50 = 393, p90 = 2,821, p99 = 14,208, max = 16,654, **capped 0.0%**.
   Quantized law (state rounded to a Q-grid every step):
   - Q = 10⁻⁴: p99 = 10⁵, **capped 2.7%** — spurious permanent traps appear.
   - Q = 10⁻³: p90 = 10⁵, **capped 14.1%** — one in seven sticky orbits never
     escapes; the true law frees all of them by 1.7×10⁴.
   - Q = 10⁻²: p90 = 512 (**tail crushed 5.5×**), capped 3.1%.
   - Same-magnitude random noise (±Q/2, Q = 10⁻³): capped 1.2%, p99 7.7×10⁴ —
     deterministic rounding is **not** interchangeable with noise of its own size;
     its systematic component builds spurious invariant structures (rounding breaks
     area-preservation, the one symmetry Hamiltonian chaos has).
   The "invariant statistics" clause fails at every Q, non-monotonically.
2. **No shadow bound in the sea (supporting; `shadow_falsifier.py`).** Sauer–Yorke
   noise test, 64 noisy copies each: in the chaotic sea (λ = 0.23–0.54) the median
   deviation from the reference grows decade over decade without saturation — at
   Q = 10⁻⁴ it reaches 2.25 (torus-scale decorrelation, diagonal 4.44) by 10⁵ steps;
   at Q = 10⁻³ decorrelation is complete by ~10³ steps. A shadowable (Anosov-like)
   system would saturate at a bounded multiple of Q. The regular island shows pure
   phase drift (actions preserved — the benign error type), which is why the
   behaviour-class metric, not phase distance, is the right instrument.
3. **Controls.** Positive: a KAM orbit stays on its island under quantization at
   Q = 10⁻² (dwell capped, unchanged) — the instrument does not break regular
   behaviour. Negative: Q = 1.0 scrambles the sticky ensemble (capped 2%). The
   float-noise arm (1) sits between truth and the quantized law — the measurement
   separates all three.

## Predictions

`predictions.md` was written before the decisive run. P4 was **wrong in direction at
fine Q** (I predicted tail crushed ≥ 10×; measured: tail *inflated*, 14% permanent
traps at 10⁻³ — a stronger refutation than predicted — and crushed only at 10⁻²).
P2 failed (no saturation in the sea; deviation passes 10³·Q without bounding). P1
failed in phase-space distance (regular-island deviation drifts to ~1 by 10⁴) and was
re-diagnosed as benign angle drift on nearby tori, consistent with the action-based
reading. P5 held (strong, non-monotonic dose–response). Reported as held/failed per
case.

## What would make it wrong

- The standard map is not the game's law. Scope: any Hamiltonian regime with
  cantori/island boundaries — the wiki's own co-orbital gold (fleets as
  rotating-frame structures) and resonance work put the game inside that scope; a
  clean proof would repeat the dwell-arm on the shipped `es-space-v2` dense order
  around a co-orbital island (the rung below).
- If the engine's integer law is exact-native (r2: "increments and kicks are integers
  native to the law, exact by construction"), there is no per-event rounding — but
  the doc's §2 error budget still allows one floor unit per event, and any
  representation change (Binet banding, doll handoffs, memo keys) reintroduces it.
  The clause should not lean on the shadowing lemma in mixed phase space; it needs a
  certificate instead (see the rung criterion).
- Cost of adopting the finding: a behaviour gate on trapping statistics (below), and
  the design text stops claiming shadowing where it has none.

## Fit with PRINCIPLES

- Principle 2 ("Behaviours matter… error type over error size"): the measured failure
  is exactly an error-type flip — the quantized law's sticky orbits are false
  behaviour classes, not larger errors.
- Julien's register ("NO ELITE style… averages crush data especially tail events"):
  the tail is what breaks; the doc's clause is an averages-style excuse in chaos.
- Principle 13 ("Errors never compound"): the rounding error does not compound in
  magnitude — it *reorganises the tail*, which is worse and invisible to magnitude
  metrics; "never compounds" is not sufficient for chaos.

## The lens: ranked attacks (premise before letter)

1. **Shadowing clause (this run's falsifier, above).** Criterion that should catch it:
   **none exists.** Missing rung: a trapping-statistics criterion — the quantized law
   vs its float oracle on a mixed-phase-space scene (dwell-distribution equality,
   e.g. capped-fraction within 2× and p90 within 1.5×; positive control = the float
   law vs itself plus sub-quantum noise; negative = Q = 10⁻²). B12's family is the
   natural home once its statistic is rebuilt.
2. **§3's averaging carve-out is narrower than the measured refutation.** The doc
   allows orbit-averaging "away from resonance" and carves out only mean-motion
   resonance, but the coupled Floquet gold (3851, 0d8c) measured averaging blind to
   100–127/144 **parametric** pumping bands — a resonance family the carve-out does
   not name. The doc (29 September) predates the evidence and was not updated.
   Criterion that should catch it: the Floquet chart (now the certificate, wiki
   handoff.md) — it exists and already did; this is a doc-debt item, not a new hole.
3. **§2's error model "never compounds".** Refuted at mass contrast: r5 VOID at its
   frozen bar; γ³-weighted per-contact quanta reach 3.7×10⁻² of pair KE at engine Q,
   2.77 median at 10⁴:1 (f3ce, 33f1). Criterion: r5's re-freeze (open direction 1 on
   contact-carry.md).
4. **§2 view premises.** "Crosses once" wrong by an integer (6eae, 8f00); no
   time-transfer law (ace6, 5977, 0b45, fb64 — golds); deflection key needs (b, sense|Q)
   and Shapiro delay (8be2, 9f4a — golds). Criteria: r6 + the missing Seen-value gate
   (2fa4).
5. **§6's cost table.** "Undisturbed orbits ≈ 0" holds only for the engine slice; the
   flyable frame is the view's and its steady p99 is still Θ(N) (62c1, 2df1);
   "AI decisions… unknown" is off-plan (Julien, 30 September). Criteria: F1/T1 cover
   the frame, none covers the table's AI row.
6. **Two-body doll — survives** (report): ν-through-the-energy-map holds at 2PN, worst
   +0.36% periastron at ν = 0.25 (ecfd). Criterion: r3 v3 did its job.
7. **Binet cells — survives in the measured domain** (report): m16/m32 pass every r1
   criterion, m8 too coarse, ~38 crossings per radial cycle; river refraction killed
   (H0205). Letter bug: N = 2πm/ln 2 = 145 at m = 16, not the doc's 128 (cells 1.16:1
   anisotropic).

Blind spot: this lens ran out of calibration budget hunting a heavy sticky tail and
settled for a modest one (max true dwell 1.7×10⁴); stronger cantori (K near a critical
value, or the shipped law) would show the distortion at finer Q. Red-teams overweight
exotic cases; here the exotic case (sea decorrelation) was the easy part and the
player-visible one (trapping lifetimes) took the calibration.
