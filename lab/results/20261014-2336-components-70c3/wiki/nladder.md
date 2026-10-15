topic: nladder
status: open
closed-by:
valid-while:
updated: 20261014-2336-components-70c3

# The N ladder: 28 live bodies toward 10⁹

## Current best

**Break 4's promotion is priced and its error discipline settled: the smallest promotion is a carried integer drift on the compact row — 636–678 ns/kick, 80 B standing, error bounded at 16 km after 2,560 kicks, while the re-rounding alternative walks linearly to 0.2 AU (5×10⁸× worse at the same quanta) (20261014-2336-components-70c3).** In miniature (SI replica calibrated to the shipped stream: |dv| p50 4.4×10⁻³ m/s, |Δa| ≈ 4.1×10³ quanta/kick vs a669's dL/L 2.1×10⁻⁷ and p01 2.4×10³ quanta): base element words frozen, kicks sigma-delta'd into separate drift words, one Kepler readout + tide + exact element update per kick, nothing compiled — fired 12.8M/12.8M = 1.000, ~93–120× under the shipped in-wave 59–76 µs/kick and 29–64× under the shipped 2.3–5.1 kB/body (Linux regen: build 39–45 µs/body, b_per_body 2,347–3,461 at 10³–10⁵, frame p50 0.039 ms flat in N). The load-bearing separation: **the quantized-memo walk is a feedback effect of re-rounding the state each kick, not of sigma-delta truncation** — requant's consumer error grows linearly in kicks (2.2×10⁷ → 4.9×10⁸ m over 20 waves) while the carried drift saturates below its wave-1 value (7.3×10⁴ → 1.6×10⁴ m) — so law.md's random-walk objection does not reach a row that never re-rounds. Misses, pre-registered: cost 636–678 ns against the 150 ns bar (the probe pays a full exact element re-derivation per kick; the linearized Gauss response on the solved readout is the named ~2–4×, not built), row 80 B against ≤40 (four channels carried, not two). Not paid in the miniature: queue, plan, demotion, and one `Orbit::compile` per consumer window (~30–75 µs once, vs 128/wave shipped). This page's proposal folds into whichever side of the standing conflicts survives.

## Refuted

- (this run adds none; it prices break 4's design rather than killing a shipped term)

## Open directions

1. (from this run) Replay **dumped shipped kicks** (`kick_clock`'s Δ-elements on the real wave) through both disciplines, and build the linearized response for the cost side — the two named steps from silver to gold; then the promotion wiring itself (the belt's event on the compact row and back) behind the cadence decision (break 1).

## Contradictions

- (the page's standing conflicts are the integrator's; unchanged by this run)

## Runs
- 20261014-2336-components-70c3 (this run, awaiting grade): the smallest promotion priced — carried integer drift on the compact row: 636–678 ns/kick, 80 B, bounded error; re-rounding walks 5×10⁸×.
