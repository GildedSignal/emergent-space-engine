# Dossier — 20261007-1106-second-20261007-1032-taleb-ab03-0263

**Claim.** The checker's named experiment, run to a decision: the secular-shadow twin (same
birth states under the Giant's exact double-averaged field, same integrator/windows/floors)
**refutes "program absorbs" for the belt** — it explains none of the belt's mean-element drift
(residual 108.71 of the 108.77 frozen bits at 20 yr; variance explained 0.000–0.005 on every
column; the twin's own averaged response is ~66× smaller in E-amplitude). The drift is not
synodic-window machinery (E bits 36.1→36.0 under synodic windows), not chaos (clone divergence
7.8 bits at 20 yr for a u32 birth-quantum, order-1 amplification; the da-clone is exactly the
birth offset, flat in t), not absorbable by cheap phase programs ((a, resonant-angle) bins
12.0% vs 12.9% permuted null; (a, synodic) 15.2%), and **bounded**: median |ma−a0| saturates at
1.8×10⁻³ AU by 40 yr (E-bits p50 36.33 at 40 and at 60 yr; per-body structure persists,
corr 0.85 between 20 and 40 yr). So the belt's ~100-bit staleness at ≥5 yr is a per-body
resonant/synodic envelope of the full field: deterministic machinery re-derivable from the
birth program (smooth map, ~8 extra bits of evaluation precision), carried in the engine by
the law's phase-resolving kick layer — not by a secular program in the store, and not as
growing per-body information.

**Bottleneck.** Board focus item "fitting 10⁹ in 8 GB … decided by distinctions created per
game-second (H_live)". Gain: the 8 GB decision's worst reading ("belt needs a secular program
per body") is killed, and the cost is relocated from storage to kick-layer cadence — the belt's
H_live is bounded machinery, so the memory question reverts to what the law's kick phase state
already costs (q-cadence), while B18b's uniform churn stays dead.

**Evidence.** Scene, integrator, floors, windows identical to the shipped run (regenerated
bit-for-bit: every `frozen` row of `twin.json` equals the shipped `hlive2.json` to <1e-9;
`hlive_probe2.py` rerun in this folder reproduces all rows, only load/mem/wall differ).
- **(A) The twin** (`twin.py` → `twin.json`, 173 s): ring field = exact time-average of the
  Giant's acceleration over uniform mean longitude, 256-node trapezoid on a 1080×2048 bilinear
  table, kicks applied to secular-domain bodies (Q0 = a0(1+e0) < 4.64; 65,522 of 65,536 — only
  14 belt bodies cross the Giant's annulus; belt hyper = 0, the shipped 94 are crossers).
  Noise controls: dt/2 gives E 25.2 / w 14.2 bits (the binding numerics), 128-node quadrature
  0.16 bits (converged). Variance explained is noise-robust (the twin's signal variance is
  ~4×10⁻³ of the full drift's, so even a perfect twin could explain ≤0.03%).
- **(B) Synodic window** (same run): E+L bits do not collapse (36.1/23.6 → 36.0/23.4).
- **(C) Clones** (8,192 bodies, full field): dλ0 = 2π/2³² → total divergence 6.8/7.4/7.8 bits
  at 1/5/20 yr (E column carries it; slow growth, no exponential); da0 = 1e-9 AU → 15.5 bits
  flat at all t = the trivial birth offset itself, zero dynamical amplification.
- **(D, E) Follow-ups** (`followup.py` → `followup.json`, 12 s; post-hoc diagnostics, chosen
  after seeing A/B): 60-yr subset run — median |ma−a0| 1.05→1.59→1.78→1.76×10⁻³ AU at 5/20/40/60
  yr (saturated; rms grows 0.026→0.057 AU only through the encounter tail); resonance-angle
  binning (nearest p:q, q≤8, 98.9% assigned) absorbs 12.0% against a 12.9% permuted null.
- Reproduce: `python3 hlive_probe2.py` (22 s), `python3 twin.py` (173 s),
  `python3 followup.py` (12 s), in this folder.

**Predictions** (`predictions.md`, written before the decisive run). Held: regeneration
(bit-exact); belt hyper = 0; twin-noise ceilings (E 25.2 vs predicted ≤18 — close); clones
smooth, no chaos (≤12 bits, linear growth); crossing minority small (14 vs predicted 150–350 —
overestimated by ~20×). **Falsified, and reported:** the twin was predicted to absorb the
w/M columns with variance explained >0.9 (measured ≈0.00 — the belt's w/M drift is not the
averaged-field precession either); the synodic window was predicted to collapse E/L ≥5×
(measured: no collapse); the resonant minority was predicted 2× worse than proper (measured
+3 bits — the envelope is belt-wide, not concentrated on the 4 strong resonances). The kill
criteria fired: absorption is refuted on the w/M columns, so I report the refutation, not the
absorption.

**What would make it wrong.** (1) The twin's averaged field is exact only to the quadrature
and table resolution claimed; the variance-explained verdict is insensitive to this (see
noise-robustness above), but the twin's own small drift (30.7-bit E signal over a 25.2-bit
noise) is not resolved — nothing in the claim leans on it. (2) 60 yr bounds the envelope on
this seed only; small-denominator libration periods can exceed it for sub-populations (the
median saturates, the rms does not — the tail is the encounter regime, a different tier).
(3) rtf: at rtf ≈ 10⁴ one play-hour ≈ 1.1 yr and the 5-yr rows apply within the first hours.
(4) Test particles: belt-belt coupling excluded (r8's 427/1.7M; the checker's own note).
Cost of adopting: none in code; the design consequence is B18b's churn model stays dead and
the belt's store question moves to kick-layer cadence.

**Corrections to the shipped record** (the checker's warts, confirmed here): the 1-play-hour
row is void (coverage 0.003 — the mean element does not exist yet; it does not "measure ≈ 0");
`control_mu0_scarred` was hardcoded in the shipped script (in `twin.py` the floors are computed
from the measured μ=0 control, which scars 0 bodies); belt orbit is 248–574 play-hours and the
synodic period 334–1,421 (not 350–580/440–1,400); with ef = 2 bits of index overhead at 100%
scarred, the frozen program is strictly worse than 144-bit individuals after ~1 window — that
statement now cuts deeper: the 100 bits are machinery, so *individuals* are not needed either;
a birth program plus phase-resolving re-evaluation dominates both.

**Fit with PRINCIPLES.** "Nothing is evolved that can be derived" (P3): the envelope is derived
from the birth state and the shared ephemeris, so storing it as scars was never required — but
the derivation is per-body phase-resolving, which is exactly "the simulation tells us what's
next" (P22), not a secular shortcut; "a test that cannot fail is a control" (P10): my
predictions failed where they should have, and the map is drawn from the failures; "rough
first" (P21): the twin's noise floor bounds only its own small signal, not the verdict.

**The lens.** Taleb's lens again over-called the mean's fragility and under-called the
mechanism's reach: the tail is real but lives in the encounter minority, and the belt's
"damage" is a bounded, deterministic envelope — Mediocristan machinery in Extremistan
clothing. The second-author blind spot I watched for was defending the original synodic-angle
mechanism; the data killed it a second time (12% vs 13% null), and I let it die.
