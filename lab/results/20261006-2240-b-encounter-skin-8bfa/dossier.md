# Dossier — 20261006-2240-b-encounter-skin-8bfa (the slack skin, a directed build)

## Claim

The slack skin is now **in `crates/encounters`** (`src/skin.rs`, library + tests + a `skin`
measurement bin), exact against the crate's independent truth at **every** kick size the lens
named — **0 missed / 0 false across ε = 1e-8, 1e-6, 1e-4** on the belt, and on held-out ring
and fleet cases (controls 0/0 everywhere) — with setups per kick cut **8.3×** on the belt at
the plane's kick size (142.3 → 17.1) and 2.1–6.7× elsewhere; the exactness needed **two new
slack terms q-skin did not have**, and its old diagnosis of the ε = 1e-4 misses was wrong.

## Bottleneck

Board focus line 3 (encounters without work per element change). Gold 20261006-0737-components
showed per-kick cost is 92% numeric-window *setup*; the lever it named was this skin. The
adopted state: q-skin (silver) had 12.6× at ε = 1e-6 but 29 misses at ε = 1e-4 and no rule.

## Evidence (Linux x86 shared runner, 8 vCPU, load from the run's own `state` lines; commands ≤ 75 s)

All numbers regenerate from the repo with the patch applied:

```
cargo build --release -p emergent-encounters --offline
T=target/release
$T/skin belt 1e-4 0.3 4     # the case that broke q-skin: now 0/0 of 73
$T/skin belt 1e-6 0.3 4     # 0/0 of 63; setups/kick 142.3 → 17.1
$T/skin belt 1e-8 0.3 4     # 0/0 of 74
$T/skin ring 1e-4 0.3 4     # held out; 0/0 of 851
$T/skin fleet 1e-6 0.3 4    # held out; 0/0 of 1232
cargo test -p emergent-encounters   # 7 tests, 14 s debug
```

Raw lines in `results.jsonl` / `work/`. Setups per kick (always → skin): belt ε 1e-8/1e-6:
142.3 → 17.1 (8.3×); belt ε 1e-4: 142.3 → 54.2 (2.6×; the drift trigger fires 37×/kick —
at kick/s ≈ 1/4 the skin legitimately approaches always); belt ε 1e-4 at s = 16·eps_u:
→ 32.9 (4.3×, sat 0.5/kick, false candidates 10%); ring 1e-4/1e-6: 351 → 52 (6.7×); fleet:
154 → 74 (2.1×, false_cand 0.66 as in q-skin — the padded cone on clustered points, the
co-orbital certificate's territory). `always` (r8 v3's behaviour, same harness) is 0/0 on
every case: the positive control holds, so the harness is not void.

## The two new terms (the physics in this run)

Porting q-skin's skin reproduced its failure (15 misses of 73 at ε = 1e-4, N = 1500). Offset
diagnosis against the stored rotation showed every miss at s\* 2–4× beyond the widened window
on **transversal** pairs (g ~ 1e-2 ≫ drift) — not q-skin's "tangential window width":

1. **Term 3b, crossing-longitude drift.** The crossing longitude θ_c (cos(θ_c−θ₀) = −ΔU/r)
   moves by up to δ·(2/q + 1/r) rad under Binet drift δ, i.e. δ·(2/q + 1/r)·r²/√p in time;
   that shifts the window *centre*, which no old term covered (the edge term covers only the
   rotation-lattice drift l·ΔP). Both window edges and the check-interval stretch widen by
   it, capped at the arc traversal (an encounter longitude cannot leave the padded arc).
2. **Term 6, the empty certificate.** `numeric_window = None` is a *proof* of "no encounter
   at these elements" with a 0.05ρ margin and no slack; kicks at ε = 1e-4 overwhelm it (the
   last belt miss: adjacent indices 322/324, "never" proof blown between trigger resets).
   An empty cert now re-proves at the first pass after any drift — kicks land at segment
   starts, so the re-proof precedes that segment's query.

Also corrected from q-skin's design notes: the tangential width term is an *inversion*
w/(1 − 2δ/g), not a pad 1 + c·δ/g (probe in the transcript: growth 96× where the pad form
bounds 4×), saturating to a reset at 2δ/g ≥ 1/2, and it applies to Cross sections only
(co-orbital/Full pairs have g ≈ 0 by construction and would degenerate).

