Grade: lead

# Check — 20261015-2041-fermi-99b5

**Abstract.** The claim "the belt's kick cadence is 1.9e-4/body/game-s, 5.4× the wiki's doll-interval law" is refuted: that number is the 10⁴ scene average, ~82% of whose kicks come from the fixed 328 near-Home/plane bodies. 3294's census on this very scene measured the belt's own interval at 28,141.5 s median (3.64e-5, = cf45's law) and published the same 1.90e-4 all-bodies counter *with* this decomposition; my unthrottled flights give 1.54e-3 / 1.93e-4 / 5.69e-5 at 10³/10⁴/10⁵ (10⁵ at rtf 900: p50 3.3 ms, unthrottled) — the fixed-locals signature, not an N-flat law. The throttle story, the 0757 "understates 4.8–60×" correction and "CPU-bound at 1.1×" all invert; at the true cadence 0757's 0.15 cores was right. Only the already-known result survives (record stack binds 10⁹ memory, 163×). Nothing to adopt.

## Reasons

**1. Reproduction (partial).** regen.sh exits 0. The 10⁴ anchors regenerate: depth-differenced rate 1.926e-4 (dossier 1.93e-4), birth 2,456–2,465 B/body, dashboard 1,352–1,437, catalogue N+76, p50 3.7–3.8 ms. The 10⁵ numbers do **not** regenerate: dossier "2.69e-5 = 14% delivered, held_max 67→2,048, growth 0.086 B/body/game-s" against regen 4.94e-5 = 25.6%, held_max 146→157, growth 0.021 (shared-box noise; direction only). regen.sh also overwrites the author's raw `work/*.txt`, so the original 10⁵ numbers are no longer auditable — freeze originals (the same lesson as 0757's checker).

**2. The headline is wrong, three independent ways.**
- *3294's census, same scene, same counter* (10⁴ coast rtf 1500, 82.5k game-s, branch `claude/lab-20261015-0724-system-3294`, evidence 2 and 4): belt median interval **28,141.5 s** (p1 26,750, p99 28,949) = 3.64e-5/body/game-s, "cf45's 2.814e4 s exactly"; "348 near-Home bodies (3.5% of all) take 81% of all fire events: ~361 fires each … against the belt's 3"; and "the ladder's own counter agrees: **1.902e-4 over all bodies incl. near-Home**." The author's 1.926e-4 is a rediscovery of 3294's number minus its decomposition. The kick-cadence wiki page the author cites carries the 28,141.5 s figure in its current best.
- *My flights* (author's frozen binary, rtf 900, shallow+deep, depth-differenced): 10³ = **1.543e-3**, 10⁴ = 1.926e-4 (regen), 10⁵ = **5.691e-5** with p50 2.3–3.3 ms and 0/7 frames over — unthrottled. An N-flat 1.93e-4 law misses 10³ by 8× and 10⁵ by 3.4×; one model — belt 3.55e-5 plus 328 locals at λ≈4.8–5.7e-3/game-s — fits all three rungs (implied λ 4.75/4.81/6.53e-3).
- *The author's own 10⁵ shallow arm*: 1.715e-5 with the belt silent (first wave at 13k game-s) = 300×5.7e-3/100,028, locals alone. Their "shallow ≈ deep" (P2) holds only at 10⁴, where locals(~82%) + belt happen to sum near the birth-window rate; at 10⁵ their own shallow/deep differ by 2.6×.

**3. The derived claims fall with it.**
- *Throttle:* at rtf 900 the 10⁵ rung delivers 5.69e-5 ≈ the true cadence (locals 1.7e-5 + the first belt wave) unthrottled; the rtf-3000 arm's 4.94e-5 is ~90–100% of truth, not 14–26% of 1.93e-4. The "predicted 17%" was circular (own-law × the scoreboard's 75 µs; at the c01c 43 µs the author themselves cite, 10⁵/rtf3000 needs 0.65 cores — no throttle). ladder.txt's 10⁵ 1.9e-5 is a 20-s-window artifact (belt's first wave at 13,051–14,534 game-s), not a budget reading.
- *Mis-citation:* ladder.txt's 10³ coast kick/b/gs is **1.86e-3**, not the "1.86e-4" in the dossier table and compose.py — and it is locals-dominated (the 1/N fall ladder.txt itself explains), so it never was evidence for the law.
- *10⁹ composition:* at 3.55e-5 — kicks 1.53 cores (c01c), re-mints **0.131 cores cap'd** ≈ 0757's "~0.15" (their "understates 4.8×/60×" inverts; 0757 was right), CPU 1.66 cores = 0.21× the M1 (not "1.13×, CPU-bound"), memory 163× unchanged, now binding ~780× harder than CPU. The author's pre-registered P4 bands (kicks ≤4, re-mints 0.1–0.3, memory ≥25× harder) would have *held* under cf45's constant — the arithmetic was fine; the one home-grown constant broke it.

**4. Novelty.** What survives is already on record: effb composed the 10⁹ ledger (cadence 2⁷/P, corrected 24× by cf45); 760f — "the wall is the record stack; 10⁹ lives in programs"; quant-0619 — the 1.4 TB burn knee; d6ba's checker — "~1 kB/body×10⁹ = 1 TB … the record stack is the term". The memory anchors reproduce but confirm 8b89. The one reusable instrument note — per-body averages over a scene with a fixed local population are not a per-body law; read cadence from the census (3294) or from N-scaling — is exactly what 3294's parenthetical already said.

**5. Predictions.** predictions.md predates the dossier (mtimes consistent; the author's flights are unverifiable after regen's overwrite). P1 "failed interestingly" was in fact the truth trying to surface: the belt *is* at 3.55e-5; the instrument (all-bodies average at the one rung where the mix coincides with the birth rate) could not test P1 at all. Honest reporting of the failures; wrong diagnosis of the cause.

**6. Goal fit.** The board's #1 item is bodies toward 10⁹; a corrected ledger matters — but this run's ledger is the fourth pass (effb → cf45 → d6ba-checker → here) and the first to move the constants backward. "Measure before claiming" was honored in megabytes and violated in the one constant the composition hinged on: the belt/local split was measurable with one extra flight at another N, and was already published.

**Page.** I corrected `wiki/n9-ledger.md` in place: the proposed current best and refuted-entries would have planted a wrong cadence law, a wrong refutation of cf45 and a wrong correction of 0757 on a new topic page.

## What the author missed

- 3294's census evidence 2+4 (on the cited wiki page's own run line): the 28,141.5 s belt interval and the 81%-of-fires locals — the discriminator was already in the building.
- N-scaling as the falsifier: any second unthrottled rung (I used 10³ and 10⁵/rtf900) exposes the fixed-locals signature in one flight each.
- Their own 10⁵ shallow arm (1.715e-5, belt provably silent) already contained the locals' rate; and "shallow ≈ deep" fails on their own 10⁵ data.
- The 10³ row of ladder.txt was misread by 10× (1.86e-3 → "1.86e-4").
- regen.sh overwrites the author's raw evidence; freeze originals before the box does.
