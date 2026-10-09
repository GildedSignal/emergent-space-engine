# Dossier — run 20261009-2043-second-20261009-1936-system-8716-88ee (lens: second author)

## Claim (one sentence)

The unified encounter certificate's index is repaired — each slow-band bin bounds |Δn|
by the exact extremes of its occupants' own mean motions n = a⁻¹·⁵ instead of a ΔU
linearization — and with that one change the shipped index emits exactly the naive
per-pair rule on every scene tested (0 drops, 0 adds over 23 scene-instances,
including the checker's const-p adversarial class, fresh seeds, beyond-domain e, and
N = 2048 fleets), zero-miss recall 1.0 holds on all fresh-seed scenes with the
5(e_i+e_j) constant fixed a priori, and the scale record now regenerates from one
shipped command.

## Bottleneck

The board's top scaling risk: candidate pairs per body vs real encounters. The
original run (silver) unified the two adopted certificates into one rule but shipped
an index whose bin window linearized Δn as ∝ ΔU; the checker falsified it (recall
0.867 on a const-p bimodal-e belt; 9–11 rule-passing pairs dropped on the author's own
scenes). This run repairs the index so "acceleration only" is true by construction —
zero-miss now belongs to the structure, not just the formula — which is the
precondition for adopting the one-rule encounters design at all (it deletes the
concentration trigger, the second certificate and the fleet category before they are
built).

## The repair (one change, exact, no new constant)

n = a⁻¹·⁵ = (U(1−e²))^1.5 depends on e as well as U; at constant p all shear comes
from e-spread and the old window 2.4·dU·H/Ū sees none of it. Each bin already knows
its occupants; it now stores their min/max n. Since n is monotone in a body's own
elements,
    dn_bound(i, bin) = max(|n_i − n_min|, |n_i − n_max|)
is the exact supremum of |Δn| over all pairs (i, j ∈ bin). The window
    w = min(TAU, dn_bound·(1+3 e_b²)·H + 5(e_i + e_max_bin) + skin_l),  e_b = max(e_i, e_max_bin),
dominates every factor of the per-pair rule's sweep, so the λ-bisect can never
exclude a rule-passing pair while emission still applies the full rule: emitted set =
naive rule, provably and (now) measurably. Tighter than the checker's suggested
1.5·n̄·max|Δ(U(1−e²))| linearization — no approximation, no constant, one min/max per
bin. Code: `exp2.py`, `Scene.unified` (old kept verbatim as `unified_old`).

## Evidence (all from shipped commands, this folder; Linux x86, orders of magnitude)

