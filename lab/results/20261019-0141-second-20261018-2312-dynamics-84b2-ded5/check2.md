Grade: gold

**Abstract.** Claim: the checker-named gold experiment (n = 12800 at horizon ∝ side,
24576) is flown — the genesis ringdown is extinct (blocks 404-421 → all-≤6 from blocks
5-7, t 10240-14336; tail 0.9-3.6 = anti-bunched baseline; late-m 0.28-0.43%), the
checker's 3.43% whole-run m was a fixed-window artifact (same series: 3.43 → 2.85 →
2.04%), the n-invariant steady-state instrument is late-window F64 (= mean64·m², flat
1.1-2.6 across n = 400-12800), and the stale record cells are fixed to the regenerated
numbers. Reproduced exactly with independent code: every table cell, bit-identity of six
arms against 84b2's committed data and of the 12800 seed-1 series against the original
checker's arm through all 9216 ticks; the binary rebuilt from 84b2's patch source is
byte-identical. Adversarial (mine): fresh seeds 7 (12800, onset block 5) and 11 (6400 at
H16384: F64_late 4.96 → 2.88 — the "6400 tell" is flown, not inferred); 25600 partial
decays to all-≤6 at t 18432, inside the dossier's predicted 18-30k band. Adoption: zero
code; the no-batch-shaping deletion holds to n = 12800 flown (25600 partial); measure
steady-state modulation as late-window F64 from ≥ 2× the ringdown onset, never whole-run
m or raw Fano.

**Reasons.**
1. **Reproduction: exact, three ways.** My own analyzer (independent of summary2.py)
   recomputes every dossier cell: the 12-block series on three seeds, m@8192/12288/24576
   (3.43/3.37/3.54 → 2.85/2.79/2.94 → 2.04/2.00/2.10%), m_late4k 0.28-0.43%, F64_late
   1.12-2.64, allocator ratios (p99/p50 whole 1.093-1.099, late 1.044-1.045; late
   max/p50 1.009-1.013), the corrected 6400 row (F64 38.18/39.05/43.77, m 2.35-2.52%,
   blocks [117.2, 19.5, 7.3, 2.7]) and poly_r (17.26 / 2.26% / 33798, late F64_late
   7.06), and the identity F64 = mean64·m² at every truncation. Bit-identity: all six
   regenerated small arms diff-clean against 84b2's committed data; ext_n12800_s1 is
   line-identical to 84b2's checker arm a_n12800_s1.csv through their last tick 9216.
   The genesis mirror in breathe.rs matches shipped worlds::gas line for line (same
   Rng(seed^n^0x6A5), same call order); I rebuilt the example from 84b2's committed
   patch at base 52db369f in the warm target dir and the output is byte-identical —
   the prebuilt binary is the patch's. Crates byte-identical 8d9e7f88→52db369f
   (verified: empty diff).
2. **Held-out.** predictions.md (01:47:32) predates the decisive launch (launch.sh
   01:54:22) and the dossier (02:17:03). Kill lines were stated and none fired: P1 held
   (no plateau; last blocks ≤ 3.6 « 8), P3/P5 held, P2 held on seeds 2-3 with seed 1
   disclosed half a block past the band (14336 vs 13500), P4's direction held with the
   point estimate missed (2.0-2.1% vs ≤ 1.6%; kill at ≥ 2.4% not fired) — reported as
   the instrument lesson (whole-run m never converges to the steady state: block 0's
   F64 ≈ 405 lifts whole-run F64 ~22-50× over baseline). An honest, explained miss of a
   point value whose falsifier survived — not the 84b2 situation where the registered
   mechanism itself died.
3. **Adversarial (outside the author's domain, my own arms, my own seeds).** (a) n =
   12800 seed 7, H 12288: blocks [368.7, 92.0, 51.9, 19.4, 13.4, 5.8] — the decay law
   and onset block 5 reproduce on a fifth seed; m@8192 3.24%, in band. (b) n = 6400
   seed 11 flown to H 16384: blocks [106.8, 21.1, 4.6, 3.9, 2.0, 2.6, 3.6, 2.1] and
   F64_late 2.88 (vs 4.96-5.15 at H 8192) — the dossier's "the 6400 row still smuggles
   ringdown" explanation is now flown on two fresh seeds (mine + the run's chk2 seed 1,
   which I recomputed: 2.87). (c) The next octave, n = 25600: my H-8192 arm's blocks
   [887, 451, 238, 119] are identical to the chk2 partial arm's first four (same seed,
   prefix determinism), which runs to [.. 11.7, 8.0, 4.3] — all-≤6 at t 18432, inside
   the dossier's pre-stated prediction (extinction 18-30k, F64_late 1-3 with one
   post-extinction block so far); m@8192 3.86% shows the fixed-window artifact keeps
   growing with the box exactly as the artifact reading requires, while the tail decays
   — coherence is not growing. Onset ratio at the new octave 1.29-1.80 vs side 1.41:
   the super-linear hint was scatter, as the dossier itself allowed.
4. **Novelty.** The live chaos-shadowing page's own open direction was "fly n ≥ 12800
   at horizon ∝ side before quoting an m"; no HISTORY entry covers it. This run answers
   it and corrects the record cells the 84b2 checker flagged. The F64_late instrument
   (raw late-m rides a 1/√mean64 counting floor: 2.38% at n = 400 → 0.74% at 3200 with
   F64_late flat 1.95-2.31) is new and is the right tool for the still-open coherent-
   fleet half.
5. **The page.** The proposed wiki/chaos-shadowing.md is faithful: every number in the
   new block matches the evidence; the prior 84b2 block is demoted, not reworded; the
   Runs list is append-only; open directions fold the flown result in. The in-place
   adversarial insert (chk2 numbers) recomputes exactly under my analyzer.
6. **Goal fit.** Board #4 (smoothness/allocator): deletes a feared N-dependent
   allocator margin (batch-shaping/dephasing machinery) for thermal dense scenes across
   32× in n, at zero code cost — "the cheapest compute is compute not done"; kill lines
   before the runs honour "a test that cannot fail is a control"; the miss is reported,
   not buried. Domain honestly bounded: one genesis family (thermal touching lattice,
   fill 0.7, β ≤ 0.09); the coherent-fleet half stays open on the page.

**Defects (none grade-bearing).** (i) This run's work/patch.diff is empty while the
dossier cites "harness … via work/patch.diff": the harness source is 84b2's committed
patch, so a cold machine cannot rebuild the binary from this folder alone (regen.sh
relies on the prebuilt lab-target binary; its header does name the patch and base, and
I verified the rebuild is byte-identical). Already flagged on the page. (ii) The
predictions P1 parenthetical "last-3 blocks 1.2-2.7" omits seed 1's block-11 = 3.6 —
cosmetic; the kill line (all ≥ 8) is nowhere near. (iii) "onset 1.7-2.5×" quotes
same-order seed pairings (worst/worst would read 3.5); the next octave shows scatter —
the dossier's own caveat covers it.

**What the author missed.** The 25600 F64_late reading (one post-extinction block in
the chk2 partial; my arm stops at H 8192) is the only cell of the scale-free table not
yet flown to two post-extinction blocks — the next run can close it in ~40 min/arm.
The absolute genesis batch cost (max_batch = n at scene start) remains unpriced on this
surface; the ringdown being self-extinguishing makes that startup spike, not the steady
state, the allocator's real dense-scene question.
