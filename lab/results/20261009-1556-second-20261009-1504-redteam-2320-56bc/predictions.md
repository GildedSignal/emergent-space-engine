# Predictions (written before any BH / envelope / occultation run)

The checker's named experiment, verbatim: "run the BH-lens transit (opaque
r\* ≤ 3M, or capture-bounded): births at doll entry plus the wrap family,
missed-image brightness and miss fraction measured the same way, and re-scope
the claim to r\* < b_E (compact lenses), folding in the occultation-recovery
blindness as the normal-star symptom."

All predictions below are fixed before running. Instrument = the shipped
`falsifier.py` tracer and continuation gather, imported unmodified (only the
scene globals M stays 1, R_STAR set per part). Same measure as the author:
image = sign change of the signed miss s(θ) at the source sphere; brightness =
1/|ds/dθ| relative to image 1; visibility bar = the author's ≥ 2%.

Scene (same as the author's): O=(0,0), S=(10⁴,0), lens M=1 at (2000,η);
θ_E ≈ 0.04, b_E = θ_E·D_OL = 80; BH capture b_c = 3√3 ≈ 5.196, θ_c = b_c/D_OL
= 2.598e-3.

## BH transit (r\* = 3M), η 400→20→400, 59 frames, author's cadence

1. **P1 (doll entry, cold start).** Tracker seeded with the single no-lens
   crossing (θ=0) — the previous frame's gather when the doll's deflection
   memo was not yet on this tube. Truth: the n=0 image pair exists at EVERY
   frame (r\* = 3 ≪ b_E = 80: no occultation possible; capture cuts only
   |θ−θ_lens| < θ_c). Prediction: continuation stays at 1 image for 100% of
   frames — miss fraction 1.000 — and the missed strong-side image is
   player-visible (≥ 2% of image 1) from entry onward, rising from ~2–10% at
   η=400 to ~30–100% at best alignment. The birth locus is doll entry, not a
   caustic: the missed image exists already at the first lensed frame.
2. **P2 (generous seed, the author's convention).** Seeded with truth at
   frame 0 (both n=0 images): the gather holds BOTH through the whole transit
   — 0 missed frames, no divergence, no double-track (no occultation, no fold
   for the n=0 pair; Fermat monotonicity per branch). So for a BH the n=0
   failure is concentrated at entry, not during transit — the opposite
   emphasis from the star.
3. **P3 (wrap family).** Zoomed grids at θ_c±: wrap images exist at ALL
   alignments (sampled η = 400 and 40, both sides), demagnified vs image 1 by
   a factor in [10⁻³, 10⁻¹] per winding (log-scale prediction; I do not trust
   my 2D vs 3D e^{−π}/e^{−2π} discrimination). Verdict rule fixed in advance:
   if every wrap image is < 2% of image 1 the wrap family is a mechanism gap
   with no player-visible consequence (benign case, reported as such); if any
   is ≥ 2% it is a visible miss and strengthens the claim.
4. **P4 (control, must pass or VOID).** On branches the gather holds,
   continuation matches the truth image (|Δθ| < 6e-4), converged, ≤ 6
   iterations, at every frame.

## Star symptoms to fold in (reproduce the checker's attacks)

5. **P5 (occultation recovery, r\* = 100 ≥ b_E, "normal star").** Transit
   η 400→5→400: truth goes 1 → 0 (occulted) → 1; the gather, which held the
   branch before occultation, holds 0 for 100% of post-occultation frames
   (≥ 20 frames with truth=1, cont=0). Emptiness is absorbing: same missing
   enumeration, common-case symptom.
6. **P6 (envelope).** Sweeping r\* ∈ {50,60,70,80,90,100} over η ∈ [0,400]:
   two-image alignments exist only for r\* < b_E ≈ 80; at r\* ∈ {90,100} the
   count is zero everywhere (the would-be secondary is born occulted).
7. **P7 (held branch near the fold).** Star r\* = 50, tracker seeded with
   BOTH images at η=40, swept outward: the held secondary dies by η ≈ 45–60,
   well inside truth's η_crit = 81.6 (reproduces the checker's finding that a
   held branch is lost near the fold at the gather's own budget).
