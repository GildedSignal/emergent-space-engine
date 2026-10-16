# Dossier — 20261016-2229-scout-ab3d

## Claim

The player's in-belt scan answer walk (the scan-queue page's latch, S = (N−314)×4.2 µs = 418 ms
at 10⁵) closes with a sound two-stage angular certificate — mean-longitude window with each
body's exact anomaly margin, then an equation-of-center series at 35–50 ns a candidate (shared box) — measured
at 1.6–1.7 ms at 10⁵ with the shipped readout (rock-scale radii, 247× under today) and 5.0 ms
at the shipped 12,850-km radii under the float-then-exact composition (`radial.rs`'s own
pattern: floats explore, the exact integer predicate decides the survivors) — both under the
6-ms bar, sound with zero missed hits in every scene including a 500-body formation and the
all-e=0.4 tail. At 10⁶ the rock point needs the standing λ-index plus the cheap readout
(≈4.8 ms), and at the shipped radii no filter can meet the bar at all: the answer's own truth
is 0.53%·N encounters a scan (5,291 at 10⁶ = 22 ms of exact readouts) — the operating point,
not the finder, is the wall.

## Bottleneck

The board's furthest gap (bodies: 28 → 10⁹), first named lab question: "which term breaks first
as the plane grows (per-frame walks…)" — the in-belt scan is that term (3999: the answer latch
at every flown N; 1250: the max-gated latch survives the knot certificate). Expected gain: 10²–10³×
on the answer half; deletes the population-level answer requirement at 10⁵ and the rock regime.
PRINCIPLES 30 ("navigation, knowledge and dynamics those need to be perfect"): the scan is the
knowledge instrument; it must be sound, and cheap enough to answer at all.

## Evidence

All numbers from `./falsifier` (`run.jsonl`, 32 rows; x86 shared box, orders of magnitude).
The replica is code-derived, not wiki-derived: belt genesis from `scenario.rs::ladder_ship`
(a ∈ [2,3) AU, e Rayleigh σ=0.07 redrawn above 0.4, uniform ω and phase), ship radius
34·2⁸ root units = 12,850 km, `near` = 2¹⁰·(r_a+r_b) = 0.176 AU, h = the belt interval
28,141.5 s (and 1,000 s), predicate = the float twin of `encounter.rs::compute` (min over
τ∈[0,h] of |d₀+wτ| ≤ near on exact Kepler states).

- **Soundness (K1 never fired):** zero missed true hits in all 22 checked scenes (3 seeds × 3
  querents × 2 horizons, rock point, 10⁶ at both points), the formation control (500 bodies at
  the querent's longitude: keep 1.000, 500/500 true hits kept) and the all-e=0.4 tail (247
  truth hits kept). The series form's tail is tabulated per e (256 bins, sound at the bin top,
  ×1.5) before any miss is counted; margin(e) likewise.
- **Keep fractions:** stage 1 (λ + static anomaly margins) 10.5–18.4% (player-like querent
  10.5%, belt querents up to 36% at e=0.39); stage 2 (anomaly resolved) 4.0–4.2% at the ship
  point, **0.19% (long h) / 0.008–0.012% (short h) at the rock point**; at 10⁶: stage-2 1,877
  of 10⁶ (rock), 42,452 (ship).
- **Costs (hot loops, 10⁶ bodies):** stage 1 = 2.8–2.9 ns a candidate (the O(N) λ pass); stage 2 =
  34.7–50.1 ns (series, two runs) / 266.8–270.2 ns (Newton) — K3 passes on the series, the Newton form alone would
  have died it (> 200 ns).
- **Composed S (c₁·N + c₂·k₁ + readout·k₂):** rock point **1.62–1.69 ms at 10⁵** (shipped 4.2 µs
  readout) — under the 6-ms bar; **5.0 ms at 10⁵ at the shipped radii under float-then-exact**
  (series stage-2 + 0.4 µs float readout on the 4,245 survivors + 4.2 µs exact predicate on
  the 529 true hits); 16.2–16.9 ms at 10⁶ (the O(N) pass 2.9 ms + 1,877 readouts 7.9 ms
  + 110k series 3.8 ms) — over until the standing λ-index removes the O(N) pass and the
  closed-form readout (3999's named 0.5 µs) takes the survivors: ≈4.8 ms, under. Ship point:
  18.9 ms at 10⁵ if every survivor pays the 4.2-µs readout (K2 fired as stated: the all-exact
  form is dead at the shipped radii; the float-then-exact form above is the wired shape);
  **at 10⁶ the truth alone (5,291 hits × 4.2 µs = 22 ms) busts the bar** — the answer is too
  big to serve, not too hard to find.
- **The truth's density:** 551–607 true encounters per 10⁵-body scan (0.55%, seeds 1–3 same
  band), 5,291 at 10⁶ (0.53% — linear in N) at the shipped radii; 0–1 at rock radii.

