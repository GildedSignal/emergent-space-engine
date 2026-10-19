# Predictions — 20261019-0141-redteam-c78d (premise red-team: the aggregate occlusion letter)

Attack: representation.md L59 "Aggregates are one sample each, and the screen caps the
work at about one sample per pixel" (+ L116 "The view ≤ 1 sample per pixel") applied to
**occlusion**: one sample ⇒ one occlusion predicate ⇒ all-or-nothing dimming. The wiki's
direction 5 names "aggregate emitters (partial dimming, not row drops)" unmeasured; 1885
killed the one-sample rule for the **velocity-dispersion** channel (k⁴ spread); this run
attacks the **spatial-extent** channel, which by construction cannot be saved by small σ_β:
it fails at β = 0 exactly, the regime where 1885's belt control reads all zeros.

Instrument (not yet run when this file is written): exact uniform-disc fleets (N = 10⁵,
seed 20261019), circle–circle overlap closed form as cross-check, exact per-ship
retarded-time + segment-vs-disc predicate for the relativistic arm (22d1's law), and a
per-pixel sampling arm (the same L59 line's other clause). Occluded flux fraction f =
(flux remaining)/(total). "One-sample" = one predicate at the aggregate's representative
point (centre; and a random-member median over 20 draws). Static arms: R_p = 1, fleet
radius R_f ∈ {0.01, 1, 3, 10}·R_p, full transit (impact 0) and held-out grazing impact
0.7·(R_p+R_f); relativistic arm: β 0.5 transverse behind the planet, exact predicate.

Pre-registered predictions (from closed forms where they exist; all MC/timing/pixel/β
numbers are blind):

- P1 (control, must pass exactly): N = 1: one-sample error = 0 at every step, every config.
- P2 (safe regime): R_f = 0.01·R_p: peak one-sample error < 5%.
- P3: R_f = 3·R_p, impact 0, centre sample: mid-transit error ≈ 1 − (R_p/R_f)² = 88.9%,
  f_1 hits 0 (total blink) while true f never drops below ≈ 0.889; the error > 80% over a
  window of order the sample's own eclipse width (≈ 2R_p of path), not the fleet's
  (≈ 2·(R_p+R_f) = 8R_p).
- P4: R_f = 10·R_p: mid-transit error ≈ 99%.
- P5: R_f = R_p: error ≈ 0 at exact mid-conjunction (both rules total), peaks on the
  ingress/egress ramps at 30–50%, and the time-above-5% covers more than half the transit.
- P6: random-member sample, median over 20 draws, R_f = 3·R_p: mid-transit error within
  ±10 percentage points of the centre-sample value.
- P7 (the cap's cure, priced): per-pixel sampling at pixel size R_p/2 (fleet spans ~12
  pixels): peak error < 15%; at R_p/8 (~48 pixels): < 5%. So the cure costs ~tens of
  samples per aggregate, not N.
- P8 (relativistic persistence): β 0.5 transverse, R_f = 3·R_p, exact retarded predicate:
  mid-transit one-sample error > 80% (the extent channel survives the light-time geometry).
- P9 (instrument check): MC f vs circle-overlap closed form: |Δf| < 1% absolute at every
  step (N = 10⁵ ⇒ σ ≈ 0.1–0.2%).
- P10 (held-out, grazing): impact 0.7·(R_p+R_f), R_f = 3·R_p: peak error > 60% and the
  blink still total (f_1 touches 0) while true f_min > 0.7.

Kill criterion for the letter (frozen before the run): the one-sample aggregate FAILS if
any config with R_f ≥ R_p shows peak flux error > 5% while the exact law shows partial
dimming (f_true > 0 wherever f_1 = 0). The letter SURVIVES only if every R_f ≥ R_p config
stays within 5% peak error.

What would make this attack wrong: if fleets in this game are always much smaller in
angular extent than the occluders they pass behind (R_f/R_p ≲ 0.1) — then P2's regime is
the game's and the letter is safe there; the census entry would then record the licensed
domain, not a refutation.
