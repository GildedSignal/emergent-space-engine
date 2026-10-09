Grade: gold

**Abstract.** The clock-path regime split (per-body Δs from the coupling its own orbit permits; one bit per octave of κ; refine-only ratchet) is real and gate-validated. Reproduced bit-exactly from `work/patch.diff`: default path digest `21c73edc…`; B13 split identical to shipped (60/64, PLANE_TRACE byte-identical); B17 PASS (pump [0.984, 1.001], libration 0.981, 34/34, 5/5); B12 shipped and split match the record text for text; belts run 4.68×/7.79× fewer kicks with deterministic digests; the naive uniform-4 cut fails B13 at 3/64 (reproduced). My adversarial high-e belt crossing Giant's band loses nothing and stays deterministic. Gain ≈8× clock-path kicks (the ramp's designed frontier); cost ≈60 lines behind a default-off flag, unit tests 29/29. One stale citation: the bench digest `bb81ae6e…` is a v1 artifact; v3 gives `fea07ab3…`.

**Reproduction** (clean tree, patch applied by `git apply`, build 38 s; Linux x86, load 1–4):

| claim | author | mine |
|---|---|---|
| control digest (no env) | `21c73edc…` | identical |
| B13 shipped / split | 60/64 both, identical text | identical text; PLANE_TRACE stderr byte-identical and equal to `data/trace-split-v3.txt` |
| B17 split | PASS [0.984396, 1.001103], 0.981, 34/34, 5/5, 35.5 s | identical, 35.5 s |
| B12 shipped / split | FAIL, median ∞ / 0.608, 44 same replaced draws | identical |
| belt wide | 78385 → 16732 (4.68×), `59752da9…` twice | identical, digest reproduced twice |
| belt inner | 78094 → 10032 (7.79×), `3a506cb5…` | identical |
| uniform-4 B13 (the contrast) | 3/64 (first author) | 3/64, worst 1.34e0 |
| bench events/s under split | 170.1 unchanged | unchanged |

**Predictions.** `predictions.md` (mtime 9 min before the first split artifact, `data/b13-split.txt`) was written before any split run. P1 held exactly (identity, and the trace proves it is structural: overlapping orbits ⇒ k = 7 throughout). P2's pre-registered stop rule was executed, not bypassed: two recorded falsifications (`data/b17-split.txt` v1 libration 0.002; `-v2` 0.008, failing exactly the two 3:2 μ = 3e-3 cases whose libration walks κ across the k = 6/7 boundary), then the re-derived ratchet passes. P3 undecidable — B12 fails on the shipped law itself (median ∞; H0215: "B12 unusable until rebuilt"); the run reports only what B12 can support. P4 held inner (7.79×), missed wide with the geometry quantified (apoapsis 1.4 R_H from Giant's band ⇒ k = 5 honestly kept). P5 falsified in number, held in substance. P6 held every time.

**Attacks (mine).**
1. *High-e belt, real encounters:* a ∈ 1.8–3.6 AU, e ≤ 0.5 (apoapsis to 5.4 AU, crossing Giant's band): split loses nothing (lost 0, refused 0, alive 2003/2003), digest deterministic on rerun, and the saving shrinks to 3.0× — the bound's honesty under the population it exists for, exactly as the dossier's own risk section predicts.
2. *The uniform-cut contrast:* B13 at `UNIVERSE_STEP_LOG2=4` gives 3/64 — the gold-carrying contrast (bulk savings without losing the passages) is real.
3. *Code audit:* `ext::constants` has one caller (step.rs:598), updated; `coupling_bound`'s axis/apoapsis formula copies shipped `source()` verbatim (`k.scale(1).sub(ONE)` denominator, `2a − p`); flooring `ds_unit` to a power of two commutes with the `2^-k` shift, and P6's bit-identity is the empirical proof. `cargo test -p emergent-universe`: 29/29 pass.
4. *Env interaction:* `UNIVERSE_STEP_LOG2=5` + split runs clean (bulk follows the anchor down, no crash).

**Novelty.** H0215 lands the motion law v2 with one fictitious clock per root-doll body at a doll-wide `step_log2`; the board's focus 1 names fewer kicks per orbit as the lever and the taste log (6 Oct) records that correctors and higher-order splits buy nothing, leaving cadence (q-cadence queued). No HISTORY entry or doc ships a per-body, orbit-coupled Δs; the direct predecessor is the first author's uniform sweep (this run's predictions), whose naive form kills B13. The refine-only ratchet as a *correctness* condition (a modulating cadence pumps resonant libration) is new and measured.

**Goal fit.** Board focus 1 directly. PRINCIPLES #14 ("ticks make no sense to me… not compatible with our certificate/compiler idea" — the step is now a per-body validity claim over what the orbit will do), #4 ("regimes are chosen by dimensionless numbers" — κ), #33 (the ant and the raindrop), #13 ("errors never compound" — the ratchet exists because its absence was measured to compound, twice).

**Defects found (why not demoted).** The dossier cites the split bench digest `bb81ae6e…`, which the shipped patch does not regenerate: v3 gives `fea07ab3…`, deterministic across reruns. `data/bench-split.txt` predates the v2/v3 iterations (its mtime sits with the v1 B17 run), so it is a v1 artifact cited as final — the exact 5-October lesson ("results that the shipped code could not regenerate"). It stays gold because the number sits on the scene the dossier itself proves blind to the clock path (events/s unchanged, within-session kick-bench identity reproduced: 286 samples / 268 rebinds / 45 shapes both arms in my session), while every load-bearing number regenerates bit-exactly. Second, the kick-bench absolute counts (630/611) are paced-bench, load-dependent and carry no caveat. Third, the v1/v2 falsifications are single-harness records not regenerable from the patch (only v3 ships) — internally consistent (v2 fails exactly the two libration-walking cases; v3 = v2 + hold passes), but one harness.

**Gold bar.** Reproduced; held-out predictions held (the wide-belt miss is quantified honesty, the inner belt sits at the rule's designed 2³ frontier — 7.79× ≈ 0.9 decades on the clock-path kicks of the belt-like population the billion-body goal is made of). It deletes the doll-wide constant (one rule replaces it) and corrects a premise (cadence may only refine — a constraint the queued q-cadence build must carry, evidenced by two falsifications). Adoptable within one step: default-off flag, off = shipped bits by construction, tests green.

**What the author missed.** The v3 bench digest was never re-recorded, so the dossier cites a v1 number. The kick-bench absolute counts lack the load caveat. The B17 shipped baseline is cited from H0215, not rerun in-session. Belt cost runs show handoffs = 0, so no clock restart — the ratchet's re-derivation at handoff — is exercised anywhere in the cost evidence, and the ratchet↔encounter-skin coupling (the leak the author names) remains untested; a scattered-then-refining probe would close it. The i8 cast of `k_held` silently assumes `step_log2` < 128 (integrator-owned config; harmless today).
