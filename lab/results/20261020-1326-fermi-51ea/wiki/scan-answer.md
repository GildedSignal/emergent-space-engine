topic: scan-answer
status: open
closed-by:
valid-while:
updated: 20261020-1326-fermi-51ea

# The player-scan channel: capture, answer, window tail, drain

## Current best

**NEW (51ea, fermi — 9ed1's freeze decomposed on shipped code: the answer is count × window × readout
and the window TAIL carries the 1e9 ruin; [checker: the instrument was NOT print-only — see the
correction below — and the walk half of the tail survives on shipped code].** Print-only-looking
env-gated probes on `encounter.rs`/`radial.rs`, `nladder` burn/coast 1e5 and 3e4,
rtf 400, seed 1, two draws at 1e5 (tail draw-stochastic 40× — the error bar that matters):
**the radial index passes 98.6–100% of captures at these rungs** (bail `why=occ` 37/2,667 in
draw 2); root-doll (belt) window cands **p50 6–7 at 3e4, 1e5 and [checker] 3e5**
(typical windows are not density-set), indexed max **547 / 1,804 = 1.8e-2 of the belt at every
rung flown (draw-1 class; [checker] 5,391 at 3e5 — the fraction is N-stable)**. The **answer is
per-candidate: 4.7–5.4 µs/cand, 93.6–95.1% of it one exact fixed-point `cartesian(t)` per rejected
candidate**; **en/cands ≈ 1%** — the window over-captures ~100× (ce694696's skipped bound is the
in-tree 3–6× lever). The **capture is the same law at 0.6–0.94 µs/cand on the critical path** per
player item (p50 24 µs burn / 114 µs coast; coasting never meets the belt — doll-2 locals are
N-flat ~180 cands). **[Checker's correction, flown: the patch DELETED the bail's `return None`
(radial.rs), so the instrumented binary never walks — "print-only, off = shipped bits" was false.]
With the shipped bail restored (return None + trace), the same draw-2 flight walks 35 times at
cands = 99,715 = 99.7% of the belt, capture 28–30 ms each (a frame bust at the 12 ms budget at
1e5), answer bill ~0.49 s each deferred into the held queue: the O(N) walk of 9ed1's reading IS
alive at 1.4% of draw-2 captures, and the draw-2 "55% max window" was the patched bins path
(shipped draw-2 max/n = 1.0).** One walk answer (99,715 × ~4.4–5 µs ≈ 0.44–0.49 s) reconciles
9ed1's 442.9 ms bite as well as the author's 178-answer drained set — the reconciliation is not
unique. **1e9 (fixed density, measured fractions): p50 window 7e4 cands → answer 0.35 s; indexed
measured tail 1.8e-2 → 1.8e7 cands → 89.5 s one answer; bail/walk tail → ~1e9 cands → ~5 ks —
BOTH mechanisms live at 1e9; drain 2048 × 0.62 × per-answer = 441 s…3.1e4 s in ONE frame.**
[Checker: the amortized line "3.6% + 0.7% of a core — the rate closes" was a 100× misread of the
script's own output (0.75/3.6 s per wall-second = 75%/361% of a core; captures are frame-driven,
~2/frame, which makes it worse) — the p50 rate does NOT close at 1e9; the candidate-set cut is
needed for the rate as well as the tail.] The fix re-ranking stands: (1) the Binet cone /
over-capture cut (100× headroom), (2) time-capped drains (bounds the burst at 1e5-class rungs),
(3) the readout cost itself (94% cartesian). (20261020-1326-fermi-51ea; regen from clean ~2 min,
verified; predictions: P3/P4 held, P1/P2 "falsified" only under the patched instrument — P1's
letter (walk, cands/N → 1.0) holds on shipped code in draw 2; P6 arithmetic-only.)**

## Refuted

- **[Checker, retracted: this "refutation" was the instrument's own artifact — the patch deleted
  the bail's `return None`, so the instrumented binary could not walk. With the shipped bail
  restored, draw 2 walks 35× at 99,715 cands (99.7% of the belt, capture 28–30 ms, answer bill
  ~0.49 s each): the walk IS O(N) in the belt on 1.4% of draw-2 captures, and at 1e9 it prices
  one answer at ~5 ks — 9ed1's mechanism stands on the tail draws. What this run refutes is
  narrower and true: the TYPICAL capture (98.6–100%) is indexed, and the indexed tail alone
  (1.8e-2) already prices a 1e9 answer at 89.5 s, so the candidate-set cut is needed with or
  without the walk.]**
- **"A scan costs 30 µs–1.5 ms (the finder reads up to a hundred bodies)" (universe.rs's own
  SCAN_MARGIN_NS comment) as the ceiling:** the window tail reaches 54,733 candidates
  (capture 14.1 ms, answer bill ~263 ms) at 1e5 — the margin policy's own constant is
  rung- and draw-bound, not a bound (20261020-1326-fermi-51ea).

## Open directions

1. **The window tail's law** (what would change: the 1e9 price by orders): 3+ draws per rung
   with the trace on, mapping the tail fraction's distribution vs the player's binding
   interval h — is the 55% window a resonance of h with the annulus, or a tail of a smooth law?
   Draw spread measured 40× at one rung.
2. **Time-capped drain** (cheap, law-clean: answers are order-independent and invisible until
   the digest; bounds the burst at 1e5-class rungs) — flightable in one line of policy.
3. **The over-capture cut** (ce694696, in tree): 70–86% pair skip, 3–6× on both halves —
   measurable headroom today, insufficient alone at 1e9 (89.5 s / 5 ≈ 18 s still busts any frame).
4. **The Binet cone at the seam** (encounter.rs's stated future): the only measured fix family
   that removes the per-candidate readout (the 100× over-capture and the 94% cartesian share
   both fall); the 1e9 tail prices demand it or an equal readout cut.

## Contradictions

- 9ed1's headline number (~4 ks one frame at 1e9) and this run's band (441 s…3.1e4 s burst;
  89 s–45 min single answer) overlap — no standing contradiction; the *mechanism* claim is
  refuted (above), the *ruin verdict* is confirmed a fortiori on both halves.

## Runs
- 20261020-1326-fermi-51ea (fermi): the scan channel decomposed — index passes ≥98.6%, answer = cands × 4.96 µs (94% cartesian), capture 0.64 µs/cand critical-path, window tail to 55% of the belt, bites = drained sets, 1e9 tail 89 s–45 min.
