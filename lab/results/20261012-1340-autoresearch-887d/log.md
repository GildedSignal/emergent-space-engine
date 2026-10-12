# Autoresearch log — 20261012-1340 (artifact: the plane's kick path; scalar: ns/kick)

Metric: bench_kick 64 ships / 2 planet periods / step_log2 7, threads=1. Baseline 38.8 µs/kick, digest 82d40ca8…f324.
Verification per round: digest identical + event counts identical. Machine load spikes (shared window) → interleaved A/B binaries when a round looked ambiguous.

| # | Hypothesis | Change | ns/kick | Verdict |
|---|---|---|---|---|
| 0 | — | baseline (instrumented, timers add ~0) | 38,837 | — |
| 1 | `from_state` computes a residual `bind_in` discards (it recomputes its own against the doll decode) | split `from_state` / `from_state_fit`; bind path takes the fit only; handoff path (`TubeEvent::bind`) keeps the residual wrapper | 35,771 (−7.8%) | KEEP |
| 2 | `rebind` re-decodes `orbit_state(old.event_time)`, which the previous `bind` already returned as `Bound.orbit` | cache it on `Binding.orbit` (filled at all 4 construction sites) | 33,300 (−7.0%) | KEEP |
| 3 | `kick_clock` decodes at `t` (`readout`), `rebind` decodes the same `t` again | `readout_with_orbit` returns both; `rebind` takes the orbit as a parameter | 30,400 (−8.7%) | KEEP |
| 4 | see below | | | |

Profile after round 3 (per kick): rebind ≈ 19 µs total — from_state 12.4 (fit_key 3.9, Orbit::compile 4.0, at_radius 1.1), bind rest 3.4; readout 3.0; secondaries 1.5; field 0.8; kepler+plan 0.4; boundary events ≈ 8.4 µs outside kick_clock.
| 4 | boundary decodes (3 µs) only to check crash/leave certificates the tube's own periapsis/apoapsis already decide | `boundary_clock` reads `entry.trajectory.key()` bounds; exact fallback when the tube can cross | 28,800 (−8.6%) | KEEP |

Held-out (64/2/7 tuned, 16/3/7, 128/2/9, 64/1/6): digests identical to pristine on all four; gains 16.4–23.7% (window load inflates absolutes; interleaved A/B is the measurement). Tests: emergent-space + emergent-universe 66 passed, 0 failed. Stopped by the 60-minute budget, not by the stop rule (no three consecutive <10% rounds yet; rounds were 7.0–8.7%).
