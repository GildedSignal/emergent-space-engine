
===== 20261006-0220-scout-4ea2 =====


===== 20261006-0737-components-4643 =====
**Claim.** On the belt's kick workload, deferring dormant encounter pairs to calendar wakes
is the wrong lever: pairs are indeed deeply dormant (99.7% of first in-window passages lie
>100 orbits ahead; median 26,000), but per-kick cost is 92% numeric-window *setup* — the
far-future exact checks that deferral would skip are only 7–8% of the work — and the
zero-eval analytic window is killed by a 427× over-firing penalty.

**Bottleneck.** Board focus item 3 (encounters without work per orbit or per element
change) and the open taleb-3ec1 lead ("99% of setup work lands on dormant pairs, defer
it", handoff "Next, not started"). This run measures that lead and kills it as a
standalone configuration, redirecting the lever to setup-skipping (the slack skin).

## Evidence

Binary: `crates/encounters/src/bin/dormant.rs` (experiment-only addition; the patch is

===== 20261006-1135-spacex-317c =====
**Claim.** The slack skin's missing window-width term exists and is native to the representation
(build every window as the ρ-level set at ρ_eff = ρ + √2⁺·s·r²max, Cross shortcut disabled): it
makes the deferred certificate **exact at s = 4·eps_u on every case measured** — 0 missed /
0 false on the belt at the plane's kick size (eps 1e-6, of 163), on the held-out fleet
(of 1179) and on the ring truth control against the dense truth (of 1506), where the published
skin missed 29–102 — **and at the plane regime the lever survives soundness: setups/kick 14.9
vs always's 188.6 (the 12.6× cut, unchanged), us/kick 2547 vs the published always's 3312**.
But the sound certificate's price scales with s: at 100× the plane's kicks (eps 1e-4) the same
s = 4·eps_u costs more than it saves (fleet 37.9k vs 23.8k µs/kick; belt unfinished in 300 s vs
always's 38 s) — the sound skin is a plane-regime lever with a measured economy boundary, not
a general one.

**Bottleneck.** Board focus line 3 (encounters without work per orbit or per element change).
The 6-October gold (`components-4643`) named the slack skin "the lever" attacking the 92% setup

===== 20261006-1545-second-20261006-1436-scout-eab7-73f0 =====
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

===== 20261007-0711-taleb-2e81 =====


===== 20261007-1550-dynamics-71a5 =====
**Claim (one sentence).** The encounters certificate's premise — a pair's section is an
"exact integer circle rotation ... a certificate valid until a kick" (docs/law.md;
`crates/encounters` models fixed `pom`) — has a finite horizon under the law's own compiled
apsidal precession: equal precession ages nothing (a rigid rotation, measured exact), but
differential precession Δϖ̇ carries the pair's relative Binet angle to its next orbit-tangency
in t_tang = (angular distance to that tangency)/Δϖ̇, where the standing "never" certificate
dies (measured: 12/12 runs, every realized encounter lands after its tangency, none before)
and the active schedule decorrelates (measured: 27/27 proposals wasted at the highest rate) —
so sections must live in the pair's co-precessing frame (an O(1) angle update per pair from
the tubes' exact Δφ per cycle), which matters exactly in the strong field (≈ 40–400 orbits at
p ≈ 50 M for generic belt pairs; 4×10⁸ orbits in the weak-field scene, irrelevant there).

- **Bottleneck.** Board focus "finding encounters without work per orbit or per element
  change" and the top scaling risk (candidate work must track real encounters). The horizon

===== 20261007-2344-second-20261007-2246-system-969a-5d90 =====
**Claim (one sentence).** The checker's named experiment holds and the original claim now
carries its measured half — the shipped timing tier (`sections` + `dioph::first_hit` +
exact check, byte-identical `crates/encounters` code) stacked on the run's 12+12-bit
Catalogue-key window recalls every fine-truth encounter on every scene inside the window's
sound domain (0 missed, 0 false; steady/dense/spread/formation), with marginal tier-2 work
**bit-identical** to the same tier fed the shipped cone candidates and the key-only
breadth costing zero tier-2 work, and r8 v4's frozen `steady` and `checks` gates passing
for both tier-1 sources (1.400 vs 1.296 at 10⁵ orbits, gate ≤ 2.0; 1.10 checks/hit, gate
≤ 1.5) — **but the sound domain ends at e ≈ 0.969, not the checker's e ≈ 0.9995**: there
the pad's 1/g term crosses the periapsis (g < √(2⁻¹²)), the u-interval inverts, tier-1
silently excludes 46% of bodies and the stacked tier misses **206/289 (71%)** of the fine
truth's encounters, a boundary the checker's extreme-e probe could not see because its
sampled truth was underpowered (10 pairs).


===== 20261008-1058-second-20261008-0945-taleb-48e5-abd7 =====


===== 20261009-0401-second-20261009-0208-fermi-fe6b-90fb =====
**Claim.** The checker's named experiment, done: the kick→pair-certificate cascade is now
anchored on the shipped code at N = 10⁶ (with exact soundness controls), the event-queue term
is measured and wired in, and the original claim **holds in rank but not as written** — the
cascade is still the only term near a core (0.966 no-skin / 0.077 with skin per 10⁴-cell,
M1-implied, reproducing the original's numbers from the reproduced anchor), but (a) "every
other term ≥ 3 orders below" is false: a window-keyed queue costs 0.032 cores (2.4× below the
skin cascade, not 10³), so the program-level keying rule is load-bearing, and (b) the 812.8
pairs/kick is a **cell constant, not a belt-density convention**: measured law
`pairs/kick = 0.0346·n·(1+X)/(2(X−1))` (six geometries, 10⁴→10⁶, ≤ 7% error; anchor point
86,332 pairs/kick at 10⁶ fixed extent), so 10⁹ in one belt costs 2×10⁴–10⁵ cores and the
working point requires the billion partitioned into ~10⁵ cells of ~10⁴ bodies — plus a new
does-not-fit: the shipped global U-index itself (16 B/body = 16 GB at 10⁹).

**Bottleneck.** Same as the original run (board: fitting 10⁹ in 8 GB; candidate work vs real

===== 20261009-0521-library-189e =====
**Claim.** The 30-September lead — "a pair's next close conjunction is a Diophantine approximation (continued fractions)" — is killed at belt scale: the conjunction calendar is not a one-rotation-number problem there, because conjunctions come in clusters whenever the relative wobble rate 2e·n exceeds the synodic drift rate |Δn| (≈90% of belt pairs at e ≤ 0.05).

**Bottleneck.** Board item "finding encounters without work per orbit or per element change (the Binet cone, r8 v3, plus a skin)". This deletes the planned CF-calendar path before it was built, and demotes commensurability class from selector to non-selector. It does not speed up what exists; it removes a component from the design queue (less is more).

**Evidence** (all commands ≤ 60 s, from `lab/results/20261009-0521-library-189e/work/`):
- `python3 probe_cf.py metrics.json` (13 s): 3×66 held-out seeds, two-body Kepler truth (fine time grid), predictors from elements only. Median percentile rank of the CF-predicted conjunction among 30: **0.48 / 0.55 / 0.45** for e ≤ 0.05 / 0.15 / 0.30 — indistinguishable from the random-k control (0.48 / 0.48 / 0.62). O(1) drift inversion: same (0.52 / 0.45 / 0.48). Exact-window hit ≤ 7.6% everywhere.
- Controls: homogeneous instrument (three-distance theorem: argmin ‖kω‖ ∈ convergent denominators) passes **1.000** after I found and fixed a CF-recurrence init bug — the first run's 46% was my bug, caught by the pre-registered control, reported. Inhomogeneous (shifted target) passes 0.63: convergents certify returns, not arbitrary residues.
- Mechanism, demonstrated: `a2/a1 = 1.012, e ≈ 0.03` gives **5 longitude crossings in one synodic period** sweeping 0.8 turns (cluster), then a gap — relative longitude oscillates through several turns per close pass. Regime number χ = 2e·n/|Δn|; belt census (`census.py`, 0.6 s, N=500, 124,750 pairs): χ < 0.5 for only **10.1%** of pairs; envelope-disjoint (group bulk-no) **29.3%**; "skin" (neither) **5.3%**.
- What survives: weak recurrence — after the true best conjunction, the one at +q_best (best convergent denominator) has miss 0.48–0.67× the median vs 1.00× for a random offset. A hint, not a calendar.
- Readwise evidence cached: `work/highlights.jsonl` (4,580 highlights, 770 books) + `work/quotes.md` (verbatim quotes used below).

**Predictions** (`predictions.md`, written before the run): P1 (median rank ≤ 10%, ≥60% top-decile, ratio ≤ 1.5 at small e) **failed on all three** (0.48 / 7.6% / 1.9). P2 failed (no band below 0.45). P3 held numerically — ≥50% adjacent pairs with sharp convergent q ≤ 13 → measured 92.6% — but the metric is near-vacuous (92.5% of *all* pairs have one; measure theory predicts ~this), so the "held" is a lesson, not a win. Degeneracy probe: exact 7:1 vs ε detuning changed nothing (flatness 0.104 → 0.114; k_true stable) — the r4-v2 commensurability degeneracy does not appear in miss-distance space. Kill criteria as pre-registered: **KILL confirmed** (median rank > 30%; ≥50% of seeds > 2× minimum in two bands).

**What would make it wrong.** My truth is a two-body Kepler pair with a shared primary and no perturbations; three-body forcing or a real belt's element diffusion could add the coherence my predictor lacked — unlikely to help a method that loses to random at e ≤ 0.05. The cluster diagnosis rests on the equation-of-center argument; if `state()` had a second bug the instrument would not have passed 1.000. The census assumes uniform a and e ≤ 0.05; a resonance-sculpted belt (Kirkwood gaps) would raise the sharp-convergent fraction above vacuity — that is the one workload where the CF idea deserves a second look.

===== 20261009-1345-second-20261009-1259-fermi-c7eb-46a6 =====


===== 20261009-1504-second-20261009-1345-system-136a-ca96 =====


===== 20261009-2043-second-20261009-1936-system-8716-88ee =====


===== 20261010-1029-taleb-5c01 =====


===== 20261010-1947-second-20261010-1920-spacex-cb3f-f79a =====
**Claim.** The named next probe is done and it is a **kill**: a provably-safe same-doll rejection
pre-filter at the scan seam exists and is bit-identical everywhere tested (9/9 seeds × placements,
plus full 3×10¹⁰ runs), but the only airtight bound rejects 0.07 % of ship-scale pairs — no
deletion; every tightening that would reject measurably misses encounters (three independent
digest breaks recorded), because the player's scan interval (2⁴⁰ doll-time, its ~22 s step)
multiplies any velocity-bound looseness across every ship-scale gap, and the cheap bound (the
binding's own velocity word) sits 8–16× above the true speed once kicks begin. The dense
same-doll cohort the original never grew is now measured: the exact tier is **4.1 µs per pair,
linear in population** (3.02 M pair checks at cohort 200; 794–860 µs per player item vs 57–64 µs
in the star-doll belt; ~4 s per player item at 10⁶ same-doll bodies) — the deletion belongs to the
encounters seam (phase certificates), not a per-pair filter.

**Bottleneck.** The checker's one-experiment-to-gold: the safe ≥10× on the scan intercept, or a
kill. Board line 1 and the top scaling risk. Delivered: the kill, with the frontier measured on

===== 20261011-1102-second-20261011-0924-library-9834-5c16 =====
**Claim.** The checker's named gold experiment is done: under real kicks at the plane's
rate (κ=0.3/body/orbit, eps=1e-6, slack-skin quantum s=4·eps_u), the original's
three-number record does **not** hold — its retrigger period (the phase-error quantum,
measured 13/263/449 synodic intervals at ρ=1e-4/2e-3/5e-3) is the same order as the
slack-skin period, so with the record's own scan-based window construction charged,
amortized work per interval is **0.05–0.89× the plain per-interval scan** (a 1.1–20×
loss, rising to 96× at eps=1e-4) and work per real encounter is 43k–3.97M evals against
scanning's 38k — the 33–146× claim inverts under real kicks; what survives is a
different certificate (exact per-kick anchors + closed-form conjunction-longitude
arcs), which wins 18–23× on work but is **not proven zero-miss** anywhere that hits
exist, because at belt eccentricities (e up to 0.08) the relative longitude rate
reverses (94–100% of pairs) and the hit set is genuinely 2D.

**Bottleneck.** The board's top scaling risk (candidate work must track real

===== 20261011-1234-taleb-62f7 =====
**Claim.** The bulk regime — the one every encounters run since 6 October has measured and
punted on ("ruin in absolute terms at fleet scale", "the encounter-skin problem") — is now
priced and owned: when concentrated packets cross, the real contacts are Θ(n_A·n_B)
(measured exponent **1.94**, per-pair probability flat at **0.021** across n = 50–800 per
fleet), so the per-ship load grows **0.021 contacts per opposing ship** — **2.1×10¹⁰
contact events in one 10⁶-ship-per-fleet crossing, ~21,000 per participating ship** — and
*no discovery certificate can help, because discovery is already exact: the events
themselves are the workload*. The escape is measured and works: **one aggregate event per
packet crossing** — per-ship flux λ_i = ρ_B,2D · 2R · L_i, the contact tube swept by ship
i's exact Kepler trajectory through the opposing packet's measured density grid in the
co-rotating frame — costs 257·(n_A+n_B) evals (O(n)), has **zero free parameters**, and
reproduces the exact truth's total contacts at ratio **0.87–1.04 on all ten packet
scenes** including a held-out crossing geometry (in-window 0.95–1.01), the active-ship set
within 0.003–0.04 absolute, per-active load (26.8 vs 26.0 at n = 300), and per-ship ranking

===== 20261011-2132-second-20261011-2028-system-3b42-214f =====


===== 20261007-1801-dynamics-532c =====
**Claim.** For coplanar belt pairs the encounter tier is split by one dimensionless
number, the crossing fraction χ_t = Δa/(e₁a₁+e₂a₂): every pair that can physically
encounter has χ_t < 1, and in that whole regime the conjunction longitude advances
with jitter ψ = O((4/3)/χ_t) rad (measured std 1.9–2.5 rad) and conjunction-anchored
distance checks — raw radial or the Öpik perpendicular correction — miss 40–97 % of
true close approaches, so the continued-fraction certificate on the synodic rotation
is valid only in the sparse sub-tier ν = W·ε(R) ≪ 1 (events per orbit per pair),
and the deep-crossing tier (ν ≳ 1, ψ ~ 2π) must be scheduled by a phase-neighbour /
dense mechanism, not by per-pair synodic CF.

**Bottleneck.** Board: "finding encounters without work per orbit or per element
change" and the top scaling risk (candidate work must track real encounters). This
run says where per-pair certificates pay and where they cannot: it sizes the
payment schedule (events per conjunction ε, gap tail, cluster factor, drift

===== 20261012-1340-quant-e49d =====


===== 20261011-0517-quant-d7bd =====


===== 20261011-0736-dynamics-ec74 =====
