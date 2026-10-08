# check.md — 20261008-0234-autoresearch-dd3e

Grade: silver

**Abstract.** The kick path decoded the same binding's tube three times per kick; caching the proper time at the binding event (`tau_event`) and returning the orbit state with the readout (`readout_with`) leaves one decode. Reproduced from a clean tree with my own base and final binaries (identical bench code, interleaved): pure kick 36.2–36.5 → 28.9–29.1 µs (−20 %, absolute ~7.2 µs on every seed), digests bit-identical on the four author configs and four adversarial ones of mine (m4/m16/m64 sparse, m8 dense), 54/54 tests green. Gain is a constant ~1.25× on the kick event and ~5–7 % on whole-universe settle. Adoption is ~30 lines, zero concepts, bit-identical. Below gold: no 10×, no component deleted, no premise killed — and the dossier says so itself.

## Reproduction (clean tree, my own builds)

- Applied `work/patch.diff` at detached HEAD; built final; reverted the four src files (bench example kept verbatim) and built base — both sides carry identical measurement code, closing the gap that the author's saved base binary ran a bench variant (phase instrumentation) not in the patch.
- Pure kick, interleaved, min of 5: seed 1 m8 36.29→28.97, seed 7 m8 36.21→28.92, seed 23 m32 36.27→29.03, seed 3 m16 dense 36.39→29.10 µs. Matches the dossier's 36.0→28.3 etc.; −20.1 %, ~7.2 µs absolute on every config — prediction 2 (seed-independent absolute saving) holds on my numbers even better than on the author's noisier dense row.
- Digests bit-identical base vs final on all four author configs (canonical cut 3e10) — and my rebuild reproduces the author's recorded digests exactly.
- `cargo test --release -p emergent-universe`: 54 passed, 0 failed (matches the claim).
- Clippy: no new warnings from the patched lines (pre-existing warnings elsewhere; a `drop` lint sits in the throwaway bench example only).

## Held-out check

File order supports pre-registration: `baseline.txt`/`kick_bench_base` → `predictions.md` → `kick_bench_final` → `heldout.txt` → `dossier.md`. All four predictions held, and held again on my independent A/B: (1) digests identical everywhere; (2) ~7.2 µs absolute, seed-independent; (3) rebind loses two decodes — structural, confirmed by reading both code versions (base `kick` decoded at `t` in `readout`, then `rebind` decoded again at `t` and at `event_time`; final does one decode at `t`, `tau_event` is a cache of the construction-time decode of the same immutable fields — `Bound.orbit` comes from the very `decode(&entry,&tube,clock_exp,units,t)` whose fields the Binding stores, so the identity is exact, not approximate); (4) settle improves less than the pure kick (my numbers: 50.9→47.6 to 107.5→103.9 µs/item on sparse, −5–7 %; dense within load noise, as predicted).

## Attack (my adversarial cases)

- seed 11 m16 sparse, seed 5 m64 sparse (110 604 items), seed 42 m4 sparse (smallest fleet), seed 9 m8 dense at a non-canonical cut (3e9): digests bit-identical base vs final in all four; kick −6.6 to −7.3 µs everywhere; identical item counts (no event set change).
- No mutation path exists for a Binding's tube/entry after construction (bindings are replaced); the `None` fallbacks preserve the error paths; every remaining `orbit_state` call is a decode at a genuinely different time. I found no way to make the cache desynchronize.

## Novelty

`tau_event`/`readout_with` appear nowhere in committed history. Nearest prior art: the exact-key memo (dbd4add, taste log 5 Oct) — cross-kick memoization of compiled orbits, dead at 0 % distinct hits — a different mechanism, correctly cited and avoided. The ungraded `20261006-1931-b-readout-cost-43c6` (grade: missing) is a physics change (ramp from kick samples), not this.

## Goal fit

"The cheapest compute is compute not done. Delete before optimizing" (P1) — pure deletion, bit-identical, no law, gate or representation touched. On the board's live question 1 from the ns-per-event side. Honest about being a constant factor.

## Why silver, not gold

Reproduced and adoptable in one step, but the gain is ~1.25× on the kick event — an order of magnitude short of the gold bar (10×, component deletion, or a killed premise). The author's own bottleneck section states this.

**The one experiment that would make it gold:** the run's named next lever — a cross-body `(binding, tick)` memo in `Ctx` for the three remaining same-tick decodes (own readout, secondaries, tide), which re-decode the *same other bodies* at the *same tick* across a fleet and are invisible to the single-ship bench. Same bit-identity gate, measured at fleet scale (m32/m64 settle plus the leaver-dominated kick population via the existing xtask kick bench). If that deletes the redundant decode work wholesale, the pair is a component-level deletion of the kick path's decode layer, not a constant factor.

## What the author missed

1. **Population weighting.** The bench times one ship's identical kick 3 000×; 73 % of real kicks are leavers with median 66 µs (dbd4add) and an unmeasured phase mix. The 20 % pure-kick gain shows up as only ~5–7 % at settle — the fleet-weighted gain is the number the board cares about and was not isolated.
2. **Memory delta unmeasured.** +16 bytes (`Option<Scalar>`) per Binding against board bottleneck 5; asserted negligible, never measured.
3. **Reproducibility gap in the A/B control.** The saved base binary's bench code (phase-split, different output format) is not in the patch; I had to rebuild both sides with identical bench code. Numbers agree, so no harm, but a checker without the base-rebuild step would have compared a tuned bench against an instrumented one.
4. `run.log` is empty (0 bytes); the run's stdout was never captured.
5. Clippy not run (outcome benign; see above).
