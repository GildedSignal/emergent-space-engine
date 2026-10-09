# Dossier — 20261009-0208-second-20261008-2206-library-73ca-618f (second author on 20261008-2206-library-73ca)

**Claim.** The α-profile (decade-local growth exponents of the running max of |ΔC/C₀|) separates
bounded from compounding error **on B12's own scene** — the circular restricted three-body Jacobi
constant with doll-edge handoffs, median seed — with planted controls on both sides: bounded
plants read top-decade α = 0.00–0.01 (32/32 seeds), compounding plants read 0.94–1.22 (32/32),
against the frozen 0.2 threshold, while B12 v1's single-window slope false-kills 21/32 bounded
seeds — the checker's named experiment, done, and the claim held.

**Bottleneck.** Handoff "Risks to attack first" #3 and the board: B12 cannot tell bounded from
compounding error on chaotic ships; the silver run validated the α-profile only on an integrable
two-body energy series plus synthetics. This run moves the instrument onto the gate's scene, the
gap the checker named. Not an engine speed change: the gain is a gate that stops killing bounded
laws (measured false-positive rate 21/32 under v1, 0/32 under the α-profile on the same seeds)
and still convicts every compounding plant.

## Evidence (run folder; deterministic, RNG seed 20261009; every process < 200 MB)

