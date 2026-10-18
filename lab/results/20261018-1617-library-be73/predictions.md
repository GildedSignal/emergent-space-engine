# predictions.md — written before compose_fix.py and verify_quotes.py ran

Target: the scan pin's fix ("answer-or-expire", named by acf2 on the nladder page,
2026-10-18 15:30) composed from page-cited constants. All inputs are other runs'
published numbers; the predictions below are my hand arithmetic BEFORE the script.

- P1 (the one-doll bust law): t_8GB(K) = 8e9 / (λ·224·(K+38)) with λ = 0.0526/gs
  regenerates acf2's measured 687 game-s at K = 10⁶ within 5% (my hand: ~679 gs),
  and acf2's "~1 game-s at 10⁹" within 2× (hand: 0.68 gs).
- P2 (the count-cap's byte edge): the 2048-entry cap binds 8 GB at
  K = 8e9/(2048·224·m) − 38; at m = 1 entry/mint → ~1.7×10⁴, at m = 1.95 (acf2's
  measured entries/mint) → ~3.4×10⁴, i.e. acf2's own "K ≲ 3.4×10⁴" band falls out
  of the byte law with no new constant.
- P3 (the answer half's cost): per-frame arrivals 0.0526 × 1.5 gs/frame = 0.079
  mints/frame. In the fix's own forms the answer stream is ≤ 0.5% of the 12-ms
  budget at 10⁶ (compare-form 0.515 ns/member → ~41 µs/frame; store-grounded
  0.67 ms/scan → ~53 µs/frame) and ≤ 3.5% at 10⁷; in the SHIPPED walk form
  (~190 ns/body) it is ≥ 100% of the budget at 10⁶ — the form, not the policy,
  carries the cost.
- P4 (the spike): ONE forced answer at the latch in the shipped walk form is
  190 ns × K = 19–44 ms at K = 10⁵–2.3×10⁵ (acf2's letter), busting the 12-ms
  frame at every K ≥ 6.3×10⁴; the same answer in the compare form is 380× cheaper.
- P5 (the supersede bound): with expiry on the census's own supersede triggers,
  the steady pin is the question's structure, ~1.9–2.0 entries/mint (acf2) →
  ~2 × (D+38) × 224 B: at D = 10⁶ that is 425–448 MB, ≥ 17× under the 8 GB wall,
  and the partition ceiling is D ≈ 1.7–1.8×10⁷. This bound is load-independent
  (it no longer depends on the drain margin µ), so b8e2's utilization knob
  (µ/λ = 1.0 quiet vs 0.03–0.15 loaded) can no longer grow memory.
- P6 (held-out quote property): all five lesson quotes carried in the dossier are
  byte-identical fragments of the fresh export (5/5), searched over all 4,590
  highlights; author/title attributed as in the export.

What I expect to be the composition's headline (falsifiable): at the fix's own
10⁶ target the answer half is not the wall — the trigger is. Answering every mint
at arrival in the fix's form costs ~0.4% of the frame budget; the only way the pin
reaches 8 GB at 687 gs (as measured) is answers never firing AND nothing expiring.
