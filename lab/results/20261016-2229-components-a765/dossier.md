# The kick's floor, derived and measured: the rebind is compile-bound, and the closed-form key is exact at the law's quantum

## Claim

On the shipped representation the fired kick's rebind is **compile-bound, not fit-bound** —
`Orbit::compile`/`Passage::compile` is 85–90% of the rebind (52.6–64.8 µs of a 60–72 µs
mean rebind, three seeds), `fit_key` is 4.4 µs (6%), of which the 128-step bisection's
whole deletion buys 2.1 µs (3% of the rebind) — and a Newton-from-seed prototype
reproduces the shipped key **exactly at the law's quantum on 4,553/4,553 rebinds across
three seeds** (bit-identical 2,896; the 1,657 bit-disagreements are all sub-quantum,
`disagree_quantum = 0`), so the derived arithmetic floor of the rebind is ~6 µs
(Carlson-priced compile 2.9 + key 2.3 + tail 1.0): the shipped rebind sits ~10–12× above
its floor — not ~1,800× (b063's 42–56 ns, which prices the output bits, i.e. the write
floor) and not ~1.3× (1e74's ~26 µs, which prices the shipped jet arm's own machinery).

## Bottleneck

Board #3, "the kick: 75–160 µs against a ~50 ns floor; the cheapest exact kick on the
shipped representation." The floor in the board's headline was never derived: the record
carries three floors 460× apart (42–56 ns gold b063; ~1.5 µs silver 8c81; ~26 µs gold
1e74), each run quoting the one convenient to it. This run derives the floor term by term
from the shipped law and measures each term on the bench's own rebind population. What it
lets us delete: the priority reading "the fit is the wall" (71 runs chased the fit/jet;
the fit is 6% of the rebind on the plane population) — the wall is the cycle compile at
the plane's eccentricities, where cd6e/de99's verified Carlson closed form (≤2.9 µs,
exact to the walk's quantum) is the named replacement, ~18× cheaper than the shipped
52–65 µs compile here.

## Evidence

All numbers: `lab/results/20261016-2229-components-a765/regen.sh` (≈3 min: one build +
four bench runs <1 s each), x86 shared runner, xtask `universe --kick-bench --seed S
--rtf 100 --seconds 10`, audit behind `ES_FLOOR_AUDIT=1` (stage timings inside
`Rebinding::from_state` + a Newton prototype of `fit_key`, work/patch.diff; the clean
bench is untouched by the patch — same code path, `floor_audit::on()` false).

Run-to-run: the counters (agreement, quantum disagreements, exact-path, passages, key
census) are deterministic and identical across reruns; the stage timings move a few
tenths of a µs with box load (regen under load read fit_key 4.4–5.6, compile 52–64).

**Clean anchor (seed 1, matches the record):** kick resolver median 35.7 µs (made
bodies, n=137) / 203.3 µs (leavers, n=535); exact memo hit 0.0% (653 cycle rebinds, 653
distinct keys), 12+12-bit quantized hit 93.6% — 12db's 34.8/203.3 µs and 98% on the same
bench.
| seed | calls | fit_key | compile | tail (phase+residual+decode) | proto | rebind mean |
|---|---|---|---|---|---|---|
| 1 | 1,467 | 4.44 µs | 63.92 µs | 3.13 µs | 2.33 µs | 71.49 µs |
| 7 | 1,737 | 4.39 µs | 54.87 µs | 2.97 µs | 2.26 µs | 62.23 µs |
| 42 | 1,349 | 4.42 µs | 52.78 µs | 3.05 µs | 2.31 µs | 60.25 µs |

- compile share of the three stages: 85–90%. Passages are 55–66 per flight (~350 µs
  each, ec9d's domain) ≈ 1.3–1.6 µs of the mean; the cycle compile at the plane's e is
  the rest (~51–62 µs) — cd6e's e-monotone belt→strong curve, not c4d3's 4.4 µs belt
  keys: the plane's kicks are the strong-e tail of the compile's domain.
- fit errors 0; the exact BigInt path (`inverse::fit`) fired **0 times** in 4,553
  rebinds (it guards near-circular/near-separatrix states the fired kicks never hit);
  the circular branch 0.
- **Key agreement:** bit-identical 2,896/4,553 (63.6%); of the 1,657 disagreements,
  **all 1,657 are below the census quantum** (periapsis significand 2⁻²⁰, k mantissa
  2⁻²⁴): `disagree_quantum = 0` on every seed. Mechanism: only k is word-quantized
  (48-bit); `periapsis` carries the full 63-bit significand, so any ulp difference in the
  turning root moves the key bits — the bisection's exact-rounded root is one of many
  roots inside the same law quantum.
- The prototype (closed-form prefix + 8 Newton steps from the shipped `root_witness`
  seed, verbatim key tail) runs 2.26–2.33 µs vs fit_key's 4.4 µs: the 128-step bisection
  + witness premium is ~2.1 µs, i.e. 3% of the rebind.
- Key census: 836→811 / 961→937 / 767→744 distinct exact→2⁻²⁰-census keys: keys barely
  repeat even at the tolerance check's quantum; the reuse domain is the coarser 12+12-bit
  memo (93.6% here). The exact key's non-repetition is not "28 unbound bits" — at 2⁻²⁰
  they still do not repeat.

**The floor, term by term:** key from (x, v): 2.3 µs measured (prototype; the arithmetic
is ~30 Scalar ops + 8 Newton evaluations). Cycle compile: ≤2.9 µs at Carlson prices
(de99, verified to the walk's quantum on 29 keys; rf/rd/rj kernels 50–152 ns) vs 52–65 µs
shipped here. Tail (phase placement, residual, decode): 3.0–3.1 µs shipped, Carlson
floor lower. Reads and the write sit outside the rebind proper (5ade's belt wave: sources
23%, tau pair 15% — the tau carry is built and digest-identical). Arithmetic floor ≈
**6 µs**; shipped rebind mean 60–72 µs ⇒ **~10–12×**. b063's 42–56 ns is the write floor
(the binding's output bits: tube 16 B + residual 32 B + turn + kick record ≈ 1–2 cache
lines) — real, but it prices storage, not the law's required arithmetic. 1e74's ~26 µs
machinery floor is the jet arm's own residue (its walks), already beaten ~4× by the
Carlson-priced composition.

## Predictions

`predictions.md`, written before the decisive run. Held: 1 (compile dominates, 85–90%
vs predicted 40–70), 5 (exact BigInt path 0 < 1%), 6 (floor 6 µs, gap ~10–12×, inside
the predicted 1.5–5 µs ×(1–2) band). Half-held: 2 (search premium 48% of fit_key vs
predicted ≥60%; fit_key 6% of the rebind vs predicted 10–30%). Died as stated: 3 —
bit-level ≥99% agreement (actual 63.6%; my mechanism was wrong: periapsis is
full-precision in the key, only k is worded) — but the quantum-level claim it was aimed
at holds exactly (0/4,553 quantum disagreements); 4 — quantized keys ≪ rebinds at 2⁻²⁰
(actual 811/836: they do not repeat at the law's tolerance; the memo's reuse domain is
coarser, 12+12 bits).

## What would make it wrong

The agreement result is population-scoped: fired kicks of the plane's bench (three
seeds, 4,553 rebinds, e in the plane's band). Near-circular and near-separatrix states
were never sampled (circular branch and exact path 0 hits); there the Newton seed is
untested and the shipped code deliberately leaves to `inverse::fit` — adoption for those
regimes needs them generated and run (the branch code is shared, so the risk is the
seed, not the branch). The timing decomposition shares one thread and one box with
nothing else (clean runs, wall <1 s each); means over 1,300–1,700 calls, orders of
magnitude only — the M1 re-measures. The compile share is the plane population's; at
belt keys (c4d3: 4.4 µs) the rebind's wall moves to the tail and the reads, and the
floor gap shrinks to ~3–4×.

## Cost of adopting, and fit with PRINCIPLES

The compile term's Carlson replacement is already derived and verified (cd6e, de99);
this run supplies the missing population-level share: on the plane the compile is
85–90% of the rebind, so the composed closed-form kick (8–19 µs, cd6e) lands at the
derived floor's edge, and the "cheapest exact kick" the board asks for is the
integrator's one-step wiring, not new physics. The key-extraction deletion (bisection →
Newton) buys only 3% on the plane and is **not digest-identical** (keys move at ulp
level): it is a law change by the record's own rule (taste log, 5 Oct) unless the
rounding rule is kept — we report it as the measure of the fit's floor, not as an
adoption. "Compute only surprises" and "the cheapest compute is compute not done" point
at the compile: it rebuilds tables the lazy-retention work (b9ae) shows are read
~once per binding on this population — compile-on-read is the deletion that makes the
kick's floor the read floor.

## The lens

First-principles, one component (the rebind): requirement quoted per term; floor from
the law's own arithmetic; gap measured on shipped code. What the lens may have missed:
the audit counts the bench's replay pass and the frame's own pass in one accumulator
(the double pass is visible as repeated keys in the census, 836 distinct of 1,467 calls);
per-population medians (made vs leaver) were not separated inside the stages, and the
neighbours outside the rebind (reads, allocator) are priced from 5ade's belt wave, not
re-measured here.
