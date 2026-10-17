# Dossier — 20261017-1918-inversion-8994 (inversion lens)

## Claim

The merged N1 gate's headline — "N = 10⁶ keeps F1 for a 20-s flight, frame flat in N" — is a
property of its 20-s window, not of the flight: the window (2,000 game-s at rtf 100) ends
**11,051 game-s before the population's first belt item** (13,051; all first items within
13,051–14,542, `belt_first`), so the gate measured the birth, never the duty cycle. Flown through
that first comb, budget-free, the worst rolling wall-second of engine work crosses the 12-ms letter
between N = 10⁴ (3.15 ms) and 10⁵ (18.0 ms) and reaches **85.9 ms at 3×10⁵ (7.2× the budget)** —
super-linear in N (5.0× the wave term for 3× the bodies; cache, as the ladder itself saw on the
walk). On the shipped 12-ms budget path the letter still holds at 3×10⁵ (lag ≤ 2 game-s, 8 frames
over) because deferral plus cache-warm draining absorb the crest, but the crest's event mass
scales with N into a **fixed 1,491-game-s span while the inter-comb budget capacity does not**:
at the gate's own 10⁶ the crest (≈1.1–1.2×10⁶ events, ×3.33 of the measured 3×10⁵ arm) needs
~15–35 s of engine work at M1-class rates against ~20 s of budget before the next comb — **the
letter's true N through the first comb is ~3×10⁵–10⁶ (M1), not 10⁶; the gate's number is
window-bounded** and coincides with 917c's checker-corrected ≈6×10⁵ letter, here reached from the
shipped path at both measured ends.

## Bottleneck

The board's top item (bodies in the flyable engine). The inversion: what makes the headline worse
that we do now — the gate freezes a window 7× shorter than the population's first duty cycle, so
every "smooth at N" claim in the merged table is untested against the population's own first event.
Gain: correctness of the board's top number (its N is ~2-3× overstated as a flight-wide letter);
nothing to build — the fix is the gate's window (one line: fly the letter to ≥1.2× the belt's
second comb, ~46,000 game-s, or state N as birth-scoped), not the engine.

## Evidence (Linux/x86, 8 vCPU shared, load 3.9-4.4, 1 thread, seed 1; orders of magnitude only)

