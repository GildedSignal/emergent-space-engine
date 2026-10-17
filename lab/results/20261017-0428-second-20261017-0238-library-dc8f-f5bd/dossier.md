# Dossier — 20261017-0428-second-20261017-0238-library-dc8f-f5bd (second author on library-dc8f)

**Claim.** The checker's named gold experiment is flown (the compose/fence flight, `nladder`
ported to Linux behind 1a46's patch plus this run's instruments, both arms to the full
8×10⁶-game-s target), and it refutes **both** published constants while confirming the
library run's mechanism: there is no quantum fence (the law's coarsest acting angle grid —
the tube's 32-bit periapsis angle, 8.38×10⁻⁸° — is crossed at ~68 gs, and the published
2.6×10⁻⁴° debt at 5,400 gs was already 3,000× above it), the debt follows no candidate law
(t^2.15 dies past ~2×10⁵ gs — measured 14.7° at 7.41×10⁶ gs where it predicts 1,450° —
linear-from-11,000-gs dies too — 18× under — and there is no saturation), so k*, the
re-kick interval in carried kicks at the belt cadence, is **2^−8.7 … 2^+3.7 for every angle
bar from the tube grid to 1°** (T* measured inside the flown range for every such bar:
3.6×10⁵ gs at 1°), the page's universal **2^10–2^12 band needs a bar of ~70°** — a fifth of
a circle — and the dc8f "~10⁷-gs horizon / 2^8.5" constant dies with it; what stands is the
mechanism (bind the re-kick to a horizon, derive k per population) with the horizon set by
**the certificate's angle bar in degrees, which no page has frozen**; and the re-kick's
cost is now measured, not assumed: **37,056 ns = 0.51× one fired kick (72,004 ns)**, so the
add-back budget never binds at any cadence.

