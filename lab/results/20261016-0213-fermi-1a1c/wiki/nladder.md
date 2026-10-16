topic: nladder
status: open
closed-by:
valid-while:
updated: 20261016-0213-fermi-1a1c

# The N ladder: 28 live bodies toward 10⁹

## Current best

**The 10⁹ budget of the flyable plane is assembled on merged main, and the record's wave reading
was an instrument artifact: the belt's unstaggered first-kick wave — whose TRUE peak frame is 487
events / 22.95 ms budget-free at 10⁵ (47–51 µs/event this box; 36.1 ms under load; 14.3 ms at the
M1's 29.3 µs/event) — already violates F1's 12-ms letter at 10⁵ [checker: confirmed beyond the
author's range — 3×10⁵ budget-free peaks at 1,328 events / 71.7 ms; scaling exponent 0.91, so the
letter break-N recomputes to 8.3×10⁴, the author's 8.4×10⁴; the paired 12-ms arm on the identical
10⁵ flight reports max 11.99 ms / 334 events — the cap, not the wave], and after2's "the wave
holds at 3×10⁵" (max 11.95–12.00 ms, ~409 events) was the 12-ms budget CAP reporting itself as
the peak (~410 events is what a 12-ms M1 frame processes; the excess is deferred into window
slack, lag 0 — playability holds to the throughput break ≈ 1.0×10⁶, the letter does not)
(20261016-0213-fermi-1a1c, Fermi lens, budget-free flights + budget.py).** Ranked break-Ns
(M1-projected, rtf 100, 12 ms × 60 fps,
~6 GB): view gather (page-side) 1.2×10³ → **wave, F1 letter 8.4×10⁴** → wave throughput 1.0×10⁶ →
memory 1.6×10⁶ at the 4 GiB gate (post-first-kick standing is 4,750 B/body measured, break
1.3×10⁶) → build 2.1×10⁶ (8.0 M1-core-hours at 10⁹, one-time) → steady event stream 1.6–8.1×10⁷
(49–243 cores at 10⁹ by three rate anchors: the doll law 128 kicks per Cinder period, this run's
post-wave residue 4.5×10⁻⁵, ed3a's plateau 8.3×10⁻⁵ — bracketing cf45's composed 148×; no 10×
disagreement) → player scan 5.3×10⁷ (one held scan pins 113 GB at 10⁹). The first-kick window is
N-independent (13,051–14,542 game-s at 10⁴ and 10⁵, width 1,491). Composed end state at 10⁹:
every compute term fits ONLY as (ES_STAGGER ∧ kick-at-the-0.11 µs-key-arm) TOGETHER — each lever
alone leaves 45–11,900× over (wave letter 1.19×10⁴ unstaggered → 2.7× with both, ~0.5× by ed3a's
own staggered-birth composition); steady stream 0.19–0.91 cores at the key arm; memory stands only
phase-locked (5.0 GB; the 126-bit driven floor is 15.8 GB = 2.6× the machine). Instrument rules for
the next rungs: wave arms must fly BUDGET-FREE (a 12-ms arm reports the cap as its max), and the
locals' N-independent event storms (10–15.6 ms frames at every N, the 300 locals + exodus) sit
under every wave number — the 20-s letter's binder is that baseline, not N. Consequences:
ES_STAGGER is load-bearing for any flight reaching 13–14.5k game-s (built, default-off); the lever
order is wave cadence, then the standing store, never the frame walk (p50 0.007–0.039 ms flat to
10⁵ on Linux: the walk fix holds off the M1 too).

**[Prior best retained — see lab/wiki/nladder.md's standing text: the plan-pass attribution and
hoist (cfe5), the view-walk deletion (d86c), the burn-mint ruin and SCAN_BACKLOG mis-sizing
(51b7), 404b's birth-rail split, the scout's last-segment floor, the depth axis (398f/57ec), the
seam/retention family (e0f9, 0757, b0ed, quant-0619, f55d), 8b89's ES_LAZY_ALL, b172's formation
falsifier, 1343/3dc8's passage pricing). This proposal folds the assembled budget in; the merge
resolves against whatever side of the page's conflict stands.]**

## Refuted
- **"The wave's frames hold" at 3×10⁵ (after2's BEYOND-THE-GATE table, max 11.95–12.00 ms,
  390–458 events, and 51b7's same-hour page line "the wave's frames hold under the merged
  fixes"), and any break-N read from 12-ms-budget wave arms:** the reported max is the budget
  cap, not the wave — the checker flew the identical 10⁵ flight both ways (12-ms budget: max
  11.99 ms / 334 events; budget-free: 487 events / 36.1 ms), and 3×10⁵ budget-free peaks at
  1,328 events / 71.7 ms = 38.9 ms at the M1 rate, 3.2× the letter; the F1 letter breaks at
  ≈ 8.3×10⁴ (0.8–1×10⁵); the budget converts the peak into absorbed deferral (lag 0) until the
  throughput break (20261016-0213-fermi-1a1c; checker arms in its check.md). Caveat: on slower
  boxes the N-independent exodus frame (15.6–16.8 ms budget-free) already exceeds the letter at
  every N — 8.3×10⁴ is the first N-scaling break, M1-projected (the M1's exodus fits: 9.6–11.6 ms).

## Open directions
1. **Fly the staggered wave at 3×10⁵–10⁶ budget-free on main** (ES_STAGGER default-off): predicted
   peak ≈ 487/16.7 ≈ 29 events ≈ 0.9 ms at 10⁵, and the staggered-break at ~1.4×10⁶ — just under
   the memory break; that composes the birth at 10⁹ with the key-arm kick (0.5–2.7× the letter,
   the one number this budget could not pin).
2. (prior directions stand: the shared "planets at t" readout, the compact store's wiring, the
   cadence law, the page's standing conflicts for the integrator)

## Contradictions
- The page's standing merge conflicts (main vs d86c vs 51b7) remain the integrator's; this run's
  section is additive and sides with neither.

## Runs
- 20261016-0213-fermi-1a1c (this run, awaiting grade): the assembled 10⁹ budget on merged main —
  the wave's true peak breaks F1's letter at ≈ 8×10⁴ (after2's 3×10⁵ was the budget cap); at 10⁹
  compute fits only as stagger ∧ key-arm kick together.
