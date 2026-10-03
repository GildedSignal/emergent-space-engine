# Dossier — 20261003-1030-scout-ef10 (scout lens): symplectic correctors for fewer kicks

## Claim

On the engine's own split (exact compiled Kepler drift + tidal kicks, `docs/law.md` "Perturbed
motion"), output-only symplectic correctors (Wisdom–Holman–Tou 1996; Laskar–Robutel 2001;
as shipped in WHFast, Rein & Tamayo 2015, arXiv:1506.01084) cut the Jacobi error 6–8× at a
fixed kick count in the moderate-e regime, which converts into a solid 2× fewer kicks per
orbit at B12-flavoured gates in the strong-tide regime — not the 10× the asymptotic
literature numbers suggest, because the engine operates at coarse steps (n ≤ 64/orbit)
where the corrector series is not yet asymptotic.

## Bottleneck

Live engine question #1: "fewer kicks per orbit at the same behaviour… kicks dominate the
engine's cost" (board); handoff: "the bigger lever is fewer kicks (GLM `q-correctors`)" —
queued, never run, no H entry. Measured lever: 2× at gates, 6–8× at fixed n. What it
deletes outright: the open read-out defect "readouts between kicks carry the pending half
kick (Jacobi 6e-3)" (handoff, open issues) — that oscillation is exactly the mapping-vs-real
term a corrector removes.

## Evidence

Toy = engine structure: massless particle, exact universal-variable Kepler drift about the
dominant mass (verified 5e-15 against analytic over 200 random drifts, ±dt), kicks from a
prescribed circular secondary (m2 = 0.3 strong / 0.01 Jupiter-class, a_out = 4.5, 8.37:1),
DKD map, n kicks/orbit, 600 orbits, output each orbit. Jacobi constant of the true flow
conserved to 1e-13 over 477 orbits (RK4). Corrector = Z(a,b)=K(a)I(−b)K(−2a)I(b)K(a) with
rebound's exact coefficients (orders 3/5/7/11), applied at init and output only — zero
per-kick cost. Gates: precession within 1% of the n=128 oracle AND max |ΔC_J/C_J| ≤ 1e-4.

| case | plain n* | best corrected n* | saving | dCJ reduction at fixed n=8 |
|---|---|---|---|---|
| m2=0.3, e=0.2 | 32 | 16 (3,5,7,11) | **2×** | 6.1× |
| m2=0.3, e=0.6 | 64 | 32 | **2×** | 2.6× |
| m2=0.01, e=0.2 | 8 | 8 | 1× | 8.0× |
| m2=0.01, e=0.6 | 16 | 16 | 1× | 1.1× |
| m2=0.3, e=0.4 (held out) | 32 | 16 | **2×** | 2.1× |
| m2=0.01, e=0.4 (held out) | 8 | 8 | 1× | 1.7× |
| m2=0.01, e=0.85 (held out) | 32 | 32 | 1× | 1.0× |
| m2=0.3, e=0.85 (held out) | none ≤64 | none ≤64 | — | 1.2× |

Precession never binds at n ≥ 8 (phase-locked periapsis outputs; the plain map's
precession bias ≤ 1.4e-3 relative even at n=16). ΔC_J stays bounded everywhere
(oscillation, no secular walk: last ≪ max). Corrector cost: 4–20 sub-kicks per output;
in the engine the sub-DRIFTS are free (tubes are derived), and outputs are rare (gates,
handoffs, view), so amortized cost ≈ 0. Orders 5, 7, 11 saturate within 2× at these steps.

Commands (each ≤ 60 s): `python3 corrector_falsifier.py smoke` (1 s);
`python3 decisive.py` (26 s). Data: `results-sweep.json`, `results-heldout.json`.

## Predictions

`predictions.md` was written before the sweep. Held: P1 (precession never binds), P2 (2×
at m2=0.3), P3 (1× at m2=0.01), P4 (5–8× at fixed n, orders saturate), P7 (bounded ΔC_J).
Two honest misses: P5 claimed e=0.85/m2=0.3 would "still pass at high n" — nothing passes
at n ≤ 64 (strong pericentre tides; the corrector cannot rescue it); P6 claimed the
corrupt3 control (wrong inv sign) would be strictly worse than plain in n* — it is worse
at every fixed n but only ties in n* (its error sits between plain and the true corrector,
a silent degradation, which is itself a useful control finding: a misapplied corrector
does not blow up, it quietly stops helping).

## What would make it wrong; adoption cost; fit

Wrong if: the engine's kick layer samples the interaction other than at DKD points (the
cancellation target changes); gates tighter than ~1e-5 are imposed (then 6–8× at fixed n
is worth only ~2.5× in steps, h² scaling); kicks are not the dominant per-body cost at the
operating point. Near mean-motion resonances correctors are not expected to help at all
(the resonant term is physical first-order-in-μ structure, r4 v2's kill) — not tested
here, UNVERIFIED at source beyond WHFast's discussion.

Adoption: a stateless near-identity transform on the elements, applied when state is read
(handoffs B12, gates, view). It is the principled fix for the pending-half-kick read-out
defect, and a 2× kick cut in strong-tide regimes. Float here; an integer version on the
(E, L) fixed-point bands looks representable (coefficients 0.42…2.09 for sub-drifts,
1e-5…7e-2 for sub-kicks) — UNVERIFIED.

Principles fit: "Behaviours matter, not continuum fidelity: error type over error size"
(it removes a bounded oscillation's amplitude, asks no trajectory identity); "Compute only
surprises" (cost paid only at observation, zero per kick); "Steal what works, from skin in
the game" (planetary-mechanics integrators had exactly our cost structure).

## Sources

Verified at source: Rein & Tamayo 2015 (arXiv:1506.01084, fetched: corrector mechanism,
output-only application, order statement O(εh²)→O(h^K)+O(εh²)); rebound
`src/integrator_whfast.c` (fetched: Z composition and all coefficients used verbatim).
UNVERIFIED at source this run: Wisdom, Holman & Tou 1996; Mikkola & Palmer 2000; Laskar &
Robutel 2001 (mechanism provenance, cited via WHFast); WHFast512 (2026 AVX-512 rewrite
whose headline speedups lean on correctors); Farrès et al. 2013 (high-order comparisons).

## The lens (what scout may have missed)

The literature optimizes energy error — a proxy; I partially inherited that (my binding
gate became Jacobi amplitude, still an error-size gate in disguise; a behaviour gate on
kick-count vs precession would have been closer to the goal). Not examined: the real Rust
kick layer (29 µs/kick, rebinding costs), so the wall-clock translation of "2× fewer
kicks" is unmeasured; the toy is 2D coplanar with one prescribed secondary, not multipoles
from many sources; no resonant case (B17 territory) where the corrector must fail to help;
no M1 timing; no integer exactness. Self-grade: **silver** — real, cheap, one step from a
rung; the named gold experiment is `q-correctors` rung at coarse n with a Jacobi gate, a
strong-tide e > 0.6 case, and the resonant case planted as a must-NOT-help control.
