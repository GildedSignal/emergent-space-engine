# Dossier — 20261013-1915-system-81ca (system lens)

## Claim

The bound cycle's per-cycle advance is **one exact integer Carlson RF call on the key's
own dyadic fields** — `advance = 2·[RF(0, B, A) − π]`, `A = 1 − q(8k−2)`, `B = 1 − q(4k+2)`
(no division: RF's homogeneity absorbs the √A) — reproduced independently of
20261013-1428-scout-21ba, priced at **1.82–2.10 µs certified-exact in pure integers
(13–15 duplication steps, 3 isqrt each)** against the shipped compile's 6.2–228 µs
(**3.3×–108× cheaper per key, and O(1) in e where the walk's band cuts explode**);
and the same kernel is the missing exact per-pair precession primitive the encounters
tier's co-precessing frame and the slack skin need, at ~2 µs/tube.

## Bottleneck

The board's #3: one kick at 75–160 µs against a ~50 ns floor, of which the exact
recompile is 49–97% (kick-jet page) and the panel walk is the compile. This kernel
replaces the walk's φ channel outright and (with the twice-verified τ/t reductions,
RD/RJ family) the compile term entirely — flat in e, deleting the band-cut machinery
where it explodes (the leaver/plunge tail that drives F1's stutter). Secondarily it is
the O(1) per-pair Δφ the co-precessing sections (encounters open direction 3, 71a5)
and the skin's per-pair precession sizing (8f99, 73f0) currently approximate
linearly. Expected gain: 3–108× on the compile half now measured; the kick's
remaining floor becomes fit + readout.

## Evidence

All numbers from `cargo test --release -p emergent-space --test carlson_probe
-- --nocapture` (Linux x86 shared runner, single thread, orders of magnitude only;
regen via `regen.sh`, output in `probe-out.txt`). Grid: p_slr = 12·2^j (j = 0..16
passed only for j ≥ 1: p = 6 is inside the ISCO/plunge refusals) × e ∈ {0…0.9, 0.99};
170 strong keys (q > 2⁻¹⁸), 6 weak; 8 held-out keys listed in `predictions.md`.

- **Exactness (strong domain):** worst relerr(f64 closed form vs shipped walk) =
  **9.20e-10** over all 170 strong keys — under the walk's own Q30 output quantum
  (9.31e-10). The integer pipeline (floor-rounded duplication, stop at spread ≤ 2⁻²⁴,
  Carlson bound ≤ 10⁻¹⁵, π subtracted in integers) matches the f64 arm to better than
  1 quantum everywhere: worst rel_int = 9.20e-10 (identical worst key, (12, 0.0)).
  The (RF−π) cancellation is exact in integers — this was the one real trap (a f64
  composition costs 3.87e-7 at small advance).
- **The formula is exact, not fitted:** at (7.3, 0.05), q = 0.144: agreement 1.3e-12.
  An O(q²) error in A/B would show at the 1e-2 level there; it does not.
- **New: the walk's certificate is already broken at a shallow corner.** At the
  held-out key (8.0, 0.995) (q = 0.249, 1−m = 5.5e-3) both my arms agree with each
  other to 1e-12 but differ from the shipped walk by **3.30e-8 = 35 quanta** — the
  walk's Q30 claim fails where the kicked bodies live (median e = 0.94, kick-jet
  page). This extends 21ba's second-checker observation (walk error 6.7e-7 at
  1−m → 3.5e-9) two decades away from the separatrix.
- **Cost:** integer RF 1.82–2.10 µs flat (13 iterations typical, 15 at (8, 0.995)),
  vs compile 6.24 µs at (12, 0.0) rising to 169.8 µs at (12, 0.99) and 227.7 µs at
  (8, 0.995). Ratio: **0.30× at the cheapest key, 0.011× at e = 0.99, 0.009× at
  e = 0.995.** A f64 Carlson reference runs 0.70–2.0 µs in this probe's naive
  28-iteration form (21ba's checker measured 90–420 ns for a series-stopped one);
  the integer arm is the canonical one (floats never decide outcomes; here the Q30
  bits come from floor-rounded integers + Carlson's published spread bound).
- **Per-pair co-precession (the unification price):** one exact Δφ/cycle per tube at
  ~2 µs vs one compile per tube at 6–228 µs: a co-precessing pair update is
  **3.3×–110×** cheaper through this kernel than through recompiles — and exact,
  where the current skin sizing is linearized (8f99).
- **Weak-branch control:** relerr 3.97e-10…1.15e-5 on the 6 weak keys — the walk's
  own first-order truncation shows (it must NOT match to a quantum there, and it
  does not).

## Predictions

`predictions.md` was written before the first run (including the factor-2 RF/√A
correction — my first implementation had it wrong and the grid caught it). Outcome:
- P1 ✓ (9.20e-10 ≤ 1e-9). P2 ✓ (integer arm within 1 quantum of f64, both ≤ quantum).
- P3 **half-failed:** iterations are 13–15, not ≤ 10 (the ×4 spread decay needs 12
  steps from e₀ ≈ 1 to 2⁻²⁴); no key exceeded 15; (8, 0.995) at 15 crosses my >14
  flag — the m→1 complementary form would shave ~2 steps there, unpriced.
- P4 ✓ (0.30 ≤ 1/3 at e ≤ 0.5 everywhere; 0.011 ≤ 1/20 at e ≥ 0.99).
- P5 ✓ (weak separation 1.15e-5; some weak keys do coincide at 4e-10).
- P6 **partial:** 3.3×–110×, not ≥ 10× everywhere — the ≥10× fails only at the two
  cheapest keys (p = 12, e ≤ 0.1) where a compile is already just 6–9 µs.

## What would make it wrong

The A/B algebra is verified against the shipped walk only (no independent GR oracle
in this run beyond internal consistency: f64 and integer arms are independent
arithmetic, not independent physics). τ/t are not priced here as integers (their
reductions are verified twice in 21ba's checks; RD/RJ's integer port is the remaining
unpriced half). The readout's crossing table is still panel-built. Kerr and the
passage (unbound) branch are untouched. Adoption is a law change (the compile path
swaps, gates re-freeze); the memo's standing objection — the integer port's error
analysis — is answered for RF by construction (floor rounding + the published spread
bound), not yet for the whole three-channel compile.

## Fit with PRINCIPLES

"We just need to have the right representation so that math is trivial" (#18): the
u-band's ~11 octaves of cuts become one duplication chain with a published bound.
"Less is more" (#1): the φ channel's cost stops depending on e at all. "Compute only
surprises" (#3): a kick pays a constant, not a tail. "Behaviours over many seeds" —
the exactness claim is per-key over a 178-key grid with held-out keys, not an average.

## The lens

What this lens may have missed: the unification's encounters half is priced by proxy
(2 RF vs 2 compiles), not measured inside `crates/encounters`' sections; the elegant
closed form may hide a hard special case in the readout (the crossing table's
incomplete-Carlson replacement is asserted by 21ba, unpriced — if it has none, the
compile dies but the readout survives panels and the kick only halves). The run also
left the machine's shared-box noise in the µs columns (medians only, orders of
magnitude).
