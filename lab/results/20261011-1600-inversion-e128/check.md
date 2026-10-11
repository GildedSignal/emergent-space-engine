# Check — 20261011-1600-inversion-e128

Grade: gold

## Abstract for the integrator

The merge's green test (level-15 burn reaches β 0.999, no refusal; `plane.rs:237`) sits inside a broken, ungated regime: the tube's proper time — the clock the player's page reads (`view.rs:262`) and the burn flushes against (`step.rs:312`) — saturates at dt/dτ = 2, so a held burn reaches γ its own coordinate time cannot afford (3.7× wrong at the test's own green point, 112× at the freeze); the frozen 3% work gate is unpassable above β 0.247; and the flight dies at γ 1761 in `Space(Range)` — the orbit-key range check (`orbit.rs:48`) during the kick's rebind, 137× short of the leave. Both commands reproduced **byte-identically**; every headline number regenerated. My own level-12 run reproduces collapse and wall independently (deficit 112 at freeze, γ_wall 1791, same fault). Cost to adopt: none — re-aim `b-high-gamma` at the time map before raising the wall.

## Reproduction

- Clean tree at `a838a284`, applied `work/patch.diff` (one new example, edits nothing else). Both dossier commands rerun: the CSVs are **bit-for-bit identical** to `work/l15b.csv` and `work/l5.csv` (`diff` empty), including the fault `Some((Kick(0), Space(Range)))` and loss at t = 17035876708.
- Independently recomputed from my own CSVs, not the author's analysis: deficit γ/γ_ext = 3.72 at the green point (β 0.999177, γ 24.65), 87.3 at γ 1262, 111.7 at freeze (γ 1761.4); local dt/dτ tail = 1.96, 1.96, 2.00; work gate crosses the frozen 3% bound at **β 0.2474, ratio 1.0303** (with the true t = 0 baseline; the start state in the log gives e₀ ≈ −8e−10), 27.2× off at the last healthy checkpoint; relativistic work vs ΔE∞ = 2.35%; pt_exp = −64 throughout, pt → −0.5 (2⁻⁶⁴ units) within 7e−10, max constraint violation 6.4e−11; lag < 2^24 and steps 2^18→2^22 while healthy. γ_pred matches to 3.8e−3 worst (author said ≤ 3e−3 — a nit, see below).
- The clock really is the one claimed: `view.rs:262–267` builds the player's `proper_seconds` from `rec.proper + orbit_state.proper_time` (the probe's exact formula); `step.rs:311–314` flushes the same ("the tube's length since the last binding is the body's clock reading"); the burn is exact in this τ (P2), so the engine and the view agree on a clock that is wrong above γ ≈ 2.

## Predictions

`predictions.md` is substantive and pre-registered (its P1 shape — γ³ — is provably wrong against the data, which is itself evidence it preceded the run; mtimes: predictions.md and the first decisive `l15.csv` share a minute, `l15b.csv` 8 min later). Outcome as reported: P2 held (3.8e−3, not the stated 3e−3 ceiling), P4 held exactly, P5 held, P1's conclusion held with the shape honestly corrected to the saturating Newtonian energy, P3 wrong — and the wrongness is the finding (the compile refuses 137× short of the leave; the wall was never the register or the word). Honest reporting throughout.

## Attack (my own cases)

1. **Level 12** (in-domain, α = 2⁻³²): the collapse reproduces independently — dt/dτ → 2.000, deficit 111.7 at freeze, γ_pred err 3.8e−3, max viol 1.8e−11, register saturates at −c²/2 in its own doll's units (pt_exp −66), same fault `Space(Range)` at γ_wall 1791.4. Not a level-15 or one-seed artifact; the wall is level-independent to 1.7%.
2. **Level 20** (out of domain): the engine's rapidity rate silently saturates at level 15's α (readout γ follows cosh(2⁻²⁹τ); the throttle's top is 15, matching the register's "0.35 g to 10⁴ g") — so the probe's γ_pred/γ_ext/work columns are wrong for levels > 15 while its engine columns stay valid (same wall γ 1761.4, same fault). The author never probed an out-of-domain level; the probe should assert level ≤ 15.
3. **Gate baseline**: with the naive baseline (energy at the first checkpoint, not t = 0) the crossing spuriously reads β 0.037 — with the correct t = 0 baseline it is exactly the dossier's β 0.2474 / 1.0303. The dossier's number is the honest one.

## Novelty

`docs/HANDOFF.md:73` lists "flying past γ ≈ 2,000 is refused" as a known limit **with no cause**; no HISTORY entry documents the dilation saturation or names the refusing check. The nearest entries are the register merge itself (the H-entry at HISTORY ~line 3171: "an integer energy register… the register is Kepler's, not the geodesic's") — a different defect (register semantics, not the tube's time map). The compile-side shape checks out in source: `orbit.rs:604–608` gives the tube's proper time as a closed form ∝ t·√(1−3q) under the compile's envelope (`u_p < 1/3`, else Range; lib.rs), and `orbit.rs:48` is the orbit-key Range check the freeze faults on — consistent with the author's flagged [INFERENCE] (a saturating weak-field energy map), now grounded though not fully derived.

## Goal fit

PRINCIPLES 30: "I want the player to feel what a human would feel in space, it's about immersion" — the one instrument of that feeling at high c is the clock, and it saturates at ×2. Principle 2: "error type over error size" — a silent saturation is the worst type. Principle 34: "the oracles are guards, not shepherds" — the work gate guards only β < 0.25 and the merge's no-refusal test guarded nothing above it. The finding kills the premise of a just-merged green test, deletes the belief that the register or the word is the wall, and re-aims the queued `b-high-gamma` build — adoptable within one step (build order, not code). This is the same shape as the 6 October gold: a measurement that breaks a live premise.

## What the author missed

- The L5 control's "< 1e−6" is not regenerable from the artifacts: at level 5 both work and ΔE print as 0.000 in the CSV and stderr (below the printed precision), so the claim rests on unwritten digits — the taste-log failure mode ("numbers the shipped code cannot regenerate"), here on a control rather than the finding.
- The probe assumes α = 2^(thrust_log2+level) for any level and does not assert level ≤ 15; for level 20 its γ_pred/γ_ext columns are silently wrong (mine, above).
- Minor overstatements: γ_pred "≤ 3e−3" (measured 3.8e−3 at one checkpoint); pt "= −2⁶³ exactly" (it is −2⁶³ + 2.98e9, the β < 1 limit).
- Untested, as the author concedes: reverse burns, turn keys at high γ, and the `seen` shifts/Doppler (which read retarded states and could mask or double the wrongness the player perceives). The exact algebra of the 2.0 asymptote (√(1−3q) → 1/2, i.e. which q saturates at 1/4) is left to whoever fixes `crates/space`.
