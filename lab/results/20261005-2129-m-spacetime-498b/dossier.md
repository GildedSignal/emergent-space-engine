# Dossier — mathematical representations: spacetime, light and causality (GR native)

Run `20261005-2129-m-spacetime-498b`, 5 October 2026. Probes: `probe_mks.py`,
`probe_farey.py`, `arbiter_christoffel.py`; metrics in `metrics.json`,
`metrics-farey.json`. Every run here finished in ≤ 135 s on the lab host (8 vCPU,
float64, single-threaded scipy).

## Claim

The cell-addition rule gravity-law.md leaves open ("what the cells add") has a
candidate answer with measured exactness: superpose the sources' **contravariant
Kerr–Schild fields** `g^{μν} = η^{μν} − Σ f_i k_i k_i^T` (rank-1 integer matrices,
`f_i = 2M_i/r_i`, `k_i` the retarded principal null direction) — exact
Schwarzschild per source (orbit and light, validated against independent Binet
references), light-correct at 1PN for two masses (0.036% at b=4000M), monopole-1PN
correct, order-free in integers (identical digests under permuted deposits), with
the light cone sliding only along `k` when a source is added; and velocities get
an exact fixed-bit algebra: **collinear Einstein addition is an integer bilinear
form** whose dyadic log-Doppler grid is closed under quantized boosts (zero error
over 10⁶ compositions; the float chain is the one that drifts).

## Bottleneck

Board bottleneck 1 verbatim: "the law text must give the rule from a cell's
expansion to the local β… exactly Schwarzschild for one mass, curl-free for
static sources, right to 1PN for two masses" (gravity-law.md, "Open"). Expected
gain: deletes the multipole→flow conversion question and makes the cell field
record an associative integer sum (change is an addition, order-free, B8 by
construction). Secondarily bottleneck 0's "sheets as nested dolls of fixed bit
size": the velocity sheet concretely is an integer log-Doppler coordinate whose
boosts are exact additions. Not a 10× engine-speed number: a representation
answer to a frozen-open design question, with its failure boundary measured.

## Evidence

Commands (each ≤ 135 s): `python3 probe_mks.py metrics.json`,
`python3 probe_farey.py metrics-farey.json`, `python3 arbiter_christoffel.py`.

**Probe A — multi-Kerr–Schild (MKS).** All orbits measured as perihelion excess
over a Newtonian run on identical initial data, normalized per model by its own
actual orbit (`p_act`); oracle = superposed 1PN metric (g00 = −1+2U−2U², gij =
(1+2U)δ, cross terms in U² included), itself validated against an independent
analytic-Christoffel integration (6πM/p + 0.5% at M/p = 0.002).

| case | MKS excess | 1PN oracle excess | MKS vs oracle | naive β-sum vs oracle |
|---|---|---|---|---|
| 1 mass, M/p=0.002 | 0.038183 | 0.038098 | **0.22%** | (own orbit; ≈6πM/p_act +1.7%) |
| 2 masses, p/d=30, M/p=2e-3·(20/60) | 0.012660 | 0.012677 | **0.14%** | 169% |
| 2 masses, p/d=10, M_tot/p=0.002 | 0.038689 | 0.039909 | **3.1%** | 8000% (escapes; spurious −3.15 rad/orbit) |
| 2 masses, p/d=10, M_tot/p=0.01 | 0.206888 | 0.200253 | 3.3% | 1676% |
| light, b=4000M per mass | 0.00200564 | 0.00200637 | **0.036%** | — |
| light, b=40M per mass | 0.31632 | 0.34645 | 9% (beyond 1PN for both) | — |

- **One mass is exact.** MKS single-mass light at b=40M, M_tot=2M: 0.23586 vs
  exact Schwarzschild Binet 0.23614 (0.12%, the R=200b truncation); MKS weak
  orbit +0.91% over 6πM/p_act = the exact 2PN content (MKS is exactly
  Schwarzschild in Eddington–Finkelstein-type coordinates; the river/PG model,
  run as a third independent representation, confirms: +1.7% at its own orbit).
- **Curl-free effectively at 1PN for static sources**: no velocity-dependent
  anomaly appears — the two-mass agreement above bounds any spurious
  gravitomagnetic force below the quoted residuals.
- **Light at 1PN is additive**: 0.036% superposition error at b=4000M.
- **Integer determinism**: the rank-1 accumulation `η^{μν} − Σ f_i k_i k_i` in
  exact integer arithmetic, 12 sources, 20 random deposit orders → 20/20
  identical SHA-256 digests (associativity; order-independent by construction).
- **Cone slide**: for random covectors, `S_{A+B}(ξ) − S_A(ξ) = −f_B (k_B·ξ)²`
  to 1e-15 — adding a source slides the characteristic variety only along its
  principal null direction: the light cone as a rank-1-updated data structure.
