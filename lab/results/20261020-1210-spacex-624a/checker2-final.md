Working...
**Grade: gold** — written to `check2.md`, with two amendments to the author's `wiki/mint-knots.md`.

**What I did:**

1. **Reproduced every number** independently from the raw census rows: fleet 1,104,124 knots / 105,241 panels touched (90.3% never landed), medians 14.3%/0.68%, big-tail 5.1%, 399,440 = 39.8% of cycle knots. Digest neutrality holds on all ref/cen pairs; the runner's regen exited 0 with matching output. ("21,449" is an arithmetic slip for 21,520 — already fixed on the page.)

2. **Ran four attacks** (fresh pristine+patched builds, arms in `work/ck2-*.json`):
   - **Instrument attack** — the circular fast path bypasses the knot table, so dead mints could fake the headline: measured **zero-touch mints = 0 on every arm**; every counted mint was live. The author never ran this check.
   - **Seed 11** (held out): never-landed 91.6%/94.1%, medians 10%/0.7% — same law; 36/25,468 cycles (0.14%) reach 0.9, *above* the page-note's 0.007–0.07% range, so I amended the note.
   - **55 s lifetime attack**: coverage stays flat (18.2% median) — long lifetimes don't rescue the eager span.
   - **rtf 10000** (two decades beyond the author, one beyond the page's probe): never-landed 80.0%/98.6%, zero of 157,906 mints ≥ 0.9 — over-provisioning *worsens* with rtf. replay_digest repeat-stability confirmed.

3. **Novelty/goal fit**: the topic page's open direction 1 named exactly this measurement as unmeasured; nothing in HISTORY prior. It kills the class-split fork (waste tracks walk, not class) and prices the lazy sums-spine lever at 4–7× (ceiling 10×) on both scoreboard rows — "Compute only surprises" (#3), "a fix signals the wrong representation" (#19).

**Caveats recorded, not grade-changing**: pricing constants are bd4b's (awaiting grade; this arm implies ~1.9–2.5 µs/knot, a factor-~2 spread the adoption estimate should carry); the spine cut is priced, not flown; the belt cadence stays the honest residual fork. Tree restored clean; no commits made.
