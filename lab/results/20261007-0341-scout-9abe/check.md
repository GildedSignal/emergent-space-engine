Grade: silver

**Abstract.** Claim: a local jerk-triggered kick cadence holds fixed-cadence behaviour at 2.5–4 kicks/orbit, and near resonance de-phased coarse cadences beat phase-locked dense ones. All three commands reproduce bit-identically (only wall times differ); predictions.md predates the outputs by 7 min. Real and robust: on S3, TRIG-0.25 Pareto-dominates FIXED-8 (2.75 vs 8.2 kicks/orbit, da_rel 0.0149 vs 0.036, epump 0.998 vs 1.02); at 2:1 the epump ranking (TRIG2-2.0 1.55 < de-phased 1.7–2.0 < FIXED-2 < FIXED-16 4.1 < AVG 10.3) holds over 100–250 orbits and phase π/4. But the rule is 2:1-specific: my 3:2 probe inverts it (FIXED-64 best at 0.12, TRIG2-2.0 worst at 11.8). Gain ~2–3× at held behaviour; adoption is one compare per kick plus κ per horizon.

## Reproduction

- Copied `work/cadence.py`, `work/extra.py` to a clean `/tmp` tree; ran `python3 cadence.py S1`, `python3 cadence.py S2c,S2d,S2c2,S3,S4`, `python3 extra.py`. All three JSONs match the stored ones **field for field**; the only diffs are `wall` times and nan-vs-nan pairs from unbound S4 policies (35 such pairs, all `unbound`). Every dossier number checked out: S1 FIXED-16 7.15e-6/1.223 and TRIG-0.5 2.5/orbit 5.95e-6/11.56; k1quantum 44.03 (vs K1's logged 32.5, disclosed); S2c AVG 10.268, FIXED-8..64 2.87–4.11, TRIG2-2.0 1.69/orbit 1.553; S2d TRIG-0.5 0.814, TRIG2-0.5 1.016; S3 TRIG-0.25 2.75/orbit, 0.0149, 0.998 vs FIXED-16 0.0209/1.041; S4 all FIXED unbound, AVG/TRIG2-0.5 survive at da_rel ≥ 0.24; extra.py FIXED-2 2.41 / FIXED-4 1.80; AVG ≡ FIXED-1 exactly (10.268, 1.06 — identical by construction, tau = P both).
- **Predictions before the run:** predictions.md mtime 03:51:31; out_S1.json 03:58:57; out_S2c… 03:59:05; cadence.py 03:58:56 (same version produced both runs). Held-out set was written first, as required.
- **Prediction scoring verified against the data:** P1 partial (2.5/orbit in range, da better, e-target 2e-7 missed), P2 falsified (rate spread S1↔S2c ≈ 1.5×, predicted ≥8×; walls 0 everywhere — confirmed in all stored rows), P3/P4 held, P5 untested, P6 (author's own gold bar, ≥4× on mixed scenes with one κ) not met (≈2×). The author reports all of this honestly, including the falsification of the trigger's central detection claim.
- `work/patch.diff` and `run.log` are empty: no repo edits, everything self-contained in the run folder.

## Adversarial cases (my own, `/tmp/chk/adv.py`, output `adv_out.json`)

1. **Mechanism split at 2:1 (S2c).** FIXED-3: 3.98/orbit, epump 3.96; FIXED-5: 5.27 — as bad as FIXED-16 (4.11). De-phased non-integer cadences: DEPH-2.5 (3.37/orbit) 2.01, golden-ratio gap (1.54/orbit) 1.67, DEPH-8.5 3.40. So the villain is **phase-locking, not the power-of-two ladder** — every integer n/orbit cadence is exactly commensurable, and the dossier's "power-of-two steps are maximally commensurable with p:q resonances" framing is wrong; de-phasing is what helps, at 2:1.
2. **Generalization across resonances.** 3:1 (µ=1e-3): everything holds except AVG (8.4). **3:2: the rule inverts** — FIXED-64 epump 0.12 (least bad), FIXED-4 1.49, DEPH-2.5 2.55, FIXED-2 3.53, AVG 8.61, **TRIG2-2.0 11.78 (worst of all)**. The surviving prescription "trigger locally for cost, de-phase near commensurabilities" is calibrated on one resonance and is actively harmful at 3:2. What does generalize, and matches law.md's existing rule, is only: orbit-averaging fails at every resonance tested, and resonance must be read from compiled frequencies — which the author's own falsified P2 already concedes.
3. **Rank stability at 2:1.** n_orb = 100/150/200/250 and t0 = π/4: the ranking TRIG2-2.0 < DEPH-2.5 < FIXED-2 < FIXED-16/64 < AVG holds at every horizon and phase (at π/4 the gaps shrink: 2.23 vs 4.35 vs 9.75). The 2:1 result is not an endpoint-sampling artifact of the 200-orbit stop.
4. **S1 "e-walk" mischaracterized.** TRIG-0.5 epump on S1: 18.7 (30 orbits) → 11.6 (60) → 5.5 (120) → 4.95 (240). The error is bounded and relaxes; it does not compound. The conclusion (TRIG-0.5 misses the e-target) stands; the mechanism name is wrong, and principle 13 is not in fact violated on this scene.
5. **The author's named adoption risk, tested.** Snapping TRIG2 fire times to a power-of-two anchored grid (P/4096 base): S2c kpo 1.69→5.72 with epump 1.55→**0.64 (better)**; S1 kpo 9.53→11.17, epump 1.48→1.70. No re-locking catastrophe; part of the de-phasing gain survives in kicks (5.72 still under FIXED-8's 9.3). One interpretation of the anchoring rule, but the feared failure did not materialize.

## Novelty

No `event-triggered|Lebesgue|self-triggered|dither` hits in docs/HISTORY.md or docs/. K1 (32.5 kicks/orbit) is the premise probe (H0186 evidence; integrator reran 32.48) — the S1 scene replicates it and the +35% replica gap (44.03) is disclosed. `q-cadence` sits unstarted in lab/queue.txt, so the question was the board's own, not preempted. "Resonance kills averaging" is already law (law.md kicks; 29 Sept premise red-team) and the dossier cites it; new here are the measured trigger rule and the phase-coherence observation. No prior H entry covers cadence choice.

## Goal fit

Board focus #1 (fewer kicks per orbit at the same behaviour). Real movement: the S3 Pareto point, and a measured kill of "a local bound can pick the cadence near resonance" (P2). Fits PRINCIPLES 3 ("compute only surprises") and 22 ("the simulation tells us what's next not us"); the trigger-as-certificate-expiry reading of H0195 is a good framing. Cost honesty: the trigger pays 3 tide evals + a solve per kick against FIXED's 1 eval; at equal eval count S3's 5.9× kicks is ~1.9× evals. Kicks are still the right unit for the engine if per-kick overhead dominates (components-4643: window setup is 92% of per-kick evals), but the dossier's headline does not say this.

## Why silver, not gold

Reproduced exactly and honestly reported, with pre-registered predictions — but by the author's own pre-registered bar (predictions.md: total cut < 4× ⇒ SILVER) the gold case failed, my 3:2 probe breaks the generality of the surviving rule, and the mechanism story (power-of-two commensurability) is contradicted by FIXED-3/5. Not a lead: the S3 Pareto win and the stable 2:1 coherence effect are real, adoptable knowledge, and the falsification of local-bound resonance detection is itself a result the cadence design needs.

## The one experiment to gold

A cadence study on a resonance lattice — 2:1, 3:2, 3:1, 5:3, each with detunings, ≥3 starting phases, ≥2 horizons — where the cadence (dense / coarse / de-phased / trigger) is **chosen from the compiled frequencies** the law already carries, cost counted in tide evals + anchors (not bare kicks), gate = held behaviours (epump, da_rel) at ≥4× total cut on mixed scenes including the resonant ones. If no frequency-derived rule holds across the lattice, the local trigger is killed as a cadence law and only the selector survives — either outcome with this harness would be gold-shaped.

## What the author missed

- Only one resonance class (2:1) grounded the "de-phase near commensurabilities" rule; 3:2 inverts it and 3:1 is benign — the rule as stated would mis-cadence real belts.
- "Power-of-two" is the wrong axis: odd FIXED-3/5 pump like FIXED-16; it is phase-locking vs de-phasing (delta-sigma dither), which the prior-art section actually says.
- Eval-count accounting: 3 tide evals + solve per trigger kick vs 1 for FIXED — the 5.9× headline is kicks, not cost.
- "e-walk" on S1: the error relaxes (18.7→4.95 over 30→240 orbits), it is bounded, not compounding.
- Their named grid-anchoring risk was measurable in their own float harness (I ran it: no re-locking, epump improves at 2:1) and P5's clustering was measurable from the kick_times they already recorded but left unexamined.
- Cosmetic: k1quantum's comment says "monitoring grid 4096/orbit" while the code uses 2048; the K1 anchor comparison inherits that unexplained factor alongside the disclosed +35%.
