Grade: silver

**Abstract.** The claim: the bound cycle's per-cycle advance is one exact Carlson RF
call on the key's own dyadic fields (`A = 1−q(8k−2)`, `B = 1−q(4k+2)`, `q = 1/r_peri`,
`k = 1/(1+e)`), priced 1.82–2.10 µs certified-exact in integers vs the shipped
compile's 6.2–228 µs (3.3–108×), and the shipped walk's Q30 certificate is broken at
(8, 0.995). Reproduced bit-for-bit; the formula independently re-derived from the
Schwarzschild geodesic cubic and confirmed by three oracle paths (mpmath 50 dps,
QUADPACK, DOP853 ODE) to ≤1e-15 on a 28-key attack grid; the walk break extends to 62
quanta at 1−m = 2.8e-4. Not gold: only the φ channel is replaced — the walk's t/τ
channels (RD/RJ) and the readout are unported/unpriced, so the walk is not deletable
and nothing is adoptable within one step. Cost of adopting: a law change, gates
re-frozen.

## Reasons

**Reproduction.** `git apply work/patch.diff` + `regen.sh`: STRONG n=170 worst
rel_f64 = rel_int = 9.20e-10, max_iters 13; WEAK n=6, 3.97e-10…1.15e-5; held-out
worst 3.30e-8 at (8, 0.995) with 15 iterations; compile 5.5–172.8 µs, int arm
1827–2134 ns flat — all identical to `probe-out.txt` (exactness columns bit-identical;
µs columns same order, shared box).

**The formula is exact GR, not fitted — independently established.** From the
Schwarzschild timelike cubic with `u₂ = q`, `u₁ = q(2k−1)`, `u₃ = ½−2kq`:
`Δφ_cycle = 4·RF_C(0, B, A)` exactly, i.e. the author's `2(rf−π)` with their
`rf = 2·RF_Carlson` (their `rf_f64` returns `2/√mean`). Three independent numerical
paths (mpmath 50 dps `ellipk` on exact rational reductions of the key's raw integer
fields; scipy QUADPACK θ-quadrature; DOP853 rtol 1e-13 on the textbook geodesic ODE
`u'' + u = 1/L² + 3u²`, periapsis-to-periapsis) agree with both author arms to
≤1e-13 everywhere on my 28-key attack grid — including every key where the walk
disagrees. The A/B algebra and the domain edge are also structurally right: the walk's
own separatrix refusal `1−q(4k+2) ≤ 0` is exactly `B ≤ 0`.

**The negative finding is real and I extend it.** Against the mpmath oracle the walk
is off by 35.4 quanta at (8, 0.995) (author's key, confirmed), and by **62.5 quanta at
(7.801, 0.9)** (1−m = 2.8e-4), 35.5 at (7.81, 0.9), 14.0 at (7.01, 0.5). The break is
non-monotonic in 1−m — (7.85, 0.9) holds at 0.2 quanta — i.e. panel-refinement noise
near the separatrix, not a smooth law; any claim of a clean broken-domain boundary
would be wrong. Deep-e keys far from the separatrix ((20, 0.9999), (50, 0.99999))
hold at 0.4–0.6 quanta while compiling at 300–375 µs: cost and exactness break in
different places, as the dossier implies but does not separate. Iterations stayed
13–15 at every attack key including 1−m = 2.8e-4.

**Weak-branch control confirmed**: walk-vs-oracle −2.8e-7…−5.7e-6 ≈ 3q (the branch's
own first-order truncation), as read.

**Predictions.** Written before the run (mtime ordering consistent; grid and held-out
sets match). P1 ✓ (9.20e-10 ≤ 1e-9), P2 ✓, P4 ✓, P5 ✓ (with the disclosed
coincidence), P3 half-failed (13–15 vs ≤10) and P6 partial (3.3× vs ≥10× at the two
cheapest keys) — both disclosed, neither load-bearing.

**Novelty.** Against `lab/wiki/kick-jet.md` and 21ba: the closed form itself is
21ba's (verified twice there, at 18 keys; this run's independent derivation adds the
third and fourth confirmations). The genuinely new parts: (a) the **certified integer
RF port** — the memo's standing objection, and kick-jet open direction 1(b) verbatim —
built and priced (1.9 µs, 13–15 floor-rounded duplication steps, 3 isqrt each,
π-subtraction exact in integers); (b) the walk-break moved six decades in 1−m (5.5e-3
vs 21ba's 3.5e-9) into the leaver band. No earlier H entry or wiki page has the
integer port or this break.

**Goal fit.** Board #3 (the kick: 75–160 µs vs a ~50 ns floor; the compile is
49–97%). PRINCIPLES #18 "we just need to have the right representation so that math
is trivial": ~11 octaves of band cuts become one duplication chain with a published
bound; #1/#3: the φ channel's cost stops depending on e. Respects "floats may
explore; only integers decide" — the canonical arm is integer end-to-end.

**Why silver, not gold.** The 3.3–108× compares one channel against the whole
compile: the walk's knots carry t and τ too, so adopting RF alone deletes nothing —
the walk still runs. The measured, adoptable-in-one-step deletion does not exist
until the RD/RJ integer port (open direction 1) and the readout's crossing-table
pricing (open direction 3) land; the author says as much in "What would make it
wrong". The walk-break sharpens 21ba's already-recorded separatrix break rather than
killing a standing premise.

## The one experiment to gold

Port RD/RJ as certified integers on the same pattern, price the readout's crossing
table (incomplete Carlson forms), and measure the **whole compile replacement**
(knots and all) on the shipped kick path — one run, three channels, walk deleted.
(Alternative in-situ route: wire the per-pair Δφ into `crates/encounters`' sections
and measure the co-precessing update against recompiles there.)

## What the author missed

- The walk break reaches **62 quanta** at 1−m = 2.8e-4 and is non-monotonic in 1−m
  (panel noise) — the "two decades shallower" framing underplays both the size and
  the character of the break.
- The integer certificate is RF-**relative** (≈1.1e-15): it decides Q30 quanta only
  while advance ≳ 3.4e-6. The strong branch's edge (q = 2⁻¹⁸ ⇒ advance ≥ 1.1e-5)
  keeps ~3× margin; on the weak branch the certificate no longer covers a quantum
  (measured 2.3e-10 at p = 1.6e7 against a bound of 2.7e-9) — harmless today (the
  weak branch is first-order anyway) but it belongs on the kernel's domain line.
- The repo already ships an independent float oracle for periapsis advance
  (`xtask gr-oracle`: Darwin quadrature vs Binet ODE, H0195 era) — "no independent GR
  oracle available" overstated the run's isolation; this check used three paths.
- The dossier's formula line `advance = 2·[RF(0, B, A) − π]` uses a nonstandard RF
  (2× Carlson's); in standard notation it is `4·RF(0,B,A) − 2π`. Code correct;
  a reader reimplementing from the dossier alone will be wrong by 2RF.
- The two held-out refusal keys ((5, 0.0), (5.5, 0.9999)) are silently dropped by
  `filter_map`; predictions promised "record the refusal" and nothing records it
  (both are `B ≤ 0`, verified by hand).
- The unification half (encounters co-precession at ~2 µs/tube) remains a proxy
  (2 RF vs 2 compiles), unmeasured in `crates/encounters` — disclosed in the lens,
  repeated here because the claim sentence states it as a capability.
