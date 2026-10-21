Grade: silver

**Abstract.** The checker-named experiment is flown and reproduces: the `beltc` control matches
cbe6's record to the digit (same worst-J vector, kicks 19,772), ddeb's defaults regenerate
(115.41 events, 78×), the zone ladder runs 4.8e-8 → 2.2e-5 (step 4) and fails at step 3, zero
deaths/refusals/captures, Δe step-independent per ship. My adversarial extensions hold: 800
planet periods (2.6e-5, no walk), the untested q=3 zone 5:2 passes at step 4 (2.6e-5), width
×0.33–×3 flat, e-tail 9.0e-5 at 400 P/seed2. **But the headline constant is one octave off: the
engine counts ~33 kicks/Giant-period at the step-4 dial** (329 kicks/10 P/ship; cbe6's own
19,772 = 32.95), so "16/GP → 838×" is a mislabeled rate inherited from cbe6; dial-true
composition is ≈21.9 events/body/belt-orbit → **≈410×**, and the page's adoption sentence
Δs = 2⁻⁴·P_G would fly the failing step-3 dial (2⁻⁵ is certified). ddeb's 78× retraction stands;
≈410× ≈ 10^2.6. Adoption cost: a relabel, not code.

**Reasons.**

1. **Reproduction.** Clean tree, `git apply work/patch.diff`. Control `beltc 4 100 6` → worst-J
   `1.2e-5 … 9.4e-6`, kicks 19,772 — byte-identical to cbe6's `ladder.txt`. `zone31 4 100 16 1`
   → worst 2.2e-5 (regen.log agrees). `beltcensus` defaults → 115.41/78×, seeds 1–3; floors
   16/16/16 → 10.73/838×; plane's 2,700 → 837–841×; wmult 0.5/4 and both design arms match
   ddeb's record. The runner's regen (exit 0) and my fresh runs agree everywhere.
2. **Predictions.** `predictions.md` predates the dossier (file times, bracket structure quoted
   verbatim in the dossier). It pre-declared branch (a) ("step 4 passes → ddeb's premise
   correction retracts") — the branch that fired; the point prediction (step 5, conf. 0.4)
   missed and is reported as missed. Note: the branch-(a) bracket was 280–700× on the label
   convention; the dial-true 410× lands inside it.
3. **Adversarial (mine).** (i) **Libration horizon, 800 P** — 8× the flown horizon, outside the
   author's range: zone worst 2.6e-5 (2.2e-5@100P, 2.4e-5@400P), centre 3.4e-5 — bounded, ≥3×
   margin, no walk. The dossier's open edge (a) does not flip. (ii) **q=3 zone (5:2, 2.9% of the
   belt), priced by the census at the 3:1-measured floor but never flown** — I added a `zone52`
   class: worst 2.5e-5 at step 4 (PASS), 7.1e-4 at step 3 (FAIL); 400 P/seed2 2.6e-5. The
   "weaker ⇒ coarser, conservative" extrapolation is now measured, not argued. (iii) **e-tail,
   400 P/seed2**: 9.0e-5 — 1.1× under the bar, confirming the author's own flag that this is the
   fragile class; does not flip. (iv) **Width ×3 and ×0.33 on the zone predicate**: 1.7e-5 /
   2.3e-5 — the floor is width-model-independent; census ×2 keeps 838× (all classes at one
   floor), so the cliff is placement-side, as claimed.
