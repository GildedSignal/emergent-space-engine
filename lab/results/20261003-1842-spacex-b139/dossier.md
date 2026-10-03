# Dossier — 20261003-1842-spacex-b139 (SpaceX lens)

## Claim
The plane's every kick rebuilds its orbit's compiled quadrature from scratch, and 99.8% of those compiles are recompiles of the same 24 shapes; routing `from_state`'s Cycle branch through `crates/space`'s existing exact `ShapeMemo` deletes them with bit-identical digests and cuts the kick ~12–16% (interleaved A/B, median 22.54→19.92 µs seed 1, 30.45→25.62 µs seed 7, p99 −15%) — and the stage table this run measured shows where the kick's remaining ≈40× idiot index lives.

## Bottleneck
Board focus #1 ("kicks dominate the engine's cost") and the plane's measured #3 (29 µs per kick, 15 in "rebinding fit and compile"). The expected gain of the memo itself is ≈1.2×, not 10×; the run's real product is the measured cost table below, which names the 10× levers in order. What it lets us delete: the per-kick quadrature compile outright (the memo), and, next, most of the per-kick fit/decode work.

## Evidence (cloud Linux/x86, 2 shared vCPU — orders of magnitude only)

Where a plane kick's 22.5 µs goes (median, `kick_stages 10`, seed 1, 13,800 kicks, all fired, 0 carried):

