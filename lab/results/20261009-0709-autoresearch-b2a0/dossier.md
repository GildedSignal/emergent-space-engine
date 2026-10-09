# dossier — 20261009-0709-autoresearch-b2a0

## Claim

On the geodesic compiler's hot path (`fast_quad` in `crates/space`), replacing the four
u128/u128 software divisions per quadrature node with the crate's own exact 128/64 word
division (`div_w64`, guarded fallback) plus one algebraic identity (`a = 4k + 2x`) makes
`Orbit::compile` ~5% cheaper in total and ~9% at the median with **bit-identical outputs**
— and, more useful to the board: the measurement shows the compile's per-node cost is at
its structural floor under bit-identity, so the 10× lever for kicks is not micro-speed.

## Bottleneck

Board item "fewer kicks per orbit / cheaper events" (kicks dominate engine cost; the plane
recompiles an orbit on ~99% of kicks; H0210: kicks cost 29 µs). The compile is the kick's
inner event. Expected gain found: one order of magnitude less than hoped — **0.05–0.09×,
not 10×.** What it deletes: nothing structural; it deletes ~60% of the division
instructions on the strong-field path only.

## Evidence

All on this Linux runner (i7-4790, shared — orders of magnitude only; the M1 re-measures).

- Per-compile instrumentation (feature `profile`, removed from the final patch):
  p=2^4 M, e=0.9 → 67 band cuts (13.4 µs) + 71 panels (57.2 µs) ⇒ **quad = 93%** of
  compile, ~800 ns/panel, all `fast_quad`; e=0.97 → 96 cuts + 100 panels.
- Interleaved A/B (git stash ↔ patch; `ab.sh`):
  - tune set: A 1329.1/1328.8 k-ns → B 1262.1/1269.5 k-ns (**−4.7% total; median
    7340→6660 ns, −9%; p90 −11%**);
  - held-out set (never tuned on): A 2433.4/2379.7 → B 2260.5/2296.5 (**−5.3% total;
    median −8%**).
- Bit-identity: 64-bit fingerprints over periods, advance, crossing times, knot ψ grid and
  16 phase readouts per key — identical A↔B on both sets
  (tune `f4bd77fc76c8b072`, held-out `9356db3f24802745`).
- `cargo test -p emergent-space`: 50/50 in release **and** debug (debug exercises
  `div_word`'s precondition assertions).

Reproduce (each ≤ 60 s):

```
cd lab/results/20261009-0709-autoresearch-b2a0/bench && cargo build --release
/home/glmlab/lab-target-2/release/compile-bench tune 0.3
/home/glmlab/lab-target-2/release/compile-bench heldout 0.3
sh ../ab.sh tune      # interleaved A/B against the pristine tree
```

## Predictions (predictions.md, written before the decisive runs)

- **P1 FAILED:** predicted ≥ 25% for the word divisions on strong keys; measured ~5–9%.
  The u128/u128 divisions were not as expensive as estimated on this box (the compiler's
  `__udivti3` is already near the two-hardware-division word path).
- **P2 HELD:** cut-side changes (isqrt/ratio_sqrt/gmax word divisions) bought ≈ 0 →
  reverted; cuts are 7% and stay 7%.
- **P3 HELD:** max/median ratio 19.5× → 19.2× (within ±20%): cost tracks band count, and
  no bit-identical change touches the count.
- **P4 HELD:** fingerprints identical; the one mid-run revert that silently broke `isqrt`
  (`y <<= shift/2` dropped) was caught immediately by a changed fingerprint — the
  broken build's −30% was an artifact, disclosed here and in log.md.

## What would make it wrong

The speed claim is machine-specific (x86 division latencies; the M1's `udiv` economics
differ — the gain there must be re-measured, and could be smaller or larger). The
bit-identity claim is machine-independent and checked by fingerprint + the exact tests;
it would be wrong only if some input reaches the wrapped-`a` path (`a < 0` on null keys,
pre-existing behaviour, preserved) in a way the population and tests miss.

## Cost of adoption, and fit with PRINCIPLES

~30 lines in `crates/space/src/{num,orbit}.rs`; no API change; no new dependency; the
law id is untouched because outputs are bit-identical. Fits "the cheapest compute is
compute not done" and "cheapest arithmetic" (OC#38) — but honestly: this is polish on a
path whose cost is structural, and "polishing what may be replaced" is a named sin.
The plane's kick cost is dominated by *recompiling at all*, not by these nanoseconds.

## The lens (what it made me miss)

A local search over instructions cannot see the representation. Three structural exits
this lens cannot take: (1) exact division-by-reciprocal with correction — one
multiplication-plus-fix per node instead of four divisions, still bit-identical, but a
delicate proof and a run of its own; (2) the ~5 µs fixed cost per compile (Scalar
machinery in `Self::new`/`from_shape` at e ≈ 0) is untouched by node-level work; (3) the
real 10× is compiling less, not faster — the memo/hook story already on the board
(H0213). Grade suggestion: **lead** — real, reproduced, bit-safe, but 0.05×, not 10×;
kept as the floor measurement for this path.
