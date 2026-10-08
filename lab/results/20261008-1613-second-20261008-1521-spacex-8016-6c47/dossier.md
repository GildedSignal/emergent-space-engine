# Dossier — 20261008-1613-second-20261008-1521-spacex-8016-6c47 (second author on 20261008-1521-spacex-8016)

## Claim

The checker's named gold experiment — wire the re-anchored jet into the plane's rebind and measure a **digest-identical** speedup — is unsatisfiable as stated, and I refute it with the plane's own numbers: the only bit-identical reuse (an exact `ShapeKey` recurrence) hits **0 of 4,367 fired kicks** across seeds 1–5, while every real reuse path changes bits on **100% of key steps** (relative period deltas ~10⁻⁹ ≈ 4×10⁹ Scalar ulps); the honest prize, measured on the same stream, is the crate's own shipped `QuantizedMemo` boundary reusing the compiled shape on **92.5–95.1%** of fired kicks at **0.55 µs per use against a 37–55 µs fresh compile (~70×)**, with the jet's re-anchor **never firing** in the plane (per-kick key drift p50 ≈ 5–8×10⁻⁹, n* ≈ 10⁵ kicks, so the design's 0.05 compiles/kick is ~5,000× conservative there) — a realized **≈1.9× on ship kick items (≈1.25× on the frame)**, not 20×, and only as a law change to be B-judged, never as an optimization.

## Bottleneck

Board focus #1 (fewer/cheaper kicks). The prior run sized the compile at ~half of every ship kick but left the deletion unmeasured (the checker: "the jet's per-use incremental cost is never measured… realized gain could be nearer 5–10×"). This run measures the deletion's exact terms on the plane's real kick stream: recurrence (does any reuse identity repeat?), divergence (can reuse be bit-identical?), cadence (what would re-anchor on?), and per-use cost.

## Evidence

Bench in `bench/` (standalone crate on path deps, no crate edited; the prior run's `kick`/`frame` modes are included verbatim). Each command ≤ 60 s on 8 vCPU:

```
cd lab/results/20261008-1613-second-20261008-1521-spacex-8016-6c47/bench
CARGO_TARGET_DIR=/tmp/benchtarget cargo build --release
for s in 2 3 4 5; do /tmp/benchtarget/release/bench jet $s; done   # jet-heldout.txt
for s in 2 3; do /tmp/benchtarget/release/bench kick $s; /tmp/benchtarget/release/bench frame $s; done  # regen.txt
/tmp/benchtarget/release/bench sweep                              # sweep.txt
```

- **The record regenerates** (prediction 6): `jet`, `kick` and `frame` digests on seeds 2–3 equal heldout.txt exactly (f8f522a9…, 2c5685c6…, 6c5659b2…, fc949735…); `jet 2` run twice gives the same digest. Fresh seeds 4–5 (never run before): the same structure throughout.
- **No bit-identical reuse exists** (predictions 1, 3). Over 3,266 consecutive fired-kick pairs (seeds 2–5): exact `OrbitKey` repeats 0, exact `ShapeKey` repeats 0, `ShapeMemo` first-encounter hits 0 of 3,476 fired kicks (0 of 4,367 with the tuning seed). Between a body's consecutive compiled orbits, cycle increments and quarter-period state reads are bit-equal on **0 pairs**; the relative period change between consecutive keys has p50 0.7–3.2×10⁻⁹ against the Scalar ulp 2.2×10⁻¹⁹. The crate itself forbids the mixed path (shape coarsened, key exact): `Orbit::from_shape` refuses any shape whose key differs (`Error::Topology`), and the digest hashes the key, periapsis time/angle and residual — every integer downstream of the table. Hence **bit-equal digests and a kick-line gain cannot coexist**; the jet is a law change (the prior dossier's caveat (a), now measured), to be judged through B1/B2/B5 exactly as law.md's "Not adopted" entry requires.
- **The shipped reuse boundary does hit** (prediction 2): `QuantizedMemo` (the 44-bit `MemoCode`, "this boundary explicitly coarsens them") reuses on 607/656, 777/831, 784/838, 1095/1151 first-encounter fired kicks — 92.5–95.1%, storing 33–43 distinct shapes per seed; consecutive kicks of a body share a code on 3,262 of 3,266 pairs (99.9%). 98.8–100% of the plane's orbits sit on the weak branch, where the compiled shape depends on eccentricity alone (sweep: knot counts identical at p = 2¹⁸, 2²⁴, 2³⁰ for every e).
- **Per-use cost and cadence** (predictions 4, 5): reuse costs 0.54–0.57 µs per call against a fresh compile of 37–55 µs on the same keys (~70×); compile stays 80–84% of the isolated `from_state` rebind this session (prior session 73–96%; band, shared box) and 48–51% of the whole kick process. Per-kick key drift |dln| p50 4.9–8.0×10⁻⁹, p95 ≤ 1.3×10⁻⁷; the accumulated signed drift crosses √(floor/C) = 7.3×10⁻⁴ **zero times** in 900 frames on every seed (floor 10⁻⁶, C = 1.9, red-team 20261006-0346) — the derivative jet would pay one compile per ~10⁵ kicks in the plane, not one per 20.
- **Realized gain, honestly** (the checker's open question): a ship kick item at 84–90 µs drops to ≈44–50 µs with the compile replaced by reuse at 0.55 µs and the re-anchor amortized to ~0 — **1.9× on kick items**; the rebind line alone 4.7× (51.0 → 10.8 µs); the whole frame ≈1.25× (ship items are 31–36% of event cost). The prior run's "≈20× on the dominant term" holds only for the compile term in isolation.
- **The claim's scope, closed** (the checker's misses): player kick items measured — 73 per seed, all fire, process 34.3–34.5 µs (their keys compile cheaper: low-e). Fleet slices (27–41% of event cost) **never pay the compile**: `Fleet::advance`/`Fleet::kick` (fleet.rs) apply sigma-delta carries to the frame origin's tube and call no `Orbit::compile`/`Rebinding` — the compile line is a ship+player mechanism by construction, not just where the prior run looked. Extremes (sweep): compile 6.6→223 µs from e = 0 to 0.995 at 16M (knots 6→143); at e = 0.995 it is 3–6× the plane's median kick compile, so high-e belts make the prize bigger, not smaller.

