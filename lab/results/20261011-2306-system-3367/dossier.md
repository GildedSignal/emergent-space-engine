# Dossier: the plane's measured cost vs the autopilot queue

**Claim.** On the plane's own integer resolver, every distinct kick re-fits a fresh exact cycle
(1125/1125, exact memo hit 0.0%) while 95.5% of those fits share only 51 quantized law keys, the
motion law v2 is the plane's most expensive mechanism per event (the player ≈ 1.0 ms per resolved
item, 25–50× a fleet slice), and the frame itself is the debug view (64–71% of wall, engine ≤ 24%
even unpaced) — so the 14-build queue extends the expensive path before the adopted-but-unbuilt
memo/jet deletes ~95% of its cycle fits, and no engine build can show up in the frame dashboard at
this scale.

**Bottleneck.** Board focus line 1 (kicks dominate the engine's cost) and the queue's order
(`lab/queue.txt`: 14 `b-*` builds, six of which extend the v2 path). Expected gain: the memo hook
(assigned to Sonnet, in flight, `docs/law.md` "Not adopted: a quantized (E, L) memo … the jet,
re-anchored") makes a kick's rebind a multiply-add on a shared cycle instead of a compile
(`docs/representation.md`: "a kick updates the cycle by a multiply-add"), deleting ~95% of cycle
compiles on the kick path. What it lets us delete: the per-kick exact fit (and, once landed, the
reason to spend builds shaving the fit itself).

## Evidence

Commands (each ≤ 60 s; Linux/x86, 8 vCPU, load 0.6–1.0, 15 GB, `CARGO_TARGET_DIR` as configured;
orders of magnitude only, the M1 re-measures; JSON in this folder):

```
cargo build --release -p xtask
$CARGO_TARGET_DIR/release/xtask universe --bench --rtf 100 --seconds 30        # bench-rtf100.json
$CARGO_TARGET_DIR/release/xtask universe --bench --rtf 100 --seconds 10 --unpaced  # bench-rtf100-unpaced.json
$CARGO_TARGET_DIR/release/xtask universe --bench --rtf 1000 --seconds 10       # bench-rtf1000.json
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --rtf 100 --seconds 30   # kickbench-rtf100.json
```

Scene: 4 dolls, 28 bodies, 1 fleet of 48 (`--describe`). Digests: bench rtf 100
`41343a143a92f956…` at cut 609076340; kick replay `0e02bf0f34481650…`.

1. **The frame is the view.** Shares of wall frame time (paced rtf 100 / unpaced rtf 100 / paced
   rtf 1000): view gather 70.6 / 63.8 / 68.9%; view JSON + wire 13.0 / 12.0 / 6.6%; engine 16.4 /
   24.1 / 24.4%. Even unpaced (no 5 ms budget cap) the engine stays under a quarter. Frame p50
   2.56 ms paced rtf 100; p99 9.2 ms; worst 11.96 ms; zero hitches > 16.7 ms; rtf median holds
   target with 16/1800 overflow frames (rtf 100) and 46/600 (rtf 1000) — the smooth-dip overflow
   behaves as designed (`docs/plane.md` foundation 7).
2. **Per-event cost by mechanism** (the universe's own accounting, `engine_cost_by_kind`):
   player (motion law v2, fictitious clock + `p_t` register) 1009 / 365 / 982 µs per item at rtf
   100 paced / 100 unpaced / 1000; ship (root-doll ships and leaver rebinds, same law) 179 / 68 /
   157 µs; fleet (Fermi-frame battle slices, the old dense order) 39.5 / 20.4 / 33.2 µs. The
   newest law is the most expensive per event, 5–30× the machinery it is scheduled to replace.
3. **Kicks re-compile, exactly.** Kick bench (pure resolver, distinct pending kicks only): 1158
   kicks; made bodies median 35 µs (p99 67), fleet leavers median 93 µs (p99 401); **memo:
   cycle_rebinds 1125, exact_shapes 1125, exact_hit_rate 0.0; quantized_shapes 51,
   quantized_hit_rate 0.955**. The 5 October artifact correction ("the exact memo hits 0% on
   distinct kicks") is confirmed on the real integer resolver, not a float replica.
4. **Two motion laws coexist** (`crates/universe/src/step.rs` header: "Two clocks, until the dolls
   are coordinates"): v2 for root-doll ships and the player; the Wisdom–Holman/SyMBA split for
   planets' dolls. Handoffs: 0 in every run — the standard bench never crosses a doll edge, so the
   handoff machinery (and `b-handoff-surface`) is unexercised by the dashboard's own scene.

## Predictions

`predictions.md` was written before the runs. P1 held (engine share < 40%: 16–24%; view > 50%:
64–84%). P2 held (leavers 68% of kicks; 35–93 µs on x86 against 29 µs on M1). P3 held exactly
(0.0% exact, 95.5% quantized against the predicted ≈ 0% and > 80%). P4 held (paced p99 9.2 ms
< 8 ms was my threshold — **missed**: p99 9.2 ms on the shared box, though zero hitches above
   16.7 ms; the M1's 2.7 ms p99 does not transfer, as expected for x86). P5 held (kicks 1365 of
2875 engine events at rtf 100; step = 1/64 radial period per `step_for`).

## What would make it wrong

- If the player's ~1 ms is not the fit but the fictitious-clock time transformation or the i128
  register, the memo deletes less of it than claimed. I could not attribute it: `crates/space`'s
  `profile` feature instruments `compile_sums` (roots/cuts/integration/convert), but the plane's
  rebinds go through `orbit.rs`'s `Orbit::compile`, which is uninstrumented — my instrumented run
  (`--features emergent-space/profile`, `kickbench-rtf100-profile.json`) returned zero stages.
  That gap is itself a finding: the shipped profiler measures a path the plane does not use.
- If the queue's v2 builds (energy register, plunge tubes, root keys) are judged only by gates, the
  per-event cost regression risk is invisible until the scene grows; a 2× on the player's 1 ms
  halves the engine budget headroom at rtf 1000 (46/600 frames already overflow).
- The view share falls as scenes grow (one sample per pixel caps it, `representation.md` §2), so
  "the frame is the view" is a statement about the plane's scale, not about 10⁹ bodies.

## Cost of adoption, fit with PRINCIPLES

Adoption is ordering, not code: land the memo hook (Sonnet, in flight) and re-measure the kick
bench before reviewing the v2-extending builds; wire `Orbit::compile` into the profiler so
per-event attribution exists; add one bench scene that actually hands off. Nothing here weakens a
gate. Principle 1 ("the cheapest compute is compute not done") and 18 ("the right question, then
the representation"): the per-kick exact fit is compute done because the representation makes an
integer kick a new shape; the adopted memo/jet is the representation that makes it an addition.
Principle 22 ("the simulation tells us what's next not us"): the queue is a 6 October listicle;
this run re-reads it off the plane's dashboard and per-event costs. Principle 19: the profiler
measuring an unused path is a fix-shaped smell, reported, not patched.

## The lens

What the whole-system lens may have missed: the elegant unification ("kicks are compiles; make
them additions") hides the hard special case — the quantized key is a law change on its own (the
taste log: it "changes orbits"), so exactness rides entirely on the jet's offset-plus-derivatives
and its √(floor/C) re-anchor, which this run did not test; deep/strong-regime kicks may not hit
the memo at all. And cost-by-kind charges a batch of leaver rebinds to "ship", so the 179 µs
figure mixes populations; the kick bench's split (35 vs 93 µs) is the cleaner instrument. The
harness's `machine_state` is macOS-only (every field "unavailable" on Linux): "measure the way the
player runs it, heat and load" cannot be recorded on the lab host as built — load was recovered
from `uptime` in the bench JSON instead.

## Files

`bench-rtf100.json`, `bench-rtf100-unpaced.json`, `bench-rtf1000.json`,
`kickbench-rtf100.json`, `kickbench-rtf100-profile.json`, `predictions.md`. Tree edit (saved as
this run's patch): `xtask/src/universe/kick_bench.rs` gains the `cycle_compile_ns` block (needs
`--features emergent-space/profile`; currently reports zeros, see above).
