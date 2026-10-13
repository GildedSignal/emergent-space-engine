# Dossier — 20261013-0350-scout-7d2b

## Claim

The reciprocal-division lever for the exact kick (kick-jet open direction 1, as named by
20261013-0236-fermi-061f) is **dead on shipped x86 for a structural reason**: the hot
sites' divisors do not repeat (measured repeat fraction 0.019 over 32,384 divisions),
the cold reciprocal costs *more* than the compiler's own `__udivti3` (40.4 vs 23.6 ns),
and division is anyway only ~29% of a compile's panel arithmetic — the compile's cost is
a three-way tie between division (29%), the u128 `isqrt` (30%) and the `cos` series
(24%), so no division-only lever can buy more than ~1.4×.

## Bottleneck

`kick-jet` direction 1 ("cheapen the exact recompile — now a pure count question ... fewer
panel evaluations per compile and fewer wide divisions per panel ... exact
division-by-multiplication with correction where divisors repeat", the page's top open
direction after 061f closed allocations and key search). Expected gain if the premise
had held: ~900 division-equivalents at ~31 ns → ~9 ns would cut a ~33 µs kick by ~60%,
2–3× on the frame-cost wall (the kick is 84.6% of kick wall, rebind 49–62%). What it
would have deleted: the `__udivti3`/Knuth division cost of the compile walk, with no law
change.

## Evidence

All numbers from this run's builds (regen.sh, ~4 min total; each stage ≤ 60 s).
Machine: the lab's Linux/x86 i7-4790-class runner, single thread; orders of magnitude
per the lab rules; the integrator re-measures on the M1.

**Table 1 — primitives (fuzz 10⁷ precondition-satisfying pairs, 0 mismatches for
every implementation against hardware `/`; max correction steps 3):**

| implementation | ns/op |
|---|---|
| u64/u64 native (control) | 7.7 |
| u128/u128 `/` (`__udivti3`) — what fast_quad already does | 23.6 |
| `div_word` schoolbook (shipped, `Scalar::div` path) | 27.8 |
| Möller–Granlund-style reciprocal, cold | 40.4 |
| reciprocal, amortized (same divisor 2²⁰×) | 8.9 |
| reciprocal, 8× repeat | 13.0 |

Sources (verified at the source): Möller & Granlund, *Improved division by invariant
integers*, IEEE TC 60(2):165–175, 2011, gmplib.org/~tege/division-paper — GMP's own;
Granlund & Montgomery, PLDI 1994; Granlund's x86 timing tables (the practitioners'
instruments). The reciprocal is my own construction (m = floor(2^127/v), q̂ from two
u128 products, correction loop) — bit-identical by construction and by fuzz, but the
mechanism and the economics are the paper's.

**Table 2 — repetition census, the structural kill (48-key exact `Orbit::compile`
sweep, p ∈ {8…8192} M × e ∈ {0…0.97}, schoolbook arm):**

| site family | calls/compile (avg) | distinct divisors | repeat fraction |
|---|---|---|---|
| `div_word` (`Scalar::div`, incl. `weak_quad`) | 26 | 196 total | 0.846 |
| u128 `/` sites (`fast_quad`: g, g1, ratio, rt) | **674** (min 89, max 1,752 across keys) | 31,776 total | **0.019** |

Divisors are functions of the node's ψ (x, √, horizon are recomputed per node), so
nothing repeats within a compile; 061f's hedge "where divisors repeat" has no purchase
on the hot path (the 0.846 in `div_word` is real but is 4% of the volume). Total
divisions ≈ 700/compile independently reproduces 061f's ~900-per-kick estimate.

**Table 3 — workload arms (same 48-key sweep, structural Eq over every knot):**
libcall mismatches **0 of 48**; the arm's attributable effect is bounded by the census
at 26 divisions × 4.2 ns ≈ **0.1 µs per compile** (invisible), and the observed sweep
wall varies 53–74 µs/compile across invocations on this shared box (one rerun printed
74.4 schoolbook vs 59.0 libcall — machine noise larger than any arm effect, disclosed;
the deterministic census is what carries the conclusion, and it reproduced bit for bit:
1,274 / 32,384 calls, repeat fractions 0.846 / 0.019 identical across runs).
Swapping `div_word`'s schoolbook for the libcall cannot move the compile because
`div_word` is 26 of ~700 divisions (≈0.7% even at 18% per-call).

**Table 4 — where a compile's node arithmetic actually goes (~169 nodes/compile,
≈320 ns/node measured; ingredient micros × per-node counts):**
4 divisions 94 ns (29%) + 1 u128 `isqrt` 96 ns (30%) + 1 `cos` 77 ns (24%) + u128
multiplies ~1.35 ns each (~5%) ≈ 282 of 320 ns. (The `word_root` branch replaces the
u128 isqrt by a u64 one for far-field shapes, so 30% is the compact-shape share.)

Commands: `bash lab/results/20261013-0350-scout-7d2b/regen.sh` (applies
work/patch.diff — the census/arm instrumentation in `num.rs`, `orbit.rs`, `lib.rs`, all
bit-preserving — then runs the three benches A–C above).

## Predictions

See predictions.md (written before the benches). P1 held (cold reciprocal 40.4 ns ≥ 25
kill line — dead); P2 held at 8.9 vs the predicted <8 (3.1×);
P3 **split**: held for the hot u128 sites (0.019 repeat) and was refuted for `div_word`
(0.846 — but irrelevant volume); P4 held (bit-identity 10⁷ fuzz + 48 compiles); P5 held
as a kill (the arm's attributable gain is ~0.2% by the census, unmeasurable under the
shared box's ±20% run-to-run spread). Pre-registered kill criteria: all confirmed dead —
this is a KILL of the *division-primitive* lever, not of the exact-recompile direction.

## What would make it wrong, adoption cost, PRINCIPLES fit

- **Wrong on other silicon.** The primitive ranking is x86-specific: on the M1, u64
  division is much faster and `__udivti3` is different code, so cold-reciprocal or
  div_word rankings could flip (measure before adopting anything). The structural facts
  — no divisor repetition, the 29/30/24 three-way split — are hardware-independent.
- **What survives for the next builder:** the compile's floor is three primitives, not
  one. A bit-identical Newton `isqrt(u128)` (u64 seed + correction; fuzz at perfect
  squares) attacks 30%; a shorter-exact or table-shared `cos` attacks 24%; only panel
  *count* (a law change) moves all three at once. The reciprocal-division code and its
  10⁷-case fuzz harness are in this run's patch if the M1 ever flips the economics.
- **Adoption cost of this result: negative** — nothing to adopt, one direction closed
  with the reason, plus the decomposition that redirects direction 1.
- PRINCIPLES: "Less is more ... The cheapest compute is compute not done" — the run
  deleted a candidate lever before anyone built it; "Iteration speed ... Run the
  simplest falsifying test first" — one standalone bench killed the premise in 5 s;
  "A failed experiment kills that configuration, never the method" — the exact
  recompile stays; only its mispriced lever dies.

## The lens

Scout read the prior art first and measured primitives before touching the shipped
code — right order for a kill, but it prices only x86 and only the compile; it did not
measure the *bind/fit* half of the kick, did not test the M1, and its key sweep is
hand-chosen (far-field-heavy) rather than the plane's real kick population — the 29/30/24
split should be re-read on a real settle before it steers a build. It also stopped
before prototyping the Newton isqrt that its own decomposition nominates.
