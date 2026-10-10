# Predictions (written before the decisive run)

Context: this second-author run fixes the clock bug the blind checker found in
20261010-1816-system-67f2 (force clock advanced 1.5·H per kick vs the body's H;
perturber phase led by ~119 revolutions per 1000 orbits), adds the
quantize-and-carry control (same quantum, exact timing), and reruns both scenes
with Scene B now at the TRUE 2:1. Checker 2's probes (check2.md §3–4) indicate
the core kill survives; these predictions commit me before I measure. The q
ladder, force law and mark cadence are the author's, unchanged, so where the
author's buggy record has a number, I predict the corrected one beside it.

Scene: restricted circular three-body (Sun + Jupiter μ=1e-3 + ship),
Wisdom–Holman split, exact Kepler drift, kicks at the body's own time,
truth at 1024 kicks/orbit (512 for scene B).

Predictions:

1. **Scene A off resonance: the kill reproduces under the corrected clock.**
   a=2, e=0.05, 10³ orbits. Immediate: max|ΔE| within 3× of the author's 8.2e-7
   (the force phase changed; the error scale should not), exponent ≤ 0.2.
   Deferred walks at EVERY q that saves renewals: exponent in [0.85, 1.15] at
   all four q (2,8,32,128 × dv_est), renewals/orbit within 30% of the author's
   36.4 / 10.9 / 2.9 / 0.04.

2. **Quantcarry is bounded where deferred walks (the split rule, cleanly).**
   At the same q = 8·dv_est: quantcarry exponent ≤ 0.5 and max|ΔE| ≥ 10× below
   deferred's. At e=0.3 quantcarry stays ≤ 0.5 while deferred ≥ 0.85.

3. **The author's "discard stays bounded" surprise retracts (it was the bug).**
   Under the corrected clock, discard at 8·dv_est walks: exponent ≥ 0.6
   (author's buggy record: 0.06). The bounded-instrument role passes to
   quantcarry; discard (residue dropped) was never the right control.

4. **True 2:1: deferral distorts the resonant response, and can eject.**
   a0 = 5.2·2^(−2/3), e0=0.02. Deferred pump (e_max ratio vs immediate@64)
   leaves [0.8, 1.25] at the mildest q=2·dvr; at q ≥ 8·dvr either pump ≥ 1.5
   or outright hyperbolic ejection (E > 0) within the 10³ orbits. ψ winding
   (now the true resonant angle) differs from immediate's by more than its
   own q-ladder spread — the reported sign flip in the buggy record does not
   survive, but a phase distortion does.

5. **Convergence probes still gate the replica.** Deferred q=1e-9 and 1e-7
   reproduce immediate's max|ΔE| to 3 digits (accumulator crosses every kick);
   quantcarry q=1e-7 likewise. Discard walks even at small q once it saves
   rounding (q=1e-6 → exponent ≥ 0.4).

Kill criterion for the split-rule claim: if under the corrected clock deferral
stays bounded (exponent ≤ 0.5) at ANY q that saves ≥ 2× renewals, or quantcarry
also walks secularly (≥ 0.8) at the same q, the timing-vs-magnitude split dies
and I report the refutation.
