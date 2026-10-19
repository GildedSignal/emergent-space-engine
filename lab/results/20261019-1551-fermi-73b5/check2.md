Grade: gold

**Abstract.** The e828/1176 encounters conflict is a units conflict; both runs' raw
measurements agree, and the corrected churn row is 0.35–1.4 cores. Verified from
primary sources: 1a29's 355 recomputes to 355.3 from their verbatim constants and is
per pair-touch; the epoch divisor is E_pair under both wirings, so 1176's
E_cell = (n/2)·E_pair understates n/2 = 10³–5×10³ (their 3.5×10⁻⁴ → 0.35 cores);
like-for-like the leak is 7× over at P = 4, not 140× under. e828's harness is
byte-identical, anchors bit-identical; fresh seed 31337 and κ = 2⁻²⁹ probes reproduce
the laws. The game coupling is r ≈ 6×10⁻⁹–2.3×10⁻⁸ (a game-tick/replica-tick mix plus
a dropped TAU; ~10³×, not the page's "~10⁶×" — fixed) — conservative everywhere.
Ledger shifts −1.4 to −5.1 cores; the 363-core arm is dead. Adoption cost: freeze
wording only.

**Reasons.**

1. **Reproduction.** regen.sh exit 0 (runner); I re-ran `book 20261018 1e-4` from the
   prebuilt binary: bit-identical to e828's committed `book.txt` on their branch, and
   to this run's `out/book.txt`. `work/epochflux.rs` is byte-identical to e828's
   committed harness (extracted from their `work/patch.diff`). ledger.txt matches
   dossier §F; every anchor (w p50 53,946; armed(1e6) 0.7767 — e828's dossier's 0.7742
   is the smallh sample, also present in both runs; dues q10/50/90; deep flips
   0.169–0.174; 8/1,535,976 = 5.208×10⁻⁶ on seed 777; dv0/E=1 zero) reproduces.
2. **The 355 row and the divisor** (the load-bearing claim). 1a29's quote verified
   verbatim on their branch: "sound wholesale = n−1 = 355 cores per 10⁴-cell occupancy
   at 1 µs/eval, 1 kick/body/interval on the checker's 28141.5-s clock" →
   10⁹/28141.5 × 9999 × 10⁻⁶ = 355.3, and the unit is per pair-touch per kick. The
   amortization holds under both wirings: a per-pair epoch of E_pair touches costs
   (n−1)/E_pair per kick, and a per-cell batch re-scan every (n/2)·E_pair kicks costs
   n(n−1)/2 per (n/2)E_pair kicks — the same (n−1)/E_pair. 1176's divisor is wrong
   either way. Their quotes ("E_cell ≈ (n/2)·E_pair … ~3.5×10⁻⁴ cores", "140× under")
   verified verbatim on their branch.
3. **Adversarial probes (mine, beyond both grids).** Seed 31337: P=1 column
   7.16×10⁻⁶ at E=2, per-kick falling to 3.3×10⁻⁷ at E=1024; E-shape at P=1024
   saturating 1.07×10⁻³ → 5.83×10⁻² — the same laws. κ = 2⁻²⁹ (64× weaker than the
   quantum): the P=1 column zeroes on seed 777 (which leaked at the quantum) — the
   weak-κ end of the saturation law; certification only strengthens.
4. **The one wrong constant, found independently.** Dossier claim 3 ("e828's coupling
   r = 5×10⁻⁶ is the shipped one") is wrong. Clock-consistent: kick interval
   27.4–27.6k game-s (budget-1e9 page: waves 14.3k/41.7k/69k → step ~27.4k gs)
   against T_syn at the harness's own belt (epochflux.rs:98 `a_lo: 2.0`, window 1e-4)
   gives T_syn = 1.19–4.6×10¹² game-s → **r ≈ 6×10⁻⁹–2.3×10⁻⁸**. e828's 5×10⁻⁶
   divided game ticks (view.rs:23, 4.925 µs) by replica ticks (kepler.rs:29
   `TAU·a^1.5·2³²` per period → 1.169 ms at a=1 = 1 yr): a 237× clock mix × a 6.28×
   dropped TAU, at a=2.5 instead of 2.0. The author's "cross-check" repeated e828's
   formula, so it was not independent. Correction ≈ 10²·⁵–10³×, not the page's
   "~10⁶×" (I fixed the letter, and one stale r·E ≤ 5×10⁻³ → 3×10⁻⁵). Conservative in
   every downstream use: P = 4 is ~10⁸–10⁹× off (deader than argued), and the
   leak certification at E* = 1024–256 gains orders of margin.
5. **Novelty.** No HISTORY entry; the published encounters page carries both
   same-day contradictory paragraphs (355/E vs 3.5×10⁻⁴). This run's paragraph is
   the resolution and corrects a graded-gold constant by 10³×. Goal fit: board live
   question 2; PRINCIPLES "Measure before claiming"; a KILL of 1176's two
   conversions, never of its measurements ("a failed expectation is not
   automatically a failed method").
6. **Predictions.** predictions.md predates the harness and all outputs. P2's
   pre-registered kill test held (355.3 per pair-touch). P4, P5 held exactly.
   The page records P1 honestly ("direction held with its r constant corrected").

**What the author missed.**
- The r constant above: the run whose whole method was "find the unit slip" inherited
  e828's third one; the dossier still asserts it flatly and says "P1–P5 all held".
- Dossier evidence 6's "e828's conservative per-kick bound 8.1×10⁻⁸–2.0×10⁻⁸" is
  neither e828's (their bound is the measured P=1 column: 3.3×10⁻⁶/1.6×10⁻⁶/6.5×10⁻⁷
  per kick at E=64/256/1024) nor a bound on that column (the P=1 per-interval leak
  grows ~128× from E=2 to E=256); it is 5.2×10⁻⁶/E, sound only under the
  game-coupling composition, where the honest bound is smaller still. Certification
  survives regardless — via e828's column at E=1024 (6.5×10⁻⁷ < 10⁻⁶) and via
  r·(miss per passage) under the corrected r.
- The divisor conclusion is wiring-independent (per-pair epoch and per-cell batch
  coincide amortized — worth one line in the freeze wording, since 1176's own freeze
  words it per cell).
- patch.diff contains the harness twice (two identical stanzas); harmless but sloppy;
  regen's fallback copy is the byte-identical one.