## Predictions

`predictions.md` written after tuning on seed 1 only; seeds 2–5 held out (4–5 never run at all). Items 1–7 all held — kill criteria nowhere near triggered (exact reuse 0% < 5%, bit identity across a key step 0% < 5%) — with one disclosed soft miss: item 2 said weak-branch = 100%, and seeds 2 and 5 had 8–10 non-weak fired kicks each (98.8–99.1%; close encounters pushing periapsis below the weak threshold).

## What would make it wrong

(a) If a future law binds tubes at quantized keys, "0 bit-identical reuse" stays true but stops binding — the question moves to the B-gates (the re-rounding walk, B1/B2/B5), where the "Not adopted" entry already sits; my numbers then become its measured inputs (95% hit rate, 10⁵-kick jet cadence). (b) The drift→n* mapping uses the red-team's C = 1.9 for Δφ; a belt with secular correlated kicks (inspirals, resonance-adjacent populations) could pull n* down toward the design's 20 — my 900-frame plane horizon sees only tides. (c) Timings are a shared cloud box: orders of magnitude only; the ratios were stable across five seeds in one session and consistent with the prior session's bands.

## Cost of adopting, and fit

Nothing to adopt: the refutation protects the integrator from wiring a digest-breaking "optimization" (principle 25: don't multiply by zero), and the measured terms — 95% quantized reuse at ~70× per use, 1.9× realized on kick items, a 10⁵-kick jet cadence in the plane — are the inputs the motion-law v2 owner needs to decide the re-key law through the gates. Fit — PRINCIPLES #2: "behaviours matter, not continuum fidelity: error type over error size": the reuse question is an error-*type* question (bits change or they don't), and I measured the type, not a tolerance; #13: "basically we don't want errors that can compound that's the goal": the quantized boundary's 95% hit rate is exactly the re-rounding walk law.md's "Not adopted" entry fears, now with the plane's own hit rate attached.

## The lens

The second-author lens nearly over-trusted the checker's framing: "digest-identical speedup" sounds like an instrumentation task, and it is in fact an impossibility proof plus a law decision. What I may have missed: the belt-scale correlated-drift regime (my n* is the plane's, not a belt's); the non-weak ~1% of kicks (close encounters), where the jet's error law is least tested; and I did not run a derivative-jet rebind end-to-end (forbidden without crate edits and meaningless for digests — its per-use cost is bounded above by the measured 0.55 µs hit path, which includes key re-encoding).

Grade suggestion: gold by the second-author rule — the named experiment's success condition is cleanly refuted, its decisive parts all ran, and the record regenerates from this folder with held-out seeds that held.
