# Dossier — 20261012-0753-taleb-59d4: the train certificate's "rank ≤ 4" is a property of diffuse fleets, not a law

## Claim (one sentence)
The phase-neighbour train certificate adopted from gold `20261006-0346-taleb-09b5` ("every real
encounter lies within partner rank 4", O(n_c·k) with k≈4) is measured on an instrument and a
fleet family that both flatter it: rank-at-closest-approach hides the approach (at 200 ships in
a radially-aligned formation the entry rank into the encounter tube already exceeds 4 for
11–14% of contacts while the gold's instrument reports max 4), the invariant itself breaks at 800 ships (distance-rank max 15, 15% of contacts over 4, true-longitude rank likewise), and the
design's "sort by longitude" is unsound in mean longitude — 90–99% of contacts exceed mean-λ
rank 4 in *every* case including the gold's own control regime — so k must be sized by a
dimensionless 3D packing number with a pile-up escalation, and the sort key pinned to true
longitude, before the certificate is built (`b-coorbital-cert` is still "missing": this lands
pre-adoption).

## Bottleneck
The board's top scaling risk (candidate work must track real encounters) and HANDOFF's first
"risk to attack first" (co-orbital concentration). The gold replaced the quadratic candidate
tier with the train; if k=4 is hardcoded as adopted, the certificate *silently misses*
encounters exactly in the concentrated regime it exists for — missed contacts are the worst
error type for a game (no crash, wrong history). No 10× speed gain claimed; this is a
correctness-of-premise correction to adopted work, aimed at the freeze that follows.

## Evidence (Linux x86, 8 vCPU shared, < 300 MB, each case ≤ 141 s; all from this folder)
Reproduce: `python3 probe.py <case>` (numpy only; fleet generator matches the gold's
`fleet()` family: a ~ U(1±a_hw), e ~ Rayleigh(σ_e) capped, ϖ ~ U(ϖ₀±pom_spread), λ ~ N(λ₀,σ_λ);
ρ=1e-4; brute all-pairs truth on a common grid with motion per step ≤ 0.25ρ, vectorized
ternary refinement of t*; ranks are min over both partners).
Full logs: `run-entry.log`, `run-pileup.log`, `run-scale800.log`, `run-jam*.log`; machine-readable: `probe-*-out.json`.

1. **Control reproduces the gold** (nc=200, a_hw=1e-5, σ_λ=1e-2, σ_e=1e-3, seeds 31/32):
   90/104 contacts, distance-rank max 1, entry-rank max 2–3, over-4 = 0. The invariant holds
   in their regime with an independent harness — the finding is not an instrument dispute there.
2. **Longitudinal packing alone does NOT break distance rank** (jam ladder σ_λ ∈ {3e-3, 1e-3,
   3e-4}, σ_e=1e-3, seeds 31–33): packing Π = 2ρ·n_c/(σ_λ√2π) up to 53, yet distance-rank max
   ≤ 3. My pre-registered mechanism was falsified: contacts also need |Δr| ≲ ρ, and the
   e-spread (10ρ) radially diffuses the jam. The gold's own fleet family is protected by its
   radial spread — the invariant was never in danger from λ-tightness alone.
3. **Radially-aligned formations (a flown fleet: σ_e=3e-5, ϖ spread ±0.01) bend then break
   the invariant.** nc=200: rank-at-contact max 4–7 (5/544 over 4 at σ_λ=3e-4) — marginal;
   **entry rank max 6–9: 48/425 = 11% and 61/440 = 14% over 4 at σ_λ=1e-3 (seeds 71/72), and
   150/544 = 28% over 4 at σ_λ=3e-4 (seed 74)**. **nc=800, σ_λ=1e-3:
   distance-rank max 13–15, 581–599 of 4000 sampled ≈ 15% over 4, 76–116 over 8** (seeds
   81/82; the gold's nc=800 case was uniform-λ, never jam+scale together).
4. **The instrument gap is the general lesson**: d_min values are ~10⁻⁷–10⁻⁸ (near-exact
   coincidences), and rank-at-the-minimum counts only ships closer than that; during the
   approach through 2ρ many ships can be closer than the partner. Rank-at-contact and
   rank-at-entry coincide in diffuse fleets and decouple in piles — the gold's measured
   invariant is the flattering member of the pair (their own lesson 6, repeated one level up).
5. **Mean-longitude sort misses ~everything, including in the control regime**: mean-λ rank
   max 182–198 (nc=200) and 789–798 (nc=800), with 86–532 of the 90–544 ranked contacts at
   nc=200 and 3,970–3,979 of 4,000 at nc=800
   over 4 — the ϖ spread (±0.1, as in the gold's own generator) decouples mean from true
   longitude at contact by Δϖ. True-λ rank tracks distance-rank closely everywhere. The
   design line "sort by longitude, watch k≈4 neighbours" must be pinned to *true* longitude
   (a derived quantity), never the stored mean element.
6. **Design-scale arithmetic (computed, not run)**: rank scales ~ n_c/σ_λ at fixed radial
   alignment (200→800 at σ_λ=1e-3: 4→15). A 10⁶-ship aligned formation at σ_λ=1e-2 is ~125×
   denser still → k ~ O(10³), n_c·k ≈ 10⁹ sections × ~72 B ≈ 70 GB against 8 GB: the train
   re-ruins at exactly the concentration it was adopted for. It needs a second dimensionless
   trigger (3D packing: expected ships inside the encounter tube, 2ρ·n_local × radial
   eligibility ρ/σ_r) that escalates a dense pile to a clump/pile-up representation — the
   same move as the design's existing Binet clump trigger, one level down (self-similar, #33).

## Predictions
`predictions.md` written before the runs; an addendum before the refined runs after the ladder
falsified the first mechanism. Held: control reproduction; jam-tightness alone breaking
nothing *was* the falsifier of my own mechanism and is disclosed; mean-λ inflation (held,
stronger than predicted); k breaking at 800 with radial alignment (held; magnitudes
over-predicted 2–5×: my Π ignored radial eligibility and standing-proximity saturation —
reported as held-with-wrong-scale). Failed: absolute rank magnitudes in the addendum
(predicted 25–60 at σ_λ=3e-4/nc=200, measured 4–7; the 15%-over-4 shows only at 800).

## What would make it wrong
One ρ (1e-4), one a (=1), 2D coplanar (inclination spreads would further decouple phase from
distance, likely worsening ranks — untested), 2 orbits with a_hw=1e-5 (slow synodic sweep;
longer windows raise contact counts but ranks at entry are set by instantaneous packing),
Gaussian jams and Rayleigh e (adversarial lattices could differ), entry horizon fixed at 2ρ
(a different watch horizon shifts entry ranks by the local slope), and the 10⁶-scale claim is
extrapolated from the 200→800 scaling, not run. All headline numbers are two seeds each
(the entry-rank batch hit the shell's 240 s limit mid-run; the second seed completed into
`run-entry2.log` and confirms at 14%); the effect is far outside seed noise
but the exact rates are scenario-bound.

## Cost of adopting the correction, fit with PRINCIPLES
Nothing is added to the engine: pin the sort key to true longitude, replace constant k=4 with
k derived from the 3D packing number, and reuse the existing clump-escalation move for dense
piles. Fit: "regimes are chosen by dimensionless numbers" (#4 — k is not a constant, it is a
regime variable); "A failed experiment kills that configuration, never the method" (#9 — the
train survives, its hardcoded width dies); "Compute only surprises" (#3 — a pile is one
surprise, not n²/2 pairwise watches); "errors never compound" (#13 — a silently missed contact
is the compounding kind: the history that never gets made). The gold's own "what would make it
wrong" anticipated exactly the e-spread/one-seed-family gap; the second checker widened seeds
but not tightness-at-scale.

## The lens (what Taleb made me miss)
Concavity-hunting made me attack the mean (jam tightness) when the ruin lived in the joint
tail (tightness × radial alignment × scale) — my first mechanism died on my own control, which
is the lens working as intended but only at the second try. A speed lens would have measured
the watch's rebuild cost (the gold checker's open item) instead of its correctness; both are
now open before `b-coorbital-cert` is built. I did not test the checker's other named gap
(resonance piles, ϖ ≈ 90° crossings).