Reproduce: `cd lab/results/20261016-2229-scout-ab3d && rustc -O falsifier.rs -o falsifier &&
./falsifier` (13 s; `regen.sh` does exactly this and checks the row count).

## Predictions

Written before the run (`predictions.md`). What held: soundness (0 misses, formation control,
tail control — P6); seed spread within ±30% (P9: 0.039–0.053 vs 0.042); series cost 15–60 ns
(P5: 34.7); the bar met at 10⁵ rock (P3/P4, though I priced it at the wrong radii). What
failed, and why: **P2's keep fraction was 35× low — a decimal slip in my own arithmetic**
(I wrote near ≈ 1.76×10⁻⁴ AU; the code-derived value is 0.176 AU: the ladder ships are
12,850-km bodies, 34·2⁸ root units, root unit 1,477 m — Home is 4,313 root units = Earth).
P1's band (4–12%) held only for the player-like querent (10.5%); belt querents carry both
margins (up to 36%). P7 half-held: stage 1 blows up at the tail (33%) but the composed
two-stage survives it (6.3% keep2, 247 hits kept, S ≈ 5 ms at 10⁵ with the cheap readout).
P8 (h-halving) failed at the ship point (near dominates |w|h: 4.16→4.00%) and held at the
rock point (0.19%→0.012%, the |w|h term rules there).

## What would make it wrong

- The replica is planar, unperturbed Kepler between epochs (λ linear; true under the shipped
  key between events, since every kick re-anchors) and float; the shipped window carries
  residual/rounding widenings my float twin idealizes — wiring must carry them or the cut
  eats a hit.
- The 3999 record reports the belt-band scan with ZERO encounters; my code-derived replica
  finds 0.55%·N at the shipped radii. Likely reconciliation: their zero is the *log* (the
  latch froze the drain, so no answer was ever served), and their nearest-candidate distance
  (2.1×10⁶ × reach) is not in the units I assumed — but if their scan's `near` is genuinely
  smaller than my derivation, the operating point moves toward the rock point and every
  verdict above improves. This cross-check is the first thing the checker should adjudicate.
- The capture half (the 0.046–0.111 µs/body walk at `universe.rs:772`) is untouched; at 10⁵
  it is 10 ms and becomes the binding term once the answer half closes.
- The standing λ-index (needed at 10⁶) is priced by arithmetic (renewal at the body's own
  events, the MD-cell-list pattern), not built; its maintenance cost and the doll-splitting
  of bins are unmeasured.

## Cost of adopting, and fit

Adoption is one additive filter in front of `Scan::compute`'s readout loop plus (at 10⁶) a
λ-bin registration beside `radial.rs`'s hulls — no law change, outcomes unchanged by
construction (the certificate only drops provably-far candidates, the `radial.rs` pattern:
floats widened, integers decide). PRINCIPLES: #3 "compute only surprises" (99.8% of the
in-belt reads deleted at the rock point), #26 "steal from people with skin in the game" —
the mechanism is molecular dynamics' cell/Verlet lists (rebuild on drift; Chialvo 1990, Awile
2012, Kim 2023 — the skin renewal) composed with satellite conjunction screening's
apsidal-filter-then-time structure (George's CSieve 2011, Saingyen 2023; UNVERIFIED beyond
abstracts) and the textbook equation-of-center series (Battin; Murray & Dermott) with a
rigorous per-e tail. #14 "no ticks": the index renews at the body's own events, never per frame.

## The lens

The scout searched MD, satellite conjunction screening, game broadphase and databases (interval
trees answer hull stabbing in O(log N + k) — useless here, the hull answer is dense; the cut
must be in time/phase, not hull space). What the lens may have missed: the integrator-side
fields (event-driven MD's neighbor books) and the GR doll's apsidal advance (4e7c's flag: a
precessing ω breaks a static ω registration — the margin must renew with the doll's own
precession, priced nowhere here). The bigger miss is mine, not the lens's: I read the ship
radius wrong by 10³ before the run; the checker should re-derive every constant from
`scenario.rs` before trusting the operating point.
