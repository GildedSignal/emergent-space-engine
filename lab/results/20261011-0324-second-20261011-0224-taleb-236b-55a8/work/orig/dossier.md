# Dossier — 20261011-0224-taleb-236b

**Claim.** The phase-neighbour certificate adopted on 6 October (gold taleb-09b5:
"every real encounter lies within partner rank 4 along the orbit") is valid only
for shear dispersion (Δa): in co-orbital families with e-vector dispersion — a
collision family, an interception, or any real fleet with ϖ spread — encounters
occur at fixed phase offsets set by orbit-crossing geometry, at rank ≈
n·ΔM*/extent (measured: 95–100% of contacts beyond rank 4, medians 0.24n–0.54n),
so a rank-k certificate silently drops nearly all contacts exactly where the
window tier it replaces is quadratic.

**Bottleneck.** Board's top scaling risk: "candidate pairs per body grow with N
… candidate work must track real encounters", and the queued build "the co-orbital
certificate" (GLM `lab/lenses/b-*.md`, Codex `queue-sol.txt`). This is the
pre-freeze falsifying probe for it (AGENTS: "Before any freeze, one GLM red-team
and the cheapest falsifying probe must have run"). Gain: it deletes a wrong
invariant before two lanes build it, and replaces it with the right one
(offset windows in the same phase ordering, O(n·k) preserved).

**Evidence** (exact two-body Kepler truth about one parent, GM=1, a0=1; contacts
< R in distance; rank = |index difference| in the fleet's mean-anomaly ordering
at contact time; seed 20261011; full data in `metrics-R*.json`):

| scenario | n | contacts | frac rank ≤ 4 | median rank | cone frac |
|---|---|---|---|---|---|
| S0 shear (σa=3e-4, e,ϖ pinned) | 500 | 659 | **1.000** | 1 | 0.00 |
| S1 collision family (same a, ϖ uniform, e 0.1) | 1600 | 80 | 0.025 | **869 (0.54n)** | 1.00 |
| S2 interception, cross-group only | 800 | 182 | **0.000** | 406 (band 399–413) | 1.00 |
| S4 realistic formation (σϖ=0.1 rad, σe=2e-3) | 300 | 871 | 0.033 | **71 (0.24n)** | 0.98 |

Mechanism (why): with dispersion orthogonal to phase, ΔM=0 is not a close
approach (same mean anomaly, different ϖ ⇒ separation ~ r·Δϖ; verified directly:
59 conjunction pairs in S4 all miss by 0.02–0.33). Encounters happen only where
the ellipses cross, and the two ships are there simultaneously only when their
mean-anomaly difference equals the geometry's fixed offset ΔM* — never rank-local.
In a clumped family the rank of that offset scales with n (spacing = extent/n),
so it worsens as fleets grow: at the design's 10⁶-ship formation scale, S4's
0.24n is rank ~2×10⁵.
Controls on both sides: S0 (the certificate's home regime) passes at 100%, and
the rank instrument's random-pair baseline (median ~n/6 < S1's 0.54n) rules out a
metric biased low. Sensitivity: R = 3e-5, 1e-4, 3e-4 (10×) leaves the structure
invariant (S1 medians 832/869/853; S2 cross medians 405.5/406/405; S0 ≥ 0.9993)
— the mechanism, not the threshold. Trigger: the family's intra-family Binet
cone fraction (U,V,W are the design's own coordinates) separates the regimes
exactly here: 0.00 (shear, rank-k valid) vs ~1 (offsets required).
Reproduce: `cd lab/results/20261011-0224-taleb-236b && python3 probe.py [R]`
(writes `metrics-R<R>.json`; 26 s at R=1e-4 on this 8-vCPU runner, < 300 MB).

**Predictions** (`predictions.md`, written before the full-size run; four
reduced-n smoke runs fixed scenario parameters and are disclosed there): P1
control ✓ (100%); P4 ✓ (3.3% ≤ 4, median 0.24n > 0.2n); P5 R-invariance ✓ all
three R; P6 trigger ✓ (cone fraction 0 vs ~1). Missed, held as held-out: P2's
"≤1% at rank ≤4" measured 2.5% (2 of 80) at R=1e-4 and its scaling band
[610,830] for S1's median measured 869 (+5%); P3's cross-median model (555,
uniform-density assumption) measured 406 — clumped fleets concentrate rank at
~n/2, and my within-fleet birth-stacking bound (≤60) measured 184. The claim
does not rest on the missed numbers: every crossing-regime measurement sits at
0–3.9% rank ≤ 4 across three R values.

**What would make it wrong.** If the shipped certificate's dimensionless trigger
routes crossing-dispersed families (cone fraction ≈ 1) to the pairwise window
tier instead of the phase certificate, the silent drop disappears — but then
those families pay the quadratic setup the certificate was adopted to remove
(taleb-09b5 measured ~40 TB of setup for a 10⁶-ship fleet), so the scaling risk
survives in cost form. My truth is unperturbed two-body Kepler (no_secular
exchange between members): real families precess and de-phase, which smears the
offset band over time but cannot move encounters to rank 0 — conjunctions stay
non-encounters while ϖ differs. Cost of adopting: none beyond the certificate
build itself — the fix is one generalization: maintain the phase ordering, check
partner windows at the family's crossing offsets {ΔM*(g)} (a small set, two per
crossing geometry) in addition to rank k; the trigger is already computable in
Binet space. Fit with PRINCIPLES: "A fix signals the wrong representation" (19)
— rank-in-phase was the wrong invariant; "under the right representation many
symmetries can appear" (32) — offsets are the same ordering, one more window;
"Gates are frozen before the first run" — this probe runs before the
certificate freezes.

**The lens** (Taleb): I looked for the concavity in a fresh adoption rather than
measuring speed again; the blind spot is that this lens prizes the falsifying
corner case and says nothing about how expensive the offset-window certificate
is to build or keep exact under precession — the next run should measure that
(the window count per body vs. element-change rate, the same steady-state test
as r8 v3). Also, all four scenarios share one harness (my Kepler truth, my rank
metric); the S0 control and the random-pair baseline are the only in-run
independence — the checker should re-derive at least one scenario with its own
propagator.
