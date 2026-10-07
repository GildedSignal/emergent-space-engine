# check2 (second checker, blind to check.md)

Grade: gold

**Abstract.** The dense order (the fleet battle's lattice events) is instrumented at its two funnels, and the scene's H_live exists with horizon-invariant objects. Reproduced: all seven digests bit-exact, including against the pristine clean tree (the instrumentation is read-only); every integer and scar field identical; tests 2+6+10 pass. Scene at the 800-game-second protocol: 59.7/64.3/56.6 bits/s entropy and 300.7/336.5/253.9 scar (seeds 1/2/7); contact scar 11.03 bits per body-event, tide ~75 per member-epoch. Adversarial seed 5 and horizons 100/3200 s hold the widths; the scar rate decays 1215→77 bits/s over 100→5000 s, so no single rate exists, as claimed. Gain: the memory decision number moves ~11× (dense scar is 10.9× the sparse order). Adoption: a default-off, +240-line recorder.

## Reproduction

Clean tree at a838a28; `git apply work/patch.diff`; `cargo build --release -p xtask` (shared lab-target, 30 s); all eight dossier commands rerun, each < 1 s wall.

- **Digests:** all seven (bench s1/s2/s7, sweep 200/400/1600/5000) reproduce bit-exact. Stronger than the dossier claims: I also built the **pristine clean tree** (no patch at all) — seed 1 gives the same digest `29f440d6…`, so both patches are digest-neutral and the VOID criterion in predictions.md is dead.
- **H numbers:** every deterministic field (calls, body_events, zero_delta, per-word mean/max/distinct/samples, fleet counters, all scar rates) matches to 1e-6 via rounded-hash comparison. The entropy floats differ in the last 1–2 ulps (HashMap iteration order): seed 1 sparse bits 7163.4565043022**02** vs the stored …2**06**. See "missed".
- **Cross-checks:** contacts 77/58/116 = fleet `contacts()`; epochs 310 = `epochs()`; leavers 43; E = 800/310 = 2.58 game-s; dk fires 12 of 5,856 member-word-events (0.2 %); tide carries 100 % distinct (2928/2928), means 37.35/37.31, max 42/48 ≤ 48-bit register; contact Δk max 8 ≤ 22. All as stated.
- **Tests:** emergent-lattice 2, emergent-engine 6, emergent-universe 10 — all pass.
- **Instrumentation cost:** my p50 1.018 ms (instrumented) vs 1.026 ms (clean) — the claimed ≤ 20 % overhead is conservative.
- **Arithmetic:** 0.356 bits/body/s × 3600 × 10⁹ = 160 GB/h ✓; 28.9 × 3600 = 13 kB/member/h ✓; 8 GB / 13 kB ≈ 6.2×10⁵ member-game-hours ✓; H(T) 18.0/22.2/30.1/45.3/55.4 kB ✓.

## Predictions

predictions.md (file time 17 min before the decisive JSONs at 12 min; the kill-criterion reference run at 22 min — correct order; run.log is empty, so file times are the only order evidence). P1 held (31×); P3 held where it bites (dk 95/97 distinct; entropy ≈ log₂ per-body samples, 6.83/word); P5, P6 held. P2's contact **rate** failed low by ~10× (0.096/s vs ≥ 1/s) — the collision soup never forms; P4 failed outright (0 % vs ≥ 80 % zero-delta epochs) and became finding 1: the tide carry moves for every member every epoch. Both failures are pre-registered, reported against the author, diagnosed, and the claim is explicitly re-based on what held (widths + H(T) + the fixed protocol, not a rate). That is H0183's discipline, not a miss.

## Attack (three cases of my own)

1. **Unseen seed 5, 800 game-s:** scene 49.1/230.9 bits/s (within the seed family); tide scar 74.63 (invariant holds); contact scar 15.51 — above seed 1's 11.03 but inside the pre-registered [10,120] band; Δk max 8 ≤ 22; dk fires 2×; counters 94 = 94.
2. **Unseen horizon 3200 game-s (seed 1):** epochs capped at 769 (the battle ends ~1984 game-s; fleet dead, members 0), tide entropy frozen at 16.87 and scar 73.31 — identical to 5000 s. The transient story is confirmed at a horizon the author never ran.
3. **Horizon 100 game-s (shorter than any swept):** all 77 contacts have already happened — sharper than the dossier's "first ~200 s". The scene scar rate decays monotonically 1215→720→444→301→227→136→77 bits/s over 100→5000 s: no single scene rate exists, exactly as claimed; H(T) is the protocol-free object.

## Novelty

docs/HISTORY.md has no H_live, dense-order or live-bits/s entry; the memory line ends at shipmem's "program plus scars" (programs are static; this measures live distinctions per game-second, the quantity the board says decides the 10⁹/8 GB question). The sparse protocol is the first author's (this run's base, carried in work-patch.diff and confirmed verbatim — 183 added lines on top, exactly hlive.rs + hooks + readout); the dense instrumentation, the scar-width definition and the horizon-invariance result are new. Nothing in HISTORY supersedes it.

## Goal fit

Board: "fitting 10⁹ in 8 GB … decided by distinctions created per game-second" — the dense half of that number was unmeasured; now the dense order is measured at 10.9× the sparse order's scar (275 vs 25 bits/s), an order-of-magnitude correction to the decision number, plus the first number for `b-h-live` to argue with (8 GB < 6×10⁵ member-game-hours at storage width). PRINCIPLES: "influences below one quantum accumulate" (§6, measured: the whole tide lives below one velocity quantum, 0.2 % integer firings, two ~37-bit carries); "Compute only surprises" (§3 — 33 % of contact body-events and the integer words store zero); "the memory floor is information" (§24). It also shows a premise wrong: a scene-wide rate does not exist.

## Why gold

Reproduced bit-exact including against the pristine tree; the invariants survive an unseen seed and unseen horizons; the two prediction failures are diagnosed and load-bearing for the finding rather than for the claim; adoption is one small default-off step. The bar "moves a bottleneck ≥ 10×" is met as a correction: the scene's storage rate was undercounted ~11× by the sparse-only protocol, and the 57 GB/hour face is now printed beside its 160 GB/hour face.

## What the author missed

- **"Every sparse entropy digit reproduces" is luck, not a property:** the entropy estimator sums floats in HashMap order, so its last 1–2 ulps vary per process (…202 vs …206 here). Integers and the digest are exact; only say that.
- **"Per body touched" is imprecise:** contact body-events include every body in the response batch; 33 % store zero bits. The mean is honest (zeros cost 0); the phrase is not.
- **The scene sum spans two representations of the same bodies** (catalogue words at apply, lattice words in the battle), so scene H_live is a storage/write accounting across layers, not a mutual-information bound. Right face for the memory bottleneck; the name invites the stronger reading.
- **My 100 s probe sharpens the transient:** all contacts complete within 100 game-s, not ~200 — the fixed-protocol number is even more transient-dominated than stated.
- **The tide-scar "invariant" drifts ~6 %** (77.5→73.3) with population composition; fine at orders of magnitude, but it is not a constant.
- The named deletion experiment (recompute the tide carry from the tube; correlated carries share one tidal field) is correctly identified — 48 carries moving together are not 48 independent words, so 75 bits/member/epoch is an upper face, and the run says so.
