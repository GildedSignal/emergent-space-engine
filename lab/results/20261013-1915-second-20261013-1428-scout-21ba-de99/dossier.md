# Dossier — 20261013-1915-second-20261013-1428-scout-21ba-de99 (lens: second author)

## Claim

The named experiment is done and it holds: an **honest Carlson kernel — RF/RC/RD/RJ
verbatim from Carlson 1994 (arXiv:math/9409227, downloaded and read at source), with the
certified stop rules (2.2)/(2.9)/(2.25)/(2.17) at r = 10⁻¹⁵, normalized-deviation series,
and `std::hint::black_box` on input and output — delivers the panel walk's **three
increments (advance, period, proper_period) as a drop-in**: on every strong-branch key
of a 29-key grid (q_key 1.8×10⁻⁶…0.2436, e to 0.99999, m to 0.99999999) all three agree
with shipped `Orbit::compile` to **1.2×10⁻¹⁰…8.7×10⁻¹¹** (7.6×10⁻¹⁰ at e = 0.99999) —
the walk's own ~2⁻³⁰ quantum — at **black_box wall 129 ns (φ), ~0.7–1.4 µs (τ or t),
2.9 µs all three, flat in e**, against the walk's 5.4 → 307 µs: **φ 42–2378×, all-three
3.5–106×**, with the certified per-iteration law measured at 0.2500 spread ratio
(min = median = max over 4.15×10⁷ duplications) and final relative deviation X ≤ 3.3×10⁻³
inside Carlson's (3r)^{1/6} = 3.8×10⁻³ envelope. At the m→1 edge the walk degrades to
6.7×10⁻⁷ (all channels, P = 1−q(4k+2) = 3×10⁻⁹) while the kernel stays ≤ 3.6×10⁻¹⁰ from
truth — the closed form beats the walk exactly where the walk's certificate stops.

## Bottleneck

`kick-jet` open direction 1, the record's last ≥10× lever (panel count, filed as "a law
change"). Check2's silver verdict: "the cost half was not honestly measured … The one
experiment to make it gold: build and price an honest Carlson kernel — E₂-normalized
series, stop at spread ~10⁻³ (~6 iterations), black_box-timed — delivering φ, τ and t
closed forms as a drop-in … with the certified per-iteration error bound stated; the
readout (crossing table → Newton) may be priced or fenced off." That is this run, no
cheaper part taken.

## Evidence (all numbers regenerate: `regen.sh`, < 1 min, physics columns bit-identical)

Probe: `crates/space/examples/elliptic_kernel.rs` (this run's patch); output
`probe-out.txt`; grid 29 keys = the first run's 18 + both checkers' extensions
(e 0.9999/0.99999, p2³ e0.9 with m = 0.947, e→10⁻⁹) + a 9-rung P-ladder at the m→1 edge
(arbitrary-periapsis keys, P = 10⁻¹…3×10⁻⁹ at e 0.5/0.9).

1. **Kernel exactness (kernel vs independent tanh-sinh truth, no shared code):**
   0…2×10⁻¹⁶ typical — the f64 roundoff floor, far under Carlson's certified r = 10⁻¹⁵;
   worst on the grid 2.1×10⁻¹³ (e = 0.99999: the Π(−β) = K+(n/3)RJ route amplifies
   roundoff by ≈K/Π ≈ 10³ at β = 2×10⁶ — predicted, quantified, still 10³× under the
   walk's quantum); 3.6×10⁻¹⁰ at the m→1 edge (the DE truth's own f64 limit on an
   integrand peaking at 1/√P ≈ 1.8×10⁴).
2. **Drop-in vs shipped, strong branch (20 compiled keys):** advance 1.9×10⁻¹⁰–8.7×10⁻¹¹
   (8.7×10⁻¹¹ at m = 0.947, 3.4×10⁻¹⁰ at e = 0.99999); period/proper 1.2×10⁻¹⁰–7.6×10⁻¹⁰.
   Refusal: p2² e0.5 → `NoBoundOrbit`, closed form returns the same boundary (A ≤ 0 ⟺
   m ≥ 1 ⟺ q ≥ 1/(4k+2)).
3. **Weak rows (q_key ≤ 2⁻¹⁸):** advance 4.3–4.5×10⁻⁶ — the branch's own Taylor
   truncation, the first run's number; period/proper 5×10⁻¹¹–1.2×10⁻¹¹ (the branch's
   clock corrections carry the exact numerators).
4. **The m→1 ladder:** walk error 1.4×10⁻¹² (P = 10⁻¹) → 3.2×10⁻⁸ (10⁻³) → 2.8×10⁻⁷
   (10⁻⁵) → 6.7×10⁻⁷ (3×10⁻⁹, all three channels) — check2's 6.7×10⁻⁷ reproduced —
   while kernel-vs-truth stays ≤ 3.6×10⁻¹⁰.
5. **Honest cost (black_box in and out, medians):** compile 5.4 µs (5 panels) → 307 µs
   (282 knots, e = 0.99999); φ channel 129 ns flat in e; τ 714–1386 ns; t 703–1392 ns;
   all-three 1.55–2.90 µs. **Gains: φ 42× (small e) → 2378× (e = 0.99999); all-three
   3.5× → 106×.** On the leaver tail (e ≥ 0.999) the honest all-three gain is 79–106×
   and φ's is 1490–2378× — 10²–10³× as the adoption case claimed, now on an instrument
   that cannot delete the work.
