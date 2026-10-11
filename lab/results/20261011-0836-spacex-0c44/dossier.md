# Dossier — 20261011-0836-spacex-0c44 (spacex lens)

## Claim

On the motion-law-v2 plane **no fixed kick cadence passes the plane's own frozen gates**: B13's
worst flybys are cadence-independent (worst ΔE *grows* 2.1e-2 → 1.8e-1 as the cadence is refined
4×), and B14 fails at the only cadence its 60 s gate budget admits (apsides 0/53) while timing
out at every finer one — so the board's question #1, "fewer kicks per orbit at the same
behaviour" *at a fixed cadence*, is dead on v2: the flyby tail is a representation error, not a
cadence error, and the per-kick cost (43 µs median, zero memo reuse, one full cycle rebind per
kick) is the lever the jet already targets.

## Bottleneck

Board focus #1 (kicks dominate the engine's cost; the lever is cadence) and the top of
`q-cadence`'s brief. Expected gain: re-aiming the lever — a per-regime cadence rule cannot fix
B13's tail (no 2^N does), and the 43 µs/kick rebind is a ~1000× idiot index against the ~50 ns
of arithmetic a kick is (readout, one acceleration, two integer adds). What it deletes: the
search for a better *fixed* cadence, and any hope that the shipped default (step_log2 = 7) can
be lowered or raised into a pass.

## Evidence

All commands from the repo root, binary at `/home/glmlab/lab-target-3/release/xtask`
(`cargo build --offline --release -p xtask`, 38 s). Cloud Linux/x86: walls are order-of-magnitude
only; the pass counts and error magnitudes are exact and machine-independent. Logs:
`work/sweep.log`, `work/extra.log`, event counts in `work/sweep.log.trace` (PLANE_TRACE=1).

```sh
# B13 sweep (each ≤ 9 s): steps 7..1 and the refinement end 8, 9
xtask behave --law plane --gates B13 --plane-step N   # N in 1..9
# B14 at the only cadence that fits its own 60 s limit
xtask behave --law plane --gates B14 --plane-step 2
# per-kick cost, distinct kicks only (the bench de-duplicates re-timed kicks)
xtask universe --kick-bench --seconds 8
```

**B13 (assists; 64 flybys, periapsis 1.2–50 R_p, v∞ 5–20 km/s; same 9 oracle-domain draws
replaced at every N, so the population is identical across N):**

| N (kicks/period) | within 1e-2 | worst ΔE | worst ΔL | wall |
|---|---|---|---|---|
| 9 (512) | 58/64 | 1.77e-1 | 1.28e0 | 8.3 s |
| 8 (256) | 62/64 | 1.26e-1 | 4.39e-1 | 4.2 s |
| 7 (128, default) | 60/64 | 2.12e-2 | 2.12e-2 | 2.1 s |
| 6 (64) | 41/64 | 8.47e-2 | 8.48e-2 | 1.1 s |
| 5 (32) | 15/64 | 3.39e-1 | 3.39e-1 | 0.6 s |
| 4 (16) | 3/64 | 1.34e0 | 1.34e0 | 0.3 s |
| 3 (8) | 1/64 | 2.87e3 | 1.22e2 | 0.15 s |
| 2, 1 | 0/64 | 2.87e3 | 3.64e2 | ~0.1 s |

