# r8 v2 — finding encounters without work per orbit

**Claim.** No. In a cold belt (run shorter than any wide synodic cycle, encounters
~3e-3 per body per orbit), every candidate representation certifies "no
encounter" at the cost of the broad phase: work ∝ the candidate set
(~N·σ_a·a·e pairs, independent of ρ), not ∝ true encounters. Median
work_per_encounter: element-sort 786, hier-bounds 2.6e4, shear-grid 4.9e5,
against the criterion's 10. All three candidates are KILLed on `cheap`;
element-sort and shear-grid also on `scales` (exponent 2.00), hier-bounds
worst (2.48). Controls behaved (oracle passes all four; ring-cells fails
complete at 0.494 missed and cheap), so the rung is adjudicable.

**Bottleneck.** Board B3 (cost at a billion) and the integrator's question
in the rung text. The certification floor measured here is 1.1 events per
body per orbit (element-sort), 68 (hier-bounds), 1.9e3 (shear-grid, because
cells must be ρ-sized), 15 (ring-cells, fixed cells, and it still misses
half). At a billion that is 1e9–1e11 events per orbit against ~3e6 true
encounters: the broad phase, exactly as suspected.

**Evidence** (cloud Linux x86, 4 vCPU, 16 GB, idle load, numpy 2.4.6;
orders of magnitude only). 16 frozen belts, N = 1e4, 20 orbits, seed
20261008; truth = exact Kepler per synodic conjunction, minimised over the
passage window, Newton-refined (d/rho percentiles 8e-4..1.0).

| config | missed | false | work/enc (med) | ev/body/orbit | scale expo |
|---|---|---|---|---|---|
| element-sort | 0 | 0 | 786 | 1.10 | 1.99 |
| shear-grid | 9.0e-5 | 0 | 4.9e5 | 1.9e3 | 2.00 |
| hier-bounds | 0 | 0 | 2.6e4 | 67.8 | 2.48 |
| oracle | 0 | 0 | 1 | 2.7e-3 | 0.91 |
| ring-cells | 0.494 | 0 | 6.7e3 | 15.3 | 1.00 |

Belt spread: truth 124..9929 per belt; element-sort work/enc 97..1.25e4.
Scaling (σ_e=1e-2, ρ=1e-4·1e4/N): N=1e3,1e4,1e5 exact (1e5 chunked, 855 s),
N=1e6 by closed forms validated on the exact points (Σ#conjunctions and
candidate count by (a,e)-bin integration: −6.3% at 1e3, +0.6% at 1e4;
truth at 1e6 = conj_cf × P(enc|conj, N=1e5) × ρ-ratio, the P ∝ ρ law
validated on the same-T 1e3→1e4 pair: exponent 0.97). Measured truth grows
~N^0.9 per orbit (336 → 3320 → 989 → ~9.8e3): **the rung's premise (truth
linear in N) held; my prediction 5 was wrong.** The encounter probability
per conjunction is 1-D, not 2-D: P ≈ 1.7e-2·(ρ/1e-3)^0.97 — during a
conjunction passage the radial difference beats many times while the
tangential offset drifts slowly through zero, so only the tangential
dimension gates ρ.

Reproduce: `python3 run_belts.py belts.json` (~16 min); `python3
run_scaling.py scaling.json` (~18 min); `python3 make_metrics.py` (<1 s,
writes metrics.json + picture.svg). Single-belt spot check ~13 s: belt 0
gives cand=1.68e6, conj=1.39e5, truth=427, element-sort work/enc=326.

**Predictions** (predictions.md, written after tuning on belt 0 only):
controls behaving ✓; element-sort missed=false=0 ✓, work/enc in [50,3000]
✓ (786), exponent 2.0±0.1 ✓ (1.99); shear-grid complete ✓ (2 misses of
22173), work/enc range ✓; hier-bounds [1e3,1e6] ✓ (2.6e4); ring-cells
missed [0.6,0.95] — measured 0.494, slightly luckier than predicted;
truth-scaling premise ✗ (it held; see above). The mechanism prediction
held precisely: shrinking ρ does not shrink the work.

**What would make it wrong.** (i) Dense belts, ρ ~ a·σ_e: work/enc → O(1)
and everything passes `cheap` — the kill is about cold belts. (ii) A
representation that certifies batches by *phase* structure: (a,e)-envelopes
cannot (perpendicular phases always align badly, so only envelope-disjoint
groups certify); a sheared-longitude sort with ρ-margin windows is the
untested candidate — but that is element-sort's own mechanism, whose swaps
we measured. (iii) The N=1e6 point is semi-analytic (0.6–3% validated).
(iv) shear-grid's φ-path is smoothed (bin-jump crossings not charged) —
favourable to it, and it still fails by 4.9e4×. (v) hier-bounds' renewal
accounting credits group certificates with one event per expiry and
splits at >64 renewals; a lazier implementation is worse, a cleverer one
still pays the floor member tests (~6.5e6 of its 1.04e7 events on belt 0).

**Cost of adoption.** None: nothing here is adopted. The design
consequence for docs/representation.md §6: "undisturbed orbits cost ~zero"
is true only after certification, and certification is a per-candidate-
pair geometric fact that costs ~1 examination per overlapping pair per
element-epoch. Since a pair's encounter status is frozen with its elements
(H0190's world), that cost amortizes as 1/(orbits per element change) —
the number that matters at a billion is candidate pairs per element-
epoch, ~σ_a·a·e ≈ 500 per body here, not the encounter rate.

**PRINCIPLES.** "Compute only surprises" (3): encounters are the surprise,
but the absence of an encounter is not derivable without touching the
pair — the certificate (21) cannot be cheap enough yet, and that is a
property of the representation (19), not of the tunings. "The simulation
decides; heuristics schedule" (22): the belt decided — the oracle line in
the picture is 400× below element-sort's floor. Every reported encounter
is an exact per-pair check; bounds only guided (the rung's own rule).

**The lens.** A directed rung, no lens file; the author's blind spots:
tuned on the smallest-σ_e belt (belt 0 is the *easiest* for work/enc —
the median belt is 2.7× worse); assumed 2-D encounter geometry until the
data disagreed; and spent the budget on reference exactness rather than
on a fourth candidate (phase-bucketed sheared sort) that might have
beaten `cheap` — that is the next run's experiment if the integrator
wants one.

Environment at freeze: Linux x86_64, kernel 6.18, 4 vCPU, 15 GB RAM, load
~0 before each run, wall times as printed by the scripts.
