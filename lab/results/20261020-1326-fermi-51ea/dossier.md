# Dossier — 20261020-1326-fermi-51ea

**Claim:** The scan-answer freeze (9ed1) is not an O(N_belt) walk: it is **(drained-answer count) × (window-candidate count) × 4.96 µs/candidate**, the window tail (not the typical scan) carries the 1e9 ruin — one measured tail window held **55% of the belt** — and both halves of the channel, capture and answer, are **readout-bound** (one exact fixed-point `cartesian` per candidate, 93.9% of answer time; `binding_at` at 0.6–0.94 µs/candidate on the critical path).

**Bottleneck:** board item 1 (bodies: 28 → 10⁹), the named next freeze target (9ed1: "the exact player-neighbourhood check's answer ... at 1e9 a walk ∝ doll population is the allocator's true ruin"). This run replaces the checker's mechanism inference with the measured decomposition, which re-ranks the fixes: the drain policy caps the *burst* but nothing scheduling-side fits a single tail answer at 1e9 (measured: 89 s–45 min); only a candidate-set cut (the Binet cone, the seam's own plan) or a ≥100× per-candidate cut closes the tail.

## Evidence (all numbers regenerate: `regen.sh`, ~4 min; this box, load ~1–2.5)

Instrument: print-only, env-gated (`ES_SCAN_TRACE`), off = shipped bits; three probes — per-capture (n, walk/indexed, near, cands, µs, µs-per-candidate), per-answer (cands, en, µs, cartesian µs, wall epoch), per radial-bail (reason, hit, unbounded, bodies). Plus the nladder Linux footprint stub (`/proc/self/status`, the macOS probe's stand-in). Flights: `ES_SCAN_TRACE=1 …/nladder <N> <burn|coast> 40–55 400`, seed 1, 12 ms budget.

- **The radial index does not fail at the rungs that matter** (P1's letter falsified, refined by draw 2): 2,595 captures at 1e5 burn draw 1 — **0 bails**; draw 2 — 37 bails (1.4%), all `why=occ`, each triggering the full 0..n_bodies walk (capture max **14.1 ms**). Root-doll (belt) window cands: p50 **6–7** at BOTH 3e4 and 1e5 (not density-set), p90 55→174, max **547 → 1,804 → 54,733** across draws (max/n = **1.8e-2, 1.8e-2, 5.5e-1** — the tail ∝ belt density within a draw, draw-stochastic by ~40× between draws at the same rung).
- **The answer is per-candidate, not per-body:** cand_us p50 **4.71–5.16 µs** (p99 ≤ 9.3) across all arms; **cart share 93.8–95.1%** — the cost is one exact `cartesian(t)` of the candidate's compiled orbit per rejected body. en/cands ≈ **1%** (en p50 = 1): the window over-captures ~100× (encounter.rs's own skipped bound, commit ce694696, would cut 70–86%).
- **The capture is the same law at 1/8 the price:** 0.60–0.94 µs/candidate (`binding_at` + filters), **on the frame's critical path**, per player item; captures p50 24 µs (burn) / 114 µs (coast: player never leaves the locals' doll — coast cands are N-flat at ~180, max 194; the belt is never met while coasting).
- **No single answer explains a bite:** max answer in-flight **7.5–8.1 ms** (1,804 cands). 9ed1's bites reconcile exactly as drained *sets*: **442.9 ms ÷ en 178 = 2.49 ms/answer = cands ~502 × 4.96 µs** (mid-tail); 1,273.5 ÷ 178 = 7.15 ms = cands ~1,442. f_d (distinct fraction of captures) = **0.61–0.62**; backlog cap 2048 ⇒ 2048 × 0.62 × per-answer is the burst ceiling. The two 1e5 draws here did not catch a bite frame (draw-stochastic, 1-in-3 per 9ed1; disclosed) — the burst-count reading is [INFERENCE] from the en-arithmetic + backlog cap, not a caught frame.
- **The biggest answers defer:** draw 2's 54,733-cands scan (answer bill ~263 ms) was still held at flight end — the tail answers land at settle/digest, a second concentration path behind the drain.
- **1e9 composition** (fixed density; window fractions from 1e5 draws; cand_us 4.96, capture 0.64):
  | window | cands at 1e9 | one answer | one capture (critical path) |
  |---|---|---|---|
  | p50 (7/1e5) | 7.0e4 | 0.35 s | 0.045 s |
  | mid-tail (~500/1e5) | 5.0e6 | 24.8 s | 3.2 s |
  | measured tail (1.8e-2) | 1.8e7 | 89.5 s | 11.5 s |
  | draw-2 tail (5.5e-1) | 5.5e8 | ~45 min | ~5.9 min |
  Amortized at play rtf 100 the p50 channel is cheap (capture 0.7% of a core, answers 3.6%) — **the ruin is the tail and the burst, not the rate**: 2048 × 0.62 × per-answer = 441 s (p50 windows) … 3.1e4 s (mid-tail) in ONE frame. The checker's "~4 ks at 1e9" sits inside the measured band with the opposite mechanism.

## Predictions (predictions.md, written 13:52/13:56 before the flights)

P1 **falsified as written** (0 bails in draw 1; 1.4% in draw 2 — rare but real, and the walk exists); P2 **falsified** (no per-body capture walk at these rungs; the capture is 0.6–0.94 µs/candidate, p50 24 µs); P3 **held** (cand_us 4.7–5.2, cart 94%); P4 **held and sharpened** (the ≥100 s bar is passed by the tail windows, 89 s–45 min per single answer; a per-candidate cut of 3–6× leaves the tail ≥ 15 s — only the cone's ~100× candidate cut, or an equal readout cut, closes); P5 **half-held** (coast shows the same indexed structure but never meets the belt — the doll split is the correction); P6 (appended after draw 1) **held by arithmetic, not by a caught frame** ([INFERENCE], above).

## What would make it wrong

A caught bite frame whose answers-per-frame is ≤ 5 (then the burst law dies and the bite is elsewhere); a third draw showing the tail fraction bounded ≪ 1e-2 (then the 1e9 tail prices collapse toward the p50 row); M1 timings differing in kind (x86 here; orders only). The window fractions are 2 draws at 1e5 + 1 at 3e4 — the tail's draw spread (40×) is itself the error bar that matters.

## Cost of adoption / fit

Nothing to wire (measurement + decomposition). For the integrator's named target: the fixes re-rank — (1) the Binet cone or the window's over-capture cut (100× measured headroom: en/cands = 1%); (2) a time-capped drain (bounds the burst at 1e5-class rungs; cannot fit a tail answer at 1e9); (3) per-candidate readout cost (the exact `cartesian` is 94% of the answer — the cheap-bound commit ce694696 is the 3–6× lever already in tree). PRINCIPLES #1 ("the cheapest compute is compute not done" — 99% of the readouts buy nothing), #3 ("compute only surprises"), #34 ("the oracles are guards, not shepherds").

## The lens (Fermi)

The estimate that mattered was the rejection one: the checker's 4.3 µs/body and my O(en) alternative both fit three rungs at fixed density; the falsifier was the *decomposition* (cands and cand_us measured separately), which killed the walk mechanism while confirming the headline band. What the lens missed until draw 2: the tail's draw stochasticity (40×) — the wiki's own ≥3-flights rule applies to window tails, not just to wall integrals.

## Reproduce

`bash lab/results/20261020-1326-fermi-51ea/regen.sh` (applies `work/patch.diff`, builds, flies the four arms sequentially, runs `work/analyze.py`). Each flight ≤ 60 s; total ≈ 4 min.
