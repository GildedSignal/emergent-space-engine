Grade: silver

Abstract: The kick-bench attribution reproduces essentially bit for bit: seed-1 dump (72 binds) byte-identical to the author's; replay `output_hash 95fafd8590f8f8ee`; passages 14/72 = 19% of calls and 87% of bind µs (claimed 86%), compile 307–590 µs, cycles 13–147 µs at 0.56 µs/knot, readouts 3.2/7.3 µs; p99 tail 505–1011 µs on `kick_us_all` (author 908); `div_word` 1.29× and exact on 200k random cases. Nothing is adopted, correctly. But my probe kills the dossier's headline expectation: shrinking the compile-out radius buys exactly 44 µs/octave, and the deepest passage still costs 636 of 985 µs at the largest valid shrink — a 1.5× ceiling, not the claimed 10×. Cost to adopt: zero (knowledge + scaffolding).

## Reproduced (clean tree at f51ddd2, patch applied per instructions)

- Baseline `--seconds 15 --seed 1`: `replay_digest 50b705f1…` exact, stable over 4 runs. Absolute medians drift with co-tenant load (mine 66–71 µs at load 3.9 vs 45.4 at theirs; they declared this 20–50% drift).
- `KICK_DUMP` 55 s seed 1: 72 lines, **byte-identical** (`cmp`) to the author's `bind_dump_seed1_55s.jsonl`.
- Replay: `output_hash 95fafd8590f8f8ee` exact; 14 passages of 72 (19% of calls), 87% of total bind µs (claimed 86%); passage compile 307–590 µs (claimed 307–658); cycle bind 13–147 µs (log: 13–146); cycle compile 0.56 µs/knot (claimed 0.57); cycle readout 3.19, passage readout 7.35 (claimed 3.2/7.3).
- Tail: `kick_us_all` p99 = 504.6 µs (seed 1), 1010.7 µs (seed 3) vs the author's 908 — reproduced. (The dossier omits that 908 is the `kick_us_all` key, `kick_us` is made-only; that cost me a false miss on first read.)
- `divbench`: 1.29× (claimed 1.32×). Adversarial strengthening: a 200k-case randomized differential test of `div_word` vs truncated `u128` division in `fast_quad`'s operand ranges — 0 mismatches; the "proven output-identical" claim holds beyond the shipped 4-case assert.
- Memo `exact_hit 0%` on seeds 1, 2, 3 (taste log, 5 October).
- Seed 2 (author's unreached held-out): digest `9efc7582` stable, exact_hit 0, p99 172 µs (weaker passages — consistent with "no deep passages, no tail").
- The `div_word` swap is house code (`crates/space/src/num.rs:13`, already used by `quad` and `scaled.rs`), correctly left as a lead after the pre-written kill criterion fired.

## Adversarial: the 10× expectation does not survive

The dossier's bottleneck line promises "expected gain 10× on the kick tail (p99)" from compiling passages out to a trajectory-relative radius. I probed it on the run's own harness (edge exponent ±shift on the deepest passage, n=31, interleaved reps, ±1% spread): compile is cleanly linear at ~44 µs per octave of `outer_radius`, from 985 µs (baseline) down to 636 µs at −8 octaves; −10 octaves **refuses** (`outer_radius ≤ periapsis`, `Error::Topology` — the physics floor). So the radius-driven part of the deepest passage's compile is ~1.55×, and ~636 µs of near-periapsis quadrature remains that no compile-out radius can remove. The real tail lever is law-level (fewer/tiered panels near the turn, or passage shape memoization), which the author correctly flags as not this run's to make — but the stated magnitude is ~6× optimistic, and the integrator should not spend a law decision expecting 10×.

## Predictions, novelty, goal fit

- P4 held (digests identical across seeds and runs, including dump-on/off); P1 honestly reported unresolvable under co-tenant load (I see the same); P3 untested because the kill criterion fired first — correct discipline. predictions.md pre-existence is unverifiable after packaging (all mtimes re-touched); the honest reporting of the miss argues good faith.
- Novel: H0210 knew "kicks cost 29 µs"; the taste log knew memo 0%. The decomposition (median ≈ secondary readouts + 13–25 µs cycle rebind; p99 = passage compiles at 86% of rebind µs; cost linear in log₂(edge/periapsis)) is new, and the dump/replay harness regenerates it.
- Fit: board item "a kick costs 29 µs, 15 in rebinding"; Julien's "i care about the p95/99". "Measure before claiming" — the unresolvable gain was not claimed.

## The one experiment for gold

Measure the tail counterfactual on the replay harness itself — compile the captured passages at `outer = k·periapsis` and at tiered panel budgets, and report the measured p99 cut (my probe says ≈1.5× from the radius alone; panel tiering/memoization is the untested remainder). That converts this map into a measured lever the integrator can price.

## What the author missed

1. The 10× expectation (above) — their own harness could have falsified it in seconds.
2. The claim line's "13–25 µs cycle rebind" understates their own data (cycles run to 146 µs; 92-knot cycles are a second, p90-level tail).
3. Bench keys: `kick_us` (made) vs `kick_us_all` (made+leavers) are never named; the tail lives only in the latter.
4. The n=31 passage compiles at 590 µs inside the full replay but ~985 µs isolated — cold-cache sensitivity worth one sentence, since the bench times in-scene.
