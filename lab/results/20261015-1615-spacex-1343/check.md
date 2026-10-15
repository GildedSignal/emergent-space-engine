Grade: silver

**Abstract.** Claim: the passage tail is priced (`knots + 96 B×panels`, 10.74 panels/octave past the 2^10 join; `Passage::compile` pure in its two arguments ⇒ re-mint bit-identical), so the seam's never-demote rule is needed for plunges alone. Reproduced byte-for-byte (bench; five flights via the runner's regen; three more flown by this checker). Adversarial, beyond the author's domain: the curve is universal in w across a second compactness class; held-out w=13/21/29 within ±1 panel; identity 0/64 out to w=100 (w=61 is not "the law's edge"). One domain claim refuted: the cap is on outer radius, not w — star-grazing comets (peri = 1.3 R_star) mint w=20, 25.7 kB, all alive: worst case ~213× the 120 B record, not 157×. Gain: deletes 18.8–25.7 kB per unbound body. Cost to adopt: two-line demote-set change + the shipped accessor, then one digest-identity flight.

## Reasons

**Reproduction.** Clean tree + `work/patch.diff`; `regen.sh` exit 0 (runner) and my own run: every structural number identical — panels/knots/standing byte-for-byte at all 16 w values; slope (68,144−16,592)/(549−12) = 96.0 B/panel; 537/50 = 10.74/octave; join at 2^10 (knots 145→161→saturated, matching `orbit.rs`'s `join = 2^-10`); cycle control 6/10/19/37/58 knots; coast censuses 632/668 B/body; burn exactly 1 passage (w=2, 0 panels, 1,808 B); comet12 2,000 alive at w=14/35 panels/18,800 B (37.6 MB); comet13 990 dead, w=15/19,856 B. Compile µs within jitter (332 vs 327/349 at w=9). Code claims verified: `body.rs:193` `Passage(_) => 4096` (2.26× over at w=2, 4.59× under at w=14); `Trajectory::key()` `None` for Plunge only; `radial.rs:16` unbounded = always candidate; `binding.rs:400` loss radius 2^40.

**Predictions.** `predictions.md` at 16:20:53, dossier 16:31:35 — ordering consistent; the author's own bench/flights outputs were overwritten by the runner's regen, so file-time proof of "before the decisive run" is unavailable, but the regen reproduces the numbers from the frozen patch. P1 held, including the pre-registered held-outs (my w=13/21/29: 34/120/206 vs 33/119/205). P3 held — and generalizes (below). P4 held (tighter than predicted: w=2). P6 held (code). **P2 and P5 failed as written** and are honestly reported with correct diagnoses (join saturation; the loss-radius cap). Under this lab's precedent (1 Oct law red-team: one failed held-out prediction ⇒ silver), that alone caps the grade.

**Attack (three adversarial cases, each beyond the author's domain).**
1. *Second compactness class, bench:* peri ~200× tighter (L=100 vs 1500), e≈1.0 vs 1.5 — knots and panels **identical at every matched w** (145/161/161…; 12/34/206/549…), identity 0/64 throughout. The pricing curve is universal in w, with no compactness term — stronger than the dossier's `knots(compactness)` wording, and unclaimed by the author.
2. *Beyond the sweep edge:* w=70/80/100 all compile (646/753/968 panels, 77–108 kB), identity 0/64. The wiki line "the law's w=61 edge" is wrong — 61 is the sweep's end; no law edge found to w=100.
3. *Tight-peri flights (same r0 as comet12, under the loss radius):* peri = 0.15 AU ⇒ 1,000/1,000 alive at **w=16, 59 panels, 21,104 B**; peri = 0.006 AU (1.3 R_star) ⇒ 1,000/1,000 alive at **w=20, 105–107 panels, 25,520–25,712 B**. The window cap is on the minted outer radius (≈2×r0, loss-radius-bounded), not on w: **"structurally capped at w≈15" and "the honest worst case is 18.8 kB" are peri = 1.2 AU numbers stated as structural.** The formula itself holds at the extreme (105 ≈ 10.74×10 panels; 96.0 B/panel).

**Novelty.** No passage-tail pricing in docs/HISTORY.md or the wiki; 5465/760f proved re-mint identity for *cycles* (doll body; belt), e0f9's seam explicitly never demotes passages. The premise refutation (passages need no retention; the placeholder wrong both ways) is new and moves the board's memory-at-10⁹ line. Page corrections applied in place (below).

**Goal fit.** Board's "bodies in the flyable engine: memory per live body" and "memory at 10⁹". P6 "Store the generator, not the generated" — the compiled arc is regenerable from ~120 B; P1/17 "the best part is no part". No law arithmetic touched: accounting, scenario plumbing, a Linux footprint shim.

**Why not gold.** (a) P2/P5 failed as written; (b) the worst-case/cap sentence is refuted at the physical edge — the adoption arithmetic should use 25.7 kB (213×), not 18.8 kB (157×); (c) the deletion itself was not flown — the demote-passages variant of the seam needs one digest-identity flight, the same bar that separated 760f (priced, not flown) from e0f9 (flown, adopted). Everything that was claimed at the law level reproduces and generalizes; the page's "closed for passages" should read "closed at the law level, unflown on the seam".

## The one experiment that would make it gold

Build the two-line demote-passages variant of the seam (record = key + `outer_radius` + sense/unit, ~120 B), fly it **digest-identity** across the standard ladder plus a mixed-peri comet stream (1.2 AU and star-grazing), measuring in-flight promotion counts and the re-mint bill against never-demote; pre-register the identity and the promotion-ratio predictions. Fold in the corrected worst case (w=20, ~25.7 kB) so the retention working-set arithmetic uses it.

## What the author missed

1. The cap is on outer, not w: star-grazing periapsis (the canonical comet) mints w=20/25.7 kB alive — honest worst case ~26 kB, 213× the record; "w≈15 structural cap" is a peri artifact.
2. The curve is universal in w (no compactness term) — a free strengthening of their own claim.
3. w=61 is not the law's edge (w=100 compiles; 108 kB).
4. "The belt's 43 knots sits on this curve" is unsupported: the flown belt censuses give 632–668 B/body ≈ 6–7 knots (760f: 672 B/body); 43 knots appears nowhere reproducible.
5. Minor: dossier's comet12 "383 MB"/"3.06e-3 kicks" vs regen's 371 MB/2.961e-3 (known wall-schedule nondeterminism); "16× the belt's coast rate" is true only against the 10⁴ rate (1.9e-4) — the 10³ coast rate is 1.86e-3 (1.6×); name the anchor.

## Page

Corrected `wiki/nladder.md` in place: appended the checker note to the current-best paragraph (cap on outer not w, with the two flights; w=61 not an edge; universality in w), amended open direction 4 with the gold experiment and corrected worst case, and set the run's grade in the Runs line. The pre-existing merge conflicts (main vs taleb-b0ed) were left for the integrator — they adjudicate other runs' checker notes.
