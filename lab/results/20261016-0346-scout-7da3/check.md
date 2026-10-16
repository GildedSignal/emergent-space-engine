Grade: silver

**Abstract.** The window-level claim reproduces exactly: budget-free at 10⁵/3×10⁵ the staggered train shows no re-concentration at any of four wave positions (top 250-s windows 2,700–2,775 / 6,288–6,366; every event count bit-exact on re-run; period 14,167 game-s, decay ×0.66–0.72; I extended it to 10⁴: wave windows 1,090 vs unstaggered 5,109). But the headline letter arithmetic is refuted: flying the letter's own width (rtf 100, budget-free, 42k game-s) the staggered worst frame is 342/366 events at 10⁵/3×10⁵ — 5.1–7.5× the ÷10-converted 45.5/71.1, and N-flat (a ~660-s sub-grid beat, not the belt stream). Corrected: staggered letter break ≈ 6×10⁵ (below memory 1.3×10⁶, +7× not +20–26×); composed 10⁹ ≈ 0.7× the letter at the key arm (band bottom, not 2.2×). Adoption cost unchanged (ed3a's 14-line patch); the cure stands, the numbers don't.

## Reproduction (runner's regen + my own re-derivation from the CSVs, independent code)

- Deterministic structure bit-exact: max ev/frame 4,243/455/12,729/711; wave positions 14,167/28,317/42,483/56,617; totals 588,464/465,665/1,388,464/1,019,581; off-arm crest regeneration 87%/96% of the record's rtf-100 anchors; events −21/−27% on-arm. All re-derived with my own code from the CSVs, not `analyze.py`.
- Timings are load-dependent: the author's 50.8/53.6 µs/ev on birth-wave peaks read 78.8/74.5 in the runner's regen (shared box). P4's µs/ev bar (40–55) holds only on the author's own load; the event anchors are exact.
- `work/patch.diff` is minimal and correct: one env-gated hunk in `step.rs` (t=0, Ship only, off = `t + half`, shipped verbatim by construction) plus the instrument example. Predictions.md (03:53) predates analyze.py (03:55) and dossier (04:01); the author's work logs were overwritten by regen, so log order can't be fully audited — timestamps are consistent with predictions-first.

## Predictions

- P1 FAILED as written (455 ev / 16.5 ms vs bars 150 / 8 ms), disclosed. The author's diagnosis — "in the letter's own frame width (45.5 events / 1.65 ms) it passes with margin" — is itself wrong: measured at rtf 100 the worst frame is 342 events = 10.0 ms at the M1 rate (25.5 ms this box). P1 fails at every width against a fixed-event bar.
- P2 FAILED as written (crest 1.56× for 3× N), disclosed; diagnosis (fluctuation-dominated) incomplete — the crest is N-flat because it is a sub-grid beat, not a belt statistic.
- P3 held decisively, and holds beyond the author's domain at 10⁴ (my flight `chk_10000_on`: wave windows 1,000–1,101 events; kill bar was ≥ 2,555 = 50% of the unstaggered 5,109).
- P4 held in events and density; µs/ev only on the author's load (above).
- P5 FAILED in its number while meeting its letter (≥ 10⁶): the true break is ≈ 6×10⁵ by the corrected arithmetic.

## Adversarial (all budget-free, `chk_*` in work/)

1. **Letter-width flights (rtf 100, 42k game-s, 25,200 frames, 10⁵ and 3×10⁵): worst frame 342/366 events, N-flat** — the ÷10 conversion the break-N rests on is refuted 5.1–7.5×. The crest is a beat of ~200–350 events at exactly 660/662-game-s spacing (identical positions in both arms and both rtf; the off arm's inter-wave train shows the same class at 333-s spacing, tops ~454 at rtf-1000 width). At the M1 rate the letter holds at both N (10.0/10.7 ms < 12); the first N-scaling term is the smooth stream (4.62×10⁻⁵ ev/body/game-s), breaking ≈ 6×10⁵. Zero frames ≥ 410 events anywhere in either flight.
2. **10⁴ staggered through wave 2** (the author's named held-out): no window at any wave position reaches even the 6th-highest window; kill bar cleared 2.3×.
3. **Window-distribution audit**: past 15k game-s the staggered train's 250-s windows span 1,544–2,775 (bimodal: beat/no-beat), not "uniform ±3–4%" — only the top windows are flat. No spikes; the P3 substance is unaffected. Page corrected in place.

## Novelty

The rung was nladder open direction 1 (pin the staggered break and the composed 10⁹ letter) — aimed correctly, and the record's own instrument rule ("wave arms must fly budget-free") was half-applied: budget-free yes, but at rtf 1000, then ÷10-converted against the record's rtf-100 anchors. The "never flown staggered anywhere past wave 1" premise overstates: ed3a's published birth-stagger page already flew staggered through the 41–44k window (under the 12-ms budget, which clamps crests — so this run's budget-free version is a legitimate strengthening, not a repetition). New and standing: the 14,167-s period, the ×0.72 decay, the 50-vs-12 µs/ev birth-wave cost, and the permanence at four periods.

## Goal fit

Aimed at board live question 1. The wave is genesis phase-lock, not physics; spreading it is PRINCIPLES #3 ("compute only surprises") and #12 (spike compute). The corrected result keeps the qualitative conclusion — the stagger deletes the belt's coherent wave from the letter, and (stagger ∧ key-arm kick) fits the 10⁹ letter at ~0.7× — while the run's specific numbers (1.7–2.2×10⁶, "past the memory break", "~2.2× composed") are wrong by ~7× and are corrected on the page.

## The one experiment to gold

Fly the letter's own instrument — rtf 100, budget-free — as the rung's arms (done here, `chk_*_r100long`; a rerun on an unloaded box with the beat attributed to its owning doll, plus one N between 3×10⁵ and 6×10⁵ to catch the beat+stream crossing, makes the corrected break a measured number rather than my extrapolation).

## What the author missed

The record's own lesson (a 12-ms arm reports the cap; an rtf-1000 arm reports a 10×-averaged crest) was applied to the budget but not to the width: the whole letter arithmetic converted a wide-frame crest by ÷10 instead of flying the letter's width, which the example supports natively. Also missed: ed3a's published wave-2 row (overstated novelty), the beat structure sitting under the "flat" train (visible in the author's own CSVs as bimodal window sums and ≥200-ev rtf-1000 frames between waves), and P1's failure was diagnosed with the same broken conversion that caused it.
