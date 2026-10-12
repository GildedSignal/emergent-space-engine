
===== 20261006-0220-scout-4ea2 =====
# dossier.md — run 20261006-0220-scout-4ea2 (lens: scout)

## Claim (one sentence)

The plane's four B13 failures are a representation gap, now measured end to end: a flyby must be
an **event entered by analytic detection at ≥ 1.5·SOI** (the two conics already know the
encounter), after which the plane's own in-doll rule (exact planetocentric Kepler drift + tide
kicks at 1/64 of the passage) holds B13's 1% gate on the near-parabolic corner — **15/15, worst
2.4×10⁻³, ~65–120 events per encounter, independent of e_h** — where the star-doll cadence rule
passes **0/60 anywhere** and the pure Öpik one-event map (no interior) passes **≤ 7/41**: adopt
the encounter event (crates/encounters detection wired as the doll door), not the patched-conic
leg.

## Bottleneck

Board focus 1/2 (kicks dominate; the lever is cadence) and the live gate failure

===== 20261007-0711-taleb-2e81 =====
# Dossier — taleb-2e81: the fleet engagement (two swarms on crossing orbits) is a second, distinct ruin of the pairwise encounters tier — quadratic store with the trigger and the point-node guard both blind to it — while the tier itself is perfectly sound there

