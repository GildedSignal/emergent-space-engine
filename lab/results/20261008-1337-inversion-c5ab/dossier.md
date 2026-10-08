# Dossier — 20261008-1337-inversion-c5ab (lens: inversion)

**Claim.** The phase-neighbour certificate adopted from gold `20261006-0346-taleb-09b5` ("every
real encounter lies within partner rank 4 along the orbit") holds only on zero-dispersion
formations: the required rank grows as ~n·σ_e (measured k99 ≈ 0.7·n·σ_e with aligned apsides,
≈ 1.3·n·σ_e with the best key under apsidal spread, ≈ n/2 for mean anomaly under apsidal
spread), one kick of δe = 10⁻² puts 100% of the kicked ship's real encounters outside rank 4,
and maintaining the sorted order costs O(n²·σ_e) exchanges per orbit — so the trigger must gate
on the dimensionless product n·σ_e (not concentration alone) or the tier silently misses half
to all real encounters.

**Bottleneck.** "Candidate work at scale / co-orbital concentration" (board, risks to attack
first). The `b-coorbital-cert` build is queued on the gold's premise; if it ships with rank 4
and tests only "the gold run's scenes and a dense ring" (both zero-dispersion), it misses
48–100% of real encounters on any realistic fleet. Expected gain: not a speedup — a prevented
wrong adoption (a certificate that is wrong only in the scenes it was built for, concentrated
fleets, is worse than the quadratic tier it replaces, because it fails silently).

**Evidence.** Scenes: co-orbital formations, one exact integer period for all bodies (a = 1,
maximal concentration — the gold's trigger must fire), n bodies, phases uniform, Rayleigh e
(belt-sampler style) or fixed e, aligned or random ϖ, ρ = 10⁻⁴ (10⁻³ for kicks). Truth: the
crate's own `truth_pair` (conservative advancement, dense in time, no conjunction logic) over
every radially overlapping pair, one full period (equal periods ⇒ every distinct relative
configuration occurs once per period). Cross-checked by an independent Python dense sampler
(`debug_gap_model.py`) which also validates the geometry law ΔM* = 2Δe to <1% on every
encountering pair.

| scene (n=1600) | enc pairs | miss@k4 (mean-anom) | miss@k4 (mean-long) | miss@k4 (true-long) | k99 (best key) | exchanges/orbit |
|---|---|---|---|---|---|---|
| A control σ_e=0 | 46 | 0 | 0 | 0 | 1 | 0 |
| B aligned σ_e=10⁻³ | 73 | 0 | 0 | 0 | 3 | 10,804 |
| C aligned σ_e=10⁻² | 89 | 0.483 | 0.483 | 0.371 | 11 | 30,177 |
| D aligned σ_e=3×10⁻² | 85 | 0.741 | 0.741 | 0.600 | 32 | 86,130 |
| E fixed e=10⁻², random ϖ | 58 | **1.000** | 0.828 | 0.586 | 20 | 54,327 |
| F σ_e=10⁻², random ϖ | 91 | **0.989** | 0.791 | 0.604 | 18 | 52,773 |
| G1/G2 = C at n=400/800 | 6/19 | 0 / 0.158 | 0 / 0.158 | 0 / 0.158 | 2 / 8 | 3,071 / 7,747 |

- Rank scales linearly in n at fixed σ_e (k99: 2 → 8 → 11 at n = 400/800/1600, noisy at small
  counts), and the analytic law rank = n·2Δe/2π matches the measured integer ranks exactly.
- Kicks (n = 3200, ρ = 10⁻³, zero-dispersion fleet, one ship's e raised, mean longitude kept;
  3 seeds each): δe = 10⁻³ → encounters at rank 3–5 (caught, one true-longitude miss);
  δe = 10⁻² → ranks 9–12, **100% missed** under mean-anomaly/mean-longitude; δe = 3×10⁻² →
  ranks 29–72, **100% missed** under every key. Predicted ranks 1.0 / 10.2 / 30.5 (2δe·n/2π).
- Churn: the true-longitude order exchanges ~n²·σ_e times per orbit (co-rotating reference;
  control exactly 0), i.e. 148–1013 exchanges per real encounter at σ_e = 10⁻³–3×10⁻² — a
  dynamically re-sorted tier already costs 100–1000× the encounter rate at n = 1600.
- Safe domain at k = 4: n·σ_e ≲ 6 (aligned, mean keys), n·σ_e ≲ 3 (spread apsides, best key);
  mean anomaly under apsidal spread needs k ~ n/2. At the gold's n = 10⁶ fleet: σ_e ≲ 3×10⁻⁶.

Reproduce (each ≤ 60 s, Linux/x86, 7 threads, < 200 MB):

```
cd lab/results/20261008-1337-inversion-c5ab
cargo build --release            # binary at $CARGO_TARGET_DIR/release/inversion-coorb
$CARGO_TARGET_DIR/release/inversion-coorb        # all scenes, ~8 s; log in decisive-run.log
python3 debug_gap_model.py       # independent truth + ΔM* = 2Δe validation, ~30 s
python3 debug_kick.py            # the equal-period window correction, ~2 s
```

**Predictions.** `predictions.md`, written after the control and one debug kick scene, before
the decisive run. Held: control (rank ≤ 1, churn 0), B (0 miss, k99 ≈ 3), E/F mean-anomaly
(uniform ranks, k99 ≈ 790), H ranks (9–12 and 29–72 measured vs 10.2 and 30.5 predicted),
encounter counts (~81 predicted, 58–91 measured), churn order of magnitude. Missed: C/D miss
fractions (predicted 0.85/0.98, measured 0.48/0.74) and k99 (predicted 22/65, measured 11/32) —
I used a sloppy Rayleigh-difference tail, exp(−x²/4σ²), which overestimates P(Δe > x) by ~2×;
the geometry law itself is exact (validated at <1%). Half-missed: the mean-longitude key
absorbs Δϖ exactly (residual ≤ 4e from the equation of center), which I did not derive in
advance; measured k99 ≈ 20 in E instead of ≈ 790.

**What would make it wrong.** If the gold's certificate re-derives the sort at the churn rate
and pays O(n²σ_e) anyway, the miss numbers stand but the "silently" weakens to "expensively".
If the formation trigger requires exact element sharing (one tube, zero dispersion by
construction) the tier is sound inside it — but then any kick (r8 v4 case d: δa/a ≈ 10⁻³, and
this run: δe = 10⁻² ⇒ 100% missed) exits the domain instantly, so the trigger must know the
dispersion regardless. The truth inherits the crate's `truth_pair` (terrace minima in the
control: 1009 minima on 46 locked pairs — r8 v3's dip-quantum issue); pair-level membership,
which is all the miss analysis uses, is unaffected, and the dispersed scenes show isolated
dips (90 minima / 89 pairs).

**Cost of adoption.** One factor in the existing trigger, no new component: the doll knows n
and its bodies' σ_e; gate the phase tier on n·σ_e ≲ k_budget/1.3 (and re-derive or fall back to
the cone tier on any kick, since a kicked body jumps ~n·δe/π ranks at once). PRINCIPLES #4:
"regimes are chosen by dimensionless numbers" — the number must include dispersion, not
concentration alone. H0183: "a failed expectation is not automatically a failed method" — the
certificate is not killed; its domain is now measured.

**The lens.** Inversion attacks premises, and this premise came from a scene generator (a
formation as one ellipse) that may never have been stated as an assumption. What it may have
missed: real fleets with station-keeping may indeed hold σ_e near 10⁻³, where the tier is safe
at n ≤ 10⁴ (n·σ_e ≈ 10 ≈ unsafe already at 10⁴, though); the cost of the fallback (cone tier on
concentrated workloads, the gold's 135×/40 TB number) is the price of dispersion and is not
measured here; and the churn cost assumes the sort must be maintained per orbit — a lazy,
amortised re-sort ordered by exchange times was not explored.
