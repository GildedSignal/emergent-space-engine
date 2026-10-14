# dossier.md — 20261014-0000-redteam-f3ce (lens: premise red-team)

## Claim

The design's error model for contacts — "at most one floor unit per event, carried
forward so that it never compounds" (representation.md §2) — is **false as measured on
the shipped contact law for mass-contrast pairs: the pair-sum carry is an unbounded
random walk whose per-contact step is a fixed fraction of the pair's kinetic energy
(median 8×10⁻⁴, worst 2.7×10⁻² of KE per contact at mass ratio 1000:1, β 0.3–0.7),
reaching 100% of KE within ~10²–10⁴ contacts**; for equal masses the same carry is
bounded (2×10⁻⁶ of KE, growth exponent 0.02), so the premise survives exactly where
masses are comparable. Secondary: the contact outcome itself is label-invariant
(0/10 seeds diverge under a full id swap), and no rung, gate or oracle anywhere watches
contact energy.

## Bottleneck

Not a board bottleneck: a design-letter defect in the dense order's floor (bottleneck
"encounters"/dense order, adjacent). What it deletes if fixed: nothing yet — but it is
the "one error budget" of §2, the sentence every other carry in the design (tide
carries, kick carries, the burn carry) cites as its licence. Gain: a regime gate or a
pair-scaled carry keeps §2 honest before the dense order scales to 10⁹.

## Evidence (all on shipped code: `crates/lattice`, law `es-lattice-relativistic-v1`,
the law the engine's battle scenes ship — `crates/engine/src/scenes.rs:43`; probe:
`crates/lattice/examples/rt_carry.rs`, regenerable by `regen.sh`, ~6 min total)

**Instrument self-test:** the growth-exponent estimator reads α = 0.500 on a planted
√t series (the saturating control reads 0.345 because its cap sits inside the last
decade — disclosed; the estimator itself is exact on walks).

**Ledger control (positive):** ΣE(t) − ΣE(0) = Σ residual **exactly at every
checkpoint of every arm and seed** (10 gas seeds × 11 checkpoints, 10+10 pair seeds,
5 perm seeds). The bookkeeping is perfect; the physics it books is not.

1. **Equal-mass hot gas** (200 bodies, β ≤ 0.7, 5 seeds, 6×10⁴ chronons, ~4×10⁴
   contacts): median running-max exponent of per-body |residual| α = 0.020; end
   |Σres|/KE ≤ 4.5×10⁻⁶ (median 1.9×10⁻⁸). **Bounded — the premise holds here.**
2. **Cold gas** (β ≤ 0.014): median α(max|res|) = 0.194 — sitting on the b12 bar —
   and |Σres| walks (α = 0.380) to 2.4×10⁻⁴ of KE; the momentum carry reaches
   1.99×10⁵ quanta ≈ 0.5% of one body's momentum (seed 5, t = 6×10⁴).
3. **Mass-mixed gas** (m = 1…1000, β ≤ 0.9, seeds 1–5 + held-out 11–15): end
   |Σres|/KE = 0.9–2.7% (median 9.8×10⁻³, held-out median 4.5×10⁻³); the walk
   exponent shows on 3/10 seeds (0.457, 0.379, 0.534), 0 on the rest. **My frozen
   kill bar (median α ≥ 0.2 or median frac > 1%) does NOT fire: 0.055 and 0.98%.**
   The gas dilutes the pair mechanism; the isolated pair isolates it:
4. **The pair** (masses 1000:1, head-on, β 0.3–0.7, 159–209 contacts, 10 seeds):
   the pair-sum carry wanders with per-contact steps of 2×10⁻⁵ – 2.7×10⁻² of KE
   (median 8.4×10⁻⁴); the end excursion reaches 16.5% of KE at the median seed and
   **558% of KE** (seed 4); the series (seed 4: −1.47×10¹² at t = 4×10³, +5×10⁸ at
   t = 2×10⁴, −1.04×10¹² at t = 4×10⁴, in units where KE ≈ 2.6×10¹²) is a **walk,
   not a monotone leak, and not bounded**. The step scale is the light body's energy
   quantum (2Q² per unit mass ≈ 6×10⁻⁴ of pair KE at β 0.6): the ledger's quantum is
   per-unit-mass while the physics is per-pair — a representation mismatch, the
   "bandaid signal" of principle 19.
5. **Speed control** (same pair, β 0.02–0.05): per-contact step median 4.2×10⁻⁵ of KE
   — ~20× smaller but the same unbounded mechanism; even slow mass-contrast contact
   compounds, at 100% of KE after ~3×10⁴ contacts.
