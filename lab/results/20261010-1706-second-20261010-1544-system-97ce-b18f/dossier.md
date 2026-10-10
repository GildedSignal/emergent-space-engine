# Dossier — 20261010-1706-second-20261010-1544-system-97ce-b18f (second author on 20261010-1544-system-97ce)

## Claim

The checker's named experiment is done — the re-anchor is wired on the belt path (config-gated, integer threshold per law.md) — and it **refutes adoption as a memo at the law's own threshold**: the compute targets hold (0.016 compiles/kick against the 0.05 target, 1.75–1.8× belt wall, exactly the checker's ≈1.7× attribution; deterministic bit-for-bit), but the offset-carry **moves the belt's behaviour**: |Δa|/a ≈ 1.5×10⁻³ median over 24 game-years on every held-out Jupiter seed (max 4.6×10⁻², one ship dies in one law and not the other, one readout leaves the integer word), because law.md's error = C·drift² was measured for the jet *with stored derivatives*, and this engine's residual carries none — its position error is first-order in time within each anchor window. The trade-off is priced end-to-end: error ∝ threshold, compiles/kick ∝ 1/threshold (48× tighter: 0.520 compiles/kick, |Δa|/a 2.1×10⁻⁵), so **no threshold reaches the 10⁻⁶ floor below one compile per kick**; the re-anchor needs the jet's derivative terms (or averaging first) before it can delete the compile. The lever ships wired but off (`reanchor_num: 0`, today's law; the full crate suite stays green).

## Bottleneck