## Predictions (predictions.md, written before the post-fix sweep)

Held: belt 1e-4 s16 0 missed with sat > 0; belt 1e-6 0 missed with ≥ 5× cut; belt 1e-8 and
ring/fleet 0 missed everywhere; controls 0/0. **Not held:** belt 1e-8's setups/kick predicted
< 5, measured 17.1 (13.8/kick are `setup_new` — pairs flipping at the padded-cone edge on
rescan, a cost the skin does not defer); belt 1e-6/1e-8 checks/kick predicted ≤ always,
measured 1.08 vs 0.78 (widening buys exactness with ~30% more exact checks), and at ε = 1e-4
evals/kick 7160 vs always's 2850: the skin trades setup evals for check evals and wins where
setups dominated — the sparse-belt case the components gold measured, not a dense kicked
belt at the largest ε.

## Gates, both ways (the lens's named gates)

- **The crate's own tests**: before 3 passed (kepler closed forms, dioph brute force ×2);
  after **7 passed** (the 3 plus `exact_at_kick_eps_1e8/1e6/1e4`, `skin_cuts_setups_at_plane_kicks`),
  14 s in debug, each test ≪ 60 s. Falsifiability checked: with terms 3b and 6 compiled out,
  `exact_at_kick_eps_1e4` FAILS (5.1 s); restored, it passes.
- **r8's truth construction**: the skin's tests judge against conservative advancement over
  every radially overlapping pair, dense in time, phase-reanchored per segment (`truth_pair`,
  Halley states vs the method's Newton — independent solver paths). r8 v4's dip quantum is
  noted in the bin: a fixed-h flank test drops the ring's real slow encounters
  (rise ~ (v h)²/2d < δ·ρ), so the harness matches at the crate's 1e-3 tolerance instead,
  as `verify` does.
- **verify a/b/c** (the crate's self-check, 10 belts): before and after identical —
  0 missed / 0 false / 0 dup on every belt, same matched counts (`work/*verify*.jsonl`).

## What would make it wrong

The 1.1 fresh-window safety and the 1.5 edge factor remain empirically sized (q-skin's
inheritance); a workload with near-tangential Cross pairs at kick/s ≳ 1/2 is unsound by
construction (the tangency reset covers it by re-setting up, measured 0.21/kick on the belt).
The fleet's 66% false candidates is the padded cone on clustered Binet points — the
co-orbital certificate (a separate build, `b-coorbital-cert`) owns that. Cost of adoption:
one new module (649 lines with derivation comments and tests, plus a 301-line measurement bin) plus two additive fields on `Section`; the
engine's `pair_events` path is untouched (`sections` now delegates to `sections_pad(0.0)`).
Cloud timings are orders of magnitude only; the integrator re-measures on the M1.

## Fit with PRINCIPLES

"Compute only surprises" (§3): the certificate stops being rebuilt when kicks are inside its
own slack. "A fix signals the wrong representation" (§19): the two new terms are the slack
expressed in the certificate's own units (crossing geometry, None-proof), not a global s —
and q-skin's misdiagnosis is itself an example of patching at the wrong scale. "baby spartans
start small" (§10): one belt run reproduced the failure before any fix.

## The lens

The directed build asked for implementation, and implementation is what exposed the two
terms — measurement-driven, but the exactness argument in the module docs is derivation plus
empirical constants, not a proof. What the lens may have missed: no run at N > 1500 (the
10⁴ belt timing), no kappa ≠ 0.3 (kick-rate sensitivity), and the memory cost of stored
certificates (99k certs at N = 1500) is counted nowhere — that belongs to q-candidate-degree
and the 10⁹-body fit.

## Grade (self): silver-to-gold for the integrator to judge

Everything the lens named is delivered: the skin in the crate, exactness as code comments,
zero misses across ε = 1e-8 to 1e-4 against the independent truth, setups/kick measured,
gates green both ways, and the tests falsify. The step past q-skin is real: the ε = 1e-4 end
is now exact, with the rule for it in the certificate's own units. What is not yet gold on
the lab's own bar: the M1 numbers, N = 10⁴ timing, and the fleet's false-candidate width all
wait on the named sibling builds.
