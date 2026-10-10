# Dossier — 20261010-2052-inversion-9a33 (inversion lens)

**Claim (one sentence).** The co-orbital phase-neighbour certificate (gold
`20261006-0346-taleb-09b5`, adopted; build `b-coorbital-cert` in flight) silently
assumes a zero-spread formation: with any element spread at all — a burn footprint
of r8 v4's own magnitudes — spatially concentrated fleets put 85–99% of real
encounters at partner rank ≫ 4 in the along-orbit sort (rank follows
k ≈ 6σ_e·n/Δφ, so rank 4 needs e below one phase spacing), and a two-group
intercept puts every war event near rank n/2, while the fleet still looks
maximally concentrated to any spatial trigger.

**Bottleneck.** "Candidate work at scale" (the board's first risk; HANDOFF "Risks
to attack first"). The gold replaced the quadratic tier for concentrated
workloads on the premise "every real encounter lies within partner rank 4 along
the orbit" — an O(n·k) tier with zero misses. If that premise's domain is only
the measure-zero zero-spread formation, the certificate as specified (rank 4,
concentration trigger) silently misses contacts in every post-burn fleet — the
very failure class (dropped contacts) that killed the window tier. This run
bounds the domain before the build lands.

**Method (independent of any tier).** Coplanar Kepler fleets, a = 1, GM = 1,
encounter radius ρ = 1e-4 (r8 v4's conservative end). Truth = brute-force closest
approaches: every pair ever within thr = ρ + v_rel·Δt/2 + margin of a coarse
sample is a candidate; every coarse local minimum is refined by golden section to
~1e-8 in time; an encounter is a distinct local minimum below ρ. No conjunction
logic, no candidate tier, no element sort. Ranks are measured in mean longitude
(the frozen along-orbit order; same rate for all bodies) and, as a diagnostic, in
instantaneous true azimuth, both centred on the largest circular gap. Worst
relative speed is checked against the margin in every run (`vrel_max_seen` in the
JSONs).

**Scenes.**
- **A (control, the gold's premise):** n = 800, circular, zero element spread,
  uniform mean longitude over 0.2 rad (spacing 2.5e-4 ≥ 2ρ).
- **B1e-3 / B3e-3 / B1e-2 (post-burn fleet):** scene A plus σ_a/a = 1e-4 (r8
  v4's kick scale) and σ_e = 1e-3 / 3e-3 / 1e-2 (r8 v4's steady σ_e), random
  apsidal orientation per body — i.e. the fleet every real burn leaves behind.
- **C (intercept):** 400 + 400 ships, e = 0.05, apsides anti-aligned, tight mean
  longitude clumps (σ_λ = 8e-3) timed to co-arrive at an orbit crossing — a
  designed intercept; spatially denser than scene A.

**Evidence** (`probe.py`, `probe-*.json`; commands at the end):

| scene | n | encounters | miss @ k=4 (mean-longitude) | max rank | miss @ k=4 (azimuth) |
|---|---|---|---|---|---|
| A control (gold's premise) | 800 | 316 | 0.0% | 4 | 0% |
| B σ_e = 1e-3 | 800 | 587 | **84.7%** | 31 | 0% |
| B σ_e = 3e-3 | 800 | 339 | **97.1%** | 94 | 0% |
| B σ_e = 1e-2 | 800 | 149 | **99.3%** | 226 | 0% |
| C intercept | 800 | 1174 (30 cross-fleet) | 3.5% total; **100% of cross-fleet** | 413 (cross); 5 (within) | 0.94% |

Reading of the numbers:
- The control is exact: the gold's scene reproduces (316 contacts ≈ the analytic
  320, max rank 4, zero misses). The premise scene is real — the gold is not
  wrong, it is domain-limited.
- One burn footprint (σ_a/a = 1e-4, σ_e = 1e-3 — r8 v4's own magnitudes) turns
  "zero misses" into 85% misses. The encounter population becomes dominated by
  apsidal-crossing pairs: ships that meet at an orbit crossing while their mean
  longitudes differ by up to ~2(e_i + e_j), i.e. rank ≈ 2(e_i+e_j)/spacing.
- The needed width follows the derived law: k_needed ≈ 6σ_e·n/Δφ predicts
  23 / 68 / 228 for the three B scenes against measured 31 / 94 / 226. Rank 4
  requires e below one phase spacing (here 2.5e-4) — a measure-zero formation.
- The certificate degenerates toward the quadratic tier as spread grows:
  k_needed/n ≈ 6σ_e/Δφ reaches 1/2 at σ_e ≈ Δφ/12; beyond that the O(n·k) tier
  *is* the O(n²) tier it was meant to replace.
- Scene C: each fleet alone is a valid formation (within-group max rank 5,
  0.96% miss), yet every cross-fleet event — the war events, the reason
  encounters exist in a game — is at rank ≈ n/2. C is spatially as dense as A
  (`clump_rms_radius` 0.058 both; a belt of the same n is ~0.7): any spatial
  concentration trigger fires, and the miss is silent.
- The azimuth sort misses ~0 everywhere, as predicted: at the encounter instant
  partners share an azimuth by definition. The break is specifically the frozen
  along-orbit order; an azimuth order is a different certificate that pays churn
  (Kepler shear re-sorts it, ~e·n rank exchanges per orbit), not the frozen one.

Commands (one shared-runner core; timings: A 7 s, B1e-3 65 s, B3e-3 60 s,
B1e-2 75 s, C 90 s):
`cd lab/results/20261010-2052-inversion-9a33 && python3 probe.py A` (then
`B1e-3`, `B3e-3`, `B1e-2`, `C`). Dependencies: numpy, scipy. The JSONs are saved
beside this dossier.

**Predictions.** See `predictions.md`, written before the decisive runs. Verdicts:
the control held exactly (max rank 4, 316 ≈ 320 analytic contacts); the mechanism,
the scaling law k ≈ 6σ_e·n/Δφ (23/68/228 predicted vs 31/94/226 measured), the
intercept (cross rank ≈ n/2, 100% miss) and the azimuth-sort catch-all (0% miss)
all held. One magnitude missed, reported as missed: I predicted the σ_e = 1e-3
miss fraction at "roughly half"; it is 85%, because the rank-near contact class
is far sparser than I estimated (radial offsets from δa and δe veto most
same-phase pairs). The pre-registered bound was conservative in the finding's
favour — the truth is worse for the certificate than predicted.

**What would make it wrong.** The trigger ("a dimensionless concentration
number") is not public: it lives on the gold run's branch. If it is an
orbit-space trigger (a Binet-cone cluster in (U, V, W), which separates
anti-aligned groups), scenes B and C fall outside the certificate's declared
domain and the miss is not silent — the fallback tier runs and pays the measured
quadratic cost instead. That weaker claim is still a result: the build brief's
tests ("the gold run's scenes and a dense ring") contain no spread scene, so the
domain boundary would otherwise ship unmeasured. My scenes keep the fleet a
tight spatial clump (`clump_rms_radius` in every JSON), so any spatial or
position-plus-speed trigger fires. Second caveat: n = 800–1600, one orbit, one
seed per scene, coplanar; the scaling law and the C scene's geometry are derived
and measured to agree, but the rung-scale confirmation (r8 v4's own sampler and
dip quantum, N ≥ 10⁴, many seeds, inclined fleets) is the named next experiment.

**Cost of adopting the finding.** Small and design-level, before the build lands:
(i) the certificate width must scale, k ≈ 6σ_e·n/Δφ, not k = 4; (ii) the trigger
must be measured in orbit space ((U, V, W) of r8 v4), where a post-burn fleet is
one cluster but an intercept is two; (iii) two-group intercepts need a
cross-group term — the Binet cone already crosses such pairs geometrically.
No crate on main is touched by this probe.

**Fit with PRINCIPLES.** "A failed expectation is not automatically a failed
method" (H0183): the certificate is not killed — its domain is measured and its
width corrected. "Build the simplest falsifying test first": one script, no
engine. "Measure before claiming, and never strawman": the control reproduces
the gold's own scene exactly, and the spread magnitudes are r8 v4's, not mine.
"A test that cannot fail is a control": scene A is the control that passes;
B and C are the tests that fail the premise.

**The lens.** Inversion looks for what a success silently assumes; it may have
under-weighted the cheaper fix — if the concentration trigger were simply the
existing Binet-cone cluster test, most of this finding collapses into "the
trigger must not be spatial", one sentence instead of a probe. The lens also
flags its own incentive: a red-team profits from a kill, and the honest outcome
here is a boundary plus a corrected width, not a kill.
