# Predictions (written before the decisive run)

Attack: Binet cells freeze the Binet equation's coefficient at the band's representative
u_k, so stability (sign of 1−6u_k) is a property of the BAND, not of the body's r. The
true ISCO is a point (r = 6M); the band version is a cliff at a band edge. Cases below
were not tuned on; they follow from the frozen r1 convention (u_k at the band's
geometric centre, r_k = 2^(k/m), M = 1).

Held-out predictions:

1. **Misclassified strip.** With m = 16, the band containing r = 6 is [5.9067, 6.1669);
   its centre u_k makes 1−6u_k > 0, so every circular orbit in [5.9067, 6.0) — truly
   INSIDE the ISCO, unstable in exact Schwarzschild — is classified stable. Strip width
   ≈ 0.093 M = 1.56% of 6M. No orbit is wrongly unstable under the centre convention
   (error is one-sided downward: effective ISCO = 5.9067, −1.56%).
2. **Convention mirror.** Under an inner-edge convention (u_k = 1/r_k), the same band
   has 1−6u_k < 0, so orbits in [6.0, 6.1669) — truly stable — plunge. Effective ISCO
   = 6.1669, +2.78%. One-sided upward. Any fixed per-band convention has a wrong strip
   of width up to one band adjacent to 6M, on one side or the other.
3. **Float orbits.** Near-circular at r = 5.95 (exact Binet, h² = r²/(r−3), 10⁻³
   radial perturbation): exact dynamics plunge (u ≥ 0.5) within 150 rad of φ; the
   m=16 centre-convention band dynamics stay bounded (|u − u_eq| < 1% of u_eq) for
   250 rad. Mirror: at r = 6.05, exact stays bounded 250 rad; edge-convention band
   dynamics plunge within 100 rad.
4. **m does not simply halve the strip.** With r0 = 1 (rings 2^(k/m)), m = 32 leaves
   the strip [5.9067, 6.0) unchanged (same dyadic phase of 6), width still 0.093 M;
   m = 64 shrinks it to ≈ 0.028 M. The strip is set by where 6M falls inside its band
   (dyadic phase), not by m alone; worst case is a full band at every m.
5. **Doll phase.** Shifting the ring phase (r0 = 1.3) moves the strip to a different
   width/position: identical black holes get different effective ISCOs depending on
   each doll's ring phase.
6. **r1's frozen gate is blind.** The r1 ISCO cases (L at r = 7, r = 5.5) classify
   correctly under both conventions, and the bound-seed sampler draws p ≥ 6.5 + 2e,
   so no seed sits in the strip. `isco_correct` = 1 while the strip is wrong.
7. **Epicyclic staircase.** The in-band radial frequency √(1−6u_k) is a staircase in
   r; over (6.17, 7.0) the relative error vs √(1−6/r) exceeds 10% somewhere, and the
   jump between adjacent bands exceeds 25% somewhere in (6, 6.5). The smooth GR
   approach ω_r → 0 at 6M (the "feel" of the ISCO) is replaced by a cliff.
8. **View at high c (cost premise).** Doppler sweep factor k = 1/(γ(1−β)) ≈ 14.1 at
   β = 0.99, 44.7 at 0.999: the observer's past cone sweeps through the sources'
   tube-version history k× faster than proper time, so per-frame gather work per
   visible body scales with k and with each body's kick rate — not the flat
   "1 sample per pixel" of the design's cost table.
