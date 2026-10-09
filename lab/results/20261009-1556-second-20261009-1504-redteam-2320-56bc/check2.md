Grade: silver

**Abstract.** Second author on the view-gather's enumeration hole. Every number
regenerates bit-identically from the shipped scripts in a clean tree (five
JSONs; wall times within 5%; the star record matches the first author's). The
BH strengthens the kill: at r\*=3M truth has ≥2 images at all 59 frames, the
cold-started continuation holds 1 (miss 1.000), the missed strong image is
3.5–77.6% of image 1; even a generously handed strong branch dies at frame 1
and never recovers. Normal stars: absorbing emptiness, 36/36 post-occultation
frames. My attacks confirm the scope physically (D_OL=1000: boundary moves to
b_E≈60 as r\*<b_E predicts) and find the naive empty-tracker re-seed fails at
occultation exit: only true enumeration fixes it. Cost: one design sentence
plus r6 criteria.

1. **Reproduction (clean scratch tree, shipped scripts, patch.diff empty).**
   `falsifier.py` 14.7 s, `diag.py` 0.13 s, `bh.py` 21.6 s, `star-extra.py`
   24.6 s, `envelope.py` 17.7 s, `wraps.py` 10.8 s. All five output JSONs are
   byte-identical to the stored ones modulo `wall_s`; `falsifier-out.json`
   also matches the first author's `falsifier-out-author.json` exactly. Star:
   9/9 two-image frames missed, η_crit 81.6, rel-mag 0.412–0.661, control
   outside passes. BH cold: 59/59 truth≥2, miss 1.000, cont always 1, missed
   strong 0.0353–0.7763, ≥2% every frame, held branch on truth, ≤5 iterations.
   Generous: strong lost at frame 1, held fraction 1.7%, n_cont after frame 1
   = 1. Occultation: 36/36 post frames truth 1 / cont 0. Envelope: 6, 5, 4, 0,
   0, 0. Fold: drop at η=45 against 81.6. Census b 7.9 (0.15%) → 18.5 (3.6%).
   Every dossier number I extracted matches.

2. **Predictions.** `predictions.md` mtime 16:04:27; every decisive script and
   output ≥16:14 (the 16:02 falsifier re-run is the record reproduction, not
   new science). P1, P4 (control), P5, P6, P7 held. **P2 was refuted** —
   honestly reported, in the strengthening direction (the handed strong branch
   dies at frame 1; `diag.py`'s replay shows the fallback step jumping to the
   domain clamp, then the secant landing in the direct image's basin). P3's
   numeric band missed low (pre-registered decision rule held). By the lab's
   own bar ("the held-out predictions held") and the 1 Oct precedent, a
   refuted pre-registered prediction blocks gold however honest the report.

3. **Attacks (my own, four).**
   - **Geometry scaling:** at D_OL=1000 (b_E≈60 predicted) two-image
     alignments are 5, 4, 1, 0, 0 for r\* = 40–80: the compact-lens boundary is
     the physical Einstein radius, not an artifact of the one scene. The
     re-scoped claim generalizes.
   - **The dossier's hatch 3 is false near exit:** re-seeding the empty tracker
     with the undeflected direction recovers the post-occultation image at
     η=177.2 and 339.2 but **fails at η=96.2** (truth at θ=−0.023, 0/1
     recovered in 6 iterations). A cheap rescue is insufficient; the hole is
     deeper than the dossier assumes — this strengthens the kill and corrects
     an escape hatch.
   - **Brightness proxy:** ray-density ratio for the missed strong image at
     entry 47/1283 = 3.66% vs slope-based 3.53% — the 1/|ds/dθ| measure is
     good to ~4%.
   - **Wrap family:** classifying zoom roots by impact parameter, the wrap-only
     range is 3.24e-6 – **2.32e-3** (the η=1600 +side root at offset 1.06e-3,
     b=7.9), so both dossier figures understate the top end (claim 2e-4,
     evidence 1.0e-3). Still ≥8× below the 2% bar; the benign verdict stands.
     Refinement shift 6e-9 and the hold-test failure (a handed wrap fails the
     shipped tolerance at the first frame even with a 40× march) both
     reproduce.

4. **Novelty.** docs/HISTORY.md has no entry on image enumeration or caustic
   birth in the gather; H0211/H0213 record "the gather finds each crossing by
   Newton from the last frame's" as implemented, and representation.md:130
   scopes r6 to cost only ("Newton iterations and samples per frame") — the
   dossier's point that r6 would freeze a blind gather is accurate against the
   live docs. The quoted premise (representation.md §2 / law.md:53) is verbatim
   in the tree. This run is the checker-named continuation of today's first
   author run (not yet journaled), with the scope correction (r\*<b_E) and the
   BH/occultation evidence being new.

5. **Goal fit.** Principle 30: "what really matters is navigation, knowledge
   and dynamics those need to be perfect" — a gather that deterministically
   drops a ≥2%-bright companion image for a BH at every alignment and never
   re-acquires a source after a plain occultation is wrong knowledge, not a
   cost issue. Principle 19: the fix proposed (enumerate the ±b branches per
   lensing doll, or go per-pixel) changes the representation; probe rays and
   rescue hacks are the bandaid. Adoption is one design sentence plus two r6
   behaviour criteria — zero engine compute.

**The one experiment for gold.** Pre-register predictions against the
*corrected* claim on genuinely new held-out cases and run them: (i) two
overlapping lensing dolls on one sight-line — the ±b enumeration combinatorics
the fix must bound (untested by author and by me); (ii) the fix sentence itself
at the worst gradients: branch enumeration from the doll's ±b at BH entry and
empty-tracker re-enumeration near occultation exit, where my η=96.2 result
shows the naive rescue fails; (iii) the geometry scaling as a prediction (my
attack already confirms it). If those hold, gold.

**What the author missed.**
- The wrap-brightness top end is understated in both dossier sections
  (measured 2.32e-3, not 2e-4/1.0e-3); verdict unaffected.
- Escape hatch 3 was asserted, not measured, and is false at occultation exit —
  the cheapest version of the fix does not work there.
- No second geometry was run (cheap, and it hardens the r\*<b_E scope).
- Multi-doll sight-lines and 3D geometry remain untested (acknowledged in the
  lens section); the 1/|ds/dθ| brightness is a 2D proxy (acknowledged).
