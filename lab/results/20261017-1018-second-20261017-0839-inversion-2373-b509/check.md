Grade: gold

**Abstract.** The shipped conjunction calendar (`tier::arm_pair`, `dioph.rs` first-hit) is
measured on fleets: it is sound and it deletes the per-rebuild window sweep, closing the
missing 10⁹ fleet ledger row as a certificate term (keys F* = 3,232–6,463 at L = 25–100,
conditional on standing-contact wiring) plus population terms no certificate deletes (train
firing flow 50,731 cores at F = 10⁴; kick-created firings ~2,500 cores). Reproduced
bit-identically on both seeds in a clean tree (runner regen and this checker's independent
rerun): arm 1.01–1.16 µs/pair vs the exact check's 57.7/414.7 µs, so 2373's sweep ledger
(3.24 µs at a 1-orbit horizon) understated the shipped sweep 129–143×. Checker: soundness
holds on clustered formations and high-e fleets (0 dropped at 379k–473k events); γ = 2.00
at F = 25,600; a full F = 10⁵ enumeration validates the subsample (478,782). Adopt: one
wiring step, every constant measured.

## Reasons

1. **Reproduction.** `regen.sh` exit 0 (runner) and my own clean-tree run of both
   instruments: every deterministic field identical on both seeds (armed counts, truth
   events, negctl drops, due histograms, kick flip counts); only µs timings move (≤7%,
   shared box under 3-way load). The composition constants were recomputed by hand from
   the JSONL (F* 6,463/3,232; train 51,344 cores, F* ≈ 88; kick rows 10,213/403,392; the
   event floor 1.6×10⁵ cores) — all match `work/composed.txt`. The patch is print-only
   (two new example files; zero shipped lines) and reverse-applies cleanly.
2. **Predictions.** `predictions.md` (10:46) precedes the decisive outputs (11:07+); fitted
   on pilot seed 7 only. 14/16 bands hit; the two misses are disclosed and neither helps
   the claim (P7 cap_us 27.5 µs vs ≤15 — the composition uses the larger measured value;
   P10's histogram model died under the pre-registered K4, replaced by direct re-arm at
   interval 10 before composing). K1/K2/K3 did not fire.
3. **Attack (mine, seed 31337, fresh instrument on the same shipped APIs).**
   - *Clustered formations* — the taleb-09b5 killer regime, never tested by the author's
     truth arm: σ_l = 0.05, 0.01 and a clustered train, F = 2,000, H = 100 orbits:
     383,516 / 473,248 / 378,524 events, **0 dropped, 0 added** each.
   - *High-e fleet* (σ_e = 0.2, e to the 0.5 cap): 15,100 events, 0/0.
   - *Outside the tested range*: keysev at F = 12,800/25,600 (author stops at 6,400):
     γ = 2.000 on that decade — the event-floor claim extends.
   - *Subsample audit*: full F = 10⁵ keys arm pass (296.5 M pairs) gives 478,782 armed vs
     the 2,000-row estimates 477,050/473,900 — the estimator is good to ~1%.
4. **Novelty.** The mechanism is shipped and known (r8-v2 lead; `189e` killed the
   CF-calendar *as a close-conjunction predictor* at belt scale — a different use); no
   earlier run measures `arm_pair` on fleet populations (wiki Runs checked). New: the
   per-pair price at sound horizons, the soundness gates with dropping negative controls,
   the 129–143× horizon correction of 2373's published ledger, keys F*, and the two-term
   closure of the missing row.
5. **Goal fit.** Board item 2. Deletes a component (the per-rebuild sweep as the fleet
   representation: 57–370× per pair at horizons a sound rebuild can actually use) and
   shows a published premise wrong (2373's 36/383/4,500-core row). PRINCIPLES #3 "compute
   only surprises" — the sweep paid for empty windows every rebuild, the calendar pays
   exactly the firings, and where the firings overran the budget (trains at 10⁴) the run
   says so instead of hiding it. #19: the window was the drowning car for fleets. The
   negative answer at F = 10⁴–10⁵ is reported with the same numbers as the positive one.

## What the author missed

- **One dossier constant is wrong**: "under shipped per-interval re-check semantics a keys
  fleet pays armed×31.6 ms per interval (2.4×10⁸ cores at F = 10⁴)" — that formula gives
  4,775 × 33.0 ms = 157.6 s per fleet-interval ≈ **5.6×10⁴ cores**; 2.4×10⁸ appears to be
  the belt-stream formula (2N×31.6 ms) misapplied. Same verdict (far OVER 4), wrong number.
- **The formation regime is sound but unpriced.** My clust cases show the calendar arms
  19% of window pairs on a clustered train (383,858/1,991,577) vs 0.18% on keys — the
  certificate-term advantage shrinks exactly in the regime fleets are flown (taleb-09b5).
  fleetcal has no clust arm; the page's formation cost row remains 2373's window quadratic.
  That is the next run's experiment, not a flaw in this one's stated domain (keys/train).
- **The wiki page violated the schema**: it dropped 56 of the 57 append-only run lines and
  the Domain paragraph, and carried three numbers that match no stored run ("F* ≈ 2,000"
  in its own run line, 1,877 train kick-firings vs the measured 1,924/1,862, 58.8/426.6 µs
  vs the stored 57.7/414.7). I corrected the page in place: runs restored (deduped against
  main), Domain restored and extended with this run's domain and my adversarial results,
  numbers aligned to the evidence.
- x86-only timings (disclosed; the ratios and exponents are unit-free). Soundness gates
  stand at F = 2,000, H = 100 orbits; the F = 10⁵ rows are subsampled extrapolations
  (disclosed, and now audited).
