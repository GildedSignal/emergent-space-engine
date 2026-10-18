# The 10⁹ CPU rail: the standing 10.3-core row is not regenerable; the pace and the exclusion width are one >100× dial

**Claim.** The kick-cadence page's standing 10⁹ CPU row (10.3 M1 cores, 2.6× over, split
S* ≈ 20, "kick ≤ 23 µs REQUIRED" — 4e2d/de7b/f790) is **not regenerable from any anchor on
its own page at any pace**: it implies a belt rate of 9.9 events/body/interval where the
page's own thrice-measured census says **2.00** (1.00 kicks + 1.00 boundaries; a9d7 gold,
3294's fire-rate-1.000, 8ffc + two checkers) — a 4.9× **locals-dominated scene-rate
artifact** (the row's own anchors: 73.8k + 71.6k events per comb window at N = 10⁴ with the
locals' N-independent 86–88k/interval stream, divided per-body). Recomposed from the
census: **rail = 2.08–5.12 cores × (rtf/100) × S** (two combs, cost bracket 29.3 µs M1
event / 50 µs x86 / 72 µs fired kick; S = belt survival under the secular delete, 1 /
0.615 / 0). At rtf 1 (the literal "compared to real time") everything fits (≤ 3.15 with the
flown delete). At the **shipped player pace rtf 100** (Julien flies `--rtf 100`, HANDOFF)
the stream alone is 208–512 cores no-delete and 128–315 at the flown delete — the row
**understates 20–50×** there — and closure needs the RES-legal delete (S = 0) plus b509's
fleet contract: the two never-pinned conventions (pace, exclusion width) are together a
>100× dial and are THE 10⁹ CPU decisions.

**Bottleneck.** Board #1/#3 composite (the 10⁹ letter and the kick requirement). Gain:
deletes the "split ≥ 21×" and "≤ 23 µs kick, no measured lever" requirements at rtf 1;
at rtf 100 it replaces them with the correct, harder pair (pin the pace; price the
resonance-exclusion width) — the S dial is worth 21–51 cores per 0.1 of survival.

**Evidence** (`python3 compose.py`, ~1 s, deterministic; `compose.out` shipped):
- Identity: 1/28,141.5 game-s = 3.553×10⁻⁵ = a9d7's census; `belt_first` p50 14,071.5 =
  interval/2. Positive control: 9e75's own "the average fits: 1.75 cores at rtf 1"
  regenerates exactly (one comb @ 50 µs = 1.78).
- The standing row's failure: 10.3 cores needs 9.9 ev/B/interval; census 2.00. Its rtf-100
  siblings regenerate as pace costs (two combs @29.3 µs ×100 = 208 ≈ 9e75's "185–187 at
  rtf 100"; one comb @50 µs ×100 = 178 ≈ e7ef's "104–178").
- Recomposed table (both paces, both costs): rtf 1: S=1 → 2.08–5.12; S=0.615 → 1.28–3.15;
  S=0 → ~0.97 (re-kick 0.28% @0.57× + encounters 0.95 + view 10⁻⁴ + reabsorb 0.011).
  rtf 100: ×100 each (stream), terms scale with pace too.
- No measured cadence lever closes rtf-100 CPU at S ≥ 0.615: split 8 (f790, measured)
  → 26–64; split+delete → 16–39; the ~50 ns event floor → 0.36 (so at rtf 100 the floor
  finally IS the requirement, or the delete must go to RES).
- The crest at rtf 1 is the genesis wave, not a steady rate: steady demand 7.1×10⁴
  ev/wall-s (2.1–5.1 cores); the wave peaks ~20× for ~1.4×10³ game-s at birth
  (C50 40–58×, calendar d520), one-time and stagger-cured (f82a). 9e75's 19–20-h freeze
  is the rtf-100 budget clamp.
- The S dial, from shipped `scenario.rs` (belt uniform [2,3) AU, e Rayleigh 0.07; Home
  2⁻¹⁸ at 1.0003 AU, Giant 2⁻¹⁰ at 5.196 AU, Cinder 2⁻²¹ at 0.391 AU): the frozen
  exclusion replica (j,k ≤ 8, 2% on period) spares 0.530 (anchor 434/712 = 0.615, ratio
  0.86); **no first-order (j+1):j resonance of any planet falls in [2,3) AU** — the
  belt's commensurabilities are all ≥ 2nd order, Cinder contributes exactly zero — and
  the frozen 2% flat width is the Giant's shipped first-order width
  (2.5·μ^(2/3) = 2.46%, resonance.rs:59) × 0.8 but 33× Home's and 131× Cinder's:
  Giant-width protection for resonances with no first-order member. The width is a dial,
  not a tide fact.
- Memory row (6793, controls): 8 GB/5,060 B = 1.58×10⁶ live; q16 3.0 GB + 1.3 kB live ≈
  8.0 GB at ~3.85M live (at the ceiling); 126-bit store 15.75 GB busts (negative control).

**Predictions** (`predictions.md`, written before the compose): P1 held (spared 0.530 ∈
[0.45, 0.80]); P2 held (NONE first-order, exact); P4 held at rtf 1 (S=0 total 0.96 < 1.5);
P5 held (Giant 0.407 of 0.530, Cinder 0.000). **P3 failed at rtf 1 and holds at rtf 100**
("rail at S=0.615 exceeds every budget ≥ 1.25×": measured 0.16–0.79× at rtf 1, 32–79× at
rtf 100) — the prediction was written against the standing row's unstated pace; its split
across conventions is the finding, reported as held/failed per pace, no post-hoc tuning.

**What would make it wrong.** (1) A 10⁹ belt on a different cadence than the shipped
28,141.5-gs interval (the identity control breaks loudly if so). (2) A belt kick cost
outside 29.3–72 µs on the M1 — the 29.3-vs-72 bracket is itself unreconciled on the record
(named open constant; the verdict at rtf 1 survives it, at rtf 100 it moves the
understatement factor, not the direction). (3) If the player's pace is pinned at rtf 1,
the "understates 20–50×" half of the claim inverts to "overstates 5×" — both halves are
computed and shipped in the same table. (4) The exclusion replica's reading of the frozen
rule (j,k ≤ 8, 2% on period) hits 0.86× of the anchor; a different letter of the patch's
rule moves S by ≤ 0.1. Cost of adoption: none in code; re-base the kick-cadence 10⁹ row on
the census rate and pin the pace in the ledger's units.

**Fit with PRINCIPLES.** #27 "The goal, never a proxy": the ledger's unit must be pinned to
the player's pace before any "×-over-budget" has meaning — two proxies (an artifact rate
and an unstated rtf) were multiplying each other. #26 "steal from people with skin in the
game": the Fermi estimate is the quant's back-of-envelope that catches a unit slip before
it prices a strategy. "A test that cannot fail is a control": the C− controls (the standing
row, the 126-bit store) fail as they must; the C+ control (9e75's own rtf-1 sentence)
passes to 2%.

**The lens.** Fermi arithmetic sees rates and units, not instruments: it cannot measure
the kick cost on the M1, adjudicate the exclusion legality (a B17-class flight), or pin
the pace (one sentence from Julien); all three are carried as named brackets. Its blind
side here is trust: the wiki's numbers were assumed consistent until two of them
contradicted — the check that found it is the one this lens exists to run.
