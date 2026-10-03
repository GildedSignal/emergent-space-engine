# Predictions — 20261003-1842-spacex-b139

Written before the decisive experiment (wiring `crates/space`'s existing exact `ShapeMemo`
into `Rebinding::from_state`'s Cycle branch, behind a thread-local capped cache).

## Tuned on
Seed 1, `Order::Sparse`, 1 thread, 48 members, 10 s of frames (`kick_stages 10`):
kick median 22.53 µs, p99 31.17 µs; 13,801 `from_state` calls, all Cycle, **24 distinct
shape keys, hit rate 0.998**; fired rebinds 13,800 / carried 0; stage split per call:
fit_key 2.31, compile 3.36, at_radius 0.80, residual 2.71 µs.
Baseline digests: replay `8f353a2b…74f73bb`, universe `cb815b7e…d44d4ebb8`.

## Predictions (held-out cases first)

1. **Digests are bit-identical.** With the memo, the same plane replay produces the same
   `replay_digest` and `universe_digest` as the baseline, because `ShapeMemo::get` returns
   the same content `Orbit::compile` builds (already asserted by `crates/space`'s own test
   `api.rs`: memo advance/period equal compile's). A pure cache cannot change bits.
2. **Held-out seed (7) and held-out order (not run yet):** shape-key hit rate stays ≥ 0.95,
   because a firing kick changes the true conic by ~2⁻⁵⁹ relative while the shape key
   quantizes at 48 bits — consecutive kicks of one body land on the same key for thousands
   of kicks. If the hit rate were an artifact of seed 1, this prediction fails.
3. **Kick median drops to ~19 µs** (compile 3.36 → ≤ 0.3 µs/call; the rest of `bind`
   unchanged). That is a ~15% cut of the kick, not a 10×: fit_key (2.3) and the residual
   path (2.7) remain, and they are the next levers.
4. **All `emergent-universe` tests pass unchanged** (no behaviour change to test).
5. **Passages are not helped**: ships on flyby orbits bind `Passage`s whose tail depends on
   the continuous edge, so this scene's gain does not transfer to flyby-dominated scenes.
   The plane's own stream (this run) showed 0 passages, so the headline number is honest
   for the plane but must not be sold for encounters-heavy scenes.
6. **Memory**: distinct shapes per running scene are tens (24 here), each a knot table;
   a 4096-entry cap clears on exceed — bounded by construction.

## What would make the claim wrong

- Any digest difference (would mean the memo changed content, not just caching).
- Hit rate collapsing on other seeds (would mean the 99.8% is a seed-1 artifact).
- `cargo test -p emergent-universe` failing after the change.
