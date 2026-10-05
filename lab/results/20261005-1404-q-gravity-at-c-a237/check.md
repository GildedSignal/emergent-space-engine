Grade: silver

**Abstract.** Claim: gravity-as-news (kick toward the tube version the consumer's past light cone last saw, evaluated at now) keeps instantaneous-gravity orbital behaviour while restoring causality. I reproduced every scene exactly (binaries bit-identical; system/flyby/thrust to rounding; news/inst cost 6.0× vs claimed 6.1×). Validated: news=inst to ~1e-7 on flybys, one-step light-cone arrival (9.504 vs 9.5002), ret unbound in 4.2/12.1 orbits. But the headline "every orbital behaviour" is falsified at e=0.9: news drifts dE≈0.145, a +17% in 5 orbits, spurious precession 0.04/orbit — dt-flat, c-flat, iteration-flat (inst holds 4e-5); e=0.6 is clean. Comparable-mass perturbers (3e-3, a=1/1.25) blow tube validity to dE 0.05–0.18. Cost to adopt: tube rings + a bounded e/perturbation envelope. One experiment from gold.

## Reproduction (clean tree, `rustc -O gravc.rs`)

- Binary matrix: my reruns match the stored `m-bine3-*` bit-for-bit (a_final 43.78337, unbound 1.5498, dE 0.9751838, prec −0.1624907). `results.json` rows trace exactly to raw files: ret 12.1/4.2 orbits = 75.8478/26.6238 ÷ 2π (circular scene), news 5.6e-4/1.6e-3, oracle 6π/(1.4286·0.91·100)=0.1449 ✓.
- System: moon survives (news, both β), lost at 5.9 orbits (ret c=3.333), dE 1.4e-3/5.9e-5 vs inst 3e-6 — all ✓.
- Flyby: news vs inst max |Δv∞| 1.28e-7 abs, ≤9.2e-7 rel (claimed 6e-7, same order); ret 21.4% max / 7.5% median ✓.
- Thrust: news onset 9.504 vs exact 9.5002 (one step) at c=3.333 and 8.504/8.5 at c=10; inst reacts at 8.112 (1.39 early) ✓; twins bit-identical pre-arrival (pre_noise 0).
- Bench n256: inst 434 ns, news 2620 (6.0×), ret 2857 — ret/news ordering flips within container noise; the 6× headline stands, the 1.19× news/ret precision does not.
- Memory arithmetic: 541 versions × 112 B = 59.2 kB ✓; 16 B × 32/orbit × light-orbits ✓.
- Timing: predictions.md (14:33:48) predates every `m-*.json` (14:33:59+); the pre-prediction smoke runs are disclosed in its header. Held-out discipline real.

## Predictions

Held: P2 fully (prec 2.5e-5 ≤ 1e-3; drift dt-quadratic, ratios 4.03/3.94 ✓); P5's news/inst parts exactly. Missed: P3's <1e-4 (measured 1.4e-3, disclosed); P4's "half the seeds >10%" (disclosed); P6 absolute ns (disclosed, ratio held). **Not disclosed:** P1's numeric bands all missed low — measured 12.1 vs 2–8 orbits, 4.2 vs 1–3, e-fold ~7× slower than the claimed 1/(2πβ), k≈0.34 vs 0.01–0.03 — yet the dossier reports P1 as "held". P5's ret sub-prediction (ret reacts early) also missed: ret onset 10.008, *late* by 0.5.

## Attacks (mine)

1. **e=0.9 binary (extremes rung).** News: dE 0.145, a 10→11.70 (+17%/5 orbits), spurious precession +0.038–0.041/orbit. Flat under dt 0.004→0.001, under c 3.333→10, and under 15 retarded-time iterations. Inst at identical dt: dE 4e-5, a drift 0.004%. The source is an isolated mutual pair in perfect free fall, so the dossier's validity condition does not exclude it — the claim "keeps every orbital behaviour… for a source in free fall" is falsified as stated. Pericentre tube error stays 5e-7; the drift enters on the periapsis legs. e=0.6 is clean (dE 2.7e-4, drift 0.03%, prec 4.5 orders below oracle): the boundary is sharp, between 0.6 and 0.9, and unexplored.
2. **Fast sources (β→1).** Circular binary at c=1 and c=0.5: news stays bound (dE 4.3e-4/6.0e-4, a=1.0004/1.0006) while ret unbinds in <1 orbit. Strengthens the aberration-cancellation claim far beyond the tested β=0.3.
3. **Comparable Jupiters** (m=3e-3, a=1/1.25, tube-validity attack). Inst dE 4e-5; news dE 0.049 (c=3.333) / 0.18 (c=10) with different end orbits; dt-refinement does not help (0.18→61 at half dt: chaos amplifies a systematic lag-extrapolation error). Confirms, with numbers, the gap the lens section flagged: bare-Kepler tubes extrapolated over the light lag fail when the source is strongly perturbed. The plane's tubes carry compiled kicks — unproven there.

## Novelty

`docs/law.md` §"Gravity travels at c" (5 October) already states the news candidate, Laplace's kill of naive retardation, and Carlip's aberration cancellation, marked "under a GLM falsifier" — this run is that commissioned falsifier and cites law.md. New here: the measurements (ret unbound 4–12 orbits, news=inst to 1e-7, one-step arrival, 6× upper-bound cost, ring arithmetic, ret's 1PN-scale spurious precession, news's dt-quadratic drift) and the boundary conditions. The earlier retarded-kernel lineage (H0011–H0026, isolated law-lab GEM) is a different track. Not a duplicate; not a new idea either.

## Goal fit

Moves the causal contract of board item 0 for the whole plane at measured bounded cost. PRINCIPLES #23 "Nothing past c… it allows to cheaply partition compute" — the version switch at the cone is that partition, now demonstrated; #3 "Compute only surprises" — the near-bit-identical flyby twins show a freely falling source generates no news; #6 "Store the generator, not the generated" — the tube travels, not the position. Error types are right (#13): news's residual is truncation that converges; ret's is a systematic sink.

## Why silver, not gold

Reproduced and decisive in its regime, but (a) the headline claim is stated without its envelope and my e=0.9 run falsifies the universal form — a ladder rung the author skipped while asserting "every orbital behaviour"; (b) P1's numeric misses are reported as "held"; (c) the plane's own kick path (per-pair cursor, table hit) is asserted, not measured — the 6× is a probe upper bound.

## The one experiment for gold

The e-ladder rung on the news binary: e ∈ {0.6, 0.75, 0.9} × c ∈ {10, 3.333} with dt-refinement, root-causing the dt- and c-flat drift (mutual-tube evaluation on the periapsis legs is the suspect). If it is a probe artifact, fix it and the claim stands as written; if it is the mechanism, law.md's news paragraph gets its e-bound and the claim is gold-worthy within that bound.

## What the author missed

- The extremes rung on his own headline (e>0.3 never run; the falsifying case is one scene flag away — his probe already accepted the e0 parameter).
- P1's quantitative misses (e-fold rate ~7× off, k 10× off, both bands) glossed as "held".
- The "1.03× the 1PN oracle" mixes scenes: −0.149 is the *circular* binary's precession, 0.145 the *e3* oracle (a=1.4286); the fair circular ratio is 0.79× (oracle 0.1885). Conclusion (1PN-scale systematic) survives.
- ret's S4 onset (10.008, late) contradicts his P5 prediction (early) — unflagged.
- Chaos amplification of the lag-extrapolation error (my Jupiter scene) — flagged qualitatively, never measured.
- Observational consistency (his own lens note: does the *player's* light switch on the same cone as the kick?) — still open, and it is the player-facing payoff of the whole representation.