Scene (frozen before the run, mirroring the repo's own conventions): CRTBP, μ = 2⁻¹⁰
(Jupiter-like, as `crates/universe/examples/jacobi.rs`), rotating frame, doll edge = sep/16
= 0.907 Hill (the engine's `2^(2·Δlog₂m/5)` rule, records.rs), horizon 10⁴ planet orbits,
dt = 2π/256, |ΔC/C₀| sampled per orbit, doll bookkeeping every step inside the doll
(doll-local coordinates and sources — the indirect term of law.md — rotation about the
barycenter in local form). Ships: retrograde irregular satellites, q ∈ [0.55, 0.75] Hill,
Q ∈ [0.95, 1.05] Hill, random orientation; 60 candidates, 21 survive 10⁴ orbits, 16 kept
(gate's replacement rule), 1.7×10⁴–7.0×10⁴ doll-edge crossings each under the bounded law —
the ≥ 20-crossing requirement is exceeded by ~10³×. **Measured scene fact for the gate's
builders:** a heliocentric co-orbital population (offsets 1.2–2.6 Hill, the first attempt) is
ejected entirely within 10³ orbits — the Wisdom chaotic zone — so at this μ and horizon the
crossing population that survives is the retrograde irregular one.

Laws (planted, from the requirement "errors never compound", not fitted):
`sym-fixed` (2nd-order symplectic split, fixed dt) and `sym-sched` (same, dt/4 until orbit
300 then dt — a bounded law with a representation-change transient) = bounded controls;
`sym-var` (same split, dt re-chosen from the state each step over a 2-Hill taper — the plane's
diagnosed failure mode, "the step re-chosen mid-encounter") and `rk4-fixed` = compounding
controls.

| law (plant) | median seed | final max | α per decade [10→10² … 10³→10⁴] | verdict (rule: α_top > 0.2) | B12 v1 window [1,10⁴] |
|---|---|---|---|---|---|
| sym-fixed (bounded) | 13 | 2.55e−5 | +0.00 +0.07 +0.02 **+0.00** | BOUNDED | +0.02 (agrees) |
| sym-sched (bounded+transient) | 0 | 2.50e−5 | +1.40 +0.39 +1.25 **+0.00** | BOUNDED | **+0.76 — false KILL** |
| sym-var (compounding) | 11 | 1.06e−3 | +0.00 +0.00 +0.92 **+0.98** | COMPOUND | +0.48 (agrees) |
| rk4-fixed (compounding) | 8 | 3.22e−4 | +0.86 +0.99 +1.00 **+1.05** | COMPOUND | +0.98 (agrees) |

Per-seed separation (the rule classifies every seed, not just the median): bounded plants
α_top ∈ [0.00, 0.01] over all 32 seeds; compounding plants α_top ∈ [0.94, 1.22] over all 32
usable seeds (one `sym-var` seed died near the horizon; its partial profile also reads
+0.29 +0.73 +1.22). Zero misclassifications. B12 v1's single-window slope exceeds 0.2 on
**21/32 bounded plant-seeds** (the orbit-300 transient and the early band-exploration decades
bleed into the fitted window) while convicting 32/32 compounding seeds — v1's error is one-sided
and the α-profile removes it by judging the settled top decade only, with the profile kept for
diagnosis. The profile shapes also carry the mechanism: sym-var reads α ≈ 0 for two decades
(walk hidden under the band) and emerges at +0.9…+1.0 — a single early window would acquit it;
rk4 reads ≈ +1 from decade 0 (linear systematic drift); sym-sched's transient is a spike in
decade 2 only. Levels: bounded plants stay ≤ 3.4e−5 (under the gate's 10⁻⁴ level criterion);
compounding plants end ≥ 1.4e−4 — on this scene type and level agree, but the rule needs only type.

Commands (deterministic; sequential ≈ 33 min, laws in parallel ≈ 16 min; not ≤ 60 s, disclosed —
the horizon buys the four decades the statistic needs):
```
python3 b12_scene.py select --candidates 60        # 6.5 min: seeds.json, series_sym-fixed.npz
python3 b12_scene.py law --lawname sym-var         # 9.9 min (parallel with the next two)
python3 b12_scene.py law --lawname rk4-fixed       # 9.6 min
python3 b12_scene.py law --lawname sym-sched       # 6.5 min
python3 b12_scene.py analyse                       # 1 s: b12_alpha.json (the table above)
```
Files: `seeds.json` (the 16 initial states), `series_*.npz` (per-orbit error series, ~1.2 MB
each), `b12_alpha.json` (per-seed profiles, medians, verdicts), `*.log` (the run transcripts).

## Predictions (predictions.md, written before the decisive run)

P1 held (sym-fixed median: α_top = 0.00 < 0.15, every decade d ≥ 1 < 0.2, final 2.55e−5 ∈
[10⁻⁶, 2×10⁻⁴]); P2 held (sym-var median α_top = 0.98 > 0.2; final 1.06e−3 = 42× the bounded
median, predicted ≥ 10×); P3 held (rk4 median α_top = 1.05 > 0.2); P4 held and was stronger
than predicted: B12 v1's window over [1,10³] reads +1.01 on the median seed and over the full
[1,10⁴] still reads +0.76 — both false-kill — while the α-profile acquits at α_top = 0.00.
The shakedown-informed priors were honest: the walk in sym-var was indeed slow to emerge
(α = 0.00 for two decades), which is precisely why the top-decade rule and the full profile,
not any early window, carry the decision. No kill criterion triggered.

## What would make it wrong; adoption cost; PRINCIPLES fit

- **Operating rule (state, do not hide):** conviction is safe, acquittal is horizon-limited —
  a transient must die one decade before the horizon to acquit; a delayed-onset leak convicts
  (the checker's adversarial case, reproduced there). The α-profile is a *type* instrument and
  **complements, never replaces, B12's level criterion** (10⁻⁴): a law must pass both.
  Smallest detectable leak on this scene: one that lifts the running max ≥ 10^0.2 ≈ 1.6× per
  top-decade decade above the band (the bounded plants' band creep, ≤ +0.07, is the noise);
  slower power-law leaks (α ≲ 0.1) remain invisible at any horizon — the instrument's floor,
  still open for `q-b12-design`'s leak control.
- What would break it: a scene where bounded laws' bands creep at α ∈ (0.1, 0.2) for decades
  (deep chaotic exploration), or a compounding mechanism that saturates below the band. Neither
  appeared here, but both are one experiment away on a different scene.
- Adoption cost: small — the statistic is a function over the error series B12 already samples;
  the rule is one derived threshold (the gate's own 0.2) on the top decade, median seed, with
  the 10⁻¹² float-noise floor kept. Hand to `q-b12-design`/`b12-v2`: the plants
  (`sym-fixed`, `sym-var`, `rk4-fixed`, `sym-sched`) are the both-sides controls, runnable in
  their harness from this folder.
- PRINCIPLES: *"Errors never compound… types of errors and not just errors"* (13) and
  *"error type over error size"* (2) — the α-profile is error type made measurable, now on the
  gate's own scene; *"A statistic is calibrated on a planted pair before it freezes"*
  (method.md #9, the B12 lesson) — done here, with controls on both sides.

**The lens's blind spot.** A second-author Taleb lens inherits the first run's framing and
tests the statistic it proposed; I did not run the rejected recurrence ratio on this scene, nor
any non-Taleb alternative. My doll handoff is exact by construction (a coordinate translation
with doll-local sources — rounding-level noise); the plane's real handoff is a tube rebinding
that can inject representation error larger than rounding, so the α-profile must be re-measured
on the plane itself once `b12-v2` lands — this run validates the statistic on the scene, not on
the engine. The scene's chaos is tide-driven (retrograde irregulars), milder than the co-orbital
layer that cannot survive; the strongest chaos in the record is under the compounding plants
themselves. And all of it is one machine, Linux/x86 float64 — margins (0.01 vs 0.94 around 0.2)
are too wide for platform noise to flip, but that is inference, not measurement.

**Grade sought:** gold for the named experiment — the claim now holds on the shipped record
(`b12_scene.py` + `seeds.json` + `series_*.npz` regenerate every number above) with the
checker's named experiment done and every prediction held.
