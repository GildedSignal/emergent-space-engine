# Dossier — 20261013-2005-second-20261013-1915-system-81ca-6701 (second author on 81ca)

## Claim

**The checker-named gold experiment is run and splits in two.** The whole compile
**is** three certified-exact integer Carlson channels: the shipped walk's advance,
period and proper period all reduce to one basis `K = RF(0,1−m,1)`,
`E = K − (m/3)·RD(0,1−m,1)`, `Π(ν|m) = K + (ν/3)·RJ(0,1−m,1,1−ν)` in the A-frame
(`m = 4q(1−k)/A ∈ (0,1)`, `ν = −2(1−k)/(2k−1) < 0`, `ν_h = 4q(1−k)/H1 ∈ (0,1)`),
with the squared x-factor carried by the classical
`∂Π/∂ν = [νE+(m−ν)K−(m−ν²)Π]/(2ν(m−ν)(ν−1))`; the **integer RF/RD/RJ port is built
on Carlson's published algorithms verbatim** (arXiv:math/9409227 eqs 2.7, 2.23, 2.31:
floor-root duplication, his stop rules, his series tails in exact Q62 arithmetic) and
matches the shipped walk **to the walk's own channel quanta on all three channels at
once — worst 5.3e-10 (adv), 3.7e-10 (t), 3.8e-10 (τ) over the 170-key grid, 6.2e-9 /
4.9e-9 (t, τ) on the attack keys** — at 18–40 µs flat (O(1) in e), against the shipped
compile's 5.8–374 µs. **But the readout's crossing table is not cheaply replaceable
per-query: one 3-channel incomplete Carlson evaluation costs 11–28 µs against the
panel table's 4.0–5.4 µs read** — the walk deletion stands on the compile side and
the memory (0.5–12 kB per shape), not on the readout.

## Bottleneck

Board #3 (the kick: 75–160 µs against a ~50 ns floor; the compile is 49–97% of every
rebind). The checker of 81ca kept it silver because only the φ channel was replaced;
this run ports RD/RJ, prices the readout, and measures the whole-compile replacement —
the exact experiment it named.

## Evidence

All numbers from `cargo test --release -p emergent-space --test carlson_compile_probe
-- --nocapture` (Linux x86 shared runner, single thread, orders of magnitude only;
regen via `regen.sh` = the probe + an independent 50-dps mpmath check of all three
channels from the raw (k, q) fields, output in `probe-out.txt`). Grid: p_slr = 12·2^j
(j = 1..16) × e ∈ {0.05…0.9, 0.99}: 170 strong keys, 6 weak controls; held-out + the
checker's attack keys: 12 more strong ((8, 0.995), (20, 0.9999), (50, 0.99999),
(7.801/7.81/7.85, 0.9), (7.01, 0.5), …). Refusals are recorded, never dropped:
(5.5, 0.9999) → `NoBoundOrbit`; (5, 0) is the k = UNIT circle branch (the shipped
compile already special-cases it in O(1); no walk to replace).

- **Three channels, exact, integers.** On every strong key the integer arm, the f64
  arm and an in-probe GL4 quadrature of the raw ψ-integrands agree with the shipped
  `advance()/period()/proper_period()` to the same level (integer = f64 = quad to the
  printed digits): grid worst 5.28e-10 / 3.73e-10 / 3.77e-10; attack worst adv
  5.82e-8 at (8, 0.995) — 81ca's known walk break, still only a φ-channel break
  (t, τ stay at 6.2e-9 / 4.9e-9 there). The mpmath arm (6 keys × 3 channels, 50 dps)
  holds ≤ 1e-12. Pre-registered bars P1–P3 all pass.
- **The port's certification** is Carlson's own theorems, not new analysis: his stop
  rules (2.17)/(2.25) at our five-variable spread 2⁻²¹–2⁻²⁰ certify relative error
  r = 4·ε⁶ ≈ 2⁻¹¹⁸ per primitive; floor rounding adds ≤ a few ulp per step; RJ's
  RC(1,1+e) corrections run as RC = RF(1,1+e,1+e) by the same certified duplication,
  with the exact short series 1 − e/3 + e²/5 below |e| ≤ 2⁻²⁴. Iterations ≤ 15
  (grid), 19 (attack); every RJ argument is pre-scaled ≤ 1 by homogeneity
  (RJ(4x,4y,4z,4p) = 8·RJ), which keeps every internal product inside u128/i128.
