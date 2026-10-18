# Dossier — 20261018-1237-components-271c

## Claim

The compile node's two `isqrt` implementations — the last unpriced arithmetic slices of
read-stream open direction 2 — are now priced with a bit-identical replacement: a
seed-plus-single-hardware-division Newton (u128) and an f64-seeded corrected sqrt (u64)
cut the shipped compile **−2.6% to −13.0% in situ across every key class** (best on the
eccentric strong keys the rebind population rides), are **bit-identical on every
instrument** (3×10⁶ fuzz operands, 0 mismatches; 34 compile hashes, all MATCH; 75 crate
tests green), and with them **no bit-exact arithmetic lever above ~13% remains in the
node** — the compile's real levers stay structural (0355's class memo, a law change) or
node-count (a law change), never arithmetic.

## Bottleneck

The board's #3 (the kick): the rebind is compile-bound (84–87%, a765), the compile is
92.3% shared quadrature (0355), and the node's slices were: division — dead, 0–15% by
load (d4ce, this morning); `isqrt` — unpriced (this run); cos/multiply-chain — law-owned
bits (the nested-floored polynomial's value IS the law; any re-evaluation changes bits).
Expected gain: single-digit to ~10% of compile = single-digit % of the kick (compile is
49% of the fit stage sum on belt keys, d399). What it deletes: nothing structural — it is
an exactness-preserving cleanup of the node's innermost arithmetic, one step on the floor
ladder, closing od 2's arithmetic half.

## Evidence (Linux/x86, i7-4790, load 0.6–2.6 recorded in every log; orders of magnitude)

Instrument: `crates/space/examples/isqrtbench.rs` + the `work/patch.diff` arm
(`num::isqrt_mul` u128 = f64 seed + 2 Newton steps each with ONE hardware `div_word`
(the quotient provably fits u64 for every x < 2¹²⁸; x ≥ (2⁶⁴−1)² answered exactly) +
bounded exact floor correction; `num::isqrt_u64_mul` = f64 seed + bounded correction;
both switched at runtime by `set_isqrt_fast`, interleaved A/B/A pairs, 9 rounds,
medians; census counters inert unless enabled).

- **Bit-identity (control, both sides):** 3×10⁶ fuzz operands (10⁶ random u128, 10⁶
  gate-shaped `denominator<<62`, 10⁶ random u64): 0 mismatches, both arms, main and
  held-out ladders. 34/34 compile hashes (knot psis, period, advance, proper period,
  crossing times, 8-phase states) identical. `cargo test --release -p emergent-space`:
  75 passed, both arms. Refusals identical (held-out p=7, e=0.52 refused NoBoundOrbit in
  both arms — key validity never touches isqrt).
- **Isolated slice prices (2×10⁵ calls, black-box summed):** wide `num::isqrt` 110.6 →
  80.6 ns (−27%); **std `u64::isqrt` 27.8 → 10.0 ns (−64%)** — std's own Newton pays u64
  divisions per node on every `word_root = true` key.
- **In situ, interleaved pairs (medians of 9):** weak belt (the flight's belt compile
  path — census: `fast=false, word_root=false` at q ≤ 2⁻¹⁸, i.e. the weak branch, knots
  6–21): −2.6/−6.4/−3.4%. Planet/strong `word_root=true` (e ≤ 0.9): −8.1 to **−10.5%**.
  `word_root=false` band (delta ∈ [2.3×10⁻¹⁰, ¼], p ∈ (6+2e, ~8+2.7e)): −8.1 to −8.4%.
  **Held-out near-separatrix sweep (e 0.56–0.96, not tuned on): −10.5% to −13.0%.**
- **Census (new, read once before timing):** the wide isqrt fires per node on the
  `word_root=false` band (164–498 calls/compile, ~2.05 Newton iterations each) and
  per compile (5–24 calls) everywhere else including the weak belt; the u64 isqrt fires
  per node on every fast `word_root=true` key. Per-compile wide-call counts grow with
  crossings (cut() → ratio_sqrt → isqrt), not just knots.

Commands (each ≤ 60 s, from the repo root with the patch applied):

```
cargo build --release -p emergent-space --example isqrtbench
/home/glmlab/lab-target-3/release/examples/isqrtbench all      # isolated + census + exact + pairs
/home/glmlab/lab-target-3/release/examples/isqrtbench heldout  # held-out sweep + belt2
cargo test --release -p emergent-space
```

Raw logs: `bench-main.txt`, `bench-heldout.txt` (this folder).

## Predictions (predictions.md, written before the decisive run)

- **P1 held** (0 mismatches everywhere; all hashes MATCH).
- **P2 half-held:** belt keys are indeed ~100% off the fast path — but the census
  surprised: the belt is `fast=false` via the **weak branch** (compactness zeroed at
  q ≤ 2⁻¹⁸), the cheapest node of all (no per-node isqrt); the wide per-node isqrt band
  is the razor-thin p ∈ (6+2e, ~8+2.7e) window, which my first ladder missed by an
  eccentricity-scale slip (millionths) — caught by the census, fixed, disclosed.
- **P3 failed as predicted-number, kill not met:** predicted ≥25% on `word_root=false`
  rungs; measured −8.1 to −8.4% there (the isolated −27% is two-thirds absorbed by OoO,
  generalising d4ce's lesson) — BUT the held-out eccentric rungs measure −10.5 to
  −13.0%, above my own 10% kill bar, so od 2's arithmetic half does NOT close at "no
  lever ≥ 10%"; it closes at "no lever above ~13%, one adoptable cleanup at −3 to −13%".
- **P4 held:** belt-class ≤ 8% (−2.6 to −6.4% measured; my own alternative reading
  "std u64 isqrt ≥ 20% of the belt node" is dead — the belt node has no isqrt at all).

## What would make it wrong

The in-situ percentages are load- and machine-dependent (Haswell x86 here; the M1 has no
hardware 64÷64 as cheap and a different div profile — the integrator re-measures). If
`div_word`'s precondition proof is wrong for some operand, exactness would fail loudly
(fuzz + hashes + tests all watch it). The census's node classification could misattribute
if `OrbitShape::new`'s gates change; the gates are quoted in the patch. The claim does
NOT extend to the slow `node()` path (delta < 2³⁰, the plunge-adjacent domain): those
keys are unreachable through `bound(p, e)` at integer p (they need
`from_invariants`-class construction) and were not timed — named as the instrument's
one unflown corner.

## Cost of adoption

~60 lines in `num.rs` (two functions + switch), two call-site lines in `orbit.rs`
(`fast_quad`'s `word_root` branch), no law change, no digest change, no memory change.
Fit with PRINCIPLES: #16 "it's about what's cheapest to compute" and #26 "keep doing
those smarter math and old tricks" (f64-seeded exact sqrt is the compute-starved
practitioner's move); #2 "exact means deterministic and reproducible" — exactness is
the certificate, and it is bit-level. The lens's floor reading: with division (0–15%)
and isqrt (≤13%) priced, the node sits at roughly 2–3× its pure-ALU floor, and the
remaining gap is dependency-chain and the law-owned cos — i.e. the node's idiot index is
now single-digit, and the compile's 10× levers are representational, not arithmetic.

## The lens

First-principles, one component at a time: it prices and stops; it does not chase the
structural levers it names (class memo, node count) because those are law changes, the
integrator's to decide. Blind spot measured: the neighbours — the read half (e106's
regression) and the memory half (the knot table this arm leaves untouched) are where the
compile's real 10× still lives; this run's −3 to −13% is the honest ceiling of the
bit-exact arithmetic lane.
