# Dossier — 20261007-0528-second-20261007-0341-scout-9abe-67be (second author on 20261007-0341-scout-9abe)

## Claim

The scout run's cadence claim is refuted at its root: on a correctly-built
resonance lattice the impulsive kick layer is **uncertifiable near any
first-order commensurability at every cadence tried** (2:1 and 3:2, all of
centres, ±2/3 W and ±2 W edges, 3 phases, 2 horizons — 29 of 30 rows fail the
behaviour gate; 5:3 fails across the whole sweep under the relative-e gate),
the **oracle ceiling** — cheapest holding policy per row, which no real rule
can exceed — is **1.14× in tide evals and 1.24× in kicks** against the
cheapest holding fixed cadence (gate-robust: 1.05–1.18× under three gate
variants), so no frequency-derived cadence rule can reach the 4× bar; and the
original run's central evidence was an artifact: **its "2:1 resonance centre"
was never at 2:1** — a Python operator-precedence bug (`2**(2/3)**1.5` parses
as `2**((2/3)**1.5)`; n_per = 0.6857 instead of 0.5) put it 2.29 W off a 3:2,
its "detuning" S2d was 0.98 W off a *different* resonance (the true 2:1), and
the checker's "2:1 vs 3:2 inversion" contrasted two mislabelled positions of
two different resonances. What survives is the selector: read the
commensurability from the compiled frequencies and hand the body to the
resonant representation (law.md's doll); cadence is not the lever near
resonance, and away from it the cheapest certified cadence is already fixed
and coarse.

## Bottleneck

Board focus #1 (fewer kicks per orbit at the same behaviour). The scout run
claimed 2.5–4 kicks/orbit vs fixed's 8–32; the checker named the gold
experiment: a resonance lattice, cadence chosen from compiled frequencies,
cost in tide evals, gate = held behaviours at ≥ 4× total cut. This run does
that experiment and kills the claim: the achievable cut on certifiable scenes
is ~1.1–1.2× in evals, and the resonant part of phase space — where a belt's
interesting dynamics live — is not cadence-certifiable at all.

## Evidence

All in `work/` on this Linux runner (8 vCPU, load 0.4–1.3, pure Python,
orders of magnitude only; every command ≤ 80 s).

**The record regenerates from shipped code.** `python3 cadence.py
S2c,S2d,S2c2,S3,S4` (7.6 s) reproduces the stored JSON field for field — the
only diffs are `wall` times and 35 nan-vs-nan pairs from unbound S4 rows,
exactly as the first checker found. My instrumented copy (`lattice.py`,
layer2) matches the shipped layer bit-identically on the precedence-clean
scenes S2d and S3 (10 policies × 2 scenes, every kpo/epump/da_rel equal to 6
decimals).

**The scene bug (measured).** Shipped S2c: n_per = 0.68571, intended 0.5.
Distances in half-widths (W = 2.5 μ^(2/3) = 0.025): to 3:2 −2.29 W, to 2:1
−14.9 W. Shipped S2d ("2/3 W detuning of the centre"): n_per = 0.48773 →
+0.98 W from the true 2:1, and 7.9 W away from S2c in n_per — the shipped
"centre vs detuned" pair was really "3:2-edge vs 2:1-edge". S2c2 inherits the
bug. The shipped numbers still describe real physics of those (mislabeled)
scenes — consistent with my lattice, where first-order rows within ±2 W all
fail (best S2c-class epump 1.55, all da_rel ≥ 0.04, exactly the shipped
pattern).

**The lattice (decisive, pre-registered in `predictions.md` before the run).**
`python3 lattice.py full` (79.4 s) → `out_full.json`: 4 resonances (2:1, 3:2
first-order; 3:1, 5:3 second-order) × 5 detunings (0, ±2/3 W, ±2 W,
parametrized so Δ₁/W = |δ| exactly) × 3 phases (0, π/4, π/2) + S3 + S1; 14
policies (FIXED-2..64, AVG, DEPH-2.5, GOLDEN, TRIG-0.25/0.5, TRIG2-0.125/0.5/2.0,
grid-snapped TRIG2G-2.0); horizons 100 and 200 orbits (30/60 for S1); truth
RK4 @1024 steps/orbit. Gate: epump ∈ [0.8, 1.25] (B17) and da_rel ≤ 0.05 at
both horizons. Cost = tide evals/orbit (1/kick fixed, 3/kick trigger).

- **First-order (30 rows): 29 fail for every policy** (one fluke: 21_d+2.000
  phase π/2, FIXED-64). At the 2:1 centre, truth librates e 0.02→0.100→0.031;
  best policy FIXED-64 reaches epump 1.34, da 0.025. At the 3:2 centre
  FIXED-64 gives epump 0.12, da 0.053. The violent zone reaches ±2 W.
- **5:3 (15 rows): 0 certified.** Truth's e oscillates through small values
  (0.02→0.004→0.016), so the relative band demands absolute-e accuracy no
  cheap cadence delivers; under an absolute-e gate (de ≤ 0.01) most still
  fail on da. **3:1** is the only benign structure: off-centre rows (±2/3 W,
  ±2 W) hold with FIXED-16 (12 rows), the centre holds only via a trigger on
  2 of 3 phases.
- **Oracle bound:** over the 17 certifiable rows, baseline (cheapest holding
  FIXED) 466.8 evals/orbit; per-row oracle (cheapest holding policy of any
  kind) 409.6 → **1.14× in evals, 1.24× in kicks**. Oracle winners:
  FIXED-16 (6 rows), TRIG-0.25 (5), FIXED-64 (4), TRIG2-0.5 (1), AVG (1, on
  S3 at 1 eval/orbit). No trigger, de-phased, golden or averaged policy
  holds across all certifiable rows (best: TRIG-0.25, 7/17). TRIG2G-2.0
  (the checker's grid-snap variant) holds nowhere.
- **Gate sensitivity** (`python3 gatesens.py`): pre-registered → 17/62
  certifiable, 1/30 first-order, cut 1.14×; absolute-e (de ≤ 0.01) → 25/62,
  2/30, 1.18×; loose (de ≤ 0.02, da ≤ 0.10) → 38/62, 8/30, 1.05×. The kill
  is not an artifact of my gate; and loosening the gate certifies rows by
  making *fixed* cadences cheaper faster than any alternative.
- **S1 (quiet LEO):** under the two-horizon gate only FIXED-64 is certified;
  TRIG2-0.125 (9.5 kpo, 28.5 evals/orbit) fails the epump band. Even the
  quiet-scene cut does not survive the eval accounting.

**Commands.** `python3 cadence.py S2c,S2d,S2c2,S3,S4` (7.6 s);
`python3 lattice.py full` (79 s — over the 60 s guide, split per resonance if
needed); `python3 analyze.py out_full.json` (<1 s); `python3 gatesens.py`
(<1 s); `python3 lattice.py pilot` (1.4 s, the 2:1-centre pilot).

## Predictions (`predictions.md`, written before `lattice.py full`)

- P1 (nothing holds at first-order centres) — **held**, and stronger: the
  whole ±2 W sweep fails.
- P2 (edges ±2/3 W uncertified) — **held** (12/12 rows fail).
- P3 (second-order benign, de-phased wins at < 4×) — **half wrong,
  informatively**: 3:1 off-centre behaves as predicted (FIXED-16 holds,
  TRIG-0.25 cuts 16.4→8.4 evals = 1.95×); 3:1 centre and all of 5:3 are
  uncertified. "Second-order = weak" is false for 5:3 at μ = 1e-3, e0 = 0.02.
- P4 (far detuning quiet) — **wrong for 5:3 and first-order ±2 W**, right for
  3:1; the < 4× conclusion held everywhere.
- P5 (global: no ≥ 4×, trigger killed as a cadence law, selector survives) —
  **held** with the oracle bound making it a ceiling, not just a measurement.
- P6 (the inversion dissolves; it was the mislabeled scene) — **held**.
- P7 (S1: no eval cut, TRIG2-0.125 out of band) — **held**.

## What would make it wrong, cost, fit

Wrong if: (i) the engine's per-kick cost is so window-setup-dominated that
kicks are the only unit — the kill still holds (oracle 1.24× in kicks on the
mixed set); only quiet-only workloads see the trigger's 2–6× kick cut, and
those are the scenes where the compiled average already wins (S3: AVG holds
at 1 eval/orbit); (ii) μ is much smaller — W ∝ μ^(2/3), so at real-belt mass
ratios (1e-5–1e-7) the uncertified zones shrink 100–1000× in frequency and
the certified region dominates; this run is measured at the lab's standard
μ = 1e-3 and says nothing about the zone scaling, only that inside the zones
cadence is dead; (iii) the resonant doll certifies the zones cheaply — that
is the selector's handoff, outside this layer. Adoption cost of the verdict:
zero — nothing is built; the design consequence is to stop looking for a
cadence law near commensurabilities (read them from the compiled
frequencies, as law.md already says) and to count costs in evals, where the
trigger's float-harness 3-evals-per-kick overhead must be re-derived in the
integer engine (one compare) before any kick-cut claim is quoted again. Fit:
principle 9 — this failed configuration (trigger as cadence law) is killed,
not the method; principle 22 — "the simulation tells us what's next" survives
as the frequency selector, which is exactly what the compiled frequencies
are for; principle 13 — near resonance the impulsive layer's error is
coherent and structural, the compounding the run's own P2 falsification
pointed at; principle 2 — the gates judge behaviours (e-ratio, a-drift), not
trajectory identity.

## The lens (what this second-author lens may have missed)

I inherited the checker's adversarial frame, which defined "the inversion" I
then dissolved; a fresh frame might have asked for μ- and e0-scaling of the
violent zones instead of one working point (all resonant scenes share
e0 = 0.02, single perturber, circular — 5:3 is an e-type resonance and may be
tame at other e0). The float harness cannot speak for the integer engine's
re-anchoring or for ensembles beyond 3 phases × 2 horizons; S4-class chaotic
scenes remain outside the gate. The oracle bound is computed over rows where
some FIXED holds, which biases the certified set toward fixed-friendly rows —
but that is also the honest definition of "certifiable by this layer at all".
