# Run 20261013-1145-components-9384 — the isqrt primitive, taken to its floor's edge

- **Claim:** the law's exact `isqrt(u128)` primitive ran ~5–9× above its arithmetic floor; a bit-identical replacement (f64 seed + one Newton division + exact square fix-ups) cuts the primitive 96.5→54.2 ns (1.78×) and the real `Orbit::compile` path −9.5% (58.0→52.5 µs, A/B/A), with the compile digest, all 70 frozen-oracle tests and the plane digest bit-identical.
- **Lens:** components — one component (the integer primitive `isqrt`, `crates/space/src/num.rs`), its floor, its idiot index, a design closer to the floor.

## Bottleneck

`kick-jet` open direction 1a (7d2b): the retired jet's replacement is the exact recompile, and the ~320 ns node holds `isqrt` at ~30% (7d2b) / 6–14% of the compile (c914). The lever was named ("a bit-identical Newton isqrt(u128)") and unmeasured. Every call site is exact-integer (`isqrt = floor(sqrt(x))` is a unique integer), so a faster exact implementation is bit-identical by construction — the cheapest class of cut: no recertification, no law change.

## The component, its floor, its idiot index

- **Requirement:** `isqrt` = exact floor of the square root, an integer function of an integer input (num.rs's own header: "any faster implementation must return the same bits"). It serves the compile's `fast_quad` root (`isqrt((denominator as u128) << 62)`, per node), `ratio_sqrt` (per `cut()` crossing), and the fit-time isqrts in `lib.rs`.
- **Floor:** one correctly-rounded f64 sqrt (≈53-bit seed), one division-equivalent or a handful of widening multiplies for refinement, and ≤3 u64×u64→u128 square comparisons to pin the exact floor: **≈10–25 ns** on this box. No information-theoretic slack: the output is 64 bits and the input 128; the arithmetic above is what any exact method must at least smell like.
- **Shipped:** u64-Newton seed (itself division-based) plus 2–3 soft u128/u128 divisions (`__udivti3`, ~30 ns each per c914) in the decreasing-Newton loop. Measured **96.3–98.7 ns/op** on the compile's own operand distributions.
- **Idiot index: ~4–9×.** The new design sits at **54.2 ns = ~2–5× above floor** (the residue is the one remaining soft division plus the u128→f64 conversion).

## Evidence (all from `regen.sh`, ~6 min)

1. **Exactness:** 24,000,000 fuzz cases over 8 operand distributions (uniform, the two real call-site shapes `d<<62` and `num·den`, perfect squares, squares±1, small, powers of two±1) plus 15 edge corners including `u128::MAX`: **0 mismatches** vs the shipped algorithm (itself cross-checked against an independent slow reference). `isqrt` is a unique integer, so identical outputs = identical canonical bits everywhere.
2. **Primitive cost** (mixed domain, 5 M ops, checksummed): shipped 96.5 ns → B (f64 seed + `div_word` 128/64) 57.9 ns → **C (f64 seed + one soft-div Newton + fix-ups) 54.2 ns**. C wins because two u64 hardware divisions (in `div_word`) cost more than one `__udivti3` here; the f64 seed lands ~2^10 from the root at full width (histogram in the harness) and the single Newton step + ≤3 fix-up squares close it — 54 ns/op is itself proof the fix-ups are short.
3. **Real compile path A/B/A** (`isqrt_sweep`, 65 bound keys p∈{4..1024 M}, e∈{0..0.99}, best of 40): base 58.0, 58.0 µs/compile → patched 52.5, 52.5 µs/compile = **−9.5% (1.105×)**, sweep digest `7ea39076…` identical in all arms.
4. **Frozen oracles:** `cargo test --release -p emergent-space`: 70/70 pass (unit, api, clock, envelope, events, kerr, light, near_circular, plunge).
5. **Whole engine:** plane settle digest (`tail 10 100 1 48`) `f5b8cd23…d7ce` **bit-identical** base/patched/patched-again.

## Predictions (predictions.md, written before the wiring)

Held: bit-identity (3, 4, 5 — all confirmed exactly); the fix-up loops short (6 — confirmed implicitly: 54 ns/op bounds them at ≤ a few). **Missed low:** I predicted a 4–9% compile drop off c914's 6–14% share; measured −9.5%, i.e. the true share on this key grid is ~17% — between c914's compile-level split and 7d2b's 30%-of-node (these keys are the compile-heavy e≤0.99 shapes). **Not measured:** kerr compile timing (prediction 2) — the kerr oracle tests pass bit-for-bit, but the kerr A/B was not run; it is one `regen.sh`-style command away.

## What would make it wrong, adoption cost, fit

- **Wrong if** the f64 seed were not correctly rounded on some target (IEEE guarantees it on x86-64 and the M1) — and even then the fix-up loops restore exactness, degrading only speed. The M1 re-measure is the integrator's (cloud timings are orders of magnitude only).
- **Adoption cost:** a 16-line body swap in `num.rs`, no signature or call-site change, no law or gate change; `div_word` and everything else untouched. It lands on every isqrt caller at once (compile, fit, kerr, plunge).
- **Fit:** "The cheapest compute is compute not done. Delete before optimizing" (P1) and "it's just what's the biggest quantization… no it's about what's cheapest to compute" (OC#38): same bits, fewer cycles, no new parts. The kick-level yield is honest but modest: with compile ≈ half the rebind and rebind ≈ half-to-84% of a kick, −9.5% on compiles is **≈−3–5% on a plane kick** — this closes the named isqrt lever, it does not move the 1,400–1,800× idiot index by itself (that is panel count, a law question).
- **The lens's blind spot (checked):** a local optimum can move cost to a neighbour — it cannot here: the primitive's outputs are bit-identical, so no neighbour sees any difference at all.

## Open (for the next run)

The mul-only reciprocal-sqrt Newton (no division at all: one f64 seed, one u128 fixed-point iteration of ~3 widening multiplies, mulhi extract, fix-ups) is the design at the ~15–25 ns floor; untested here for time. Divisions remain at their x86 floor (c914), so removing this last division is the only arithmetic left in the node before `cos`/`isqrt` panel-count questions.

Machine: shared GitHub runner, Linux x86-64, i7-4790-class, 8 vCPU; load and neighbours recorded by `regen.sh` (`uptime`). Orders of magnitude only.