`equiv` (original scenes + checker's adversarial class, fresh seeds; ≤ 55 s):

| scene | naive | old drops | old recall | new drops | new adds | new recall |
|---|---|---|---|---|---|---|
| belt seed 1 (N=768) | 70,534 | **9** | 1.0 | **0** | **0** | 1.0 |
| mixed seed 3 | 68,916 | **11** | 1.0 | **0** | **0** | 1.0 |
| fleet s=1e-3 seed 2 | 95,823 | 0 | 1.0 | **0** | **0** | 1.0 |
| const-p {0.05,0.35} H=16 (fresh) | 107,260 | **11,495** | **0.881** | **0** | **0** | **1.0** |
| const-p 8-e-spread H=8 (fresh) | 90,524 | 4,914 | 1.0 | **0** | **0** | 1.0 |
| belt e∈[0.4,0.55] | 30,671 | 0 | 1.0 | **0** | **0** | 1.0 |

Reproduces the checker exactly (his 9 / 11 / 0.867 at his seed) and repairs it: exact
naive equality everywhere. `equiv3` (11 fresh-seed registered scenes) and `scale2`
(N = 512/1024/2048): new drops = new adds = 0 on all 17 further instances.

`truth3` (fresh seeds, 5-constant untouched, T=1024 truth; ≤ 80 s): unified recall
**1.0** on all 11 scenes — fleets s ∈ {1e-3, 3e-2, 0.1}, H=16 fleet, belts, uniform-e
belt, mixed, both const-p classes, and both beyond-domain scenes (e ≤ 0.55). Controls:
cone-only 1.0 everywhere; ideal-trigger 0.15–0.35 on fleets and 0.901 on mixed (the
rank-4 design stays falsified), 1.0 on belts. `sweep2` (8 tightness points, fresh
seeds): unified 1.0 at every point; candidates 0.049×–0.80× of cone-only. `truthres`:
T=4096 truth finds 0 new pairs vs T=1024; recall 1.0.

`scale2` (the record the original could not regenerate; ≤ 45 s): fleet candidates as a
fraction of C(N,2): **0.709 / 0.723 / 0.733** (e0=0.02) and **0.225 / 0.224 / 0.223**
(e0=0.002) at N = 512/1024/2048 — the checker's 0.718/0.223 confirmed, fraction set by
window/arc, not N. Per-body candidates grow **linearly** (181→370→751 and 58→114→228):
the original's prediction 5 ("≤ ~√N·log") was falsified by its own data and remains
falsified — re-reported, not reframed.

Cost of soundness (new, honest): the exact Δn bound widens bin windows, so unified
*evals* now exceed cone-only on belts (238k vs 186k, +28%; const-p H=16: 252k vs 131k)
and crossover sits near s ≈ 0.01–0.03 (s=0.3: 55.5k vs 16.6k evals) — but *candidates*,
the quantity the Diophantine tier below pays per pair, stay far below cone-only
(belt 0.51×, mixed 0.48×, sweep 0.05×–0.80×), and equality with the rule is what makes
them trustworthy. The saturation guard for saturated bins (skip the scan when the
window is the full circle) remains the one unmeasured production trim.

## Predictions (`predictions.md`, written before the decisive run)

Tuned only on one dev scene (seed 99, excluded from the record). Held: P1 equality
0/0 on all 23 instances; P2 old-index defect repro (9/11/0.881 fresh-seed); P3 recall
1.0 on all fresh in-domain scenes, ideal-trigger still missing; P4 equality
e-independent with recall ∈ [0.9, 1.0] beyond domain — measured 1.0 (no miss
materialized on these seeds; consistent with the checker's own beyond-domain probes);
P5 fractions ≈ 0.7/0.22 constant in N with linear per-body growth; P6 zero new true
pairs at T=4096. No failed prediction this run.

## What would make it wrong

The equality claim rests on the domination argument (dn_bound, e_b, e_max_bin each ≥
the rule's per-pair factors). A counterexample would be a scene where the bisect
excludes a rule-passing pair — e.g. float-boundary effects at exact window == sweep, or
a bin-membership gap I have not imagined. The class is broad now (const-p, bimodal,
uniform-e-spread, e beyond domain, N=2048), but "all pairs" is only ever sampled, never
exhausted. The *rule's* zero-miss on truth remains scene-tested, not proven: the
equation-of-center bound 4e + 2.5e² ≤ 5e fails for e ≳ 0.42, so the claimed domain
stays e ≤ 0.4; beyond it these seeds passed but that is luck, not guarantee.

## Cost of adoption, fit with PRINCIPLES

One min/max per bin replaces one multiply — negligible; no new state (n = a⁻¹·⁵ is
already each body's element), no new constant, no category. PRINCIPLES 4 ("no
categories: regimes are chosen by dimensionless numbers") and 19 ("a fix signals the
wrong representation"): the fix removes the index's hidden second window — the very
category the run set out to delete — by making the bin bound exact rather than by
adding machinery. PRINCIPLES 13 ("errors never compound"): a dropped candidate is a
silent lost encounter, the compounding error class; the structure can no longer
produce one. Still no 10× anywhere by itself: this run makes the original's deletion
claim *adoptable* (structure-sound zero-miss plus a regenerating record), not faster.

## The lens

The second-author lens fixes records and runs the named experiment; it may under-weight
whether the widened windows (evals +28–90% on belts) matter for the engine's frame
budget — that question belongs to the allocator bottleneck, not to correctness, and I
report the numbers rather than judge them. I also did not re-derive the rule's physics
(the equation-of-center bound) — the checker's rule-level tests passed and mine agree;
a dedicated red-team of the 5-constant at e near 0.4 remains open.
