Grade: gold

**Abstract.** e56b closes chaos-shadowing's game case, and every number reproduces: a coherent
fleet crossing a belt is not a wall-reflection train (no 4·w clock — |r| at 4·w = 0.039 on the
H=24576 arm; wall hits a rain of 4-10/chronon vs a block's n/2) but one ~14·extent season
(39.2-39.5 contacts/fleet body at n=1600) plus an area-extensive hot plateau: late mean × box
width 438k/431k/466k/**417k (my bs4)**, 15.5× the matched cold control, stationary to H=24576;
free space: one season, walls=0. Zero-code adoption: budget one season, treat a post-crossing
~15× rate step inside a confined region as standing cost — trigger confinement × optical depth;
no train guard for fleet×belt, ever. Two constants corrected on the page (below); substance
unaffected. Premise shown wrong twice (train mechanism; checker2's coherence reading).

## Reasons

1. **Reproduction.** Runner's regen green (`REGEN_DONE`, `DETERMINISM_OK`); my own clean rerun
   of mb1600_bs2_s1 is digest-identical (`012568e5…`). Every dossier number matches the
   regenerated `work/final.json`/`table.txt`: late means 1007.5/496.0/357.0 and ×w =
   438k/431k/466k (6.3% spread); 15.5× vs controls 31.9/32.4 (F64 0.91/0.92, walls ≤ 3/ch);
   block means 3373→2286→2209 (−3.4%); free peaks 1152/960/640 with late 0.41-1.56, walls=0;
   the 65× peak-window claim measures exactly 65.0 (58 at n=400); season duration 2368 ch =
   13.6·extent; spacings 2752/2304 vs predicted 3480 and 1472/1920 vs 1800 as stated.
2. **Predictions.** File times put predictions.md before grid.log; kill branches were
   pre-stated for P1/P5. P1 and P2 fired their kill branches — honored as the central result,
   not hidden; P3's alternative branch fired; P5 held (its matched-rate half honestly voided);
   P4 half-held, P6 held-in-exponent, P7 held. This is the pre-registration working as designed.
3. **Adversarial (4; two outside the flown domain, one untested axis — all confirm).**
   (a) boxscale 4, beyond the {1,2,3} ladder: late 239.5, late×w = 417k, inside the band;
   walls still rain (9/ch). Extensivity survives another rung. (b) Free space at n=6400, one
   octave past the flown free arms: one season (peak t=2048, the geometric meet time), walls=0;
   the flat tail is untestable there at H=8192 (the season itself is ~4.8k ch) — a domain note,
   since the author's free claim was n ≤ 1600 where it holds. (c) σ = q/256 fleet dispersion —
   the axis no arm had flown, a genuinely generic formation: same season (39.93/fleet body),
   same plateau (492.6 vs 496.0), autocorr top lag 64 ch. "Energy, not formation" passes its
   hardest probe. (d) The one methodology gap I found — analyze2's H=16384 autocorr cannot see
   4·w = 6840 at n=6400 — closed by computing it on the long arm: |r| = 0.039, top-5 lags all
   ≤ 320 ch.
4. **Novelty.** The mixed fleet×belt scene, the wall-reflection train and free-space geometry
   are named unflown in 90b7's paragraph (and checker2's bracket) on this very page;
   docs/HISTORY.md has no fleet×belt/plateau entry. Checker2's "the fleet stays coherent
   through a dilute cloud forever" is refuted with mechanism evidence (no block wall signature
   ever; σ-invariance; free-space dispersal), replacing a misreading with the attractor.
5. **Page corrections made in place (the two overstatements I found).** (i) Season 1 is
   1.15·per_row at n=400, not 1.35 — that constant holds only at n=1600 (1.36); linear-ish in
   per_row, not one constant. (ii) The echo ratio at per_row 29 is 0.60-0.63 on a fixed
   2048-ch window, both seeds agreeing; the reported 0.31-0.35 (s2) and the discarded 1.0 (s1)
   are the same trough-detection artifact in opposite directions. The per_row 29-vs-15 flip
   (echo clearly below 1 vs ≥ 1) is robust, so the arrival-time-diffusion reading stands.
   A checker bracket with my probes is appended to the page per its own convention.
6. **Goal fit.** Board item 4 (allocator) into the belt wiring: deletes a component that would
   never be needed (no train guard for fleet×belt) and hands the wiring a dimensionless
   trigger. PRINCIPLES: "Compute only surprises" (3) — the crossing is the one surprise, what
   it leaves is a rate step; "Regimes are chosen by dimensionless numbers" (4) — confinement ×
   optical depth; "A failed expectation is not automatically a failed method" (9) — two dead
   predictions are the result. Gold bar: premise shown wrong, reproduced, adoptable in one
   step (zero code).

## What the author missed

- Both the season constant and the echo constant were analyzer-window artifacts (in opposite
  directions on the two seeds); a fixed-span echo window was the obvious robustification, and
  it changes the quoted echo from 0.31-0.35 to 0.60-0.63 without changing any verdict.
- Per-body velocity instrumentation was skipped, so "velocity exchange / two-temperature" stays
  [INFERENCE] (the dossier says so); σ-invariance now carries that claim indirectly.
- Free-space flatness at n=6400 remains unflown (needs H ≥ 16k); cross-n rate comparisons are
  not area-normalised (box height grows with the fleet) — both stated by the author.
- The plateau's slow decay constant and the game's gravity-held (wallless) belts stay open —
  correctly named as the next run's questions.
