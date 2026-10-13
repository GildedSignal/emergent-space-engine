Working...
**Grade: gold** — written to `lab/results/20261013-2252-components-be78/check2.md`, tree restored, author's page corrected in place.

**What the run claims:** the hand-out's fit-again retry (40–62% of hand-outs compiling their member's tube twice) is deleted by deriving the integer word from the state's turning key before the bind — env-gated `ES_WORD_FIRST`, ~40 lines, no map.

**Reproduced (patch self-applied, clean tree):**
- m1500-s3 and m8000-s3: digests `7b33d0b866149e71` / `79ec315d7e51f6b5` equal off/on and equal to the author's stored JSONs bit for bit; counts identical (205/121, 6,099/3,200 → 0 retries); bind −42% both.
- Every table count re-derived from her JSONs; aggregates across three passes 531→352, 538→360, 519→343 µs — the µs wobble she disclosed, the equalities never moved. The off2 wobble control verifies (presented 101.3M vs 90.9M ticks between two *shipped* runs, digest `540ec08d…` ×3).
- `predictions.md` timestamps are clean: after the disclosed tuning run, before every held-out run. P1/P2/P7 held everywhere; P3/P4/P6 missed at band edges and were disclosed as misses.

**Attacks, all outside her domain — all held:** 16,000 members (2× her max: 13,729 hand-outs, 7,192→0 retries, digest identical, RSS 391 MB); m400 at rtf 400 (4× deeper collapse, all members handed out: 253→0, digest identical); seed 11 (99→0); and the universe suite green with the probe **forced on**. The named soundness hole never fired in 23,711 hand-outs plus the suite. I also verified the identity structurally in source: `Passage::compile` stores its `outer_radius` argument verbatim, and `word_of_key` is token-identical to `word_for`'s arithmetic.

**Novelty:** quant-7055's page named "choose the word before the first bind" as the remaining lever; this run builds and measures it — a new current best closing that direction, and the memo proposal dies with the retry.

**Corrections:** the page (and dossier) said "8,908 hand-outs"; both passes count **9,395** — fixed on the page, noted in check2.md. Gold bar met via the deletion clause: a shipped component removed, adoptable in one step (inline the choice in `from_state`, delete the retry branch), gain 1.4–1.6× on the promotion stream.
