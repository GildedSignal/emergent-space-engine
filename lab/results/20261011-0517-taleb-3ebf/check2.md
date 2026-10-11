Grade: silver

Abstract: Claim: the phase-neighbour certificate's rank-locality is a property of equal periods, not concentration — under element-clump grouping a two-fleet battle silently drops 61–72% of encounters, and a different-period interception has no along-orbit rank (cross partners at median ~n/2, max 0.70·n; cone cross pairs exactly n², exponent 2.00), so the planned gate cannot fail on the game's central event. Reproduced bit-identically (35.9 s, all 8 scenes, all keys incl. exponents 2.00/1.97–2.02/1.91–1.98); held out on three fresh geometries. One headline is contradicted by its own log: zero-miss union certificate is 9.4× fewer pairs (k=32), not "19×, zero misses" (18.7× carries a 2.1% miss). Adoption: two gate scenes + grouping-key edit; the fix's period-spread boundary is unmeasured.

## Reasons

**Reproduction.** Clean tree, empty patch (the lib is a verbatim copy of `crates/encounters`; only `src/bin/battle.rs` added). `cargo run --release --bin battle` in 35.9 s: every stored key in `battle.jsonl` matches the stored run exactly (deterministic seeds) — truth_enc/cross, cone_cross, plateaus, union k-curves, kmax/kmed, setup evals, exponents (cone_cross 2.00; cross setup evals 1.97–2.02; cross encounters 1.91–1.98; ~397 setup evals/pair at b2-300; window tier 286 evals/encounter b1-300). Controls reproduce the gold regime (formation kmed rank 2; ring kmax 5; `outside_cone` = 0 everywhere; window tier exact but one disclosed 1-of-22178 event). Wall and memory claims hold.

**Predictions.** Ordering is consistent (battle.rs 05:32 → predictions.md 05:33 → battle.jsonl 05:36); run.log is empty, so the "controls already run" claim rests on the author's word, but the three misses with honest diagnosis (#1 50%→61–72%; #5/#10 ∝n → flat, correctly re-derived) are the signature of genuine pre-registration. 8/11 held, most quantitatively.

**Adversarial cases (mine, fresh seeds, copied crate in /tmp, 10.5 s).**
1. *Apogee-graze interception from inside* (a=0.95, a geometry the author never ran): t=0 union sort catches 0.886 at k=32, 0.956 at k=256 — the fragility is not specific to the perihelion transfer.
2. *Perihelion interception, independent builders*: 0.898 at k=32 — reproduces b2 without the author's code path.
3. *Wide packets (2.5 rad)*: 0.930 at k=32 — weaker concentration shrinks cross_frac (10%→7%) but the silent miss persists; "degrades toward the belt case" is only a claim about cost, not correctness, and the author says so.
4. *t_meet-sort control* (merge-join by predicted longitude at the crossing epoch): kmax drops 299→41 and 210→48; ≥0.991 at k=32 on both interceptions — the author's one-sentence fix hint is validated, though they never tested it.

**Novelty.** HISTORY.md and the board's taste log: the gold (20261006-0346) tested one formation on one orbit; q-candidate-degree tested belts at fixed density; no prior run tests two fleets or cross-group encounters. The gold's own summary ("under a formation... partner rank 4") confirms the untested extension. New.

**Why not gold.** One headline the log contradicts, by the author's own canon ("a headline the log contradicts... the run loses its grade"): "19× fewer pairs, zero misses". From `battle.jsonl` b1-300: caught_union = 1.000 at k=32, 0.979 at k=16; window sections 179,701; n·k = 600·32 = 19,200 → **9.4× at zero miss**; 18.7× (k=16) drops 2.1% silently — the exact failure mode the run exists to forbid. 9.4× also sits under the 10× gold bar; the claim's gold-worthiness rests on the premise-is-wrong clause alone, which stands. Second, the positive fix ("grouping key is the integer period, belt `keys`") is underspecified against its own data: b1's fleets have a-spread 1e-4 (distinct integer periods, ~4e6 ticks apart), so literal integer keying fragments them — the union sort works because periods are *near*-equal, and my sweep shows that regime ends fast: at a-spread 1e-3 (0.15% period), kmax=121, caught_union 0.730 at k=32 — the catching k is already ~0.4·n; at 1e-2 the fleets never meet (no radial overlap). The fix is sound only if fleets are period-quantized onto exact shared keys, a requirement the dossier never states, with the boundary unmeasured. Minor: the fleet-clump plateau ≈ 1−cross_frac is definitional (cross pairs cannot appear in a clump-local sort) — the measured substance is cross_frac and the union ranks; and the table's "0.93 at k=256" is the n=600 worst case only (1.0 at n=150/300; the text says so, the cell does not).

## The one experiment for gold

Period-keyed grouping, measured: fleets on exact shared integer periods (belt-`keys` construction) vs a-spread 1e-4/1e-3/1e-2, reporting the catching k and the point where the union sort stops being eternal — plus the corrected 9.4× zero-miss number and one line stating that fleets must be period-quantized for the fix to hold. My sweep (above) is the sketch; it belongs in the run's own record with the crate's builders.

## What the author missed

- The 19×/zero-miss arithmetic error (k=32 vs k=16 at n=600).
- The fix's validity regime: no period-spread sweep, so "quasi-eternal" is never bounded; the integer-period keying vs a-spread contradiction is unexamined.
- Their own merge-join hint was one cheap probe away from validation and left untested; as written, the adoption suggestion hands the integrator an unverified design sentence for the missing tier.
- 3-D inclinations (disclosed; the crate is 2-D, so out of scope here).
- The Taleb lens self-flag (over-weighting extremes) is fair, but the wide-packet case shows the miss persists at 2.5 rad packets — the fragility is less concentration-dependent than the lens note implies.