| stage | µs | share | physical floor |
|---|---|---|---|
| secondaries (moon's tube readout at t) | 7.72 | 34% | ~0.1 µs (position read) |
| bind (fit_key 2.31 + compile 3.36 + at_radius 0.80 + residual 2.71 + bind_in's extra decode ≈2.4) | 11.58 | 51% | ~0 (a 1-quantum velocity add) |
| own readout (decode + turn) | 2.66 | 12% | ~0.1 µs |
| force + h·dv + quantize | 0.54 | 2% | this IS the physics |

- Physical content of a kick = 0.54 µs of 22.5 µs → **idiot index ≈ 40×**, and it is bookkeeping, not physics.
- 13,801 `from_state` calls → **24 distinct shape keys, hit rate 0.998** (seed 1 AND held-out seed 7: same 0.998, 24 distinct). A firing kick changes the true conic by ~2⁻⁵⁹ relative; the shape key quantizes at 48 bits — thousands of kicks land on one key.
- A/B (same process, 150-frame alternating blocks, so shared-box noise hits both arms): seed 1 control 22.54 vs memo 19.92 µs median (p99 30.86 vs 26.30); seed 7: 30.45 vs 25.62 (p99 2054 vs 65 — control caught a 2 ms scheduler hiccup; medians robust). Compile stage 3.36 → ~0.5 µs/call.
- **Digests bit-identical with and without the memo** (replay digest and universe digest, seed 1, two independent runs) — the memo is a pure cache, as `crates/space`'s own api test already asserts (`memo.get` ≡ `Orbit::compile`).
- `cargo test --release -p emergent-universe`: all pass (motion, plane, view, lifecycle, replay-to-the-same-universe).

Commands (each ≤ 60 s except the suites):
- `cargo build --release -p emergent-universe --example kick_stages`
- `./target/release/examples/kick_stages 10` (stage table, digests)
- `./target/release/examples/kick_stages 10 ab` (interleaved control/memo A/B)
- `./target/release/examples/kick_stages 10 ab 7` (held-out seed)
- `./target/release/xtask universe --kick-bench --seconds 8` (official metric, memo on: median 37.3 µs on 23 samples at rtf 1 — too few samples on a loaded box to rank; the A/B above is the honest number)

## Predictions
Written before the decisive run (`predictions.md`): digests identical (held), held-out seed hit rate ≥ 0.95 (held: 0.998), kick ≈ 19 µs not 10× (held: 19.92), tests pass (held), passages not helped (held — this scene binds 0 passages; flyby-dominated scenes keep their compile cost), shape count tens (held: 24). No prediction failed.

## What would make it wrong
- Correctness: only if `ShapeMemo::get` differed from `Orbit::compile` (refuted by space's api test and by the digests here), or if `Arc` identity were load-bearing (it is not: the catalogue indexes slots and digests hash state).
- Speed: a scene whose kicks walk the shape key fast — high-eccentricity periapsis passages, or strong-field dolls where compactness (not just k) enters the key. Then the memo costs a hash lookup (~50 ns) instead of saving 3.4 µs; it cannot make the kick slower by more than that.
- Cost of adoption: ~15 lines in `crates/space/src/binding.rs` (`shape_memo`, capped at 4096 entries, clear-on-exceed — bounded memory). The lab seam is a thread-local; the production seam should hang the memo off the resolver's worker context (the plane resolves single-threaded today, and events of independent bodies may resolve on any thread, each with its own memo — still deterministic, it is a cache).
- Fit with PRINCIPLES: "The cheapest compute is compute not done. Delete before optimizing" (§1); "Nothing is evolved that can be derived when looked at" (§3); "Store the generator, not the generated" (§6 — the generator was being regenerated per kick).

## The next levers, as measured (for the queue, not this run)
1. **fit_key 2.3 µs per kick, recomputed although the key moves ≤1 quantum:** the exact invariants update incrementally (E' = E + v·Δv + Δv²/2, L' = L + x×Δv — exact integer algebra, no bisection); the bisection/witness then runs only when the quantized key actually ticks. Estimated ≥ 2 µs/kick.
2. **Three trajectory decodes per bind** (from_state's `at_radius` + `decoded_event`, then `bind_in`'s own decode): one decode would do; the residual path alone is 2.7 µs.
3. **Secondaries 7.7 µs per kick for one moon:** a full binding clone + history search + trajectory state evaluation per kick, per secondary. The moon's tube changes only when the moon rebinds; a per-doll memo of the secondaries' bindings between their rebinds (validated by digest) deletes most of it.
4. Structural (changes bits, belongs to the law's owner, not the lab): in this scene **every kick fires** — the sigma-delta carry absorbs nothing — so a 1-quantum Δv triggers a full tube refit each time. Carrying the Δv in the binding's integer residual and refolding at a certificate boundary would delete most of the remaining bind cost, but it changes the map's error terms (kick deferral is O(Δv·H)) — that is a law decision with the Jacobi judge, not a cache.

## The lens
SpaceX's delete-first found a redundant generator, but the deeper miss is that I accelerated the incumbent representation instead of questioning it: the table says the kick is 98% bookkeeping, and the honest structural questions (4 above, and "why does a firing kick rebind at all") are law-level, one-way-door decisions this lens is prone to underweight ("a frozen law is a one-way door" is in my own blind spot).

## Patch contents (saved by run.sh)
- `crates/space/src/binding.rs`: the adoptable `shape_memo` (+cap) wired into `from_state`'s Cycle branch; lab-only scaffolding to drop on adoption: `STAGES`/`take_stages` instrumentation, the `MEMO_ON` A/B switch, per-stage timers.
- `crates/universe/examples/kick_stages.rs` (new): the stage-split A/B replay; reusable as the kick-cost probe.

## Grade (author's self-assessment, for the checkers)
Silver: reproduced, held-out predictions held, bit-identical, adoptable in one step — but it moves the bottleneck ~1.2×, not 10×. The stage table plus the named levers 1–3 are what the next run should pick up (together they point at ≥ 3× on the kick without touching the law).

One substantive result: the kick's cost table with a verified deletion.

**A found impurity, fixed in the patch:** `ShapeMemo::get` is NOT equivalent to `Orbit::compile` for unstable circles (`k == UNIT`, compactness ≥ 1/6): compile has a special symbolic-circle branch that mutates the shape; the memo's generic builder refuses them (`NoBoundOrbit`). Discovered by `crates/space`'s own `exact_parabolic_and_unstable_circle_ties_are_generators` test failing on the first patched build. The patch passes `k == UNIT` keys through to `Orbit::compile` unmemoized, restoring exact equivalence (all space tests then pass; digests unchanged). **Note for the integrator:** `crates/space/src/events/records.rs` uses the same `ShapeMemo` for the events store and would refuse an unstable-circle key that `Orbit::compile` accepts — same latent gap, worth an owner's eye.
