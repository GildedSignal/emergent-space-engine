# Dossier — run 20261007-2344-taleb-6f01 (lens: Taleb)

## Claim

The phase-rank co-orbital certificate (gold 20261006-0346-taleb-09b5: "every real
encounter lies within partner rank 4 along the orbit") is safe only while the formation's
scatter in rank units, S = N·Δ/2π, stays below k — and S grows with fleet size at fixed
scatter, so at the 10⁶ scale the certificate was built for, mean-anomaly rank silently
drops 90–97% of contacting pairs under any realistic formation spread (even Δe = 10⁻⁴),
true-longitude rank survives static orientation but cracks the same way once the
epicyclic wiggle e·Δϖ or window drift Δn·W reaches rank scale, and both failures are
invisible to period/phase-density triggers — the gate must be the Binet-cluster extent
times N/2π (or the game's own knowledge that a fleet is law-maintained in lockstep).

## Bottleneck

The board's top scaling risk ("Candidate work at scale: co-orbital concentration (fleets)
makes the pairwise tier miss contacts and go quadratic; work must track real encounters")
was answered by the gold's phase-neighbour tier, and the build `b-coorbital-cert` is in
the lab queue. This run closes a ruin path before the build ships: a tier that silently
drops contacts corrupts every downstream encounter certificate (principle 13), and the
drop is worst exactly at the motivating scale. Expected effect: the build lands with a
validity gate and a sort-key choice it would otherwise lack; no new component.

## Evidence

All from `cert.py` (this folder; numpy 1.26.4, Linux x86, 8 vCPU, load/memory in
`state.txt`). N bodies on exact Kepler orbits, GM=1, a ∈ [1, 1+10⁻⁴] (a fleet:
period-concentrated), e0 = 3×10⁻⁴ unless said, contact radius ρ = 10⁻³, window 30 orbits.
Truth contacts: λ-adjacency + dense per-pair refinement; independence check: no-λ-logic
brute force on random pair subsamples (`brute_agree: true`). Certificate: circular
partner rank at k=4, in mean-anomaly order and true-longitude order, at window open
(t=0, the scheduling decision) and at encounter. Miss = fraction of contacting pairs the
O(n·k) tier drops (event-level fractions in the JSONs; locked pairs repeat 30–61×, so
pairs are the honest unit — the memo lesson again).

Controls, both behave:

- `aligned-gold` (the gold's domain: exact shared ellipse): 149 contacts, 0 misses,
  max rank 3. Reproduced, not strawmanned.
- `wide-belt` (da=0.1, ϖ random): 100% miss — the instrument sees a broken tier.

Orientation spread D (ϖ extent at fixed e, N=300; `python3 cert.py wscan`, ~90 s):

| D (rad) | S=N·D/2π | miss_M pairs | miss_λ pairs |
|---|---|---|---|
| 0.05 | 2.4 | 0.6% | 0 |
| 0.2 | 9.5 | 23% | 0 |
| 0.5 | 24 | 72% | 0 |
| 1.0 | 48 | 87% | 0 |
| π | 150 | 95% | 0 |

λ-sort absorbs static ϖ (partners meet at equal λ); M-sort does not (partner anomaly gap
≈ Δϖ), so the gold's two readings of "along the orbit" — indistinguishable on an exactly
aligned formation — separate here, and only the λ reading survives orientation spread.

Where λ-rank breaks instead (`python3 cert.py escan`, ~8 min; the N=600 fat-e cases are
the expensive ones — per-case seconds are in each JSON line):

| case | N | miss_M pairs | miss_λ pairs |
|---|---|---|---|
| station-keeping dvec=10⁻⁴ | 300 | 90% | 1.7% (max rank 7) |
| station-keeping dvec=10⁻³ | 300 | 95% | 0 |
| station-keeping dvec=3×10⁻³ | 300 | 97% | 3% |
| e0=0.02, dvec=0.02 | 600 | 97% | 52% |
| e0=0.02, dvec=0.005 | 600 | 93% | 20% |
| e0=0.02, dvec=0.02 | 300 | 97% | 38% |

Even Δe = 10⁻⁴ (an order below the gold's own σ_e = 3×10⁻⁴) puts 90% of contacting pairs
past rank 4 in M. The λ cracks scale with N at fixed e (38% at 300, 52% at 600) and are
driven by the epicyclic λ-wiggle, which my prediction under-sized: it scales as
e·sin(Δϖ/2), not just Δe — a matched-e fleet with orientation spread still breaks λ-rank.

Scaling law (rank arithmetic — integers, not float extrapolation): partner rank ≈
N·(sort-key gap)/2π. Zero-miss domain: orientation Δϖ ≲ 2πk/N, wiggle e·Δϖ ≲ πk/N,
window drift Δn·W ≲ 2πk/N. Confirmed in N at fixed D=0.5: 57% → 72% → 87% miss_M for
N = 150 → 300 → 600. At the motivating N = 10⁶, k = 4: allowed spread ≈ 2.5×10⁻⁵ rad.
No statistical swarm holds that; only a fleet maintained on one exact ellipse by the
game's own law does — which the game knows a priori because it issued the formation.

Silence: across the whole D/dvec sweep, dn_rel is identical to 4 digits (same seeded
a-draws) and phase density is exactly N/2π, while miss goes 0.6% → 97%. Period- or
phase-density triggers are blind. The Binet-cluster radius grows monotonically through
the sweep (5×10⁻⁵ → 3.7×10⁻⁴ at fixed e; 4×10⁻⁴ → 1.2×10⁻² under station-keeping), so
N·(Binet extent)/2π is a working gate — in the representation the encounters tier
already uses (law.md: orbits as Binet points (U,V,W)).

ρ-insensitivity (D=0.5, N=300): miss_M pairs = 72/72/70% at ρ = 3×10⁻⁴/10⁻³/3×10⁻³ —
the boundary is rank geometry, not contact scale.

Rank at encounter is no certificate: miss_λ_enc = 0 in every case including wide-belt —
at the moment of contact the partners are at the same λ by definition. The scheduling
rank is the one at window open, which is what the tables above use.

Bonus for the cost model: max_events_per_pair = 30–61 in the scattered cases (librating
pairs, Δn≈0, cross alignment twice per orbit). Encounter-event counts overweight locked
pairs ~30–60×; "work per real encounter" must be counted per distinct pair or the tier's
cost model is off by 1.5 orders.

## Predictions

Written before the decisive runs (`predictions.md`), tuned only on the pilot control.
Held: every miss_M direction and rough size (0.6/23/72/87/95% pair-level vs "≈0/58/83/92/97"
predicted — the last two within 5–10 pp); λ ≈ 0 across the whole ϖ family; exact trigger
blindness; ρ-insensitivity (measured tighter than the ±5 pp I claimed); station-keeping
M-misses (predicted >50/96–98/96–98%, measured 90/95/97%); the N=600 λ-crack > 10%
(measured 52%). Missed, both reported as held-out failures: (1) D=0.2/0.5 point values
came in low — partner |Δϖ| is triangular under seeded draws and contact selection weights
small gaps, not uniform as I modelled; (2) `lamsafe-N600` predicted < 2%, measured 20% —
the λ-safety number needs the e·sin(Δϖ/2) term, so my parameterization was incomplete.
The law (S ≳ k breaks the tier) is stronger for it; my formula for S_λ was the weak part.

## What would make it wrong

- If fleets in the game are exact shared ellipses by law (spawn + station-keeping on one
  orbit), S ≈ 0 within them and the certificate is safe for exactly those — but then the
  gate is the fleet law itself, and everything not law-maintained (battle debris is still
  period-concentrated!) must route to the cone tier. A period-only trigger would route
  debris into the phase tier and drop 90%+ of its contacts.
- Kepler-only model: N-body scattering only grows Δ, so S can only grow; the boundary
  moves the unsafe way. 2D only: inclination adds a third sort-key gap of the same form;
  expected to widen S, unmeasured.
- Kill criterion (pre-registered): if miss_M had not tracked N·D/2π, or λ-miss were not
  ≈0 on the ϖ family, the safety-number law would be dead. Both held.

Cost of adoption: one gate — compute S = N·(Binet extent)/2π (plus Δn·W in rank units)
per concentrated cluster; S ≲ k → phase tier sorted by true longitude; S > k → cone tier.
Alternatively the fleet law asserts S ≈ 0 for formations it maintains. No new component;
a guard on the one being built.

Fit with PRINCIPLES: "a failed expectation is not automatically a failed method" (H0183)
— the gold's tier stands, its domain is now bounded. Principle 4: regimes chosen by
dimensionless numbers — S = N·Δ/2π is that number. Principle 9: this kills the ungated
configuration, never the certificate. Principle 22: the simulation (here, the scatter the
game itself creates) decides the tier, not a heuristic. Principle 24: the 10⁶
extrapolation is integer rank arithmetic, not a float trajectory claim.

## The lens

Taleb asks what breaks at 10×: the fix for concentration is broken by concentration — its
safety margin shrinks as 1/N with the very fleet size that justifies it, and the break is
silent under the natural trigger. What this lens may have missed: speed (the O(n·k)
constant and cone-tier costs were not measured — if the cone tier is cheap at 10⁶, the
right move is deletion of the phase tier, not gating it); 3D; and the game-design side
(whether fleets are law-maintained lockstep formations is Julien's call, not mine).
