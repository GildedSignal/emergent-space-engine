# Dossier — 20261016-2229-second-20261016-2138-fermi-e7ef-98cb

**Claim.** The checker's named gold experiment is run whole, and it splits: the measured cadence
levers, composed into the shipped ladder (the 8× regime split wired constants-only at ≥ 4 Hill
radii of band separation, plus f82a's genesis stagger, plus b583's retired crash search), **cure
the 10⁶-scale freeze outright — spell 21.1/21.8 s → 0.1 s at 3×10⁵ rtf 1800 (deficit −98%, 99% of due
game time delivered, 90–96% still at 36× the player's pace, both runs), with real ceilings above (72×/144×
controls clamp) — but the composed 10⁹ ledger does NOT close: b583's kick-cost halving never acts
on the belt population (fires N-independent at 1,179, identical shipped vs composed; Ĉ 48.7 vs
50.2 µs on/off), so with the interval-measured ÷8.00 cadence the stream stands at 22.5 cores x86 /
13.2 M1, 8.8 / 5.1 with 1a46's 61% delete — over 4 on both anchors, and the ≤ 23 µs kick stays a
requirement, not a delivered lever.**

**Bottleneck.** The board's bodies-28→10⁹ row, via e7ef's silver ("one experiment for gold":
compose the measured kick-cost cut with the measured cadence levers and fly 10⁵–10⁶ at rtf
100–1800). Gain: the freeze cure is now a wired, flight-proven configuration (de-phase + split),
and the 10⁹ critical path is corrected — the belt kick's cost lever is the bind/refit (84–89% of
the kick, b063), not the crash search; a 10⁹-motivated crash-search programme is misaimed.

**Evidence** (`./regen.sh`, ~7 min, < 1.5 GB; the tree patch is `work/patch.diff` — step.rs,
ext.rs, binding.rs, nladder.rs; every lever env-gated, off = shipped):

- *The split is real and exact in its ratio* (`belt_first` off/on): belt first-kick p50
  **14,072 → 112,574 game-s = 8.000×** (the interval, directly), all 2,700 belt bodies qualify as
  bulk at the 4-Hill rule, the locals' line identical. Legality is cited (7f97's B17 bulk
  16/period; 1db4's far-belt ~2/orbit), not re-flown; health on every arm: refusals 0, dead 4–10
  (= shipped's own 4–13), player alive, peak 705 MB at 3×10⁵.
- *The freeze, cured at matched N and pace* (9e75's instrument, shipped arms reproduce its
  record): 3×10⁵ rtf 1800 shipped **spell 21.1/21.8 s, deficit 36,748/38,040, 32–34% of due game time** →
  composed **spell 0.1 s (3 frames), deficit 806/831, 99%** (first run / regen); 10⁵: 7.5/7.2 → 0.1 s.
  At 36× the player's pace (rtf 3600) composed delivers **90–96%** of due game time (spell 0.2–2.1 s
  across the two runs — shared-box wobble), riding the 12-ms budget (p50 9.4–9.5 ms). Controls that must fail, do: rtf 7200
  (72×) spells 21.0 s; rtf 14400 (144×) spells 13.0 s — the composed stream has a ceiling, the
  no-freeze arms are not vacuous.
- *b583's term is absent from the 10⁹ population*: the impact-guess counters fire **1,100–1,179
  times at 10⁴, 10⁵ and 3×10⁵ alike** (the locals'/fleet's searches — never the belt's: a belt
  body's periapsis ≥ 1.2 AU never crosses the star's surface, so `next_impact` is never called),
  identical shipped vs composed; `IMPACT_GUESS=0/1` moves per-event cost **48.7 vs 50.2 µs (3%)**.
  The belt kick's cost is unchanged by the split too (composed arms 39–54 µs vs shipped's 50.6).
- *The composed 10⁹ ledger* (`ledger2.py`, from these flights): anchors belt rate 3.55e-5 ÷ 8.00
  = **4.44e-6/B/game-s** (interval-measured), Ĉ 50.6–52.2 µs x86 / 29.7–30.6 M1 (×0.586): shipped
  180–185 → split **22.5–23.2** → split+delete **8.8–9.0** cores x86; M1 **13.2–13.6 / 5.1–5.3** — none fits 4; required kick
  with split+delete **23.1 µs**, exactly e7ef's paper number, now shown to have **no measured
  lever on the belt** (b583's halving lands on the plane's flying arm, a different population).
- 10⁶ is not flown: its build (2.34 GB, 9e75) busts this container's 2 GB cap; the cure's
  N-scaling rides 9e75's measured linearity (spell ∝ N) — the composition only lowers the
  constant.

**Predictions** (`predictions.md`, written before the matrix): P1 HELD (8.000× direct; the naive
in-window deconvolution is window-shaped and reported as such); P2 HELD (0.1 s; 36×-pace arm 0.2–2.1 s
≤ 5 s); P3 HELD (72× control spells 21.0 s ≥ 3); P4 HELD (fires N-independent and identical,
Ĉ 3% < 10%, both runs); P5 HELD (refusals 0, dead 4–10, alive, 705 MB < 1.5 GB).

**What would make it wrong.** (i) The bulk test (4 Hill radii) misclassifying some scene — then
the measured qualifier fraction moves with it; here all 2,700 qualify and the flight rates
agree. (ii) The 10⁶ extrapolation: the staggered first interval is 225k game-s, longer than any
flown window, so the cure is measured on the interval's leading ~20% plus the controls' clamps;
a full-interval 10⁶ flight needs > 2 GB and stays open. (iii) Ĉ on the M1: the ×0.586 ratio is
1051's, not re-measured here. (iv) The split's behaviour legality (B13/B14/B17) is cited, not
re-flown — a belt rung at Δs × 8 would close that; the refusals/dead counts moved by individual
cases only. **Cost of adopting:** the stagger + split are two env flags on a ~60-line patch
(constants-only, off = shipped); the freeze cure is adoptable within one step. **PRINCIPLES fit:**
#1 "the cheapest compute is compute not done" — 8× fewer kicks, not faster kicks; #34 "the
oracles are guards, not shepherds" — the crash-search lever was adopted into a ledger for a
population that never runs it, and the flight said so.

**The lens.** Second author: I inherited the checker's frame (the composition as named) and ran
it whole rather than re-derive it; the sharpest finding (b583's term empty for the belt) was
visible in the code before the flight, and the flight confirms it — the counters make it a
measurement, not a reading. What the lens may have missed: the locals'/fleet's stream (1.55/s,
N-independent) becomes the composed plane's floor at 10⁶-scale paces — at rtf 7200 it is what the
delivered 84% rides on, and no lever here touches it; and I did not fly a burn arm, so the
cure's interaction with the burn's wave (the budget's binding, 9e75) is untested.