6. **Certified convergence law, stated and measured:** Carlson 1994 — deviations
   contract by exactly 4 per duplication (paper §2 text; measured ratio 0.2500 =
   min = median = max, n = 4.15×10⁷); series truncation error falls 4⁶ = 4096 per extra
   duplication (paper intro); each R returns relative error < r with n from
   4⁻ⁿQ < |Aₙ| (algorithm statements). At r = 10⁻¹⁵: measured duplications 5–6 per RF/RJ
   call (up to 11 inside RJ at β = 2×10⁶), inner RC ≤ 3; X_final ≤ 3.34×10⁻³ ≤
   (3r)^{1/6} = 3.80×10⁻³. Kernel-vs-truth at the f64 floor (item 1) is the empirical
   seal.
7. **Readout fence (priced as storage, fenced as compute):** at e = 0.999 the walk
   stores 177 knots × 88 B = 15.6 KB + 175 crossing indices to feed `at_phase`/
   `crossing_state`, against 48 B for the three increments; the increments and the knot
   sums come from the **same** 4(knots−1) = 704 `node()` evaluations, so the closed form
   deletes all of them — but replacing the knot table itself needs the incomplete
   (amplitude-carrying) Carlson forms, same duplication algorithm: fenced, not built.
   If the table must survive for other consumers, panels are half the win, not none.

## Predictions

`predictions.md` written before the decisive run (after a disclosed debug run — see
Instrument). Scorecard: 1 ✓ (held, floor-level); 2 ✓ (2×10⁻¹³ at the tail vs predicted
10⁻¹²–10⁻¹¹, mechanism as predicted); 3 ✓ (≤ 7.6×10⁻¹⁰ strong); 4 ✓ exactly (6.70×10⁻⁷
at P = 3×10⁻⁹; truth columns ≤ 3.6×10⁻¹⁰ vs predicted < 10⁻¹¹ — the DE truth's own
limit, disclosed); 5 ✓ (4.3×10⁻⁶ weak advance; 10⁻¹¹ periods); 6 ✓ (same refusal edge);
7 mostly ✓ (spread ratio exactly 4; 5–6 iterations typical; up to 11 at β = 2×10⁶ vs
predicted 6; X ≤ 3.3×10⁻³ ✓); 8 partially (φ 129 ns ✓, τ/t over the predicted ceilings on
the two most extreme rows only: 1.39 µs vs 900 ns, 2.9 vs 2.5 µs; the predicted gains
held with margin: φ ≥ 2378× vs ≥ 450×, all-three 106× vs ≥ 75×); 9 ✓ (0.2500 exactly);
10 no kill triggered.

## Instrument (disclosed, in order)

- The first Rust run was a debug run: it exposed (a) my J₀ hand-derivation's wrong
  K-coefficient (−(n+m)K; an m = 0 spot check cannot catch it — both candidates equal
  n there). Correct reduction derived with sympy from the endpoint-zero identity
  d/dθ[sc√(1−ms²)/(1−ns²)] and verified against mpmath's ellippi/ellipk/ellipe to
  **1.1×10⁻¹⁶** before the decisive run:
  `J₀ = [(n²−2(1+m)n+3m)Π + (n−m)K − nE] / (2(n−1)(n−m))`.
- **The first run's tanh-sinh `de` was broken, now found and fixed:** its weight used
  cosh(t) with t the tanh *value*; sech² applies to the tanh *argument*
  (cosh(π/2·sinh u)) — the weight was ~8.5× too large (∫1dt returned 17.0). This
  explains the junk `C_t_dev`/`C_tau_dev` = 1.00e0 columns both checkers saw in
  probe-out.txt of 21ba, and its "never converged" h-floor behaviour.
- The t-channel needed the horizon prefactor γ⁻¹, γ = 1−2q(2k−1): the debug residuals
  equalled γ⁻¹−1 exactly on every row (1.95×10⁻³, 7.8×10⁻³, 2.5×10⁻² at γ = 0.998,
  0.992, 0.975).
- Two of my own edge-key construction bugs briefly faked a "walk collapse" (denormal
  >62-bit significand; then `Scalar::raw(n, bp)` misread as n·2⁻ᵇᵖ when it is n·2ᵇᵖ —
  cf. `bound`'s `raw(k, −48)`). After the fix the ladder reproduces check2's 6.7×10⁻⁷.
  The intermediate garbage rows are not in the record.

## What would make it wrong, cost of adopting, fit

- **Wrong if** the integer port cannot carry the certified bound at the law's quanta —
  this run is f64 (the checker allowed either); the port is the next named step, and
  the duplication loop's only non-add primitive is the sqrt (isqrt closed bit-identical,
  9384). Or if a consumer needs the knot sums' *intermediate* values, not just the
  increments — then panels are half the win (item 7).
- **Cost of adopting:** unchanged from the first run — a law change with recertification:
  incomplete Carlson forms replace the crossing table/readout; the integer port needs
  its own error analysis. This run removes the "cited, not measured" qualifier from all
  three channels and prices the win on an honest instrument.
- **Fit (PRINCIPLES):** #18 "we just need to have the right representation so that math
  is trivial" — three increments, three closed forms, O(1) in e; #1 "the cheapest
  compute is compute not done" — 704 node evaluations deleted per compile at e = 0.999;
  #19 "if you find yourself fixing things … wrong representation" — the band cuts and
  the λ-ladder were fixes for representing an elliptic integral as panels; #10
  iteration speed — the falsifying instrument (the timing loop) was the thing fixed
  first.

## The lens

The second-author lens inherits the scout's blind spots and adds its own: everything is
still Schwarzschild-equatorial (kerr.rs's quartic radial polynomial is the same Carlson
family — Fujita–Hikida — still unverified at source); the readout's Newton solve was
priced as storage, not as the in-cell search cost; walls are one shared Linux box —
orders of magnitude only, the integrator re-measures on the M1.
