Working...
Check complete. **Grade: silver** — written to `check2.md`, page corrected, tree restored (my `finframe2.rs` experiment removed, author's patch reverted to found state).

**What held (the core):**
- Frames-mode reachability reproduced: my fresh window crashed **3/6** at the decisive arm (rate 600, n=120, author's binary, gaps 16–64 = 1–4 strides), plus 3 author panics on disk and the runner's n=240 crash. Chunked 2/2 again (12/12 across four sessions).
- Pre-registration verified by mtime (predictions 08:45:49 < first drift run 08:45:55); P1–P4 held, P5 honestly missed.
- Novel: decides the published page's open direction 2 (9b46: "untested"). Mechanism verified in code (`alloc.rs:1451` inside the stride-start walk; publish at 1759/1777; `release_cap` at 1752).
- Adversarial outside range: n=480 (1,920 bodies) 0/2, n=60 0/2, Q/4 closing 0/3 — all clean.

**Why not gold:**
- "Never with slack (rate 300: 0/6)" is contradicted by the run's **own `out/`**: two undisclosed, uncounted panics labelled `r300a`/`r300b` (plus `r1200a`), and my fresh window crashed 1/6 at rate 300 — rate-300 total 3/22 draws. The band is a gradient, not a wall (this strengthens reachability, but the printed claim is false).
- Author-window counts (10/14, 3/3 chunked) not regenerable from artifacts; "surviving frontier > 2100" wrong (actual 1408–1456).
- The ahead cap was dismissed from one value; my sweep (3/6 crash at 0.25 s vs 0/3 at 0.05 s and 1.0 s) leaves its role unsettled — folded into the page's open direction 2.

One experiment to gold: a disclosed rate-300 recount (≥6 draws, acknowledging r300a/b) with the incidence restated as a gradient — the reachability core needs nothing more.