Board line 1 (kicks dominate; the recompile per kick) and the first run's silver gap. Expected gain was ~20× compiles and ≈1.7× wall; measured wall gain 1.75–1.8× — and the behaviour cost kills the configuration at this threshold, not the method (principle 9). What the refutation deletes: any plan to adopt offset-carry reuse without derivative terms; what it redirects to: the jet's stored derivatives (the red-team's mechanism, never yet built) and H0190's averaging (post-averaging tides are the red-team's *safe* row — Saturn at 2⁻¹², which never recompiles, still drifts |Δa|/a 5.8×10⁻⁵, so averaging, not the threshold, is the real lever on the weak field).

## Evidence (8 vCPU x86 cloud runner, shared; orders of magnitude only)

`git apply work/patch.diff` (the first run's instrumentation plus this run's wiring), then from `crates/`:

- `cargo test -p emergent-universe --release --test hlive -- --nocapture --test-threads=1 belt_reference` (22 s) — the record, first run's own seed:
  - **REFERENCE 2⁷ reproduces the author bit-for-bit**: events 406,220 (kicks 203,017, boundaries 202,818), rekeys 203,017 (1.0000/kick), 22.8–24.8 µs/event across passes.
  - **ANCHORED 2⁷ (threshold 48/2¹⁶ = √(floor/C))**: compiles 3,204 → **0.0160 compiles/kick** (≤ 0.05), wall 9.25→5.14 s = **1.80×** (1.75× on an earlier pass), 12.8 µs/event, re-anchors 197,340.
  - 2⁴: compiles/kick 0.109 (> 0.05) with 2,859 compiles vs 3,204 at 2⁷ — **compiles track accumulated drift, not kicks**: the per-kick target is cadence-dependent by construction.
  - The blind instrument is fixed (`fired_dv`): every fired belt kick is ~9.6×10¹² quanta ≈ 2.3×10⁻⁵ of the orbital speed (8× that at 2⁴) — the key flips every kick because q48 is far finer than the kick, not because the kicks are large.
- `cargo test -p emergent-universe --release --test hlive -- --nocapture behaviour_vs_reference_many_seeds --test-threads=1` (131 s, eight A/B pairs + determinism; the one command over 60 s, disclosed) — held-out seeds, both perturbers, reference law vs anchored:
  - Jupiter (2⁻¹⁰), seeds 2–6: compiles/kick 0.015–0.021; **|Δa|/a median 1.5×10⁻³, max 8×10⁻³–4.6×10⁻²; |Δx|/r median ~4×10⁻², max 0.55–1.0; |Δe| max up to 5.6×10⁻²; seed 6: alive-diff 1 and one anchored readout outside the integer word** (counted, not crashed on).
  - Saturn (2⁻¹² at 9.58 AU), seeds 2–4: compiles/kick 0.0000 (never recompiles — the tide never crosses the threshold); |Δa|/a median 5.8×10⁻⁵, |Δx|/r median ~9×10⁻⁴ — 26× gentler, still 58× over the floor with *zero* compiles saved-turned-into-error beyond the first.
  - Determinism: seed 7 twice — identical kick count, bit-identical readouts (integer threshold, integer arithmetic).
- `cargo test -p emergent-universe --release --test hlive -- --nocapture control_coorbital` (3 s) — strong field: co-orbital kicks are **97% deferred** (11 compiles of 408): the law's threshold does not fall back per-kick near a planet, it recompiles on accumulated correlated drift; |Δx|/r ≈ 9×10⁻⁴ over half an orbit, alive-diff 0.
- `cargo test -p emergent-universe --release --test hlive -- --nocapture threshold_tightening` (19 s) — the scaling falsifier, seed 2 at 1/2¹⁶ (48× tighter): **compiles/kick 0.520, |Δa|/a median 2.1×10⁻⁵** — error ∝ threshold, compiles ∝ 1/threshold; the 10⁻⁶ floor needs ~10 compiles/kick, i.e. never.
- `cargo test -p emergent-universe --release` — **54 passed, 0 failed** with the default off (the lifecycle behaviour pin `the_origin_takes_the_dolls_kicks_like_a_ship` fails at threshold 48, which is the refutation seen by an existing gate, not a wiring bug).
- `cargo test -p emergent-universe --release --test hlive -- --nocapture belt_offset_headroom` (6 s): max |carried| 6.0×10¹⁴ quanta vs smallest threshold 3.1×10¹⁴ — ships do cross, ~63 kicks apart (~0.65 ship-orbit windows).

## Predictions (`predictions.md`, written before the held-out runs)

Held: compiles/kick 0.015–0.021 on all Jupiter seeds (band 0.010–0.030); wall 1.7–1.9×; elements ordered as predicted (|Δa|/a ≪ |Δx|/r); no deaths except the measured one; determinism; the 2⁴ cadence row. Failed honestly: Saturn compiles/kick predicted 0.002–0.020, measured 0.0000 (the weaker tide never crosses); |Δx|/r max predicted ≤1×10⁻², measured up to ~1 (the first-order position error accumulates more coherently than my random-walk reading — the tide is phase-locked per ship); my control prior ("co-orbital kicks must compile every kick") was wrong before it was measured — 97% defer. The pre-registered kill line (|Δa|/a max ≥ 10⁻³ on any belt seed, or any alive-diff) **tripped on every Jupiter seed**.

## What would make it wrong

- If the belt's behaviour gates (B9/B12-class, judged on distributions) tolerate |Δa|/a ~10⁻³ and 5%-level lifecycle deviations, then "adoptable" reopens — but that is Julien's law call, and the lifecycle pin already votes no.
- If the reference law itself (compile every kick) is not the truth but merely today's convention: both runs are the same split with the same oracle; the anchored one is the one that freezes position response to kicks for whole windows, so the error attribution is structural, not conventional.
- If motion-law v2's `p_t` register or the view's ramp hides part of the deviation: the register is updated identically in both (measured in the state, not the binding), and the ramp is unchanged; the element drift is read from canonical readouts at the horizon.

## Cost of adoption, fit with PRINCIPLES

Adoption at threshold 48 is refuted; the wiring itself is cheap (one config field, one 40-line helper, one guard in `apply` on the catalogue slot) and stays in the tree, off by default. PRINCIPLES: "a fix signals the wrong representation" (19) — the residual without derivatives is the wrong water for this fish, exactly as the red-team said of frozen increments; "a failed experiment kills that configuration, never the method" (9) — the jet with stored derivatives is untouched and is now the priced next step; "errors never compound" (13) — they compound here at first order, which is why the answer is no. The lever the refutation points at: H0190's averaging (Saturn shows even zero-compile carry drifts 5.8×10⁻⁵ — the threshold is not the weak field's problem; the unaveraged tide is).

## The lens (what this may have missed)

The second-author lens takes the checker's experiment as given and may have under-weighted alternatives the checker did not name: carrying the *position* response too (a second-order-correct offset), or re-anchoring the fit only (re-fit the tube's phase without a full compile) — either could change the scaling constant, though neither can beat error ∝ threshold with compiles ∝ 1/threshold. Also: 24 game-years, one belt shape, two perturbers; the resonant and encounter regimes are touched only by the co-orbital control, and B12/B13's scenes (where the plane failed before) were not run.
