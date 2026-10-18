Working...
Check complete. **Grade: gold** — written to `check2.md`, with corrections on the run's wiki page.

**What I did:**

1. **Reproduced** (regen.sh, clean tree, patch self-applied, ran twice incl. runner's): all five flights match the dossier — 86.2/215.2/684.9/85.4/191.8 ms fleet-class (author's seed-7 timings were load-inflated, counts exact); dissolution 768/768 at seed 1 m=768; seed 7 dissolves at 192; slices member-flat 21.9→22.9 µs (m≤192); quotes 5/5 byte-identical. All five code claims verified in source (extent rule `r_p/32` + scale-free epochs at frame.rs:34-37/80-82 with unit test; one-fleet assert :513; player loop :733; deadline cap :787; `Fleet::new` takes any doll).

2. **Attacked beyond the author's range:**
   - **Seed 3** (never tuned): structure reproduces, no dissolution at 192. Found the leaver's ship-class life exceeds the fleet class at m≥192 (725 vs 199 ms) — the 0.89 µs rate excludes it.
   - **m=3,072** (author's attempt died on a relative path — I hit the identical error; CARGO_TARGET_DIR is elsewhere): completes bounded (0.67 GB), total ×72.7 for ×64 members (exponent 1.05 — P1's predicted band 0.8–1.2 actually *holds* there; the author reported the decay-confounded 0.65). Cost ≈ 1,515 leavers × ~4 ms hand-out storm — the extent gate refusing, not the carrier carrying.
   - **m=6,144** (the author's declared but unflown held-out case): completes at 1.9 GB, exponent 0.72, no quadratic onset.

3. **Found two instrument defects** (corrected on the page, neither touching the finding): the bench's presented-time collapse at m≥768 (m=3,072 presents 20.9 of 2,000 nominal game-s) makes the nominal normalization — and the first checker's "0.22 µs / all-battle 2.2×10² cores" — artifacts; honest rates are 96/30 µs, still under P2's own 100 µs kill bar, and the all-battle bound is packing-dependent (~9×10² cores at Armada packing, under the row). Also: the batch-scan term was 10³ high (favorable), "reproduces every count" overstates (m=48 flips dissolved 0→1), and the "L4/L5 quarter outside" clause is asserted, not measured.

4. **Novelty/goal fit:** cf2a priced *finders* and concluded "no cheaper finder closes it" — this run's answer is *no finder*: the carrier question, left unpriced at 10⁹, prices at ~0.15 cores quiet maintenance against 4,510 (≥4,500×, board bottleneck #2's dominant row), deleting the designed rank-certificate finder. PRINCIPLES 4 (dimensionless gate) and 26 apply verbatim. Gold rather than silver because the deleted requirement doesn't wait on the unflown doll-0 joint: even with zero period discount the carrier beats the row ~5×.