## Claim (one sentence)
When two tight swarms on crossing orbits meet (the fleet-engagement case every prior concentration test skipped), 100% of the n_A·n_B cross pairs become cone candidates (40k/40k, 160k/160k, three seeds) each carrying 2 Cross sections — a Θ(n_A·n_B) store, ~144 TB at 10⁶×10⁶ — that neither the adopted clump trigger (cross Binet separation 0.29 vs eps_u 4×10⁻⁴; an eccentric swarm's own intra-diameter 5×10⁻² because it scales as e·Δϖ/p, so it never becomes a "clump") nor a point-node interchange guard (partner's node-passage distance p50 6.3×10⁻² ≈ 630× the ρ/v_rel window, from the same ϖ spread smearing each pair's crossing longitudes) can cheapen — yet the tier is exactly sound there (0 missed, 0 extra against full conservative-advancement truth, 36+34 encounters, two seeds) and amortized-cheap (51–55 evals per hit, flat from 40k to 160k pairs): the engagement's ruin is the store and its per-kick invalidation, not compute or correctness.

## Bottleneck
The board's top scaling risk ("candidate work must track real encounters"), extending gold taleb-09b5 beyond the regime it measured. That gold killed the quadratic tier *inside* a co-orbital formation (dormancy-compute ruin, Wide windows at 606 evals/pair, 4–6% misses) and adopted a phase-neighbour train triggered by Binet clump diameter. The engagement is the complementary regime: the store is the ruin (Θ(n_A·n_B) Cross sections, 0 numeric setup evals, 55 evals/hit amortized, zero misses), the trigger cannot fire, and the natural analogue of the train (two trains meeting at the ≤2 crossing longitudes) is measured dead as a point certificate.

## Evidence (all runs ≤ 9 s, Linux x86, 8 vCPU, < 100 MB; `evidence.log`; binary `crates/encounters/src/bin/cross.rs`, copy in this folder)
Reproduce: `CARGO_TARGET_DIR=/tmp/x-target cargo build --release -p emergent-encounters --bin cross`, then `cross econ 200 200 20`, `cross econ 400 400 20`, `CROSS_SEED=7 cross econ 200 200 20`, `cross guard 200 200 20`, `CROSS_SEED=7 cross guard 200 200 20`. Swarm A: a=1±10⁻⁵, Rayleigh e≈10⁻³, ϖ±0.1, λ uniform; swarm B: a=1.2, e=0.3, ϖ=0, same spreads (crosses A's annulus at ±1.259 rad); ρ=10⁻⁴. Truth = `truth.rs` conservative advancement (Halley states); method = sections + Diophantine first-hit + exact check (Newton states) — no shared solver path.

1. **Saturation (prediction 1 held):** 100.0% of cross pairs are cone candidates at 20×20, 200×200 (three seeds) and 400×400. Cross Binet separation [0.284, 0.291] sits ~3 orders above eps_u (3.9×10⁻⁴), so the gold's clump trigger never fires for the cross set. Worse: swarm B's *intra* diameter is 5.5×10⁻² ≫ eps_u — the ±0.1 rad ϖ spread enters Binet V as e·Δϖ/p ≈ 0.027 — so an eccentric fleet never triggers its own internal train either; the trigger's ϖ sensitivity scales as e, ~300× tighter at e=0.3 than at the gold's e≈0.001.
2. **The ruin is the store, not compute (prediction 2 held; a different signature than taleb-09b5's):** every cross pair makes exactly 2 sections, all Cross kind (analytic crossing windows), **0 numeric setup evals per pair** (vs the formation's Wide 606). Method work is 51–55 evals per real encounter, flat in n (40k→160k pairs), ~70× cheaper than the gold's sea-sea reference (3.7×10³). But the store is Θ(n_A·n_B) sections ≈ 1.4×10¹⁴ B ≈ **144 TB at 10⁶×10⁶**, and every element change during the engagement re-opens every section. Per-pair hit rate ≈ 9×10⁻⁴ per 20 orbits (flat, three seeds) ⇒ a 10⁶×10⁶ engagement generates ~9×10⁸ real encounters per 20 orbits (~45 per body per orbit) — the discovery tier is *not* the fat tail; the contact law behind it is.
3. **Soundness (prediction 3 held, stronger than expected):** full truth audit of all 40,000 cross pairs over 20 orbits: 36/36 found, **missed 0, extra 0**; seed 7: 34/34, 0/0. The co-orbital regime's boundary-miss pathology (4–6%) does not transfer: transversal crossings are what the Cross window was built for.
4. **The point-node guard is dead as specified (prediction 4 failed via my own pre-registered P5; prediction 5's risk materialized):** I proposed the analogue of the train — two streams meeting at the ≤2 crossing longitudes of the mean orbits, a merge scan in node-passage time, judged by partner rank. Measured: rank p50 3–4, max 9 — but the diagnostics kill it: the partner's own node passage is **p50 6.3×10⁻²** from the encounter time, ~630× the ρ/v_rel ≈ 10⁻⁴ coincidence window, and the A body's likewise. Encounters are pinned to each *pair's* crossing longitudes, which the ϖ spread smears over ±0.1 rad — ~1000× wider than ρ — so a ρ-window merge at the mean node finds none of them; the measured "rank ≤ 9" was ordering noise, not coverage. (The node-longitude column in evidence.log is wrap-bugged, θ₁ unnormalized; the conclusion rests on the time distances, which are clean.) A k-nearest watch would have had to watch k ≈ n·(smear/period) neighbours — linear in n: dead.


===== 20261008-1058-second-20261008-0945-taleb-48e5-abd7 =====
# Dossier — 20261008-1058-second-…-abd7 (second author on 20261008-0945-taleb-48e5)

## Claim

The silver's radial result stands and is now **radius-flat in per-doll units**: candidate work per
real encounter is `cpe ≈ 1.2–1.3·a^2.53/ρ` (hit-weighted; the silver's 2.6 was an unweighted-fit
overstatement), the a-exponent decomposes exactly as **a^1.5 local clock × a^1.0 relative-ρ**
(degree cancels in cpe by construction — not "degree growth"), so carrying **ρ ∝ a and per-doll
(local-orbit) time** makes work per encounter radius-flat with measured residual exponent
**0.000 over a 100× scale ladder** — an exact self-similarity of the shipped cone/sections
machinery, not a bound. The record regenerates from shipped code except `CE.jsonl`'s per-bin degree
columns (the author's disclosed pre-fix artifact, left stale; belt-level fields are bit-identical),
and the three misreported numbers are corrected below.

## Bottleneck


===== 20261009-1345-second-20261009-1259-fermi-c7eb-46a6 =====
# Dossier — 20261009-1345-second (second author on 20261009-1259-fermi-c7eb)

## Claim

The checker's named experiment is done and the corrected claim stands, stronger than the original:
with the impulse coefficient validated by integration on real truth encounters (1091 RK4 runs,
meas/pred median 0.998, v_rel exponent −0.889 vs the author's −2), belt encounters cross the law's
period-tick grid only above **m_crit ≈ 1.3×10⁻¹⁷ M☉ (a ~1.3-km rock; p1 1.2×10⁻¹⁸ ≈ 600 m)** at
game density (N=10⁹, a=2.7, σ_e=σ_i=0.1, ρ=10⁻⁴ AU) — the prior run's 500-m/8×10⁻¹⁹ was ~16× low
but conservative in direction — and the sub-threshold random walk cannot make belt self-evolution
a binding term: in a walk on the measured kick distribution (1000 walkers × 10⁵ kicks) **no 50-m
rock crosses one period tick within 1.7×10⁴ orbits** (0/1000; Gaussian arithmetic says 4.7×10⁶
but the kick distribution is borderline Lévy α=2 — impact-parameter density ∝ d·dd makes E[x²]
log-divergent — so only the walk bound is quoted; 500-m rocks cross in ~10 orbits), and although
the tp/phase channel (which the prior run never checked) first-crosses far sooner (~340 orbits for
a 50-m rock; no mass above ~10⁻²⁴ M☉ survives 10⁴ orbits), each phase tick is 5×10⁻¹¹ rad —

===== 20261009-1504-second-20261009-1345-system-136a-ca96 =====
# Dossier — run 20261009-1504-second-20261009-1345-system-136a-ca96 (second author, system lens)

## Claim

The checker's named gold experiment, run on the shipped crate, **refutes the caching half of
20261009-1345-system-136a's claim**: the Δϖ rotation that cached `sections()` tolerate with zero
missed encounters is ≈1×10⁻⁵ rad — ~24× below the fine Δϖ-band (2.4×10⁻⁴) the original assumed safe
(9.3% of encounters silently missed there; 99.5% at the wide band 1.5×10⁻²), the radial half of the
key fails too (18.5% missed at half-bucket e-drift), the dossier's own mitigation (per-kick ti/tj
refresh) recovers 30× but not zero (0.32% at the fine band) and window widening ×16–512 changes
nothing — so the binding staleness is the arc geometry θ_c, which only a re-setup recomputes. The
corrected zero-miss amortization is ×1.8 at the unaveraged cadence (residence 0.056 orbits ≈ 2
kicks) and pure loss (×0.02) at the averaged cadence. The **discovery half** of the original claim
(bucket tier as conservative candidate index, zero misses) is unaffected and reproduced.

## Bottleneck

===== 20261009-2043-second-20261009-1936-system-8716-88ee =====
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

===== 20261010-1029-taleb-5c01 =====
# Dossier — 20261010-1029-taleb-5c01 (lens: Taleb)

## Claim (one sentence)

The pairwise encounter tier's silent misses are not a concentration corner (the gold's 2%): they are a **horizon-edge soundness hole** — every real encounter already in progress at the start or end of the scheduling horizon is silently dropped (284 missed pairs at 1 orbit vs 281 at 2 orbits while true pairs grow 1407→2250: the dropped set is pinned to the horizon's two edges), which hits **20% of true encounters for any population that starts bunched** (any fleet at kick/handover time), is **not guardable by the breathing number** a·(e_i+e_j)/ρ (misses peak at R1≈10 and vanish at R1≥30 — the dangerous side is e-spread ≈ ρ, not ≫), and does not respond to the d_of_s grid (k=256: identical).

## Bottleneck

"Candidate work at scale … work must track real encounters" (HANDOFF risks, board focus). The co-orbital certificate replaces the pairwise tier only in the concentrated regime; everywhere else the pairwise tier stays, and **every kick or handoff re-opens a horizon, recreating the edge**. A certificate that silently drops the encounters in progress exactly when the player's influence arrives is the ruin class (wrong canonical event list, no signal): PRINCIPLES #13 "basically we don't want errors that can compound that's the goal". It also falsifies the premise behind run 20261010-0306's "the shipped cone tier missed **0** encounters on every scene": that measurement's truth (conservative advancement in the same crate over the same horizon) shares the blind axis — the third independence failure in the lab's record (memo re-timing, λ-binned brute, now this).

## Evidence

Linux x86 cloud, 8 vCPU, < 300 MB. Instrument: `taleb missmap nc a_hw sig_e rho sig_lam seed orbits [debris_n debris_e]` (added by this run to `crates/encounters/src/bin/taleb.rs`, on top of the gold 20261006-0346 patch, which must be applied first: `git show origin/claude/lab-20261006-0346-taleb-09b5:lab/results/20261006-0346-taleb-09b5/work/patch.diff | git apply`). Truth: uniform-in-time grid (4096 samples/orbit, motion per sample ≤ 5e-6 ≪ ρ), pairs with coarse min < 4ρ refined by 2048 dense samples + golden section — **no binning, no cones, no shared machinery**. Method: `cone_pairs`+`sections`+`run_section` exactly as shipped, over [0, H]. Reproduce (each ≤ 60 s except the 20-orbit run, ~80 s; CARGO_TARGET_DIR=`/home/glmlab/lab-target-1`):

```
cargo build --release -p emergent-encounters

===== 20261011-2132-second-20261011-2028-system-3b42-214f =====
# Dossier — run 20261011-2132-second-20261011-2028-system-3b42-214f (second author on 20261011-2028-system-3b42)

## Claim

Both of the checker's named gold experiments are done, and the original claim **holds**:
the encounter tier's same-key (straggler) branch freezes as an **arc window on the tube's own
phase axis** — width `W = 1.5·(4·e_hi + 3·e_hi²) + dn_cell·t_end` from the key cell's constants
alone — with **zero missed encounters at every n and every dial**, **same-key candidates per
real encounter constant in n** (5.3→5.6 at the engine dial, n 400→3200, both terms ∝ n²), and
the birth-fixed branch (equal integer periods) permanent and 25–32× cheaper than all-pairs; and
the strong-field key order survives because **U(L)|E never turns in the stored (bound) domain**
(0/200 E-columns through the separatrix-adjacent region; the dossier's worry was conjecture),
with the (E,L)-key lattice zero-miss (7,924,025/7,924,025 exact-tier pairs, inflation 1.002) and
the Newtonian-contiguity U-scan complete (0 misses) at r_p down to 4.6 GM.

One correction to the author's record: rank-k is **not** the certificate (member clustering

===== 20261012-1340-quant-e49d =====
# Run 20261012-1340-quant-e49d (quant lens): the wake of one kick in the encounter tier

## Claim

One kick's re-certification wake in the Binet-cone tier is O(candidate degree) = O(N) single-thread
work (6.8 ms at N=10⁴, slope 1.00–1.07; a full 16.7 ms frame at N≈2.4×10⁴), and the queued slack
skin cannot absorb player burns (skippable 94.6% at δa/a=1e-9 but 0.25% at 1e-3, where the slack
rule is also unsound: 5 skipped pairs changed outcome) — but 98% of the wake (the window setups)
has deadlines ≥ tens of orbits away (no candidate pair's first post-kick conjunction inside 10
orbits; 99.95% of setups find no encounter within 10 orbits), so deadline-ordered scheduling turns
the burst into a stream; only the cone re-scan (1.3–2.1% of the wake) must land in the kick's
frame.

## Bottleneck

The top scaling risk (board, 5 October): candidate work must track real encounters, and

===== 20261011-0517-quant-d7bd =====
# Dossier — 20261011-0517-quant-d7bd (Quant lens)

## Claim

In the flying plane, every resolved player item pays `PlayerNeighbourhood::find`, an exact
neighbourhood scan that clones and evaluates every body in the universe: measured 1.5–1.7 µs
per body (linear), so one player event alone crosses a whole 16.67 ms frame at ≈10⁴ bodies in
the store and costs ~1.6 s at belt scale (10⁶) — the exact-encounters seam behind
`Encounters` breaks by four orders of magnitude before the belt, and the Binet cone (or a
skin) is the only asymptotic fix; work must track encounters, not bodies.

## Bottleneck

Board's top scaling risk ("candidate pairs per body grow with N; candidate work must track
real encounters") and the encounters seam (plane.md foundation 6: "an exact per-doll check
now, the Binet cone later"). This run puts a number on *when* "later" must arrive: the

===== 20261011-0736-dynamics-ec74 =====
# Dossier — 20261011-0736-dynamics-ec74 (dynamics lens)

## Claim

The impulsive-conjunction encounter representation has a **measured domain rule** —
it is valid only for passages inside the Hill sphere (b ≲ 3·r_H, where toy/RK4
agree within 8–42% at χ ≤ 0.31; outside, shear-shielding makes free-space
Rutherford 2–5× wrong) — and on the swarm-coupling axis Ψ = μ_g/(aσ_e)³ a
mutual-scattering swarm shows three regimes: a **gas** (Poisson events, λ ∝
Ψ^0.95, no stirring runaway), a **birth-burst/capture** regime (event load 18×
above steady state at birth, Fano 177→2186 growing ~ w^1.1 — avalanche scaling),
and a **clump** regime beyond the representation. Real game swarms (ships,
asteroid belts) sit far inside the gas regime at Ψ ≲ 10⁻⁶, where mutual
gravitational encounters are deletable.

## Bottleneck