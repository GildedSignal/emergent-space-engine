# The bind's floor: one of its three event readouts is dead, and it is deletable today

## Claim

Every bind in the shipped engine pays **three** full trajectory readouts of the same instant, and
**the two of them that are bit-identical (400/400, both ensembles, both seeds) include one that is
entirely dead**: `Rebinding::from_state` closes by computing `residual = Residual::between(state,
decoded_event())`, a readout whose result the universe's `bind_in` never reads (it recomputes its
own turn-based residual from its own `decode`). Skipping it on the engine's path is **bit-identical
end-to-end** (Bound digests equal on 4 ensembles; a flown plane's canonical digest and every
counter equal: 32,049 kicks / 30,757 boundaries / 905 encounters) and cuts the bind **−15 to −19%
on the belt mix** (18.5 → 15.0 µs), −7 to −14% on a held-out strong-field tail.

## Bottleneck

The kick is the scoreboard's ~10^3.3 gap (75–160 µs vs a ~50 ns floor), and after the crash-search
levers (2ae0, unmerged) the **bind is 41–65% of every event-carrying item** (ad26). This run is the
components lens on that one component: its requirement, its floor, its idiot index, and one
deletion closer to the floor. The deletion is small (−18% belt); the identity finding is the
structural result: the read the bind pays to "close" itself is the same read the engine pays again
one layer up, proven bit-for-bit — so a further deletion (reuse, not recompute) is a refactor away.

## Evidence (this box: Linux x86, shared, 8 vCPU; orders of magnitude only)

`examples/bindfloor.rs` (work/, shipped code, root-doll belt ensemble: 400 states, 0.5–8 AU,
e ≤ 0.25 biased small — the scenario's own belt mix; `Unit::ONE`, the root doll's):

| belt bind (shipped) | µs | share |
|---|---|---|
| `bind()` whole | 18.5–18.8 | 100% |
| `Orbit::compile` alone | 5.5 | 29% |
| **dead `decoded_event()`** | **3.3** | **18%** |
| fit_key + at_radius + phase (residual) | 5.0–5.3 | 27% |
| live decode (the turn's) + turn + conversions | ~4.6 | 25% |

- **Identity:** `from_state`'s `decoded_event()` ≡ `bind_in`'s `decode()` at the same instant —
  **400/400 bit-identical, worst word delta 0** — on belt and strong ensembles, both seeds
  (`Unit::ONE`; the two paths do the same arithmetic in a different order and agree at every bit).
- **A/B (work/patch.diff: `from_state_fit_only`/`ending_at_fit_only`, used by `bind_in`):**
  bind() 18.50→15.04 / 18.84→14.72 (belt, tuned seed), 18.81→15.99 / 18.84→14.57 (belt, held-out
  seed 1337) — **−15 to −23% belt**; 49.71→42.92 / 46.96→42.74 (strong tail, e 0.5–0.95, held
  out) — **−9 to −14%**. Bound digests equal in all four ensembles (regen `diff`: pairwise
  identical).
- **Flight:** `bindflight` (plane_extra, N=1000, rtf 100, canonical cut 4×10⁹ ticks, first kick
  wave): digest `f6d0ffc6…` and all counters **identical** shipped vs patched; wall 4.58→4.42 s.
- **Floor (measured primitives, this box):** Scalar mul 3.6 / div 34.1 / sqrt 99.9 ns; i128 div
  13.7 / mul 2.3 ns. The bind as a bijection (E, L: 3 mul + 1 div ≈ 45 ns; turning-point cubic
  ≈ 150–250 ns; phase inversion ≈ 250 ns; event decode ≈ 250 ns; turn+residual integers ≈ 30 ns)
  ⇒ **floor ≈ 0.5–1 µs, idiot index ≈ 19–37×** (16–32× after this deletion). The bind is NOT
  fa08's ~270×: that floor priced two integers, not the law's own exact `Scalar` arithmetic.

Reproduce: `lab/results/20261015-0250-components-d7b1/regen.sh` (builds both sides, prints both
tables, diffs the digests; ~2 min wall).

## Predictions

Written before the A/B (`predictions.md`): belt −17±2% (**held**: −18.7/−15.0); strong tail −5–10%
with the absolute dead-read growing (**held**: −6.6%, one arm −13.7%, dead read 3.32→3.46 µs);
identity 100% (**held**: 400/400 ×4); flight digest immobile (**held**). No kill criterion fired.

## What would make it wrong

The dead readout is only dead on paths that never read `Rebinding::residual` — `bind_in` provably
does not, and the flight digest is the independent check; a future caller of `from_state` on the
engine path that reads `.residual` would silently get zeros (the patch marks them ZERO/`fit_only`).
The floor is priced on `Scalar` primitives at this box's rates; on the M1 (no fast i128 divide)
the div-heavy terms move up. The identity is proven at `Unit::ONE` (the root doll — the belt, the
10⁹ target); non-unity dolls add conversions between the two paths and were not bit-compared.

## Fit with PRINCIPLES

- #1 "The cheapest compute is compute not done": a readout whose result is discarded.
- #3 "Compute only surprises": the same instant read three times is zero surprise twice.
- #13 "Errors never compound": deletion is bit-identical — the carried remainder is untouched.
- #6 "Store the generator, not the generated": the compiled table (29% of the bind) remains the
  next deletion (cd6e's closed form), and the live decode (25%) is information `at_radius` already
  computed once — the 400/400 identity is the evidence that reuse, not recompute, is available.

## The lens

First-principles, one component: the bind serves #6+#13 (state → stored generator + carried
remainder). What it may have missed (the blind spot): cost moved to neighbours is not measured
here — the deletion makes the bind cheaper but does not touch the queue, the catalogue mint, or
the read-side amortization b8fc measured; the kick's remaining walls (compile, fit_key's
divisions/isqrt, the live decode) each already have named levers in the record. This run adds the
one deletion those levers do not cover, and the floor arithmetic that sizes all of them.