4. **The octave error (why not gold).** The dial-rate label "step_log2 = 4 ↔ 16 kicks per
   planet-period" is false by 2×: `stats.kicks` (kick events only — `Resolved::Kick`, boundaries
   counted separately) gives **329 kicks over 10 planet periods for one belt ship = 32.9/GP**,
   with the planet doll adding zero; the example's `period` constant is exact in ticks (planet
   returns to θ=0 at t=period). cbe6's own gold record says the same (19,772/100 P/6 ships) —
   the error originates there, was inherited by ddeb's census and this run, and **the dossier's
   verification sentence contradicts its own evidence**: the instrument prints "kicks/planet-
   period per ship: 32.3–33.5" and the dossier calls this a re-confirmation of 16. Consequences,
   all verified by recomposition: composed rate 21.9 (not 10.73) events/body/belt-orbit;
   headroom ≈410× (not 838×; ≈205× one octave finer); one doll-wide Δs overpays ~400×, not
   ~10³×; and the page's "Δs = 2⁻⁴ of the Giant-period grid" is the **failing** step-3 dial
   (16.5 kicks/GP: clean belt 1.8e-4, zone 5.6e-4–1.9e-3) — the certified constant is 2⁻⁵.
   Adopting the page as written would fail B12 at the first flight. The PASS/FAIL ladder itself
   is dial-based and physics-absolute; the retraction of ddeb's 78× (an order-of-magnitude
   claim) survives the correction untouched, and ddeb's own 78× barely moves (its bill was
   256/own-orbit-dominated).
5. **Novelty.** The wiki's open direction 1 named exactly these two arms ("the zone floor for
   q ≥ 2 … and the bridge floor … are the two unflown arms that pin the 78–170× interval");
   nothing in the topic's 116-run history measures a q≥2 zone floor (67be is first-order, 5022
   near-2:1 first-order, cbe6 clean circles only). New measurement, not a repetition.
6. **Page.** Corrected in place: the current-best constants (step-4 dial ~33/GP, ≈410×, ≈205×
   octave-finer), a checker bracket documenting the dial-rate evidence, the `Δs = 2⁻⁵`
   correction, the Refuted entry, the cbe6 standing block (its label flagged), open direction 1
   (800-P and 5:2 now flown), and the Runs line. The current best remains over the 15-line
   budget (as the page already was before this run, per the index); I did not trim further to
   avoid gutting the ddeb/1fd7 conflict resolution — the compile-back belongs to the next run on
   this topic.
7. **Goal fit.** Board macro row 1, as claimed: the interval pins and the per-class Δs constants
   collapse to one dial. PRINCIPLES 33 ("a body resolves only the influences that are
   significant at its own scale") — the census's price list collapsing to one line is that rule
   measured; PRINCIPLES 2 ("error type over error size") — the certificate stays the frozen bar
   on the conserved quantity. The conduct is good: honest prediction miss, honest thin-margin
   flags, kill criteria for the instrument declared and not triggered.

**The one step to gold** (no new flight needed): relabel to the dial-true rate and recompose
from shipped code — give `beltcensus`'s clean-class branch the same floor argument (5-line
edit; it is currently hardcoded at 16/GP with no dial), rerun at 32.7/32.7/32.7 for all five
classes, and the record prints ≈21.9/≈410×; correct dossier and page to "step-4 dial ≈ 33
kicks/GP ≈ 16/conjunction, Δs = 2⁻⁵·P_G". (I verified the arithmetic: every class's rate scales
linearly in its /GP floor; 10.73 × 32.7/16 = 21.9.)

**What the author missed.**
- The 2× dial-rate label, while printing the correct 32.3–33.5 in their own evidence; cbe6's
  kicks count (19,772) was already in the inherited record — one division exposes it. This also
  means **cbe6's gold headline constant needs the same correction** (its floor dial and ladder
  stand; only the "16/planet-period ≈ 8/conjunction" label is one octave low) — worth a page
  note on the next compile.
- The 800-P libration horizon and the q≥3 zones were left argued; both now measured (above).
- Code/prose mismatch: the dossier says the strong <4.1 Hill tail is "kept at 64", but
  `beltcensus` charges every gap<6.3 body at `bf` (16 in the 16/16/16 run) — the strong tail is
  undercharged by ~0.1 events (1%, immaterial, conservative direction disclosed as (c)).
- The `beltcensus` clean-class branch has no floor dial, so the tool as shipped cannot price the
  clean class at anything but 16/GP — the composition's "measured floors" reach only the three
  fine classes.
