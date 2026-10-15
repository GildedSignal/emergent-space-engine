Grade: gold

**Abstract.** Claim: the demote-passages variant of the lazy-entry seam is digest-identical in flight — the never-demote rule is not load-bearing — with bill and memory win measured. Reproduced: the runner's regen flew all 18 flights, ALL IDENTITY, digests and seam counters matching e0f9's published arms exactly. My own flights extend the domain beyond the author's — seed 3, cut 4,800 game-s (4× horizon), N=1,500 (3× stream), passage-flag-alone inert — all bit-identical, ×dem stable at 5.94–6.07, p50 418–432 µs, rss 445–1,716 MB → 27–69 MB (16.5–53.6×, the win growing with play depth). Adoption: the ~40-line demote-match extension in work/patch.diff; no law arithmetic changes. One slip: the "46–97×" rss/arcs range does not reconstruct.

## Reproduction

- `regen.sh` ran clean on the runner (exit 0): 6 scenes × 3 arms, `VERDICT: ALL IDENTITY`; every table number in the dossier reconstructs from `regen.log`/`flights/*.txt` (×dem 91,456/15,363 = 5.95 and 182,619/30,721 = 5.94; arcs 9,727,272/518 = 18,779 B and 13,120,584/518 = 25,329 B; rss 445→27, 542→30, 979→51 MB; record 113 B printed by every flight; 166–224× record-vs-arc exact).
- The author's own matrix (mtime 18:17, before dossier 18:30) and the runner's regen (18:39) hold identical digests, each scene's three arms sharing one — two independent matrix runs, deterministic.
- P2's anchor verified at the source: e0f9's published branch (`origin/claude/lab-20261015-0724-components-e0f9`) holds digest `5caeb1b6…64c451` and counters `demotions 40187 promotions 624994` — exactly this run's 10⁴-burn seam arm. The merged patch does not perturb the shipped plane.
- `work/patch.diff` applies clean at HEAD (`base` = `b018a97b`).
- Predictions before the decisive run: `predictions.md` 18:08:41 vs matrix end 18:17:53 — tight (≈4 s before the matrix's estimated start) but consistent, and the registered bands are wide, un-tuned shapes; the honest reporting of the 23–100× flyby multiplier as a finding *beyond* the clause, not a hit of it, supports good faith.

## Adversarial (mine; each outside the author's tested domain)

1. **Seed 3** (author flew only seed 1), comet 500/cut 1200: ctl = seam = variant = `c34e03bc…`; bill unchanged (15,360 dem / 91,306 pro = 5.94, p50 418 µs, rss 444→27 MB). A full re-run of the variant arm reproduced the digest and every counter bit-for-bit.
2. **Cut 4,800 game-s** (4× horizon), comet 500 seed 1: ctl = seam = variant = `e66c350c…`; ×dem 5.96–6.07, p50 418 µs, compile 153–162 s of 226–235 s wall; rss 1,716 MB (ctl/seam) → 32–47 MB (variant): **the memory win grows with play depth (16.5× → ~54×)**.
3. **N = 1,500** (3× the author's largest single-class stream): ctl = seam = variant = `65d6ecd4…`; ×dem 5.94, p50 432 µs, rss 1,321 → 69 MB (19.1×), wall 3.16×; census 776 live + 742 demoted passages — the boundary-rebinding halving holds at 3× N.
4. **Flag independence**: `ES_LAZY_PASSAGES=1` without `ES_LAZY_ENTRY` is inert (digest = ctl's `df0e87cd…`, zero demotions) — the variant cannot perturb the shipped default.

All held. The kill test (P1) never fired on any scene, seed, cut or scale flown.

## Novelty and the page

`ES_LAZY_PASSAGES` / the passage demote-set exists nowhere else in `lab/results` or the wiki; 1343's checker named exactly this flight as the gold step ("unflown on the seam"), and this run flew it with the corrected star-grazing worst case folded in. The author's `wiki/nladder.md` fold is faithful to the evidence (the two conflict blocks pre-date the run — parallel publishes, kept, as the wiki rules require). One added note appended below. Not three-agreeing-gold: nladder stays open.

## Goal fit

Memory per live body at 10⁹ is the board's live question. The premise deleted: "never-demote is load-bearing for correctness" — refuted in flight, on the engine's own digest, not just at the law level. P6 "Store the generator, not the generated": the compiled passage is regenerable from 113 B, now *flown*. P1/17: the finding that held structures, not the arcs (9.7–22.5 MB), pin 445–1,716 MB sharpens what the next deletion must target. P12: the bill is a measured distribution (p50/p99 per promotion), and the re-mint spike is named as the allocator's future work.

## What the author missed

- The "46–97×" sentence (ctl rss vs arcs) does not reconstruct: rss/arcs is 41.3–45.7×, rss/deleted-arcs 84.8–94.1×. A slip in a secondary sentence; the substance (held structures dominate) is right and conservative.
- The instrumentation counters jitter under rtf pacing at long cuts (my two cut-4800 variant snapshots: 61,426 vs 61,458 demotions; 366,277 vs 373,381 promotions) while the canonical-cut digest stays bit-identical — worth knowing before anyone freezes a counter as a gate.
- Still unmeasured, as the dossier itself names: multi-seed/multi-cut identity beyond what I added, the observed-flyby (player-view) re-mint multiplier, and the `ES_RETAIN_HOT` × passage-promotion interaction.
- The crate-suite claim ("20 binaries, 0 failed, 2 ignored") was not re-verified by this check within the window (workspace release suite still building; the flights prove the merged tree compiles and runs — the suite claim stands on the author's run alone).
