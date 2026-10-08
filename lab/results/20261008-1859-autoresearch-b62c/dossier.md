# Dossier — 20261008-1859-autoresearch-b62c

## Claim

Per-pair window setup in the encounters crate (`crates/encounters`) is 1.4–4.3× cheaper (n = 10³–10⁵:
40.6→9.9 µs, 15.9→3.8 µs, 9.2→3.2 µs, 6.2→4.1 µs, 4.9→3.5 µs per candidate pair) with every
encounter still found (missed = 0, false = 0 on all 14 verify belts; identical `enc_per_body_orbit`
to the baseline at every scale), because the merged-arc certificate is free: the numeric hull crawl
for near-identical orbits is replaced by a closed-form superset window from the encounter's necessary
angular condition.

## Bottleneck

Board focus "candidate work must track real encounters" (top scaling risk, 5 October) and the 6 October
gold (components-4643): 92% of per-kick evals are window setup, and every kick re-pays setup. Expected
gain: ~3× on the setup term at belt scale; deletes the per-pair numeric crawl (setup evals/pair 20.3→0.05
at n = 10⁴, 123→39 at n = 10³) — compute not done, per principle 1.

## Evidence

Machine: shared 8-vCPU Linux (agonbox runner), load 0.1–1.3, timings are x86 orders of magnitude only.

```
# baseline and optimized binaries are saved in this folder (encounters-base, encounters-opt)
./encounters-base scale n          # setup_ns_per_pair per n
./encounters-opt  scale n          # same belts, same cone pairs, same hits
./encounters-base verify a|b|c|d|long   # missed/false per belt
./encounters-opt  verify a|b|c|d|long
./encounters-opt  decompose 10000  # setup split: scan/cross/wide/diophantine
./encounters-opt  census 10000     # why sections become Wide
```

- Held-out battery (b, c, d, long, scale, steady — nothing tuned on them; predictions.md written
  first): missed = 0, false = 0, truth_outside_cone = 0 on every belt; `enc_per_body_orbit` identical
  to baseline in all 9 scale cases; steady hits/body/orbit identical (0.0184670 → 0.0184670 at h=10).
- Decomposition at n = 10⁴ (baseline → final): scan 118→110 ns, cross 3342→~2030 ns, wide
  4266→20 ns, Diophantine 669 ns unchanged; setup evals/pair 20.26→0.05.
- Controls: positive — baseline and final both pass every belt (the gate passes when it should).
  Negative — the merged window shrunk 10× (lam ×0.1) yields missed = 1 (verify b, belt 1) and
  missed = 3 (verify d, mixed): the missed-counter detects an unsound merged window on the belts
  whose Wide sections carry truth encounters. (Predicted on verify c; c's merged sections carry no
  truth encounters, so the control fires on b/d instead — prediction 6's belt choice was wrong, the
  instrument is not.)

## Predictions (predictions.md vs what happened)

Held: zero misses everywhere; k=16 risk did not materialize; false ≤ 3× baseline and method_s below
baseline on 9/10 held-out belts (dense 2.33→0.64 s, hot 0.46→0.21 s); setup 2.5–4.5 µs at 3k–100k
(measured 3.5–4.1 µs). Failed, reported as failed: run_ns ≤ baseline at every n (n = 10³ +40%,
n = 3×10³ +20% at 1000-orbit horizons; better at n ≥ 10⁴) and steady at h = 1000 (7.88→12.87
events/encounter, 1.6×). Neutral at h ≤ 100 (13.17→13.31, 1.34→1.44).

## What would make it wrong

The merged window's superset proof uses |λ_true − λ_mean| ≤ 2.2e (equation of centre, safe to e ≈ 0.4),
chord ≥ r·Δθ/2, |Δn|·T ≤ 2e-3 (from merged ⇒ Δp ≤ eps·p²), all with a 1.2 margin — an error in those
bounds shows up as missed > 0 on belts with Wide-carried encounters (b/d demonstrated sensitivity).
The k=16 Wide check assumes ≤ ~1 minimum per period-bracket; a counterexample would need |Δn|·T ≳ 1
rad within a merged pair, which the eps bound excludes. The cost regression at small n + long
horizons is real: if certificates live ≥ ~1700 orbits (n = 10³) the merged change loses on the run
term; below that (and at n ≥ 10⁴, always) it wins. Break-even horizons: ~1700 (n=10³), ~3300 (n=3×10³).

## Cost of adopting

One file (`crates/encounters/src/pairs.rs`): j-grid caching in `d_of_s`, the merged-arc branch in
`arc_section`, adaptive k in `check`. Plus instrumentation (decompose/census subcommands, WIDE_CENSUS
atomics) that a checker reproduces with and can delete. No interface change; `run.sh`'s harness
untouched. The engine's encounters design inherits: merged pairs need no numeric window at setup.

## Fit with PRINCIPLES

- "The cheapest compute is compute not done. Delete before optimizing" (1): the crawl is deleted, not
  tuned — evals/pair 20.3 → 0.05.
- "Cost follows change and entropy… Nothing is evolved that can be derived when looked at" (3): the
  merged window is derived from the elements (closed form), not measured by integration.
- "It's a game. Behaviours matter… error type over error size" (2): the acceptance gate is missed = 0
  on adversarial belts, and the negative control proves the gate can fail.
- "A failed experiment kills that configuration, never the method" (9): the cap-window intermediate
  (round 2) was killed by its own measurement and replaced; the loop log keeps both.

## The lens

Autoresearch on a working artifact optimizes locally. The remaining setup is now ~60% analytic-cross
trig per section; the structural move (per-body mean-longitude tables shared across all ~870 partners,
setup O(cone_per_body) → O(1) per pair) is named in log.md but unbuilt. The lens also hides scale:
every gain here is at fixed density and µ = 1; the co-orbital gold's O(n·k) phase-neighbour certificate
is the real answer to concentrated workloads, and this patch does not touch it.
