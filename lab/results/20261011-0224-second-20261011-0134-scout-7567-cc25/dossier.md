# Dossier — 20261011-0224-second-20261011-0134-scout-7567-cc25 (lens: second author)

**Claim.** The scout's named gold experiment, run on the real harness, **refutes the composite
as specified**: on the real frozen B12 ships the derived-cap + 10×-horizon test does *not*
satisfy the B12 contract — every ratio clause false-fails `echo`, the oracle itself (median
max₁₀/max₁ ratio 2.23 at 10×, 11.4 at 40×, max err 1.4e-14 ≪ B12's 1e-12 floor), and
`bounded` (5.15 at 10×; the real a-diffusion saturates only at the law's AXIS_CLIP around
10×, not within the 1× window) — while the cap clause, degenerate for every kept ship to the
law's own reading clip (CAP = TOL_B·(10−a₀)/(R_H/sep) ≈ 1.3e-5, because all 16 level sets open
the planet's unbound channel; brute-force state sampling confirms), misses the compound walk at
any affordable horizon (3.1e-6 at 10×, 4.4e-6 at 40×). The scout's *negative* half is
confirmed on the real laws: the shipped exponent cannot separate the must-pass control from the
must-fail fault — median growth exponents at 1× are **bounded 0.353 vs compound 0.416**
(ranges [−0.07, 1.47] and [−0.11, 1.65], 14 judged ships).

**Bottleneck.** B12's instrument (HANDOFF "Risks to attack first", the three in-flight
rebuilds). This closes the scout's branch with a measured verdict on the real harness: the
separation the composite sought does not exist at fixed statistics, because (i) the real
scene's a-diffusion does not saturate within the gate's horizon — the composite's hidden
premise — and (ii) even the conserving oracle's residual grows with horizon (sub-floor, but
ratio-measurable), so any horizon-ratio clause without B12's own 1e-12 floor rule false-flags
the perfect law. What survives for the rebuilds: cap-only + floor rule + the measured walk
growth (√encounters, 30.6 encounter-units at 10× on the wildest ship) sets the detection
horizon for the planted leak class at ~10⁴–10⁵ periods (100–1000× the gate's), not 10×.

**Evidence** (all from `harness/`, the shipped `xtask/src/behave/**`, `measure.rs`,
`gr_oracle*.rs` copied byte-identical — sha256 check in `run.log`; only `composite.rs` and
`main.rs` are new; real frozen ships via the real `handoff::kept()`, real laws through their
real `Law` impls; 1× maxima are an exact prefix of the same run — the checker's prefix demand
holds by construction):

| 10× horizon (2000 periods, 14 s, md5 `d6989c9e…`, rerun bit-identical) | median ratio | worst max err | verdict | contract |
|---|---|---|---|---|
| echo (must PASS) | **2.23** | 1.44e-14 | FAIL | **broken** |
| bounded (must PASS) | **5.15** | 1.32e-5 (=cap) | FAIL | **broken** |
| const (must PASS) | 1.00 | 3.0e-8 | PASS | ok |
| compound (must FAIL) | 2.024 | 3.06e-6 | FAIL | ok (margin 1.2 %) |
| drift (must FAIL) | 6.26 | 3.1e-9 | FAIL | ok |
| kick (must FAIL) | 4.34 | 9.7e-4 | FAIL | ok |

- Ratio clauses false-flag echo and bounded; compound's catch is razor-thin (2.024 vs 2.0) and
  seed-fragile like the leak panel. Leak panel 1e-8…1e-7 × 8 seed variants at 4e-8: all FAIL,
  but *spuriously* — they ride bounded's ratio; over-cap counts 0–2 ships of 14 with margins
  < 6 % (the checker's attack (a), now on the real scene).
- 40× horizon (8000 periods, 37 s): echo median ratio 11.4 (max 5.2e-13, still under the
  floor — the conserving oracle's residual grows with horizon; B12's floor rule protects it
  only to ≈ 10⁴ periods), bounded 6.9, compound 3.45, worst compound 4.41e-6 vs cap 1.3e-5.
- The cap derivation, done honestly from each ship's C_J zero-velocity curve (exact near-planet
  axis scan for the unbound channel + far-field grid + brute-force validation, 4000 states per
  ship): every kept ship's level set opens into the planet's deep lobe (all cross R_SOI ≥ 8
  times, closest 3.6–77 planet radii), so the accessible osculating-a band is [0, AXIS_CAP=10]
  and the cap loses all per-ship structure. The scout's synthetic closed band (±5 R_H/sep,
  cap 5e-7) does not exist on the real scene.
- Real a-diffusion rate (prediction 4 of the scout's dossier, now measured): the bounded error
  is a linear readout of a(t); max at 1× spans 1.0e-6–1.3e-5, at 10× seven ships sit exactly at
  the clip — saturation time ≈ 10× the gate's horizon, not within it.

**Commands** (from `harness/`, each ≤ 60 s): `cargo build --release`; `./harness 2000 1600 6`
(writes `composite-out.json`, the 10× record); `./harness 8000 800 6 1e-7:0` (40×);
`./harness 200 400 6` (1× probe). Outputs: `composite-out-10x.json` (frozen), plus per-run
`composite-out.json`.

**Predictions** (`predictions.md`, written before the 10× run): held — bounded false-fails
with median ratio in [2, 10] (measured 5.15, mechanism exactly as predicted: the trace's
a-range grows until it touches the clip); compound FAIL via ratio ≈ √10 (2.024); drift FAIL
(6.26); kick FAIL; leak floor seed-fragile (0–2 ships over cap at 4e-8); the scout's floor
formula does not transfer (cap degenerate → detection rides the bounded component). Missed —
echo's ratio: I predicted 1.05–1.15 (white-noise window growth); measured 2.23 median
(per-ship 1.0–11.1): the conserving integrator's residual is *growing*, not white — the same
mechanism that false-flags bounded also reaches the oracle, one floor below. This strengthens
the refutation; had I checked it I would have predicted echo's failure too.

**What would make it wrong.** The composite could be rescued with three amendments (floor rule
on the ratio, per-ship caps re-derived against a *requirement* clip rather than the law's own
AXIS_CAP, horizon 100–1000×) — that is a new design to be rung, not this one; my refutation is
of the composite as specified and of its 10× headline. Two machines: not covered — one Linux
x86 runner only (shared, load 1.8–1.9, i7-4790); the composite is reference-free so the
echo-on-Linux failure mode does not apply, but the numbers are order-of-magnitude. The `const`
and `leak` controls are my constructions on the real echo states (copied `lay`/`star_axis`
machinery), not shipped laws; the checker asked for "scaled" — if that meant a different law,
this gap stands. Judged subset 14/16 (2 excluded: reference inside the planet / unconverged),
matching the gate's own exclusion accounting.

**Fit with PRINCIPLES.** "A test that cannot fail is a control" — the composite failed its own
positive control on the real harness, which is exactly what the gold experiment was for.
"A failed expectation is not automatically a failed method" (H0183): the cap-only + floor
re-derivation is the surviving configuration, with the detection horizon now measured rather
than assumed. "Error type over error size": the separation bounded-vs-compound remains open
on the real scene — the exponents 0.353 vs 0.416 are the same type to every growth statistic.

**The lens.** The second author ran the named experiment, not a design search: I did not build
or rung the amended composite (floor rule + requirement clip + 100–1000× horizon), so "the
claim, amended, holds" is untested; only "the claim, as specified, is refuted on the real
harness; the negative half is confirmed on the real laws" is measured. The checker's two-machine
clause and the cap-coefficient-as-requirement question stay open for the integrator.
