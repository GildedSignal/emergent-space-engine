topic: closed-form-kernel
status: open
closed-by:
valid-while:
updated: 20261013-1915-system-81ca

# One exact O(1) kernel for the cycle: Carlson RF on the key's own dyadic fields

## Current best

**The bound cycle's advance is one certified-exact integer Carlson RF call —
`advance = 2·[RF(0, B, A) − π]`, `A = 1 − q(8k−2)`, `B = 1 − q(4k+2)`, all dyadic, no
division (homogeneity absorbs the √A) — independently reproduced from
20261013-1428-scout-21ba and priced at 1.82–2.10 µs in pure integers against the
shipped compile's 6.2–228 µs: 3.3×–108× per key, flat in e (20261013-1915-system-81ca).**
Exactness: worst relerr vs the shipped walk 9.20e-10 over 170 strong keys (under the
walk's Q30 quantum 9.31e-10), with the integer pipeline (floor-rounded duplication,
stop at spread 2⁻²⁴, Carlson's bound ≤ 10⁻¹⁵, π subtracted in integers — the
cancellation trap: a f64 composition costs 3.9e-7) matching the f64 arm to < 1
quantum everywhere. 13–15 duplication steps, 3 isqrt each. The formula is exact, not
fitted (1.3e-12 at q = 0.144, where an O(q²) term would show at 1e-2). **New: the
walk's own Q30 certificate is broken at the held-out key (8, 0.995) (q = 0.249,
1−m = 5.5e-3): 35 quanta, both closed-form arms agreeing to 1e-12 — two decades
shallower than 21ba's second-checker separatrix point (6.7e-7 at 1−m = 3.5e-9), and
exactly where the plane's kicked bodies live (median e 0.94).** The system claim:
this one kernel is also the exact per-pair Δφ/cycle primitive the co-precessing
sections (71a5) and the slack skin's precession sizing (8f99, 73f0) currently
linearize — ~2 µs/tube, 3.3–110× cheaper than recompiles.

**[Checker, this run's check: the closed form is now verified by three independent
paths — mpmath 50 dps `ellipk`, QUADPACK θ-quadrature, and DOP853 on the geodesic
ODE `u'' = 1/L² + 3u² − u` from the key's exact integer fields — agreeing with both
arms to ≤1e-15 on a 28-key attack grid beyond the author's domain (e 0.99999 at
p 50, compile 310 µs; 1−m 2.8e-4). The walk break extends: 62 quanta at (7.801,
0.9), 35 at (7.81, 0.9), 14 at (7.01, 0.5), and is NON-monotonic in 1−m ((7.85,
0.9) holds at 0.2) — panel noise, not a smooth separatrix law. Deep-e keys far
from the separatrix (20, 0.9999; 50, 0.99999) hold at 0.4–0.6 quanta while costing
300–375 µs: the closed form wins cost everywhere, exactness near the separatrix.
Iterations stay 13–15 at every attack key. Boundary found: the integer certificate
(spread 2⁻²⁴ ⇒ RF-relative ≈1.1e-15) decides Q30 quanta only while advance ≳
3.4e-6; the strong branch's edge (q = 2⁻¹⁸ ⇒ advance ≥ 3π·2⁻¹⁸ ≈ 1.1e-5) keeps
~3× margin, the weak branch does not need it (measured 2.3e-10 at p = 1.6e7
against a certificate bound of 2.7e-9). Notation trap: the run's `RF` returns
2/√a, i.e. 2× Carlson's RF — the standard-form identity is `advance = 4·RF(0,B,A)
− 2π`; the code is correct.]**

## Refuted

- "The integer Carlson port's error analysis is the standing objection" (Opus memo,
  via kick-jet): answered for RF by construction — floor rounding plus Carlson's
  published spread bound, integers deciding every Q30 bit
  (20261013-1915-system-81ca; τ/t RD/RJ still open).
- "The shipped walk holds Q30 across the strong domain": it does not — 35 quanta at
  e 0.995, q 0.249 (20261013-1915-system-81ca; extends 21ba's second checker).
- My own pre-registered ≤ 10 duplication iterations: 13–15 needed (spread decay ×4
  from e₀ ≈ 1 to 2⁻²⁴); no key exceeded 15; the m→1 complementary form would shave
  ~2 at the deepest corner, unpriced (20261013-1915-system-81ca predictions.md P3).

## Open directions

1. **Price the τ/t channels as integers** (RD/RJ; reductions verified twice in 21ba's
   checks): completes the compile's replacement; then the law change — swap the
   walk, re-freeze the compile's gates. Would change: the kick's compile term
   (49–97% of the rebind) becomes O(1) in e; the leaver tail (228 µs → ~2 µs/key)
   stops driving F1's stutter.
2. **Wire the kernel as the co-precessing frame's per-pair update** inside
   `crates/encounters` sections (71a5's O(1) angle update) and the skin's exact
   slack sizing (8f99): measured proxy here (2 µs vs 6–228 µs per tube), unmeasured
   in situ.
3. **The readout's crossing table** (incomplete Carlson forms, 21ba's assertion,
   unpriced): if it has no cheap form, panels survive in the readout and the kick
   only halves — the adoption case should price this first.
4. **The m→1 complementary forms** near the separatrix: keeps iterations at 13 and
   the exactness at the deepest corner where the walk is already 35 quanta off.

## Contradictions

None open. The weak-branch control behaves as law.md says (first-order truncation,
1.15e-5 at the shallow end; some weak keys coincide at 4e-10).

## Runs

- 20261013-1915-system-81ca (awaiting grade): advance = one exact integer RF on the
  key's dyadic fields: 1.9 µs vs 6–228 µs compile, 9.2e-10 worst, walk 35 quanta off
  at e 0.995.
