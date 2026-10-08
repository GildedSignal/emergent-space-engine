# Dossier — 20261008-2113-second-20261008-2031-constraint-4b27-08f7 (lens: second author)

**Claim.** The checker's named experiment is done and the original claim now holds on the shipped record: with the tolerance re-derived from one display quantum (`1e-4·dist` bounds |Δdirection| in rad and relative |Δlight_seconds| alike) and the author's one-probe curvature cap replaced by **measured checkpoints** (probe the true state at the current crossing tick whenever the extrapolation span crosses an armed tick or the distance halves; refresh the linear model from the probe; re-solve exactly past half the quantum), the event-gated view holds max_dir ≤ 5.3e-5 and max_rel_ls ≤ 5.8e-5 — inside the 1e-4 bound — at 5400 frames (was 1.675e-4/1.641e-4), at rtf 400, and on seeds 1–3, with the universe digest bit-identical baseline↔gated and a matched-state frame p50 gain of 2.4× (gather p50 5.4×) measured interleaved on one machine state.

## Bottleneck

Which one: the player's frame (the original run's diagnosis stands — view gather 66–69% of the paced frame, its atom the ~5 µs orbit phase solve per emitter per frame; reproduced here: baseline gather share 0.659–0.689). Expected gain: ~2.4× on the paced frame p50 at rtf 100, 1.9× at rtf 1 (matched state, Linux cloud, orders of magnitude only). What it deletes: the per-frame per-emitter phase solve — the view pays events plus verification checkpoints, not frames (PRINCIPLES #3, #14).

## Evidence (Linux cloud, 8 vCPU, load 1.9–3.3; scripts and raw outputs in this folder, `data/`)

Repair (this run, `work/second-repair.diff` = author patch + checkpoint gate; applied on the run's own patch as the starting point):

- **The leak, diagnosed.** The author's cap measured curvature once at `t_e ± 8192` ticks and τ²-scaled it to a 1e-4 rad bound — extrapolating ~600× beyond the probe on long arcs. The bound was exceeded 1.7× (1.675e-4 at 5400 frames), worst on the planet Home: a cold worldline on a long event-free arc, where the curvature beyond the probe point (toward star passage) outruns the local estimate. An endpoint-verified upfront cap is impossible in principle here: the allowed span extends far beyond `t_now` (the readable present is only ~the light lag back from it), so no read at solve time can bound the span's end.
- **The mechanism now.** `tol_len = 1e-4·dist` (one quantum: the direction error is Δpos⊥/dist, the relative light-seconds error Δpos∥/dist — the author's separate 1e-5 ls bound was the mis-derivation the checker named). When the extrapolation span `tau` crosses `next_cp` (armed at `tau·(tol/2dev)^¼`, clamped 1.2–4×: quartic-safe, so even power-4 deviation growth lands at the tolerance) or `dist` halves, the gate probes `state_rate` at `t_exact + tau` — the crossing tick the model claims, always readable (`≤ t_now`) — measures the model's actual deviation, refreshes the model from the measured state and re-arms. Past half the quantum it re-solves exactly. Measured, not modeled.

Held-out matrix (`cargo build --release -p emergent-universe --example profile_view` then `$CARGO_TARGET_DIR/release/examples/profile_view <rtf> 48 <frames> <seed>`; each ≤ 6 s wall):

| case | readouts/frame p50 | gather p50 µs | max_dir | max_rel_ls | max_rel_shift |
|---|---|---|---|---|---|
| rtf 100, 5400 f, seed 1 (checker's failing case) | 2 | 59.8 | **5.33e-5** | **5.73e-5** | 2.3e-6 |
| rtf 400, 1800 f, seed 1 | 7 | 104.0 | 3.45e-5 | 5.83e-5 | 3.0e-6 |
| rtf 1, 1800 f, seed 1 | 0 | 48.2 | 4.92e-5 | 4.44e-5 | 2.2e-7 |
| rtf 100, 5400 f, seed 2 | 4 | 84.9 | 5.08e-5 | 5.37e-5 | 2.3e-6 |
| rtf 100, 5400 f, seed 3 | 4 | 81.5 | 5.33e-5 | 5.79e-5 | 2.6e-6 |

All inside the 1e-4 quantum on every component; the worst offender is still Home (biggest event-free arc) but now bounded. Baseline for comparison: the same gated binary's cold (memo-less) gather — the ungated cost on this machine state — is 0.95–1.78 ms p50 (`gather_cold_us_p50` in the profiles, 39–76 bodies at the cut), and the interleaved baseline bench leg's gather p50 is 1.198 ms; the 62 readouts/frame baseline figure is the author's, checker-verified bit-for-bit on their rerun.

Matched-state bench pair (`/tmp/xtask-base` vs `/tmp/xtask-gated`, built from the pristine tree and the repaired tree, run interleaved G,B,B,G at 30 s each, load 2.4–3.3, engine p50 0.121 vs 0.124 ms confirming the same state — `data/interleave-*.json`):

- frame p50 **1.650 → 0.684 ms (2.4×)**; gather p50 **1.198 → 0.221 ms (5.4×)**; gather share 0.659 → 0.294; digest `41343a14…` identical in every leg.
- Earlier non-interleaved pair (load ~1): frame p50 0.993 → 0.518 ms (1.9×), gather 0.730 → 0.131 ms (5.6×) at rtf 1; digest `d96acc05…` identical (`data/bench-{base,gated}-rtf*.json`).
- The 7× headline of the original run is retracted as machine-state mixing, as the checker held; the honest number is ~2.4× frame / ~5.4× gather at rtf 100.

Tests: `cargo test --release -p emergent-universe` — exactly the two frozen cache-purity tests fail (`a_crossing_is_a_property_of_the_state_and_not_of_the_cache`, `relativistic_content_is_found_exactly_and_in_about_one_readout`), the disclosed contract price, unchanged by the repair.

## Predictions (`predictions.md`) — what happened
1. 5400 f rtf 100 within 1e-4, worst offender no longer unbounded: **held** (5.3e-5; Home still worst but bounded). 2. rtf 400 within bound, readouts ≤ 25: **held** (7; 104 µs ≤ 250). 3. rtf 1: **held** (0 readouts, 48 µs ≤ 60). 4. Seeds 2–3: **held** (≤ 5.8e-5). 5. Readouts ≤ 20, gather ≤ 250 µs: **held** (2–4 readouts, 60–105 µs — the 300-frame shakeout had shown 15 readouts; by frame 5400 the seen set shrinks from ~70 to 49 emitters as the fleet battle resolves, and warmed spans stretch, so the median falls). 6. Digest identity both rtf: **held** (bit-identical, four interleaved legs). 7. Frame gain 2–4×, gather 3–8×: **held** (2.4×/5.4×).

Disclosure: predictions.md calls its tuning set "one 1800-frame run"; the debug run actually used was a 300-frame rtf-100 shakeout (readouts 15, errors 4.3e-5) — narrower than stated, so the held-out claim is if anything stronger. The predictions file is left as written.

## What would make it wrong

- The bound between checkpoints is armed for power-4 deviation growth and half-quantum headroom; a worldline whose deviation grows faster than τ⁴ between checkpoints (no smooth-gravity case known: that needs a jerk that doubles within the span) would exceed 1e-4 for the frames before the next checkpoint catches it. The 5400-frame × 3-seed sampling (every 100th frame, ~3000 diffs per seed) is the control; a longer adversarial run (hours, heavy encounters) has still not been run.
- The bracket property (`g(t_e) ≤ 0 < g(t_e+1)`) does not hold for extrapolated crossings, as before; anything downstream reading `age`/`t_e` as exact is wrong within the same 1e-4.
- The tolerance is a display argument only: any consumer feeding the view's floats into outcomes must turn the gate off for those emitters. The universe digest is untouched (bit-identical, four legs).
- Checkpoint cost scales with curvature, not with events: a scene of many cold bodies on tight, eccentric arcs pays a checkpoint every ~1–4 frames each (the rtf 400 leg: 7 readouts median). At 10⁹ bodies the gather must become the pixel-cone sampler anyway; the checkpoint's shape (re-read on measured surprise) is the right primitive, but its arithmetic here is per-emitter.

## Cost of adoption, and fit

- **Contract change (unchanged from the original run, still the integrator's call):** the frozen 20261003 cache-purity contract ("any cache gives the same view", bit-equality) becomes "within `1e-4·dist`, validated by chain mark + periapsis + measured checkpoints". The two failing tests are the honest price; this run does not relax them.
- One `state_rate` readout per checkpoint (~11 µs), amortized: 2–7 per frame at rtf 100–400 vs the baseline's 62.
- PRINCIPLES: "Compute only surprises… Nothing is evolved that can be derived when looked at (clocks, redshift, views)" (#3); "the simulation tells us what's next not us" (#22 — the checkpoint measures and decides, no modeled bound); "the view is an instrument" (#28 — the quantum is a display tolerance, not physics); behaviours over many seeds (#20 — seeds 1–3 held).

## The lens: what this lens may have made me miss

- I repaired the mechanism and kept the author's frame; I did not re-attack the diagnosis (gather dominance) — the interleaved baseline confirms it (0.66 share), so the constraint statement stands on its own record now.
- The checkpoint is still per-emitter debug-view arithmetic; if the integrator judges this view throwaway, deleting per-emitter gathering remains the cheaper move ("the best part is no part", #17). The measured atom costs and the checkpoint primitive price the future pixel gather either way.
- One machine, shared, load 1.9–3.3 across legs; I cancelled drift by interleaving and by the engine-p50 cross-check, but M1 re-measurement remains the integrator's, and all absolute times are order-of-magnitude only.
