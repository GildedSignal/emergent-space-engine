Working...
Check complete. Verdict: **Grade: silver** — written to `lab/results/20261021-0142-q-compile-promotion-e094/check.md`, with four stale grade tokens corrected in the author's page.

**Reproduction** — `./regen.sh` exit 0, every dossier number identical (407/234 → 87/13; census 546→542 verbatim/4 behind runs/0 lost; runs 14 ids kept; five headline numbers verbatim). Predictions genuinely pre-registered (mtimes 01:48 < 01:54 < 01:55 < 01:56). Budget-rule citation accurate at `lab/wiki.py:88`. Sandboxed shipped `wiki.py index` on the compiled page reads no over-budget flag.

**Adversarial passes:**
1. **Independent census** (different tokenizer, short tokens included, comma artifacts caught before they misled): exactly the author's 4 absent tokens and nothing more — all non-load-bearing, all behind cited runs. Every truncated-tail probe (formation arm, seam checker block, control matches) present. The 0-lost claim holds under a stricter instrument.
2. **Adoption path** (outside the author's tested range): replicated `wiki.py apply`'s literal Runs union — merged page lands at 104 lines (flag disappears, unlike nladder's 322) but `## Runs` re-inflates 14 → 32 lines with 13 duplicated ids. The dedup doesn't survive adoption; the dossier omits the caveat two prior compile checkers already named.
3. **Grade tokens audited against the integrator's log** (not branch check.md — they disagree where second checkers overruled): corrected c4d3 → gold, b083/396d → silver, 4f59 → gold; 760f's "silver" was already right. Verifier still PASS after corrections.
4. **One silent number change**: mint p50 "3.7–5.3" → "3.7–5.6" (self-consistent with both pages' 5.2–5.6 sub-arm, but undisclosed — flagged).

**Not gold** for the same reason all six prior compiles are silver: no board row, component, or premise moves — the compile genre's ceiling. The one gold experiment: make `wiki.py apply`'s union id-aware (deletes the dup-line disease for every future compile), then push the page through the real apply+index.