Coarsening degrades as ~h² (worst 2.12e-2 → 8.47e-2 → 3.39e-1 → 1.34e0, ×4 per halving), but
**refining does not converge the tail**: worst error *grows* 2.12e-2 → 1.26e-1 → 1.77e-1 (ΔL to
1.28e0) and the within-threshold count is non-monotonic (60 → 62 → 58). The 2–6 deepest flybys
sit on a cadence-independent error floor of ~1e-1 — the close-encounter representation
(H0214's diagnosis), now measured on v2 at up to 512 kicks/period. No fixed cadence passes
B13 (needs ≥ 63/64); none ever will.

**B14 (Hill moons, 256 moons, 50 planet orbits):** steps 7, 6, 5, 4 all `FAIL timeout` at the
gate's own 60 s limit (four runs, `work/sweep.log`); at step 2 (4 kicks/orbit) it completes in
59.75 s and fails on behaviour: classification 243/255 (needs ≥ 99%), **apsides 0/53 within 10%
(worst inf; 102 of 155 bound moons without a stable rate)**. The wall is ~flat ≈ 60 s across
steps 2–7 (oracle-dominated), with the law's cadence-bound share on top — so the gate admits
only cadences at which the law's behaviour is broken. B14 has no passing fixed cadence either.

**Cost anatomy (kick bench, the plane's own scripted scene, distinct kicks):** median 43.4 µs
per kick, p99 59.9 µs; `cycle_rebinds` = kicks (23/23), `exact_hit_rate` 0.0,
`quantized_hit_rate` 0.0 — every distinct kick compiles a fresh cycle; nothing is reused. At the
default cadence one body-orbit costs ≈ 128 × 43 µs ≈ 5.5 ms of CPU; B13's gate wall tracks 2^N
exactly (2.13 s → 0.07 s over N = 7 → 1), confirming the law's cost is cadence-linear where the
oracle does not dominate. [INFERENCE] The rebind (the compile) is the occupant of the ~1000×
idiot index: the kick's own arithmetic is readout + one acceleration + two integer adds
(`step.rs::kick`), and the compile (band cuts, Gauss–Legendre panels, a Newton solve) is the
only heavy part left; this was not separately timed.

B17 is unchanged by this run (passes at steps 4–6 in the weak field, law.md; not re-swept for
time). B12 was not swept: its statistic is known miscalibrated and is being rebuilt (queue
`q-b12-design`); its cadence behaviour is unmeasurable until then.

## Predictions

`predictions.md` was written before the sweep. **The pre-registered hypothesis is killed**: I
predicted a knee at N ≈ 3 (B13 holding to 8 kicks/orbit, B14 to N=4, a 16× waste in the shipped
default). Measured: B13 fails at *every* N from 1 to 9; B14 cannot run at N ≥ 3 within its own
budget and fails at N = 2. What held: the h² scaling in the coarse direction (prediction 4's
mechanism), the negative control (N=1–2 fail decisively — the gates do see cadence), and the
cost prediction (per-kick µs cadence-independent; law cost ∝ 2^N, confirmed by B13 walls and
the bench). The inversion — refinement *worsening* the worst flyby — was not predicted and is
the strongest single datum here.

## What would make it wrong

- If B13's tail failures are oracle-domain artifacts (the reference is a point mass; the
  adjudicated rule already replaces reference passes inside the planet — the same 9 draws are
  replaced at every N, so the judged population is clean; but a *law*-side surface or capture
  refusal at the closest periapsis would mimic a floor). Check: per-draw error vs periapsis at
  N=8/9; the trace logs `refused` and `lost` counts per run.
- If the 43 µs is not the rebind (e.g. it hides in the readout or the forces): instrument
  `step::process` once. The jet's value scales with that fraction.
- If B14's oracle (not the law) is what times out at N ≥ 3, then "B14 has no passing cadence"
  is a judge-cost statement, not a law statement — the behaviour verdict at N=2 stands either
  way. Separating them needs a law-only timing harness for the B14 scene.

## Cost of adoption, and fit

Adoption is a re-aiming, not a build: (1) q-cadence's brief should state that no fixed 2^N
passes B12–B14+B17 on v2, and that the deep-flyby tail is out of its scope (a representation
fix, already the changeover/encounter work); (2) the jet (law.md "not adopted ... re-anchored",
gold by one checker, second never ran) becomes the priority for the *cost* side: it attacks the
one compile per kick that this run measures at 100% of distinct kicks. PRINCIPLES: "A failed
expectation is not automatically a failed method: diagnose which one broke" (#9, and the
failure here is the fixed-cadence premise, not the kick layer); "Compute only surprises" (#3 —
a rebind that recompiles an orbit it cannot distinguish from the last one is compute done for
no reason); "a test that cannot fail is a control" (the N=1 negative control failed as
required, so the sweep measures something).

## The lens

SpaceX's idiot index pointed at the kick before the sweep did: 43 µs against ~50 ns of
arithmetic. The lens also pushed "question the requirement" — and the requirement here (a
fixed cadence to minimize) is what broke. What the lens may have made me miss: I nearly
framed the run as "find the knee and cut the default 16×" (delete-and-accelerate reflex); the
tail's non-convergence and B14's flat oracle wall are regime facts a rocket-shop lens is
tempted to steamroll. The blind spot named in the lens card — a frozen law is a one-way door —
cuts the other way too: no cadence should be frozen into the default until the per-regime rule
exists.
