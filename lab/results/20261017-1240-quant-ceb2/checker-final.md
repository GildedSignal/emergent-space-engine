Working...
Check complete. **Grade: gold** — `lab/results/20261017-1240-quant-ceb2/check.md` written.

**Reproduction:** Patch applied clean on base 0d86cb4e. Sizes and both wave arms bit-identical to the author's regen (e.g. 577,535 allocs / 650,057,850 B / 34,537 kicks at N=3000 — identical across four executions); micro within the stated wobble (read cold delta 3.2–3.8 µs vs claimed 3.0–3.9).

**Predictions:** Written 12:48, before the decisive arms (12:57). #3 (wave byte bill, held-out N=10000) and #4 (roofline acquittal) held; #1/#2 killed by their own pre-registered rules and honestly reported — the shared-footprint diagnosis is real and verified.

**Attacks (all outside the tested domain):** N=1000 → 19.7 KB/kick, N=30000 → 9.6 KB (mix envelope 9.6–19.7 KB; allocs 15.5–16.9 flat; still ≥43× under compute); 2× flight stable; e=0.999/0.9999 (knots 177/230, a decade past 124) keep the cold tax flat with data-only ≤0.6 µs (≈0 at 230 knots — the knot table is even more innocent than claimed); p=7 e≥0.6 is `NoBoundOrbit`, the law's own domain edge. No claim overturned.

**Novelty:** No prior event-path byte/bandwidth measurement anywhere in the wiki or HISTORY; memory-h-live's compute ≫ bandwidth ordering prices a different stream (persistence, not events).

**Page:** Faithful; corrected three overstatements in place (hot band is 1.9–3.1 µs at planet keys / 5.0–5.2 at p=7, not 2.9–3.3 everywhere; shared share 62–92%, not 75–85%; Vec churn 2.2–4×, not ~2.2×) and appended a checker bracket with the extended envelope. Tree left pristine; probe example removed; nothing committed or pushed.