6. **Label symmetry** (the lens's principle-4 attack): swapping the ids of the 1000:1
   pair changes **no velocity at any contact in 10/10 seeds** (the carry's *home*
   differs; `digest_same = false` only because ids and carry homes are digest state).
   A 32-body gas with pseudo-randomly permuted ids diverges at tick 16–25 on 5/5
   seeds (end |Δk| up to 3.4×10⁴ velocity quanta ≈ 0.5c after 2×10⁴ chronons of
   chaotic amplification). **Outcome label-invariance survives in the isolated-pair
   domain; in a many-body gas the id routing is one more quantum-scale seed, no
   larger than the rounding itself.**
7. **Letter mismatches found in passing:** §2 says contacts resolve "in the frame of
   one of the two bodies" and "solve one quadratic"; the shipped law resolves in the
   pair's centre-of-momentum frame (Minkowski reflection in the hyperplane orthogonal
   to N = (d·P, E·d)) and "no square root enters the rule" (relativity.rs:15–17).

**Commands** (each as in `regen.sh`): `cargo run --release -p emergent-lattice
--example rt_carry -- gas-hot|gas-cold|gas-mixed 1 2 3 4 5|gas-mixed 11 12 13 14 15|
label|label-slow|perm`.

## Predictions

`predictions.md` was written before the decisive run. Score: ledger control **held**
(exactly, everywhere); cold "saturates" **half-held** (α 0.194 not < 0.1; frac 2.4×10⁻⁴
not < 10⁻⁴); hot **held**; my commitment to a mixed-gas walk at the median **failed**
(median α 0.055 — the gas dilutes; the walk lives in the pair and in 3/10 gas seeds);
label first-contact **held**; label divergence **failed — 0/10** (the outcome is
label-invariant; a better result than I predicted); perm digests differ **held**;
held-out seeds **held** (same split class). My pre-registration's real flaw: the kill
bars were gas-scoped, so the strongest phenomenon (the pair) had no frozen bar — the
pair numbers above are exploratory and labelled so.

## What would make it wrong

The pair walk is measured at stress scale (Q = 2¹⁶, radius = Q, box = 64Q): a
different Q rescales the step (the quantum is 2Q² per unit mass against KE ~ mβ²Q²,
so the *ratio* is Q-independent at fixed β and mass ratio — the failure is not a
small-Q artifact). What would rescue the premise: a demonstration that the walk's
step is bounded by the *velocity* quantum's worth of energy (m·2γ³k per k-step,
~10⁻⁴ of the observed step) — i.e. that the minimiser can always cancel owed to that
scale; my measurements say it cannot at mass contrast. Also unmeasured by me: the
per-contact error *distribution* (I measured the cumulative walk), 3-body carry
routing chains, and any contact geometry that is not a two-body box.

## Cost of adoption, fit with PRINCIPLES

Fix directions (integrator's call, not mine): scale the carry to the pair (CM-frame
energy where the quantum is the pair's own), or gate the law's certificate on mass
contrast (equal-mass contacts are already exact to 10⁻⁶). Cost: local to
`resolve_law`, no caller changes; the ledgers stay exact either way. Fit: principle
13 "basically we don't want errors that can compound that's the goal" (CL 09-25) —
compounding is measured; principle 19 — a fix-at-the-carry signal that the carry's
representation (per-body, per-unit-mass quantum) is the wrong one; principle 2 —
error *type* (unbounded walk at pair scale) over error size.

## The ranked attacks (the lens deliverable)

1. **Contact error model at mass contrast (above) — lands.** Rung that should have
   caught it: **none exists.** r5 (dense order) was never frozen; B12 judges the
   orbit laws' energy statistics, never the contact resolver; H0173 measured the
   entropy floor, not conservation. Proposed criterion for r5: a 1000:1 pair at
   β 0.6, 200 contacts, |Σres|/KE < 1%, with the equal-mass pair (2×10⁻⁶) as the
   positive control — it would have caught this in seconds.
2. **Outcome label-invariance — survives** (0/10 pair seeds; gas permutation is
   chaos-amplified quantum noise, same class as any rounding). No rung needed; worth
   one sentence in law.md so nobody re-litigates the lower-id routing.
3. **Equal-mass contact carry — survives with numbers** (α = 0.02, 10⁻⁶ of KE): the
   dense order as built is sound for peer-to-peer battle.
4. Already-refuted premises I confirm from the wiki rather than re-measuring (the
   lens's list): two-body doll survives 2PN (ecfd); Binet rings passed r1 (H0205);
   the cycle-derivative multiply-add is dead (kick-jet 6164, law.md:36) while
   representation.md:67 still states it — the doc lags the law; the orders are not
   bit-identical at the seam (redteam-8398); the view has no time-transfer law
   (ace6, 5977); undisturbed cost ≈ 0 is real but the view, not the orbits, is the
   frame constraint (f22e).

## The lens

A premise red-team overweights the exotic (a 1000:1 relativistic pair) — I ran the
slow control to price that bias: the mechanism is the same at β 0.03, just 20×
slower, so this is not an exotic-only failure; but the player-visible horizon (hours
of battle at real contact rates, not stress scale) is the honest unit, and I did not
measure contact rates in game-seconds. I also nearly froze kill bars on the diluted
mixture (the gas) instead of the phenomenon (the pair) — pre-registration design,
not measurement, was my weakest link this run.
