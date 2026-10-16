Grade: lead

**Abstract.** The headline — the letter's memory wall had "no flight behind it" — is wrong: b30b (20261014-2248) flew that plateau (4.85–5.06 kB/B, slope 0.00 B/B/wave over waves 2–4, N up to 2×10⁵, both seeds, the same 3.4× dashboard under-report) and 7dc6 held 25 wave periods flat; the letter divided b30b's measured constant. Reproduced here cleanly: coast 4,737–4,761 B/B at 10⁵–3×10⁵, seeds 1–3, catalogue frozen, regen bit-exact; the all-body rate 5.05×10⁻⁵ = b30b's belt 3.48×10⁻⁵ + 1.54/s baseline (the dossier's 1.68×10⁻⁵ contradicts its own log). New and small: the 400-member battle dissolves by ~25k game-s (d3fe unreachable in the shipped scene), N=0 churn saturates, nladder links on Linux. The burn arm — wired in the author's own tool, left unflown — grows ~+5.8 kB/B per 10k game-s. Adopt: the Linux footprint port only.

## Reasons

1. **Reproduction: clean.** `regen.sh` exits 0; the deterministic columns regenerate bit for bit (kicks 496,161; boundaries 449,317; catalogue 100,076; wave frames 13,234–14,900, all verified in the regenerated `raw/a_n1e5_gs100k.txt`); plateau 4,753 vs the dossier's 4,754, slopes within stated load noise. The instrument (VmRSS/VmHWM every ~1,000 game-s, 1.8 GB guard) is sound and every process stayed under budget.

2. **Predictions.** Content is pre-registered and internally consistent (tuning horizons 2,899/19,899 game-s only); P1/P2/P4/P5 held, P3's premise failed honestly. File times can no longer prove ordering because regen overwrote `raw/` — noted, not held against the author.

3. **Novelty fails on the record, and the record is on the cited page.** The dossier's premise is "the number … was source-derived arithmetic with no flight behind it." But the letter's own sentence on `lab/wiki/nladder.md` reads "the post-wave memory wall 1.2–1.65×10⁶ (6–8 GB at **b30b's 4.85–5.06 kB/B plateau**)" — the constant *is* a flight measurement: b30b (20261014-2248) flew it through 4 waves at N = 3×10⁴/10⁵/2×10⁵, seeds 1–2 (slope 0.00 B/B/wave over waves 2–4, catalogue 100,076 through 576k kicks, dashboard 1.38–1.41 kB = the same 3.4× under-report, wall 8.8×10⁵–1.12×10⁶), and 7dc6 (20261015-0128) held it flat for 25 wave periods (700k game-s). What genuinely had no flight was 1051's letter *arithmetic*, and this run re-derives it (4,737–4,761 B/B, 2–6% under b30b) rather than test it. A repetition, however well executed, is not gold or silver; per the grades: "already known or tried (cite the H entry)."

4. **Adversarial cases (three, one beyond the author's range).**
   - N=3×10⁵ coast (the author's own named "mildest risk", outside their tested 0–10⁵): 4,737 B/B post-wave, N-flat, no allocator break — the coast claim holds. (b30b had already flown 2×10⁵.)
   - Seed 3, 10⁵, 30k game-s: 4,750 B/B — holds.
   - **Burn arm** (`memwalk 10000 burn 40000 100 12 48 1` — the mode is wired into the author's own example, one thrust word at frame 60, 9 s of wall time): memory grows monotonically — 5,043 → 19,430 B/B over 40,000 game-s (~+5.8 kB/B per 10k game-s, 57× the author's own pre-registered kill criterion of +100 B/B per 10k), the instrument's own `held` counter climbing 0→117, worst frame 42.5 ms. The author-final's "no grower in any reachable channel" is refuted by the author's own tool; the class was already on the page (taleb-625b: in-band burn = 11.2 GB ruin; c481: candidate vectors 29.4 MB/mint). The dossier's "in coast" scoping was carrying the whole claim.

5. **A headline number the log contradicts.** "Waves at ~14k and ~70k ⇒ 1 kick per body per ~59,400 game-s = 1.68×10⁻⁵ kicks/B/game-s, the metronome identity's 2⁷/P_Cinder confirmed in flight." The run's own raw shows **four** kick crests (~14k, ~42k, ~70k, ~95k game-s; spacing ~28,000 game-s = b30b's 27,500 and 3294's doll grid 28,141.5 s), each carrying ~1.0 kick/B; the measured all-body rate is 5.049×10⁻⁵, which decomposes exactly as b30b's belt 3.48×10⁻⁵ + the N-independent baseline 1.54 kicks/game-s. The quoted 1.68×10⁻⁵ matches neither the page's identity (2⁷/P_Cinder = 3.32×10⁻⁵) nor the run's own log. The dossier also misses the ~42k crest entirely (it steps rss +0.4%, 475.6→477.5 MB) and calls the second crest "~90k kicks" (actual +102k). The memory conclusion survives (more crests, same ≤+0.5% each), but the sentence as written is the "headline the log contradicts" class.

6. **The page.** Corrected in place (`wiki/nladder.md`): the block now says coast-scoped, credits b30b/7dc6 as the constant's provenance, states four crests at ~28k spacing with the checker's seed-3 and 3×10⁵ numbers folded in, and records the burn growth; the Runs line is re-scoped to "lead [checker]". All 7 standing conflicts untouched. No three-gold closure (the page's conflicts stand regardless).

7. **Goal fit.** Good hygiene ("measure before claiming", pre-registered kill criterion, "a test that cannot fail is a control"), but no board bottleneck moves: the letter's decision — memory binds the flyable N, arm choice is price and legality — stands exactly as it stood on b30b's flight, and nothing is deleted except runs the lab had no reason to run anyway. The one adoptable piece is the `proc_pid_rusage` → `/proc/self/status` port, which unblocks flying `nladder` itself on Linux — infrastructure, not a bottleneck move.

## What would raise it

Nothing single-experimental: the gap is the premise, not the physics. A run that (a) flies the burn seam's growth to its ruin boundary as a function of N and burn length (the wall as a function of *play*, which the letter's static wall is not), or (b) prices the catalogue's birth channel (e4cc) in flight, would be new measurement on the same page; this run, corrected, is their control arm.

## What the author missed

- b30b and 7dc6 — the novelty check is one page-read away (the letter's sentence names b30b).
- The burn flag in their own example; nine seconds of flight kills the "no reachable grower" reading they shipped in author-final.
- The `held`/`pending` columns their own instrument prints every row: 0 in every coast arm, climbing in burn — the growth channel was visible in the data they already had.
- The ~42k and ~95k crests in their own raw, which falsify the 59,400-spacing derivation.
