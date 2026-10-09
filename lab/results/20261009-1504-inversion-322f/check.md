Grade: silver

**Abstract.** Claim: the gold's "sort by longitude, watch k≈4" read as a mean-longitude train fails by the equation of center — a k=4 λ-watch catches 36% of encounters in the gold's own control fleet (λ-rank p50 6, max 33) while the distance-rank statistic passes everywhere, so the shipped sort key must be pinned. Reproduced: `verify_mech.py` exact (Δλ = Δeqc, 46.4 vs 46.6ρ); S0 and all S2 rows bit-identical; my probe gives 32–33% catch on three fresh seeds and 46% miss at e-cap 1.5e-3 (not the truncation tail). Gain: kills the last naive reading before b-coorbital-cert builds; cost ≈ zero. Not gold: the divergence and mechanism are already on the record from four uncited runs, and the built train already bounds the equation of center.

## Reproduction

- `python3 verify_mech.py`: identical to the dossier verbatim (227 encounters, 46.4/46.6, 42.9/42.1, median 12.2ρ).
- `python3 invert_train.py`: S0 and S2 rows (σ_λ 3e-3…3e-4) regenerate **bit-identically** from the shipped script (S0: dist max 2, λ p50 6/max 33, catch 0.3625; S2: dist max 8–9, le4 0.97–1.0; λ catch 0.02–0.1). The S1 rows reproduce in `ev3.log` (θ max 1, λ catch 0.15/0.276); I could not rerun S1 inside the checker window (CPU contention), but its θ-rank≈1 is forced by geometry (uniform λ, θ-spacing 157ρ ⇒ contact implies between-count <1) and matches the author's exact re-audit.
- The three logs tell a consistent, disclosed story: `evidence.log` (pre-fix: S1 θ inflated to ~300, λ max to 184) → script fixed → `evidence2.log`/`ev3.log` clean. The λ catch rates are unchanged by the fix (0.1/0.0325/0.02/0.025 in both), so no headline rests on the contaminated code. `work/patch.diff` is empty (no tree edits).
- **Predictions:** file times support pre-registration (predictions.md 30 min before evidence.log); P1/P2 held, P3 held only per its instrument (see attack 1), P4 (Binet ratio ≥100) failed at 33× and is disclosed as failed. Honest reporting throughout.

## My attacks

