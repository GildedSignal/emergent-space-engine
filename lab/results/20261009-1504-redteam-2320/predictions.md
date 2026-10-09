# Predictions (written before the decisive run)

Setup (2D, geometric units M=1, the design's own Binet photon law u'' = 3u² − u,
integrated in float as the truth oracle): observer at (0,0), source at (10⁴, 0),
lens star M=1, r* = 50 at (2000, η) with η swept 400 → 20 → 400 over 80 frames
(a transit across the line of sight; equivalent to observer motion, which B16
already separates out as a deflection-accuracy question, not an enumeration one).
Continuation gather = per-image warm-started secant/Newton on the arrival angle,
exactly representation.md §2 ("Newton's method finds the crossing, starting from
the previous frame's"), seeded with the truth at frame 0, no re-enumeration.

Cases not tuned on (I fixed the numbers from the small-angle lens formula before
running anything):

1. **P1 (birth):** the second image exists only inside the caustic tube,
   |η| < η_crit = 4M·D_LD/(D_S·r*) = 0.064·2000 ≈ 128. It is born at the star's
   limb (r_min ≈ r*), at angular offset ≈ r*/D_OL = 0.025 rad from the lens,
   ≈ 1.5–3° from image 1. Prediction: truth has 2 images inside, 1 outside;
   continuation NEVER acquires the second image (0% of inside frames).
2. **P2 (visibility):** the missed image's magnification (1/|ds/dθ| relative to
   image 1) is ≥ 2% over most of the missed window → player-visible as a companion
   point on a dark sky, and wrong "knowledge" (duplicate source) for navigation.
3. **P3 (death):** at caustic exit the stale branch either fails to converge and
   is dropped cleanly, or briefly double-tracks image 1. I expect dropped cleanly
   (secant stalls near the limb). If it double-tracks, the view over-brightens.
4. **P4 (control, must pass):** outside the caustic, continuation == truth
   (1 image, converged, ≤ ~4 iterations/frame). If this fails my instrument is
   broken, not the design.
5. **P5 (survivor):** on any persistent branch, warm-started Newton/secant stays
   well-behaved (no divergence, small iteration counts) at any alignment —
   consistent with Fermat monotonicity (d/dt of [arrival − emission − optical
   path] < 0 per branch). The exposure is branch *enumeration*, not convergence.
6. **P6 (untested but stated):** near a black-hole lens the wrap family (b →
   3√3 M) exists at ALL alignments in 2D, so births occur at doll entry/exit
   (regime change), not at a caustic line; same mechanism gap, harsher geometry.
   Not run in float today (star transit is the cheaper, more common case).