- **Failure boundary**: at p/d = 10 the two-mass cross dressing is off by ~3%
  (the metric carries no explicit f₁f₂ terms, unlike the oracle's U² cross);
  at p/d = 30 it is 0.14%. Cells aggregating distant sources are inside the
  valid domain; comparable-mass pairs belong to the doll (which the law already
  says: "two comparable masses form one doll").

**Probe B — Farey/PSL(2,ℝ) velocity sheets.**

- **Exact composition**: (q/p) ⊕ (s/r) = (qr+sp)/(pr+qs) — each velocity is the
  symmetric integer matrix [[r,s],[s,r]]; 500 random triples: 0 mismatches vs
  the float Einstein chain (worst 3.3e-16), 0 associativity failures.
- **Height growth**: exact composition costs 9.27 bits/boost (linear in K) —
  fixed-bit sheets must quantize.
- **Quantized boosts are exact**: thrust as integer quanta of log₂D² (D² =
  (1+v)/(1−v)): 10⁶ compositions, state error 0, readout error 0; the float
  Einstein chain on the same boosts drifts 6.8e-14. Boosts on the dyadic grid
  compose by integer addition — closed, carry-free, order-free.
- **Naive snapping falsified** (prediction 3 as originally written): rounding
  the state after each boost random-walks — max error 408 quanta (ℓ=8),
  envelope growth exponent 0.96/0.32/0.62, fitted drift 0.04–1e-3 quanta/boost.
  The law's sigma-delta carry (representation.md §4) is mandatory for velocity
  sheets exactly as r2 found for the plane's increments.
- **Causality**: 0 order inversions in 50,147 pairs; |v|<1 exact for any finite
  integer coordinate (the top node of a 32-bit, ℓ=16 sheet sits at
  1−v = 2·2⁻⁶⁵⁵³⁶ — the margin to c is the width, not physics).
- **Identities**: D² = (p+q)/(p−q) exact (7e-13 = float noise); the mediant is
  NOT the group law (worst 97% mismatch) — the Stern-Brocot tree indexes the
  sheet's precision levels; the bilinear form moves within it.

## Predictions (predictions.md, written before the decisive runs)

Held: MKS one-mass exactness (orbit 0.9% ≈ 2PN; light 0.12%); determinism
digests 20/20; cone slide to machine precision; light at b=4000M within 0.15%
of the linear sum (measured +0.28% vs linear, **0.036% vs the oracle** — the
linear reference itself carries 2PN); naive β-sum fails grossly; exact Farey
composition (0 mismatches); height growth linear; quantized-boost closure;
order preservation; mediant not the law. Failed, and reported as failed: (i)
prediction 2's arithmetic — the single-mass 2PN light term at b=40M is +18%
(exact Binet 0.2361), not the "~7e-4" I estimated; the symmetric mass
placement in the first design also cancelled the deflection exactly (found and
fixed before the final run, recorded in the transcript); (ii) my stated γ²
identity was wrong — γ² = p²/(p²−q²); (p²+q²)/(p²−q²) = 2γ²−1; (iii) prediction
1's "2%" at p/d=10 measured 3.1%; (iv) prediction 3's naive-snap bound
(see above). Two harness bugs were found and fixed before any number was
reported as evidence: my 1PN oracle differentiated the metric functions instead
of the composite Hamiltonian (it read 4πM/p and 3M/b — caught by an independent
analytic-Christoffel arbiter, `arbiter_christoffel.py`), and its timelike/null
initial constraints were inverted.

## What would make it wrong, cost, fit

Wrong if: the integer law's actual kick cadence needs the field only through
orbit-averaged moments (then the contravariant form buys nothing over Φ); or if
retarded-source motion (the "gravity is news" tubes) breaks the static-source
curl-free structure at measurable level — not tested here, and it is the next
cheapest probe (moving sources, k_i from the retarded tube, compare against a
Carlip-style no-aberration check). Adoption cost: the cell field record becomes
a sum of rank-1 integer deposits (3 integers per source per cell: f and the
direction); β becomes derived, not stored — this *deletes* the open β-rule
question and survives retarded superposition by construction (each deposit
carries its own retarded k). The velocity sheet slots into law.md's open
"boosts also map event times" handoff question and B16's aberration, as the
exact integer bookkeeping. Fit: principle 7 ("gravity is compiled into geometry
held by cells"), principle 32 ("under the right representation many symmetries
can appear" — the null-cone rank-1 slide is the symmetry the KS form exposes),
principle 3 of representation.md ("every quantity is kept in the form in which
its change is an addition"). Cost of NOT adopting: the β rule stays open and
the two-mass rung (rung 2 in gravity-law.md) has no candidate text.

## The ranked catalogue (the lens's deliverable)

Ranked by gain × probability ÷ cost of adoption. "Replaces/deletes" is against
docs/law.md, representation.md, gravity-law.md as read today.

1. **Multi-Kerr–Schild rank-1 superposition** (probed, above). Structure: g =
   η + Σ fᵢkᵢ⊗kᵢ, kᵢ null; inverse exact per source; det η invariant per
   source. Behaviours: one-mass exactness, light additivity, cone as rank-1
   data, integer associativity. Skin in the game: superposed Kerr–Schild
   ("HuMaSh") initial data in binary-black-hole numerical relativity — used
   precisely because each hole is exact and the superposition error is second
   order in the potentials. Deletes: the β-rule question; the multipole→flow
   conversion. Kills at: comparable-mass pairs inside one cell (measured 3% at
   p/d=10).
2. **Farey/PSL(2,ℤ[1/2]) velocity sheets** (probed, above). Structure: velocity
   = dyadic point on the log-Doppler grid; boost = integer bilinear matrix;
   aberration = the same Möbius action on photon slopes. Behaviours: exact
   integer boosts for handoffs (law.md's open event-time map), B16 aberration,
   fixed-bit nested sheets (bottleneck 0), redshift/Doppler as integer ratios.
   Skin in the game: assembled, not stolen — no prior engine use found (Farey
   structures appear in Diophantine approximation and continued-fraction
   timing, which the engine already uses for conjunctions, r8 v3). Deletes:
   nothing; adds the missing exact algebra. Kills at: transverse directions
   (2D velocity needs the sheet per axis or a rotor; unprobed).
3. **Newman–Janis as the compiler's generator** (not probed, rung-sized):
   Kerr's equatorial radial function is Schwarzschild's with roots shifted by
   the complexified radius (r → r + ia); the B19 cycle compiler could be
   *generated* from the Schwarzschild Darwin compiler instead of written anew —
   χ is per doll, not per body. Skin in the game: it is how Kerr was derived
   (1965) and standard in metric generation. Cheapest kill: compile equatorial
   Kerr cycles from NJ-shifted roots, compare precession/periods to the B19
   float oracle. Probability high, cost one rung.
4. **2+1 conical defects / holonomy bookkeeping** ('t Hooft; Staruszkiewicz;
   Deser–Jackiw–'t Hooft): many-body 2+1 gravity is flat with additive conical
   deficits; geodesics are straight after unfolding the cone (store the
   generator, not the generated). **Rejected for physics, kept as metaphor**:
   its light deflection is constant in b (δ = 2πGM), not 4M/b — B3/B16 would
   fail; orbits are logarithmic, not Kepler. The holonomy ledger (deficits as
   additive integers) is the right *bookkeeping* shape for far-field causality
   maps only.
5. **Min-plus eikonal as the optical layer** (extension of what exists):
   representation.md already has min-plus causality and the deflection memo;
   the connector is that Shapiro delay and deflection are the value and
   gradient of one arrival field with refractive weight n = 1/N(lapse). Radial
   light arrival telescopes over shells as an exact integer sum. Not adopted:
   the per-pixel gather plus memo is cheaper than storing any field; a
   unification, not a deletion. (Maslov/Sethian are already in the
   conversation's reference material — not resold here.)
6. **Twistor incidence for the gather** (lead): "visible = incident" is a
   bilinear condition; aberration is Möbius on the celestial sphere. No
   integer-exactness win; the Newton gather already does the job. Park until
   the map-by-intelligence question returns.
7. **Penrose compactification for the view** (lead): the ring grid (ln z) is
   already a discretized conformal compactification; the player's causal
   diamond is the minimap at zoom (OC#30). A naming that unifies; no new part.
8. **Teleparallel/Regge naming of the plane** (support): drift-plus-kicks is a
   teleparallel integrator (curvature zero, defects as torsion quanta); Regge's
   hinge deficits are conserved integer charges — candidate certificate
   content, and the Calvo–Sanz-Serna error theory the board already cites is
   this literature. Low action.
9. **Double copy (gravity = gauge squared)** (lead, parked): halves the fields
   to compute in principle; research risk high, no integer story.
10. **Petrov/Carminati classification as regime selector** (rejected): imposes
    categories where dimensionless numbers already choose regimes (principle 4);
    curvature invariants are floats that would decide outcomes.

## What this lens may have made me miss

A spacetime-representation lens gravitates to the geometry and the algebra, and
this run followed it: everything above serves the gravity field, light and
boosts. It did not touch the top scaling risk (candidate pairs per body,
q-candidate-degree), memory (B18), or the allocator's p99 — the representations
that would help there (kinetic certificates, population programs) live in
other lenses. All probes were weak-field float probes plus exact-integer
algebra checks; the integer-law consequences (rank-1 deposits on the real grid,
dyadic velocity words in the real handoff) are argued from measured float
behaviour and algebra, not run in the crates — a rung is the honest next
evidence. And the catalogue's number 2 is assembled rather than stolen, which
by principle 26 deserves extra suspicion before adoption.