1. **The S2 truth detector shares the θ-train's blind axis.** `formation_scene` detects contacts only between θ-sort *adjacent* pairs plus one lookahead (`invert_train.py:148-164`). In the σ_λ=1e-3 jam (spacing 0.16ρ), I densely sampled 2 orbits and counted sub-ρ contacts by exact θ-between-count: **47.4% have ≥2 bodies between** — invisible to the detector. So S2's "θ-train catches 100% (max rank 2)" is circular (the instrument *is* a k≤2 θ-train), and "dist-rank ≤4 for 97–99%, misses stay rare" is biased low: the missed half is exactly the high-rank half. The real jam law was already measured with an unbiased per-pair truth by **b1c0**: rank ≈ 1+(1.2–1.7)·J, k=4 misses 19–78% at J=5–87. S0 is unaffected (spacing 1.3ρ ⇒ between-count 0 at contact) and S1 uses analytic crossing search. The dossier's own heuristic — "agreement is not independence; check that the measured events are distinct" — applies to its S2 rows.
2. **Not the e-tail.** With e capped at 1.5e-3 (vs the gold's 1e-2 truncation) the λ-watch still catches only 46%: the failure is the Rayleigh body, not the cap. Circular control e≈0 gives rank 1, catch 1.0 (control passes both sides).
3. **Seed robustness.** Seeds 41/42/43: catch 0.3325/0.32/0.3225, λ max 35–40. The 36% is not seed 27.
4. **θ-churn is real.** Direct simulation, S0: 23.75 θ-order swaps per body per orbit vs 2.29 for λ-order (~10×) — the author's asserted "a θ-order churns every orbit" is correct and now measured; their `swaps_over_horizon` (net unwrapped laps, 336 fleet-wide) under-counts order swaps and should not be reused.
5. **Trigger horns confirmed**: Binet diameters 3.25e-3 (control) vs 0.107 (debris) reproduce in the logs; the 33× gap and both horns are consistent with the record below.

## Novelty — why silver, not gold

The headline ("the instrument vouched for the wrong quantity; mean-longitude order ≠ proximity order by O(2e)") is substantially on the record, none of it cited:

- **The gold itself** (taleb-09b5, lesson 6): its first λ-binned brute "missed 193/233 encounters because co-orbital proximity aligns *true* longitude and the equation of center … dwarfs ρ" — same scene (n=200, σ_λ=0.01 phalanx), same mechanism, milder window.
- **d1b0** (8 Oct, `lab-20261008-2349`): measured the law (λ-distance at contact ≈ (1–2)·σ_e) and concluded "the watch-list must be the bodies inside a λ-window of ~2σ_e, not k=4 nearest".
- **a937** (9 Oct 02:08, **gold-graded**): the same adopted sentence, same divergence measured at its extreme (distance-rank 100% vs longitude-rank 244–363, 98–100% miss, polar; quadratic retrograde churn) — this run's memo-artifact framing is a937's finding restated, coplanar.
- **b1c0** (9 Oct 05:21): k is not a constant (crowding law, 19–78% misses), "crowding must be measured in the coordinate the sort uses"; trigger never fires (19–461× above threshold).
- **2360** (9 Oct 12:59, **gold-graded**, two hours before this run): the built train's engagement logic and ζ.
- **The thing that would actually ship** — `train.rs` in b-coorbital-cert's patch (executed by 2360) — watches λ̄ pairs within the *sound* per-pair window L̄ = δ·(1+L_E) + K_v·|(ΔV,ΔW)| (coarsely δ + φ(e_i) + φ(e_j)): the equation of center is rigorously bounded, by construction. Attacking the fixed-k=4 sentence attacks a spec the lab had already superseded three times.

What is genuinely new and decision-relevant: (a) the k=4 **λ-rank** measurement in the gold's *exact* control scene (36%, seed-robust, not tail-driven) — b1c0 measured θ-rank there (≤3, zero misses), d1b0 λ-rank only in its own scenes; (b) the pinwheel battle-debris scene (all 79,800 pairs crossing, dormant 0.004 enc/ship/orbit, λ-order frozen: 12–17 swaps/20 orbits, Binet 33×) adding the trigger's other horn — exclude debris and the quadratic ruin stands for exactly the battle aftermath the game produces; (c) the θ-vs-λ churn distinction, which the record had only as b1c0's λ-overtake counts. These sharpen the pre-build spec; they do not move a bottleneck 10× or delete a component.

## The one experiment that would make it gold

Attack the live design, not the dead sentence: run the *built* `train.rs` (sound λ̄-window + ζ trigger) on these scenes — phalanx, jam at J≈6, pinwheel at e=0.05 (φ(e) ≈ 0.1 each ⇒ window ~0.2 rad ⇒ ~13 watched partners per body in a uniform-λ clump). Measure ζ, watch degree, misses and cost per real encounter. If the sound window is mute or quadratic on debris/battle aftermath — the scenes this run introduced — that is a gold-shaped correction of what ships. If it holds, the train question closes.

## What the author missed

- The S2 instrument bias (attack 1): their own memo-artifact lesson, one layer down — the truth detector and the θ-train agree because they have the same shape; P3's "misses stay rare" is the artifact, and b1c0's unbiased numbers are the truth.
- The four prior runs on the same certificate (two gold-graded, one two hours earlier) and the gold's own lesson 6: an inversion of an adopted gold should search the successors of that gold first; the novelty claim ("scenes it never ran") is true only of the gold, not of the record.
- The built train's eqc-bounded window: the dossier's "fix" (sort by θ, size k by multiplicity) is b1c0's conclusion plus d1b0's window; the one design already encoding the mechanism is not examined.
- Minor: P2's "caught 72–88%" should read *missed* (ev3 catch is 15%/28%); S0 ranks the first 400 of 729 encounters by insertion (earliest) order — a mild selection, immaterial at these numbers.
