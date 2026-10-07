Grade: silver

Claim: each kick paid two redundant exact tube decodes for clock bookkeeping; deleting them is bit-identical and makes the median made kick 16–21% and the leaver kick 6–11.5% cheaper, leaving certified quadrature in `Orbit::compile` (60–66%) as the wall. Reproduced: with the patch's diagnostic scopes stripped, made −17…−19%, leavers −6…−10% across the four dossier scenes plus three adversarial edges (members 200/4, rtf 10); digests bit-identical everywhere, `refused` 0, 18 suites green, `u_tau2` → 0.0%. Caveat: the patch as shipped (always-on per-panel prof scopes, ~350 drops/kick) is a net leaver regression (+9–12%) — strip `prof.rs` before adopting. Gain ~1.1–1.2× per kick: below the 10× bar; it closes the micro layer and points the lever at cadence.

## Reproduction

Clean tree at `a838a28`; built base (`git HEAD`) and patched binaries from one target dir; box swung ~1.6× in load during the check (base made 39→62 µs), so ratios only, interleaved.

- **Digests:** `replay_digest` and canonical `digest` bit-identical between base and patched on all 7 scenes — the author's exact values (`eaef383e…`/`c8ab26da…` tuned; per-scene values match their `data/*.json`). `refused` 0 everywhere. The gate is real: the canonical digest hashes `r.proper` (`universe.rs:1024`), the accumulated τ the deleted solves fed, plus `event_time`, tube, keys, carries.
- **Source-level bit-identity:** `proper0` is the same decode at the same event tick in all four `Binding` construction sites (`bind_in` → `Bound.orbit`; `rebind_at`; `universe.rs` ×2; `bind_exact` with a `None` fallback). `readout_state` returns the identical decode `orbit_state(t)` would recompute. Proven by construction and confirmed by digest equality.
- **The optimization's timing:** with the prof scopes neutered (only `scope()` made a no-op; call sites untouched), interleaved base-vs-opt medians: tuned made 60.3–61.7→49.7–51.3 (−17%), leavers 149.6–150.2→137.0–138.7 (−8%); m24 −18.6%/−9.2%; m96 −18.8%/−9.7%; rtf60 −17.5%/−8.2%; my m200 −17.6%/−7.7%; rtf10 −13…−18%/−5…−6%; m4 −21%/−12%. Matches the claimed ranges.
- **Profile:** `EMERGENT_PROF=1` on the patched binary: `u_tau2` 0.0% at 224 ns/x; compile subtree (`compile`+`quad`+`weak_quad`+`node`) the clear majority of resolver time. Matches the structural claim.
- **Tests:** `cargo test --release -p emergent-universe -p emergent-space`: 18 suites, 104 passed, 0 failed, 1 ignored.

## The finding the author missed

**The shipped `patch.diff` does not regenerate the headline numbers.** Its diagnostic scopes are always-on (`EMERGENT_PROF` gates only the dump): ~350 guard drops per kick, including one per quadrature panel (`quad` 189k, `weak_quad` 173k, `node` 115k calls in a 10 s run). Measured base vs full patch, interleaved, under load: made +2% (no gain), leavers **+9–12% regression** (tuned 150→164, m96 127→142); on a quiet box: made −6%, leavers +4%. The dossier's commands, run verbatim, produce a regression; the claimed gains appear only after stripping `prof.rs`. The A/B evidently held the diagnostic overhead common-mode (both sides instrumented) — the dossier never says so. The lab's own rule ("numbers the shipped code cannot regenerate … the run loses its grade") caps this at silver despite clean physics.

## Predictions

`predictions.md` at 17:00:34, held-out baselines 17:00:43–46, decisive results in `log.md` at 17:09 — written before the decisive A/B. Leaver medians −8…−15% predicted: −6% tuned (below range, as the author disclosed), in range on m24/m96/rtf60/m200, −5…−6% at rtf10. Made −5…−12% predicted: exceeded (−17…−19%), disclosed. Digest identity, p99 within 10%, `u_tau2` collapse: all held. Seed-blindness (identical digests, seeds 1–3) confirmed in their own `data/base-s*.json` and disclosed before the run. Kill criterion pre-registered. Minor: the predictions' absolute baselines (35/91 µs) are from a quiet moment of the box and match neither the author's `base-s1.json` (74.8/183.4) nor the A/B — only ratios were load-bearing, which the dossier states.

## Novelty

No H entry covers the rebind's redundant decodes. Distinct from the adjudicated compile-memo story (taste log, 5 October: a memo at quantized keys *changes orbits* — a law change; this deletes redundant exact solves bit-identically), from H0213's relativistic gather cache, and from `components-4643` (deferred encounter setup, different path). The negative half — compile is 60–66% and has no bit-identical slack (`exact_shapes` ≈ `cycle_rebinds`, so exact keys never repeat) — is a useful confirmation, not a new premise kill.

## Goal fit

Board focus line 1, "cheaper events" (correctors and splits dead, so per-event cost is what is left). PRINCIPLES §1: "The cheapest compute is compute not done. Delete before optimizing" — this is a pure deletion, no new parts beyond one `Option<Scalar>` cache field; §3 "Nothing is evolved that can be derived when looked at": the event-time proper time is derived once and read. The lens honestly marks its ceiling: the per-kick recompile itself is outside its reach (one-way doors: memo = law change, cadence = the integrator's queue).

## Why silver, and the one experiment for gold

Reproduced, bit-identical, novel, on-goal — but a 1.1–1.2× per-kick cost cut moves no bottleneck by 10×, deletes no component, and kills no premise; and the as-shipped patch regresses what it claims to speed until `prof.rs` is stripped. The experiment that would make it gold: land the deletion scope-free (so the shipped code regenerates the numbers) and take the cadence rung it now makes measurable — fewer rebinds per orbit against the measured 60–66% compile share, the only lever left on the kick path. That is the integrator's `q-cadence` queue, and this run's profile is its justification.

## What the author missed

1. The always-on scope cost itself (the patch's own `prof.rs` claims "~25 ns each"; measured effect is ~10 µs+/kick, ~350 drops, enough to invert the leaver sign) — and therefore the regeneration gap above.
2. A per-panel scope was never needed for the phase table; whole-`compile` scoping alone gives the 60–66% share at negligible cost.
3. The m96 leaver p99 (3.2 ms in their own data) is tail poisoning on a shared box; medians-only is right, and they said so — worth carrying into every future bench read here.
