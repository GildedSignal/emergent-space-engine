# Five lessons from practitioners with skin in the game
Bottleneck: board focus #1 (kicks dominate cost; the lever is cadence), plus the slack skin
and the top scaling risk. Quotes verbatim from Julien's Readwise export (cached here).

1. **Kick when the state leaves the band, not when the clock says so.** "The more frequently
   you look at data, the more noise you are disproportionally likely to get" — Farnam
   Street, *20 Aphorisms from Nassim Taleb*. Option desks paying real spreads rehedge only
   outside a band (zone hedging, Whalley–Wilmott 1997; band ∝ (cost×curvature×variance)^⅓).
   Change: trigger = |state − tube| > w per body. Tested: 2.8–5.2× (e=0.6), 4.0–6.7× (e=0.9)
   fewer kicks at equal worst error; 0 kicks in 10 orbits with no tide (fixed paid 639).

2. **The band is the certificate; size it at the growth tail.** "How frequent the profit is
   irrelevant; it is the magnitude of the outcome that counts." — Taleb, *Fooled by
   Randomness*. Fixed-cadence error is emergent, ∝Δt² (measured 5.3e-3→3.6e-7, j=4→512); a
   band *states* its worst error (measured maxdev = w, 1.00–1.05×). Change: gates judge the
   bound (bounded = the error type); w is bought at periapsis/conjunction, not the mean. My
   coarse-check probe could not burst it (≤1.05×) — tail-sizing is unproven at steep
   conjunctions, which the law already routes to exact pair events.

3. **The slack skin is a barbell, sized by the p99 burst, not the mean frame.** "so is the
   barbell a domestication, not an elimination, of uncertainty." — Taleb, *Antifragile*.
   Shipped speculation (branch prediction, ahead-compute) runs the cheap likely-next work on
   idle units, discards it when wrong; airline padding is sized on the delay tail. Change:
   the skin's look-ahead horizon = p99 burst length of the surprise stream from a plane
   replay. Test: replay the plane's log, count storm frames before/after a p99 horizon.

4. **One primitive — (certificate, expiry) — for kicks and encounters alike.** "Invert,
   always invert." — Munger (Farnam Street); his own notes: "O(N²) knowledge growth – each
   incremental piece of content you consume has *N* other ideas/atoms/sources to connect to"
   (reasonabledeviations.com). Sweep-and-prune/KDS (shipped games): a certificate predicts
   its own failure time (next swap; next conjunction by continued fractions — the r8 v2
   lead); nothing is re-scanned. Change: the band's crossing time is computable; kicks and
   encounters share one event heap. Test: Binet-cone harness emits expiries; work/orbit → 0.

5. **Adopt the pending deletion; concentrate on the one representation.** "Removing radar and
   ultrasonic sensors and relying solely on vision may make the perception problem easier."
   — Karpathy, Lex Fridman #333 (export text verbatim; an AI-notes summary, not transcript).
   Each extra channel costs streaming, fusion and maintenance and fragments improvement;
   Tesla shipped the deletion. Change: delete the measured-unused `shipmem` and `encounters`
   crates (~4,500 lines, HANDOFF 6 Oct); design lives in `docs/law.md`. Test: delete, run the suite unchanged.
