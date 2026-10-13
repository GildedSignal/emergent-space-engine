topic: closed-form-kernel
status: open
closed-by:
valid-while:
updated: 20261013-2005-second-20261013-1915-system-81ca-6701

# One exact O(1) kernel for the cycle: the Carlson basis, all three channels

## Current best

**The whole compile is one certified-exact integer Carlson basis — advance, period
and proper period together, not just the φ channel — verified against the shipped
walk to its own channel quanta on 182 strong keys (grid + held-out + every attack
key): worst 5.3e-10 (adv) / 3.7e-10 (t) / 3.8e-10 (τ), at 18–40 µs flat (O(1) in e)
against the shipped compile's 5.8–374 µs, and 0.5–12 kB per shape deleted with the
knot table. The readout half is measured and negative: one 3-channel incomplete
Carlson evaluation costs 6.5–30 µs against the panel table's 4.0–5.3 µs read (1.6–6.4×
at every row), so the crossing table is a load-bearing amortization of the same
integrals, not dead storage (20261013-2005-second-20261013-1915-system-81ca-6701).**

The reduction (standard Carlson notation): `K = RF(0,1−m,1)`,
`E = K − (m/3)RD(0,1−m,1)`, `Π(ν|m) = K + (ν/3)RJ(0,1−m,1,1−ν)`, with the A-frame
characteristics `m = 4q(1−k)/A ∈ (0,1)` [21ba's m], `ν = −2(1−k)/(2k−1) < 0`,
`ν_h = 4q(1−k)/H1 ∈ (0,1)`; the squared x-factor rides the classical
`∂Π/∂ν = [νE+(m−ν)K−(m−ν²)Π]/(2ν(m−ν)(ν−1))`; `advance = 4RF(0,B,A) − 2π` (81ca,
standard notation). The integer port runs Carlson's published algorithms verbatim
(arXiv:math/9409227 eqs 2.7/2.23/2.31): floor-root duplication, his stop rules
(certified r = 4·ε⁶ ≈ 2⁻¹¹⁸ at spread 2⁻²¹), his series tails in exact Q62
arithmetic; RJ's arguments are homogeneity-pre-scaled ≤ 1 so no internal product
leaves u128/i128. Verified three ways: mpmath 50 dps from the raw (k, q) fields
(≤ 1e-12, regen.sh), an in-probe quadrature of the raw ψ-integrands, and the shipped
walk itself (integer = f64 = quad to the printed digits). The walk's Q30 certificate
break at (8, 0.995) is a φ-channel break only: t and τ stay at 6.2e-9 / 4.9e-9
there. Cost: cheaper at every key with e ≳ 0.4 (9.4× at the (50, 0.99999) leaver
tail), 2.2–3.4× dearer on the whole low-e band (every p at e ≤ 0.1, where compile is
already 6–9 µs, and 1.1–1.4× at large p mid-e) — the belt's own band — the compile's
cost stops depending on e at all, which is the F1-stutter lever. The incomplete Carlson
readout is correct (t 9.8e-9, τ 8.9e-9, adv 3.3e-8 vs shipped at matched amplitude,
inbound mirror included) but 1.6–6.4× slower per query than the panel table, and a
naive closed-form solve is ~1.3 ms: deleting the walk trades compile time (won, 9×)
for read time (lost) unless the table is rebuilt coarser from Carlson values.

**[Checker, this run's check: reproduced bit-identically (all physics numbers,
mpmath 2.9e-13). Domain hole found past e ≈ 0.9999: the t/τ composition feeds
(m−ν²) (raw 2^97 at e = 0.99999) into imul, whose asserted operand bound is 2^96 —
debug builds panic, release silently corrupts (idiv denominator 2^98 overflows a
long-division limb): int t = 1.23e-7 vs 50-dps truth at (99991, 0.99999) — above the
run's own pre-registered 1e-7 port bar — and the showcase key (50, 0.99999) already
runs out-of-domain (int 5.1e-9 vs f64 1.9e-10). e ≤ 0.9999, the e→0 corner (4e-14)
and 10× closer to the separatrix (2.8e-13) are clean; readout holds at fr 0.001–0.999
(≤3.5e-8); Par::from_key is 0.18 µs (cost omission negligible). The certificate claim
is true on e ≤ 0.9999 only until the ν-corner is pre-scaled.]**

## Refuted

- "The integer Carlson port's error analysis is the standing objection" (Opus memo,
  via kick-jet): answered for RF, RD **and** RJ by construction — Carlson's own
  published stop rules and series tails, floor-rounded Q62 end-to-end, integers
  deciding every stored bit (20261013-1915-system-81ca; extended
  20261013-2005-second-20261013-1915-system-81ca-6701).
- "The shipped walk holds Q30 across the strong domain": it does not — 35 quanta at
  (8, 0.995), 62 at (7.801, 0.9), non-monotonic in 1−m (checker of 81ca).
- "The readout's crossing table is cheaply replaceable by incomplete Carlson forms"
  (21ba open direction 3, priced here): **not per-query** — 6.5–30 µs per 3-channel
  incomplete evaluation vs 4.0–5.3 µs for the shipped panel read (1.6–6.4×); the
  table amortizes the same integrals (20261013-2005-second-20261013-1915-system-81ca-6701).
- Pre-registered ≤ 10 µs per incomplete 3-channel evaluation (this run's P5): 6.5–30
  µs measured, f64 — the prediction failed low at the cheap end of the band.

## Open directions

1. **The law change, compile half**: swap the walk's three channels for the Carlson
   basis (RF+RD+RJ per key, ~4 chains), keep or rebuild the readout's table; gates
   re-freeze. First close the ν-corner (pre-scale the t/τ composition as rj_int
   pre-scales its arguments, release-mode asserts) — the certificate currently fails
   exactly on the leaver tail it wins most. Would change: the compile term (49–97% of
   every kick rebind) becomes O(1) in e; the leaver/plunge tail (228–374 µs) drops
   ~9–19×; 0.5–12 kB/shape freed.
2. **A Carlson-built crossing table**: rebuild the knots at coarser, error-bounded
   amplitudes from incomplete Carlson values (compile once, read fast) — the route
   that keeps the 4 µs read and deletes the walk's band-cut machinery.
3. **The m→1 complementary forms** near the separatrix and the ν-pole corner's extra
  pre-scaling duplications (~4 at e = 0.99): unpriced shavings.
4. **The passage (unbound) branch and Kerr** (Fujita–Hikida forms): the same basis,
  untouched.

## Contradictions

None open. The weak-branch controls behave as law.md says for advance (1.15e-5
truncation); the weak branch's t/τ match the closed form at 2.5e-10 (the walk's weak
t/τ are not first-order truncated — noted, unexplained, harmless).

## Runs
- 20261013-1915-system-81ca (awaiting grade): advance = one exact integer RF on the
- 20261013-1915-system-81ca (silver): advance = one exact integer RF on the key's
- 20261013-2005-second-20261013-1915-system-81ca-6701 (awaiting grade): all three
