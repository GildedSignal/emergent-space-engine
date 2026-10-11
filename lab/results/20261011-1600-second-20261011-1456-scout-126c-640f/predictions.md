# Predictions (written before the decisive run)

Second-author run on 20261011-1456-scout-126c (silver). The checker named the gold
experiment: every number regenerating from one command (`separatrix_cost()` in
`main()`, a working bound-control path), the valley rescue measured on the law's
FIXED integer cut bands (not adaptive float bisection), valley-kick cases at
δ ≤ 1e-6, and P7's true domain stated. These predictions cover exactly that work.

The fixed layout under test (the law's bands, applied to the valley):
- center η_U = η(r_U), the critical radius of the cubic (V_eff′ = 0) — a fixed
  function of (E, L) alone, no integrand probing;
- rung scale σ = |Im η*| where η* is the phase image of the complex root pair of
  the radial cubic (measured in the design probe: σ = 2.56·√δ at L̃² = 13);
- edges: a uniform base of 32 panels over the phase span, plus dyadic rungs
  η_U ± h₀·2⁻ʲ (j = 1..J, J = ⌈log₂(h₀/(σ/2))⌉) — B9-style geometric bands
  (2^(k/m), here m = 1 per octave of distance-to-barrier-top) as cuts in the
  phase, the law's own "band edges are cuts in ψ" pattern;
- R evaluated two ways: the shipped `Rfun = E² − V_eff` (cancels near the valley
  bottom, noise ~eps/δ) and the law's root-factored form
  R = (E²−1)(r−r₃)((r−a)²+b²)/r³ (no cancellation; the law factors the cubic).

## P-A — valley panels on fixed cuts (the rescue, measured properly)

Outer plunges at δ = (E²−V_max)/E² ∈ {1e-2, 1e-4, 1e-6, 1e-8, 1e-10}, turning
point to r = 3, terminal (Δφ, Δt, Δτ) vs the DOP853 oracle:
- panel counts ≈ 32, 38, 44, 52, 58 (base 32 + 2⌈log₂(h₀/(σ/2))⌉): logarithmic
  growth, ~4 panels per decade of δ; every count ≤ 64, i.e. under both the P2
  budget (96) and the bound cycle's own B9 budget (~78 at m = 16 for a
  comparable span), and below the adaptive float bisection counts
  (43/83/133/205/3765) at every δ ≤ 1e-4;
- accuracy with the root-factored R: ≤ 1e-9 relative on all three terminals at
  every δ down to 1e-10 (hard line: the P2 kill criterion, ≤ 1e-6);
- accuracy with the shipped Rfun form: equal to factored for δ ≥ 1e-6, but
  floored by cancellation below: between 1e-10 and 1e-6, growing like eps/δ
  (predict ~1e-9..1e-8 at δ = 1e-8, ~1e-7 at δ = 1e-10). This floor is an
  artifact of the float R-form, not of the layout: the law's factored R has no
  such floor.
- oracle validity: first-integral violation |ṙ² + V_eff − E²|/E² ≤ 1e-11 along
  every valley trajectory used as truth (probe measured 1.4e-13 at δ = 1e-8).

## P-B — valley kicks (P7's true domain)

A bound orbit (E² = ½(V_min+V_max)) kicked at deterministic phases
(r_k = r₂ + f·(r₃−r₂), f ∈ {0.35, 0.7}) into E²_k = V_max(1+δ),
δ ∈ {1e-4, 1e-6, 1e-8}:
- uniform 64 panels: holds at δ = 1e-4 (≤ 1e-7), fails at δ ≤ 1e-6
  (≥ 1e-3), reproducing the checker's finding — this is P7's true domain:
  uniform panels carry kicks that clear V_max by δ ≳ 1e-4 only;
- the fixed ladder at ≤ 64 panels: ≤ 1e-9 (factored R) at every δ down to
  1e-8 — the kick claim extends to the valley at the same panel budget.

## P-C — bound control regenerates

With the endpoint fixed at r_end = r₂ + 1e-9·(r₃−r₂) (a strict crossing; the
old r₂ endpoint is a tangential touch the direction-filtered event can never
fire on) and `eta_of_r` clamped at cos-domain edges:
- all three seeds (mid-field, near-V_min near-circular, near-V_max) run and
  land within the stored ballpark: ≤ 5e-8 at 8 panels, ≤ 1e-9 at 16–32
  (mid-field ~1e-12); every number written by `main()`.

## P-D — everything regenerates from one command

`python3 falsifier.py` writes every key of `metrics.json`, including the two
the checker found orphaned (`separatrix_valley_panels_to_1e-11`, unchanged
function now called from `main()`; `bound_control_apo_to_peri`, now a live
path). E1–E6 numbers are bit-identical to the stored record (their code paths
are untouched; the clamp only affects the cos branch, used by the new bound
control alone).

## Kill criteria (pre-registered)

- Fixed-ladder (factored R) terminal error > 1e-6 at any δ ≥ 1e-8 in a
  decidable case → the P2 kill extends to the law's fixed cuts: the rescue is
  refuted, and the dossier says so.
- Fixed-ladder panels > 96 at δ = 1e-8 → the rescue fails the P2 budget:
  refuted as specified (not panel-grade).
- Any valley-kick ladder case > 1e-6 at δ ≥ 1e-8 → P7's extension fails.
- Bound control still not regenerating, or any metrics key written by no
  shipped path → the record stays broken (not gold).

## What I expect to learn even if it passes

The Rfun cancellation floor is the first float measurement of a difference the
integer law should not have (factored R): if the factored-form numbers do NOT
stay clean at δ = 1e-10, the floor is in the layout or the parametrization,
not in R's form — that would weaken the "no such floor in integer arithmetic"
claim and I would report it as such.
