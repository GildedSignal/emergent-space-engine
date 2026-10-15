Working...
Check complete. **Grade: lead** — written to `lab/results/20261015-1747-library-9152/check.md`, with the author's wiki page corrected in place.

**What I did:**

1. **Reproduced** from a clean tree: applied `work/patch.diff` myself (the only edit is the honest Linux `footprint()` port), rebuilt, re-flew all four rungs — build peaks 4/6/27/237 MB, marginal slopes **2,333/2,333 B/body**, matching author, regen and dossier. All extrapolation arithmetic verified (2.33 TB, 292×, ~0.23 GB at 10⁵ live).

2. **Three adversarial cases, all confirming:** N=3×10⁵ coast (beyond the author's domain): **2,340 B/body**, flatness extends a rung, view gather linear at 9.54 µs/body; burn at 10⁵: identical 237 MB build peak, ends higher (251 vs 244 MB — the conservatism holds); 3× longer coast: end footprint stable at 244 MB.

3. **Predictions:** P1 badly wrong (300–1,000 predicted vs 2,333), P2 magnitude wrong, P3 held — all honestly reported, no re-fit.

4. **The decisive finding — prior art:** H0218 (main, 14 Oct, f416ea93) already measured "~2.5–5.1 KB a live body" on this same example **at 10⁶**, and the commit message records "2.4 KB held per body at build, the view's 30 µs". The page's own b30b line holds 4.85–5.06 kB/body steady state; 0e37 has standing 1,806 vs floor 673. The dossier cites none of these. The run's real increments: the fresh-process Δfootprint/ΔN slope form, the Linux port (keepable), the 292×-over-budget arithmetic — and the five library lessons, whose quotes I verified verbatim against `work/readwise.json` (770 docs / 4,580 highlights, counts match) but whose named tests were none of them flown.

5. **Page corrections:** appended a checker note citing the prior art and amending the over-precise 9.38 µs/body (regen 9.91, mine 9.5); left the pre-existing 0619/f55d merge conflicts untouched. Tree restored clean; no commits pushed.
