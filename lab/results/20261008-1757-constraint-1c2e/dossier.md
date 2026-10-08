# Dossier — 20261008-1757-constraint-1c2e (lens: the constraint)

**Claim.** On the plane as shipped, the engine's per-event constraint is the orbit-shape compile
that (almost) every kick pays, and its price is a measured law — 0.73 µs per knot, knots ≈ 6 +
15.4·log₂(r_apo/r_peri), the same dyadic law as B9's readout bound — which the plane's own
workload makes expensive: 76% of its kicks are fleet leavers at median e = 0.94 (p99 = 0.9995),
so the compile is 54% of the mean kick (59% of the median) and carries the p99 tail (415 µs);
no bit-identical reuse exists (807/807 distinct ShapeKeys), so the levers are cadence and a
law-level quantized grid — plus one new representation lead this run prices: compile only the arc
the next event reads.

**Bottleneck.** Board #1 ("fewer kicks per orbit at the same behaviour: kicks dominate the
engine's cost"). Expected gain in orders of magnitude: the levers now have prices — cadence 4×
(32→8/orbit) at any e; the quantized relative-gap grid ~18× of compile work on this mix (45 shape
cells served 807 compiles) but changes canonical outcomes (5 Oct adjudication; Julien's call);
lazy arcs up to ~cadence× of compile work if the period can be had without the full integral.
What it deletes: per-kick compile work, concentrated exactly on the leavers fleets manufacture.

**Evidence** (Linux x86, 8 vCPU shared, load 0.7–1.2 during runs; orders of magnitude only; all
commands ≤ 60 s except the gate run; tree restored after the run, the two instruments are the
saved patch):

1. *The whole, at player pace* — `cargo run --release -p xtask -- universe --bench --seconds 20
   --rtf 100` (`bench-rtf100.json`): frame p50 4.57 ms / p99 10.8 / worst 11.2, zero hitches
   above 16.7 ms, rtf median 100.0; **engine 19.9% of the frame, view gather 67.5%** (a debug
   instrument, not the game's view); events/s 330; 71 bodies, 5075 bytes/body, catalogue_live 71.
   Smoothness is not the constraint at player scale — per-event throughput is.
2. *The kick, decomposed* — `universe --kick-bench --seconds 15 --rtf 100` with an added
   out-of-line `Orbit::compile(key)` re-run per sample and an e-dump of the 807 cycle rebinds
   (`kickbench-final.json`; replay digest unchanged, 10597678d37370c8; refused 0): kick mean
   106.8 µs / median 97.7 / p99 415.1 (n = 830); plane-made ships median 39.6; **leavers median
   103, mean 126**; compile of the same keys mean **57.6 µs over 807 compiles = 54% of the mean
   kick**; memo: cycle_rebinds 807, exact_shapes 807 (hit rate 0.0 — confirmed at the mechanism
   level: every kick's ShapeKey is distinct), quantized_shapes 45 (hit rate 0.944, the adjudicated
   law change); **e of the kicks: p10 0.006 / p50 0.872 / p90 0.9966 / p99 0.9995; leavers-only
   p50 0.941**. Seed 7 held out (`kickbench-seed7.json`): mean 93.1, p99 604, compile mean 48.3
   (1010), e p50 0.818 — same structure.
3. *The cost law* — `cargo run --release -p emergent-space --example compile_sweep`
   (`compile-sweep.txt`; periapsis 2²⁷ M weak field, 2³ M strong field held out): compile is
   exactly linear in knots — 1.37 knots/µs weak, 0.58 strong (2.3–2.5× at equal knots); knots =
   6 + 15.4·log₂((1+e)/(1−e)): e 0.1 → 4.8 µs, e 0.9 → 50.3, e 0.99 → 90.7 (weak). The plane's
   measured compile mean (57.6 µs ≈ 79 knots) sits between its e p50 and p90, as the law predicts.
4. *Gates* — `behave --law plane` (99 s): matches the handoff exactly (B13 60/64; B14 timeout
   60.1 s marginal; B12 known miscalibrated; G1–G6, B7, B9–B11 unanswered by the adapter's
   design). Nothing new; the instrument agrees with the record.

*Scale Fermi with these constants* (per game-second, rtf 1): the plane's cadence is ~32
kicks/orbit and its ships' orbits are ~1.2 game-hours (measured: 830 distinct kicks per 1500
game-seconds over a ~71-body scene ≈ 0.0075 kicks/body/game-s). A billion bodies at that cadence
and period ≈ 7.5M kicks/s ≈ 800 x86 cores at the measured 9.4k kicks/s/core; the same billion at
real-AU periods (1 year) is ~10³ kicks/s ≈ ½ core. So the billion-body kick bill is decided by
where bodies orbit (period) and at what e — the cost law per kick and the period distribution,
not N alone. The e-mix is a *design output*: the fleet's ejection machinery manufactures
near-parabolic levers, the most expensive kind per orbit; at goal scale, ejection design is a
throughput decision.

**Predictions** (`predictions.md`, written before the sweep and the e-dump): P1 held in form
(cost strictly linear in log₂(r_apo/r_peri)) and at the top of its band on magnitude (10.5× from
e 0.1→0.9 against a predicted 5–8×). P2 **failed**: the plane's kick mix is near-parabolic (p50
e = 0.87), not near-circular (predicted p50 < 0.2); its second half held (the leavers' 102 µs
median is the e tail). P3 **failed as written** (no single weak-field compile ≥ 300 µs at
e ≤ 0.99; the strong field reaches 226 µs) but the mechanism held: the observed p99 kick of
415 µs is the e = 0.9995 tail plus the rest of the resolver. P4 held: deleting the compile
entirely buys ≤ 2.6×, so no faster compile reaches a billion; cadence or reuse-of-shape-work must
move.

