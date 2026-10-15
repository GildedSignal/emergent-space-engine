Working...
Check complete. **Grade: silver** — written to `lab/results/20261015-1338-quant-1d52/check.md`, with a checker note folded into the proposed `wiki/nladder.md` (the page's established italic-note convention).

**What I did:**
- **Reproduced** from a clean tree: re-applied `work/patch.diff`, rebuilt (no source drift), confirmed every deterministic number — all four scenes' digests, demotions/promotions (41,053/131,053/273,200/39,459 = demotions exactly under retention), hits 763,888/715,422/2,436,522, and the anchors `2109a2e0…`/273,200. Only load-dependent walls differed (seam compile 12.41→13.34 s), which the dossier scopes as order-of-magnitude. Lib+tests: 77 passed, 0 failed (the `nladder` example's Linux link failure is pre-existing macOS-only code, untouched by the patch).
- **Five adversarial cases, all outside the author's flown domain — every one confirms:** burn (never flown by the author: identity, promotions=demotions 40,187, 93.6% hits, compile 15.5×); mid-N 3×10⁴ and 2×10⁵ (hits **exactly 763,888 at both** — and demotions = belt + 31,053 at every rung, turning the "hot set is the locals" inference into arithmetic); a 100k-game-s deep cut (identity; **retained_now plateaus at 2.0×N** — bounded, a flat +3% rss); `ES_RETAIN` alone inert.
- **Novelty:** no retention build exists anywhere in docs/wiki/history; e0f9 only named the rule. The run corrects the integrator's open call #1: "keep until the next kick" deletes the CPU bill exactly but erases the memory win.
- **Why silver, not gold:** the run's own conclusion is that the configuration it flew (global retention) should not be adopted, and the rule it recommends (bounded hot cache) is explicitly named-but-not-built — one ~30-line flight away, same shape as 760f→e0f9 on this page.
- Predictions were pre-registered and held (P1/P2/P3/P4/P6); flagged that P5 was an unfalsifiable either/or, honestly reported. The one new caveat for the integrator: the retain arm's wall residue over shipped grows ~linearly with wave count (+0.7/+2.8/+8.8 s at 20k/48k/100k), though the hit stream itself is N-independent.

Tree restored exactly as found; nothing else in the run folder touched.
