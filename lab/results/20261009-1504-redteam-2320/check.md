Grade: silver

**Abstract.** Claim: representation.md §2's view gather (Newton continuation from the previous frame) has no mechanism to *find* crossings lensing adds: in a lens transit it misses the caustic-born second image in 100% of frames. Reproduced: 9/9 two-image frames, missed image 4.7–5.1° away, 0.41–0.78 as bright; control passes; instrument stable under grid and step refinement; predictions pre-registered. Novel: no gate or rung covers image enumeration (B3/B16 single-path; r6 unfrozen). Adopt: one design sentence (±b branch enumeration per lensing doll, or per-pixel gather) plus one r6 criterion. **Scope overstated**: visible secondaries exist only for r* < b_E ≈ 80 here (r*≥80: zero); normal stars occult. The scene (r*/M=50) is compact-lens territory; the in-goal case (black-hole lens, P6) was stated, not run.

## Reproduction

`python3 falsifier.py` (14.7 s here vs 22.8 s author; summary identical otherwise, every quoted number verified). k=25 example exact: truth {−0.0262, +0.0630}, tracked {−0.0262}. Birth at the limb verified: secondary r_min = 52.7 at η=72.4 (r*=50), rising with alignment. Rel-mag series symmetric [0.412 … 0.776 … 0.412]. Quote at representation.md:57 verbatim; law.md "Observation" carries the same per-tube sentence. `work/patch.diff` empty — no tree edits. File times: predictions 15:12:05 → script 15:20:01 → output 15:20:24; P1's 1.6× miss was honestly reported half-held.

## Attacks (5, beyond the author's)

1. **Scope envelope (decisive).** Swept r* at M=1, D_OL=2000: visible secondary exists only while r* < b_E≈80 (50→41/100 alignments, 60→24, 70→11, 80→0, 90→0; full transits at r*=100 and 500: zero two-image frames). The dossier's lens note "normal stars give narrower caustic tubes but the same birth" is **falsified**: past b_E the star occults, no birth exists to miss. "Plain star-transit — no black hole, no exotic case" is wrong about the scene it used (25 r_s matches no real star); the finding's true domain is compact lenses — which the goal does contain (billions of black holes), but that is P6, untested.
2. **P3 closed (was vacuous).** Seeded the tracker *with* the secondary at η=40 and swept outward: it holds it one frame, drops it cleanly at η=50 (truth keeps it to η≈81.6), no double-track anywhere, exit clean. P3's "dropped cleanly" confirmed; and the miss is worse than reported — even a held branch dies near the fold under the author's own generous budget.
3. **Occultation recovery — the common-case symptom the author missed.** r*=100, transit 5→400: for all 36 frames after occultation ends (η≥45.5), truth has 1 image, the gather holds **0** — the tracker's emptiness is absorbing. The same missing enumeration makes a *normal* star/planet transit delete the source from the view permanently (under this reading of "starting from the previous frame's"). This, not caustic birth, is what "every dogfight near a planet" actually meets.
4. **Instrument.** η=60: 2 images stable at 16001-point grid and dphi 0.0025, thetas identical to 5 decimals; birth-side r_min confirms limb emergence. Note: scalar-vs-grid |Δs|=0.0 shares the integrator (consistency, not independence); the dphi halving (1.4e-8) is the real convergence evidence — sufficient, since image *existence* is robust to 10⁻⁸ shifts.
5. **Novelty.** No HISTORY entry, gate or rung tests image count/enumeration at the gather; B3 ("deflection within 1%") and B16 (moving-lens deflection) judge single paths; r6 absent from lab/rungs/ (unfrozen, cost-only in §7). The §1 arithmetic check verified by hand (2π·16/ln2 = 145.1 ≠ 128).

## Goal fit

Pre-freeze premise red-team, which AGENTS mandates; principle 30 ("navigation, knowledge and dynamics those need to be perfect") and 19 (branch enumeration is the representation; threshold-spawned probe rays would be the bandaid). The fix is one sentence and the proposed r6 criterion (image count vs exact backward trace over a transit, planted continuation gather must fail) is concrete and two-sided.

## Why silver, not gold

The mechanism hole is real, reproduced and adoptable, but the Claim sentence's scope ("plain star-transit — no black hole, no exotic case") is measured false at the margin that decides which scenes exhibit it, and the actual in-goal instance (black-hole lens) is P6, stated and untested. Same class of deduction as the 1 October law red-team (real and adopted, not gold on a misreported margin).

**The one experiment:** run the BH-lens transit (opaque r* ≤ 3M, or capture-bounded): births at doll entry plus the wrap family, missed-image brightness and miss fraction measured the same way, and re-scope the claim to r* < b_E (compact lenses), folding in the occultation-recovery blindness as the normal-star symptom. That is one afternoon on the existing script.

## What the author missed

- The r* < b_E envelope: image birth is a compact-lens phenomenon; normal stars occult (my #1).
- The absorbing empty tracker after occultation — the common-case failure of the same premise (my #3).
- A held secondary branch is lost within one frame near the fold at the author's own budget (my #2): the gather is more fragile than "convergence is safe" suggests, though still without divergence.
- P6's BH case is the goal's named object and was left as prose; it, not the compact star, carries the finding's weight.
- The 2D magnification measure is the right 2D-native one (1/|ds/dθ|), but player-visible brightness of point images in the 2D game is a mapping choice the dossier states without argument.
