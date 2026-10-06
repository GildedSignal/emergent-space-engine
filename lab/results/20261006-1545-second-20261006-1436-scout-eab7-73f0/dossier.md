# Dossier — 20261006-1545-second-20261006-1436-scout-eab7-73f0 (second author on scout-eab7)

**Claim.** Driven by the checker's named experiment — the law's own kick stream at the plane's
cadence (32 kicks/orbit; orbit-averaged exterior tide + compiled 1PN precession = pure
differential apsidal rotation, the systematic shear the scout run's random walk understated) —
**the skin's mechanism is confirmed and its horizon confound resolved: setup cost tracks churn,
with the cut equal to the measured mean cache lifetime (42.5× at 0.057 rad/orbit, 15.1–19.4× at
0.19, and τ ≈ 2.2e3–1.1e5 epochs at real belt rates, where the skin never re-setups inside any
run) — but the scout's soundness claim is refuted at strong rotation: the shipped pairing
(slack 0.5, widen 2.0) misses 5 real encounters in 459 at 0.19 rad/orbit (rg = 1e-2, a ≈ 100 r_g)
on belt and tangential seeds, because pure rotation leaves the validity gate's timing term
identically zero while shifting eccentric pairs' crossing geometry by ~drift/(e/p), more than
ρ-scaled widening absorbs; a corrected pairing (widen 6, or slack 0.1) is sound there, and
over-widening (12) instead breaks the exact check itself (32 misses).**

**Bottleneck.** Board focus item 3 (encounters without work per orbit or per element change).
The checker's gold experiment verbatim: drive the arms with the law's own kick stream at
~32 kicks/orbit on belt and co-orbital/tangential scenes, show zero misses with
setups-per-kick cut ≥ 10×, and convert the horizon-limited 8× into a mechanism property
(mean cache lifetime). The setup is 92% of per-kick cost (components-4643); at the plane's
cadence the baseline pays it 32× per orbit.

**The stream (why it is the law's own).** Planar belt of test bodies around a dominant mass
with a circular coplanar exterior perturber (μ_p = 1e-3 at a_p = 5.2) plus the central 1PN
field: the double-averaged disturbing function is axisymmetric, so da = de = 0 exactly and each
body's apsidal line precesses at a rate fixed by its own (a, e):
ϖ̇ = 3n·rg/(a(1−e²)) + ϖ̇_tide, ϖ̇_tide from the Lagrange planetary equation on a numerically
double-averaged potential (deterministic 64×24 product grid; `lawskin validate`: tide =
1.05–1.07 × the analytic quadrupole (3/4)nμ_pα³ over e ∈ [0.001, 0.2]; sign set prograde per
secular theory). The kick is a pure function of (a, e): identical in both arms by construction.
a, e, period, tp never change, so the scout's validity gate reduces to its Binet term and each
body's Binet point rotates at radius e/p. Rate anchors (rad/orbit at a=1): tide-only 3.6e-5
(asteroid-belt-like), rg 1e-4 → 1.9e-3 (a ≈ 10⁴ r_g), rg 3e-3 → 5.7e-2 (a ≈ 670 r_g),
rg 1e-2 → 0.19 (a ≈ 100 r_g), rg 3e-2 → 0.57. One global kick every TAU/32.

**Evidence** (Linux x86, shared 8-vCPU box; orders of magnitude only; every arm ≤ 96 s and well
under 2 GB). Driver `lawskin/` (standalone crate on the repo's `crates/encounters`, untouched).
Arms share belt, stream, candidates and exact per-pair checks; only setup policy differs. Skin
slack 0.5, widen 2.0 exactly as the scout shipped. Misses/extras are TRUE multiset differences
(the scout's extras were a length difference; fixed). Full log `sweep-log.txt`; per-case outputs
in `scratch/<case>/`. Reproduce from this folder:

    cd lawskin && cargo build --release      # → /home/glmlab/lab-target-3/release/lawskin
    /home/glmlab/lab-target-3/release/lawskin validate
    ./sweep2.sh && ./sweep3.sh && ./sweep4.sh   # sweep.sh = the same matrix in one file
    /home/glmlab/lab-target-3/release/lawskin diag belt 120 0.1 0.01 0.01 4242 0.001 5.2 38 116 21.648

Main sweep (n 120, ρ 0.01; "cut" = baseline/skin setups per kick; τ = mean cache lifetime in
kick epochs = cache_hits/repairs; wall = baseline→skin seconds):

| case | scene, seed | rad/orbit | cut | τ | wall | misses |
|---|---|---|---|---|---|---|
| B0 | belt 4242 | 3.6e-5 (tide only) | 64.0 = horizon | 0 repairs (τ ≈ 1.1e5) | 46.0 → 1.5 | **0**/88 |
| B4 | belt 4242 | 1.9e-3 | 64.0 = horizon | 0 repairs (τ ≈ 2.2e3) | 45.0 → 1.5 | **0**/88 |
| B2 | belt 4242 | 5.7e-2 | **42.5** | **62.2** | 95.7 → 3.9 | **0**/189 |
| B1 | belt 4242 | 0.19 | 15.1 | 15.9 | 90.4 → 7.6 | **2**/159 — (38,116) t=21.648, (33,75) t=24.839 |
| B1b | belt 777 (held out) | 0.19 | 15.7 | 16.7 | 86.2 → 7.0 | **2**/150 |
| B3 | belt 4242 | 0.57 | 5.5 | 4.9 | 45.7 → 8.9 | **1**/84 |
| G1 | tang σ_e 0.02, 4242 | 0.19 | **37.7** | 52.1 | 71.0 → 2.6 | **0**/70 |
| G1b | tang, 777 (held out) | 0.19 | 40.7 | 58.3 | 69.8 → 2.4 | **1**/80 |
| G2 | tang 4242 | 0.57 | 13.7 | 16.2 | 35.8 → 3.0 | **0**/39 |
| O1 | coorb σ_e 0.05, 4242 | 0.19 | **19.4** | 26.3 | 55.8 → 3.6 | **0**/107 |
| O2 | coorb 4242 | 1.9e-3 | 64.0 = horizon | 0 repairs | 56.4 → 1.8 | **0**/106 |
| N1 | negative: belt, 0.19, **widen 0** | 14.2 | 16.9 | — | **7**/67 (detector sensitive) |

The mechanism property the horizon hid: τ = slack·eps_u·32/((e/p)·g_per-orbit) predicts every
measurement (B2 50–110 → 62.2; B1 15–35 → 15.9/16.7; G1 60–100 → 52.1/58.3; O1 20–40 → 26.3),
and at real rates it gives τ ≈ 2,200 epochs (rg 1e-4) and τ ≈ 1.1e5 (tide-only): **at the
belt's real drift the skin re-setups about once per 70 orbits of continuous shear — the setup
cost genuinely tracks churn, not kick epochs, and the cut at the plane's 32× cadence is the
lifetime, ≥ 10× wherever churn is measurable.** Skin run_evals = 1.89–1.92× baseline (B0
837,586→1,582,020; B1 1,747,305→3,325,419; B2 1,754,566→3,376,133): the widened-arc asymptote
the checker named; with setups 92% of baseline cost the skin wall is run-eval-bound (30× at
tide-only, 24.7× at 5.7e-2, 11.9× at 0.19). The B1 arm was rerun end-to-end (sweep3): every
counter and both miss times reproduce to 15 digits — the record regenerates from shipped code.

**The refutation, its mechanism, and the fix attribution.** Misses appear exactly where the
pre-registered kill criterion 1 said (rg ≤ 1e-2): 2/159 + 2/150 (belt, two seeds) + 1/80
(tang, held-out seed) at 0.19 rad/orbit, 1/84 at 0.57. `diag` on both B1 misses: well-crossing
eccentric pairs (e 0.19/0.22 and 0.09/0.15; |ΔU|−R ≈ −2.9 and −1.9 eps_u — not tangential),
large Δa. Under pure rotation the gate's timing term (tp/period drift) is identically zero —
the scout's walk re-timed tp every kick, so that gate was always exercised there and never
here — while the tolerated geometric drift slack·eps_u rotates the crossing longitude and
passage times by ~drift/(e/p) ≈ 0.1 rad ≈ 0.1 time units per lifetime, 5× the ±0.02 widening
on the thin Cross windows eccentric pairs get. The tangential scene (Wide/Full sections,
intrinsically wide) misses 10× less often; co-orbital Full sections are sound everywhere
tested. Post-hoc attribution arms against B1's truth (not pre-registered):

| arm | change | misses | τ | cut | run_evals |
|---|---|---|---|---|---|
| D1 | slack 0.5 → 0.1 | **0**/159 | 2.58 | 3.5× | 1.91× |
| D3 | widen 2 → 6 | **0**/159 | 15.9 | **15.1×** | 3.62× |
| D2 | widen 2 → 12 | **32**/159 | 15.9 | 15.1× | 5.89× |

Tightening slack 5× restores soundness but drops the cut below 10×; widening 3× restores
soundness at the full 15.1× cut (this is the geometry-scaled widening q-skin called for:
widen·ρ ≈ slack·eps_u/(e/p)); widening 6× makes it worse than baseline pairing — the widened
arcs dilute the exact check's minima-bracketing (found drops to 127/159), so widening has a
hard ceiling. At 0.57 rad/orbit no pairing reaches 10× (τ ≈ 5): churn-limited, the skin
degenerates to baseline-plus-validity (harmless: wall 8.9 vs 45.7 s).

**Predictions** (`predictions.md`, written before the sweep; only rg=0 4-epoch sizing pilots
preceded it). Held: B0, B4 (0 repairs, 0 misses, horizon cut), B2 (τ and 0/189), G1 (0/70, τ),
O1 (τ 20–40 → 26.3, 0 misses), O2, N1 (7 > 0, comparison sensitive), the τ formula everywhere,
the 1.9× run_eval asymptote, B3 as boundary. **Failed: B1, B1b, G1b soundness** — predicted 0
misses at rg = 1e-2, measured 2+2+1; that failure is the result. The D arms were not
pre-registered (attribution after the kill).

**What would make it wrong.** One law-shaped drift family (axisymmetric secular: pure
rotation, e and a frozen); streams that move e and a (inclined/Kozai/resonant belts, where the
law does not average) re-activate the tp gate and may fail differently. The candidate set is
frozen at epoch 0 in both arms (as in the scout run). One (μ_p, a_p); one field-strength
family. The miss diagnosis rests on `diag` of two pairs plus the tang/belt/coorb contrast, not
an exhaustive per-miss audit. Encounter volumes are 39–189 per arm, so the sound rows bound the
miss rate at ≲ 0.5% at these rates, they do not exclude it. τ constants are this belt's
(eps_u, e/p medians).

**Cost of adoption.** Take: (1) the mechanism is real at the plane's cadence — build the skin
with slack/widen sized from the law's own precession via τ = slack·eps_u·32/((e/p)·g);
(2) the shipped pairing (0.5, 2.0) is sound only for g ≲ 0.06 rad/orbit — near strong-field
dolls use geometry-scaled widening (widen·ρ ≈ slack·eps_u/(e/p), here ≈ 6) or a rotation-aware
validity term (bound accumulated per-body Δϖ against the snapshot: Δpassage ≈ Δϖ/n, ~4 flops,
in production an integer against the stored element version); (3) never widen past that scale:
the exact check's bracketing degrades. Not adopted here: the repaired gate is a new experiment
(a rotation-stressed rung at g = 0.19 judging misses and τ with widen 6 and the Δϖ gate).

**Fit with PRINCIPLES.** "Compute only surprises" (3): a steadily rotating orbit is not a
surprise; "the simulation decides, heuristics schedule" (22): the skin schedules, the exact
check decides; "A failed experiment kills that configuration, never the method" (9): the
pairing died at strong rotation, the mechanism was confirmed and its true number (τ) measured;
"Errors never compound" (13): the 6 misses are exactly the error type that must not ship;
"Rough first, refine when a certificate could break" (21): slack/widen now have a measured
soundness boundary instead of one tuned κ.

**The lens (what this second-author lens may have missed).** I kept the scout's gate
byte-identical to isolate its flaw, so the repaired gate (Δϖ term) is argued, not measured;
the D arms are single points against one truth (B1), not a sweep; scenes are planar with one
perturber; the co-orbital case is a band, not the gold run's phase-neighbour formation; G2's
0/39 at 0.57 rad/orbit is underpowered next to B3's 1/84 at the same rate (scene-dependence of
the boundary is mapped coarsely); the tide's quadrupole e-power is unresolved numerically
(irrelevant at these e, but stated). The negative control (N1) proves the miss detector sees
staleness; it cannot prove the sound rows are miss-free at rates below their sensitivity.
