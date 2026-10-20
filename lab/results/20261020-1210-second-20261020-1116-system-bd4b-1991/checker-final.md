Working...
Check complete. Verdict written to `check.md` in the run folder; the tree is clean (no source edits remain; the author's patch was applied only to reproduce and then reverted).

**Grade: gold** — with evidence:

**Reproduction (bit-for-bit).** All four arms regenerate every deterministic field of the stored JSONs. Stronger than regen.sh: I built the **unpatched shipped tree** and confirmed it produces the same digests (`b42da477294f7619…`, `8c242b023e8b79e4…`) — the census is genuinely print-only. Constants audited in source: `PSI_PI` = `tables::PI`, `scale(-1)` = ÷2, release at `outer_radius/2`; the bracket/unwrap logic is correct including edge cases.

**The one hole, filled by my probe.** The author's horizon control never fired at 30 s (disclosed). At 300 s it fires: **2300 repeat mints across 345 bodies — 93% land exactly on the planned/estimated t1, never early, worst 8.5×** (late rows are carried sub-quantum kicks, `step.rs:426-429`). Corrected never-read with true horizons: median 0.987, no row below 47%. The claim is conservative-robust. Adversarial seeds 4/5, populations 100/800, and the 55 s default all hold the class structure.

**CPU-kill verified in code**: `step_for` (`step.rs:75-78`) reads `period()`/`duration()` at the latest one boundary after the mint — a lazy compile defers the traversal at most half an interval, never deletes it.

**Page corrected in place** (overstatements, not measurement errors): the "~interval/8 nested sub-kick" mechanism — measured walk ÷ interval = 1.000 on all 2645 rows — and the tail's "≤ 1e-4" (seed-1-only; seeds 2–3 reach 7e-3 with never-read still ≥ 93%). Also noted: passage tail panels/bytes uncounted — conservative for both claims.

**Predictions**: P2/P4 held; P1/P3 failed as the author's own priors, disclosed in bold — the failures are the finding (bd4b's premise refuted), and the pre-registered kill criterion did not trigger. Novel against 4ea0 (memo generations) and history-demand (history stock): the walked-span-by-class measurement is new, exactly as the page's checker scoped it.
