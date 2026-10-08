# Dossier — 20261008-2031-constraint-4b27 (lens: the constraint)

**Claim.** The plane's frame constraint is not the engine (the board's whole focus) but the view gather — 69–74% of every frame — and its atom is the tube's orbit phase solve (~5 µs) paid once per emitter per frame; an event-gated crossing (extrapolate between events, re-solve on surprises) cuts the paced frame p50 from 4.45 ms to 0.63 ms (7×) with a bit-identical universe digest, at the cost of relaxing the view's frozen "any cache gives the same view" contract from bit-equality to a ~1e-4 display tolerance.

## Bottleneck

Which one: the player's frame, measured whole (`where_the_time_goes_ms`). Expected gain: ~7× on the frame (measured, Linux cloud, orders of magnitude only; M1 re-measure needed). What it deletes: the per-frame per-emitter phase solve — the view stops paying frames and starts paying events, which is PRINCIPLES #3 ("Compute only surprises… clocks, redshift, views") and #14 ("no work for no reason… we only care about changes") applied to the one component the board had not measured.

## Evidence (Linux cloud, 8 vCPU, load ~0.5; commands each ≤ 60 s)

Baseline, the plane's own instrument (`cargo build --release -p xtask` then run `$CARGO_TARGET_DIR/release/xtask`):

- `xtask universe --bench --seconds 30` (rtf 1): view_gather share **73.7%** (p50 2.36 ms), engine 5.0% → `data/bench-default.json`.
- `xtask universe --bench --seconds 30 --rtf 100`: view_gather share **69.4%** (p50 3.48 ms), engine 17.7% (p99 5.25 ms = at its 5 ms budget cap, 46/1800 overflow frames) → `data/bench-rtf100.json`.
- Structure (instrumented gather, `crates/universe/examples/profile_view.rs`, unpaced): bodies loop = 95% of gather; ~62 readouts/frame at ~76 bodies; `state_rate` = 11.3 µs each; its atoms: `cartesian` (the orbit phase solve, Newton+quadrature in `crates/space`) = **5.0 µs**, `secondaries` (sources' cartesians for the partial step) = 4.9 µs, `binding_at` = 24 ns. Fleet loop 12 µs, player prologue 17 µs. Nothing in the gather is quadratic; it is O(bodies) per frame by construction — fatal at 10⁹ regardless of the constant.

The change (this run's patch, saved by `run.sh`): each emitter's crossing is re-solved exactly only when an event has been committed in its doll chain since its last exact solve (mark = max event time up the chain, plus the binding's periapsis time as a foreign-cache check), or when the extrapolation span exceeds a curvature cap measured by one probe readout at each exact solve; between those, the crossing of the linear model with the past light cone is solved in closed form (a quadratic — no readout, no drift), and pre-first-light emitters are answered from the cache directly.

- Gated, same bench, same seed: frame p50 **4.45 → 0.63 ms**, p99 10.7 → 2.81 ms, p99.9 12.3 → 5.5 ms, worst hitch 15.6 → 6.2 ms, view_gather p50 3.48 → **0.20 ms** (17×), **digest identical** (`41343a14…` both runs) → `data/bench-rtf100-gated.json`.
- Readouts per frame: 62 → **4** (rtf 100), → **0** (rtf 1); warm gather p50 687 → 86 µs (rtf 100) → `data/profile-gated.txt`.
- After the gate the constraint moves: engine 38%, view_gather 28%, view_json 24% of the frame. Next bottleneck: the engine's kicks (the board's existing focus) and then view_json/wire.

Reproduce: `cargo build --release -p xtask && $CARGO_TARGET_DIR/release/xtask universe --bench --seconds 30 --rtf 100` with and without the patch (the patch is this run's saved diff); profiler: `cargo run --release -p emergent-universe --example profile_view -- 100 48 1800`.

## Predictions (`predictions.md`) — what happened

1. Readouts ≤ 5 median, gather ≤ 150 µs at rtf 100: **held** (4; 86 µs). 2. rtf 1: 0 readouts, ≤ 60 µs: **held** (0; 47 µs). 3. Display error vs exact: direction held at 1.1e-4 rad (bound 1e-4, 13% over on one frame); **light-seconds failed its bound** — measured 1.1e-4 relative against the predicted 1e-5 (one order); shift 1.4e-6 held. All still ~0.1 pixel; the ls bound was mis-derived (I bounded position error by distance ratio, not the light-time change the ls field reports). 4. Hot bodies re-solve on their events: held (median frame: 3 mark rejections at rtf 100, 0 at rtf 1). 5. Digest unchanged, observation tests pass: digest **held**; **not held as stated** — the two view tests that freeze cache purity fail (`a_crossing_is_a_property_of_the_state_and_not_of_the_cache`, `relativistic_content_is_found_exactly_and_in_about_one_readout`: `assert_eq!(cold, hot)`), the other 13 pass.

## What would make it wrong

- The gate could miss an event kind that changes a worldline without moving any chain event time or the current binding's periapsis (a doll re-key, a fleet handover?). The mark+periapsis check covers kicks, handoffs, creations and flushes; a missed kind shows as display error growth — the 1e-4-ceiling diff samples are the control, and they bound it over 1800 frames, but a longer adversarial run (heavy burns, encounters, leavers) has not been run.
- The bracket property (`g(t_e) ≤ 0 < g(t_e+1)`) does not hold for extrapolated crossings by construction; anything downstream that reads `age`/`t_e` as exact is wrong within ~the same 1e-4 tolerance.
- The tolerance is a display argument, not a law argument: if any consumer ever uses the view's floats as inputs to outcomes, the gate must be off for those emitters. The view stays a pure read of (state, cache); the *universe* digest is untouched.

## Cost of adoption, and fit

- **Contract change:** the frozen 20261003 cache-purity contract ("any cache, however stale or foreign, gives the same view", bit-equality) must become "within a display tolerance, and validated by the chain mark + periapsis". That is an integrator decision on a frozen gate — this run does not take it. The failing tests are the honest record of that price.
- The cap's probe adds one readout per exact solve (amortized ~100× at rtf 100).
- At scale this is the bridge to representation.md's "≤ 1 sample per pixel per frame": per-emitter readouts must eventually become per-pixel cone samples; the event gate is what makes the per-emitter debug view cost events, and the same gate (re-read only on surprises) is the right shape for the pixel gather.
- PRINCIPLES: "Compute only surprises… Nothing is evolved that can be derived when looked at (clocks, redshift, views)" (#3); "no ticks… we only care about changes" (#14); "the view is an instrument" (#28 — the tolerance is a display quantum, not physics). Goldratt: the constraint was found in the frame's own dashboard, exploited as-is (no new part), and named where it moves next.

## The lens: what it may have made me miss

- I optimized the *displayed* view's cost, not the engine's scaling (the board's billion-body focus): the gate does nothing for kick cost, encounters or H_live. If the integrator judges the debug view as throwaway (visuals come later), the right move is to delete per-emitter gathering, not to gate it — "the best part is no part" (#17). The measurement (69–74% of the frame in the gather, atom = the phase solve) survives either decision and also prices the future pixel gather's per-sample cost.
- The pacing effect (paced gather 3.48 ms vs unpaced 0.69 ms for the same work on this shared cloud box) means all absolute times here are machine-state-dependent; shares and ratios are the sturdy numbers.
- r6 (view) was already an open rung; the novelty here is the measured constraint statement plus the event-gated mechanism and its honest contract price, not the idea that views should be cheap.