Population: the ladder's own (`plane_extra`, seed 1, 48 fleet, identical draw to gate N1's probe),
coast, rtf 100. Instrument `crates/universe/examples/wave.rs` (this run's patch): the ladder's
frame loop with `Budget::unlimited` (budget-free arms) or the shipped 12-ms deadline (budgeted
arms), horizon in game-s; the letter's test is the worst rolling 60-frame (one wall second) mean
engine-ms. Raw: `raw/`. Reproduce everything: `regen.sh` (~6 min).

| arm (coast, rtf 100) | horizon gs | worst rolling 1-s mean ms | at game-s | frames >12 ms | max lag gs | events |
|---|---|---|---|---|---|---|
| budget-free N=0 (28 bodies) | 45,000 | **1.01** | 153 (exodus) | 2 | – | 23,461 |
| budget-free N=10⁴ | 45,000 | **3.15** | 153 (exodus) | 110 | – | 173,696 |
| budget-free N=10⁵ | 45,000 | **18.02** | **14,135** | 189 | – | 443,696 |
| budget-free N=3×10⁵ | 45,000 | **85.94** | **14,140** | 1,321 | – | 1,043,696 |
| shipped 12-ms budget N=10⁵ | 17,000 | 11.96 | 14,332 | 4 | **1** | 157,238 |
| shipped 12-ms budget N=3×10⁵ | 20,000 | 12.01 | 14,583 | 8 | **2** | 364,487 |
| shipped 12-ms budget N=3×10⁵, long (BOTH combs) | 46,000 | **12.05** | **41,824 = second comb** | 81 | **2** | 1,043,328 |

- **The wave is where `belt_first` says it is, at every N:** the budget-free worst second sits at
  game-s 14,135/14,140 (10⁵/3×10⁵) — inside the belt's first-item band 13,051–14,542
  (`belt_first 100000`: min 13,051, p50 14,072, max 14,542 — a 1.11× span, ~90 frames at rtf 100).
  Locals' first items: p50 661 game-s (inside every window ever flown).
- **N-scaling of the crest (budget-free, N=0 floor 1.01 subtracted):** 17.0 ms → 84.9 ms for
  3× N = **5.0×, super-linear** (the crest's dense drain thrashes the cache, the same term the
  ladder measured when the walk left the cache: 24→54 ns a requeue). Crest frames at 3×10⁵ carry
  1,000-1,328 events at 50-135 ms each; max frame 135.0 ms.
- **The shipped path holds to 3×10⁵ — deferral, not headroom:** budgeted arms cap at ~12 ms
  (worst60 11.96/12.01), lag ≤ 2 game-s, zero refusals, zero dead, and the work is all done
  (364,487 events by 19,231 gs ≥ the belt's first items). The budget-free crest number
  overstates the threat to the shipped path by the cache factor (~3-7× per event): draining at
  budget pace is cache-warm. This is why the letter does NOT break at 10⁵ despite an 18-ms
  budget-free crest.
- **Why it breaks at 10⁶ anyway [INFERENCE, anchored at measured ends]:** the crest's mass scales
  with N into the same 1,491-game-s span: at 10⁶ ≈ 1.1-1.2×10⁶ events (×3.33 the 3×10⁵ arm's
  measured crest) × 25-45 µs/event (measured quiet-path rates here; the M1 runs the ladder's
  events ~1.5-2× faster) ≈ 15-35 s of engine work, against ~20.3 s of 12-ms budget between comb
  starts (28,141 game-s ≈ 1,690 frames × 12 ms). At 3×10⁵ the same arithmetic gives 9-16 s of
  work vs 20.3 s of capacity — drains, as measured. At 10⁶ it does not drain before the second
  comb: **combs stack and the lag grows without bound** — the letter fails at the gate's headline
  N on the shipped path, on both measured ends of the scaling.
- The gate table's own per-body event columns are window artifacts: at 10⁶, 5.85e-6 ev/b/game-s
  over 2,000 game-s = 0.012 events a body — the belt has had no item; the number is the locals'
  stream divided by N.

## Predictions (predictions.md, written before the decisive runs)

- **P1 held, with a disclosed miss:** the wave appears at 13-15k game-s at every N > 0, absent at
  N=0; mass ∝ N — measured super-linear (5.0× for 3×N), I predicted linear ±20%.
- **P2 held:** N=0 floor worst60 = 1.01 ms ≤ 4 ms.
- **P3 direction held, magnitude missed 5× low:** I predicted the crossing at 3×10⁵-10⁶ with
  worst60 ≈ 8-18 ms at 3×10⁵ on the budget-free instrument; measured 85.9 (the cache term).
  The pre-registered kill ("all three under 6 ms AND sub-linear") did not fire. The shipped-path
  letter is NOT broken at 3×10⁵ — my claim survives only in the window-bounded form above, with
  the 10⁶ failure carried by anchored arithmetic, not a flown 10⁶ arm (memory: 2.4-2.7 GB at 10⁶
  exceeds this box's 2 GB process cap).
- **P4 wrong ~4×:** the steady inter-comb stream at 10⁶ computes to ~4 ms a frame (measured rates),
  not 12-25 ms — between combs the letter has margin; it is the crest mass that kills, as P3 said.

The long 3×10⁵ budgeted arm ran after the dossier's first draft and confirms the drain assumption
at the measured end: through BOTH combs (46,000 game-s) the lag stays bounded at 2 game-s, the
second comb (worst second 12.05 ms at game-s 41,824 = first items + 28,141, exactly) is absorbed
like the first, and the budgeted engine does the same work as the budget-free flight to 0.035%
(1,043,328 vs 1,043,696 events) — nothing dropped, nothing refused. So at 3×10⁵ the shipped path
is healthy end-to-end; the 10⁶ verdict stands on the anchored arithmetic (crest mass ×3.33 into
the same span against fixed inter-comb capacity).
## What would make it wrong

A flown 10⁶ arm (needs >2 GB or a memory-lean build) showing the crest drained with bounded lag —
possible only if per-event cost at 10⁶ falls ≥3× below every rate measured here (10⁴-3×10⁵, quiet
and crest). The old drain question — does the first crest drain before the second comb —
is answered by the long arm above: it drains, both combs absorbed at 3×10⁵.

## Cost of adopting, and fit

Cost: the gate's window, not the engine — one probe flag (`wave <N> <horizon>`) exists now; N1's
letter should be restated as birth-scoped or re-frozen with a horizon past one comb interval
(≥46,000 game-s ≈ 460 wall-s a rung at rtf 100 on this class of box; budget-free crest arms are
the cheap pre-filter at ~1/5 of that). No law change; no compute regression; digests untouched
(this probe only reads). Fit — PRINCIPLES: "Measure before claiming" and the test ladder
("extremes and chaotic scenes"): the gate froze its window before the population's first extreme;
"Gates judge a representation" — this one judged a window. The failure class is the known
oracle-domain family (B12, B13, B17, r3): the instrument's domain, not the law's.

## The lens

Inversion asked what the newest merge silently assumes: that a 20-s window contains the flight.
It contains 14% of the wait before the population's first event. What the lens may have missed:
the burn arm (the ladder's burn reaches the star's doll at 15.8 s and changes the scan regime) —
unflown here; and the M1's exact rate (all arms x86; the 10⁶ verdict carries a 1.5-2× speed
assumption, stated).
