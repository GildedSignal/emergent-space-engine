# Check — 20261006-0346-inversion-8cee

Grade: silver

## Abstract

Inverted on the r8/q-candidate "zero misses": the shipped encounter check (`crates/encounters`, fixed k = 24/64/256 Δr·Δv sign brackets) misses real encounters exactly where no frozen belt ever looked — 17/241 (7.1%) and 9/167 (5.4%) at e ∈ [0.60, 0.95], 2/3890 on a clustered-phase fleet wall; work per encounter inverts 309 → 505,314 evals (1,600×) across families. All five scenes reproduce bit-exactly; I re-confirmed 16/28 misses with the independent dense finder (all held) and a fresh-seed scene misses 6.3%. `make_belt` caps e at 0.5, so the verification premise is shown wrong. Adopt now: two scene families in every frozen encounter verify set. The certified-step guard is specified but not built — one experiment from gold.

## Reproduction

- Built `enc` (byte-identical copy of `crates/encounters/src` + `bin/invert.rs`; `work/patch.diff` empty, tree otherwise clean). All five scenes reproduce exactly: ctrl 2093/0/0 (309 evals/enc), highe-align 241/17/0 (254,060), highe-rand 167/9/0 (505,314), formation 398/0/0 (24,901), wall 3890/2/0 (2,485). Cone rejection 11 pairs at 73.6–285.8 ρ; `max_util_cross` 0.876; highe-align sections [0, 5696, 20180] (no Cross) — every dossier number matches the saved JSONs and my re-runs. Each command seconds; machine load 1.6–3.2, memory far under budget.
- The misses are genuine. Truth and the comparison-based dense scanner (Halley states, golden refine, no brackets) agree to 6 digits per event. The author's artifacts validate only 3/28 misses individually; I validated 13 more (all 9 highe-rand, plus highe-align (130,190), (0,200), (135,137), wall (39,151)): every one a real sub-ρ minimum the method never samples. Distinct events, distinct decision rules (the 5-October lesson held).
- Mechanism confirmed in shipped code: `pairs.rs:387` fixes k; (28,121)'s dip is 0.048 wide inside a ±6.34 window sampled at ≈0.11; wall (6,17)'s terrace is ≥ 0.24 wide against a 0.00228 half-width. The proposed fix's Lipschitz certificate already exists in `numeric_window` (`pairs.rs:317`).

## Adversarial cases (mine)

- Fresh seed (`highe-align-s2`): 16/252 = 6.3% missed — not seed luck. Anti-aligned apsides: 8/179 = 4.5%. Wall clustered 6× tighter: 1/17060.
- Near-parabolic `para-align` (e 0.90–0.99, aligned): **0/326 missed**. The failure is not monotone in e; it is the window-width × k interaction at mid-high-e crossing belts. B13's near-parabolic territory is fine in the crate.
- False reports: 0 in all nine scenes — prediction 4's failure is robust; the check's failure mode is misses only.

## Predictions

`predictions.md` (03:56:19.7) precedes the decisive highe-align start (≈03:56:22; JSON 03:56:57 minus 35.05 s wall) — barely, but before. The predicted mechanism (Cross-window Taylor) was wrong — highe-align has no Cross sections — which is itself good evidence of genuine pre-registration. P1 (misses at high e) and P2 (aligned ≥ random) held; P3's condition was moot; P4, P5b and P6b failed, all disclosed. Honest scorecard. By lab precedent (1 Oct red-team), failed held-out predictions cap the grade below gold even when honestly reported.

## Novelty

`make_belt` caps e at 0.5 (`belt.rs:49`) and phase-mixes; it is the crate's only belt generator, so the r8/q-candidate "zero misses" was measured outside the game's e and phase space. Overlap to state plainly: the board (6 Oct overnight) already records q-candidate-degree's finding that a proposed Wide *tightening* misses 23% at e 0.7–0.9 (dropped). This run's delta — the *shipped* check itself misses 5–7% at e 0.6–0.95, with per-event anatomy and the crate-level cost inversion — is new. H0214's B13 losses are the plane's representation, not the crate.

## Goal fit

Board focus item "finding encounters without work per orbit" and the top scaling risk; nothing deleted, a premise corrected before the motion law v2 freezes. PRINCIPLES: "Floats may explore; only integers decide canonical outcomes" — the bracket is a float sign decision deciding a canonical outcome at tuner-chosen resolution; "A failed experiment kills that configuration, never the method" — this kills the tuned bracket, not the Binet-cone/first-hit representation.

## The one experiment for gold

Build the guard: size k inside `check` by the Lipschitz bound `numeric_window` already proves (max relative speed × step ≤ ρ/2), and promote flat-D/terrace pairs to Full by the same test that demotes Cross to Wide — or show the certificate fits the integer first-hit layer. Pre-register, then run the two new scene families plus my variants (fresh seed, anti, para, wall-tight): zero misses at bounded cost. That converts a premise-kill into an adoptable law change.

## What the author missed

- "Every miss confirmed by two finders" outran the record: the in-run dense opinion covered 3–4 orbits on 1/24 of pairs and confirmed none of the 28 directly (`dm_list` empty everywhere); only 3/28 were individually validated in the artifacts. It survives my check (16/16 attempts held), but the claim as written was unearned.
- Misses are not monotone in e: near-parabolic misses zero; the regime is long Wide windows at mid-high e. "High eccentricity" over-generalizes, and the mild wall misses (the method still reports sibling events for the same pair in the same passage train, e.g. (6,17) at t = 37.34 inside the terrace; (39,151) 7 of 8) should have been separated from the highe dips, which are wholly unreported close approaches.
- The board's q-candidate-degree entry (Wide tightening, 23% at e 0.7–0.9) is the nearest prior measurement; the dossier argues the verification-space gap but never states its result against that entry.
