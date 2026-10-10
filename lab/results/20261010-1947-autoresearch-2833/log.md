# Autoresearch log — kick resolver (universe --kick-bench), metric: kick_us median (21 reps, digest-checked)

Artifact: the plane's pure kick resolver (`crates/universe/src/step.rs::process` on `What::Kick`),
behaviours pinned by the bench digest (971e97d7… seed 1) and the universe test suite.

Phase profile (clean spans, instrumented then reverted): rebind ≈ 2/3 of the kick:
tau readout 9.6 µs (two orbit_state decodes), fit_key 6.4, compile 7.5, residual decode 5.2,
at_radius 1.6; outside rebind: readout 5.3, secondaries 3.7, force 6.5.

| # | Hypothesis | Change | Metric (seed1/2/3 µs) | Verdict |
|---|---|---|---|---|
| 0 | — | baseline (clean tree, 21 reps) | 45.59 / 44.88 / 44.12 | — |
| 1 | rebind recomputes a fixed quantity: the tube's proper time at its own event_time (bind_in already returns it as `Bound.orbit`) | cache `proper_at_event: Scalar` on Binding, filled by every constructor; `bind_exact` becomes fallible | 43.44 (single-shot; −7.3%) | KEPT (digest identical) |
| 2 | orbit_state computes the cartesian integer word and discards it (`decode(...)?.1`) | split `decode_orbit` (state only) out of `decode`; `orbit_state` uses it | 40.87 / 40.66 / 39.95 (−10.3/−9.5/−9.5%) | KEPT (digests identical, seeds 1–3) |
| 3 | the compile's knot Vec grows by doubling (P2: 1–2 µs) | `knots.reserve(96)` in `OrbitShape::bound` | 40.85/42.87 vs 42.57 without — below the ~4% batch noise floor | REVERTED (unmeasurable ⇒ weight) |
| — | stop rule | three consecutive rounds < 10% (7.3%, ~3%, <2%) | — | loop stopped |

Held-out (never tuned on; baselines recorded before the post-change values were used):
seeds 2/3 −9.5/−9.4%; seconds 6 −7.5%; `--describe` md5 identical; tests 74/74 green.
Final: 41.12 / 40.63 / 39.98 µs. Best idea: **cache what the binding already computed at
its own event** — the tau readout's second term was a pure re-derivation, the exact thing
principle 3 forbids evolving.

Structural change that would beat this best (the lens's blind spot, stated): stop
recompiling the cycle per kick — exact-offset re-anchoring (law.md line 35), a law change,
not a cache. Second: per-(doll, tick) secondary readout cache, invisible in single-kick
kick_us but real in frame cost.
