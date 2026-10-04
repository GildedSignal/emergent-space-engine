# Dossier — the belt as a program: birth populations need no per-body memory

Run 20261004-1525-components-98bc, lens: first principles, one component at a time.
Component: population storage (`crates/shipmem`), the game's 10⁹-scale content.

## Claim

A smooth birth population (a belt: Rayleigh e, banded p, uniform angles — no majority
step, so form P rejects it today) can be carried as an exact integer program — body *i* is
a bijective counter-mix of its ordinal through dyadic quantile tables and the law's own
`Key::darwin` — which is statistically indistinguishable from the i.i.d. belt on behaviours
(KS, two-sample KS on the stored keys, nearest-neighbour encounters) and costs **0.126
bits/body at 2²⁰, 1.3×10⁻⁴ bits/body at 10⁹** where today's packed blocks cost 157.4
bits/body (19.7 GB at 10⁹, over the 8 GB machine even though the draw-entropy floor
itself, 121 bits = 15.1 GB, already does not fit).

## Bottleneck

Board focus item 5, "fitting 10⁹ in 8 GB (population programs plus scars)". The lossless
i.i.d. sample cannot fit the machine at any resolution the game could accept (121 bits at
working precision, still 72 bits at brutal player resolution = 9 GB, before tubes and
catalogues). The generator form is therefore not an optimization but the only
representation that meets the goal. Expected gain: ~3 orders of magnitude at birth
(157 → 0.13 bits/body), ~200× at 1% kick churn (157 → 0.73 bits/body). What it deletes:
the packed-block store for every population that history has not churned, and the memory
traffic of walking one (19.7 GB streamed at 10⁹ vs 16.5 KB of program).

## Evidence

Belt: Darwin p ∈ [2048, 2560)·2¹⁶ (27 bits span), e Rayleigh σ = 0.07 through a 2¹²-entry
dyadic quantile table, ω 32 bits, t_p uniform over 2⁴⁴ quanta, kind 6 bits. Draw floor
121.00 bits/body (Rng-charged, exact). All on this cloud container (Linux x86, 2 vCPU);
orders of magnitude only.

```
cargo run --release -p emergent-shipmem --example belt -- 1048576   # 21 s → belt-m20.jsonl
cargo run --release -p emergent-shipmem --example belt -- 262144    #  5 s → belt-m18.jsonl
cargo run --release -p emergent-shipmem --example belt -- 8388608   # 52 s → belt-m23.jsonl
```

- **Today (i.i.d. belt → Shelf blocks):** 157.39 bits/body (1.30× the 121-bit floor),
  bit-exact round trip (`rt_bad` 0), build 395 ns, decode 7 ns per body. Constant in n
  (157.39 at 2¹⁸, 157.37 at 2²³).
- **Program (counter-mix), same belt:** 16,456 bytes of description total. 0.126 bits/body
  at 2²⁰, 0.0157 at 2²³ (exactly ∝ 1/n), 1.3×10⁻⁴ at 10⁹. Eval 109–115 ns/body including
  `Key::darwin`; no storage read at all.
- **Scars (form P's own seal: Elias–Fano ordinals + block-coded zigzag deltas, unmodified):**
  rate 10⁻⁴ → 0.133, 10⁻³ → 0.193, 10⁻² → 0.731, 10⁻¹ → 6.07 bits/body. The program+scars
  form beats blocks at every measured churn rate (26× at 10⁻¹); a body that returns to its
  program is reabsorbed for free.
- **Fidelity of the mix (behaviours, not sample identity):** KS vs the analytic law on
  p/e/ω/t_p = 0.0009–0.0014 at 2²⁰ (critical 0.0016 at α = 0.01) and 0.0002–0.0005 at 2²³
  (critical 0.00056) — scales as 1/√n, no detectable bias. Two-sample KS on the stored
  E, L key columns vs the i.i.d. belt: ≤ 0.0016 at 2²⁰, ≤ 0.00028 at 2²³. Nearest
  neighbour in the (p, t_p) plane (the phase-space density that sets encounter rates):
  median 2.8284 = i.i.d.'s 2.8284 at 2²³; p1 both 0 (same-cell neighbours exist).
- **The rank-1 lattice killed itself** (the elegant form, measured not argued): its 1-D
  marginals are perfect (KS 0.00000) but its phase space has stripes — at 2²³ its closest
  neighbour is 3.61 cells away at the 1st percentile where the i.i.d. belt has same-cell
  neighbours, and the first lattice run panicked the 3×3-cell search with *no* neighbour
  in range. A lattice belt suppresses exactly the close encounters the game is built on.
  The counter-mix shows none of this.

## Predictions

`predictions.md` was written before the first run. Held: program ≤ 0.5 bits at 2²⁰
(0.126); ≤ 1.2 bits at 10⁻² churn (0.731); mix KS ≤ 0.002 on both key sets; two-sample KS
≤ 0.004; eval ≤ 200 ns (115); 1/n scaling (0.504 at 2¹⁸ = 4× the 2²⁰ value); blocks
round trip exact. Missed: blocks predicted ≤ 1.25× floor, measured 1.30× (codec overhead
on smooth columns — my error, not the method's). Partially held: the lattice's NN
deviation arrived in the p1 tail (4.3× suppression at 2²⁰, no-neighbour panic), not in
the median as predicted. The 2²³ run was not in the predictions and is the held-out case:
mix passed everything, lattice's kill grew with density.

## What would make it wrong

- A behaviour gate that distinguishes the mix belt from an i.i.d. belt beyond KS/NN
  (e.g. long-range correlations in conjunction sequences, r8's Diophantine structure).
  The mixer is a fixed bijection; a cryptographically strong one (Threefly/Philox, still
  O(1) integer per column) is the drop-in answer if any such gate ever fires.
- Populations defined by *history* (wrecks, defences, trade lanes) have no birth program;
  they keep needing scars or blocks — this claim covers birth populations only.
- If the engine must preserve *which* i.i.d. sample a belt is (sample identity), the
  program form is not lossless for that purpose. Nothing in the goal asks for this:
  determinism ≠ realistic trajectories (PRINCIPLES 20); behaviours over many seeds.

**Cost of adoption:** one new `Prog` variant (a per-column counter-mix key plus a
population-level quantile table, beside `Const`/`Affine`), written by the creating event
(no inference needed — the belt is program-faithful by construction), evaluated by the
existing `Program` machinery; scars unchanged, measured working today. The birth rung of
B18 should judge programs on determinism + distributional behaviours (KS/NN) + program and
scar bits, while keeping the sample-preservation floor for event-created populations —
its current "under half the floor is a failure" rule would call a 10 KB billion-body belt
a false claim.

**Fit with PRINCIPLES:** "Store the generator, not the generated" (6); "this is nowhere
near the floor on the size and information theory says so" (24); "we want determinism ≠
realistic trajectories" (20); "physics loves e while we love 2" (16, dyadic quantile
tables); every body stays real and takes part in every interaction — nothing is averaged
(the mix is a bijection: each ordinal is an individual, and history scars it as itself).

## The lens

A component lens measuring one store. It did not measure: the cost of *finding* which
ordinals a view or an event must materialize (the gather at 10⁹), scar churn under real
encounter rates rather than synthetic kicks, or the interaction of programs with the
Binet-cone encounter skin. The belt's t_p was drawn over one epoch window rather than each
body's own period; period-correct phases change no memory conclusion but would matter to
an encounter gate.
