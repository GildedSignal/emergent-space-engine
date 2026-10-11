# Dossier — 20261011-0134-scout-7567 (lens: scout)

**Claim.** No per-series statistic on the Jacobi-error trace can separate bounded from
compounding error on chaotic ships — the bounded control *is* a walk in observation space —
but a **derived-cap + horizon test** (law-only, oracle-free: extend the run 10×, require max
error to stay inside a cap derived from the C_J level set) satisfies the B12 contract on all
ten laws, where `growth_exponent`, Allan-deviation slope and Mann–Whitney rank panels each
false-flag the bounded control at the gate's own horizon.

**Bottleneck.** The instrument: B12 cannot tell bounded from compounding error on chaotic
ships (HANDOFF "Risks to attack first"), so the motion law v2's stability is judged by
probes, not a gate. This kills the "find the right series statistic" branch of the three
in-flight B12 rebuilds and hands them the separable design, which needs no reference at all.

**Evidence** (`python3 falsifier.py`, 18 s, < 100 MB; faithful port of the planted laws'
mathematics of `xtask/src/behave/laws.rs` onto B12's exact geometry of `handoff.rs`: 16
ships, 1601 samples, ~40 encounters, chaotic a-diffusion clipped by the level set; output in
`falsifier-out.json`):

| horizon 1× (the gate's) | exp | allan | rank panel | contract |
|---|---|---|---|---|
| bounded (must PASS) | 0.411 FAIL | 0.475 FAIL | z=13.9, 13/16 FAIL | PASS |
| leak 1% of compound rate | 0.415 FAIL | 0.477 FAIL | z=14.1, 13/16 FAIL | FAIL |

The bounded control and the 1 % leak are the *same process* to all three statistics
(walk-in-error ≈ state-only error riding chaotic diffusion of a). At 10× horizon, law-only
(no oracle; C_J is computed from the law's own states), derived cap = 1e-7 × (accessible
a-range on the C_J level set) = 5e-7:

| horizon 10×, cap + max-err ratio | max err | ratio | verdict |
|---|---|---|---|
| echo / const / bounded | 5.2e-13 / 3.0e-8 / 5.00e-7 (=cap) | 0.98 / 1.0 / 1.10 | PASS·PASS·PASS |
| compound / drift / kick | 4.1e-6 / — / 0.49 | 2.92 (√10) / 13.1 / 12.1 | FAIL·FAIL·FAIL |
| leak 1% / 0.1 % of compound rate | 5.40e-7 / — | 1.11 | FAIL (margin 2.9 %) / invisible |

Ten of ten contracts met at 10×. Detection floor, derived and measured: a leak is caught
when its accumulated error exceeds ~5 % of the cap; the floor scales as cap/√(encounters·H),
so each 100× horizon buys 10× sensitivity. Mechanism sources: Allan deviation (IEEE time
metrology; slopes white −1/2, walk +1/2, drift +1 — verified); rank efficiency ≥ 0.864 of
t-test (Hodges–Lehmann 1956 — verified); extreme-value bias of window maxima (the gate's own
comment: 0.1–0.3 "for a perfect law" — max of m bounded draws grows ~σ√(2 ln m)). The
analytic core: re-anchoring the law at a mid-run state reduces, inductively, to the same
one-level-down problem, so no replay trick separates either; boundedness is a **derived
bound, not a statistic**.

**Predictions** (`predictions.md`, written before the run): held — exp false-flags bounded
(0.411, predicted 0.3–0.6; red-team measured 0.49 on the real scene); Allan reads walk +1/2
for compound/kick/leaks and −0.0 for noise. Not held — Allan's saturation rescue (bounded
returns to ≤ 0 at 10×): it stays 0.48, the level-set box-crossing time exceeds any practical
horizon; the drift model reads +1/2, not +1. The winning composite (cap + ratio) was **not**
pre-registered; it is post-hoc relative to `predictions.md`, and the checker should weigh
that.

**What would make it wrong.** The synthetic a-diffusion is faithful in kind (it reproduces
the red-team's 0.49) but not in rate; a real scene whose a-diffusion saturates within one
horizon would make even the exponent pass, and one that exceeds the level-set cap would
break the cap's derivation. The real gate must derive the cap from each ship's C_J
(zero-velocity curves) — UNVERIFIED numerically here. The drift shape (DP rtol 1e-12) is
modeled, UNVERIFIED. Adoption cost: small — the composite reuses B12's frozen ships, drops
the expensive per-ship DP reference entirely (the oracle cost disappears), and adds a law-only
10× run; thresholds derive from the scene, none fitted. The named next experiment: run the
composite in `xtask`'s harness on the real frozen ships against echo, the five planted laws
and a leak at the stated floor, on two machines (it is reference-free, so the echo-on-Linux
failure mode cannot recur).

**Fit with PRINCIPLES.** "Gates judge a representation; they never size it: first derive the
representation native to the operations at stake" — the cap is derived from the scene's
physics, not fitted. "A test that cannot fail is a control" — controls on both sides pass and
fail as planted. "Error type over error size" — the verdict is walks-past-a-derived-bound, a
type. "Use idle time to compute ahead" — the 10× law-only horizon is exactly that, and floats
may explore while a threshold comparison decides.

**The lens.** The scout searched statistics and metrology; it may have missed a *dynamical*
separator (e.g. a resonance-kicked detector that reads encounter-phase correlation, the way
`plant_compound` steps at entries into 3 R_H), and it did not measure the real CR3BP ships —
the integrator-dependent claims (drift shape, saturation time) rest on models, and a checker
with the real harness should treat them as leads, not facts.
