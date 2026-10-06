# Dossier — 20261006-0346-spacex-1381 (SpaceX lens)

## Claim

The plane's kick cost is two bottlenecks, not one: made bodies pay ~41 µs (fit+compile+bookkeeping ≈ 72% of it), while **leavers — the majority of kicks — pay ~365 µs, of which one fresh `Passage::compile` (538 µs/call, 74% of all measured kick-path time) is essentially the whole bill**; exact shape memoization is bit-identical (digests unchanged) but fires only 16% on cycles and nothing on passages, so the lever is the passage's compiled-to-4-SOI tail, not memoization.

## Bottleneck

Board focus #1 ("kicks dominate the engine's cost") and HANDOFF's measured #3 ("a kick costs 29 µs, 15 of them in rebinding fit and compile", Sol's stalled job). Idiot index: one applied kick is a 1-LSB velocity quantum (sigma-delta already carries the sub-quantum part), and the response is a full geodesic recompile — for leavers, out to four sphere-of-influence radii — roughly 10⁴–10⁵× the information changed. What it lets us delete: the per-kick passage tail, worth ~7× on the kicks that dominate.

## Evidence

Machine: shared Linux x86, 8 vCPU (cloud numbers are orders of magnitude only; the M1 re-measures). Scene: the bench's own plane (seed 1, rtf 1, 3300 frames, 37 sampled distinct kicks).

Baseline (unpatched, `work/kick-baseline-unpatched.json`): made median 51.4 µs / leavers 364 µs — but that run sat under load (wall 0.13 s vs 0.20 s for a later run); the triple-run of the patched build shows made ≈ 40.9 µs with ±0.1 µs spread, so treat cross-binary medians as load-noisy (±25%) and only the profile shares and digests as hard.

Patched build (`work/kick-run{1,2,3}.json`), three consecutive runs:

- `replay_digest` = `989892a426b5…` and plane `digest` = `8283cbe3563c…` — **identical to the unpatched baseline and identical across all runs** (B8-style determinism held; the exact memo changed no bit).
- `cycle_memo`: 11 hits / 67 cycle compiles (16.4%), 56 distinct shapes.
- Profile (totals; per-call = total/calls): `fit_key` 672 µs/89 = 7.5 µs; `compile_cycle` 812/67 = 12.1 µs (≈14 µs fresh, ~2 µs on a hit); **`compile_passage` 11 829/22 = 538 µs**; `at_radius_and_tail` 1050/89 = 11.8 µs; kick-side: readout 6.1 µs, sources 11.4 µs, force+quantize 2.0 µs, proper-time bookkeeping 10.7 µs (61 calls, two decodes each).
- Made-body attribution: 7.5 + 12.1 + 11.8 + 10.7 ≈ 42 µs of rebind-side work against a ~41–58 µs median → the rebind is ~72% of a made kick (96% of a leaver's 365 µs: one passage compile).

Commands (each ≤ 60 s after one `cargo build --release -p xtask`, ~40 s):

```
cargo build --release -p xtask
/home/glmlab/lab-target-0/release/xtask universe --kick-bench --seconds 55   # repeat 3×
jq '{kick_us, kick_us_leavers, cycle_memo, profile_us, replay_digest: .replay_digest[0:16], digest: .digest[0:16]}' <run>.json
```

Patch contents (saved by run.sh): `prof` counters in `crates/space/src/lib.rs`; `from_state` instrumented + exact `ShapeMemo` wiring for the non-circle cycle branch in `crates/space/src/binding.rs` (`orbit::UNIT` made pub); kick/rebind phase timers in `crates/universe/src/step.rs`; `cycle_memo` + `profile_us` fields in `xtask/src/universe/kick_bench.rs` (the `memo` field was accidentally clobbered mid-run and restored — the final tree prints both).

## Predictions

`predictions.md` was written before the decisive runs. Held: rebind > 50% of a made kick (measured ~72%; leavers ~96%); sources gather below 20% (19.6%, borderline); the falsifier "memoization must not change the law" held — digests identical. Broke: I predicted ≈ 0% exact shape hits on this scene; measured 16.4% (the weak branch does cover part of the population). Not run: prediction 3's event-time decode cache (share measured instead: 10.7 µs ≈ 18%, above my 5–15% band — worth doing). Load lesson, twice over: my first patched run looked 15% slower than baseline; the triple-run showed that was machine contention, not the patch (the taste log's 5 October lesson, relearned on myself).

## What would make it wrong

A different scene with more secondaries shifts the sources share up; the M1's absolute numbers will differ (its made-kick was 29 µs); the 22 passage compiles could be unrepresentative of longer runs (leaver-heavy battles would make the passage share grow, not shrink). The profile counters add ~1 µs/kick and one `Instant::now` pair per phase — shares above ~5% are robust to it.

## Cost of adoption, and fit with PRINCIPLES

The memo wiring is ~30 lines, thread-local, bit-identical — but it needs an eviction owner before shipping (unbounded growth), and at 16% hits it is not the lever. The measured lever is: **do not compile the passage tail to 4 SOIs at every applied kick** — the tail is read by `next_exit` (once per interval) and at release, both of which can carry the compile lazily (the tail is a pure function of (key, outer_radius), so deferral changes no bit). That is one experiment away from a measured ~7× on the majority kick. PRINCIPLES: "The cheapest compute is compute not done. Delete before optimizing" (§1); "Compute only surprises" (§3); the tail is not a surprise, it is a re-derivation. Counterweight (lens): a frozen law is a one-way door — I changed no outcome and verified digests, but any lazy-tail patch must re-prove exactly that.

## The lens

SpaceX's delete-first found the tail; what it may have missed: the five-minute profiling detour cost me the lazy-tail implementation (hardware-rich means measure, but the battery was already dead at 22 calls); and the "requirement with no owner" — who owns the 4-SOI tail? — is a question for the integrator, not something a lab run can delete.

## Grade (author's suggestion)

Silver: reproduced 3× with identical digests, a fresh profile of the measured bottleneck, one exact patch, one clean negative (memoization ≠ the lever), and the next experiment named. Gold needs the lazy-tail patch with the same digest equality and the ~7× measured.
