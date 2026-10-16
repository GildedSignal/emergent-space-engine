Grade: silver

**Abstract.** Checker 2's named gold experiment, flown: the player-neighbourhood scan's candidates shared behind an `Arc` whenever every entry is `same()`, so the mint is one snapshot per candidate-set change, not per player binding change. Independently reproduced: the record's fenced 10⁵ burn arm completes 720 frames at 307 MB with `mints=1` (my ship side re-fenced at 1,913 MB mid-burn); A/B digests equal (10⁴ word `73972744`, 10⁵ quiet `c459ac4b`, cure digest `36f8e1a4` a third time); the held-out 10⁵ answer bill 0.38–0.39 s/distinct scan. Beyond the author's domain: identity and the mint law hold across ~18k game-s (19 mints / 931 shares) and at 3×10⁵ (840 MB, no fence). Silver only because the derived per-frame ratios are kB-as-B arithmetic slips (~10³× overstated; honest: ≤ ~12 kB/frame, ~10²–10³×, 971:1 by count) and the page's conflict resolution deleted two runs' append-only lines. Adoption: ~40 lines in `encounter.rs`; d7bc's fence can retire.

## Reproduced (clean tree, `git apply work/patch.diff`, one build)

- **10⁵ quiet A/B:** ship = cure = `c459ac4b…`, `mints=0` both sides (the robust 10⁵ identity pair).
- **10⁴ word budget-free A/B:** ship = cure = `73972744…` (= the record's own digest), 324 mints vs **1 mint + 323 shares**.
- **The fence-killer (10⁵, budget-on 12 ms):** ship `fenced=true`, 1,913 MB, dead mid-burn (75 held) — the record's ruin class; cure **completes 720 frames, 307 MB, mints=1, shares=303**, flush 116.6 s for 606 held / 304 distinct scans = **0.384 s/distinct** (dossier: 0.38–0.39), digest `36f8e1a4…` identical to the dossier's twice-reported value.
- Runner's regen: exit 0, all arms, 14 `ladder_digest` rows including all 10 record digests — bit-identical with the cure compiled in.
- Lib+bins tests: 10/10 on the patched tree. (Full `cargo test -p emergent-universe` does not *link* on Linux — `proc_pid_rusage` in the pre-existing `nladder` example is ungated macOS-only; pristine behaves the same, so not this run's defect, but "crate tests pass" is true only of the test targets.)
- `predictions.md` (02:36:50) predates every decisive-arm raw (02:39+); tuned on the 10³ smoke only, as it says. The author scores their own misses honestly (#3 denominator, #4 2× over).

## Adversarial (my own; both outside the author's tested range)

1. **The author's named unflown "natural next flight" — a multi-snapshot arm.** 10³ held burn at rtf 400 × 45 s ≈ 18k game-s, past the belt's ~13.5k re-key window (`frame_to` advances `rtf × wall_dt` game-s per frame — the probe's "game 6.7 s" line is a `hold_every=1` artifact, `late_stats` overwritten per frame). Result: A/B digest **equal** (`82ab4840…`), cure **19 mints / 931 shares** vs ship 950 mints. The mint law is confirmed as *per candidate-set change* — and candidate sets do change at depth, so "mints=1" is arm-scoped, exactly as the run scoped it. Identity survives the first re-key-while-burning boundary.
2. **N = 3×10⁵** (the record's checker fenced the ship there at 34 scans): cure `mints=1`, peak 840 MB (build 705 + one ~34 MB snapshot + backlog), no fence, 36 s wall. The mint law has no N-dependent term, as claimed.
3. **The derived per-frame ratios are wrong by ~10³.** Dossier: "(309−237−11.3)/659 ≈ 92 B/frame" — 60.7 MB/659 = 92 **kB**/frame; "(59−27−11.1)/2699 ≈ 7.8 B/frame" — kB again. The raw RSS curves: 10⁵ tail 305→308 MB over frames 420–690 ≈ **11 kB/frame** (the dossier's own headline "≤ 12 kB/frame amortized" is the honest one); 10⁴ tail flat at 59 MB. Honest multipliers: ~10²–10³× on matched RSS slopes (ship 6.1–10.4 MB/frame), 971:1 by count, unbounded in principle. The page's "steady-state ≤ ~7 B/frame (~9×10⁵×)" repeated the slip as the headline ratio. Corrected in place on the page.

## Novelty

`git log` on `crates/universe/src/encounter.rs`: the shipped seam history (916e1e9e held scans, 72b71c56 repeat, 0f112b89 radial index) never shared candidates; the pristine `Scan.candidates` is a fresh `Vec` per scan (line 195). The record (20261016-0117-taleb-51b7) priced the ruin and its checker 2 named this exact experiment; this run flies it for the first time, plus the first direct measurement of the 10⁵ answer bill (correcting encounters.md's µs/body by 2×). Not a repetition.

## Goal fit

Board #1 (bodies 28 → 10⁹): deletes the player-seam memory ruin instead of fencing it, ~40 lines, answers bit-identical, adoptable in one step. PRINCIPLES #3 "Compute only surprises" (a per-binding-change copy of an unchanged candidate set is the anti-surprise) and #19 "a fix signals the wrong representation" (the rung retires the representation error; d7bc's byte-cap bandaid can follow it out). The capture walk and the answer bill are correctly left to the candidate-set certificate.

## Why silver, not gold

The physics is gold-grade and every load-independent number regenerates, but the dossier's and page's derived per-frame multipliers ("~7 B/frame", "~92 B/frame", "~9×10⁵×", "~10⁵×") are contradicted by the run's own logs by ~10³ — a headline the log contradicts — and were not disclosed by the author. Also the page overstated identity by listing the schedule-fragile 10⁵ word pair among the "digests equal" arms (the dossier itself demotes it to a witness).

**The one step to gold:** re-issue the derived ratios from the RSS curves in honest units (≤ ~12 kB/frame amortized, ~10²–10³× by slope, 971:1 by count) and fold in a multi-snapshot arm (mine: 10³ × 18k game-s, 19 mints/931 shares, A/B-equal — 12 s of compute) so "one snapshot per candidate-set change" carries its depth measurement in the record. No new mechanism is needed; the cure itself is adoption-ready.

## What the author missed

- The kB-as-B slip (above) — in both the dossier's derivation and the page's headline.
- The page's conflict resolution was destructive: it deleted the append-only Runs lines of `20261016-0117-library-cfe5` and `20261016-0117-second-20261016-0023-scout-d86c` (restored by me) and dropped both runs' standing current-best paragraphs while leaving the page with **two copies** of `## Refuted`/`## Open directions`/`## Contradictions` and current-best paragraphs stranded inside the first Contradictions section. The three-way conflict on the page is the integrator's to adjudicate; the next publish must carry all arms' standing content.
- The page listed the 10⁵ word pair as an identity equal (corrected in place).
- "Crate tests pass" silently excludes the examples, which do not build on Linux (`proc_pid_rusage`, pre-existing); worth naming so the next author is not surprised.
- Minor: the shipped per-mint marginal RSS is not a stable 113 B/body — my ship run hit ~22 MB/held (2× the record's 11.3) at the same N; treat it as an order anchor. The record's checker already saw 118.6 B/body at 3×10⁵.

Page note: `wiki/nladder.md` corrected in place (ratios, identity-arm list, checker bracket, restored Runs lines); the duplicated-section structure and the dropped current-best paragraphs are left for the integrator's merge adjudication. Topic stays open — this is the topic's first checker-verified run at this seam, no closure.