- **Cost (whole compile).** Mine 17.7–40 µs (one RF + one RD + two RJ + exact-integer
  tails, ~4 chains × 11–19 duplications) vs shipped `Orbit::compile` 5.8–374 µs:
  cheaper at every key with e ≳ 0.4 (9.4× at the 374 µs leaver tail (50, 0.99999);
  5.6× at e = 0.99), **2–3.4× dearer at the two cheapest keys** (p = 12, e ≤ 0.1,
  compile already 6–9 µs) — pre-registered as the expected failure in P4. The
  compile's cost stops depending on e at all: the band-cut machinery (6 → 282 knots)
  is deleted, with it 0.5–12 kB per shape (88 B × knots + crossings).
- **The readout half (the crossing table).** Correctness: the incomplete Carlson forms
  (Carlson eqs 4.5–4.7 with c = csc²φ, plus the incomplete ∂Π/∂ν) reproduce the
  shipped `at_phase` outputs at the shipped solution's own amplitude: worst rel(t)
  9.8e-9, rel(τ) 8.9e-9, rel(adv) 3.3e-8 over 90 rows. Price: one 3-channel
  incomplete evaluation = 11–28 µs (f64) vs the shipped table read `signed_state` =
  4.0–5.4 µs, and a naive bisection solve on the closed form is ~1.3 ms. **The panel
  table is an amortization of the same elliptic integrals; deleting it multiplies the
  readout cost by 3–7.** So the walk's knots/crossings have a measured, load-bearing
  role per query, and "knots and all" deletion trades compile time (won) against
  read time (lost).

## Predictions

`predictions.md` was written before the first full run. Outcome: P1 ✓ (5.3e-10),
P2 ✓, P3 ✓ (both bars: formula ≤ 1e-12 vs mpmath, integer ≤ 1e-9 vs shipped), P4 ✓
as pre-registered with the disclosed cheap-key failure (0.18–0.11× at the expensive
end, 3.38× worst at (12, 0.05)), P5 **half-failed**: correctness held (t/τ ≤ 1e-8, adv 3.3e-8) but
the per-evaluation cost prediction ≤ 10 µs was optimistic — measured 11–28 µs, and
the shipped read is 4 µs, so the crossing table is not beaten per-query. P6 ✓
(weak-branch controls: adv 1.15e-5 truncation shows; t/τ on the weak branch match at
2.5e-10 — the walk's weak t/τ are not first-order truncated, unlike its advance).
P7 ✓ (no key within 2⁻¹⁰ of the m = ν degeneracy; it sits at p_slr = 4, inside the
refused region).

## What would make it wrong

The t/τ algebra is verified three ways (mpmath 50 dps, in-probe quadrature, shipped
walk) but the closed form is only as independent as those three paths — all share the
Schwarzschild geodesic premise of the walk itself; the shipped `xtask gr-oracle`
covers bound periods only in the weak field (p ≥ 20, e ≤ 0.5), so the strong-field t
channel has no shipped independent oracle beyond these. The integer certificate is
Carlson's published per-primitive bound; the composed-channel bound (division chains,
the ∂Π/∂ν cancellation) is argued from 1-ulp-per-op, not a formal ulp calculus — the
empirical integer-equals-f64-to-the-last-printed-digit agreement is the evidence. The
readout pricing is f64-only (an integer incomplete port would be dearer still). The
k = UNIT circle branch and the passage branch are untouched. Adopting the compile
half is a law change with gates re-frozen.

## Fit with PRINCIPLES

#18 "we just need to have the right representation so that math is trivial": three
channels, one basis, cost flat in e. #1/#3: the compile's cost stops following the
eccentricity tail that drives F1's stutter. #13 "errors never compound": floor
rounding with published per-step bounds, integers deciding. #34 "the oracles are
guards, not shepherds": the negative readout finding is reported as measured, not
absorbed into the design.

## The lens

What the second-author lens may have missed: the readout pricing uses f64 Carlson and
a deliberately naive solver — a smarter amortization (a Carlson-built table at
coarser knots, or integer incomplete forms) could still beat 4 µs/query; this run
prices the naive replacement, not the best one. The cost column carries the shared
box's noise (orders of magnitude only). The RJ pre-scaling adds ~4 duplications at
the ν-pole corner; an m→1 complementary form might shave them, unpriced.