**Bottleneck.** Board #1 (bodies in the flyable engine): the compose decision — whether
ES_SECULAR (adopted direction) ships without the sparse secular re-kick, and at what
cadence. This run deletes the uncertainty the checker named ("the horizon is the decisive
unflown constant, not k"): both candidate horizons are now measured against the law's own
grids.

**Evidence** (this Linux box, budget-free coast, N=1000 (1,028 bodies), seed 1, rtf 100
(calibration) / 5,000 (long), engine budget unbounded, threads 1; every command in
`regen.sh`, ~10 min at default — the flown full-length artifacts are `work/trace_{off,arm}.txt`
and `work/analyze.out`; `REGEN_FULL=1` reflies the 8×10⁶ target, ~26 min):

*Calibration — the instrument is the record's, bit for bit:*
- OFF 5,400 gs: max/p99 events 334/136, ledger 22,219 events / 9,217 kicks — the published
  record exactly; OFF 1,900 gs: 240/146, 11,111/3,624 — exactly. ES_SECULAR arm 5,400 gs:
  131/26, 6,580/1,382 — exactly. A thread-4 rerun: end states identical (schedule-determinism
  control). Patched-OFF is the record's OFF.
- The record's own end-state probe reproduces: deleted in-situ max |Δangle| = **2.620×10⁻⁴°
  at 5,400 gs** (published 2.6×10⁻⁴), **1.181×10⁻³° at 11,000 gs** (published 1.2×10⁻³);
  belt deleted 0.000° (all 274); the traced set **477 = 274 belt + 200 in-situ + 3 doll-3** —
  checker 2's 477 exactly.

*The decisive flight (both arms in parallel to the 8×10⁶-gs target — 1,480× the 5,400-gs
anchor; OFF wall 1,493 s, 24.6M events; ARM 609 s — angle trace of all 477 at 96 matched
log-spaced horizons, 5,400 → 7.41×10⁶ gs, identical read ticks):*
- **The debt curve** (max over the deleted set; per-horizon table in `work/analyze.out`):
  tracks t^2.15 to ~2×10⁵ gs (0.698° at 2.08×10⁵ vs 0.666° predicted), then bends — 1.0° at
  4.8×10⁵ (power said 4.7°), 2.2° at 1.0×10⁶ (power 19.5°), **14.65° at 7.41×10⁶ (power
  1,450°, linear-from-11k 0.81°)** — a noisy staircase (the max switches bodies; local
  exponents 1.0–1.6 late; last-half fit t^0.87, last-three-quarters t^1.18) with **no
  saturation**: still rising at the last horizon. The median over all deleted (belt-dominated)
  grows smoothly as ~t^2.0 to 1.06×10⁻³°; the belt's own max reaches 2.2×10⁻³° — three
  orders under the in-situ (the record's "belt 0.000000°" was the 6-decimal print).
- **The fence quanta, from the shipped state words** of the deleted in-situ (the dump's own
  length/velocity exponents): readout position word 2.5–5.6×10⁻¹⁷°, velocity word
  7–15×10⁻¹⁷°, carried-impulse grid 2^(vexp−16) ~10⁻²¹°; the coarsest acting angle grid in
  the law is the tube's **32-bit periapsis angle** (docs/law.md, "the periapsis angle
  (32 bits)"): **8.38×10⁻⁸°**. No grid the law acts on ever hid a 2.6×10⁻⁴° debt — the
  "behind the quantum fence, goes live near 2^16 carried kicks (~10⁷ game-s)" reading was a
  3-decimal print artifact, exactly as the checker suspected ("either the debt saturates or
  the 10⁷-gs constant is off": it is off, by five orders against the tube grid).
- **k\* from the measured curve** (T* where max debt = q; belt cadence 3.55×10⁻⁵ ev/B/gs,
  a9d7 gold): q = 8.38×10⁻⁸° → T* = 68 gs, k* = **−8.7**; 10⁻⁶° → 214 gs, −7.0; 10⁻³° →
  5.3×10³ gs, −2.4; 10⁻²° → 2.6×10⁴ gs, −0.1; 0.1° → 9.0×10⁴ gs, **+1.7**; 1° → 3.6×10⁵ gs,
  **+3.7**. Every bar ≤ 1° crosses inside the flown range, so **no horizon extension can
  move these numbers**; the checker's 3×-horizon sensitivity is answered by construction
  (and by extrapolation: at 2.2×10⁷ gs the late law puts the debt near 50°, still under the
  band's ~70° lower edge). The page's 2^10–2^12 band corresponds to bars of ~70° to beyond
  360°.
- **The re-kick bench** (attack 4), measured in flight on shipped structures — one re-kick =
  the secular-rate sum over the doll's sources (r9's τ family, the same walk `secular`
  makes per plan) + the orientation advance + a rebind through the engine's own apply path;
  56,628 samples over 595,000 gs: **37,056 ns per re-kick vs 72,004 ns per fired kick
  (41,018 samples) = 0.51×** — the ≤36× budget condition holds with ~70× margin.
- **The spared set: bit-identical** — 540 non-fleet ships kept in both arms, angle
  mismatches 0 at the final tick (6-decimal print); the delete leaks nowhere. The arm's
  deleted set at the end: 483 (the 477 launch set + 6 late belt joins).

**Predictions.** `predictions.md` written before the decisive flights. (1) WRONG in
magnitude, right in shape: the debt bends (t^2.15 dead past 2×10⁵ gs) but naive
linear-from-11,000-gs underestimates it 18× at the last horizon — the truth sits between
the dead laws (a staircase whose late slope is ~t^1.0–1.6; the 11,000-gs point was inside
the superlinear regime, as the checker suspected when calling it probe-horizon-bound).
(2) Held in its verdict, wrong in its arithmetic: the measured curve crosses 1° at
3.6×10⁵ gs (not the naive 9×10⁶), so k* at 1° is 2^3.7, not 2^8.4. (3) Held, ~70× margin.
(4) Held — every bar ≤ 1° has T* inside the flown range; horizon extension cannot flip it.
(5) Held — 540/540 spared bodies bit-identical. The calibration held bit for bit at every
flown point.

**What would make it wrong.** The trace reads at frame-crossing ticks (rtf 5,000 → 83-gs
frames), so single-horizon maxima carry fire-quantization jitter (at "5,400" the trace max
is 1.03×10⁻³° where the exact-tick probe gives 2.62×10⁻⁴° — a comb beat fires inside the
frame; the anchors are pinned exactly by the record probe). The curve's shape and all k*
for bars ≤ 1° are robust to this (crossings measured inside the range), but a single-point
reading is not. The max-debt mechanism (which body owns the maximum as the kicked orbits
evolve) is unexplained — measured, not derived; the median's ~t^2 belt law and the max's
~t^1.1 late law are different populations' truths. The re-kick's rotate step is the bench's
float form; the shipped exact-integer rotation is a representation question this run prices
(4 multiplies) but does not build. The certificate's angle bar q is not frozen by anyone
yet — k*(q) is delivered as a table, and the compose rung should freeze q first. The
checker's full 2×10⁷-gs ask was met at 8×10⁶ (0.4×) with the extension argued from the
measured late law, not flown.

**Cost of adoption.** Zero code on `main`: flight and bench are default-off probes
(patched-OFF bit-identical to the record at both calibration horizons). What the integrator
gains: the compose rung needs no sparse re-kick *scheduler* (there is no fence horizon to
schedule against); it needs the certificate's angle bar frozen in degrees — and at belt
scale a re-kick, if wanted at all, rides every fire (sub-one-carried-kick cadence) at half
a kick's cost. **PRINCIPLES fit:** "Measure before claiming, and never strawman" — both
published constants were unmeasured and are now measured; #13 "Errors never compound" —
the delete's error is bounded only if paid at the bar's cadence, and the bar, not a fence,
is what pays it; #19 "A fix signals the wrong representation" — the fence was the wrong
representation of an error that was live all along.

**The lens (what this may have missed).** The second-author lens trusts the checker's
framing; the more basic question — "was there ever a fence?" — arose only from reading the
law's grids against the published 2.6×10⁻⁴°. The mechanism behind the max-debt staircase
(secular e-cycles of the kicked path vs the frozen tube, per body) is asserted, not
measured; a body-resolved debt decomposition would settle it and is the natural next probe
if the integrator wants the law, not just the curve.