**What would make it wrong.** The compile share is measured out-of-line (a re-run of the same
key after the resolver finished): if the in-line compile enjoyed strictly warmer state than my
re-run, the share is overstated; if in-line allocator pressure is higher, understated. One
machine, shared, x86 — the M1 re-measures (the *law*, knots ∝ log₂(r_apo/r_peri), should
transfer; the µs per knot will not). The levers' prices assume the plane's mix; a belt of
low-e orbits prices the quantized grid lower. The knot law is fit on 15 eccentricities × 2 field
strengths; a panel-CAP change moves the slope, not the log shape.

**Cost of adoption.** Nothing to adopt for the finding itself. The 18× quantized-grid lever
changes canonical outcomes and is Julien's (the code already refuses to apply it silently:
`OrbitKey::quantized`, "never silently applied to an exact key"). Cadence is the board's live
lever. The new lead — *lazy arcs: compile only the knot panels the next event will read* — is
bit-compatible in sums but has one named obstacle: the scheduler needs the period P, which today
is a byproduct of the full integral (knots.last()), so laziness needs a closed-form or quantized
P; that experiment is the natural next run. It also composes with principle 17 (compute ahead in
idle time): the far-apoapsis panels of a near-parabolic leaver are exactly the work that can wait.

**Fit with PRINCIPLES.** "Compute only surprises" (#3): every kick surprises the shape, and the
price of that surprise is now a law, not a mystery. "A fix signals the wrong representation"
(#19): if near-parabolic leavers keep dominating the tail, the question is their representation
(a passage, not a bound cycle, near e → 1), not a faster integrator. "The best part is no part"
(#17): 15.4 knots per log₂ of apoapsis ratio is the part this run found to delete. "Measure
before claiming" (#10) and the lens's own rule — the constraint was read off the plane's
dashboard, and the Fermi above says where it moves next: to the period/e distribution of the
billion (an orbit-design question), then to the fit/remainder path (the remaining ~45 µs), then
to encounters.

**The lens.** Goldratt prices one constraint against the goal; I took the scene as given. The
view gather holds 67% of today's frame and I dismissed it as "a debug instrument" without
measuring how the real view's gather scales with visible bodies — at larger N it could become
the frame constraint before the engine's event path does. I also did not measure the fit /
remainder half of the kick (the ~45 µs outside the compile); the constraint may already be
hiding there for low-e belts, where the compile is cheap.
