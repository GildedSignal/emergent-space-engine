# Predictions (written before the decisive run)

Question: how many bits of live distinguishing information (H_live) does the plane's scene gain per game-second, by event kind — and what does that rate say about 10⁹ bodies in 8 GB?

Operational definition used (a proposal for the directed build `b-h-live`, which owns the final one): at the single funnel where a body's canonical record changes (`Universe::apply`), take the integer deltas of the stored canonical words — tube key, periapsis angle (wrapping), periapsis time, sub-quantum velocity carries — and measure, per (event kind, body, field), the empirical entropy of the delta given that context. A distinction is a non-zero-entropy delta; a fully zero-delta event stores nothing (it was predictable from the body's own last state). Decisions are the input words' empirical entropy. Not counted (stated, not hidden): the fleet members' internal lattice carries (the dense order lives in `crates/lattice*`, out of reach of a 60-minute patch) and the `ext` energy register.

The scene (seed 1): 4 dolls, 28 bodies + 1 fleet of 48 members; rtf 100, 8 s wall = 800 game-seconds; ~427 events/s reported by the existing dashboard.

## Held-out predictions (not tuned on)

- P1 (kicks are mostly predictable): median per-event conditional entropy of the tube words for non-player ships ≤ 12 bits/event.
- P2 (zero-delta share): ≥ 50% of non-player ship events have an all-zero canonical delta (nothing stored).
- P3 (concentration): the player's body accounts for a per-body event rate ≥ 5× any hauler/orbiter; lone haulers and orbiters sit at ≤ 2 events/game-second each.
- P4 (scene total): H_live for the whole scene lands between 10² and 10⁴ bits/game-second (point estimate ~2×10³).
- P5 (extrapolation verdict): at the measured per-ship bit rate, 10⁹ uniformly-active bodies exceed the 8 GB budget within one game-hour by ≥ 100× (so the fit must come from a small active fraction and/or scar healing — reabsorption — not from the body count).
- P6 (reabsorption today): with populations not wired, nothing heals a scar; reabsorption is only bodies leaving (lost/dissolved) and is < 20% of gained bits.

## Kill criterion for the probe itself

If the instrumented build's digest differs from the clean build's at the same seed, rtf and cut, the measurement is void (instrumentation must be read-only). If the per-kind event counts do not add up to the dashboard's events_per_second × game-seconds within 1%, the funnel misses events and the number is not H_live's.

## Fermi estimate before any code

71 bodies, ~6 events/body/game-second, guess 3–10 bits per non-zero event, half the events zero-delta: 71 × 6 × 0.5 × 6 bits ≈ 1.3×10³ bits/game-second ≈ 160 B/s for the scene. If 10⁹ bodies behaved like that: 10⁹/71 × 160 B/s ≈ 2.2 GB/s of new state per game-second — 8 GB fills in ~4 game-seconds. So the naive uniform extrapolation must fail (P5), and the real question the measurement answers is which kinds carry the bits and how concentrated they are.
